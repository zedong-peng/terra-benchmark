from pathlib import Path
import json
import sys

import jsonschema
import yaml

from benchmark.spec_data import (
    SCORING,
    TSS_WEIGHTS,
    TSS_DENOMINATOR,
    CLI_NUMERATOR_TASKS,
    CLI_DENOMINATOR_TASKS,
    TERRA_VERSION,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def schema(name):
    return load_json(SCHEMAS / name)


def validate_json(instance, schema_name):
    jsonschema.validate(instance=instance, schema=schema(schema_name))


def load_trial_metrics(trial_log_path):
    metrics = None
    with open(trial_log_path, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            if entry.get("event") == "trial_summary":
                metrics = entry["metrics"]
    if metrics is None:
        raise ValueError(f"No trial_summary event found in {trial_log_path}")
    return metrics


def compute_task_score(metrics):
    success = float(metrics["success"])
    contacts = min(float(metrics["extra_support_contacts"]) / 4.0, 1.0)
    recovery = min(float(metrics["recovery_steps"]) / 6.0, 1.0)
    energy_val = float(metrics["energy_proxy"])
    # energy_proxy == -1.0 means unavailable; skip the energy penalty
    if energy_val < 0:
        energy = 0.0
    else:
        energy = min(energy_val, 1.0)
    raw = success * (1.0 - SCORING["alpha"] * contacts - SCORING["beta"] * recovery - SCORING["gamma"] * energy)
    return round(max(raw, 0.0), 4)


def compute_tss(task_scores):
    """
    Compute TERRA Standard Score from a dict of {task_id: task_score}.
    Requires at least the tasks present in TSS_WEIGHTS. Missing tasks are skipped
    (partial TSS is computed over available tasks, scaled proportionally).

    Returns (tss, available_tasks, missing_tasks).
    """
    weighted_sum = 0.0
    available_weight = 0.0
    available_tasks = []
    missing_tasks = []
    for task_id, weight in TSS_WEIGHTS.items():
        if task_id in task_scores:
            weighted_sum += task_scores[task_id] * weight
            available_weight += weight
            available_tasks.append(task_id)
        else:
            missing_tasks.append(task_id)
    if available_weight == 0:
        return None, available_tasks, missing_tasks
    tss = round(weighted_sum / TSS_DENOMINATOR, 4)
    return tss, available_tasks, missing_tasks


def compute_cli(task_scores):
    """
    Compute Closed-Loop Index = (T5 + T8) / (T1 + T3).
    Returns None if any required task is missing or denominator is zero.
    """
    for task_id in CLI_NUMERATOR_TASKS + CLI_DENOMINATOR_TASKS:
        if task_id not in task_scores:
            return None
    numerator = sum(task_scores[t] for t in CLI_NUMERATOR_TASKS)
    denominator = sum(task_scores[t] for t in CLI_DENOMINATOR_TASKS)
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)


def evaluate_task(task_dir, trial_dir, write_output=True):
    task_dir = Path(task_dir).resolve()
    trial_dir = Path(trial_dir).resolve()
    task_spec = load_yaml(task_dir / "task_spec.yaml")
    run_manifest = load_json(trial_dir / "run_manifest.json")
    validate_json(run_manifest, "run_manifest.schema.json")
    trial_log_path = trial_dir / "trial_log.jsonl"
    metrics = load_trial_metrics(trial_log_path)
    validate_json(metrics, "trial_metrics.schema.json")
    morphology = run_manifest.get("robot", {}).get("morphology", "unknown")
    score_report = {
        "task_id": task_spec["task_id"],
        "task_title": task_spec["title"],
        "robot_name": run_manifest["robot"]["name"],
        "morphology_track": morphology,
        "build_variant": "canonical",
        "trial_dir": str(trial_dir.relative_to(ROOT.resolve())),
        "metrics": metrics,
        "scoring_coefficients": SCORING,
        "task_score": compute_task_score(metrics),
        "notes": [
            "Aggregate score is for summary use only; leaderboard views should preserve raw metrics.",
            task_spec["scoring_notes"],
        ],
    }
    validate_json(score_report, "score_report.schema.json")
    if write_output:
        out = trial_dir / "score_report.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(score_report, f, indent=2)
            f.write("\n")
    return score_report


def evaluate_suite(baseline_dir, write_output=True):
    """
    Evaluate all tasks in a baseline directory and compute suite-level TSS and CLI.
    baseline_dir should contain task subdirectories named T1_* through T8_*.
    """
    baseline_dir = Path(baseline_dir).resolve()
    task_scores = {}
    reports = {}

    for task_subdir in sorted(baseline_dir.iterdir()):
        if not task_subdir.is_dir():
            continue
        # Infer task_id from directory name (e.g. T5_height_anomaly -> T5)
        task_id = task_subdir.name.split("_")[0]
        if not task_id.startswith("T"):
            continue
        # Find the corresponding task_spec
        task_spec_candidates = list((ROOT / "tasks").glob(f"{task_id}_*/task_spec.yaml"))
        if not task_spec_candidates:
            print(f"  Warning: no task_spec.yaml found for {task_id}, skipping")
            continue
        task_spec_dir = task_spec_candidates[0].parent
        try:
            report = evaluate_task(task_spec_dir, task_subdir, write_output=write_output)
            task_scores[task_id] = report["task_score"]
            reports[task_id] = report
        except Exception as exc:
            print(f"  Warning: could not evaluate {task_id}: {exc}")

    tss, available, missing = compute_tss(task_scores)
    cli = compute_cli(task_scores)

    return {
        "terra_version": TERRA_VERSION,
        "task_scores": task_scores,
        "tss": tss,
        "cli": cli,
        "available_tasks": available,
        "missing_tasks": missing,
        "reports": reports,
    }


def validate_bundle(path):
    path = Path(path)
    reports = []
    if path.is_file():
        target = path.name
        if target == "task_spec.yaml":
            payload = load_yaml(path)
            validate_json(payload, "task_spec.schema.json")
        elif target == "run_manifest.json":
            payload = load_json(path)
            validate_json(payload, "run_manifest.schema.json")
        elif target == "score_report.json":
            payload = load_json(path)
            validate_json(payload, "score_report.schema.json")
        elif target.endswith(".json") and "leaderboard" in str(path):
            payload = load_json(path)
            validate_json(payload, "leaderboard_entry.schema.json")
        else:
            raise ValueError(f"Unsupported file for validation: {path}")
        return [str(path)]

    task_specs = list(path.rglob("task_spec.yaml"))
    for task_spec_path in task_specs:
        validate_json(load_yaml(task_spec_path), "task_spec.schema.json")
        reports.append(str(task_spec_path))

    run_manifests = list(path.rglob("run_manifest.json"))
    if not run_manifests and not task_specs:
        raise ValueError(f"No run_manifest.json files found under {path}")

    for manifest_path in run_manifests:
        validate_json(load_json(manifest_path), "run_manifest.schema.json")
        reports.append(str(manifest_path))
        trial_log_path = manifest_path.parent / "trial_log.jsonl"
        if trial_log_path.exists():
            metrics = load_trial_metrics(trial_log_path)
            validate_json(metrics, "trial_metrics.schema.json")
            reports.append(str(trial_log_path))
        score_path = manifest_path.parent / "score_report.json"
        if score_path.exists():
            validate_json(load_json(score_path), "score_report.schema.json")
            reports.append(str(score_path))
    return reports


def print_summary(score_report):
    metrics = score_report["metrics"]
    print(f'Task: {score_report["task_id"]} {score_report["task_title"]}')
    print(f'Robot: {score_report["robot_name"]} [{score_report.get("morphology_track", "unknown")}]')
    print(f'Task score: {score_report["task_score"]:.4f}')
    print(
        "Metrics: "
        f'success={metrics["success"]}, '
        f'time={metrics["completion_time_s"]} s, '
        f'contacts={metrics["extra_support_contacts"]}, '
        f'recovery_steps={metrics["recovery_steps"]}, '
        f'foot_error={metrics["foot_placement_error_mm"]} mm, '
        f'energy={metrics["energy_proxy"]}'
    )


def print_suite_summary(suite_result):
    print(f'\nTERRA Suite Evaluation (v{suite_result["terra_version"]})')
    print("-" * 50)
    for task_id in sorted(suite_result["task_scores"].keys()):
        score = suite_result["task_scores"][task_id]
        tag = "  [closed-loop]" if task_id in ("T5", "T8") else ""
        print(f"  {task_id}: {score:.4f}{tag}")
    print("-" * 50)
    tss = suite_result["tss"]
    cli = suite_result["cli"]
    print(f"  TSS (TERRA Standard Score): {tss:.4f}" if tss is not None else "  TSS: N/A (incomplete suite)")
    print(f"  CLI (Closed-Loop Index):    {cli:.4f}" if cli is not None else "  CLI: N/A (requires T1, T3, T5, T8)")
    if suite_result["missing_tasks"]:
        print(f"  Missing tasks: {', '.join(suite_result['missing_tasks'])}")
    print()


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        raise SystemExit(
            "Usage: python3 -m benchmark.score <validate|evaluate|evaluate-suite> ..."
        )
    cmd = argv[0]
    if cmd == "validate":
        if len(argv) != 2:
            raise SystemExit("Usage: python3 -m benchmark.score validate <path>")
        for item in validate_bundle(argv[1]):
            print(item)
        return
    if cmd == "evaluate":
        if len(argv) != 3:
            raise SystemExit("Usage: python3 -m benchmark.score evaluate <task_dir> <trial_dir>")
        report = evaluate_task(argv[1], argv[2], write_output=True)
        print_summary(report)
        return
    if cmd == "evaluate-suite":
        if len(argv) != 2:
            raise SystemExit("Usage: python3 -m benchmark.score evaluate-suite <baseline_dir>")
        suite = evaluate_suite(argv[1], write_output=True)
        print_suite_summary(suite)
        return
    raise SystemExit(
        "Usage: python3 -m benchmark.score <validate|evaluate|evaluate-suite> ..."
    )


if __name__ == "__main__":
    main()

from pathlib import Path
import csv
import json
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from benchmark.assets import render_all
from benchmark.score import evaluate_task
from benchmark.spec_data import BASELINE_RUNS, TASK_DEFINITIONS


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_yaml(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def task_dir(task):
    return ROOT / "tasks" / f'{task["task_id"]}_{task["slug"]}'


def render_task_files():
    for task in TASK_DEFINITIONS:
        base = task_dir(task)
        write_yaml(base / "task_spec.yaml", task)
        assembly = "\n".join(
            [
                f"# {task['task_id']} {task['title']}",
                "",
                "## Purpose",
                task["purpose"],
                "",
                "## Assembly Steps",
                *[f"- {step}" for step in task["assembly_steps"]],
                "",
                "## Surface Guidance",
                f"- Surface: {task['materials']['surface']}",
                f"- Target friction coefficient: {task['materials']['target_friction_coefficient']}",
                "",
                "## Start / Finish",
                f"- Start pose: {task['start_pose']}",
                f"- Finish condition: {task['finish_condition']}",
            ]
        )
        write_text(base / "assembly.md", assembly + "\n")
        write_csv(base / "bom.csv", task["bom_rows"])
        write_text(base / "cad" / "README.md", f"# {task['task_id']} CAD Placeholder\n\nUse `drawings/layout.svg` as the dimension reference until STEP/STL assets are authored.\n")
        example = {
            "task_id": task["task_id"],
            "difficulty_modes": list(task["variants"].keys()),
            "required_logs": ["run_manifest.json", "trial_log.jsonl"],
            "scored_metrics": ["success", "completion_time_s", "extra_support_contacts", "recovery_steps", "foot_placement_error_mm", "energy_proxy"],
        }
        write_json(base / "examples" / "submission_example.json", example)


def event_stream(task_id, trial_id, metrics):
    time_s = metrics["completion_time_s"]
    return [
        {"timestamp": 0.0, "event": "trial_start", "task_id": task_id, "trial_id": trial_id},
        {"timestamp": round(time_s * 0.25, 3), "event": "midcourse_checkpoint", "task_id": task_id, "trial_id": trial_id},
        {"timestamp": round(time_s * 0.65, 3), "event": "recovery_checkpoint", "task_id": task_id, "trial_id": trial_id},
        {"timestamp": time_s, "event": "trial_summary", "task_id": task_id, "trial_id": trial_id, "metrics": metrics},
    ]


def render_baselines():
    task_map = {task["task_id"]: task for task in TASK_DEFINITIONS}
    for baseline_name, baseline in BASELINE_RUNS.items():
        root = ROOT / "baselines" / baseline_name
        manifest = {
            "robot": baseline["robot"],
            "benchmark_version": "0.1.0",
            "notes": baseline["notes"],
        }
        for task_id, metrics in baseline["tasks"].items():
            trial_root = root / f"{task_id}_{task_map[task_id]['slug']}"
            write_json(trial_root / "run_manifest.json", manifest)
            with open(trial_root / "trial_log.jsonl", "w", encoding="utf-8") as f:
                for event in event_stream(task_id, f"{baseline_name}_{task_id}_trial01", metrics):
                    f.write(json.dumps(event) + "\n")
            evaluate_task(task_dir(task_map[task_id]), trial_root, write_output=True)


def render_results_index():
    results = {}
    for baseline_name in BASELINE_RUNS:
        baseline_root = ROOT / "baselines" / baseline_name
        scores = []
        for score_path in sorted(baseline_root.rglob("score_report.json")):
            payload = json.loads(score_path.read_text(encoding="utf-8"))
            scores.append(
                {
                    "task_id": payload["task_id"],
                    "task_score": payload["task_score"],
                    "success": payload["metrics"]["success"],
                }
            )
        results[baseline_name] = scores
    write_json(ROOT / "results" / "baseline-summary.json", results)


def main():
    render_task_files()
    render_all()
    render_baselines()
    render_results_index()


if __name__ == "__main__":
    main()

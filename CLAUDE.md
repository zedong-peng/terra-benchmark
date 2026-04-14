# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TERRA (Terrain-Engaged Robot Reasoning Assessment) is a physical benchmark for evaluating closed-loop sensorimotor intelligence in mobile robots. It defines 8 standardised tasks (T1–T8), fabrication specs, a measurement protocol, and a scoring pipeline. The core scientific contribution is the **Closed-Loop Index (CLI)** — a ratio metric that measures how much a robot degrades when terrain predictions are violated.

## Commands

### Install
```bash
pip install -e ".[dev]"
```

### Validate a file or directory against schemas
```bash
python3 -m benchmark.score validate <path>
# path can be: a task_spec.yaml, run_manifest.json, score_report.json,
# a leaderboard entry .json, or a baseline directory
```

### Score a single task trial
```bash
python3 -m benchmark.score evaluate <task_dir> <trial_dir>
# task_dir: e.g. tasks/T1_steady_walking
# trial_dir: e.g. baselines/sim_baseline/T1_steady_walking
```

### Score a full baseline suite (computes TSS and CLI)
```bash
python3 -m benchmark.score evaluate-suite <baseline_dir>
# e.g. python3 -m benchmark.score evaluate-suite baselines/sim_baseline
```

### Rebuild the leaderboard from entries
```bash
python3 scripts/build_leaderboard.py
```

## Architecture

### Data flow for a trial
```
trial_log.jsonl  ──► load_trial_metrics()  ──► metrics dict
run_manifest.json ──► validate against schema
task_spec.yaml   ──► task_id, title, scoring_notes
                              │
                              ▼
                    compute_task_score(metrics)
                    S × (1 − 0.15·C − 0.10·R − 0.05·E)
                              │
                              ▼
                    score_report.json  (written to trial_dir)
```

`trial_log.jsonl` is a newline-delimited JSON file; `load_trial_metrics()` reads it looking for the last line where `event == "trial_summary"`, which must contain a `metrics` dict.

### Suite-level scoring
`evaluate_suite(baseline_dir)` iterates subdirectories named `T*_*`, finds the matching `tasks/T*_*/task_spec.yaml`, calls `evaluate_task` per directory, then passes the collected `{task_id: task_score}` dict to:
- `compute_tss()` — weighted sum divided by 10; T5 and T8 have weight 2.0
- `compute_cli()` — `(T5 + T8) / (T1 + T3)`; returns `None` if any of T1/T3/T5/T8 are missing

### Key constants (`benchmark/spec_data.py`)
All scoring weights, task definitions, and reference baseline data live here. `TASK_DEFINITIONS` is the canonical list of all 8 task dicts. `BASELINE_RUNS` holds the raw metric data that was used to seed `baselines/`. `SCORING` holds `alpha=0.15`, `beta=0.10`, `gamma=0.05`.

### Schema validation
All schemas are in `schemas/`. The five schemas are:
- `task_spec.schema.json` — validates `task_spec.yaml` files
- `run_manifest.schema.json` — validates `run_manifest.json` in each trial dir
- `trial_metrics.schema.json` — validates the `metrics` dict extracted from `trial_log.jsonl`
- `score_report.schema.json` — validates the written `score_report.json`
- `leaderboard_entry.schema.json` — validates entries in `leaderboard/entries/`

`validate_bundle(path)` routes to the correct schema based on filename.

### Leaderboard pipeline
`leaderboard/entries/*.json` → `scripts/build_leaderboard.py` → `leaderboard/leaderboard.json`. GitHub Actions runs validation on PR (`.github/workflows/validate.yml`) and regenerates `leaderboard.json` on merge (`.github/workflows/leaderboard.yml`).

## Task and Baseline Directory Layout

```
tasks/T<N>_<slug>/
    task_spec.yaml          # canonical spec (geometry, tolerances, BOM, variants)
    task_spec.schema.json   # validated against schemas/task_spec.schema.json
    cad/                    # STEP + FreeCAD source files (where available)

baselines/<name>/T<N>_<slug>/
    run_manifest.json       # robot description + benchmark_version
    trial_log.jsonl         # JSONL event log; must contain trial_summary event
    score_report.json       # written by evaluate_task()
```

## Important Invariants

- `energy_proxy == -1.0` means the metric was unavailable; `compute_task_score` zeroes the energy term in this case (do not pass `-1.0` through the formula directly).
- `trial_metrics.schema.json` currently requires `energy_proxy` minimum 0.0, but `score_report.schema.json` allows minimum -1.0. When modifying schemas, keep these in sync.
- Geometry in `task_spec.yaml` is **frozen** for TERRA v2.0 — changing riser heights, gap widths, etc. requires a MAJOR version bump (see `docs/versioning-policy.md`).
- T5 and T8 are the closed-loop tasks; they carry `tss_weight: 2.0` and are the CLI numerator. Changing their task IDs or weights breaks CLI comparability with all published results.

# TERRA

**Terrain-Engaged Robot Reasoning Assessment** — a physical benchmark for sensorimotor competence in unstructured terrain.

---

## The Claim

Mobility intelligence is not locomotion policy quality alone. It is the quality of the loop between exteroception, proprioception, contact, and rapid correction.

A robot that walks well on expected terrain and collapses on unexpected terrain has a different kind of failure than one that falls on nominal stairs. Current benchmarks collapse both into the same result. TERRA is built to separate them.

## Why This Matters

When you descend a staircase and one step is unexpectedly taller, your feedforward prediction fails, your swing foot clips, and the problem is no longer *walking* — it is *recovering while still moving*. That closed-loop correction is exactly what current embodied benchmarks under-measure.

TERRA isolates it as the central diagnostic target.

---

## The Eight Tasks

Each task is built to emphasize one dominant movement primitive and one dominant failure mode.

| ID | Task | Primitive | Failure Mode |
|---|---|---|---|
| T1 | Steady Walking | Steady-state locomotion | Gait drift on nominal terrain |
| T2 | Narrow Placement | Precise foot placement | Lateral balance under constraint |
| T3 | Standard Ascent | Up-step estimation and clearance | Swing height underestimation |
| T4 | Standard Descent | Down-step probing and load transfer | Collapse before support confirmed |
| T5 | Height Anomaly | **Geometry mismatch correction** | Failure to update after expectation violation |
| T6 | Discrete Crossing | Discrete crossing decision | Commitment and landing stability |
| T7 | Repeated Obstacles | Sequential adaptation | Degradation across repetitions |
| T8 | Mild Recovery | **Recovery after disturbance** | Failure to continue after mild perturbation |

T5 and T8 are the benchmark's signature tasks — they test the closed-loop correction that T1–T4 do not require.

---

## Quickstart

Validate an existing submission:

```bash
python3 -m benchmark.score validate baselines/real_robot_baseline
```

Score a single task:

```bash
python3 -m benchmark.score evaluate \
  tasks/T5_height_anomaly \
  baselines/sim_baseline/T5_height_anomaly
```

Compute benchmark-level scores (TSS and CLI):

```bash
python3 -m benchmark.score evaluate-suite baselines/sim_baseline
```

---

## Repository Layout

```
tasks/          8 task kits — task_spec.yaml, assembly.md, bom.csv, drawings/layout.svg
schemas/        JSON schemas for task definitions and submissions
docs/           Technical spec, measurement protocol, fabrication guide
benchmark/      Scoring CLI and asset generation
baselines/      Simulation and real-robot example submissions
leaderboard/    Community results — submit via pull request
sequences/      Composable task chains (Standard Chain, Gauntlet)
```

---

## Benchmark-Level Scores

Beyond per-task scores, TERRA computes two summary statistics:

**TERRA Standard Score (TSS)** — weighted average across all 8 tasks, with T5 and T8 double-weighted to reflect their closed-loop significance:

```
TSS = (T1 + T2 + T3 + T4 + 2×T5 + T6 + T7 + 2×T8) / 10
```

**Closed-Loop Index (CLI)** — ratio of closed-loop task performance to nominal task performance:

```
CLI = (TaskScore_T5 + TaskScore_T8) / (TaskScore_T1 + TaskScore_T3)
```

A CLI of 1.0 means the system degrades no more on disturbance tasks than on nominal tasks. Most systems score CLI < 0.75. The CLI is the benchmark's primary diagnostic value — it is the number that separates robust sensorimotor integration from overfitted nominal locomotion.

---

## Leaderboard

Community results are tracked in [`leaderboard/`](leaderboard/). Submit via pull request — see [`leaderboard/SUBMISSION_GUIDE.md`](leaderboard/SUBMISSION_GUIDE.md).

---

## Building the Apparatus

All 8 tasks can be fabricated with standard workshop materials. Estimated build cost for the complete Standard suite: **USD 500–650** (Baltic birch plywood, aluminum extrusion, anti-slip coating).

See [`docs/fabrication-guide.md`](docs/fabrication-guide.md) for materials, surface friction targets, lighting specs, and AprilTag calibration procedure.

Per-task drawings are at `tasks/T*/drawings/layout.svg`. STEP files for the staircase module assembly are at `tasks/T3_standard_ascent/cad/` and `tasks/T5_height_anomaly/cad/`.

---

## Measurement Protocol

Metric definitions and measurement methods are in [`docs/measurement-protocol.md`](docs/measurement-protocol.md). Labs using different measurement methods must declare them in `score_report.json`. The protocol specifies compliant methods for motion capture, foot pressure plates, and overhead camera + AprilTag setups.

---

## Supported Robot Morphologies

TERRA is designed for any mobile robot that traverses terrain on legs or wheels. The `morphology` field in `run_manifest.json` accepts:

- `humanoid` — bipedal robot with two arms (flagship track)
- `biped` — bipedal robot without arms
- `quadruped` — four-legged robot
- `wheeled_legged` — hybrid wheeled-legged system
- `other` — any other morphology (describe in `notes`)

Tasks T3–T5 (staircases) require leg-capable robots. All other tasks are open to any morphology.

---

## Citing TERRA

```bibtex
@misc{terra2025,
  title   = {TERRA: Terrain-Engaged Robot Reasoning Assessment},
  year    = {2025},
  url     = {https://github.com/pengzedong/embodied-mobility-benchmark},
  note    = {A physical benchmark for sensorimotor competence in unstructured terrain}
}
```

---

## Contributing

Task proposals: open an issue using the [Task Proposal template](.github/ISSUE_TEMPLATE/task_proposal.md).

Leaderboard submissions: see [`leaderboard/SUBMISSION_GUIDE.md`](leaderboard/SUBMISSION_GUIDE.md).

CAD contributions: see [`docs/cad-standards.md`](docs/cad-standards.md).

Versioning policy: see [`docs/versioning-policy.md`](docs/versioning-policy.md).

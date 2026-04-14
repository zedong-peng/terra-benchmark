# Embodied Mobility Benchmark Specification

Embodied Mobility Benchmark V1 defines a reproducible, physical benchmark for humanoid locomotion. The benchmark is organized around eight movement primitives rather than a grab bag of demo scenes.

## Design Decisions

- Scope: humanoid and biped robots only
- Core task count: 8
- Difficulty modes: `canonical`, `parametric`, `challenge`
- Canonical geometry: absolute millimeter-based dimensions for leaderboard comparability
- Secondary normalization guidance: labs may annotate robot hip height and leg length, but leaderboard compliance is tied to canonical geometry
- Score philosophy: raw metrics remain visible; aggregate score is only a compact summary

## Core Tasks

| Task | Primitive | Signature geometry |
| --- | --- | --- |
| T1 steady_walking | Steady-state locomotion | 3000 mm flat walkway |
| T2 narrow_placement | Precise foot placement | 220 mm stepping corridor |
| T3 standard_ascent | Up-step estimation and ascent | 10 stairs, 170 mm riser, 280 mm tread |
| T4 standard_descent | Down-step control | 10 stairs, 170 mm riser, 280 mm tread |
| T5 height_anomaly | Geometry mismatch correction | One 210 mm anomalous riser in an otherwise 170 mm staircase |
| T6 discrete_crossing | Discrete crossing decision | 180 mm gap with rigid landing |
| T7 repeated_obstacles | Sequential adaptation | Five 40 mm low obstacles |
| T8 mild_recovery | Recovery after disturbance | One hidden 15 mm mismatch or slip patch zone |

## Required Submission Artifacts

- `run_manifest.json`
- `trial_log.jsonl`
- `score_report.json`

The benchmark treats `trial_log.jsonl` as the raw evidence source and `score_report.json` as derived output. Labs should submit both.

## Metric Definitions

- `success`: normalized completion success in `[0, 1]`
- `completion_time_s`: elapsed trial time
- `extra_support_contacts`: count of non-foot support contacts
- `recovery_steps`: number of steps required to re-stabilize after disturbance
- `foot_placement_error_mm`: stance error relative to the task’s intended landing region
- `energy_proxy`: normalized unitless effort term in `[0, 1]`

## Aggregate Task Score

The benchmark publishes raw metrics first. For compact comparison, it also computes:

`TaskScore = S * (1 - alpha*C - beta*R - gamma*E)`

with:

- `alpha = 0.15`
- `beta = 0.10`
- `gamma = 0.05`

where:

- `S` is success
- `C` is extra-support-contact cost normalized to `[0, 1]`
- `R` is recovery-step cost normalized to `[0, 1]`
- `E` is the normalized energy proxy

## Evaluation Rules

- No handrail or external support use
- No non-foot ground contacts for a clean success
- Disturbance ground truth may be hidden before a run and revealed only in evaluator logs
- Challenge mode may alter contrast and disturbance placement, but not the identity of the underlying task

## Deliverable Standard

Each task directory ships with:

- `task_spec.yaml`
- `assembly.md`
- `bom.csv`
- `drawings/layout.svg`
- `cad/README.md`
- `examples/submission_example.json`


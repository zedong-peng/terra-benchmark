# TERRA: Terrain-Engaged Robot Reasoning Assessment

Most robotics benchmarks still fail in the same way: they tell us that a system succeeded or failed, but they do not tell us what the system had to understand in motion.

A robot climbs a staircase. Another one clears an obstacle course. A third produces a good-looking demonstration video. These are useful demonstrations, but they often compress too many abilities into one result. Was the hard part terrain perception, foot placement, disturbance recovery, or simply a controller overfit to one apparatus?

This repository is an attempt to make that question measurable.

Today we are releasing **TERRA** — Terrain-Engaged Robot Reasoning Assessment — an open benchmark kit for mobile robot locomotion that focuses on physical reproducibility, movement primitives, and closed-loop recovery rather than a grab bag of loosely comparable tasks.

---

## The Core Observation

Human locomotion is not just motor execution. It is a closed loop between prediction and correction.

Vision estimates terrain geometry ahead of time. Proprioception and contact feedback refine that estimate once the body commits weight. The gait forms a rhythm, and then the rhythm has to break as soon as the world violates expectation.

You can feel this immediately on an irregular staircase. Most steps are uniform. Your body locks into a cadence. Then one step is unexpectedly taller. The feedforward estimate is wrong, the swing foot clips, the center of mass shifts, and the problem is no longer "walking" but "recovering".

That failure mode is exactly the kind of thing current embodied benchmarks under-measure. They test whether a robot can walk. TERRA tests whether a robot can correct.

---

## The Scientific Claim

**Mobility intelligence is not only locomotion policy quality; it is the quality of the loop between exteroception, proprioception, contact, and rapid correction.**

If that claim is right, the most informative embodied tasks are not the most cinematic ones. They are the ones where one assumption is broken and the system has to repair itself while still moving. A benchmark that does not include such tasks cannot distinguish a robot with genuine sensorimotor integration from one with an overfitted controller.

We test this claim with a concrete measurable quantity: the **Closed-Loop Index** (CLI).

---

## The Closed-Loop Index

The CLI measures how much a system degrades when its feedforward expectation is violated, relative to its nominal locomotion performance:

```
CLI = (TaskScore_T5 + TaskScore_T8) / (TaskScore_T1 + TaskScore_T3)
```

A CLI of 1.0 means no degradation under expectation violation. Most current systems score CLI < 0.75 — meaning closed-loop tasks reveal failures that nominal stair climbing conceals. The CLI is not just a summary statistic; it is the benchmark's primary diagnostic.

From our illustrative baselines, the gap is already visible:

| Baseline | T1 (walking) | T3 (ascent) | T5 (anomaly) | T8 (recovery) | CLI |
|---|---|---|---|---|---|
| Simulation | 1.00 | 0.94 | 0.62 | 0.58 | **0.64** |
| Real robot | 0.92 | 0.89 | 0.79 | 0.76 | **0.86** |

The simulation policy does well on nominal tasks and degrades sharply under disturbances. The real-robot baseline is slower and less efficient but more robust when its feedforward model fails. This difference is not visible in a benchmark that only measures success on a standard staircase. It only appears when you break the expectation.

---

## The Eight Tasks

For a first version, we focused on one question: **How many movement primitives must we measure before we can say a system has basic terrain competence?**

Our answer is eight. Each task is built to emphasize one dominant movement primitive and one dominant failure mode.

### T1. Steady Walking

A flat, unobstructed 3000 mm walkway. This is the nominal locomotion floor, not the ceiling.

### T2. Narrow Placement

A 220 mm stepping corridor that makes foot placement and lateral balance visible.

### T3. Standard Ascent

A 10-step staircase with 170 mm risers and 280 mm treads. This measures terrain estimation, swing clearance, and upward load transfer.

### T4. Standard Descent

The same staircase used in descent. This exposes the uncertainty that appears before support is fully confirmed on the lower step.

### T5. Height Anomaly

A single 210 mm riser inserted into an otherwise regular staircase at step 6. The robot is not told which step is anomalous. This is the benchmark's signature closed-loop correction task. Failing T5 while passing T3 is one of the most informative results a benchmark can produce.

### T6. Discrete Crossing

A single 180 mm gap. The robot must commit to a discrete crossing and land stably.

### T7. Repeated Obstacles

Five low obstacles, each 40 mm high, spaced 350 mm apart. This measures repeated adaptation rather than a one-off maneuver.

### T8. Mild Recovery

A flat lane with one controlled disturbance — a hidden 15 mm height mismatch or a low-friction insert. The point is not to force spectacular failure. The point is to reveal whether the system can recover and continue.

---

## Why This Benchmark Is Physical

Simulation is still essential. But the hardest mobility failures often happen exactly where simulation is weakest: at contact, at transition, and at the boundary between what the robot predicted and what the world actually did.

That is why TERRA is released as a physical kit specification:

- geometry defined in millimeters with explicit tolerances
- surfaces and friction targets documented with measurement methods
- task drawings included per task
- an operational measurement protocol for all six reported metrics
- a common logging and scoring format
- JSON schemas for automated validation

The goal is that different labs can fabricate the same apparatus, run the same protocol, and obtain results that are more comparable than "we also tested stairs." The measurement protocol in `docs/measurement-protocol.md` is what makes this possible — it specifies exactly how to compute each metric from raw sensor data, including three compliant measurement approaches (motion capture, foot pressure plates, and overhead camera with AprilTag calibration).

---

## Scoring

A binary pass/fail metric is too lossy for embodied mobility.

Each run reports:

- `success` — binary completion (1.0 or 0.0)
- `completion_time_s` — elapsed trial time
- `extra_support_contacts` — count of non-foot support contacts
- `recovery_steps` — steps required to re-stabilize after disturbance
- `foot_placement_error_mm` — mean stance deviation from designated landing zones
- `energy_proxy` — normalized mechanical work per unit distance

The repository computes a compact task score for summary use, but it keeps raw metrics visible because the research signal is often in the decomposition, not in the aggregate:

```
TaskScore = S × (1 − 0.15·C − 0.10·R − 0.05·E)
```

For benchmark-level comparison, TERRA also computes:

- **TSS** (TERRA Standard Score): weighted average with T5 and T8 double-weighted
- **CLI** (Closed-Loop Index): the ratio of closed-loop to nominal task performance

---

## Baselines

The release includes two illustrative baselines:

- `sim_baseline`: stronger on nominal locomotion, weaker on mismatch and recovery (CLI ≈ 0.64)
- `real_robot_baseline`: slower, but more robust on T5 and T8 (CLI ≈ 0.86)

That difference is intentional. A useful benchmark should not only rank systems. It should also expose *why* they differ. The CLI makes that difference precise.

---

## Open to All Robot Morphologies

TERRA is designed for any mobile robot that traverses terrain. The humanoid/biped form is the flagship track — it is the hardest case and the commercially relevant one — but TERRA's apparatus specifications are morphology-agnostic where possible. The same staircase geometry serves a Boston Dynamics Spot and a Unitree H1. Submissions declare their morphology in `run_manifest.json`, and leaderboard results are separated by morphology track.

Supported morphologies in V2.0: `humanoid`, `biped`, `quadruped`, `wheeled_legged`, `other`.

---

## Community Leaderboard

Results are submitted via pull request to `leaderboard/entries/`. GitHub Actions validates each entry against the schema and automatically updates the leaderboard. No server required. See `leaderboard/SUBMISSION_GUIDE.md`.

---

## What Comes Next

This release is a strong V2, not the endpoint.

The next steps are straightforward:

1. Real hardware results from additional labs to calibrate CLI across diverse platforms.
2. Official MuJoCo and Isaac Sim scene files generated from the same `task_spec.yaml` geometry, enabling a TERRA-Sim track and a per-task sim-to-real gap analysis.
3. Foundation tasks (F-tier) for lower-cost entry into the benchmark, targeting labs without full staircase fabrication capacity.
4. Extended task kits for challenge conditions — degraded sensing, compound terrain transitions, dynamic obstacles.

The long-term goal is not a collection of robotics demos. It is a benchmark stack that says, with some precision, which sensorimotor abilities systems actually have and which failure modes still dominate.

That is still the missing layer in embodied AI.

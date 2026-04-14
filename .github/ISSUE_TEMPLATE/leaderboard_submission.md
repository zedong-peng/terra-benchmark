---
name: Leaderboard Submission
about: Submit your robot's TERRA evaluation results to the community leaderboard
title: "[Leaderboard] <Robot Name> — <Lab> (<YYYY-MM-DD>)"
labels: leaderboard
assignees: ''

---

## Submission Checklist

Before opening this issue, please verify:

- [ ] I have run `python3 -m benchmark.score validate leaderboard/entries/<my-file>.json` locally and it passes
- [ ] My entry JSON is in `leaderboard/entries/` with a valid `submission_id` (format: `YYYY-MM-robotname-labname`)
- [ ] I have included `measurement_methods` codes for all 6 metrics
- [ ] `evaluation_date` reflects the actual date of the evaluation session
- [ ] All `task_scores` values match the `task_score` fields in the corresponding `score_report.json` outputs

---

## Submission Summary

**Robot name:**
**Lab / Institution:**
**Morphology:** <!-- humanoid / biped / quadruped / wheeled_legged / other -->
**Benchmark version:** 2.0
**Evaluation date:**
**Build variant:** <!-- canonical / parametric / challenge -->

**Task scores:**

| Task | Score |
|------|-------|
| T1 — Steady Walking | |
| T2 — Narrow Foot Placement | |
| T3 — Standard Stair Ascent | |
| T4 — Standard Stair Descent | |
| T5 — Height Anomaly (closed-loop) | |
| T6 — Discrete Gap Crossing | |
| T7 — Repeated Obstacle Course | |
| T8 — Mild Perturbation Recovery (closed-loop) | |

**TSS:** *(auto-computed if omitted)*
**CLI:** *(auto-computed if omitted; requires T1, T3, T5, T8)*

---

## Evaluation Setup

<!-- Describe your test environment: floor type, room dimensions, lighting, any deviations from the standard protocol -->

## Measurement Methods

<!-- List which measurement method code you used for each metric (see docs/measurement-protocol.md) -->

| Metric | Method |
|--------|--------|
| success | |
| completion_time_s | |
| extra_support_contacts | |
| recovery_steps | |
| foot_placement_error_mm | |
| energy_proxy | |

## Links

**Paper (optional):**
**Video (optional):**

---

*Please also open a pull request adding your entry JSON file to `leaderboard/entries/`. This issue is for discussion; the PR triggers CI validation.*

# Leaderboard Policy

The benchmark is designed to reward transparent reporting, not only headline numbers.

## Submission Rules

- Submit one `run_manifest.json` per robot configuration
- Submit one `trial_log.jsonl` and one `score_report.json` per evaluated task
- Include failed runs if they occur in the declared evaluation block

## Reporting

- Public results should show task-wise raw metrics and aggregate task scores
- Aggregate score alone is not sufficient for claims about embodied mobility competence
- Task `T5 height_anomaly` and task `T8 mild_recovery` should always be reported when making claims about closed-loop robustness

## Reproducibility

- Canonical geometry is the default leaderboard condition
- Parametric and challenge results should be reported in separate columns rather than mixed into canonical scores
- Robot morphology must be reported as humanoid or biped; cross-morphology rankings are out of scope for V1

## Integrity

- Hidden challenge parameters may be withheld until after a run block
- Selecting only the best single run is not permitted; report the declared block outcome
- If external support or manual catch occurs, that trial must be marked unsuccessful


# TERRA Leaderboard Submission Guide

This guide walks you through submitting your robot's TERRA evaluation results to the community leaderboard via pull request.

---

## Prerequisites

- [ ] You have run the TERRA Standard Suite (T1–T8, canonical variant) on your robot
- [ ] You have raw `trial_log.jsonl` files for each task trial
- [ ] You have recorded the measurement method used for each metric (see [measurement-protocol.md](../docs/measurement-protocol.md))
- [ ] Your repo fork is up to date with `main`

---

## Step 1 — Run the Scoring Pipeline

Run the evaluation suite locally to confirm scores and generate `score_report.json` files:

```bash
# Install dependencies
pip install -e ".[dev]"

# Validate your trial data first
python3 -m benchmark.score validate path/to/your/baseline_dir

# Compute task scores and suite-level TSS + CLI
python3 -m benchmark.score evaluate-suite path/to/your/baseline_dir
```

Expected output:

```
TERRA Suite Evaluation (v2.0)
--------------------------------------------------
  T1: 0.9500
  T2: 0.8900
  T3: 0.8700
  T4: 0.8200
  T5: 0.7100  [closed-loop]
  T6: 0.7800
  T7: 0.7500
  T8: 0.6900  [closed-loop]
--------------------------------------------------
  TSS (TERRA Standard Score): 0.7870
  CLI (Closed-Loop Index):    0.7854
```

---

## Step 2 — Create Your Entry JSON

Create a file at `leaderboard/entries/<submission_id>.json`.

**Submission ID format:** `YYYY-MM-<robotname>-<labname>` — lowercase, hyphens only.

Example: `2025-04-atlas-mit.json`

### Minimal entry (only completed tasks required):

```json
{
  "submission_id": "2025-04-myrobot-mylab",
  "robot_name": "MyRobot v2",
  "lab": "My Lab, University of X",
  "morphology": "humanoid",
  "benchmark_version": "2.0",
  "evaluation_date": "2025-04-15",
  "build_variant": "canonical",
  "task_scores": {
    "T1": 0.9500,
    "T2": 0.8900,
    "T3": 0.8700,
    "T4": 0.8200,
    "T5": 0.7100,
    "T6": 0.7800,
    "T7": 0.7500,
    "T8": 0.6900
  },
  "measurement_methods": {
    "foot_placement_error_mm": "overhead_camera",
    "energy_proxy": "robot_proprioception",
    "extra_support_contacts": "robot_proprioception",
    "recovery_steps": "robot_proprioception",
    "success": "robot_proprioception",
    "completion_time_s": "robot_proprioception"
  },
  "notes": [
    "Evaluation conducted on hardwood floor. AprilTag overhead camera calibrated to < 1.5 mm reprojection error.",
    "Energy proxy computed from joint torque × velocity integral via onboard motor controllers."
  ]
}
```

### Full entry (with paper and video):

```json
{
  "submission_id": "2025-04-myrobot-mylab",
  "robot_name": "MyRobot v2",
  "lab": "My Lab, University of X",
  "morphology": "humanoid",
  "benchmark_version": "2.0",
  "evaluation_date": "2025-04-15",
  "build_variant": "canonical",
  "task_scores": {
    "T1": 0.9500,
    "T2": 0.8900,
    "T3": 0.8700,
    "T4": 0.8200,
    "T5": 0.7100,
    "T6": 0.7800,
    "T7": 0.7500,
    "T8": 0.6900
  },
  "tss": 0.7870,
  "cli": 0.7854,
  "paper_url": "https://arxiv.org/abs/2025.XXXXX",
  "video_url": "https://youtu.be/XXXXXXXXXX",
  "measurement_methods": {
    "foot_placement_error_mm": "overhead_camera",
    "energy_proxy": "robot_proprioception",
    "extra_support_contacts": "pressure_plate",
    "recovery_steps": "mocap",
    "success": "mocap",
    "completion_time_s": "mocap"
  },
  "hardware_cost_usd": 3800,
  "notes": [
    "Full MoCap suite (Vicon 12-camera) for success and timing.",
    "Foot pressure plate (Tekscan HR Mat) for contact detection.",
    "Overhead GoPro + AprilTag36h11 for foot placement error."
  ]
}
```

---

## Step 3 — Validate Locally

```bash
python3 -m benchmark.score validate leaderboard/entries/2025-04-myrobot-mylab.json
```

Fix any schema errors before opening a PR.

---

## Step 4 — Open a Pull Request

1. Fork this repository (if you haven't already)
2. Add your entry JSON to `leaderboard/entries/`
3. Open a pull request with title: `[Leaderboard] <Robot Name> – <Lab> (<Date>)`

**PR description template:**

```markdown
## Leaderboard Submission

- **Robot:** MyRobot v2
- **Lab:** My Lab, University of X
- **Morphology:** humanoid
- **Build variant:** canonical
- **TSS:** 0.7870
- **CLI:** 0.7854

### Evaluation setup
Brief description of your test environment, measurement methods, and any deviations from the standard protocol.

### Checklist
- [ ] `python3 -m benchmark.score validate` passes locally
- [ ] measurement_methods codes included for all 6 metrics
- [ ] evaluation_date is the actual date of evaluation (not submission date)
- [ ] All task_score values verified against score_report.json outputs
```

CI will run schema validation automatically. Maintainers will review and merge.

---

## Partial Results

You do not need all 8 tasks to submit. Missing tasks are simply omitted from `task_scores`.

- **TSS** is computed proportionally over available tasks (noted in leaderboard as "partial")
- **CLI** requires T1, T3, T5, T8 — omitted if any are missing

If you only have one morphology track's relevant tasks (e.g., T1–T5 only), that is a valid partial submission.

---

## Updating an Existing Entry

To update a previous result (e.g., after improving your robot or fixing a measurement error):

1. Create a **new** entry JSON with a new `submission_id` (increment the date or add a suffix like `-v2`)
2. Reference the previous submission in `notes`: `"Supersedes 2025-04-myrobot-mylab"`
3. The old entry remains in history for reproducibility

---

## Measurement Method Codes

| Code | Description |
|------|-------------|
| `mocap` | Motion capture system (Vicon, OptiTrack, etc.) |
| `pressure_plate` | Floor-embedded pressure plate or mat |
| `overhead_camera` | Overhead RGB/RGBD camera + AprilTag calibration |
| `robot_proprioception` | Robot's own sensors (joint encoders, IMU, foot contact) |
| `manual_video` | Human annotation of video recording |
| `not_applicable` | Metric not relevant for this morphology/task |
| `unavailable` | Data not recorded; metric reported as -1.0 |

See [measurement-protocol.md](../docs/measurement-protocol.md) for exact operational definitions.

---

## Questions?

Open an issue with the [Leaderboard Submission template](../.github/ISSUE_TEMPLATE/leaderboard_submission.md).

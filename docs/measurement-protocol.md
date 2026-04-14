# TERRA Measurement Protocol

This document defines the operational computation method for every metric reported in a TERRA trial. All labs submitting results to the leaderboard must follow this protocol. Results computed with non-compliant methods must be flagged in the `notes` field of `score_report.json`.

---

## Overview

TERRA defines six per-trial metrics. Each metric must appear in the `trial_summary` event of `trial_log.jsonl` and in the `metrics` block of `score_report.json`.

| Metric | Type | Unit | Range |
|---|---|---|---|
| `success` | float | dimensionless | [0, 1] |
| `completion_time_s` | float | seconds | ≥ 0 |
| `extra_support_contacts` | integer | count | ≥ 0 |
| `recovery_steps` | integer | count | ≥ 0 |
| `foot_placement_error_mm` | float | millimeters | ≥ 0 |
| `energy_proxy` | float | dimensionless | [0, 1] |

---

## 1. `success`

**Definition:** Binary completion indicator, reported as a float for future partial-credit extensions.

**Canonical value:**
- `1.0` — both feet cross the finish line, no fall occurs, no external support is used, no non-foot ground contacts occur
- `0.0` — any of the above conditions is violated

**Fall definition:** The robot's pelvis height drops below 50% of its nominal standing pelvis height as reported in `run_manifest.json` under `robot.height_m`. If pelvis tracking is unavailable, any non-foot body contact with the ground counts as a fall.

**Finish line crossing:** At least one foot must be fully past the marked finish line (both heel and toe sensors or markers past the line), followed by the second foot reaching the same condition within 10 seconds.

**Note:** Do not use partial values (e.g., 0.5 for "almost finished") in the current version. Partial credit semantics are reserved for V3.

---

## 2. `completion_time_s`

**Definition:** Elapsed time from the start signal to the finish line crossing event.

**Start signal:** The timestamp of the `trial_start` event in `trial_log.jsonl`.

**End event:** The timestamp when the *second* foot fully crosses the finish line. If the trial fails (`success = 0`), report the elapsed time at the moment of failure (fall, external contact, or timeout).

**Timeout:** Each task specifies a maximum allowed time in its `task_spec.yaml` under `scoring_notes`. The default timeout is 120 seconds for all V2.0 tasks. A timed-out trial records `success = 0.0` and `completion_time_s = 120.0`.

---

## 3. `extra_support_contacts`

**Definition:** Count of distinct contact events involving any non-foot body part touching the ground, a handrail, the task apparatus, or an external object for support.

**What counts:**
- Hand, knee, shin, hip, torso, or arm contact with the ground or apparatus
- Any contact with a handrail (if present) regardless of force magnitude
- External contact with a human spotter's hand (this also invalidates `success`)

**What does not count:**
- Foot-sole contact with the ground (expected locomotion behavior)
- Foot-edge contact during normal stair climbing (lateral foot edge touching riser face)
- Robot body contacting the robot's own body parts (self-contact)

**Measurement method:**
- **Preferred:** Binary contact switches or force/torque cells on knee, shin, and hand links reporting contact > 5 N
- **Acceptable:** Vision-based detection of non-foot body segments within 50 mm of the ground or apparatus surface using overhead camera + AprilTag coordinate frame
- **Minimum:** Manual annotation from video with frame-level precision

**Counting rule:** Multiple contacts within a 500 ms window count as one event (a single stumble may cause brief multi-limb contacts). Contacts separated by more than 500 ms count as separate events.

---

## 4. `recovery_steps`

**Definition:** Number of corrective steps taken to re-stabilize after a disturbance, anomaly, or unexpected contact.

**Recovery step definition:** A footstep is classified as a recovery step if:
1. It occurs within 3 seconds after a disturbance event (logged as `recovery_checkpoint` in `trial_log.jsonl`), AND
2. The robot's lateral center-of-mass (CoM) velocity at the moment of the step is > 0.05 m/s (i.e., the CoM is still being corrected)

**For tasks without explicit disturbances (T1, T2, T3, T4, T6, T7):** Log `recovery_steps = 0` unless a stumble occurs mid-task, in which case count from the stumble event until CoM lateral velocity drops below 0.05 m/s.

**For T5 (height anomaly) and T8 (mild recovery):** The disturbance event is logged at the moment the anomalous step is encountered (T5) or the slip patch is entered (T8).

**Measurement method:**
- **Preferred:** CoM trajectory from motion capture (minimum 6 markers on pelvis and torso) at ≥ 100 Hz. CoM lateral velocity computed as 5-point finite difference.
- **Acceptable:** IMU-estimated CoM velocity (fused pelvis IMU + leg kinematics) with stated accuracy bounds in lab notes.
- **Minimum:** Manual step count from video annotation; log `recovery_steps_method: "manual_video"` in `notes`.

---

## 5. `foot_placement_error_mm`

**Definition:** Mean Euclidean distance (in the horizontal plane) between the measured foot contact centroid and the nearest designated landing zone center for each step of the trial.

**Computation:**
1. For each footstep in the trial, identify the contact centroid (center of pressure during stance phase)
2. Find the nearest designated landing zone center from the task geometry (defined in `task_spec.yaml` under `geometry`)
3. Compute the horizontal Euclidean distance in mm
4. Average over all footsteps in the trial

For flat tasks (T1, T2): the designated landing zones are defined as points on the centerline spaced by nominal step length (0.4 × leg length). Use the robot's actual step length for centroid calculation.

For stair tasks (T3, T4, T5): each tread has a single designated target zone — the center of the tread minus 50 mm from the nosing (safe landing region). Foot landing forward of the nosing by more than 80 mm or behind the nosing counts as an error.

**Measurement methods (choose one and report in `notes`):**

**Method A — Motion capture (preferred):**
- Place retro-reflective markers on heel and first/fifth metatarsal heads bilaterally
- Compute foot contact centroid as centroid of the three markers during the flat-foot stance phase (force plate zero-crossing or acceleration minimum)
- Accuracy target: ±3 mm

**Method B — Foot pressure plate:**
- Use pressure-sensitive insole or instrumented floor tile
- Contact centroid = center of pressure from peak pressure frame during stance
- Accuracy target: ±5 mm

**Method C — Overhead camera + AprilTag (minimum viable):**
- Mount an overhead camera at ≥ 2 m height with 640×480 resolution minimum
- Place AprilTag36h11 tags (tag ID 0–3) at all four corners of the task area to define the coordinate frame
- Detect foot outline from overhead segmentation; centroid = geometric centroid of foot bounding box
- Accuracy target: ±15 mm — acceptable for leaderboard but must be noted in submission

**For tasks where foot placement targets are not meaningful (T8 mild recovery):** Set `foot_placement_error_mm = 0.0` and log `"foot_placement_not_applicable": true` in `notes`.

---

## 6. `energy_proxy`

**Definition:** Normalized mechanical work per unit distance, serving as a proxy for locomotion efficiency.

**Formula:**
```
energy_proxy = W_mech / (m_robot × g × d_task)
```

Where:
- `W_mech` = total mechanical work done by all actuated joints (J) = `∑_i ∫ |τᵢ(t) · ω̇ᵢ(t)| dt`
- `m_robot` = robot total mass (kg) from `run_manifest.json`
- `g` = 9.81 m/s²
- `d_task` = horizontal distance traversed (m) — the task's nominal path length from `task_spec.yaml`

**Normalization to [0, 1]:** Divide by the reference value of 3.0 (dimensionless). A value of 1.0 or above is clamped to 1.0. Reference: an efficient walking human has an energy proxy of approximately 0.2–0.4 with this normalization; early humanoid systems typically produce 0.5–0.9.

```
energy_proxy = min(W_mech / (m_robot × g × d_task × 3.0), 1.0)
```

**Measurement method:**
- **Preferred:** Record joint torques `τᵢ` (Nm) and angular velocities `ω̇ᵢ` (rad/s) from all actuated joints at the controller frequency (minimum 100 Hz). Integrate using trapezoidal rule.
- **Acceptable for electric motors:** Power `P_i = τᵢ × ω̇ᵢ`. Use joint current × voltage × efficiency factor (0.85 assumed if not measured).
- **Not acceptable:** Battery discharge energy alone (includes thermal and computational load, not just mechanical work).

**If torque data is unavailable:** Log `energy_proxy = -1.0` and set `"energy_unavailable": true` in `notes`. This trial will not receive an energy component in its TaskScore.

---

## Sensor and Calibration Requirements

### AprilTag Calibration Protocol

Use AprilTag36h11 family for all TERRA tasks. Minimum 4 tags per task area.

**Before each evaluation block:**
1. Place tag 0 at the start zone left corner, tag 1 at start zone right corner, tag 2 at finish zone left corner, tag 3 at finish zone right corner
2. Capture 10 frames from the overhead camera with static apparatus
3. Solve for the homography between tag corners and the known task coordinate frame
4. Verify reprojection error < 2 mm at all four tag positions
5. Remove tags before the first scored trial

### Motion Capture Requirements

If using external motion capture for foot placement:
- Minimum 8-camera system covering the full task area
- Capture rate ≥ 100 Hz
- Residual marker error < 1.5 mm
- Reconstruct at 100 Hz; report frame rate in lab notes

### Inertial Measurement

If using robot-internal IMU for CoM estimation:
- Report IMU model and mounting location in `run_manifest.json` under `sensors`
- Report CoM estimation algorithm and expected drift per meter
- Calibrate against a static reference pose before each evaluation block

---

## Trial Logging Format

A well-formed `trial_log.jsonl` must contain at minimum these event types in chronological order:

```jsonl
{"timestamp": 0.000, "event": "trial_start", "task_id": "T5", "trial_id": "run_001"}
{"timestamp": 12.340, "event": "midcourse_checkpoint", "task_id": "T5", "trial_id": "run_001", "step_index": 5, "foot_placement_error_at_step_mm": 8.2}
{"timestamp": 15.780, "event": "recovery_checkpoint", "task_id": "T5", "trial_id": "run_001", "trigger": "height_anomaly_step_6", "com_lateral_velocity_ms": 0.18}
{"timestamp": 28.450, "event": "trial_summary", "task_id": "T5", "trial_id": "run_001", "metrics": {"success": 1.0, "completion_time_s": 28.45, "extra_support_contacts": 0, "recovery_steps": 2, "foot_placement_error_mm": 11.3, "energy_proxy": 0.61}}
```

**Required fields for `trial_summary`:** All six metrics listed in the Overview table above. Missing fields cause validation failure.

**Optional extended metrics block:** Labs may include an `extended_metrics` sibling to `metrics` in `trial_summary` for reporting additional data (joint-level energy, per-step foot error time series, etc.) without affecting schema compliance.

---

## Measurement Method Reporting

Every `score_report.json` must include a `measurement_methods` block in `notes` describing which method was used for each metric. Use the method codes below:

| Code | Description |
|---|---|
| `mocap` | External motion capture system |
| `pressure_plate` | Foot pressure plate or instrumented insoles |
| `overhead_camera` | Overhead camera + AprilTag frame |
| `robot_proprioception` | Robot's own joint encoders and IMU |
| `manual_video` | Manual annotation from video recording |
| `not_applicable` | Metric not applicable to this task |
| `unavailable` | Sensor not present; metric set to -1 |

Example `notes` entry:
```json
"notes": [
  "measurement_methods: success=robot_proprioception, completion_time_s=robot_proprioception, extra_support_contacts=manual_video, recovery_steps=mocap, foot_placement_error_mm=mocap, energy_proxy=robot_proprioception",
  "Motion capture: Vicon Vantage V16, 100 Hz, 12 cameras, residual < 1.2 mm",
  "Energy computation: joint torque × velocity from servo telemetry at 200 Hz"
]
```

---

## Cross-Lab Reproducibility Checklist

Before submitting results to the leaderboard, verify:

- [ ] All six metrics are present in `trial_summary`
- [ ] `run_manifest.json` includes `robot.height_m` and `robot.mass_kg`
- [ ] Measurement methods are documented in `notes`
- [ ] AprilTag calibration was performed before the evaluation block
- [ ] Task apparatus dimensions were verified against `task_spec.yaml` tolerances before the run
- [ ] `benchmark_version` in `run_manifest.json` matches the task spec version
- [ ] At least 3 trials were run per task in the declared evaluation block (median reported)
- [ ] Failed trials in the evaluation block are included in the submission (not cherry-picked)

---

*TERRA Measurement Protocol v2.0 — maintained at `docs/measurement-protocol.md`*

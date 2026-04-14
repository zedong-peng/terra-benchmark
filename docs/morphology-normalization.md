# Morphology Normalization in TERRA

TERRA is designed to be useful across all mobile robot morphologies, not just humanoids.  However, raw metric values are not always directly comparable across morphologies because leg geometry differs significantly.  This document defines how to normalize metrics for cross-morphology comparison and explains how the leaderboard groups results by track.

---

## Morphology Tracks

Results on the TERRA leaderboard are always grouped by track first.  **No cross-track ranking is shown in the primary table.**

| Track | Description | Canonical Foot Contact |
|-------|-------------|----------------------|
| `humanoid` | Upright biped with human-like proportions; standing height 1.2–2.1 m | Rigid or compliant foot sole |
| `biped` | Upright biped outside humanoid proportions; e.g., very small or very large scale | Rigid or compliant foot sole |
| `quadruped` | Four-legged platform; e.g., Spot, ANYmal | Individual paw or foot pads |
| `wheeled_legged` | Hybrid with wheels and articulated legs | Wheel contact + optional leg contact |
| `other` | Any morphology not covered above — describe fully in `notes` | As applicable |

---

## Why Normalization Matters

Consider foot placement error.  A 20 mm error represents very different difficulty for:

- A humanoid with a 300 mm foot and 0.9 m leg length
- A quadruped with a 60 mm paw and 0.4 m leg length

Raw millimetre values alone can make a small robot look worse than it is.  TERRA reports **both raw and normalised values** in the score report.

---

## Normalisation Definitions

### Foot Placement Error (FPE)

**Normalised FPE:**

```
FPE_norm = FPE_mm / leg_length_mm
```

where `leg_length_mm` is the nominal standing leg length from hip joint to ground contact, reported in `run_manifest.json → robot → leg_length_m`.

**Interpretation:** FPE_norm ≈ 0.02 means the placement error is 2% of leg length — consistent difficulty across morphologies.

### Step Clearance (informational only)

Swing-foot clearance is not a primary scored metric in TERRA v2.0, but if reported in trial logs it should be normalised by leg length for the same reason.

### Recovery Steps

Recovery steps (number of steps to restabilise) is already dimensionless and morphology-agnostic.  No normalisation required.

### Energy Proxy

The energy proxy formula already incorporates body mass and distance:

```
energy_proxy = Σ|τᵢ·dθᵢ| / (mass_kg × g × distance_m × 3.0)
```

This normalisation makes the metric comparable across mass scales.  However, the appropriate upper bound (the divisor `3.0`) was calibrated on humanoid data.  For quadrupeds and wheeled-legged platforms, `3.0` may be too tight or too loose — report `energy_proxy = -1.0` if the metric is not meaningful for your morphology, and describe the actual energy usage in `notes`.

---

## Task Applicability by Morphology

Not all TERRA tasks are equally meaningful for all morphologies.  The `morphology_tracks` field in each `task_spec.yaml` lists the tracks for which the task is valid.

| Task | humanoid | biped | quadruped | wheeled_legged | Notes |
|------|---------|-------|-----------|---------------|-------|
| T1 — Steady Walking | ✓ | ✓ | ✓ | ✓ | Universal baseline |
| T2 — Narrow Placement | ✓ | ✓ | — | — | 220 mm corridor too narrow for most quadruped stances; parametric variant may be used with wider corridor for quadruped track |
| T3 — Standard Ascent | ✓ | ✓ | ✓ | — | 280 mm tread depth accommodates typical quadruped stride; wheeled-legged excluded unless legged gait mode active |
| T4 — Standard Descent | ✓ | ✓ | ✓ | — | Same as T3 |
| T5 — Height Anomaly | ✓ | ✓ | ✓ | — | Core closed-loop task; quadruped results are especially diagnostic |
| T6 — Discrete Crossing | ✓ | ✓ | ✓ | ✓ | Wheeled-legged included if wheel can clear a 180 mm gap |
| T7 — Repeated Obstacles | ✓ | ✓ | ✓ | — | 40 mm obstacle height is trivial for most quadrupeds; parametric variant (60–100 mm) recommended for quadruped track |
| T8 — Mild Recovery | ✓ | ✓ | ✓ | — | Core closed-loop task |

Entries that skip a task because it is listed as not applicable for their morphology should set `task_scores` to omit that key (do not submit `0.0` — omit entirely).

---

## Normalisation Fields in run_manifest.json

To enable cross-morphology analysis, fill in the optional `morphology_normalization` block:

```yaml
robot:
  name: "Spot-v3"
  morphology: "quadruped"
  height_m: 0.62
  mass_kg: 32.5
  leg_length_m: 0.40           # hip joint to ground contact
  morphology_normalization:
    nominal_standing_height_m: 0.62
    nominal_pelvis_height_m: 0.55
    effective_foot_width_mm: 70
    effective_foot_length_mm: 90
```

These fields are optional but strongly encouraged.  They allow TERRA maintainers to compute normalised metrics from raw trial data in post-processing.

---

## Cross-Morphology Comparison

TERRA does **not** currently define an official cross-morphology ranking.  Comparing a humanoid's TSS directly to a quadruped's TSS is not well-defined because:

- Some tasks are excluded from some tracks
- Leg geometry affects the physical difficulty
- The control problem is qualitatively different

However, the **Closed-Loop Index (CLI)** is more morphology-agnostic than TSS because it is a ratio of two task scores from the same robot.  CLI measures how much a robot degrades under expectation violation, which is a property of the control architecture rather than the morphology.  Cross-morphology comparison of CLI values is more scientifically defensible and is the comparison TERRA primarily encourages.

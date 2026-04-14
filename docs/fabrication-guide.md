# TERRA Fabrication Guide

This guide specifies materials, construction tolerances, and measurement procedures for physically replicating the TERRA benchmark apparatus.  Follow these specifications so that results from different labs remain directly comparable.

---

## Materials

### Deck and Structural Panels

| Component | Preferred Spec | Acceptable Alternative |
|-----------|---------------|----------------------|
| Flat walkway / stair tread | **18 mm Baltic birch plywood, BB/BB grade** (e.g., PureBond 18 mm or equivalent 13-ply BB birch) | 18 mm HDPE sheet (matte finish) |
| Stair riser panels | **18 mm Baltic birch plywood** | 18 mm MDF (indoors only, seal all edges) |
| Structural frame | **30×30 or 40×40 mm 6060 aluminium extrusion with M8 T-slot** (e.g., MiSUMi HFS5 series) | Welded steel SHS box section, 25×25×2 mm |
| Disturbance insert (T8) | Same panel stock as walkway; pre-routed recess for mismatch shim | — |

> **Why Baltic birch?** Consistent void-free core minimises surface warp (< 2 mm/m guaranteed), and the light natural colour provides an even photometric background without painting.

### Surface Treatments

| Task | Treatment | Product Example |
|------|-----------|----------------|
| All flat walking (T1, T2, T7, T8 nominal) | One coat satin polyurethane, sanded to 220 grit | Varathane One-Step Floor Polish, satin |
| Stair treads (T3, T4, T5) | Anti-slip clear coat: polyurethane + aluminium oxide grit (60–80 grit, 5% by weight) | Behr Premium Anti-Slip Additive mixed into Varathane WB floor finish |
| T8 low-friction insert | PTFE dry-film spray (μ = 0.25–0.35 target) | DuPont Teflon Dry Film Lubricant or Sprayon S00204 PTFE |
| Challenge variant low-contrast nosings | Tinted polyurethane to reduce nosing contrast ratio to ≤ 1.5:1 luminance vs tread | Mix with universal tint; verify with luminance meter before evaluation |

### Lane Markings and Tape

- **Centerline / start / finish box:** 25 mm matte black vinyl tape (e.g., 3M 471 or Presco Products matte vinyl)
- **Stepping corridor (T2):** 12 mm matte black vinyl tape — *not glossy*, to avoid specular cues
- **Stair nosing:** 50 mm bright yellow matte vinyl tape (standard variant); replaced with low-contrast tape for challenge variant
- **AprilTag mounts:** Flush laminate or foam-board mount; do not raise tag surface more than 3 mm above floor

---

## Target Friction Coefficients

| Task | Surface | Target μ (static) |
|------|---------|-----------------|
| T1, T2, T6, T7 (nominal) | Sealed plywood | 0.60–0.75 |
| T3, T4, T5 | Anti-slip coated plywood treads | 0.65–0.80 |
| T8 slip insert | PTFE-coated insert | 0.25–0.35 |

### Measuring Friction — 1 kg Sled Method

1. Cut a 100×100 mm piece of the same plywood stock
2. Attach a rubber sole piece (Shore A 60) to the bottom face — identical to the material on the robot's foot or test sled sole
3. Pull at constant speed (< 100 mm/s) with a spring scale or force gauge on the flat surface
4. Compute μ = F_pull / (sled weight × g).  Repeat × 3 and average.
5. Record μ and sled material in your submission's `notes` field.

> **Inclinometer alternative:** tilt the panel and record the angle θ at which the sled just begins to slide. μ = tan(θ).

---

## Flatness and Dimensional Tolerances

| Requirement | Tolerance | Measurement Method |
|-------------|-----------|-------------------|
| Flat lane panel flatness | ≤ 2 mm/m | Machinist's straightedge + feeler gauge, 5 points per panel |
| Stair riser height uniformity | ≤ 1 mm (± 0.5 mm from nominal) | Digital calipers, both ends of each riser |
| T5 anomalous riser height | 210 mm ± 2 mm | Digital calipers before each evaluation block |
| Stair tread depth | 280 mm ± 2 mm | Steel rule |
| T6 gap width (canonical) | 180 mm ± 2 mm | Steel rule at both edges and centre |
| T6 gap edge parallelism | ≤ 1 mm | Steel rule + feeler gauge |
| T2 corridor marking width | 220 mm ± 2 mm | Steel rule at 3 positions along corridor |

---

## Estimated Build Costs

These are approximate component costs in USD (2025); labor is not included.

| Tier | Tasks | Approx. Material Cost |
|------|-------|----------------------|
| **Flat-surface module** | T1, T2, T7, T8 | ~$150–200 |
| **Staircase module** (standard) | T3, T4 | ~$300–450 |
| **Staircase + anomaly module** | T5 | +$50 over T3 |
| **Gap crossing module** | T6 | ~$80–120 |
| **Full canonical suite** | T1–T8 | **~$600–900** |
| Full suite with aluminum extrusion frames | T1–T8 | **~$1,200–1,800** |

> The staircase module dominates cost. Labs that already have a standard staircase (T3/T4) can add T5 for ~$50 (one additional stair box at 210 mm riser height).

---

## Lighting

- **Preferred:** Diffuse overhead fluorescent or LED panel, 300–700 lux at task surface
- **Measure:** Lux meter at 5 positions on the task surface; record min/max in submission notes
- **Avoid:** Direct sunlight patches, point light sources creating hard shadows on stair nosings
- **Challenge variant lighting (optional add-on):** Reduce to 80–150 lux for increased visual difficulty; log actual lux values

---

## AprilTag Calibration Setup

Calibration tags are used to establish a coordinate frame for overhead camera-based foot placement measurement.

1. **Tag family:** AprilTag36h11 (48-bit, Hamming distance 9) — provides robust detection at typical evaluation room distances
2. **Tag size:** 150 mm × 150 mm printed and laminated; place flush with task surface or on a rigid elevated card ≤ 3 mm above surface
3. **Placement:** Mount 4 tags at the corners of the evaluation zone before each evaluation block
4. **Homography verification:** Solve homography from tag corners to world coordinates; verify reprojection error ≤ 2 mm at all 4 tag corners before scoring runs
5. **Removal:** Remove all tags before the trial starts — tags should not be visible to the robot during the run

**Camera requirements for overhead measurement:**
- Minimum 1080p resolution
- Field of view covers entire task zone with ≥ 10% margin on all sides
- Frame rate ≥ 30 fps
- Mount rigidly (no movement during trial)

---

## Modular Stair Box Construction

Each stair module is a self-contained 900 × 280 × h mm plywood box.

**Construction (per box):**
1. Cut two side panels: 280 mm wide × h mm tall × 18 mm thick Baltic birch
2. Cut one top tread: 900 × 280 mm × 18 mm Baltic birch
3. Assemble with wood glue and 4× M5 × 40 mm machine screws through countersunk holes
4. Verify height after assembly: measure at 4 corners, tolerance ≤ 1 mm
5. Apply anti-slip coating; let cure ≥ 24 h before use
6. Mark tread nosing with 50 mm yellow matte vinyl tape, flush with front edge

**Anomaly module (T5):**  Identical to standard module but riser height is 210 mm instead of 170 mm.  Mark module with a small colour dot on the underside (not visible to robot) to distinguish it from standard modules in storage.

---

## Safety

- Assign one spotter per robot during development and warm-up runs — spotter intervention invalidates a scored trial
- Confirm all stair modules are mechanically latched before any ascent or descent trial
- Inspect all tread coatings and nosing tapes before each evaluation block; replace any visibly worn tape
- Ensure the T8 low-friction insert is fully seated and flush before each trial; an unseated insert creates an uncontrolled tripping hazard
- Log any safety incidents in the submission `notes` field, even if the trial was not scored

---

## Pre-Evaluation Checklist

Before each scored evaluation block:

- [ ] All dimensional tolerances verified with calipers/straightedge
- [ ] Surface friction measured and within spec
- [ ] AprilTag homography reprojection error ≤ 2 mm
- [ ] Camera recording started and field of view verified
- [ ] Robot sensors calibrated in evaluation environment (IMU, camera white balance)
- [ ] Ambient light measured (lux) and recorded
- [ ] Safety spotter briefed on when to intervene (robot contacts spotter or human safety barrier)
- [ ] Baseline trial (robot standing still) logged to verify timestamp synchronisation

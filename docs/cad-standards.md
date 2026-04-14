# CAD Standards and Contribution Guide

This document defines the conventions for TERRA CAD files so that models contributed by different labs remain consistent and mutually compatible.

---

## Directory Structure

CAD files live inside the relevant task directory:

```
tasks/
└── T3_standard_ascent/
    └── cad/
        ├── stair_module_900x280x170.step      ← primary deliverable
        ├── stair_module_900x280x170.FCStd     ← parametric source (FreeCAD)
        └── README.md                          ← origin, software version, parameter table
tasks/
└── T5_height_anomaly/
    └── cad/
        ├── anomaly_module_900x280x210.step
        ├── anomaly_module_900x280x210.FCStd
        └── README.md
```

---

## File Formats

| Format | Purpose | Required? |
|--------|---------|----------|
| `.step` (AP214) | Universal exchange — works in FreeCAD, Fusion 360, SolidWorks, CATIA, OpenSCAD | **Required for all contributed models** |
| `.FCStd` | FreeCAD parametric source — preferred for version control and modification | Strongly recommended |
| `.f3d` | Fusion 360 source | Optional |
| `.stl` | Mesh only — do not use as primary format, dimensions are not guaranteed | Not accepted as primary |

---

## Coordinate System

All TERRA models use a **right-handed coordinate system with Z up**:

- **+X:** forward (direction of robot travel)
- **+Y:** left
- **+Z:** up

Origin is placed at the **bottom-front-left corner** of the module (standing at ground level looking forward).

---

## Naming Convention

Files are named with the task ID and the critical dimension:

```
<task-slug>_<width>x<depth>x<height>.step
```

Examples:
- `stair_module_900x280x170.step` — one stair tread box, 900 mm wide, 280 mm deep, 170 mm riser
- `anomaly_module_900x280x210.step` — anomaly riser box, 210 mm height
- `gap_crossing_apparatus_1380x600.step` — full T6 gap crossing apparatus, 1380 mm total length, 600 mm width

All dimensions in millimetres.

---

## Parametric Model Requirements

FreeCAD source models must:

1. Use the **FreeCAD Part Design** workbench with a single sketch-driven body per assembly component
2. Include a **Spreadsheet** named `Parameters` with all driving dimensions as named cells:
   - `width_mm`, `depth_mm`, `height_mm`, `panel_thickness_mm`
3. **Not embed absolute paths** — use relative references only
4. Be compatible with **FreeCAD 0.21 or later**

---

## Tolerances in CAD

CAD models should represent the **nominal geometry** (not worst-case).  Tolerances are specified in `task_spec.yaml` and documented in `docs/fabrication-guide.md`.  Do not add tolerance offsets to the CAD geometry itself.

---

## How to Contribute a CAD File

1. Create the model following the conventions above
2. Export a `.step` (AP214) file and verify it imports cleanly in FreeCAD, Fusion 360, or any other CAD tool
3. Add a `README.md` in the `cad/` directory:

```markdown
# CAD: stair_module_900x280x170

**Task:** T3 Standard Ascent
**Author:** Your Name / Lab
**Date:** YYYY-MM-DD
**Software:** FreeCAD 0.21 / Fusion 360 / etc.
**STEP version:** AP214

## Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| width_mm | 900 | Clear tread width |
| depth_mm | 280 | Tread depth (horizontal run) |
| height_mm | 170 | Riser height (vertical rise) |
| panel_thickness_mm | 18 | Plywood panel thickness |

## Notes

Any deviations or special instructions.
```

4. Open a pull request — CI does not currently check CAD files, but maintainers will verify the STEP import before merging

---

## Priority CAD Deliverables

The highest-value models for the community (complex geometry, most likely to be built incorrectly):

| Priority | File | Reason |
|----------|------|--------|
| **1** | `tasks/T3_standard_ascent/cad/stair_module_900x280x170.step` | Most common build target; used by T3, T4, T5 |
| **2** | `tasks/T5_height_anomaly/cad/anomaly_module_900x280x210.step` | Identical to above but 210 mm riser — easy to confuse |
| **3** | `tasks/T6_discrete_crossing/cad/gap_crossing_apparatus_1380x600.step` | Gap geometry requires precise edge alignment |
| **4** | `tasks/T8_mild_recovery/cad/disturbance_insert_300x600.step` | Swap-in insert must be flush with nominal panel |

---

## Version Control for CAD

CAD files are versioned alongside the rest of the repository.

- **PATCH** version bumps (e.g., v2.0.1) are appropriate for CAD corrections that do not change nominal geometry
- **MINOR** version bumps introduce new CAD files
- **MAJOR** version bumps change task geometry — this is rare and will be announced with ≥ 6 months notice

See `docs/versioning-policy.md` for the full versioning policy.

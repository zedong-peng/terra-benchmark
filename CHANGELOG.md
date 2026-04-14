# Changelog

All notable changes to TERRA are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
TERRA uses [Semantic Versioning](docs/versioning-policy.md):
- **MAJOR** — task geometry changes (rare; announced 6 months in advance)
- **MINOR** — new tasks, new morphology tracks, new suite-level metrics
- **PATCH** — documentation, CAD, measurement protocol clarifications, schema bugfixes

---

## [2.0.0] — 2025-04-01

### Added

- **TERRA identity** — project renamed from "embodied-mobility-benchmark" to TERRA (Terrain-Engaged Robot Reasoning Assessment)
- **Multi-morphology support** — `run_manifest.json` now accepts `quadruped`, `wheeled_legged`, and `other` morphologies in addition to `humanoid` / `biped`; `run_manifest.schema.json` updated accordingly
- **Closed-Loop Index (CLI)** — new suite-level metric: `CLI = (T5 + T8) / (T1 + T3)`.  Measures how much a system degrades when terrain predictions are violated
- **TERRA Standard Score (TSS)** — weighted suite average: `(T1 + T2 + T3 + T4 + 2×T5 + T6 + T7 + 2×T8) / 10`; closed-loop tasks T5 and T8 double-weighted
- **`benchmark/score.py evaluate-suite`** — new CLI command that computes TSS and CLI across a full baseline directory
- **`docs/measurement-protocol.md`** — comprehensive operational definitions for all 6 metrics with three compliant measurement methods per metric (MoCap, pressure plate, overhead camera + AprilTag)
- **`schemas/leaderboard_entry.schema.json`** — JSON Schema for community leaderboard submissions
- **`leaderboard/`** directory — PR-based community leaderboard with seed entries from both reference baselines; `scripts/build_leaderboard.py` auto-regenerates `leaderboard.json` on merge
- **`.github/workflows/validate.yml`** — CI validates all leaderboard entries and task specs on pull request
- **`.github/workflows/leaderboard.yml`** — CI regenerates `leaderboard.json` after entry merge
- **`.github/ISSUE_TEMPLATE/`** — templates for leaderboard submissions and task proposals
- **`docs/morphology-normalization.md`** — cross-morphology comparison methodology and normalisation definitions
- **`docs/cad-standards.md`** — CAD file conventions, coordinate system, parametric model requirements, and contribution workflow
- **`docs/versioning-policy.md`** — SemVer semantics with geometry-freeze commitments
- **`CITATION.cff`** — standard academic citation metadata (CFF 1.2.0)
- **`docs/paper-template/`** — LaTeX table template and required disclosure checklist for papers reporting TERRA results
- **`sequences/TERRA-Standard-Chain.yaml`** — canonical 4-task evaluation chain (T1 → T3 → T5 → T8) for rapid closed-loop assessment
- **`task_spec.yaml`** updates — all 8 task specs now include `tier: standard`, `terra_version: "2.0"`, `morphology_tracks`, `tss_weight`, and quantified challenge variant descriptions

### Changed

- **`schemas/score_report.schema.json`** — added optional `morphology_track`, `build_variant`, `tss_contribution`, and `cli` fields
- **`schemas/task_spec.schema.json`** — added `tier`, `terra_version`, `morphology_tracks`, `tss_weight` fields
- **`schemas/run_manifest.schema.json`** — `morphology` enum expanded; `height_m` minimum lowered to 0.2; `mass_kg` minimum lowered to 1.0; added optional `leg_length_m` and `morphology_normalization` fields
- **`benchmark/spec_data.py`** — added `TSS_WEIGHTS`, `TSS_DENOMINATOR`, `CLI_NUMERATOR_TASKS`, `CLI_DENOMINATOR_TASKS`, `TERRA_VERSION`, `NOMINAL_TASKS`, `CLOSED_LOOP_TASKS` constants
- **`pyproject.toml`** — renamed package to `terra-benchmark`, bumped version to `2.0.0`, added optional `[dev]` extras, added project URLs
- **`docs/fabrication-guide.md`** — fully rewritten with specific product names, friction measurement procedure (1 kg sled method), per-task surface treatment table, and cost estimates (~$600–900 full canonical suite)
- **`README.md`** — complete rewrite: TERRA identity, scientific claim, 8-task table, quickstart (3 commands), TSS/CLI formulas, leaderboard section, bibtex block
- **`blog.md`** — expanded to scientific manifesto; formal closed-loop hypothesis; CLI baseline comparison (sim CLI=0.537 vs physical CLI=0.765); roadmap

### Fixed

- `compute_task_score()` now correctly handles `energy_proxy = -1.0` (metric unavailable) by zeroing the energy penalty rather than applying a penalty on a sentinel value

---

## [0.1.0] — 2025-03-01

### Added

- Initial repository with 8 Standard tasks (T1–T8)
- `task_spec.yaml` format with geometry, tolerances, BOM, assembly steps
- Three task variants: canonical, parametric, challenge
- `benchmark/score.py` with per-task scoring formula: `S × (1 − 0.15·C − 0.10·R − 0.05·E)`
- JSON Schema validation for `run_manifest.json`, `trial_metrics`, and `score_report.json`
- Reference baselines: `sim_baseline` (MuJoCo) and `real_robot_baseline` (Unitree H1)
- `docs/fabrication-guide.md` and `docs/benchmark-spec.md`
- SVG apparatus diagrams for each task

# TERRA Versioning Policy

TERRA uses [Semantic Versioning](https://semver.org/) with domain-specific definitions for what constitutes a breaking change.

---

## Version Number Semantics

```
TERRA v<MAJOR>.<MINOR>.<PATCH>
```

| Component | Triggers | Example |
|-----------|----------|---------|
| **MAJOR** | Any change to the physical geometry of an existing task (riser height, tread depth, gap width, obstacle height, etc.) | v2.0 → v3.0 |
| **MINOR** | New tasks, new morphology tracks, new suite-level metrics, new schema fields that expand expressiveness | v2.0 → v2.1 |
| **PATCH** | Documentation updates, CAD file additions or corrections that do not change nominal geometry, schema bugfixes, measurement protocol clarifications, new leaderboard entries | v2.0 → v2.0.1 |

### The Geometry-Freeze Guarantee

Once a task is published in a **MAJOR** release, its **nominal physical geometry is frozen** until the next MAJOR release.  This means:

- `stair_count`, `riser_height_mm`, `tread_depth_mm`, `clear_width_mm`, `anomaly_step_index`
- `walkway_length_mm`, `walkway_width_mm`, `gap_length_mm`, `obstacle_height_mm`, etc.

**will not change** within a MAJOR version.

This guarantee mirrors the ImageNet contract: if you build the TERRA v2.0 apparatus today, your results will be directly comparable to results published three years from now, as long as both use `terra_version: "2.0"`.

> **Tolerances and surface specs** are not part of the geometry freeze and may receive PATCH-level clarifications.

---

## MAJOR Version Announcements

MAJOR version bumps follow this process:

1. **Proposal phase (public RFC):** ≥ 6 months before the MAJOR release, a GitHub Discussion is opened with the proposed geometry changes and scientific rationale
2. **Community comment period:** ≥ 2 months for labs to comment, request modifications, or flag incompatibilities
3. **Release candidate:** Tagged `v3.0.0-rc1` for validation; labs can report problems for ≥ 1 month
4. **Final release:** Tagged `v3.0.0`; all existing `terra_version: "2.0"` results remain valid and distinct from v3.0 results
5. **Continued support:** v2.0 leaderboard entries are preserved indefinitely in a version-tagged section of the leaderboard

---

## Task-Level Version Tracking

Individual tasks carry their own version inside `task_spec.yaml`:

```yaml
terra_version: "2.0"
```

This allows the benchmark to evolve tasks independently in future MINOR releases (e.g., adding a new task T9 with `terra_version: "2.1"`).  All 8 Standard tasks are at `terra_version: "2.0"` in the current release.

---

## Schema Compatibility

JSON Schemas are versioned with the benchmark.  Schema changes follow these rules:

- **Non-breaking** (PATCH): adding optional fields, relaxing constraints
- **Breaking** (MAJOR or MINOR with migration guide): removing required fields, renaming fields, tightening constraints

The `benchmark_version` field in `run_manifest.json` and leaderboard entries records which schema version was used.

---

## Leaderboard Versioning

Leaderboard entries include `benchmark_version: "2.0"`.  When a new MAJOR version is released:

1. Existing entries stay in the `v2.0` archive section
2. The primary leaderboard switches to show `v3.0` entries
3. Cross-version comparison is explicitly not recommended (geometry changed)

CLI values are more robust to cross-version comparison than TSS, because CLI is a ratio of scores from the same robot on the same evaluation run.

---

## Reference

- Current benchmark version: **2.0**
- Geometry freeze date: 2025-04-01
- Next planned MAJOR review: *no date set — geometry changes require community consensus*

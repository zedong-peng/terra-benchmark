# TERRA Leaderboard

The TERRA leaderboard is a **community-curated table of evaluation results** across all robot morphologies. It lives entirely in this repository — no server, no login, no API keys. Results are submitted as JSON files via pull request and validated automatically by CI.

## Current Rankings

> Rankings below are **illustrative seed entries** from the TERRA v2.0 release baselines.
> Submit your robot's results to appear here.

### Standard Track — All Tasks (TSS, canonical variant)

| Rank | Robot | Lab | Morphology | TSS ↓ | CLI | Tasks | Date |
|------|-------|-----|-----------|-------|-----|-------|------|
| — | H1-LabBaseline | TERRA-Ref | humanoid | 0.7737 | 0.7648 | T1–T8 | 2025-04-01 |
| — | AtlasSim-LocoPolicy | TERRA-Ref | humanoid | 0.7019 | 0.5370 | T1–T8 | 2025-04-01 |

**TSS** = TERRA Standard Score = `(T1 + T2 + T3 + T4 + 2×T5 + T6 + T7 + 2×T8) / 10`
**CLI** = Closed-Loop Index = `(T5 + T8) / (T1 + T3)` — measures degradation under expectation violation

> The simulation baseline's CLI of **0.537** vs the physical robot's **0.765** illustrates the core finding: current systems degrade significantly when terrain predictions are violated. Most systems score CLI < 0.80 — that gap is the benchmark's raison d'être.

---

## How to Submit

See [SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md) for the full process. The short version:

1. Run the full TERRA suite on your robot
2. Create a JSON file in `leaderboard/entries/` following the schema
3. Open a pull request — CI validates your entry automatically
4. After merge, the leaderboard updates automatically

---

## Schema

All entries must validate against [`schemas/leaderboard_entry.schema.json`](../schemas/leaderboard_entry.schema.json).

Minimum required fields:

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
    "T1": 0.95,
    "T5": 0.71,
    "T8": 0.68
  }
}
```

`tss` and `cli` are **auto-computed from `task_scores` on merge** — you do not need to supply them.

---

## Morphology Tracks

Results are grouped by morphology. Each track is ranked independently:

| Track | Description |
|-------|-------------|
| `humanoid` | Upright bipeds with human-like proportions |
| `biped` | Other upright bipeds (non-humanoid leg geometry) |
| `quadruped` | Four-legged robots (dog-style) |
| `wheeled_legged` | Hybrid wheeled-leg systems |
| `other` | Any other morphology (please describe in `notes`) |

Some tasks are not applicable to all morphologies (see each `task_spec.yaml` → `morphology_tracks`).

---

## Integrity

- All submitted results are **self-reported**. TERRA does not independently verify evaluations.
- Each entry **must** include `measurement_methods` codes (see `docs/measurement-protocol.md`) to allow readers to assess comparability.
- Entries that do not disclose measurement method are flagged `[unverified]`.
- The TERRA maintainers reserve the right to remove entries that appear to violate the measurement protocol or misrepresent conditions.

---

## Questions?

Open an issue using the [Leaderboard Submission template](../.github/ISSUE_TEMPLATE/leaderboard_submission.md) or start a GitHub Discussion.

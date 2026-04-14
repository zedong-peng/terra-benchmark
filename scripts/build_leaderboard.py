#!/usr/bin/env python3
"""
Build leaderboard/leaderboard.json from individual entries in leaderboard/entries/.

Called by GitHub Actions after a new entry is merged into main.
Can also be run locally:

    python3 scripts/build_leaderboard.py
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
ENTRIES_DIR = ROOT / "leaderboard" / "entries"
OUTPUT_PATH = ROOT / "leaderboard" / "leaderboard.json"
SCHEMA_PATH = ROOT / "schemas" / "leaderboard_entry.schema.json"

# TSS weights and denominator (must match spec_data.py)
TSS_WEIGHTS = {"T1": 1, "T2": 1, "T3": 1, "T4": 1, "T5": 2, "T6": 1, "T7": 1, "T8": 2}
TSS_DENOMINATOR = 10.0
CLI_NUMERATOR = ["T5", "T8"]
CLI_DENOMINATOR = ["T1", "T3"]

TERRA_VERSION = "2.0"


def compute_tss(task_scores: dict) -> Optional[float]:
    weighted = sum(task_scores.get(t, 0) * w for t, w in TSS_WEIGHTS.items())
    available_weight = sum(w for t, w in TSS_WEIGHTS.items() if t in task_scores)
    if available_weight == 0:
        return None
    # Scale proportionally if partial suite
    return round(weighted / TSS_DENOMINATOR, 4)


def compute_cli(task_scores: dict) -> Optional[float]:
    for t in CLI_NUMERATOR + CLI_DENOMINATOR:
        if t not in task_scores:
            return None
    denom = sum(task_scores[t] for t in CLI_DENOMINATOR)
    if denom == 0:
        return None
    return round(sum(task_scores[t] for t in CLI_NUMERATOR) / denom, 4)


def load_entries() -> list[dict]:
    entries = []
    for path in sorted(ENTRIES_DIR.glob("*.json")):
        if path.name.startswith("."):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                entry = json.load(f)
        except Exception as e:
            print(f"  Warning: could not load {path.name}: {e}", file=sys.stderr)
            continue

        # Auto-compute tss and cli if not provided
        scores = entry.get("task_scores", {})
        if "tss" not in entry:
            entry["tss"] = compute_tss(scores)
        if "cli" not in entry:
            entry["cli"] = compute_cli(scores)

        entries.append(entry)
    return entries


def build_leaderboard(entries: list[dict]) -> dict:
    # Sort by TSS descending (None goes to bottom), then CLI descending
    def sort_key(e):
        tss = e.get("tss") or -1.0
        cli = e.get("cli") or -1.0
        return (-tss, -cli)

    entries_sorted = sorted(entries, key=sort_key)
    return {
        "terra_version": TERRA_VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "entries": entries_sorted,
    }


def main():
    print(f"Scanning {ENTRIES_DIR} ...")
    entries = load_entries()
    print(f"  Loaded {len(entries)} entry(ies).")

    leaderboard = build_leaderboard(entries)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, indent=2)
        f.write("\n")

    print(f"Wrote {OUTPUT_PATH}")

    # Print summary table
    print(f"\n{'Rank':<5} {'Robot':<30} {'Morphology':<15} {'TSS':>6} {'CLI':>6} {'Tasks'}")
    print("-" * 70)
    for rank, e in enumerate(leaderboard["entries"], start=1):
        tss = f"{e['tss']:.4f}" if e.get("tss") is not None else "  N/A"
        cli = f"{e['cli']:.4f}" if e.get("cli") is not None else "  N/A"
        n_tasks = len(e.get("task_scores", {}))
        print(f"{rank:<5} {e['robot_name']:<30} {e['morphology']:<15} {tss:>6} {cli:>6}  {n_tasks}/8")


if __name__ == "__main__":
    main()

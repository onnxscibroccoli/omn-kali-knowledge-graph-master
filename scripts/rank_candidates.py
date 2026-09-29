#!/usr/bin/env python3
"""Score external candidates. Scoring is heuristic, not proof."""
from __future__ import annotations
import argparse
from pathlib import Path
import yaml
PERMISSIVE = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "PostgreSQL", "MPL-2.0"}

def score(item: dict) -> int:
    points = 0
    license_id = str(item.get("license") or "")
    if license_id in PERMISSIVE:
        points += 2
    if item.get("statusTag") == "OBSERVED":
        points += 2
    if item.get("statusTag") == "PROVEN":
        points += 4
    if item.get("stars"):
        points += min(int(item["stars"]) // 1000, 5)
    return points

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="external/candidates.yml")
    args = parser.parse_args()
    data = yaml.safe_load(Path(args.path).read_text(encoding="utf-8"))
    rows = []
    for group in data.get("groups", []):
        related = group.get("relatedTo")
        for cand in group.get("candidates", []):
            rows.append((score(cand), related, cand.get("name"), cand.get("statusTag"), cand.get("license")))
    rows.sort(reverse=True)
    print(f"{'score':>5}  {'repo':<24} {'tag':<12} {'license':<16} name")
    for sc, related, name, tag, lic in rows:
        print(f"{sc:5}  {str(related)[:24]:<24} {str(tag):<12} {str(lic)[:16]:<16} {name}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

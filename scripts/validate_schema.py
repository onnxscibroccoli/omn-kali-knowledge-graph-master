#!/usr/bin/env python3
"""Validate omnikali/*.yml against .omnikali-schema.yml."""
from __future__ import annotations
import sys
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / ".omnikali-schema.yml"
ENTRIES = ROOT / "omnikali"

def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)

def main() -> int:
    schema = load_yaml(SCHEMA_PATH)
    required = schema["required"]
    enums = schema["enums"]
    errors = []
    files = sorted(ENTRIES.glob("*.yml"))
    if not files:
        errors.append("no omnikali/*.yml entries found")
    for path in files:
        data = load_yaml(path) or {}
        for field in required:
            if field not in data or data[field] in (None, ""):
                errors.append(f"{path.name}: missing {field}")
        for field, allowed in enums.items():
            if field in data and data[field] not in allowed:
                errors.append(f"{path.name}: {field}={data[field]!r} not in {allowed}")
    if errors:
        print("SCHEMA INVALID")
        for err in errors:
            print(f" - {err}")
        return 1
    print(f"SCHEMA OK ({len(files)} entries)")
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate every registry entry against the adjacent JSON Schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=Path)
    parser.add_argument("registry", type=Path)
    args = parser.parse_args()

    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    failures = []
    for index, entry in enumerate(registry.get("entries", [])):
        for error in validator.iter_errors(entry):
            failures.append(f"entries[{index}]: {error.message}")

    if failures:
        print("\n".join(failures))
        return 1

    print(f"validated {len(registry.get('entries', []))} registry entries")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

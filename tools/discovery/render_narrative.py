#!/usr/bin/env python3
"""Render deterministic plain-text tool discovery narrative from registry JSON."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

def render(registry: dict) -> str:
    entries = registry.get("entries", [])
    by_repo = defaultdict(list)
    for entry in entries:
        by_repo[entry["repository"]].append(entry)

    lines = [
        "OmniKali Repository Tool Discovery Narrative",
        "Generated from the repository tool registry.",
        "Discovery describes source artifacts. It does not grant execution authority.",
        "",
        f"Repository count is {len(by_repo)}.",
        f"Discovered tool count is {len(entries)}.",
        "",
    ]

    for repo in sorted(by_repo):
        items = sorted(by_repo[repo], key=lambda x: x["path"])
        lines.append(f"Repository {repo} contains {len(items)} discovered tool candidates.")
        kinds = Counter(item.get("kind", "unknown") for item in items)
        kind_text = ", ".join(f"{count} {kind}" for kind, count in sorted(kinds.items()))
        lines.append(f"The repository contains {kind_text}.")
        for item in items:
            signals = item.get("discovery", {}).get("signals", [])
            signal_text = ", ".join(signals) if signals else "no additional discovery signals"
            qualification = item.get("qualification", {})
            quality = qualification.get("quality", "NOT_CLASSIFIED")
            purpose = qualification.get("intended_purpose", "No intended purpose recorded.")
            replacement = qualification.get("replacement_tool_id")
            lineage = f" A related validated tool is {replacement}." if replacement else ""
            lines.append(
                f"The tool at {item['path']} is classified as {item.get('kind', 'unknown')}. "
                f"The scanner identified it using {signal_text}. "
                f"Its runtime evidence status is {item.get('evidence', {}).get('status', 'NOT_PROVEN')}. "
                f"Its qualification quality is {quality}. "
                f"Its intended purpose is {purpose}.{lineage} "
                f"The source reference is {item.get('source', {}).get('ref', 'unknown')} "
                f"at commit {item.get('source', {}).get('sha', 'unknown')}."
            )
        lines.append("")

    lines.extend([
        "The discovery registry remains descriptive metadata.",
        "Execution authority remains with the owning control plane and its existing contracts.",
        "Missing runtime evidence remains NOT_PROVEN.",
        "",
    ])
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(render(registry), encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Read-only repository tool discovery prototype.

The engine catalogs likely executable tools. It never executes discovered tools,
changes repository state, or grants execution authority.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import stat
import sys
from pathlib import Path

SCHEMA_VERSION = "omnikali.tool-manifest/v1"
DEFAULT_IGNORES = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache", "dist", "build"}
SHEBANGS = {
    "python": re.compile(r"^#!.*\bpython(?:3)?(?:\s|$)"),
    "bash": re.compile(r"^#!.*\bbash(?:\s|$)"),
    "sh": re.compile(r"^#!.*\b(?:ba)?sh(?:\s|$)"),
}

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""

def python_signals(path: Path, text: str) -> list[str]:
    signals = []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return signals
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    imports = {
        alias.name.split(".")[0]
        for node in ast.walk(tree) if isinstance(node, ast.Import)
        for alias in node.names
    }
    imports |= {
        node.module.split(".")[0]
        for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module
    }
    if names & {"ArgumentParser", "click", "typer"} or imports & {"argparse", "click", "typer"}:
        signals.append("python-cli-framework")
    if "FastMCP" in text or "mcp.server" in text or "tools/list" in text:
        signals.append("mcp-pattern")
    if ast.get_docstring(tree):
        signals.append("python-module-docstring")
    return signals

def classify(path: Path, text: str) -> tuple[str, str, list[str]]:
    suffix = path.suffix.lower()
    first = text.splitlines()[0] if text.splitlines() else ""
    signals = []
    if suffix == ".py":
        signals = python_signals(path, text)
        if "mcp-pattern" in signals:
            return "mcp", "python", signals
        if "python-cli-framework" in signals:
            return "cli", "python", signals
        return "script", "python", signals
    if suffix in {".sh", ".bash"} or any(rx.match(first) for rx in SHEBANGS.values()):
        if "python-cli-framework" not in signals and ("$@" in text or "getopts" in text or "case " in text):
            signals.append("shell-cli-pattern")
        return "script", "bash" if "bash" in first else "sh", signals
    if suffix in {".yml", ".yaml"}:
        if re.search(r"(?m)^\s*-?\s*hosts\s*:", text) or re.search(r"(?m)^\s*ansible\.", text):
            signals.append("ansible-pattern")
            return "playbook", "yaml", signals
        if re.search(r"(?m)^\s*(name|on|jobs|steps)\s*:", text):
            signals.append("workflow-pattern")
            return "workflow", "yaml", signals
        return "unknown", "yaml", signals
    return "unknown", "unknown", signals

def executable_candidate(path: Path, text: str) -> bool:
    try:
        mode = path.stat().st_mode
    except OSError:
        return False
    return bool(mode & stat.S_IXUSR) or text.startswith("#!")

def manifest(repo: str, ref: str, source_sha: str, root: Path, path: Path) -> dict:
    text = read_text(path)
    kind, language, signals = classify(path, text)
    method = (
        "mcp-schema" if "mcp-pattern" in signals else
        "cli-framework" if "python-cli-framework" in signals else
        "yaml-playbook" if "ansible-pattern" in signals else
        "shebang" if text.startswith("#!") else
        "unknown"
    )
    relative_path = path.relative_to(root).as_posix()
    tool_id = f"{repo}/{relative_path}"
    return {
        "schema_version": SCHEMA_VERSION,
        "tool_id": tool_id.lower(),
        "repository": repo,
        "path": relative_path,
        "kind": kind,
        "language": language,
        "source": {"ref": ref, "sha": source_sha},
        "interface": {},
        "ownership": {},
        "evidence": {
            "status": "NOT_PROVEN",
            "tests": [],
            "notes": "Discovery evidence only. Runtime capability and authorization remain unproven."
        },
        "discovery": {
            "method": method,
            "confidence": "medium" if signals else "low",
            "signals": signals
        }
    }

def scan(root: Path, repo: str, ref: str, source_sha: str) -> list[dict]:
    results = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in DEFAULT_IGNORES for part in path.parts):
            continue
        text = read_text(path)
        if executable_candidate(path, text) or path.suffix.lower() in {".py", ".sh", ".bash", ".yml", ".yaml"}:
            item = manifest(repo, ref, source_sha, root, path)
            if item["kind"] != "unknown" or item["discovery"]["signals"]:
                results.append(item)
    return results

def main() -> int:
    parser = argparse.ArgumentParser(description="Catalog repository tools without executing them.")
    parser.add_argument("root", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--ref", default="unknown")
    parser.add_argument("--source-sha", default="unknown")
    parser.add_argument("--output", type=Path, default=Path("-"))
    args = parser.parse_args()
    if args.output == Path("-"):
        json.dump(scan(args.root, args.repository, args.ref, args.source_sha), sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        args.output.write_text(json.dumps(scan(args.root, args.repository, args.ref, args.source_sha), indent=2) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

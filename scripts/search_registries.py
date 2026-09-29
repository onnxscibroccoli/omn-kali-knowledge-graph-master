#!/usr/bin/env python3
"""Best-effort public registry search. Results are HYPOTHESIS until reviewed."""
from __future__ import annotations
import argparse, json, sys
from typing import Any
import requests
UA = {"User-Agent": "omn-kali-kg-research/0.1"}

def get(url: str) -> Any:
    resp = requests.get(url, headers=UA, timeout=30)
    resp.raise_for_status()
    return resp.json()

def search_github(query: str):
    data = get(f"https://api.github.com/search/repositories?q={query}&per_page=5")
    return [{
        "ecosystem": "GitHub",
        "name": item.get("full_name"),
        "url": item.get("html_url"),
        "stars": item.get("stargazers_count"),
        "license": (item.get("license") or {}).get("spdx_id"),
        "statusTag": "HYPOTHESIS",
    } for item in data.get("items", [])]

def search_npm(query: str):
    data = get(f"https://registry.npmjs.com/-/v1/search?text={query}&size=5")
    out = []
    for obj in data.get("objects", []):
        pkg = obj.get("package") or {}
        out.append({
            "ecosystem": "npm",
            "name": pkg.get("name"),
            "url": (pkg.get("links") or {}).get("npm"),
            "version": pkg.get("version"),
            "statusTag": "HYPOTHESIS",
        })
    return out

def search_pypi(name: str):
    try:
        data = get(f"https://pypi.org/pypi/{name}/json")
    except requests.HTTPError:
        return []
    info = data.get("info") or {}
    return [{
        "ecosystem": "PyPI",
        "name": info.get("name"),
        "url": info.get("project_url") or info.get("home_page"),
        "license": info.get("license"),
        "version": info.get("version"),
        "statusTag": "HYPOTHESIS",
    }]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--github", action="store_true")
    parser.add_argument("--npm", action="store_true")
    parser.add_argument("--pypi", action="store_true")
    args = parser.parse_args()
    if not (args.github or args.npm or args.pypi):
        args.github = args.npm = True
    results = []
    if args.github:
        results.extend(search_github(args.query))
    if args.npm:
        results.extend(search_npm(args.query))
    if args.pypi:
        results.extend(search_pypi(args.query))
    json.dump({"query": args.query, "results": results}, sys.stdout, indent=2)
    print()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

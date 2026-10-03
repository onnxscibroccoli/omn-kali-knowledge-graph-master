#!/usr/bin/env python3
"""List repositories for an owner via GitHub REST."""
from __future__ import annotations
import argparse, json, os, sys
from pathlib import Path
from typing import Any
from urllib.parse import quote
import requests
API = "https://api.github.com"

def session() -> requests.Session:
    s = requests.Session()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "omn-kali-kg-crawler"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    s.headers.update(headers)
    return s

def get_json(s: requests.Session, url: str) -> Any:
    resp = s.get(url, timeout=30)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()

def _paginate(s: requests.Session, url: str):
    repos = []
    page = 1
    joiner = "&" if "?" in url else "?"
    while True:
        batch = get_json(s, f"{url}{joiner}page={page}") or []
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos

def list_repos(s: requests.Session, owner: str):
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    # /users/{owner}/repos is public-only even with a token. Authenticated
    # /user/repos?affiliation=owner includes private owner repositories.
    if token:
        repos = _paginate(s, f"{API}/user/repos?per_page=100&affiliation=owner&sort=updated")
        wanted = owner.lower()
        return [r for r in repos if (r.get("owner") or {}).get("login", "").lower() == wanted]
    return _paginate(s, f"{API}/users/{quote(owner)}/repos?per_page=100&type=all&sort=updated")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", default="onnxscibroccoli")
    parser.add_argument("--out", default="inventory")
    args = parser.parse_args()
    repos = list_repos(session(), args.owner)
    snapshot = {
        "owner": args.owner,
        "total": len(repos),
        "private": sum(1 for r in repos if r.get("private")),
        "public": sum(1 for r in repos if not r.get("private")),
        "repos": [{
            "name": r.get("name"),
            "private": r.get("private"),
            "html_url": r.get("html_url"),
            "description": r.get("description"),
            "language": r.get("language"),
            "pushed_at": r.get("pushed_at"),
            "open_issues_count": r.get("open_issues_count"),
        } for r in repos],
    }
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    dest = out / "repos-latest.json"
    dest.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {dest} ({snapshot['total']} repos, {snapshot['private']} private)")
    return 0

if __name__ == "__main__":
    sys.exit(main())

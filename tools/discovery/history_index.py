#!/usr/bin/env python3
"""Attach non-evidentiary Git history to discovered candidates."""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path

def history_for(root: Path, path: str) -> dict:
    try:
        out=subprocess.check_output(
            ["git","-C",str(root),"log","--all","--format=%H","--",path],
            text=True,stderr=subprocess.DEVNULL
        )
    except (OSError,subprocess.CalledProcessError):
        return {"commit_count":0,"first_seen_commit":None,"last_changed_commit":None,"historical_changes":False}
    commits=[x.strip() for x in out.splitlines() if x.strip()]
    return {
        "commit_count":len(commits),
        "first_seen_commit":commits[-1] if commits else None,
        "last_changed_commit":commits[0] if commits else None,
        "historical_changes":bool(commits)
    }

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("registry",type=Path)
    p.add_argument("repos_root",type=Path)
    p.add_argument("scope",type=Path)
    p.add_argument("output",type=Path)
    a=p.parse_args()
    registry=json.loads(a.registry.read_text())
    scope=json.loads(a.scope.read_text())
    roots={x["repository"]:a.repos_root/x["repository"].split("/",1)[1] for x in scope["repositories"] if x.get("enabled",True) and x.get("access")=="public"}
    cache={}
    for e in registry.get("entries",[]):
        repo=e["repository"]; path=e["path"]
        key=(repo,path)
        if key not in cache:
            root=roots.get(repo)
            cache[key]=history_for(root,path) if root and root.exists() else {"commit_count":0,"first_seen_commit":None,"last_changed_commit":None,"historical_changes":False}
        e["history"]=cache[key]
    a.output.write_text(json.dumps(registry,indent=2)+"\n")
    print(f"indexed history for {len(registry.get('entries',[]))} candidates")
    return 0
if __name__=="__main__":
    raise SystemExit(main())

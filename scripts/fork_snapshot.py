#!/usr/bin/env python3
"""Read each fork against its upstream: how far ours is ahead, and which files we changed (WP5c D-3).

Read-only: `gh` GET requests only (WP5c R-4). For every fork in the snapshot, one compare of the upstream's default
branch with ours (`GET /repos/{org}/{fork}/compare/{upstream_owner}:{base}...{org}:{head}`): commits ahead (ours, not upstream's) and
behind, and the files our commits changed. A fork's own commit counts in the snapshot include the upstream's history,
so they can't tell a plain copy from an exploration; this can, for the default branch (the supervisor: "its probably worth inspecting the
upstream, and our diff from the upstream to help classify").

Usage: python3 scripts/fork_snapshot.py [--snapshot data/snapshots/2026-10-18]
Writes <snapshot>/forks.json, keyed by repository ID, with when it was read.
"""
import argparse
import datetime
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model  # noqa: E402

MODEL_SUFFIXES = (".sysml", ".kerml", ".xmi", ".uml", ".mdzip", ".mdxml", ".ecore", ".ttl", ".owl", ".rdf")


def gh(path):
    out = subprocess.run(["gh", "api", "-X", "GET", path], capture_output=True, text=True)
    if out.returncode != 0:
        return None, (out.stdout or out.stderr).strip().splitlines()[0][:160]
    return json.loads(out.stdout), None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--snapshot", default=None)
    ap.add_argument("--org", default="Open-MBEE")
    args = ap.parse_args()
    snap = pathlib.Path(args.snapshot) if args.snapshot else model.snapshot_dir()
    ids = model.by_name()
    forks = [r for r in json.loads((snap / "repos.json").read_text()) if r["fork"]]
    out = {}
    for repo in sorted(forks, key=lambda r: r["name"].lower()):
        name, row = repo["name"], {"name": repo["name"], "upstream": repo["parent"]}
        mine, err = gh(f"repos/{args.org}/{name}")
        theirs, err2 = gh(f"repos/{repo['parent']}") if mine else (None, err)
        if not (mine and theirs):
            row.update({"readable": False, "reason": err or err2})
        else:
            # compared from our side: two forks of one upstream (staged-recipes, staged-recipes-opensysml) are
            # ambiguous by owner from the upstream's side
            upstream_owner = repo["parent"].split("/")[0]
            cmp, err3 = gh(f"repos/{args.org}/{name}/compare/{upstream_owner}:{theirs['default_branch']}..."
                           f"{args.org}:{mine['default_branch']}")
            if cmp is None:
                row.update({"readable": False, "reason": err3})
            else:
                files = sorted(f["filename"] for f in cmp.get("files") or [])
                row.update({"readable": True, "ahead_by": cmp["ahead_by"], "behind_by": cmp["behind_by"],
                            "files_changed": len(files),
                            "model_files_changed": sum(1 for f in files if f.lower().endswith(MODEL_SUFFIXES))})
        out[ids[name]] = row
    doc = {"note": "Each fork against its upstream (WP5c D-3): commits of ours ahead, commits behind, files changed, "
                   "and how many are model files. Read with GET only.",
           "read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "model_suffixes": list(MODEL_SUFFIXES), "forks": out}
    (snap / "forks.json").write_text(json.dumps(doc, indent=1) + "\n")
    print(f"read {len(out)} forks: {sum(1 for r in out.values() if r.get('readable'))} readable")


if __name__ == "__main__":
    main()

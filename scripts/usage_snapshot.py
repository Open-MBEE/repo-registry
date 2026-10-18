#!/usr/bin/env python3
"""Take a read-only usage snapshot: clone counts (where readable) and release download totals (WP4 D-2).

Only `gh` GET requests (WP4 R-1). Clone counts come from GitHub's traffic API, which needs push access to each
repository and covers the last 14 days; where the credential can't read them, they are stored as unreadable, never 0.
Release downloads are the sum of `download_count` over the assets of up to 100 recent releases. Only public, live,
non-fork repositories in the snapshot are read.

Usage: python3 scripts/usage_snapshot.py --snapshot data/snapshots/2026-10-18
Writes <snapshot>/usage.json.
"""
import argparse
import json
import pathlib
import subprocess


def gh(path):
    out = subprocess.run(["gh", "api", "-X", "GET", path], capture_output=True, text=True)
    if out.returncode != 0:
        return None, (out.stdout or out.stderr).strip().splitlines()[0][:160]
    return json.loads(out.stdout), None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--org", default="Open-MBEE")
    args = ap.parse_args()
    snap = pathlib.Path(args.snapshot)
    repos = [r for r in json.loads((snap / "repos.json").read_text()) if not r["archived"] and not r["fork"]]
    usage = {}
    for repo in sorted(repos, key=lambda r: r["name"].lower()):
        name = repo["name"]
        clones, err = gh(f"repos/{args.org}/{name}/traffic/clones")
        releases, rerr = gh(f"repos/{args.org}/{name}/releases?per_page=100")
        downloads = (sum(a.get("download_count", 0) for r in releases for a in r.get("assets", []))
                     if releases is not None else None)
        usage[name] = {
            "clones_14d": ({"readable": True, "count": clones["count"], "uniques": clones["uniques"]}
                           if clones is not None else {"readable": False, "reason": err}),
            "release_downloads": downloads,
        }
    meta = json.loads((snap / "meta.json").read_text())
    doc = {"taken_with_snapshot": meta["taken_at"], "note": "clones_14d needs push access; unreadable is not zero",
           "repos": usage}
    (snap / "usage.json").write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    readable = sum(1 for u in usage.values() if u["clones_14d"]["readable"])
    print(f"wrote {snap / 'usage.json'}: {len(usage)} repos, clone counts readable for {readable}")


if __name__ == "__main__":
    main()

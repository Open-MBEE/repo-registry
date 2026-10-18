#!/usr/bin/env python3
"""Live, read-only privacy cross-check: no concealed org member's login appears in this repo (WP3 R-8).

It reads the org's members and public members with `gh` (GET only), then scans every tracked and untracked text file.
People the supervisor named in data/maintainers.yaml as already publicly known are allowed. It never prints a
concealed login: only counts, and the file names where a match was found.

Usage: python3 scripts/privacy_check.py [--org Open-MBEE]   (exit 1 if a concealed login is found)
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

import yaml


def logins(path):
    out = subprocess.run(["gh", "api", "-X", "GET", "--paginate", "--slurp", path], capture_output=True, text=True,
                         check=True)
    return {m["login"] for page in json.loads(out.stdout) for m in page}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--org", default="Open-MBEE")
    args = ap.parse_args()
    concealed = logins(f"orgs/{args.org}/members?per_page=100") - logins(f"orgs/{args.org}/public_members?per_page=100")
    allowed = {m["login"] for m in yaml.safe_load(pathlib.Path("data/maintainers.yaml").read_text())["maintainers"].values()}
    files = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], capture_output=True,
                           text=True, check=True).stdout.split()
    hits = []
    for name in files:
        if name.endswith(".gz"):
            continue
        try:
            tokens = set(re.findall(r"[A-Za-z0-9-]+", pathlib.Path(name).read_text(encoding="utf-8")))
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        if (tokens & concealed) - allowed:
            hits.append(name)
    print(f"concealed members: {len(concealed)}; files scanned: {len(files)}; files naming one: {len(hits)}")
    for name in hits:
        print(f"  {name}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())

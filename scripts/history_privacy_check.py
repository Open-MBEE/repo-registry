#!/usr/bin/env python3
"""Live, read-only privacy check of the whole history to be published: no concealed org member's login appears in
any file of any commit, or in any commit message, reachable from the refs given (WP5 D-3, R-6; WP3 R-8).

scripts/privacy_check.py checks the working tree. This checks everything a push would publish. It reads the org's
members and public members with `gh` (GET only). People the supervisor named in data/maintainers.yaml as already
publicly known are allowed. It never prints a concealed login: only counts, and the paths where a match was found.

Usage: python3 scripts/history_privacy_check.py [--org Open-MBEE] [refs ...]   (default ref: main; exit 1 on a match)
"""
import argparse
import re
import subprocess
import sys

import yaml

from privacy_check import logins

TOKEN = re.compile(r"[A-Za-z0-9-]+")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--org", default="Open-MBEE")
    ap.add_argument("refs", nargs="*", default=["main"])
    args = ap.parse_args()
    concealed = logins(f"orgs/{args.org}/members?per_page=100") - logins(f"orgs/{args.org}/public_members?per_page=100")
    allowed = set(yaml.safe_load(subprocess.run(["git", "show", f"{args.refs[0]}:data/maintainers.yaml"],
                                                capture_output=True, text=True, check=True).stdout)["maintainers"])
    concealed -= allowed
    listing = subprocess.run(["git", "rev-list", "--objects", *args.refs], capture_output=True, text=True,
                             check=True).stdout.splitlines()
    paths = {}
    for line in listing:
        sha, _, path = line.partition(" ")
        if path and not path.endswith(".gz"):
            paths.setdefault(sha, path)
    batch = subprocess.run(["git", "cat-file", "--batch"], input="\n".join(paths).encode() + b"\n",
                           capture_output=True, check=True).stdout
    hits, blobs, pos = set(), 0, 0
    while pos < len(batch):
        header_end = batch.index(b"\n", pos)
        sha, kind, size = batch[pos:header_end].decode().split()
        body = batch[header_end + 1:header_end + 1 + int(size)]
        pos = header_end + 1 + int(size) + 1
        if kind == "blob":
            blobs += 1
            if set(TOKEN.findall(body.decode("utf-8", "ignore"))) & concealed:
                hits.add(paths[sha])
    messages = subprocess.run(["git", "log", "--format=%B", *args.refs], capture_output=True, text=True,
                              check=True).stdout
    in_messages = bool(set(TOKEN.findall(messages)) & concealed)
    print(f"refs: {' '.join(args.refs)}; concealed members: {len(concealed)}; blobs scanned: {blobs}; "
          f"paths naming one: {len(hits)}; commit messages naming one: {int(in_messages)}")
    for path in sorted(hits):
        print(f"  {path}")
    if hits or in_messages:
        sys.exit(1)


if __name__ == "__main__":
    main()

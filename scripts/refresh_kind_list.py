#!/usr/bin/env python3
"""Apply the kind-list refresh: set every inferred or topic entry to what the rules and topics give today (WP5c).

The refresh view (build/demo/kind-list-refresh.yaml, rendered by scripts/recommend.py) lists the candidate entries
the rules or topics would change. This writes those candidates into registry.yaml, so the change can be reviewed and
merged as an ordinary pull request. Entries whose source is `maintainer` are never touched (WP5c OD1): only a
maintainer's merged change sets or changes them. Deterministic and offline.

Usage: python3 scripts/refresh_kind_list.py [--root .]   (renders the draft first, then rewrites registry.yaml)
"""
import argparse
import pathlib
import re
import subprocess
import sys
import tempfile

import yaml


def blocks(text):
    """Each entry's lines under `repos:`, by repository ID: an entry starts at a line '  <id>:'."""
    out, rid = {}, None
    for line in text.partition("\nrepos:\n")[2].splitlines():
        m = re.match(r"^  (\d+):$", line)
        if m:
            rid = int(m.group(1))
            out[rid] = [line]
        elif rid is not None and line.startswith("    "):
            out[rid].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = pathlib.Path(args.root).resolve()
    with tempfile.TemporaryDirectory() as t:
        subprocess.run([sys.executable, str(root / "scripts/recommend.py"), "--out", t, "--root", str(root),
                        "--kinds", str(root / "data/taxonomy/kinds.yaml"), "--tiers", str(root / "data/taxonomy/tiers.yaml"),
                        "--registry", str(root / "registry.yaml")], cwd=root, check=True, capture_output=True)
        draft = (pathlib.Path(t) / "kind-list-draft.yaml").read_text()
        changes = yaml.safe_load((pathlib.Path(t) / "kind-list-refresh.yaml").read_text())["changes"] or {}
    path = root / "registry.yaml"
    text = path.read_text()
    head, _, body = text.partition("\nrepos:\n")
    current = yaml.safe_load(text)["repos"]
    mine, theirs = blocks(text), blocks(draft)
    out = []
    for rid, e in current.items():
        keep = e.get("source") == "maintainer" or rid not in changes
        out.append((mine if keep else theirs)[rid].rstrip("\n"))
    path.write_text(head + "\nrepos:\n" + "\n".join(out) + "\n")
    print(f"refreshed {len(changes)} candidate entries; maintainer entries untouched")


if __name__ == "__main__":
    main()

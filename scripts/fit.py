#!/usr/bin/env python3
"""Render the fit report: how many repositories are unclassified, and why, in the kind list and in the rules' draft.

A view (WP5c D-6, R-7), rendered, never committed (WP5b OD4). The fit analysis (docs/fit-analysis.md) is WP4's dated
record; this view is its current counterpart, for any later refinement: the unclassified repositories by reason,
the kinds by source (inferred, topic, maintainer), and the type topics declared.

Usage: python3 scripts/fit.py [--out build/demo]   (reads build/demo/kind-list-draft.yaml)
"""
import argparse
import collections
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model  # noqa: E402


def counts(entries):
    reasons = collections.Counter(e["reason"] for e in entries.values() if "reason" in e)
    sources = collections.Counter(e.get("source", "inferred") for e in entries.values())
    kinds = collections.Counter(model.kind_of(e) for e in entries.values())
    return reasons, sources, kinds


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="build/demo")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root, out = pathlib.Path(args.root), pathlib.Path(args.out)
    kind_list = model.load("registry.yaml", root)["repos"]
    draft = yaml.safe_load((out / "kind-list-draft.yaml").read_text())["repos"]
    report = yaml.safe_load((out / "reports/kind-recommendations.yaml").read_text())["repos"]
    L = ["# Fit report", "",
         "> **PROVISIONAL.** A view (WP5c), rendered by `scripts/fit.py`; never committed. How the taxonomy fits the",
         "> org's repositories now. WP4's dated analysis is `docs/fit-analysis.md`.", ""]
    for title, entries in (("The kind list (registry.yaml)", kind_list), ("The rules' draft (kind-list-draft.yaml)", draft)):
        reasons, sources, kinds = counts(entries)
        L += [f"## {title}", "", f"{len(entries)} repositories; {sum(reasons.values())} unclassified.", "",
              "| Unclassified because | Repositories |", "|---|---|"]
        L += [f"| {r} | {n} |" for r, n in reasons.most_common()]
        L += ["", "| Source of the kind | Repositories |", "|---|---|"]
        L += [f"| {s} | {n} |" for s, n in sorted(sources.items())]
        L += ["", "| Kind | Repositories |", "|---|---|"]
        L += [f"| {k} | {n} |" for k, n in sorted(kinds.items())]
        L.append("")
    declared = collections.Counter(r.get("declared_type") for r in report.values() if r.get("declared_type"))
    L += ["## Type topics declared", "",
          (", ".join(f"{t} {n}" for t, n in sorted(declared.items())) or "None yet: no repository has an "
           "openmbee-<type> topic.") + "", ""]
    (out / "fit-report.md").write_text("\n".join(L))
    print(f"wrote {out / 'fit-report.md'}")


if __name__ == "__main__":
    main()

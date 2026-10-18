#!/usr/bin/env python3
"""Report each repository's detected license against the license-by-type policy (WP2a D-4).

Deterministic, offline: reads the stored snapshot, registry.yaml, the policy's `allowed_licenses` and
data/deviations.yaml. No license name is written in this file: the allowed sets are data (WP2 R-10).
Covered: every live repository whose kind is in the taxonomy (archived and unclassified ones, such as forks, are not).

Usage: python3 scripts/licenses.py [--out build/demo]   (a view, rendered, never committed: WP5b OD4)
"""
import argparse
import collections
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model  # noqa: E402

POLICY = "license-by-type"


def evaluate(repos, registry, kinds, policy, deviations):
    """repos and registry keyed by repository ID; kinds flattened (model.kinds). Rows keyed by ID, sorted by name."""
    allowed = policy["allowed_licenses"]
    excepted = {(d["repo_id"], d["policy"]): d for d in deviations if d.get("policy") == POLICY}
    rows = {}
    for rid, entry in sorted(registry.items(), key=lambda kv: str(kv[1].get("name")).lower()):
        kind = kinds.get(model.kind_of(entry))
        repo = repos.get(rid)
        if kind is None or repo is None or repo.get("after_snapshot") or kind["stage"] == "archived":
            continue
        spdx = repo.get("license")
        ok_set = allowed.get(kind["type"], [])
        if (rid, POLICY) in excepted:
            color, detail = "green", f"accepted exception: {excepted[(rid, POLICY)]['reason']}"
        elif spdx in ok_set:
            color, detail = "green", "allowed for its type"
        elif spdx in (None, "NOASSERTION"):
            color, detail = "red", "no license GitHub can recognize"
        else:
            color, detail = "red", f"not in the allowed set for {kind['type']} ({', '.join(ok_set)}); needs a change or an exception"
        rows[rid] = {"name": entry["name"], "kind": model.kind_of(entry), "license": spdx, "color": color,
                     "detail": detail}
    counts = collections.Counter(r["color"] for r in rows.values())
    by_license = collections.Counter((r["license"] or "none") for r in rows.values() if r["color"] == "red")
    return {"status": "provisional", "policy": POLICY,
            "counts": dict(sorted(counts.items())), "red_by_license": dict(sorted(by_license.items())),
            "repos": rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="build/demo")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = pathlib.Path(args.root)
    registry = model.load("registry.yaml", root)["repos"]
    kinds = model.kinds(model.load("data/taxonomy/kinds.yaml", root))
    policy = model.load(f"data/policies/{POLICY}.yaml", root)
    deviations = model.load("data/deviations.yaml", root)["deviations"] or []
    report = evaluate(model.repos(root), registry, kinds, policy, deviations)
    out = pathlib.Path(args.out) / "reports/license-report.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(report, sort_keys=False, width=120))
    print(f"counts: {report['counts']}  red by license: {report['red_by_license']}")


if __name__ == "__main__":
    main()

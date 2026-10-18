#!/usr/bin/env python3
"""Report each repository's detected license against the license-by-type policy (WP2a D-4).

Deterministic, offline: reads the stored snapshot, registry.yaml, the policy's `allowed_licenses` and
data/deviations.yaml. No license name is written in this file: the allowed sets are data (WP2 R-10).
Covered: every live repository whose kind is in the taxonomy (archived and unclassified ones, such as forks, are not).

Usage: python3 scripts/licenses.py --snapshot data/snapshots/2026-10-18 \
          [--report data/reports/license-report.yaml]
"""
import argparse
import collections
import json
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from recommend import kind_of  # noqa: E402

POLICY = "license-by-type"


def evaluate(repos, registry, kinds, policy, deviations):
    allowed = policy["allowed_licenses"]
    excepted = {(d["repo"], d["policy"]): d for d in deviations if d.get("policy") == POLICY}
    rows = {}
    for name, entry in sorted(registry.items(), key=lambda kv: kv[0].lower()):
        kind = kinds.get(kind_of(entry))
        repo = repos.get(name)
        if kind is None or repo is None or kind["stage"] == "archived":
            continue
        spdx = repo.get("license")
        ok_set = allowed.get(kind["type"], [])
        if (name, POLICY) in excepted:
            status, detail = "green", f"accepted exception: {excepted[(name, POLICY)]['reason']}"
        elif spdx in ok_set:
            status, detail = "green", "allowed for its type"
        elif spdx in (None, "NOASSERTION"):
            status, detail = "red", "no license GitHub can recognize"
        else:
            status, detail = "red", f"not in the allowed set for {kind['type']} ({', '.join(ok_set)}); needs a change or an exception"
        rows[name] = {"kind": kind_of(entry), "license": spdx, "status": status, "detail": detail}
    counts = collections.Counter(r["status"] for r in rows.values())
    by_license = collections.Counter((r["license"] or "none") for r in rows.values() if r["status"] == "red")
    return {"status": "provisional", "policy": POLICY,
            "counts": dict(sorted(counts.items())), "red_by_license": dict(sorted(by_license.items())),
            "repos": rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--registry", default="registry.yaml")
    ap.add_argument("--kinds", default="data/taxonomy/kinds.yaml")
    ap.add_argument("--policies", default="data/policies")
    ap.add_argument("--deviations", default="data/deviations.yaml")
    ap.add_argument("--report", default="data/reports/license-report.yaml")
    args = ap.parse_args()
    repos = {r["name"]: r for r in json.loads((pathlib.Path(args.snapshot) / "repos.json").read_text())}
    registry = yaml.safe_load(pathlib.Path(args.registry).read_text())["repos"]
    kinds = yaml.safe_load(pathlib.Path(args.kinds).read_text())["kinds"]
    policy = yaml.safe_load((pathlib.Path(args.policies) / f"{POLICY}.yaml").read_text())
    deviations = yaml.safe_load(pathlib.Path(args.deviations).read_text())["deviations"] or []
    report = evaluate(repos, registry, kinds, policy, deviations)
    report["snapshot"] = args.snapshot
    pathlib.Path(args.report).write_text(yaml.safe_dump(report, sort_keys=False, width=120))
    print(f"counts: {report['counts']}  red by license: {report['red_by_license']}")


if __name__ == "__main__":
    main()

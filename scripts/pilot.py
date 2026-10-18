#!/usr/bin/env python3
"""Render the pilot the rule in data/pilot-rule.yaml would propose today: a view (WP4 D-2; WP5b OD6).

The pilot list (data/pilot.yaml) and exclude list (data/exclude.yaml) are model tables: written once by this rule,
then kept, and changed only by a governed pull request. This script renders what the rule would propose now, so a
difference between the rule and the kept list is visible, not an error.

Deterministic and offline (WP4 R-1, R-2): it reads the stored snapshot, usage.json, registry.yaml, the kind
recommendations view and the taxonomy. The categories, quotas, weights and must-includes are all data; this file names
none of them. Every repository is proposed for the pilot or for the exclude list (R-4).

Usage: python3 scripts/pilot.py [--out build/demo]   (reads build/demo/reports/kind-recommendations.yaml)
"""
import argparse
import json
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model  # noqa: E402
from recommend import evaluate  # noqa: E402


def attributes(repo, entry, kinds, flags, usage, weights):
    """The columns the pilot rule's predicates read: declared in data/schema/model.yaml (WP5b F-15). No kind name:
    rules read type and stage (WP5b OD2)."""
    kind = kinds.get(model.kind_of(entry), {})
    u = usage.get(entry["name"], {})
    clones = u.get("clones_14d", {})
    score = (weights["release_downloads"] * (u.get("release_downloads") or 0)
             + weights["clone_uniques_14d"] * (clones.get("uniques", 0) if clones.get("readable") else 0)
             + weights["stars"] * (repo.get("stars") or 0) + weights["forks"] * (repo.get("forks") or 0))
    return {
        "name": entry["name"], "description": repo.get("description"),
        "type": kind.get("type"), "stage": kind.get("stage"), "tier": kind.get("tier"),
        "fork": repo.get("fork", False), "archived": repo.get("archived", False),
        "commits_last_3_months": repo.get("commits_last_3_months") or 0,
        "commits_last_12_months": repo.get("commits_last_12_months") or 0,
        "archive_candidate": "archive-candidate" in flags, "usage_score": score,
        "release_downloads": u.get("release_downloads") or 0,
        "clone_uniques_14d": clones.get("uniques", 0) if clones.get("readable") else 0,
    }


def select(rule, repos, registry, kinds, report, usage):
    """Everything keyed by repository ID. Returns the proposal {repo_id: {name, category, reason}} and the attributes."""
    weights = rule["usage_score"]
    attrs = {rid: attributes(repos.get(rid, {}), entry, kinds, report.get(rid, {}).get("flags", []), usage, weights)
             for rid, entry in registry.items()}
    chosen = {}

    def category_of(a):
        for cat in rule["categories"]:
            if evaluate(cat["where"], a, {}):
                return cat["id"]
        return None

    named = [(r, "must-include (supervisor)") for r in rule["must_include"]] + \
        [(r, "registers itself (X-9)") for r in rule.get("self_registered", [])]
    for ref, why in named:
        if ref["repo_id"] not in attrs:
            raise SystemExit(f"must-include {ref['name']} is not in registry.yaml")
        chosen[ref["repo_id"]] = {"name": ref["name"], "category": category_of(attrs[ref["repo_id"]]) or "must-include",
                                  "reason": why}
    for cat in rule["categories"]:
        have = sum(1 for c in chosen.values() if c["category"] == cat["id"])
        candidates = sorted((r for r, a in attrs.items() if r not in chosen and evaluate(cat["where"], a, {})),
                            key=lambda r: (-attrs[r][cat["sort_by"]], attrs[r]["name"].lower()))
        for rid in candidates[: max(0, cat["quota"] - have)]:
            first = " ".join(cat["meaning"].split()).split(". ")[0].rstrip(".")
            chosen[rid] = {"name": attrs[rid]["name"], "category": cat["id"],
                           "reason": f"{cat['id']}: {first[0].lower() + first[1:]}"}
    return chosen, attrs


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="build/demo")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root, out = pathlib.Path(args.root), pathlib.Path(args.out)
    usage = json.loads((model.snapshot_dir(root) / "usage.json").read_text())["repos"]
    rule = model.load("data/pilot-rule.yaml", root)
    registry = model.load("registry.yaml", root)["repos"]
    kinds = model.kinds(model.load("data/taxonomy/kinds.yaml", root))
    report = yaml.safe_load((out / "reports/kind-recommendations.yaml").read_text())["repos"]
    chosen, attrs = select(rule, model.repos(root), registry, kinds, report, usage)
    proposal = {"note": "A view (WP5b OD6): the pilot the rule would propose today. data/pilot.yaml is the kept list.",
                "pilot": {r: chosen[r] for r in sorted(chosen, key=lambda r: chosen[r]["name"].lower())},
                "excluded": sorted((r for r in registry if r not in chosen), key=lambda r: registry[r]["name"].lower())}
    path = out / "pilot-proposal.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(proposal, sort_keys=False, width=120))
    by_cat = {}
    for c in chosen.values():
        by_cat.setdefault(c["category"], []).append(c["name"])
    for cat, names in by_cat.items():
        print(f"{cat:26} {len(names):2}  {', '.join(sorted(names, key=str.lower))}")
    print(f"pilot: {len(chosen)}  excluded: {len(proposal['excluded'])}")


if __name__ == "__main__":
    main()

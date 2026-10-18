#!/usr/bin/env python3
"""Recommend each repo's initial kind from a stored snapshot, and write the provisional kind list.

WP1 D-5. Deterministic, no language model (WP1 R-5, WP0 R-1). The taxonomy is data: this file names no kind,
type, stage, tier or signal (WP1 R-7, WP0 R-6). It only RECOMMENDS kinds. Authority to set a repo's kind
belongs to the maintainers (WP1 Direction, AGENTS.md "Provisional data").

Usage:
  python3 scripts/recommend.py --snapshot data/snapshots/2026-10-18 \
      [--kinds data/taxonomy/kinds.yaml] [--tiers data/taxonomy/tiers.yaml] \
      [--assignments data/assignments.yaml] \
      [--registry registry.yaml] [--report data/reports/kind-recommendations.yaml]

Assigned kinds (data/assignments.yaml) come from recorded decisions. They replace the recommendation for that repo,
and a repo that isn't in the snapshot yet (such as this one) is added. The org's own kind is assigned the same way.

Derived attributes, added to each snapshot record before the rules run:
  has_semver_release   true if any non-prerelease release tag is semantic versioning (vMAJOR.MINOR.PATCH)
  latest_semver        the highest such tag, or null
  latest_semver_major  its MAJOR number, or null
"""
import argparse
import json
import pathlib
import re
import sys

import yaml

SEMVER = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?$")


class TaxonomyError(Exception):
    pass


def derive(repo):
    versions = []
    for rel in repo.get("releases", []):
        m = SEMVER.match(rel["tag"] or "")
        if m and not rel.get("prerelease"):
            versions.append((tuple(int(x) for x in m.groups()), rel["tag"]))
    best = max(versions) if versions else None
    return {
        **repo,
        "has_semver_release": bool(versions),
        "latest_semver": best[1] if best else None,
        "latest_semver_major": best[0][0] if best else None,
    }


def evaluate(pred, repo, signals, stack=()):
    """Evaluate one predicate of the kinds.yaml predicate language."""
    if isinstance(pred, bool):
        return pred
    if not isinstance(pred, dict) or not pred:
        raise TaxonomyError(f"bad predicate: {pred!r}")
    if "all" in pred:
        return all(evaluate(p, repo, signals, stack) for p in pred["all"])
    if "any" in pred:
        return any(evaluate(p, repo, signals, stack) for p in pred["any"])
    if "not" in pred:
        return not evaluate(pred["not"], repo, signals, stack)
    if "signal" in pred:
        name = pred["signal"]
        if name not in signals:
            raise TaxonomyError(f"unknown signal: {name}")
        if name in stack:
            raise TaxonomyError(f"signal cycle: {' -> '.join(stack + (name,))}")
        return evaluate(signals[name], repo, signals, stack + (name,))
    if "attr" in pred:
        value = repo.get(pred["attr"])
        ops = [k for k in pred if k != "attr"]
        if len(ops) != 1:
            raise TaxonomyError(f"attr test needs exactly one operator: {pred!r}")
        op = ops[0]
        arg = pred[op]
        if op == "eq":
            return value == arg
        if op == "in":
            return value in arg
        if op == "matches":
            values = value if isinstance(value, list) else [value]
            return any(v is not None and re.search(arg, str(v), re.IGNORECASE) for v in values)
        if value is None:
            return False
        if op == "gt":
            return value > arg
        if op == "gte":
            return value >= arg
        if op == "lt":
            return value < arg
        raise TaxonomyError(f"unknown operator: {op}")
    raise TaxonomyError(f"bad predicate: {pred!r}")


def check_taxonomy(kinds_doc, tiers_doc):
    """Structural checks on the taxonomy itself (WP1 R-6)."""
    tiers = tiers_doc["tiers"]
    types, stages = kinds_doc["types"], kinds_doc["stages"]
    problems = []
    for name, kind in kinds_doc["kinds"].items():
        if kind.get("tier") not in tiers:
            problems.append(f"{name}: tier {kind.get('tier')!r} is not a tier")
        if kind.get("type") not in types:
            problems.append(f"{name}: type {kind.get('type')!r} is not a type")
        if kind.get("stage") not in stages and not kind.get("departure"):
            problems.append(f"{name}: stage {kind.get('stage')!r} is not a stage and no departure is stated")
        if name != f"{kind.get('type')}/{kind.get('stage')}":
            problems.append(f"{name}: name must be <type>/<stage>")
        if not kind.get("meaning"):
            problems.append(f"{name}: no meaning")
    cross = {f"{t}/{s}" for t in types for s in stages}
    omitted = kinds_doc.get("omitted", {})
    for name in omitted:
        if name not in cross:
            problems.append(f"omitted {name} is not in the type x stage cross product")
        if name in kinds_doc["kinds"]:
            problems.append(f"{name} is both defined and omitted")
    for name in sorted(cross - set(kinds_doc["kinds"]) - set(omitted)):
        problems.append(f"{name} is neither defined nor omitted with a reason")
    used = {k["tier"] for k in kinds_doc["kinds"].values()}
    for tier in tiers:
        if tier not in used:
            problems.append(f"tier {tier} is used by no kind")
    if problems:
        raise TaxonomyError("\n".join(problems))


def recommend(repos, kinds_doc, assigned=None):
    signals = kinds_doc["signals"]
    assigned = assigned or {}
    results = {}
    for repo in repos:
        repo = derive(repo)
        matched = [n for n, k in kinds_doc["kinds"].items() if evaluate(k["recommend_when"], repo, signals)]
        flags = [n for n, f in kinds_doc.get("flags", {}).items() if evaluate(f["when"], repo, signals)]
        if len(matched) == 1:
            kind, reason = matched[0], None
        else:
            kind = "unclassified"
            if matched:
                reason = "Matches more than one kind: " + ", ".join(matched) + "."
            else:
                reason = next(
                    (r["reason"] for r in kinds_doc.get("unclassified_reasons", []) if evaluate(r["when"], repo, signals)),
                    "No kind's rule matches.",
                )
        if repo["name"] in assigned:
            kind, reason = kind_of(assigned[repo["name"]]), None
        results[repo["name"]] = {
            "assigned": repo["name"] in assigned,
            "kind": kind,
            "tier": kinds_doc["kinds"][kind]["tier"] if kind in kinds_doc["kinds"] else None,
            "matched": matched,
            "reason": reason,
            "flags": flags,
            "evidence": {
                "archived": repo["archived"],
                "fork": repo["fork"],
                "primary_language": repo["primary_language"],
                "latest_semver": repo["latest_semver"],
                "commits_last_12_months": repo["commits_last_12_months"],
                "commits_last_3_months": repo["commits_last_3_months"],
            },
        }
    for name, a in assigned.items():
        if name not in results:
            results[name] = {
                "assigned": True, "kind": kind_of(a), "tier": (kinds_doc["kinds"].get(kind_of(a)) or {}).get("tier"),
                "matched": [],
                "reason": None, "flags": [], "evidence": {"note": "Not in the snapshot.", "decision": a["decision"]},
            }
    for name, r in results.items():
        if r["kind"] != "unclassified" and r["kind"] not in kinds_doc["kinds"]:
            raise TaxonomyError(f"{name}: assigned kind {r['kind']} is not a kind")
    return dict(sorted(results.items(), key=lambda kv: kv[0].lower()))


def kind_of(entry):
    """The kind an entry of the kind list (or of data/assignments.yaml) names: computed from its type and stage, or
    `unclassified` for an entry that has only a reason (WP4e)."""
    if "type" in entry or "stage" in entry:
        return f"{entry.get('type')}/{entry.get('stage')}"
    return "unclassified"


def quote(s):
    return json.dumps(s)  # a JSON string is a valid YAML scalar


def write_registry(path, results, snapshot_dir, meta, org_kind, kinds_doc):
    lines = [
        "# PROVISIONAL. NOT APPROVED. Kinds recommended by rule, plus kinds assigned by recorded decisions",
        "# (data/assignments.yaml). Drafted by scripts/recommend.py (WP1 D-5).",
        "# Authority to initialize this list belongs to the maintainers (WP0, maintainer approval 4).",
        "# Format: docs/kind-list-format.md. One entry per repo: its type and stage, or only a reason. Changing a",
        "# repo's stage (or type) is a one-line edit.",
        "status: provisional",
        f"provisional_until: {quote('WP0 maintainer approval 4: the assigned kind of each repo in the registry')}",
        "org:",
        f"  name: {meta['org']}",
    ]
    if org_kind in kinds_doc["kinds"]:  # with no assignment (a toy taxonomy), the org has no type or stage
        lines += [f"  type: {kinds_doc['kinds'][org_kind]['type']}", f"  stage: {kinds_doc['kinds'][org_kind]['stage']}"]
    lines += [
        f"snapshot: {snapshot_dir}",
        "repos:",
    ]
    for name, r in results.items():
        lines.append(f"  {quote(name)}:")
        if r["kind"] in kinds_doc["kinds"]:
            lines.append(f"    type: {kinds_doc['kinds'][r['kind']]['type']}")
            lines.append(f"    stage: {kinds_doc['kinds'][r['kind']]['stage']}")
        if r["reason"]:
            lines.append(f"    reason: {quote(r['reason'])}")
    pathlib.Path(path).write_text("\n".join(lines) + "\n")


def write_report(path, results, snapshot_dir):
    doc = {
        "status": "provisional",
        "note": "Evidence for each recommended kind. Flags never change a kind.",
        "snapshot": str(snapshot_dir),
        "repos": results,
    }
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(path).write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--kinds", default="data/taxonomy/kinds.yaml")
    ap.add_argument("--tiers", default="data/taxonomy/tiers.yaml")
    ap.add_argument("--assignments", default="data/assignments.yaml")
    ap.add_argument("--registry", default="registry.yaml")
    ap.add_argument("--report", default="data/reports/kind-recommendations.yaml")
    args = ap.parse_args()

    snap = pathlib.Path(args.snapshot)
    repos = json.loads((snap / "repos.json").read_text())
    meta = json.loads((snap / "meta.json").read_text())
    kinds_doc = yaml.safe_load(pathlib.Path(args.kinds).read_text())
    tiers_doc = yaml.safe_load(pathlib.Path(args.tiers).read_text())
    assignments = yaml.safe_load(pathlib.Path(args.assignments).read_text()) if args.assignments else {}
    org_kind = kind_of(assignments.get("org") or {})
    try:
        check_taxonomy(kinds_doc, tiers_doc)
        if org_kind != "unclassified" and org_kind not in kinds_doc["kinds"]:
            raise TaxonomyError(f"org: assigned kind {org_kind} is not a kind")
        results = recommend(repos, kinds_doc, assignments.get("repos") or {})
    except TaxonomyError as e:
        sys.exit(f"taxonomy error:\n{e}")

    write_registry(args.registry, results, args.snapshot, meta, org_kind, kinds_doc)
    write_report(args.report, results, args.snapshot)

    counts = {}
    for r in results.values():
        counts[r["kind"]] = counts.get(r["kind"], 0) + 1
    print(f"{len(results)} repos; org kind: {org_kind}")
    for kind in list(kinds_doc["kinds"]) + ["unclassified"]:
        tier = kinds_doc["kinds"].get(kind, {}).get("tier", "-")
        print(f"  {kind:28} {tier:7} {counts.get(kind, 0)}")


if __name__ == "__main__":
    main()

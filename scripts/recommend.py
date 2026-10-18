#!/usr/bin/env python3
"""Recommend each repo's initial kind from a stored snapshot: a view, rendered, never committed (WP5b OD4).

WP1 D-5. Deterministic, no language model (WP1 R-5, WP0 R-1). The taxonomy is data: this file names no kind,
type, stage, tier or signal (WP1 R-7, WP0 R-6). It only RECOMMENDS kinds. Authority to set a repo's kind
belongs to the maintainers (WP1 Direction, AGENTS.md "Provisional data").

Usage: python3 scripts/recommend.py [--out build/demo] [--kinds ...] [--tiers ...] [--registry registry.yaml]

It writes two views into --out: the recommendation report (reports/kind-recommendations.yaml) and a draft kind list
(kind-list-draft.yaml), which is what the rules alone would give. The kind list itself (registry.yaml) is model data
that people change one entry at a time (WP0 R-12); the rules only propose a candidate (WP5c, the supervisor:
"the inference produces a candidate not a decision").

Precedence (WP5c OD1): a maintainer's decision (a kind-list entry whose source is `maintainer`) is kept as it is;
otherwise a type declared by exactly one openmbee-<type> topic (`type_topics` in kinds.yaml) overrides the word and
language rules, and the rules decide the stage; otherwise the rules alone propose a candidate. Each draft entry says
which source gave it. A repo with no sensed row (one created after the snapshot, such as this one) comes only from a
maintainer's decision. Rows are keyed by GitHub's repository ID (WP5b OD3).

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

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model  # noqa: E402

SEMVER = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?$")


class TaxonomyError(Exception):
    pass


def derive(repo, type_topics=None):
    """Derived columns (data/schema/model.yaml, derived): the release maturity, and the type its topics declare."""
    versions = []
    for rel in repo.get("releases", []):
        m = SEMVER.match(rel["tag"] or "")
        if m and not rel.get("prerelease"):
            versions.append((tuple(int(x) for x in m.groups()), rel["tag"]))
    best = max(versions) if versions else None
    declared = {type_topics[t] for t in repo.get("topics") or [] if t in (type_topics or {})}
    return {
        **repo,
        "declared_type": declared.pop() if len(declared) == 1 else None,  # none, or more than one, declares nothing
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
    kinds, omitted = model.kinds(kinds_doc), model.omitted(kinds_doc)
    for name, kind in kinds.items():
        if kind.get("tier") not in tiers:
            problems.append(f"{name}: tier {kind.get('tier')!r} is not a tier")
        if kind.get("type") not in types:
            problems.append(f"{name}: type {kind.get('type')!r} is not a type")
        if kind.get("stage") not in stages and not kind.get("departure"):
            problems.append(f"{name}: stage {kind.get('stage')!r} is not a stage and no departure is stated")
        if not kind.get("meaning"):
            problems.append(f"{name}: no meaning")
    cross = {model.kind_name(t, s) for t in types for s in stages}
    for name in omitted:
        if name not in cross:
            problems.append(f"omitted {name} is not in the type x stage cross product")
        if name in kinds:
            problems.append(f"{name} is both defined and omitted")
    for name in sorted(cross - set(kinds) - set(omitted)):
        problems.append(f"{name} is neither defined nor omitted with a reason")
    used = {k["tier"] for k in kinds.values()}
    for tier in tiers:
        if tier not in used:
            problems.append(f"tier {tier} is used by no kind")
    if problems:
        raise TaxonomyError("\n".join(problems))


def recommend(repos, kinds_doc, assigned=None):
    """repos: {repo_id: row} (model.repos). assigned: {repo_id: assignment}. Returns {repo_id: result}, sorted by name."""
    signals = kinds_doc["signals"]
    kinds = model.kinds(kinds_doc)
    assigned = assigned or {}
    results = {}
    for rid, repo in repos.items():
        if repo.get("after_snapshot"):
            continue  # no sensed columns: only an assignment can give it a kind (below)
        repo = derive(repo, kinds_doc.get("type_topics"))
        matched = [n for n, k in kinds.items() if evaluate(k["recommend_when"], repo, signals)]
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
        source = "topic" if repo["declared_type"] else "inferred"
        if rid in assigned:
            kind, reason, source = model.kind_of(assigned[rid]), assigned[rid].get("reason"), "maintainer"
        results[rid] = {
            "name": repo["name"],
            "source": source,
            "declared_type": repo["declared_type"],
            "kind": kind,
            "tier": kinds[kind]["tier"] if kind in kinds else None,
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
    for rid, a in assigned.items():
        if rid not in results:
            results[rid] = {
                "name": a.get("name") or repos.get(rid, {}).get("name"), "source": "maintainer", "declared_type": None,
                "kind": model.kind_of(a),
                "tier": (kinds.get(model.kind_of(a)) or {}).get("tier"), "matched": [], "reason": None, "flags": [],
                "evidence": {"note": "No sensed row: created after the snapshot.", "decision": a["decision"]},
            }
    for rid, r in results.items():
        if r["kind"] != "unclassified" and r["kind"] not in kinds:
            raise TaxonomyError(f"{r['name']}: assigned kind {r['kind']} is not a kind")
    return dict(sorted(results.items(), key=lambda kv: str(kv[1]["name"]).lower()))


def quote(s):
    return json.dumps(s)  # a JSON string is a valid YAML scalar


def entry_lines(rid, r, kinds, decisions):
    lines = [f"  {rid}:", f"    name: {quote(r['name'])}"]
    if r["kind"] in kinds:
        lines += [f"    type: {kinds[r['kind']]['type']}", f"    stage: {kinds[r['kind']]['stage']}"]
    if r["reason"]:
        lines.append(f"    reason: {quote(r['reason'])}")
    lines.append(f"    source: {r['source']}")
    if r["source"] == "maintainer":
        lines.append(f"    decision: {quote(decisions.get(rid, ''))}")
    return lines


def write_draft(path, results, org, kinds_doc, decisions):
    """The kind list the rules and topics would give, with the maintainers' decisions kept (a view): the same format
    as registry.yaml, so the refresh is a plain comparison."""
    kinds = model.kinds(kinds_doc)
    o = org or {}
    lines = ["# A VIEW (WP5b OD4): the kind list the rules and topics would give, maintainers' decisions kept.",
             "status: provisional", "org:", f"  name: {o.get('name')}"]
    if model.kind_of(o) in kinds:
        lines += [f"  type: {o['type']}", f"  stage: {o['stage']}", f"  source: {o.get('source')}"]
    lines.append("repos:")
    for rid, r in results.items():
        lines += entry_lines(rid, r, kinds, decisions)
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(path).write_text("\n".join(lines) + "\n")


def write_refresh(path, results, registry, kinds_doc):
    """The inferred and topic entries the rules or topics would change today (a view, WP5c): applying it is an
    ordinary pull request. Maintainer entries never appear: rules and topics don't change them (WP5c OD1)."""
    kinds = model.kinds(kinds_doc)
    changes = {}
    for rid, r in results.items():
        now = registry.get(rid) or {}
        if now.get("source") == "maintainer":
            continue
        would = {"kind": r["kind"], "reason": r["reason"], "source": r["source"]}
        have = {"kind": model.kind_of(now), "reason": now.get("reason"), "source": now.get("source")}
        if would != have:
            changes[rid] = {"name": r["name"], "now": have, "would_be": would}
    doc = {"note": "A view (WP5c): kind-list entries the rules or topics would change today. Maintainer entries are "
                   "never listed. Apply by a pull request.", "changes": changes}
    pathlib.Path(path).write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120))
    return changes


def write_report(path, results):
    doc = {"note": "A view (WP5b OD4): evidence for each recommended kind, keyed by repository ID. Flags never change "
                   "a kind.", "repos": results}
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(path).write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="build/demo")
    ap.add_argument("--root", default=".")
    ap.add_argument("--kinds", default="data/taxonomy/kinds.yaml")
    ap.add_argument("--tiers", default="data/taxonomy/tiers.yaml")
    ap.add_argument("--registry", default="registry.yaml", help="the kind list, for its maintainer decisions; '' for none")
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    kinds_doc = yaml.safe_load(pathlib.Path(args.kinds).read_text())
    tiers_doc = yaml.safe_load(pathlib.Path(args.tiers).read_text())
    registry = yaml.safe_load(pathlib.Path(args.registry).read_text()) if args.registry else {"repos": {}, "org": {}}
    entries = registry.get("repos") or {}
    decided = {rid: e for rid, e in entries.items() if e.get("source") == "maintainer"}
    decisions = {rid: e.get("decision", "") for rid, e in decided.items()}
    org = registry.get("org") or {}
    try:
        check_taxonomy(kinds_doc, tiers_doc)
        if org and model.kind_of(org) not in model.kinds(kinds_doc):
            raise TaxonomyError(f"org: kind {model.kind_of(org)} is not a kind")
        results = recommend(model.repos(root), kinds_doc, decided)
    except TaxonomyError as e:
        sys.exit(f"taxonomy error:\n{e}")

    out = pathlib.Path(args.out)
    write_draft(out / "kind-list-draft.yaml", results, org, kinds_doc, decisions)
    write_report(out / "reports/kind-recommendations.yaml", results)
    changes = write_refresh(out / "kind-list-refresh.yaml", results, entries, kinds_doc)
    counts = {}
    for r in results.values():
        counts[r["kind"]] = counts.get(r["kind"], 0) + 1
    print(f"{len(results)} repos; org kind: {model.kind_of(org)}; {len(changes)} candidate entries would change")
    for kind in list(model.kinds(kinds_doc)) + ["unclassified"]:
        tier = model.kinds(kinds_doc).get(kind, {}).get("tier", "-")
        print(f"  {kind:28} {tier:7} {counts.get(kind, 0)}")


if __name__ == "__main__":
    main()

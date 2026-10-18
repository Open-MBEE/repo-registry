#!/usr/bin/env python3
"""Check the policies against their meta-rules, and work out which policies apply to which kinds.

WP2 D-4 and D-5. Deterministic, no language model (WP0 R-1). Policies are data (WP2 R-10): this file names no
policy, kind, type, stage or tier. Applies-if rules use the predicate language of scripts/recommend.py, over
exactly three attributes of a kind: `type`, `lifecycle` and `tier` (WP0 A1, WP2 R-2).

Usage:
  python3 scripts/policies.py [--policies data/policies] [--kinds data/taxonomy/kinds.yaml] \
      [--tiers data/taxonomy/tiers.yaml] [--baseline data/sources/openssf-security-baseline.yaml] \
      [--table docs/policy-applicability.md] [--report data/reports/policy-applicability.yaml]

Exits non-zero, writing nothing, if any meta-rule is broken (docs/policy-format.md).
"""
import argparse
import pathlib
import re
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from recommend import TaxonomyError, check_taxonomy, evaluate  # noqa: E402

KIND_ATTRS = ("type", "lifecycle", "tier")
REQUIRED = ("status", "id", "name", "meaning", "applies_if", "github", "checks", "cites", "sop")
SOP_HEADINGS = ("## Set up", "## Automated checks", "## Attested checks")
CLAUSE = re.compile(r"^\d+(\.\d+)*$")
POLICY_ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def attrs_used(pred):
    """Every attribute name an applies-if predicate reads."""
    if isinstance(pred, bool):
        return set()
    if not isinstance(pred, dict):
        raise TaxonomyError(f"bad predicate: {pred!r}")
    if "attr" in pred:
        return {pred["attr"]}
    if "signal" in pred:
        raise TaxonomyError("applies-if rules may not use signals; use type, lifecycle and tier only")
    out = set()
    for key in ("all", "any"):
        for p in pred.get(key, []):
            out |= attrs_used(p)
    if "not" in pred:
        out |= attrs_used(pred["not"])
    return out


def load_policies(directory):
    policies = {}
    for path in sorted(pathlib.Path(directory).glob("*.yaml")):
        if path.name.startswith("_"):
            continue
        policies[path.stem] = yaml.safe_load(path.read_text())
    departures = yaml.safe_load((pathlib.Path(directory) / "_departures.yaml").read_text())
    return policies, departures


def check(policies, departures, kinds_doc, tiers_doc, baseline, root, cisa=None, nist=None, org_plan=None,
          future=None):
    future = future or {}
    """The policy meta-rules (docs/policy-format.md). Returns a list of problems."""
    problems = []
    values = {
        "type": set(kinds_doc["types"]),
        "lifecycle": set(kinds_doc["lifecycles"]),
        "tier": set(tiers_doc["tiers"]),
    }
    items = set(baseline["items"])
    adopted = {}
    for pid, p in policies.items():
        where = f"policy {pid}"
        missing = [k for k in REQUIRED if k not in p]
        if missing:
            problems.append(f"{where}: missing {', '.join(missing)}")
            continue
        if p["id"] != pid or not POLICY_ID.match(pid):
            problems.append(f"{where}: id must equal the file name and be lower-case words joined by hyphens")
        if p["status"] not in ("provisional", "approved"):
            problems.append(f"{where}: status must be provisional or approved")
        if (p["status"] == "provisional") != bool(p.get("provisional_until")):
            problems.append(f"{where}: provisional_until is required exactly when status is provisional")
        try:
            used = attrs_used(p["applies_if"])
        except TaxonomyError as e:
            problems.append(f"{where}: {e}")
            used = set()
        if used - set(KIND_ATTRS):
            problems.append(f"{where}: applies_if reads {sorted(used - set(KIND_ATTRS))}; only type, lifecycle, tier")
        for v in _literals(p["applies_if"]):
            attr, val = v
            if attr in values and val not in values[attr]:
                problems.append(f"{where}: applies_if names unknown {attr} {val!r}")
        gh = p["github"] or {}
        if not gh.get("mechanism") or not gh.get("docs"):
            problems.append(f"{where}: github needs a mechanism and at least one docs link")
        for feature in gh.get("needs_research") or []:
            if feature not in (future.get("needs_research") or {}):
                problems.append(f"{where}: needs_research names {feature}, which isn't in _future.yaml needs_research")
        if org_plan is not None and org_plan not in (gh.get("available_on") or []):
            problems.append(f"{where}: github.available_on must include the org's plan ({org_plan}); "
                            "features the plan lacks belong in _future.yaml")
        checks = p["checks"] or {}
        auto, att = checks.get("automated") or [], checks.get("attested") or []
        if not auto and not att:
            problems.append(f"{where}: needs at least one automated or attested check")
        for c in auto:
            if not c.get("id") or not c.get("reads") or not c.get("permission"):
                problems.append(f"{where}: automated check needs id, reads and permission: {c}")
        for c in att:
            if not c.get("id") or not c.get("statement"):
                problems.append(f"{where}: attested check needs id and statement: {c}")
        cites = p["cites"] or {}
        for core, known in (("cisa", cisa), ("nist", nist)):
            value = cites.get(core)
            if not value:
                problems.append(f"{where}: cites.{core} is required (a list, or \"none\")")
            elif value != "none" and known is not None:
                for ref in value:
                    if ref not in known:
                        problems.append(f"{where}: cites.{core} names {ref}, which isn't in data/sources/")
        if not isinstance(cites.get("openssf"), list):  # core since WP4c: present, empty when none is adopted
            problems.append(f"{where}: cites.openssf is required (a list of baseline items, empty if none)")
        for item in cites.get("openssf") or []:
            if item not in items:
                problems.append(f"{where}: cites unknown OpenSSF baseline item {item}")
            adopted.setdefault(item, []).append(pid)
        for clause in cites.get("iso12207") or []:
            if not CLAUSE.match(str(clause)):
                problems.append(f"{where}: iso12207 citations are clause numbers only, got {clause!r}")
        sop = root / p["sop"]
        if not sop.exists():
            problems.append(f"{where}: SOP {p['sop']} does not exist")
        else:
            text = sop.read_text()
            for heading in SOP_HEADINGS:
                if heading not in text:
                    problems.append(f"{where}: SOP lacks the heading {heading!r}")
    if cisa is not None:
        cisa_cited = set()
        for p in policies.values():
            if isinstance((p.get("cites") or {}).get("cisa"), list):
                cisa_cited |= set(p["cites"]["cisa"])
        cisa_departed = set(departures.get("cisa") or {})
        for ref in sorted(cisa):
            if ref in cisa_cited and ref in cisa_departed:
                problems.append(f"CISA {ref} is both cited by a policy and departed")
            if ref not in cisa_cited and ref not in cisa_departed:
                problems.append(f"CISA {ref} is neither cited by a policy nor departed with a reason")
        for ref, reason in (departures.get("cisa") or {}).items():
            if ref not in cisa or not str(reason or "").strip():
                problems.append(f"CISA departure {ref} is unknown or has no reason")
    departed = set(departures.get("openssf") or {})
    for item in sorted(items):
        if item in departed and item in adopted:
            problems.append(f"OpenSSF {item} is both adopted ({adopted[item]}) and departed")
        if item not in departed and item not in adopted:
            problems.append(f"OpenSSF {item} is neither adopted by a policy nor departed with a reason")
    for item, reason in (departures.get("openssf") or {}).items():
        if item not in items:
            problems.append(f"departure for unknown OpenSSF item {item}")
        if not str(reason or "").strip():
            problems.append(f"departure for {item} has no reason")
    return problems


def _literals(pred):
    """(attr, value) pairs an applies-if rule compares against, for the unknown-value check."""
    if isinstance(pred, bool) or not isinstance(pred, dict):
        return []
    if "attr" in pred:
        if "eq" in pred:
            return [(pred["attr"], pred["eq"])]
        if "in" in pred:
            return [(pred["attr"], v) for v in pred["in"]]
        return []
    out = []
    for key in ("all", "any"):
        for p in pred.get(key, []):
            out += _literals(p)
    if "not" in pred:
        out += _literals(pred["not"])
    return out


def applicability(policies, kinds_doc):
    """For every kind, the policies in effect, in policy-id order."""
    table = {}
    for kname, kind in kinds_doc["kinds"].items():
        attrs = {a: kind[a] for a in KIND_ATTRS}
        table[kname] = [pid for pid, p in sorted(policies.items()) if evaluate(p["applies_if"], attrs, {})]
    return table


def write_outputs(table, policies, kinds_doc, md_path, yaml_path):
    pids = sorted(policies)
    lines = [
        "# Policy applicability",
        "",
        "> **PROVISIONAL.** Generated by `scripts/policies.py` from `data/policies/` and `data/taxonomy/kinds.yaml`",
        "> (WP2 D-5). Do not edit by hand. A tick means the policy is in effect for that kind.",
        "",
        "| Kind | Tier | " + " | ".join(f"[{pid}](sops/{pid}.md)" for pid in pids) + " | Count |",
        "|---|---|" + "---|" * len(pids) + "---|",
    ]
    for kname, in_effect in table.items():
        ticks = " | ".join("✓" if pid in in_effect else "" for pid in pids)
        lines.append(f"| {kname} | {kinds_doc['kinds'][kname]['tier']} | {ticks} | {len(in_effect)} |")
    lines += ["", "## Policies", ""]
    for pid in pids:
        lines.append(f"- **[{policies[pid]['name']}](sops/{pid}.md)** (`{pid}`): {policies[pid]['meaning'].strip()}")
    pathlib.Path(md_path).write_text("\n".join(lines) + "\n")
    doc = {"status": "provisional", "note": "Generated by scripts/policies.py (WP2 D-5).",
           "kinds": table,
           "policies": {pid: [k for k, v in table.items() if pid in v] for pid in pids}}
    pathlib.Path(yaml_path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(yaml_path).write_text(yaml.safe_dump(doc, sort_keys=False, width=120))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--policies", default="data/policies")
    ap.add_argument("--kinds", default="data/taxonomy/kinds.yaml")
    ap.add_argument("--tiers", default="data/taxonomy/tiers.yaml")
    ap.add_argument("--baseline", default="data/sources/openssf-security-baseline.yaml")
    ap.add_argument("--table", default="docs/policy-applicability.md")
    ap.add_argument("--report", default="data/reports/policy-applicability.yaml")
    ap.add_argument("--root", default=".")
    ap.add_argument("--cisa", default="data/sources/cisa-practices.yaml")
    ap.add_argument("--nist", default="data/sources/nist-800-53.yaml")
    ap.add_argument("--plan", default="data/sources/github-plan.yaml")
    args = ap.parse_args()

    kinds_doc = yaml.safe_load(pathlib.Path(args.kinds).read_text())
    tiers_doc = yaml.safe_load(pathlib.Path(args.tiers).read_text())
    baseline = yaml.safe_load(pathlib.Path(args.baseline).read_text())
    policies, departures = load_policies(args.policies)
    try:
        check_taxonomy(kinds_doc, tiers_doc)
        cisa = set(yaml.safe_load(pathlib.Path(args.cisa).read_text())["practices"])
        nist = set(yaml.safe_load(pathlib.Path(args.nist).read_text())["controls"])
        plan_path = pathlib.Path(args.plan)
        org_plan = yaml.safe_load(plan_path.read_text())["plan"] if plan_path.exists() else None
        future_path = pathlib.Path(args.policies) / "_future.yaml"
        future = yaml.safe_load(future_path.read_text()) if future_path.exists() else {}
        problems = check(policies, departures, kinds_doc, tiers_doc, baseline, pathlib.Path(args.root), cisa, nist,
                         org_plan, future)
    except TaxonomyError as e:
        problems = [str(e)]
    if problems:
        sys.exit("policy meta-rules broken:\n  " + "\n  ".join(problems))
    table = applicability(policies, kinds_doc)
    write_outputs(table, policies, kinds_doc, args.table, args.report)
    for kname, in_effect in table.items():
        print(f"  {kname:28} {len(in_effect):2}  {', '.join(in_effect)}")


if __name__ == "__main__":
    main()

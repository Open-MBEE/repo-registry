#!/usr/bin/env python3
"""Check the model against its declaration, so that no invalid state reaches main (WP5 D-1; WP5b D-5; WP0 R-14).

The repository's records are the tables of a database, declared in data/schema/model.yaml. This check enforces that
declaration on every table: primary keys present and unique, every column declared and of its type, every foreign
key resolving (single, composite and by source), disjoint tables kept apart. Then the rules that need more than one
table: the kind list covers every repository, a repository's name agrees with its ID, a maintainer's decision is
stated with it, the pilot and exclude list cover the kind list, the proposed CODEOWNERS are exactly the maintainers, and every
predicate reads only declared columns. The taxonomy and policy meta-rules are the ones scripts/recommend.py and
scripts/policies.py already make (reused, not copied). Last, every view renders, and renders the same twice (WP5b
R-5): views are never stored, so the check is that the pipeline is deterministic.

A violation here is a construction error: invalid, and CI rejects it. A compliance error (a repository out of line
with a policy) is never checked here; it is the controller's error signal, kept and remediated (WP5b F-16).

Usage: python3 scripts/validate.py [--root .] [--no-render]   (exit 1, naming each problem; exit 0 when valid)
"""
import argparse
import datetime
import filecmp
import pathlib
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model  # noqa: E402
import policies as P  # noqa: E402
import render as R  # noqa: E402
from recommend import TaxonomyError, check_taxonomy  # noqa: E402

OPS = {"eq", "in", "matches", "gt", "gte", "lt"}
PROVISIONAL_FILES = ["registry.yaml", "data/taxonomy/kinds.yaml", "data/taxonomy/tiers.yaml",
                     "data/maintainers.yaml", "data/deviations.yaml", "data/pilot-rule.yaml", "data/pilot.yaml",
                     "data/exclude.yaml", "data/policies/_set.yaml"]
REPO_NAMED = ["registry_entry", "pilot_member", "excluded", "pilot_named", "release_authority",
              "deviation", "measured_gap"]


def provisional_mark(rel, root):
    """AGENTS.md rule 3: provisional data is marked, in a way a program can check."""
    text = (root / rel).read_text()
    doc = model.load(rel, root) or {}
    status, out = doc.get("status"), []
    if status not in ("provisional", "approved"):
        out.append(f"{rel}: status must be provisional or approved, not {status!r}")
    if status == "provisional":
        if not str(doc.get("provisional_until") or "").strip():
            out.append(f"{rel}: provisional, but provisional_until doesn't name the approval that lifts it")
        if not text.startswith("# PROVISIONAL"):
            out.append(f"{rel}: provisional, but the first line doesn't start with '# PROVISIONAL'")
    if status == "approved" and "provisional_until" in doc:
        out.append(f"{rel}: approved, so it must not have provisional_until")
    return out


def check_predicate(where, pred, readable):
    """The shape of a predicate (all, any, not, signal, attr with one operator), and the columns it reads."""
    if isinstance(pred, bool):
        return []
    if not isinstance(pred, dict) or not pred:
        return [f"{where}: bad predicate {pred!r}"]
    for key in ("all", "any"):
        if key in pred:
            if not isinstance(pred[key], list) or len(pred) != 1:
                return [f"{where}: '{key}' takes a list and nothing else"]
            return [p for sub in pred[key] for p in check_predicate(where, sub, readable)]
    if "not" in pred:
        return check_predicate(where, pred["not"], readable) if len(pred) == 1 else [f"{where}: 'not' takes one"]
    if "signal" in pred:
        return [] if len(pred) == 1 else [f"{where}: 'signal' takes a name and nothing else"]
    if "attr" in pred:
        ops = set(pred) - {"attr"}
        if len(ops) != 1 or not ops <= OPS:
            return [f"{where}: attr test needs exactly one operator from {sorted(OPS)}: {pred!r}"]
        if readable is not None and pred["attr"] not in readable:
            return [f"{where}: reads {pred['attr']!r}, which no table stores and data/schema/model.yaml doesn't "
                    "declare as derived (WP5b F-15)"]
        return []
    return [f"{where}: bad predicate {pred!r}"]


class Tables:
    """Each declared table's rows, read once. A table that can't be read is itself a problem."""

    def __init__(self, root):
        self.root, self.m, self.cache, self.problems = root, model.declared(root), {}, []

    def rows(self, name):
        if name not in self.cache:
            try:
                self.cache[name] = model.rows(name, self.root)
            except Exception as e:
                self.problems.append(f"{name}: can't be read: {e!r}")
                self.cache[name] = []
        return self.cache[name]

    def keys(self, name, column=None):
        cols = [column] if column else self.m["tables"][name].get("key") or []
        return {tuple(r.get(c) for c in cols) if len(cols) > 1 else r.get(cols[0]) for r in self.rows(name)}


def test_exists(root, ref):
    """file::Class::method names a test method that exists."""
    parts = str(ref).split("::")
    path = root / parts[0]
    return len(parts) == 3 and path.exists() and bool(
        re.search(rf"^\s+def {re.escape(parts[2])}\(", path.read_text(), re.M))


def type_ok(tables, spec, value):
    """None if the value meets the column type, else the reason it doesn't."""
    m = re.fullmatch(r"optional\((.*)\)", spec)
    if m:
        return None if value is None else type_ok(tables, m.group(1), value)
    if value is None:
        return "missing"
    m = re.fullmatch(r"list\((.*)\)", spec)
    if m:
        if not isinstance(value, list):
            return "not a list"
        return next((r for r in (type_ok(tables, m.group(1), v) for v in value) if r), None)
    m = re.fullmatch(r"enum\((.*)\)", spec)
    if m:
        return None if value in tables.m["enums"][m.group(1)] else f"{value!r} is not one of {m.group(1)}"
    m = re.fullmatch(r"fk\(([a-z_]+)(?:\.([a-z_]+))?\)", spec)
    if m:
        return None if value in tables.keys(m.group(1), m.group(2)) else f"{value!r} is not a {spec[3:-1]}"
    checks = {"id": lambda v: isinstance(v, int) and not isinstance(v, bool),
              "int": lambda v: isinstance(v, int) and not isinstance(v, bool),
              "bool": lambda v: isinstance(v, bool),
              "name": lambda v: isinstance(v, (str, int)) and str(v).strip() != "",
              "text": lambda v: isinstance(v, str) and v.strip() != "",
              "mapping": lambda v: isinstance(v, dict),
              "predicate": lambda v: isinstance(v, (dict, bool)),
              "date": lambda v: isinstance(v, datetime.date) or bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(v))),
              "path": lambda v: (tables.root / str(v)).exists(),
              "test": lambda v: test_exists(tables.root, v)}
    if spec not in checks:
        return f"unknown column type {spec!r} in data/schema/model.yaml"
    return None if checks[spec](value) else f"{value!r} is not a {spec}"


def check_tables(tables):
    """Every declared table against its declaration."""
    out = []
    for name, t in tables.m["tables"].items():
        rows, cols, key = tables.rows(name), t.get("columns") or {}, t.get("key") or []
        seen = set()
        for i, r in enumerate(rows):
            where = f"{name}[{'/'.join(str(r.get(k)) for k in key) or i}]" if isinstance(r, dict) else f"{name}[{i}]"
            if not isinstance(r, dict):
                out.append(f"{where}: a row must be a mapping")
                continue
            k = tuple(r.get(c) for c in key)
            if key and k in seen:
                out.append(f"{where}: the key ({', '.join(key)}) is not unique")
            seen.add(k)
            if not t.get("open"):
                for c in sorted(set(r) - set(cols)):
                    out.append(f"{where}: column {c!r} is not declared in data/schema/model.yaml")
            for c, spec in cols.items():
                reason = type_ok(tables, spec, r.get(c))
                if reason:
                    out.append(f"{where}: {c}: {reason}")
            if t.get("one_of"):
                matches = [g for g in t["one_of"] if all(r.get(c) is not None for c in g)
                           and all(r.get(c) is None for other in t["one_of"] if other != g for c in other)]
                if len(matches) != 1:
                    out.append(f"{where}: needs exactly one of {' or '.join('+'.join(g) for g in t['one_of'])}")
            for fk_cols, target in (t.get("foreign") or {}).items():
                fcols = [c.strip() for c in fk_cols.split(",")]
                if all(r.get(c) is not None for c in fcols):
                    value = tuple(r[c] for c in fcols) if len(fcols) > 1 else r[fcols[0]]
                    if value not in tables.keys(target):
                        out.append(f"{where}: ({fk_cols}) = {value} is not a {target}")
            by_source = t.get("foreign_by_source")
            if by_source and r.get("source") in by_source:
                target = by_source[r["source"]]
                if str(r.get("ref")) not in {str(x) for x in tables.keys(target)}:
                    out.append(f"{where}: {r['source']} {r.get('ref')!r} is not a {target}")
        for u in t.get("unique") or []:
            values = [r.get(u) for r in rows if isinstance(r, dict) and r.get(u) is not None]
            for v in sorted({v for v in values if values.count(v) > 1}, key=str):
                out.append(f"{name}: {u} {v!r} appears more than once")
        if t.get("disjoint_from"):
            for k in sorted(tables.keys(name) & tables.keys(t["disjoint_from"]), key=str):
                out.append(f"{name}: {k} is also in {t['disjoint_from']}")
    return out


def check_rules(tables):
    """The rules that span tables (kind-list meta-rules 4 and 8; TX-5; WP3; WP5b F-10, F-15)."""
    out, root = [], tables.root
    repo = {r["repo_id"]: r for r in tables.rows("repo")}
    for name in REPO_NAMED:
        for r in tables.rows(name):
            if isinstance(r, dict) and r.get("repo_id") in repo and r.get("name") != repo[r["repo_id"]]["name"]:
                out.append(f"{name}: repository {r['repo_id']} is named {r.get('name')!r} here but "
                           f"{repo[r['repo_id']]['name']!r} in the snapshot (renamed?)")
    reg = {r["repo_id"]: r for r in tables.rows("registry_entry")}
    for rid in sorted(set(repo) - set(reg)):
        out.append(f"registry.yaml: repository {repo[rid]['name']} ({rid}) has no entry (kind-list meta-rule 4)")
    names = [str(r.get("name")) for r in tables.rows("registry_entry")]
    if names != sorted(names, key=str.lower):
        out.append("registry.yaml: entries must be sorted by name, ignoring case (kind-list meta-rule 8)")
    for r in tables.rows("registry_entry") + tables.rows("org_entry"):
        if (r.get("source") == "maintainer") != bool(str(r.get("decision") or "").strip()):
            out.append(f"registry.yaml: {r.get('name')}: a decision is stated exactly when the source is maintainer "
                       "(WP5c OD1)")
    for s in sorted(tables.keys("signal") - tables.keys("signal_explanation")):
        out.append(f"data/taxonomy/kinds.yaml: signal {s} has no explanation in `explain` (WP5d D-1)")
    for r in tables.rows("maintainer_set"):
        owners = r.get("owners") or []
        if owners and not 2 <= len(owners) <= 3:
            out.append(f"data/maintainers.yaml: owners must be empty (not decided yet) or 2 or 3 maintainers, got "
                       f"{len(owners)} (maintainer policy 2; WP5f)")
        if len(set(owners)) != len(owners):
            out.append("data/maintainers.yaml: an owner is listed twice")
    for r in tables.rows("maintainer_verification"):
        if r.get("verified_by") == r.get("user_id"):
            out.append(f"data/maintainers.yaml: {r.get('user_id')}: a maintainer can't verify themself (WP5e)")
    for source, table, key in (("nist", "nist_control", "control_id"), ("dodcio", "dodcio_section", "section"),
                               ("ofac", "ofac_item", "item"), ("ssdf", "ssdf_practice", "practice"),
                               ("c_scrm", "c_scrm_control", "control")):  # WP5d (NIST), WP5e (the rest)
        cited = {str(r["ref"]) for r in tables.rows("policy_cite") if r["source"] == source}
        for r in tables.rows(table):
            if str(r[key]) not in cited and not str(r.get("context") or "").strip():
                out.append(f"{tables.m['tables'][table]['rows'].split(',')[0]}: {r[key]} is cited by no policy and "
                           "states no context")
    covered = tables.keys("pilot_member") | tables.keys("excluded")
    for rid in sorted(set(reg) - covered):
        out.append(f"data/exclude.yaml: {reg[rid].get('name')} is neither in the pilot nor excluded (TX-5)")
    if not str(model.load("data/exclude.yaml", root).get("default_reason") or "").strip():
        out.append("data/exclude.yaml: default_reason must state why a repository is excluded (F-10)")
    if tables.keys("proposed_codeowner") != {m.get("login") for m in tables.rows("maintainer")}:
        out.append("data/proposed-codeowners: must list exactly the maintainers in data/maintainers.yaml")
    readable = set(tables.m.get("derived") or {})
    for r in tables.rows("repo"):
        if not r.get("after_snapshot"):
            readable |= set(r)
    for r in tables.rows("kind"):
        out += check_predicate(f"kind {r.get('type')}/{r.get('stage')}", r.get("recommend_when"), readable)
    for r in tables.rows("flag"):
        out += check_predicate(f"flag {r.get('flag')}", r.get("when"), readable)
    for r in tables.rows("unclassified_reason"):
        out += check_predicate(f"unclassified_reason {r.get('position')}", r.get("when"), readable)
    for r in tables.rows("signal"):
        out += check_predicate(f"signal {r.get('signal')}", r.get("when"), readable)
    for r in tables.rows("pilot_category"):
        out += check_predicate(f"pilot_category {r.get('category')}", r.get("where"), readable)
    return out


def check_meta_rules(root):
    """The taxonomy's and the policies' own meta-rules, as scripts/recommend.py and scripts/policies.py make them."""
    out = []
    try:
        check_taxonomy(model.load("data/taxonomy/kinds.yaml", root), model.load("data/taxonomy/tiers.yaml", root))
    except (TaxonomyError, KeyError, TypeError, AttributeError) as e:
        out += [f"data/taxonomy: {line}" for line in str(e).splitlines()]
    try:
        pols, deps = P.load_policies(root / "data/policies")
        src = lambda rel: model.load(rel, root)  # noqa: E731
        out += [f"data/policies: {p}" for p in P.check(
            pols, deps, src("data/taxonomy/kinds.yaml"), src("data/taxonomy/tiers.yaml"),
            src("data/sources/openssf-security-baseline.yaml"), root,
            set(src("data/sources/cisa-practices.yaml")["practices"]),
            set(src("data/sources/nist-800-53.yaml")["controls"]),
            src("data/sources/github-plan.yaml")["plan"], src("data/policies/_future.yaml"))]
        out += [f"data/policies: {p}" for p in P.check_set(src("data/policies/_set.yaml"))]
    except Exception as e:
        out.append(f"data/policies: can't be checked: {e!r}")
    return out


def check(root):
    root = pathlib.Path(root)
    tables = Tables(root)
    out = []
    for rel in PROVISIONAL_FILES:
        try:
            out += provisional_mark(rel, root)
        except Exception as e:
            out.append(f"{rel}: can't be read: {e!r}")
    out += check_meta_rules(root)
    out += check_tables(tables)
    out += check_rules(tables)
    return tables.problems + out


def files(root):
    listed = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=root,
                            capture_output=True, text=True, check=True).stdout.splitlines()
    return [f for f in listed if (pathlib.Path(root) / f).is_file()]


def renders(root):
    """Every view renders, and the same twice (WP5b R-5). Broken software is a construction error too."""
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        try:
            first, second = R.render(a, root), R.render(b, root)
        except SystemExit as e:
            return [str(e)]
        if first != second:
            return ["render: the two runs wrote different files"]
        _, mismatch, errors = filecmp.cmpfiles(a, b, first, shallow=False)
        return [f"render: {f} differs between two runs (not deterministic)" for f in mismatch + errors]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--no-render", action="store_true", help="skip rendering the views")
    args = ap.parse_args()
    root = pathlib.Path(args.root).resolve()
    problems = check(root)
    if not problems and not args.no_render:
        problems = renders(root)
    if problems:
        sys.exit("invalid (WP0 R-14):\n  " + "\n  ".join(problems))
    print("valid: every table meets data/schema/model.yaml" + ("" if args.no_render else
                                                                 ", and every view renders, the same twice"))


if __name__ == "__main__":
    main()

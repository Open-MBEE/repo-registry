#!/usr/bin/env python3
"""Reproduce each finding of the WP5b data audit (work-packages/WP5b-audit.md, WP5b D-2, R-3).

Read-only and offline. Each finding is one function: it returns the rows that break the declared model
(data/schema/model.yaml), and the audit prints its ID, its count and a sample. Each query checks the condition the
finding names, so a fixed finding returns no rows (tests/test_wp5b.py checks that every one does).

Usage: python3 scripts/audit.py [F-01 ...]   (no arguments: every finding)
"""
import collections
import glob
import json
import pathlib
import re
import subprocess
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model  # noqa: E402
import validate  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
KIND_NAME = re.compile(r"\b(tool|media|research|governance)/(sandbox|incubating|graduated|archived)\b")


def load(rel):
    return yaml.safe_load((ROOT / rel).read_text())


def tracked(pattern="*"):
    out = subprocess.run(["git", "ls-files", pattern], cwd=ROOT, capture_output=True, text=True, check=True)
    return out.stdout.split()


PROSE = {"meaning", "reason", "decision", "note", "why", "basis", "statement", "known_from", "closes_in", "capability",
         "evidence_when_closed", "setup", "applies_note", "default_reason"}


def model_rows():
    for name, t in model.declared(ROOT)["tables"].items():
        if t["role"] == "model":
            for r in model.rows(name, ROOT):
                yield name, r


def f01():
    """The kind table is keyed by the kind name, a composite key (type, stage) stored as one string."""
    k = load("data/taxonomy/kinds.yaml")
    return [f"{section}: {n}" for section in ("kinds", "omitted") for n in (k.get(section) or {}) if "/" in str(n)]


def f02():
    """The kind name is stored as a value outside the kind table (outside prose)."""
    return [f"{name}.{col}" for name, r in model_rows() for col, v in r.items()
            if col not in PROSE and KIND_NAME.search(yaml.safe_dump(v))]


def f03():
    """Repositories are keyed and joined by name, not by GitHub's repository ID."""
    rows = []
    if not (model.snapshot_dir(ROOT) / "ids.json").exists():
        rows.append("the snapshot has no ids.json")
    for name, t in model.declared(ROOT)["tables"].items():
        if "repo_id" in (t.get("columns") or {}):
            rows += [f"{name}: {r.get('name')} has repo_id {r.get('repo_id')!r}" for r in model.rows(name, ROOT)
                     if not isinstance(r.get("repo_id"), int)]
    return rows


def f04():
    """A repository in the model has no row in the source table."""
    ids = set(model.repos(ROOT))
    return [f"registry.yaml: {e['name']}" for rid, e in load("registry.yaml")["repos"].items() if rid not in ids]


def f05():
    """People are keyed by login, not by GitHub's user ID."""
    return [f"data/maintainers.yaml: {k!r}" for k in load("data/maintainers.yaml")["maintainers"] if not isinstance(k, int)]


def f06():
    """A foreign key held in prose: a future feature's `strengthens` isn't a list of policy IDs."""
    pols = {pathlib.Path(p).stem for p in glob.glob(str(ROOT / "data/policies/[a-z]*.yaml"))}
    rows = []
    for feat, v in load("data/policies/_future.yaml")["features"].items():
        if "would_strengthen" in v or not isinstance(v.get("strengthens"), list):
            rows.append(f"{feat}: no strengthens list")
        rows += [f"{feat}: {ref!r} is not a policy" for ref in v.get("strengthens") or [] if ref not in pols]
    return rows


def f07():
    """Views are committed: a rendered view, or a generated report, stored in the repository."""
    views = {"data/reports/kind-recommendations.yaml", "data/reports/license-report.yaml",
             "data/reports/maintainers-match.yaml", "data/reports/policy-applicability.yaml",
             "docs/policy-applicability.md", "docs/pilot-briefing.md", "docs/data-model.md",
             "docs/policy-basis-tables.md"}
    return sorted(set(tracked()) & views) + [p for p in tracked("data/reports/*")]


def f08():
    """Hand-written documents that state derived facts, which can drift from the model."""
    rows = [f"{p}: a hand-written SOP" for p in tracked("docs/sops/*.md")]
    basis = (ROOT / "docs/policy-basis-review.md").read_text()
    if re.search(r"^\| \[[a-z-]+\]\(sops/", basis, re.M) or re.search(r"^\| (SB|TI|OI|TG|OG)-\d+ \|", basis, re.M):
        rows.append("docs/policy-basis-review.md: a hand-written policy or trace table")
    # docs/fit-analysis.md is excluded: it is WP4's dated record of one analysis of one stored snapshot, not a current
    # statement, and its figures are the findings of that analysis.
    for doc in ["docs/policy-basis-review.md", "docs/current-state.md", "docs/status.md"]:
        for n, what in re.findall(r"\b(\d{2,3})\s+(repositor\w+|repos|policies|tests|kinds|public)",
                                  (ROOT / doc).read_text()):
            rows.append(f"{doc}: a count, '{n} {what}'")
    return rows


def f09():
    """A derived value stored in the model: the pilot list stores each member's kind."""
    return [f"data/pilot.yaml: {e.get('name')}.kind" for e in load("data/pilot.yaml")["repos"].values() if "kind" in e]


def f10():
    """A constant stored once per row: an exclude-list row repeating the default reason."""
    ex = load("data/exclude.yaml")
    return [f"{e.get('name')}: repeats the default reason" for e in (ex.get("repos") or {}).values()
            if not isinstance(e, dict) or e.get("reason") == ex.get("default_reason")]


def f11():
    """Columns named inconsistently: `status` used for a color, or `why` for a row's reason."""
    rows = [f"{name}.{col}" for name, r in model_rows() for col in r
            if (col == "status" and r[col] not in ("provisional", "approved")) or col == "why"]
    return rows


def f12():
    """Data files that no declared table reads: their shape is checked by nothing."""
    declared = " ".join(str(t["rows"]) for t in model.declared(ROOT)["tables"].values())
    files = [p for p in tracked("data/*") if p.endswith((".yaml", ".json")) and not p.startswith(("data/snapshots/",
                                                                                               "data/schema/"))]
    stems = lambda p: {p, pathlib.Path(p).name}  # noqa: E731
    return [f"{p}: no table" for p in files if not any(s in declared for s in stems(p))
            and not p.startswith("data/policies/") and not p.startswith("data/sources/")]


def f13():
    """A table-level fact stored in every row: a policy file holding status or provisional_until."""
    return [f"{pathlib.Path(p).name}" for p in glob.glob(str(ROOT / "data/policies/[a-z]*.yaml"))
            if {"status", "provisional_until"} & set(yaml.safe_load(pathlib.Path(p).read_text()))]


def f14():
    """The snapshot path stored in a model file instead of once, in data/schema/model.yaml."""
    rels = ["registry.yaml", "data/pilot.yaml", "data/exclude.yaml", "data/assignments.yaml"]
    return [f"{rel}: snapshot" for rel in rels if "snapshot" in (load(rel) or {})]


def f15():
    """Predicates that read columns declared nowhere (no table stores them, and they aren't declared as derived)."""
    tables = validate.Tables(ROOT)
    return [p for p in validate.check_rules(tables) if "no table stores" in p]


def f16():
    """Gaps not split by kind of error: an expected-gaps table, a forthcoming row with no test, or a measured gap
    with no policy and check."""
    rows = ["data/expected-gaps.yaml: exists"] if (ROOT / "data/expected-gaps.yaml").exists() else []
    rows += [f"forthcoming {g}: no test" for g, r in load("data/forthcoming.yaml")["forthcoming"].items()
             if not r.get("test")]
    rows += [f"measured {g}: no policy and check" for g, r in load("data/measured-gaps.yaml")["measured"].items()
             if not (r.get("policy") and r.get("check"))]
    return rows


FINDINGS = {f"F-{i:02d}": f for i, f in enumerate([f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f12, f13,
                                                   f14, f15, f16], 1)}


def main():
    wanted = sys.argv[1:] or list(FINDINGS)
    for fid in wanted:
        rows = FINDINGS[fid]()
        print(f"{fid} ({len(rows)}): {FINDINGS[fid].__doc__.splitlines()[0]}")
        for r in rows[:4]:
            print(f"    {r}")
        if len(rows) > 4:
            print(f"    ... and {len(rows) - 4} more")


if __name__ == "__main__":
    main()

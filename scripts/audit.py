#!/usr/bin/env python3
"""Reproduce each finding of the WP5b data audit (work-packages/WP5b-audit.md, WP5b D-2, R-3).

Read-only and offline. Each finding is one function: it returns the rows that break the declared model
(data/schema/model.yaml), and the audit prints its ID, its count and a sample. A finding that is fixed returns no rows.

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

ROOT = pathlib.Path(__file__).resolve().parent.parent
KIND_NAME = re.compile(r"\b(tool|media|research|governance)/(sandbox|incubating|graduated|archived)\b")


def load(rel):
    return yaml.safe_load((ROOT / rel).read_text())


def snapshot():
    return json.loads((ROOT / "data/snapshots/2026-10-18/repos.json").read_text())


def policy_files():
    return sorted(glob.glob(str(ROOT / "data/policies/[a-z]*.yaml")))


def tracked(pattern="*"):
    out = subprocess.run(["git", "ls-files", pattern], cwd=ROOT, capture_output=True, text=True, check=True)
    return out.stdout.split()


def f01():
    """The kind table is keyed by the kind name, a composite key (type, stage) stored as one string."""
    k = load("data/taxonomy/kinds.yaml")
    return [f"kinds: {n}" for n in k["kinds"]] + [f"omitted: {n}" for n in k.get("omitted", {})]


def f02():
    """The kind name is stored as a value outside the kind table (model and committed views)."""
    rows = []
    for rel in ["data/pilot.yaml", "data/pilot-rule.yaml", "data/reports/kind-recommendations.yaml",
                "data/reports/license-report.yaml", "data/reports/policy-applicability.yaml"]:
        n = len(KIND_NAME.findall((ROOT / rel).read_text()))
        if n:
            rows.append(f"{rel}: {n}")
    return rows


def f03():
    """Repositories are keyed and joined by name; no table holds GitHub's repository ID."""
    rows = []
    for rel in ["registry.yaml", "data/assignments.yaml", "data/pilot.yaml", "data/exclude.yaml",
                "data/reports/license-report.yaml", "data/reports/kind-recommendations.yaml"]:
        rows.append(f"{rel}: repos keyed by name ({len(load(rel)['repos'])})")
    rows.append(f"data/snapshots/2026-10-18/usage.json: keyed by name ({len(json.loads((ROOT / 'data/snapshots/2026-10-18/usage.json').read_text())['repos'])})")
    rule = load("data/pilot-rule.yaml")
    rows.append(f"data/pilot-rule.yaml: must_include and self_registered by name ({len(rule['must_include']) + len(rule['self_registered'])})")
    rows.append("data/maintainers.yaml: release_authority by name")
    rows.append("data/deviations.yaml: repo by name (no rows yet)")
    if "id" not in snapshot()[0]:
        rows.append("data/snapshots/2026-10-18/repos.json: no id column")
    return rows


def f04():
    """A repository in the model has no row in the source table (the snapshot predates it)."""
    names = {r["name"] for r in snapshot()}
    return [f"registry.yaml: {n}" for n in load("registry.yaml")["repos"] if n not in names]


def f05():
    """People are keyed and joined by login, which GitHub lets a user change; no table holds the user ID."""
    m = load("data/maintainers.yaml")["maintainers"]
    return [f"data/maintainers.yaml: {login}" for login in m] + \
        ["data/proposed-codeowners: joins by @login", "data/deviations.yaml: approved_by is a login"]


def f06():
    """A foreign key held in free text: _future.yaml's would_strengthen lists policy IDs in prose."""
    pols = {pathlib.Path(p).stem for p in policy_files()}
    rows = []
    for feat, v in load("data/policies/_future.yaml")["features"].items():
        for ref in re.findall(r"[a-z][a-z0-9-]+(?:-[a-z0-9]+)+|[a-z]+", v["would_strengthen"]):
            if ref not in pols and ref not in ("and", "set", "once", "for", "all", "repositories", "who", "changed",
                                               "roles", "when", "fine", "grained", "maintainer", "powers"):
                rows.append(f"{feat}: {ref!r} is not a policy")
        rows.append(f"{feat}: would_strengthen is text ({v['would_strengthen']!r})")
    return rows


def f07():
    """Views are committed: generated files stored in the repository (WP5b OD4: views are not committed)."""
    views = ["data/reports/kind-recommendations.yaml", "data/reports/license-report.yaml",
             "data/reports/maintainers-match.yaml", "data/reports/policy-applicability.yaml",
             "docs/policy-applicability.md", "docs/pilot-briefing.md"]
    return [v for v in views if v in tracked()]


def f08():
    """Hand-written documents that state derived facts, which can drift from the model."""
    rows = [f"{p}: 'Applies to' line" for p in tracked("docs/sops/*.md")]
    rows += [f"{p}: attestation entries" for p in tracked("docs/sops/*.md") if "```yaml" in (ROOT / p).read_text()]
    rows.append("docs/policy-basis-review.md: the policy table and the coverage tables")
    for doc in ["docs/fit-analysis.md", "docs/policy-basis-review.md", "docs/current-state.md", "docs/status.md"]:
        for n, what in re.findall(r"\b(\d{2,3})\s+(repositor\w+|repos|policies|tests|kinds|public)", (ROOT / doc).read_text()):
            rows.append(f"{doc}: a count, '{n} {what}'")
    return rows


def f09():
    """A derived value stored in the model: the pilot list stores each member's kind."""
    return [f"data/pilot.yaml: {n}.kind" for n, e in load("data/pilot.yaml")["repos"].items() if "kind" in e]


def f10():
    """A constant stored once per row: every exclude-list row holds the same reason."""
    ex = load("data/exclude.yaml")["repos"]
    reasons = collections.Counter(ex.values())
    return [f"{count} rows: {reason!r}" for reason, count in reasons.items() if count > 1]


def f11():
    """The same column name with different domains, or the same idea under different names."""
    return [
        "status: a lifecycle mark (provisional | approved) in model files, a color (green | yellow | red) in reports",
        "stage: our stage in the kind list; OpenSSF's stage in the baseline (the same values, a mapped domain)",
        "the reason for a row: `reason` (registry), `why` (pilot), the bare value (exclude), `decision` (assignments), "
        "`basis` (maintainers)",
    ]


def f12():
    """Tables with no schema: shapes are checked only by code, or not at all."""
    schemas = {p for p in tracked("data/schema/*.yaml")}
    files = [p for p in tracked("data/*") if p.endswith((".yaml", ".json")) and not p.startswith("data/snapshots/")
             and not p.startswith("data/schema/")] + ["registry.yaml"]
    covered = {"registry.yaml"}  # kind-list.schema.yaml; attestations.schema.yaml is for other repositories
    return [f"{p}: no schema" for p in sorted(set(files) - covered)] + [f"(schemas: {len(schemas)})"]


def f13():
    """A table-level fact stored in every row: each policy file repeats status and provisional_until."""
    return [f"{pathlib.Path(p).name}: status, provisional_until" for p in policy_files()]


def f14():
    """A foreign key to a directory, stored as a string in several files: the snapshot path."""
    rows = []
    for rel in ["registry.yaml", "data/pilot.yaml", "data/reports/kind-recommendations.yaml",
                "data/reports/license-report.yaml", "data/reports/maintainers-match.yaml"]:
        if "snapshot" in (load(rel) or {}):
            rows.append(f"{rel}: snapshot = {load(rel)['snapshot']}")
    return rows


def f15():
    """Predicates read columns that are declared nowhere: repo attributes, derived ones, and the pilot's own."""
    cols = set(snapshot()[0])
    used = collections.defaultdict(set)

    def walk(where, p):
        if isinstance(p, dict):
            if "attr" in p:
                used[p["attr"]].add(where)
            for v in p.values():
                walk(where, v)
        elif isinstance(p, list):
            for v in p:
                walk(where, v)
    walk("kinds.yaml", load("data/taxonomy/kinds.yaml"))
    walk("pilot-rule.yaml", load("data/pilot-rule.yaml")["categories"])
    return [f"{a} (read by {', '.join(sorted(w))}): not a snapshot column" for a, w in sorted(used.items())
            if a not in cols]


def f16():
    """An undeclared join by naming convention: each expected gap XF-n is tied to a test named test_XFn."""
    return [f"{g} -> tests/test_forthcoming.py test_{g.replace('-', '')}" for g in load("data/expected-gaps.yaml")["gaps"]]


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

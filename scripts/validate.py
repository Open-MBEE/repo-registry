#!/usr/bin/env python3
"""Check every data file against its meta-rules, so that no invalid state reaches main (WP5 D-1; WP0 R-14).

Invalid means not correctly constructed: a data file breaks a meta-rule (docs/kind-list-format.md,
docs/policy-format.md, and the shapes stated in each file's header). Out of compliance is valid: nothing here reads a
policy's verdict, so a change that leaves a repository red passes. The checks the generators already make are reused,
not copied. Finally every generator is replayed from the stored snapshot in a scratch copy, and every generated file
must come out byte for byte the same (WP5 R-3). The kind list (registry.yaml) is not a generated file: recommend.py
only drafted it, and people change it one entry at a time (WP0 R-12), so its replay goes to a scratch path and the
files derived from the kind list are regenerated from the kind list as it is. Deterministic and offline.

Usage: python3 scripts/validate.py [--root .] [--no-replay]   (exit 1, naming each problem; exit 0 when valid)
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import org  # noqa: E402
import policies as P  # noqa: E402
from recommend import TaxonomyError, check_taxonomy  # noqa: E402

LOGIN = re.compile(r"^[A-Za-z0-9-]+$")
OPS = {"eq", "in", "matches", "gt", "gte", "lt"}


def provisional_mark(name, text, doc):
    """AGENTS.md rule 3 and kind-list meta-rules 2-3: provisional data is marked, in a way a program can check."""
    problems = []
    status = doc.get("status")
    if status not in ("provisional", "approved"):
        problems.append(f"{name}: status must be provisional or approved, not {status!r}")
    if status == "provisional":
        if not str(doc.get("provisional_until") or "").strip():
            problems.append(f"{name}: provisional, but provisional_until doesn't name the approval that lifts it")
        if not text.startswith("# PROVISIONAL"):
            problems.append(f"{name}: provisional, but the first line doesn't start with '# PROVISIONAL'")
    if status == "approved" and "provisional_until" in doc:
        problems.append(f"{name}: approved, so it must not have provisional_until")
    return problems


def check_predicate(name, pred):
    """The shape of a predicate in the kinds.yaml language (all, any, not, attr with one operator)."""
    if isinstance(pred, bool):
        return []
    if not isinstance(pred, dict) or not pred:
        return [f"{name}: bad predicate {pred!r}"]
    for key in ("all", "any"):
        if key in pred:
            if not isinstance(pred[key], list) or len(pred) != 1:
                return [f"{name}: '{key}' takes a list and nothing else"]
            return [p for sub in pred[key] for p in check_predicate(name, sub)]
    if "not" in pred:
        return check_predicate(name, pred["not"]) if len(pred) == 1 else [f"{name}: 'not' takes one predicate"]
    if "attr" in pred:
        ops = set(pred) - {"attr"}
        if len(ops) != 1 or not ops <= OPS:
            return [f"{name}: attr test needs exactly one operator from {sorted(OPS)}: {pred!r}"]
        return []
    return [f"{name}: bad predicate {pred!r}"]


class Data:
    """Each data file, read once. A file that can't be read is itself a problem."""

    def __init__(self, root):
        self.root, self.problems, self.text = root, [], {}

    def load(self, rel):
        path = self.root / rel
        try:
            self.text[rel] = path.read_text(encoding="utf-8")
            doc = yaml.safe_load(self.text[rel])
        except (OSError, yaml.YAMLError) as e:
            self.problems.append(f"{rel}: can't be read: {e}")
            return None
        if not isinstance(doc, dict):
            self.problems.append(f"{rel}: must be a mapping")
            return None
        return doc


def check(root):
    d = Data(root)
    out = d.problems
    kinds_doc, tiers_doc = d.load("data/taxonomy/kinds.yaml"), d.load("data/taxonomy/tiers.yaml")
    registry = d.load("registry.yaml")
    assignments = d.load("data/assignments.yaml")
    maint = d.load("data/maintainers.yaml")
    deviations = d.load("data/deviations.yaml")
    rule, pilot, exclude = d.load("data/pilot-rule.yaml"), d.load("data/pilot.yaml"), d.load("data/exclude.yaml")
    gaps = d.load("data/expected-gaps.yaml")
    if out:
        return out
    for rel, doc in [("data/taxonomy/kinds.yaml", kinds_doc), ("data/taxonomy/tiers.yaml", tiers_doc),
                     ("registry.yaml", registry), ("data/assignments.yaml", assignments),
                     ("data/maintainers.yaml", maint), ("data/deviations.yaml", deviations),
                     ("data/pilot-rule.yaml", rule), ("data/pilot.yaml", pilot), ("data/exclude.yaml", exclude)]:
        out += provisional_mark(rel, d.text[rel], doc)

    # The taxonomy (kind-list meta-rule 10; WP1 R-3, R-6).
    try:
        check_taxonomy(kinds_doc, tiers_doc)
    except (TaxonomyError, KeyError, TypeError, AttributeError) as e:
        out += [f"data/taxonomy: {line}" for line in str(e).splitlines()]
        return out
    kinds = kinds_doc["kinds"]

    # The kind list (docs/kind-list-format.md, meta-rules 1-9).
    R = "registry.yaml"
    extra = set(registry) - {"status", "org", "repos", "snapshot", "provisional_until"}
    if extra or not {"status", "org", "repos"} <= set(registry):
        out.append(f"{R}: top-level keys must be status, org, repos and optionally snapshot, provisional_until")
    org_entry = registry.get("org") or {}
    if not isinstance(org_entry, dict) or set(org_entry) != {"name", "kind"}:
        out.append(f"{R}: org must have exactly name and kind")
    elif org_entry["kind"] not in kinds:
        out.append(f"{R}: org kind {org_entry['kind']!r} is not a kind")
    repos = registry.get("repos") or {}
    if not isinstance(repos, dict):
        out.append(f"{R}: repos must map each repo's name to its entry")
        repos = {}
    names = list(repos)
    lowered = [n.lower() for n in names]
    for n in sorted({n for n in names if lowered.count(n.lower()) > 1}):
        out.append(f"{R}: {n}: two entries differ only by case")
    if names != sorted(names, key=str.lower):
        out.append(f"{R}: entries must be sorted by name, ignoring case")
    for n, e in repos.items():
        if not isinstance(e, dict) or "kind" not in e:
            out.append(f"{R}: {n}: needs a kind")
            continue
        if set(e) - {"kind", "reason"}:
            out.append(f"{R}: {n}: no fields other than kind and reason ({', '.join(sorted(set(e) - {'kind', 'reason'}))})")
        if e["kind"] not in kinds and e["kind"] != "unclassified":
            out.append(f"{R}: {n}: kind {e['kind']!r} is not a kind")
        if ("reason" in e) != (e["kind"] == "unclassified") or ("reason" in e and not str(e["reason"]).strip()):
            out.append(f"{R}: {n}: a non-empty reason is needed exactly when the kind is unclassified")
    snapshot = registry.get("snapshot")
    if snapshot:
        try:
            public = {r["name"] for r in yaml.safe_load((root / snapshot / "repos.json").read_text())}
        except (OSError, yaml.YAMLError, TypeError, KeyError) as e:
            out.append(f"{R}: snapshot {snapshot} can't be read: {e}")
            public = None
        if public is not None:
            for n in sorted(set(repos) - public - set((assignments.get("repos") or {}))):
                out.append(f"{R}: {n}: not a public repo in the snapshot, and not assigned (WP1 OD2)")

    # Assigned kinds.
    A = "data/assignments.yaml"
    a_org = assignments.get("org") or {}
    if a_org.get("kind") not in kinds or not str(a_org.get("decision") or "").strip():
        out.append(f"{A}: org needs a defined kind and the decision it comes from")
    elif a_org["kind"] != org_entry.get("kind"):
        out.append(f"{A}: org kind {a_org['kind']} differs from registry.yaml's {org_entry.get('kind')}")
    for n, e in (assignments.get("repos") or {}).items():
        if not isinstance(e, dict) or set(e) != {"kind", "decision"} or e["kind"] not in kinds \
                or not str(e["decision"]).strip():
            out.append(f"{A}: {n}: needs exactly a defined kind and the decision it comes from")
        elif (repos.get(n) or {}).get("kind") != e["kind"]:
            out.append(f"{A}: {n}: assigned {e['kind']}, but registry.yaml says {(repos.get(n) or {}).get('kind')}")

    # The policies (docs/policy-format.md, meta-rules 1-13), with the checks scripts/policies.py makes.
    try:
        pols, deps = P.load_policies(root / "data/policies")
        src = lambda rel: yaml.safe_load((root / rel).read_text())  # noqa: E731
        out += [f"data/policies: {p}" for p in P.check(
            pols, deps, kinds_doc, tiers_doc, src("data/sources/openssf-security-baseline.yaml"), root,
            set(src("data/sources/cisa-practices.yaml")["practices"]),
            set(src("data/sources/nist-800-53.yaml")["controls"]),
            src("data/sources/github-plan.yaml")["plan"], src("data/policies/_future.yaml"))]
    except (OSError, yaml.YAMLError, KeyError, TypeError, AttributeError, TaxonomyError) as e:
        out.append(f"data/policies: can't be checked: {e!r}")
        pols = {}

    # The maintainers (docs/maintainer-policy.md) and the proposed CODEOWNERS that must match them.
    M = "data/maintainers.yaml"
    if set(maint) - {"status", "provisional_until", "target_size", "maintainers", "other_powers"}:
        out.append(f"{M}: unknown top-level keys {sorted(set(maint) - {'status', 'provisional_until', 'target_size', 'maintainers', 'other_powers'})}")
    if not isinstance(maint.get("target_size"), int) or maint["target_size"] < 1:
        out.append(f"{M}: target_size must be a positive whole number")
    people = maint.get("maintainers") or {}
    if not isinstance(people, dict) or not people:
        out.append(f"{M}: maintainers must name at least one person")
        people = {}
    if len({p.lower() for p in people}) != len(people):
        out.append(f"{M}: two logins differ only by case")
    for login, e in people.items():
        if not LOGIN.match(str(login)):
            out.append(f"{M}: {login!r} is not a GitHub login")
        if not isinstance(e, dict) or not {"name", "basis"} <= set(e) or set(e) - {"name", "basis", "release_authority"}:
            out.append(f"{M}: {login}: needs name and basis, and optionally release_authority, nothing else")
            continue
        if not str(e["name"]).strip() or not str(e["basis"]).strip():
            out.append(f"{M}: {login}: name and basis must not be empty")
        for r in e.get("release_authority") or []:
            if r not in repos:
                out.append(f"{M}: {login}: release authority for {r}, which is not in registry.yaml")
    if not isinstance(maint.get("other_powers"), list):
        out.append(f"{M}: other_powers must be a list (empty when none are declared)")
    try:
        owners = org.codeowners_logins((root / "data/proposed-codeowners").read_text())
        if owners != set(people):
            out.append("data/proposed-codeowners: must list exactly the maintainers in data/maintainers.yaml")
    except OSError as e:
        out.append(f"data/proposed-codeowners: can't be read: {e}")

    # Accepted exceptions (WP2a D-3): repo, policy, reason, approver.
    V = "data/deviations.yaml"
    devs = deviations.get("deviations")
    if not isinstance(devs, list):
        out.append(f"{V}: deviations must be a list (empty when none are accepted)")
        devs = []
    seen = set()
    for i, e in enumerate(devs):
        if not isinstance(e, dict) or set(e) != {"repo", "policy", "reason", "approved_by"}:
            out.append(f"{V}: entry {i + 1}: needs exactly repo, policy, reason and approved_by")
            continue
        if e["repo"] not in repos:
            out.append(f"{V}: entry {i + 1}: {e['repo']} is not in registry.yaml")
        if e["policy"] not in pols:
            out.append(f"{V}: entry {i + 1}: {e['policy']} is not a policy")
        if e["approved_by"] not in people:
            out.append(f"{V}: entry {i + 1}: {e['approved_by']} is not a maintainer")
        if not str(e["reason"]).strip():
            out.append(f"{V}: entry {i + 1}: no reason")
        if (e["repo"], e["policy"]) in seen:
            out.append(f"{V}: entry {i + 1}: a second exception for {e['repo']} and {e['policy']}")
        seen.add((e["repo"], e["policy"]))

    # The pilot rule, the pilot and the exclude list (WP4).
    PR = "data/pilot-rule.yaml"
    for key in ("must_include", "self_registered"):
        for n in rule.get(key) or []:
            if n not in repos:
                out.append(f"{PR}: {key} names {n}, which is not in registry.yaml")
    weights = rule.get("usage_score") or {}
    ids = []
    for c in rule.get("categories") or []:
        cid = c.get("id") if isinstance(c, dict) else None
        if not cid or not isinstance(c.get("quota"), int) or c["quota"] < 0 or not str(c.get("meaning") or "").strip():
            out.append(f"{PR}: category {cid!r}: needs id, a whole-number quota and a meaning")
            continue
        ids.append(cid)
        out += check_predicate(f"{PR}: {cid}", c.get("where"))
        if c.get("sort_by") not in (None, "usage_score", *weights):
            out.append(f"{PR}: {cid}: sort_by {c.get('sort_by')!r} is not usage_score or one of its parts")
    if len(set(ids)) != len(ids):
        out.append(f"{PR}: category ids must be unique")
    in_pilot, excluded = pilot.get("repos") or {}, exclude.get("repos") or {}
    for n, e in in_pilot.items():
        if not isinstance(e, dict) or set(e) != {"kind", "category", "why"}:
            out.append(f"data/pilot.yaml: {n}: needs exactly kind, category and why")
            continue
        if n not in repos:
            out.append(f"data/pilot.yaml: {n} is not in registry.yaml")
        elif e["kind"] != repos[n].get("kind"):
            out.append(f"data/pilot.yaml: {n}: kind {e['kind']} differs from registry.yaml's {repos[n].get('kind')}")
        if e["category"] not in ids and e["category"] != "must-include":
            out.append(f"data/pilot.yaml: {n}: category {e['category']!r} is not in the pilot rule")
    for n, why in excluded.items():
        if not str(why or "").strip():
            out.append(f"data/exclude.yaml: {n}: no reason")
        if n in in_pilot:
            out.append(f"data/exclude.yaml: {n} is both in the pilot and excluded")
    for n in sorted(set(repos) - set(in_pilot) - set(excluded)):
        out.append(f"data/exclude.yaml: {n} is neither in the pilot nor excluded (TX-5)")

    # Expected failures (tests/test_forthcoming.py).
    for gid, g in (gaps.get("gaps") or {}).items():
        if not re.match(r"^XF-\d+$", str(gid)) or not isinstance(g, dict) \
                or set(g) != {"gap", "closes_in", "evidence_when_closed"} \
                or not all(str(v).strip() for v in g.values()):
            out.append(f"data/expected-gaps.yaml: {gid}: needs an XF-n id and non-empty gap, closes_in and "
                       "evidence_when_closed")
    return out


def files(root):
    listed = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=root,
                            capture_output=True, text=True, check=True).stdout.splitlines()
    return [f for f in listed if (root / f).is_file()]


def replay(root):
    """Every generator, replayed from the stored snapshot in a scratch copy, writes back exactly what is here (R-3)."""
    snapshot = yaml.safe_load((root / "registry.yaml").read_text())["snapshot"]
    steps = [["recommend.py", "--snapshot", snapshot, "--registry", "drafted-registry.yaml"], ["policies.py"], ["licenses.py", "--snapshot", snapshot],
             ["org.py", "--snapshot", f"{snapshot}/org.json"], ["pilot.py", "--snapshot", snapshot],
             ["briefing.py", "--snapshot", snapshot]]
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        work = pathlib.Path(tmp)
        names = files(root)
        for f in names:
            (work / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / f, work / f)
        for step in steps:
            run = subprocess.run([sys.executable, str(work / "scripts" / step[0]), *step[1:]], cwd=work,
                                 capture_output=True, text=True)
            if run.returncode:
                return [f"scripts/{step[0]}: failed on replay: {(run.stderr or run.stdout).strip()}"]
        for f in names:
            if (work / f).read_bytes() != (root / f).read_bytes():
                out.append(f"{f}: differs from what its generator writes; regenerate it (see docs/current-state.md, "
                           "How to check everything), don't edit it by hand")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--no-replay", action="store_true", help="skip replaying the generators")
    args = ap.parse_args()
    root = pathlib.Path(args.root).resolve()
    problems = check(root)
    if not problems and not args.no_replay:
        problems = replay(root)
    if problems:
        sys.exit("invalid (WP0 R-14):\n  " + "\n  ".join(problems))
    print("valid: every data file meets its meta-rules" + ("" if args.no_replay else
                                                            ", and every generated file replays"))


if __name__ == "__main__":
    main()

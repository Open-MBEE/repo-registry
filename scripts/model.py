"""The model's tables, read once, for every controller script (WP5b; data/schema/model.yaml).

The repository's records are the model (MVC, WP5b). This module is the one place that knows where each table lives
and how its rows are keyed, so the scripts never re-derive a join. Read-only: nothing here writes.

Keys (WP5b OD2, OD3, F-05): a kind is keyed by (type, stage); its name "type/stage" is derived shorthand. A repository
is keyed by GitHub's numeric repository ID, a person by GitHub's numeric user ID.
"""
import json
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load(rel, root=ROOT):
    return yaml.safe_load((pathlib.Path(root) / rel).read_text())


def declared(root=ROOT):
    """The declared model (data/schema/model.yaml)."""
    return load("data/schema/model.yaml", root)


def snapshot_dir(root=ROOT):
    """The current snapshot, declared once (F-14)."""
    return pathlib.Path(root) / declared(root)["snapshot"]


def kind_name(type_, stage):
    """The derived shorthand for a kind (OD2)."""
    return f"{type_}/{stage}"


def kind_of(entry):
    """The kind name an entry names by its type and stage, or `unclassified` for an entry with only a reason."""
    if "type" in entry or "stage" in entry:
        return kind_name(entry.get("type"), entry.get("stage"))
    return "unclassified"


def kinds(kinds_doc):
    """The kind table flattened to {name: row}, each row with its type and stage (the composite key) added."""
    return {kind_name(t, s): {"type": t, "stage": s, **row}
            for t, by_stage in (kinds_doc.get("kinds") or {}).items() for s, row in by_stage.items()}


def omitted(kinds_doc):
    return {kind_name(t, s): reason for t, by_stage in (kinds_doc.get("omitted") or {}).items()
            for s, reason in by_stage.items()}


def repos(root=ROOT):
    """The source repository table: the snapshot's rows, keyed by repository ID (ids.json), plus any repository read
    after the snapshot (F-04), which has an ID and a name but no sensed columns."""
    snap = snapshot_dir(root)
    rows = {r["name"]: r for r in json.loads((snap / "repos.json").read_text())}
    forks = json.loads((snap / "forks.json").read_text())["forks"] if (snap / "forks.json").exists() else {}
    out = {}
    for i in json.loads((snap / "ids.json").read_text())["repos"]:
        row = dict(rows.get(i["name"], {"name": i["name"]}))
        row["repo_id"] = i["repo_id"]
        if i.get("after_snapshot"):
            row["after_snapshot"] = True
        f = forks.get(str(i["repo_id"]))
        if f and f.get("readable"):  # the fork read (WP5c D-3), joined by repository ID
            row["fork_ahead_by"] = f["ahead_by"]
            row["fork_mostly_models"] = f["files_changed"] > 0 and 2 * f["model_files_changed"] > f["files_changed"]
        out[i["repo_id"]] = row
    return out


def by_name(root=ROOT):
    """{name: repo_id}, for the scripts that start from a name (GitHub compares names without case)."""
    return {r["name"]: rid for rid, r in repos(root).items()}


# --- rows of every declared table (data/schema/model.yaml), for scripts/validate.py ------------------------------

def _policies(root):
    out = {}
    for path in sorted((pathlib.Path(root) / "data/policies").glob("*.yaml")):
        if not path.name.startswith("_"):
            out[path.stem] = yaml.safe_load(path.read_text())
    return out


def _one(doc, *cols):
    return [{c: doc.get(c) for c in cols if c in doc}] if doc else []


def _keyed(mapping, key, value_col=None):
    """Rows of a {key: row} or {key: value} mapping, with the key as a column."""
    out = []
    for k, v in (mapping or {}).items():
        out.append({key: k, **v} if isinstance(v, dict) and value_col is None else {key: k, value_col or "value": v})
    return out


def rows(table, root=ROOT):
    """The rows of one declared table, each a dict of its columns. Unknown table: KeyError."""
    root = pathlib.Path(root)
    kinds_doc = load("data/taxonomy/kinds.yaml", root)
    snap = snapshot_dir(root)
    src = lambda rel: load(f"data/sources/{rel}", root)  # noqa: E731
    if table == "repo":
        return list(repos(root).values())
    if table == "repo_usage":
        ids = by_name(root)
        return [{"repo_id": ids.get(n), "name": n, **u} for n, u in
                json.loads((snap / "usage.json").read_text())["repos"].items()]
    if table == "org_snapshot":
        return [json.loads((snap / "org.json").read_text())]
    if table == "cisa_practice":
        return _keyed(src("cisa-practices.yaml")["practices"], "practice_id")
    if table == "nist_control":
        return _keyed(src("nist-800-53.yaml")["controls"], "control_id")
    if table == "openssf_item":
        return _keyed(src("openssf-security-baseline.yaml")["items"], "item_id")
    if table == "iso_clause":
        return _keyed(src("iso12207-clauses.yaml")["clauses"], "clause")
    if table == "github_plan":
        return [src("github-plan.yaml")]
    if table in ("type", "stage"):
        return _keyed(kinds_doc[table + "s"], table, "meaning")
    if table == "tier":
        return _keyed(load("data/taxonomy/tiers.yaml", root)["tiers"], "tier")
    if table == "kind":
        return [{"type": t, "stage": s, **row} for t, m in kinds_doc["kinds"].items() for s, row in m.items()]
    if table == "omitted_kind":
        return [{"type": t, "stage": s, "reason": r} for t, m in (kinds_doc.get("omitted") or {}).items()
                for s, r in m.items()]
    if table == "signal":
        return _keyed(kinds_doc["signals"], "signal", "when")
    if table == "flag":
        return _keyed(kinds_doc.get("flags"), "flag")
    if table == "unclassified_reason":
        return [{"position": i, **r} for i, r in enumerate(kinds_doc.get("unclassified_reasons") or [])]
    if table == "registry_entry":
        return _keyed(load("registry.yaml", root)["repos"], "repo_id")
    if table == "org_entry":
        return [load("registry.yaml", root)["org"]]
    if table == "policy_set":
        return [load("data/policies/_set.yaml", root)]
    if table == "policy":
        return [{"policy_id": pid, **{k: v for k, v in p.items() if k not in ("id", "checks", "cites")}}
                for pid, p in _policies(root).items()]
    if table == "policy_check":
        return [{"policy_id": pid, "check_id": c.get("id"), "mode": mode, **{k: v for k, v in c.items() if k != "id"}}
                for pid, p in _policies(root).items() for mode in ("automated", "attested")
                for c in (p.get("checks") or {}).get(mode) or []]
    if table == "policy_cite":
        return [{"policy_id": pid, "source": source, "ref": str(ref)} for pid, p in _policies(root).items()
                for source, refs in (p.get("cites") or {}).items() if isinstance(refs, list) for ref in refs]
    if table == "departure":
        return [{"source": source, "ref": ref, "reason": reason}
                for source, m in load("data/policies/_departures.yaml", root).items() for ref, reason in m.items()]
    if table == "future_feature":
        return _keyed(load("data/policies/_future.yaml", root).get("features"), "feature")
    if table == "deviation":
        return load("data/deviations.yaml", root)["deviations"] or []
    if table == "maintainer":
        return [{"user_id": uid, **{k: v for k, v in m.items() if k != "release_authority"}}
                for uid, m in load("data/maintainers.yaml", root)["maintainers"].items()]
    if table == "release_authority":
        return [{"user_id": uid, **r} for uid, m in load("data/maintainers.yaml", root)["maintainers"].items()
                for r in m.get("release_authority") or []]
    if table == "maintainer_set":
        return _one(load("data/maintainers.yaml", root), "target_size", "other_powers")
    if table == "proposed_codeowner":
        import re
        text = (root / "data/proposed-codeowners").read_text()
        logins = sorted({m for line in text.splitlines() for m in re.findall(r"@([A-Za-z0-9-]+)(?!/)",
                                                                           line.split("#", 1)[0])})
        return [{"login": login} for login in logins]
    if table == "pilot_category":
        return [{"category": c.get("id"), **{k: v for k, v in c.items() if k != "id"}}
                for c in load("data/pilot-rule.yaml", root)["categories"]]
    if table == "pilot_named":
        rule = load("data/pilot-rule.yaml", root)
        return [{**r, "role": role} for role in ("must_include", "self_registered") for r in rule.get(role) or []]
    if table == "pilot_member":
        return [{**r, "category": None if r.get("category") == "must-include" else r.get("category")}
                for r in _keyed(load("data/pilot.yaml", root)["repos"], "repo_id")]
    if table == "excluded":
        return _keyed(load("data/exclude.yaml", root)["repos"], "repo_id")
    if table == "control":
        return _keyed(load("data/controls.yaml", root)["controls"], "control_id")
    if table == "forthcoming":
        return _keyed(load("data/forthcoming.yaml", root)["forthcoming"], "gap_id")
    if table == "measured_gap":
        return _keyed(load("data/measured-gaps.yaml", root)["measured"], "gap_id")
    raise KeyError(table)

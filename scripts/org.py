#!/usr/bin/env python3
"""Check that the named maintainers match the people with governance power over the org (WP0 R-15; WP3 D-4).

The rule checked: the named maintainers are exactly this repo's CODEOWNERS, and every org owner is a named
maintainer. Owners are a small subset of the maintainers (org-few-owners), so a maintainer needn't be an owner.

Deterministic, offline: it reads the stored org snapshot, data/maintainers.yaml and data/proposed-codeowners.
Privacy (WP3 OD1, R-8): it never reports the org role of anyone whose membership isn't public. Those rows are yellow,
"membership not public". It reports only the total count of owners with concealed membership, never "concealed owners
not on the list", because subtracting the listed people would reveal whether they are owners.

Usage: python3 scripts/org.py [--out build/demo]   (a view, rendered, never committed: WP5b OD4)

Maintainers are keyed by GitHub user ID (WP5b F-05); CODEOWNERS and the org snapshot name people by login, so they
join to the maintainers' `login` column. A check result is a `color` (WP5b F-11).
"""
import argparse
import json
import pathlib
import re
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model  # noqa: E402

RANK = {"green": 0, "yellow": 1, "red": 2}


def codeowners_logins(text):
    logins = set()
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            logins |= {m for m in re.findall(r"@([A-Za-z0-9-]+)(?!/)", line)}
    return logins


def check(snapshot, maint_doc, codeowners):
    listed = {e["login"]: uid for uid, e in maint_doc["maintainers"].items()}
    rows = []

    def row(subject, check_id, color, detail):
        rows.append({"subject": subject, "check": check_id, "color": color, "detail": detail})

    owners = snapshot["owners"]
    public_owners = set(owners["value"]["public_logins"]) if owners["readable"] else None
    for login in sorted(listed):
        row(login, "in-proposed-codeowners", "green" if login in codeowners else "red",
            "named in the proposed CODEOWNERS" if login in codeowners else "missing from the proposed CODEOWNERS")
        if not snapshot["listed_maintainers"].get(login, {}).get("membership_public"):
            row(login, "is-org-owner", "yellow", "membership not public, so the org role is not shown")
        elif public_owners is None:
            row(login, "is-org-owner", "yellow", "the owner list couldn't be read")
        else:
            # Owners are a small subset of the maintainers (org-few-owners: 2 or 3), so a maintainer who isn't an
            # owner is fine. What must hold is that every owner is a named maintainer (checked below).
            is_owner = login in public_owners
            row(login, "is-org-owner", "green",
                "an org owner" if is_owner else "a maintainer without the owner role (fine: owners are a subset)")
    for login in sorted(codeowners - set(listed)):
        row(login, "codeowner-is-listed", "red", "in the proposed CODEOWNERS but not a named maintainer")
    if public_owners is not None:
        for login in sorted(public_owners - set(listed)):
            row(login, "owner-is-listed", "red", "an org owner with public membership who isn't a named maintainer")
        concealed = owners["value"]["concealed_count"]
        row("org", "concealed-owners", "green" if concealed == 0 else "yellow",
            f"{concealed} org owners have concealed membership; whether they are named maintainers can't be shown")
    else:
        row("org", "owners-readable", "yellow", owners.get("reason", "owner list unreadable"))
    size, target = len(listed), maint_doc.get("target_size")
    if target:
        row("list", "target-size", "green" if size >= target else "yellow", f"{size} named of a target of {target}")
    overall = max((r["color"] for r in rows), key=RANK.get, default="green")
    return {"status": "provisional", "overall": overall, "rows": rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="build/demo")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = pathlib.Path(args.root)
    snapshot = json.loads((model.snapshot_dir(root) / "org.json").read_text())
    maint = model.load("data/maintainers.yaml", root)
    owners_file = codeowners_logins((root / "data/proposed-codeowners").read_text())
    result = check(snapshot, maint, owners_file)
    out = pathlib.Path(args.out) / "reports/maintainers-match.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(result, sort_keys=False, width=120))
    for r in result["rows"]:
        print(f"  {r['color']:6} {r['subject']:12} {r['check']:22} {r['detail']}")
    print(f"overall: {result['overall']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

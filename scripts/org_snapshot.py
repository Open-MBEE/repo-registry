#!/usr/bin/env python3
"""Take a read-only snapshot of how the Open-MBEE GitHub org is governed.

WP3 D-1. Only `gh` reads (WP3 R-1). Privacy (WP3 OD1, R-8): it never writes the login of a concealed org member.
Owners are stored as a count, plus the logins of owners whose membership is public. People listed in
data/maintainers.yaml are recorded with their public membership flag only, never their org role unless their
membership is public. Anything the credential can't read is stored as null, with the reason (yellow, not "off").

Usage: python3 scripts/org_snapshot.py [--org Open-MBEE] [--out data/snapshots] [--maintainers data/maintainers.yaml]
Writes <out>/<YYYY-MM-DD>/org.json.
"""
import argparse
import datetime as dt
import json
import pathlib
import subprocess

import yaml

ORG_FIELDS = (
    # GET /orgs/{org}. GitHub returns "full details" only to owners, so any of these may be missing (yellow).
    # The *_enabled_for_new_repositories fields are deprecated (replaced by security configurations) and not read.
    "two_factor_requirement_enabled", "default_repository_permission", "members_can_create_repositories",
    "members_can_create_public_repositories", "members_can_create_private_repositories",
    "members_can_fork_private_repositories", "members_can_change_repo_visibility", "members_can_delete_repositories",
    "members_can_invite_outside_collaborators", "members_can_create_teams", "web_commit_signoff_required",
)


def gh(path, paginate=False):
    """A read-only `gh api` GET. Returns (data, None) or (None, reason)."""
    args = ["gh", "api", "-X", "GET"] + (["--paginate", "--slurp"] if paginate else []) + [path]
    out = subprocess.run(args, capture_output=True, text=True)
    if out.returncode != 0:
        return None, (out.stdout or out.stderr).strip().splitlines()[0][:200]
    data = json.loads(out.stdout)
    if paginate:
        data = [item for page in data for item in page]
    return data, None


def unreadable(reason):
    return {"value": None, "readable": False, "reason": reason}


def readable(value):
    return {"value": value, "readable": True}


def last_public_activity(login, org):
    """Date of the user's latest commit in the org's public repos (a hint only, WP3 default)."""
    data, err = gh(f"search/commits?q=author:{login}+org:{org}&sort=committer-date&order=desc&per_page=1")
    if err or not data.get("items"):
        return None
    return data["items"][0]["commit"]["committer"]["date"][:10]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--org", default="Open-MBEE")
    ap.add_argument("--out", default="data/snapshots")
    ap.add_argument("--maintainers", default="data/maintainers.yaml")
    args = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    listed = yaml.safe_load(pathlib.Path(args.maintainers).read_text())["maintainers"]

    me, _ = gh("user")
    membership, _ = gh(f"user/memberships/orgs/{args.org}")
    org, err = gh(f"orgs/{args.org}")
    settings = {}
    for field in ORG_FIELDS:
        if err:
            settings[field] = unreadable(err)
        elif org.get(field) is None:
            settings[field] = unreadable("not returned to this credential (owner-only, or not set)")
        else:
            settings[field] = readable(org[field])

    public, perr = gh(f"orgs/{args.org}/public_members?per_page=100", paginate=True)
    public = sorted(m["login"] for m in public) if public is not None else None
    owners, oerr = gh(f"orgs/{args.org}/members?role=admin&per_page=100", paginate=True)
    if owners is not None and public is not None:
        owner_logins = {m["login"] for m in owners}
        owners_doc = readable({
            "count": len(owner_logins),
            "public_logins": sorted(owner_logins & set(public)),
            "concealed_count": len(owner_logins - set(public)),
        })
        del owner_logins  # never written: concealed logins stay in memory only
    else:
        owners_doc = unreadable(oerr or perr)

    def count_or_unreadable(path):
        data, e = gh(path, paginate=True)
        return readable(len(data)) if data is not None else unreadable(e)

    snapshot = {
        "org": args.org,
        "taken_at": now.isoformat(),
        "credential": {"login": (me or {}).get("login"), "org_role": (membership or {}).get("role")},
        "settings": settings,
        "owners": owners_doc,
        "public_members": readable(public) if public is not None else unreadable(perr),
        "outside_collaborators_count": count_or_unreadable(f"orgs/{args.org}/outside_collaborators?per_page=100"),
        "app_installations_count": count_or_unreadable(f"orgs/{args.org}/installations?per_page=100"),
        "teams_count": count_or_unreadable(f"orgs/{args.org}/teams?per_page=100"),
        # Who holds security manager, CI/CD admin, moderator and App Manager: the assignee lists need an owner.
        "organization_roles_count": count_or_unreadable(f"orgs/{args.org}/organization-roles"),
        "security_configurations_count": count_or_unreadable(f"orgs/{args.org}/code-security/configurations"),
        "org_rulesets_count": count_or_unreadable(f"orgs/{args.org}/rulesets"),
        "listed_maintainers": {
            login: {
                "membership_public": (public is not None and login in public),
                "last_public_commit_in_org": last_public_activity(login, args.org),
            }
            for login in sorted(listed)
        },
        "public_owner_activity": (
            {login: last_public_activity(login, args.org) for login in owners_doc["value"]["public_logins"]}
            if owners_doc["readable"] else None
        ),
        "tool": "scripts/org_snapshot.py (gh api GET only)",
    }
    outdir = pathlib.Path(args.out) / now.date().isoformat()
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "org.json").write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n")
    print(f"wrote {outdir / 'org.json'}")


if __name__ == "__main__":
    main()

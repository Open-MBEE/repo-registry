#!/usr/bin/env python3
"""Take a read-only inventory snapshot of the Open-MBEE org's public repos.

WP1 D-1. Uses only `gh` reads (WP1 R-1; WP0 R-8, R-9). Private repos are never
fetched by name: only their count is recorded (WP1 OD2).

Usage: python3 scripts/snapshot.py [--org Open-MBEE] [--out data/snapshots]
Writes <out>/<YYYY-MM-DD>/repos.json and <out>/<YYYY-MM-DD>/meta.json.
"""
import argparse
import datetime as dt
import json
import pathlib
import subprocess

PAGE = 25

REPO_FIELDS = """
  name
  description
  url
  homepageUrl
  isArchived
  isFork
  parent { nameWithOwner }
  createdAt
  pushedAt
  hasIssuesEnabled
  hasWikiEnabled
  stargazerCount
  forkCount
  licenseInfo { spdxId }
  primaryLanguage { name }
  languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { nodes { name } }
  repositoryTopics(first: 20) { nodes { topic { name } } }
  issues(states: OPEN) { totalCount }
  releases(first: 20, orderBy: {field: CREATED_AT, direction: DESC}) {
    totalCount
    nodes { tagName publishedAt isPrerelease isDraft }
  }
  tags: refs(refPrefix: "refs/tags/", first: 0) { totalCount }
  defaultBranchRef {
    name
    target {
      ... on Commit {
        committedDate
        last12: history(since: $since12) { totalCount }
        last3: history(since: $since3) { totalCount }
      }
    }
  }
  root: object(expression: "HEAD:") { ... on Tree { entries { name type } } }
  dotgithub: object(expression: "HEAD:.github") { ... on Tree { entries { name type } } }
  workflows: object(expression: "HEAD:.github/workflows") { ... on Tree { entries { name } } }
  docs: object(expression: "HEAD:docs") { ... on Tree { entries { name } } }
"""

QUERY = """
query($org: String!, $cursor: String, $since12: GitTimestamp!, $since3: GitTimestamp!) {
  organization(login: $org) {
    repositories(first: %d, after: $cursor, privacy: PUBLIC, orderBy: {field: NAME, direction: ASC}) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes { %s }
    }
  }
}
""" % (PAGE, REPO_FIELDS)

COUNT_QUERY = """
query($org: String!) {
  organization(login: $org) {
    all: repositories { totalCount }
    private: repositories(privacy: PRIVATE) { totalCount }
  }
}
"""


def gh_graphql(query, **variables):
    """Run a read-only GraphQL query through `gh api graphql`."""
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value is not None:
            args += ["-f", f"{key}={value}"]
    out = subprocess.run(args, check=True, capture_output=True, text=True).stdout
    data = json.loads(out)
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], indent=2))
    return data["data"]


def names(tree):
    return sorted(e["name"] for e in (tree or {}).get("entries", []))


def flatten(node):
    """Turn one GraphQL repo node into a flat, stable record."""
    branch = node.get("defaultBranchRef") or {}
    head = branch.get("target") or {}
    releases = node["releases"]["nodes"]
    return {
        "name": node["name"],
        "description": node["description"],
        "url": node["url"],
        "homepage": node["homepageUrl"] or None,
        "archived": node["isArchived"],
        "fork": node["isFork"],
        "parent": (node["parent"] or {}).get("nameWithOwner"),
        "created_at": node["createdAt"],
        "pushed_at": node["pushedAt"],
        "last_commit_at": head.get("committedDate"),
        "commits_last_12_months": (head.get("last12") or {}).get("totalCount"),
        "commits_last_3_months": (head.get("last3") or {}).get("totalCount"),
        "default_branch": branch.get("name"),
        "issues_enabled": node["hasIssuesEnabled"],
        "wiki_enabled": node["hasWikiEnabled"],
        "open_issues": node["issues"]["totalCount"],
        "stars": node["stargazerCount"],
        "forks": node["forkCount"],
        "license": (node["licenseInfo"] or {}).get("spdxId"),
        "primary_language": (node["primaryLanguage"] or {}).get("name"),
        "languages": [n["name"] for n in node["languages"]["nodes"]],
        "topics": sorted(n["topic"]["name"] for n in node["repositoryTopics"]["nodes"]),
        "release_count": node["releases"]["totalCount"],
        "releases": [
            {"tag": r["tagName"], "published_at": r["publishedAt"], "prerelease": r["isPrerelease"]}
            for r in releases
            if not r["isDraft"]
        ],
        "tag_count": node["tags"]["totalCount"],
        "root_files": names(node.get("root")),
        "dotgithub_files": names(node.get("dotgithub")),
        "workflow_files": names(node.get("workflows")),
        "docs_files": names(node.get("docs")),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--org", default="Open-MBEE")
    ap.add_argument("--out", default="data/snapshots")
    args = ap.parse_args()

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    since12 = (now - dt.timedelta(days=365)).isoformat()
    since3 = (now - dt.timedelta(days=91)).isoformat()

    repos, cursor = [], None
    while True:
        data = gh_graphql(QUERY, org=args.org, cursor=cursor, since12=since12, since3=since3)
        page = data["organization"]["repositories"]
        repos += [flatten(n) for n in page["nodes"]]
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    counts = gh_graphql(COUNT_QUERY, org=args.org)["organization"]
    meta = {
        "org": args.org,
        "taken_at": now.isoformat(),
        "window_12_months_since": since12,
        "window_3_months_since": since3,
        "public_repos": len(repos),
        "private_repos_count_only": counts["private"]["totalCount"],
        "all_repos_count": counts["all"]["totalCount"],
        "tool": "scripts/snapshot.py (gh api graphql, read-only)",
    }

    outdir = pathlib.Path(args.out) / now.date().isoformat()
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "repos.json").write_text(json.dumps(repos, indent=2, sort_keys=True) + "\n")
    (outdir / "meta.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(f"wrote {len(repos)} public repos to {outdir} ({meta['private_repos_count_only']} private, count only)")


if __name__ == "__main__":
    main()

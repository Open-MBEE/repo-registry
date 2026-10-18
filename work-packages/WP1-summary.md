# WP1 — Summary for the supervisor

> Everything here is **PROVISIONAL**. The kinds and tiers wait for maintainer approval 1 (the taxonomy). Each repo's
> kind waits for maintainer approval 4 (WP0). This summary meets WP1's Definition of good enough, last item.

Snapshot: `data/snapshots/2026-10-18`, with 181 public repos (3 private repos are counted only, never named). The
recommendations come from `python3 scripts/recommend.py --snapshot data/snapshots/2026-10-18`. The evidence for each
repo is in `data/reports/kind-recommendations.yaml`.

## Kinds, tiers and how many repos each would recommend

| Kind | Tier | Repos |
|---|---|---|
| tool/active-development | high | 1 |
| tool/maintained | high | 14 |
| tool/experimental | medium | 9 |
| tool/unreleased *(departure)* | low | 63 |
| tool/archived | none | 21 |
| media/active-development | medium | 11 |
| media/maintained | medium | 11 |
| media/experimental | low | 0 *(only a governor assigns it)* |
| media/archived | none | 0 |
| research/experimental | low | 6 |
| research/active-development | low | 0 *(only a governor assigns it)* |
| research/maintained | low | 0 *(only a governor assigns it)* |
| research/archived | none | 0 |
| unclassified | — | 45 |

By tier, that is 15 high, 31 medium, 69 low and 21 none, plus 45 unclassified.

## One departure from type × lifecycle

**tool/unreleased (low).** You said a tool can be in the low tier without semantic versioning, while medium and high
require it and 0.x tools are experimental (medium). The 12-kind cross product has no low-tier tool kind, so a tool
with no semver release had nowhere to land. This kind is that landing place. If you'd rather not add a lifecycle,
the alternative is to map tool/experimental to low, but that breaks "0.x stays medium".

## Unclassified repos, and why (45)

- **25 forks.** The taxonomy has no kind for forks yet (WP0 parked item). Forks are shown, not forced into a kind
  (TX-4). Examples: `fprime`, `helix`, `syson`, `opencode`, `winget-pkgs`.
- **14 live repos with no type signal.** They have no media or research words and no programming language:
  `apv-mdk`, `flexo-mms-ontology`, `flexo-pr-manager`, `flexo-sysmlv2-swagger`, `jl_scxml`, `md-cst-rabbitmq`,
  `mms-autocref`, `mms-migration`, `mms-rdf`, `starkit`, `structured-use-cases`, `sysmod-sysmlv2-api`, `trafo-v2-v1`,
  `websysml-core`. Several are notebooks or HTML-only, which the rules don't count as code.
- **6 archived repos with no type signal.** They are inert whatever their type: `amazonaws`, `ems-config`,
  `mathematica-mdk-core`, `mms-mathematica-client`, `mvn-repo`, `zzProjectWiki`.

## Things worth your attention

1. **Only one tool is in active development by the rules** (`mtip-cameo`, v1.0.9). The most active tool,
   `OpenSysML`, is at v0.10.1, so it is experimental (medium) until it reaches 1.0.0. That is your seam working as
   designed, but it means very little sits in high today apart from the 14 maintained tools.
2. **All 14 maintained tools had no commits in the last 12 months.** They include `exec-mms`, `exec-ve` and
   `exec-cameo-mdk`. The rule calls them maintained (high). Some may really be archive candidates.
3. **74 live repos are flagged as archive candidates** (no commits in 12 months). The flag never changes a kind, but
   it's a ready list for WP4's "repos that should be archived".
4. **`repo-registry` isn't in the snapshot,** because it isn't in the org yet (it moves in WP5). Its kind should map
   to high (WP1 Direction). Because it has no 1.0.0 release, the rules would recommend tool/unreleased (low), so its
   kind will need a governed assignment rather than the recommendation.
5. **Type rules lean on names and descriptions,** because almost no repo sets GitHub topics (26 distinct topics across the
   whole org). The word lists are data in `kinds.yaml`, so they're easy to tune. Adding topics to repos would make type
   detection much more reliable.

## Checks

`python3 -m unittest discover -s tests` runs 15 checks covering R-1 to R-10 and D-4 and D-5. All pass. Two checks
need a person: R-1's code review of `scripts/snapshot.py`, and R-4's cold read of the kind and tier meanings.

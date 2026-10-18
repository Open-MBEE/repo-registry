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
| tool/unreleased | low | 63 |
| tool/archived | none | 21 |
| media/active-development | medium | 11 |
| media/maintained | medium | 11 |
| media/experimental | low | 0 *(only the maintainers choose it)* |
| media/archived | none | 0 |
| research/experimental | low | 6 |
| research/active-development | low | 0 *(only the maintainers choose it)* |
| research/maintained | low | 0 *(only the maintainers choose it)* |
| research/archived | none | 0 |
| governance/experimental | high | 1 *(assigned: `repo-registry`, not yet in the org)* |
| governance/maintained | high | the org's own administration *(assigned; not a repo)* |
| unclassified | — | 45 |

By tier, that is 16 high (counting `repo-registry`), 31 medium, 69 low and 21 none, plus 45 unclassified.
The org's administration is governance/maintained (high).

Governance kinds are assigned by decision (`data/assignments.yaml`), never recommended, and only these two exist.
The other governance kinds, and `unreleased` for anything but tools, are listed under `omitted` in `kinds.yaml`,
each with its reason.

## One added lifecycle: unreleased

**tool/unreleased (low).** You said a tool can be in the low tier without semantic versioning, while medium and high
require it and 0.x tools are experimental (medium). The 12-kind cross product has no low-tier tool kind, so a tool
with no semver release had nowhere to land. This kind is that landing place. `unreleased` is now defined as a
lifecycle, for tools only. If you'd rather not add a lifecycle, the alternative is to map tool/experimental to low,
but that breaks "0.x stays medium".

## Unclassified repos, and why (45)

- **25 forks.** The taxonomy has no kind for forks yet (WP0 parked item). Forks are shown, not forced into a kind
  (TX-4). Examples: `fprime`, `helix`, `syson`, `opencode`, `winget-pkgs`.
- **14 live repos with no type signal.** They have no media or research words and no programming language, for
  example `structured-use-cases`, `sysmod-sysmlv2-api` and `mms-rdf`.
- **6 archived repos with no type signal.** They are inert whatever their type.

## Things worth your attention

1. **A kind is a category, not a compliance verdict.** The 14 tools at version 1.0 or later with no changes in a year
   are tool/maintained, because that is their stage. Whether anyone actually does the upkeep (tracking dependencies,
   fixing reported security flaws) is checked by the maintained-lifecycle policies in WP2, not by the kind. Until
   those policies exist, nothing can be out of compliance with them.
2. **Little is in active development by the rules:** only `mtip-cameo` (v1.0.9). `OpenSysML` and `sysml-toolkit`
   stay experimental (medium) until they release 1.0.0 (WP1 A3).
3. **Maintenance duties carried to WP2:** tracking dependencies and handling reported security flaws (CVEs), as
   policies attached to the maintained lifecycle.
4. **74 live repos are flagged as archive candidates** (no commits in 12 months). The flag is a hint for WP4 and never
   changes a kind.
5. **Type rules lean on names and descriptions,** because almost no repo sets GitHub topics (26 distinct topics across
   the whole org). The word lists are data in `kinds.yaml`, so they're easy to tune.

## Checks

`python3 -m unittest discover -s tests` runs 16 checks covering R-1 to R-10 and D-4 and D-5. All pass. Two checks
need a person: R-1's code review of `scripts/snapshot.py`, and R-4's cold read of the kind and tier meanings.

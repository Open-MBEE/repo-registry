# WP1 — Summary for the supervisor

> Everything here is **PROVISIONAL**. The kinds and tiers wait for maintainer approval 1 (the taxonomy). Each repo's
> kind waits for maintainer approval 4 (WP0). This summary meets WP1's Definition of good enough, last item.

Snapshot: `data/snapshots/2026-10-18`, with 181 public repos (3 private repos are counted only, never named). The
recommendations come from `python3 scripts/recommend.py --snapshot data/snapshots/2026-10-18`. The evidence for each
repo is in `data/reports/kind-recommendations.yaml`.

## The kinds

Kinds are **type × lifecycle stage**:
- Types: tool, media, research and governance.
- Stages: the CNCF and OpenSSF project lifecycle, Sandbox, Incubating, Graduated and Archived (amendment A4). The map
  from their documents, with sources, is [lifecycle-stage-map.md](../docs/lifecycle-stage-map.md).
- Tools move from Sandbox to Incubating when they release 1.0.0.
- Graduated is never recommended by rule. The maintainers assign it on evidence of adoption and governance.

| Kind | Tier | Repos |
|---|---|---|
| tool/sandbox | low | 72 |
| tool/incubating | medium | 15 |
| tool/graduated | high | 0 *(assigned only)* |
| tool/archived | none | 21 |
| media/sandbox | low | 0 *(assigned only)* |
| media/incubating | medium | 22 |
| media/graduated | medium | 0 *(assigned only)* |
| media/archived | none | 0 |
| research/sandbox | low | 6 |
| research/incubating | low | 0 *(assigned only)* |
| research/graduated | low | 0 *(assigned only)* |
| research/archived | none | 0 |
| governance/sandbox | high | 1 *(assigned: `repo-registry`, not yet in the org)* |
| governance/graduated | high | the org's own administration *(assigned; not a repo)* |
| unclassified | — | 45 |

By tier, that is 1 high (`repo-registry`), 37 medium, 78 low and 21 none, plus 45 unclassified. The org's
administration is governance/graduated (high). `governance/incubating` and `governance/archived` are listed under
`omitted` in `kinds.yaml`, with reasons.

## Unclassified repos, and why (45)

- **25 forks.** The taxonomy has no kind for forks yet (WP0 parked item). Forks are shown, not forced into a kind
  (TX-4). Examples: `fprime`, `helix`, `syson`, `opencode`, `winget-pkgs`.
- **14 live repos with no type signal.** They have no media or research words and no programming language, for
  example `structured-use-cases`, `sysmod-sysmlv2-api` and `mms-rdf`.
- **6 archived repos with no type signal.** They are inert whatever their type.

## Things worth your attention

1. **Nothing is in the high tier by rule, by design.** High is for graduated tools, and graduation needs evidence of
   wide use and governance, which the maintainers give. The 15 incubating tools (1.0 or later, for example
   `exec-mms`, `exec-ve`, `mtip-cameo`, `opl`) are the candidates for the maintainers to consider for graduation.
2. **OpenSysML and sysml-toolkit are in Sandbox (low)** while they're below 1.0. Their rapid development stays
   unblocked, and their controls rise when they release 1.0.0 (to Incubating, medium).
3. **A kind is a category, not a compliance verdict.** Whether a repo does the work its stage asks for, such as
   tracking dependencies and fixing reported security flaws, is checked by policies in WP2. The OpenSSF security
   baseline by stage is the precedent.
4. **74 live repos are flagged as archive candidates** (no commits in 12 months). The flag is a hint for WP4 and never
   changes a kind. It matches OpenSSF's use of dormancy as a reason to *consider* archiving.
5. **Type rules lean on names and descriptions,** because almost no repo sets GitHub topics (26 distinct topics across
   the whole org). The word lists are data in `kinds.yaml`, so they're easy to tune.

## Checks

`python3 -m unittest discover -s tests` runs 16 checks covering R-1 to R-10 and D-4 and D-5. All pass. Two checks
need a person: R-1's code review of `scripts/snapshot.py`, and R-4's cold read of the kind and stage meanings.

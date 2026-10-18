# WP1 — Review report

| | |
|---|---|
| **Scope of work** | [WP1-scope-of-work.md](WP1-scope-of-work.md) |
| **Scope approval verified** | Merge commit 3bb8ee8 "Approve WP1 scope of work" by Michael Zargham, parents 1dccb62 and db2864c (the scope branch `wp1-scope`) |
| **Work reviewed** | Branch `wp1-work`, commit 1fea4f4 (`git diff main...wp1-work`) |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `scripts/snapshot.py`; `data/snapshots/2026-10-18/repos.json` (181 public repos) and `meta.json` (`private_repos_count_only: 3`, `all_repos_count: 184`) |
| D-2 | met | `data/taxonomy/kinds.yaml`: 13 kinds, each with name, meaning, `recommend_when` rule and tier. It covers forks (as unclassified, with a reason) and archived repos. `repo-registry` itself: see G-2 |
| D-3 | met | `data/taxonomy/tiers.yaml`: high, medium, low, none, with WP0's meanings |
| D-4 | met | `docs/kind-list-format.md` (shape, 10 meta-rules, examples, a reclassification diff) and `data/schema/kind-list.schema.yaml` |
| D-5 | met | `registry.yaml`: 181 entries, first line `# PROVISIONAL. NOT APPROVED.`, `status: provisional`, `provisional_until: "WP0 maintainer approval 4: …"`. Test `test_D5_covers_every_snapshot_repo` passes |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | Independent code review in a fresh context: the only call out is `gh api graphql` (snapshot.py:82-86), with `query` operations only (snapshot.py:58-77), no other network library, `privacy: PUBLIC` on the listing (snapshot.py:61), and only `totalCount` kept for private repos (snapshot.py:74, 165). meta.json: 181 + 3 = 184. Tests `test_R1_read_only_gh` and `test_R1_private_repos_count_only` pass, and a grep of `scripts/*.py` finds no `mutation`, `POST`, `PATCH`, `DELETE` or `push` |
| R-2 | met | The engine was run twice on the stored snapshot. `cmp` shows both outputs identical to each other and to the committed `registry.yaml` and report. Test `test_R2_replay` passes |
| R-3 | met | 12 cross-product kinds plus 1 departure (`tool/unreleased`, with a `departure` reason). Test `test_R3_…` passes. Each meaning is one or two lines |
| R-4 | not met | Every kind and tier has a meaning (`test_R4_…`). A stand-in cold read in a fresh context (not a real non-specialist) flagged jargon and notation: "seam" and "0.x"/"1.0.0" (kinds.yaml:24, 67, 74, 81), "inert" (tiers.yaml:24; kinds.yaml:99, 128, 156), "Terminal state" (kinds.yaml:27), "Load-bearing media" and "ancillary" (tiers.yaml:15), "single committer" (kinds.yaml:21, 137), "governor" and "rules" undefined (kinds.yaml:122, 144, 150), "(carried to WP2)" (tiers.yaml:11, 16). The lifecycle `unreleased` is used by `tool/unreleased` but not defined under `lifecycles` (kinds.yaml:23-27, 85). And `tool/maintained` doesn't say why it is high |
| R-5 | met | No repo matches more than one kind (`test_R5_rules_are_exclusive_on_the_snapshot`). An overlap is reported as unclassified (`test_R5_overlap_is_reported_not_hidden`). 45 unclassified, each with a reason |
| R-6 | met, except one part (G-2) | Map: tool/active-development and tool/maintained → high, every archived kind → none, all others → low or medium, every tier used (`test_R6_…`, `check_taxonomy`). No registry entry names a tier (`grep -c "tier:" registry.yaml` → 0). Not checkable: "`repo-registry`'s kind maps to high", because no data names repo-registry's kind (G-2) |
| R-7 | met | `test_R7_toy_taxonomy_swap_needs_no_code_change`: a toy taxonomy runs unchanged, and no kind, type or tier name appears quoted in `recommend.py` |
| R-8 | met | `test_R8_reclassification_is_one_entry`: the diff is exactly one removed line and one added line. The meta-rules in `docs/kind-list-format.md` are stated as checkable statements |
| R-9 | met | `test_R9_release_maturity_rule`: OpenSysML v0.10.1 → tool/experimental, mtip-cameo v1.0.9 → tool/active-development, exec-mms 4.0.20 → tool/maintained, flexo-cli-client (no semver) → tool/unreleased (low), EMS-Repo → tool/archived. `test_R9_semver_parsing` passes |
| R-10 | met | `test_R10_provisional_mark` passes. Meta-rule 3 in the format doc covers the mark |

Full run: `python3 -m unittest discover -s tests` → `Ran 15 tests … OK`.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| Snapshot exists with its script, and replays | met | D-1, R-1, R-2 |
| Kinds and tiers exist as data; every requirement passes its check | not met | R-4 not met (G-3); R-6 partly not checkable (G-2) |
| Kind list format exists with meta-rules and examples | met | D-4 |
| Provisional kind list covers every snapshot repo and is marked provisional | met | D-5, R-10 |
| Summary for the supervisor | met | [WP1-summary.md](WP1-summary.md) |

## Outside the scope

- **Out-of-scope changes:** `data/reports/kind-recommendations.yaml` (the evidence report behind each recommendation)
  and `tests/` (the checks, with toy fixtures) aren't named deliverables. Both support D-5 and the requirement checks.
- **Non-goals touched:** `data/taxonomy/tiers.yaml` says "Semantic versioning is required (carried to WP2)" for high
  and medium. The non-goal says tiers here say what they mean, not which policies apply (G-1).

## Observations (not counted as failures)

- If the `gh` token can't see private repos, the private count would silently read 0. Nothing records that the count
  depends on the token (independent reviewer).
- 45 of 181 repos (25%) are unclassified: 25 forks, 14 live repos with no type signal, and 6 archived repos with no
  type signal.
- Type rules lean on name and description words, because almost no repo sets topics.
- Only 1 tool is in active development by the rules. All 14 maintained tools have had no commits in 12 months.

## Open decisions (for the supervisor)

- **G-1.** tiers.yaml names a policy (semantic versioning), which touches the "no policies" non-goal.
- **G-2.** No data names `repo-registry`'s own kind, so "its kind maps to high" (R-6) can't be checked.
- **G-3.** R-4 not met: the kind and tier meanings use jargon and notation, the `unreleased` lifecycle isn't defined, and the cold read was by a stand-in, not a person.
- **G-4.** The other observations and out-of-scope files, as one item.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 | fix before acceptance | Remove the policy statement from tiers.yaml. Semantic versioning applies only to tools, which led to the amendment below |
| G-2 | fix before acceptance | Add a governance type (repo-registry: governance/experimental; the org's administration: governance/maintained; every governance kind maps to high). Needs the amendment |
| G-3 | fix before acceptance | Rewrite the kind and tier meanings in plain words, and define the `unreleased` lifecycle |
| G-4 | accept as is | The extra files support the checks. The unclassified share, the word-based type rules and the activity findings feed WP4. The private-count footnote is minor |

**Amendment needed first.** The supervisor decided that policies can attach to a type, a lifecycle or a tier, and that
there is a governance type. Both change the approved WP0 and WP1 scopes, so they go through an amendment approved by a
new merge. Then the fixes are made on `wp1-work`, and this whole review is rerun from step 1.

## Second pass (after the fixes)

Rerun from step 1 on `wp1-work` at 3f2e405. The WP1 scope approval (3bb8ee8) and amendment 1 (3c72b7d) are both
mzargham's merges.

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-5 | met | All present. `registry.yaml` now has the `org` block (governance/maintained) and the `repo-registry` entry (governance/experimental), drawn from `data/assignments.yaml` |
| R-1 | met | Fresh-context re-check: imports are argparse, datetime, json, pathlib and subprocess only (snapshot.py:10-14), with one `gh api graphql` call (:82-86), `query` operations only, `privacy: PUBLIC` (:61), and only the private `totalCount` (:74, :165) |
| R-2 | met | Two runs are identical to each other and to the committed `registry.yaml` and report (`cmp`) |
| R-3 | met | 15 kinds over 4 types × 5 lifecycles. The 5 others are under `omitted`, each with a reason. `test_R3_…` passes |
| R-4 | not met | Fresh-context stand-in cold read: (1) internal codes "(WP1 A2)" in the `omitted` reasons (kinds.yaml:207-208); (2) "governor" is undefined where readers see it (kinds.yaml:146, 170, 177); (3) "this repository" doesn't say which (kinds.yaml:26, 193); (4) "tools that … play a supporting role" (tiers.yaml:16-17), though no kind covers it; (5) maintained says "few recent changes" (kinds.yaml:36), but the maintained kinds say "no changes in the last year" (:91, :139). Every lifecycle used is defined, and each high-tier kind says why it is high |
| R-5 to R-10 | met | 16 tests pass (`python3 -m unittest discover -s tests`). No registry entry names a tier (`grep -c "tier:" registry.yaml` → 0) |
| G-1 fix | met | `tiers.yaml` names no policy. Its only mention, in a comment, says that policies are decided by their own rules |
| G-2 fix | met | `test_R6_governance_assignments` passes |
| Good enough | not met | R-4 |
| Outside the scope | — | New `data/assignments.yaml` (assigned kinds, each citing its decision). It supports D-5 and the G-2 fix |

**Gaps after the second pass:** G-3 is still not met (the R-4 items above). New observation: `data/assignments.yaml`
isn't a named deliverable.

## Third pass (after the second fixes, d667e92)

Mechanical checks: 16 tests pass, the replay is identical (`cmp`), and `tiers.yaml` names no policy. R-4: a fresh
stand-in cold read still reports issues. Items it says need fixing:

1. "the main tools that people depend on" (tiers.yaml:11): no kind says "main".
2. Maintained means "no changes in the last year" (kinds.yaml:37), yet the org's administration, which changes all the
   time, is governance/maintained (kinds.yaml:202). This contradiction came in with the second-pass fix.
3. Tier and lifecycle texts say "repositories" (tiers.yaml:25; kinds.yaml:42), but the org's administration isn't a
   repository (kinds.yaml:28, 202).
4. "Only the OpenMBEE maintainers give a repository this kind" (kinds.yaml:147, 171, 178) implies other kinds come some
   other way, and "OpenMBEE" is never defined.
5. "A tool moves on to active development when it releases version 1.0" (kinds.yaml:32-33, 101-102), but a 1.0 tool
   with no changes in a year is maintained (kinds.yaml:92).

It calls two items minor: the version numbers as notation (tiers.yaml:17; kinds.yaml:32, 39), and "controls" never
explained (tiers.yaml:11, 16, 21, 25).

Each fresh stand-in pass finds a new, smaller layer, so R-4's stopping point was taken to the supervisor a level up.

## Final pass (7b33da9)

The supervisor set R-4's stopping point: "Fix 1-5, then stop". So the third pass's five items were checked directly,
not by another stand-in read. During the fixes, the supervisor also refined three design points, each recorded in
[WP1-decisions.md](WP1-decisions.md): maintenance is active, a kind is a category and not a compliance verdict, and
active development means new features (read from feature releases, x.y.0).

| Item | Verdict | Evidence |
|---|---|---|
| R-4 third-pass items 1-5 | met | A regex scan of every reader-facing text finds no "main tools", "Only the OpenMBEE maintainers give", "moves on to active development when", "WP"/"OD" codes, "governor" or "this repository". The governance type now says the org's administration isn't a repository. "Maintained" no longer means "no changes" |
| R-4 minor items | accepted | Version numbers, each with a plain example, and "controls" (supervisor: "Fix 1-5, then stop") |
| R-1 to R-10, D-1 to D-5 | met | `python3 -m unittest discover -s tests` → 17 tests OK. Replay identical (`cmp`). No registry entry names a tier |
| Good enough | met | Every item above. Summary refreshed ([WP1-summary.md](WP1-summary.md)) |
| Outside the scope | — | `data/assignments.yaml` (supports D-5 and the G-2 fix). Accepted with G-4's out-of-scope files |
| Non-goals | not touched | No policies defined (semantic versioning, dependency and CVE upkeep are carried to WP2), nothing written outside this repo, no language model |

## Recommendation

**Recommend acceptance with the listed gaps noted.** Every deliverable, requirement and good-enough item is met after
the fixes. G-1, G-2 and G-3 were fixed. G-4 and the minor R-4 items are accepted as is, by the supervisor's decisions.
The taxonomy and kind list stay PROVISIONAL until the maintainers approve them (WP0 approvals 1 and 4).

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

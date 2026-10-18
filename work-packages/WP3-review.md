# WP3 — Review report

| | |
|---|---|
| **Scope of work** | [WP3-scope-of-work.md](WP3-scope-of-work.md) |
| **Scope approval verified** | Merge commit fd42204 "Approve WP3 scope of work" by Michael Zargham, parents 72a391b and 118f93c (`wp3-scope`) |
| **Work reviewed** | Branch `wp3-work`, commit 3895f77 (`git diff main...wp3-work`: 27 files) |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `docs/org-governance-review.md`: a snapshot section, plus tables from GitHub's documentation (A: org roles; B: repository power, teams, team maintainers, outside collaborators; C: apps and tokens; D: settings and the audit log; E: membership visibility). `data/snapshots/2026-10-18/org.json` from `scripts/org_snapshot.py` |
| D-2 | met | Five policies in `data/policies/` (org-two-factor, org-few-owners, org-base-permission, maintainers-match, governance-roles-named), each with an SOP, applying only to governance/graduated |
| D-3 | met | `data/maintainers.yaml` (aftimg, mzargham, rkarban, HuiJun; target 5; provenance stated) and `data/proposed-codeowners` (not live) |
| D-4 | met | `scripts/org.py` and `data/reports/maintainers-match.yaml` (overall red, rows explained in the summary) |
| D-5 | met | `docs/maintainer-policy.md`, ending with the cross-check against OpenSSF, CNCF, CISA, NIST and ISO clauses |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | Both scripts make only `GET` requests (`test_R1_snapshot_only_reads`; grep) |
| R-2 | met | 46 of 47 table rows in D-1 cite a docs page. The one exception, the PAT-policy row, refers to section C, which carries the citations. 21 items are marked UNCONFIRMED rather than filled in |
| R-3 | met | `python3 scripts/policies.py` passes. `test_R3_org_policies_pass_meta_rules_and_adopt_SB2` |
| R-4 | met | `test_R4_check_replays` |
| R-5 | met | `test_R5_unreadable_is_yellow_not_off`. Unreadable settings are stored with their reason |
| R-6 | met | `test_R6_provisional` |
| R-7 | not met | Advisory stand-in cold read (G-1) |
| R-8 | met | Three tests, including indistinguishability (`test_R8_check_reveals_nothing_about_concealed_roles`). Live: `scripts/privacy_check.py` reports 71 concealed members and 0 files naming one. The stand-in also found no privacy problem |

All tests: `python3 -m unittest discover -s tests` → 40, OK (2 expected failures).

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-5 exist, and every requirement passes | not met | R-7 (G-1) |
| The match check has run on the snapshot, and the result is in the summary | met | [WP3-summary.md](WP3-summary.md) |
| Summary for the supervisor | met | [WP3-summary.md](WP3-summary.md) |

## Outside the scope

- **Out-of-scope changes:**
  - `scripts/privacy_check.py`, a live privacy scan that supports R-8;
  - seven NIST controls added to `data/sources/nist-800-53.yaml`;
  - the SB-2 row of WP2's `policy-basis-review.md`, updated because SB-2 is now adopted.
- **Non-goals touched:** none. Nothing was written to the org, no credential was set up, and the CODEOWNERS is proposed,
  not live.

## Gaps

- **G-1 (R-7 not met).** The stand-in cold read found five problems.
  1. `org-base-permission`'s steps are in the wrong order. Lowering the base permission before granting team access
     would cut people off.
  2. `org-two-factor` says "warn them first" without saying how to find who lacks two-factor authentication.
  3. `maintainers-match` says "record the attestation" without saying where or how.
  4. Internal shorthand that a reader must act on: "R3", "WP0", "XF-1", and an unexplained "security manager role".
  5. The maintainer policy says every maintainer makes their membership public, but `governance-roles-named` checks
     only owners.
- **G-2 (the agent's reading of the scope).** Owners are a subset of the maintainers. Every owner must be a named
  maintainer, but a maintainer needn't be an owner. This is how OpenSSF's 2 to 3 owners and the target of 5 maintainers
  both hold. The match check and the maintainer policy depend on it.
- **G-3 (observations, one item).**
  - The out-of-scope files listed above.
  - The snapshot leaves out GitHub's deprecated `*_enabled_for_new_repositories` fields.
  - Several governance features are Enterprise Cloud only, so they can't apply to Open-MBEE: the audit-log API, SSO,
    custom roles, and owner-only outside-collaborator invites.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 (R-7, five plain-language items) | fix before acceptance | Supervisor: "Fix all five". Fixed and checked (below) |
| G-2 (owners are a subset of the maintainers) | accept the reading, and fix | Supervisor confirmed: owners are the root authority, 2 to 3 of them; maintainers can be more; owners check the maintainers' powers. The maintainer policy now says so |
| G-3 (observations) | accept as is, plus a new rule | Supervisor: "accept as is but don't make policies that require the use of features openmbee cannot use". Then: "we need immutable releases and rulesets so let's keep those in our policies but flag a need for further research". Implemented as checkable meta-rules (below). This applies to WP2's policies too |

## Final check after the fixes

| Item | Verdict | Evidence |
|---|---|---|
| G-1.1 base-permission order | met | Team access first (step 1), then lower the base permission (steps 2 and 3) |
| G-1.2 two-factor: who lacks it | met | The SOP says how to filter the People and Outside collaborators pages by 2FA, how members turn it on, and what GitHub does to each group |
| G-1.3 how to attest | met | Declared under `other_powers` in `data/maintainers.yaml`, by a pull request an owner merges. The key exists |
| G-1.4 shorthand | met | No "R3", "WP0" or "XF-1" in reader-facing text. The security manager role is explained and linked |
| G-1.5 every maintainer public | met | `governance-roles-named` now also checks every named maintainer's membership (`maintainers-public`) |
| G-2 owners check maintainers | met | The maintainer policy says an owner approves adding a maintainer or changing their powers, the owners run the annual review, and five is a starting point |
| G-3 plan rule | met | OpenMBEE is on GitHub Free (`data/sources/github-plan.yaml`). Every policy declares `available_on`, including `free` (meta-rule). Immutable releases and rulesets are kept and flagged under `github.needs_research`, with questions in `_future.yaml` (meta-rule). Enterprise-only features (audit-log API, SSO, custom roles, org rulesets, owner-only invites) are under `features`, and no policy requires them (`PlanTests`) |
| Privacy | met | `scripts/privacy_check.py`: 71 concealed members, 0 files naming one |
| All tests | met | 43 tests, OK (2 expected failures) |

## Recommendation

**Recommend acceptance with the listed gaps noted.** Every deliverable, requirement and good-enough item is met after
the fixes. Two features (immutable releases, rulesets) are kept in the policies, flagged for research on plan
availability. Everything stays PROVISIONAL until the maintainers approve it (WP0 approvals 2 and 5).

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

# WP2 — Review report

| | |
|---|---|
| **Scope of work** | [WP2-scope-of-work.md](WP2-scope-of-work.md) |
| **Scope approval verified** | Merge commit 92cbe58 "Approve WP2 scope of work" by Michael Zargham, parents f1d4af5 and f526d50 (`wp2-scope`) |
| **Work reviewed** | Branch `wp2-work`, commit f3cfcfe (`git diff main...wp2-work`: 47 files) |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `docs/policy-basis-review.md`: sources with pinned commits; GitHub read tiers and the 404 hazard; the proposed set; trace tables for all 25 OpenSSF items, all 56 CISA practices, the NIST controls cited, the ISO clauses, and the CNCF cross-check |
| D-2 | met | `data/policies/` holds 15 policies, all `status: provisional`, plus `_departures.yaml` |
| D-3 | met | `docs/sops/` holds 15 SOPs with the three sections, and a shared README attestation block |
| D-4 | met | `docs/policy-format.md` (11 meta-rules), enforced by `scripts/policies.py` |
| D-5 | met | `docs/policy-applicability.md` and `data/reports/policy-applicability.yaml`: 14 kinds × 15 policies |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | Meta-rule 5 holds for all 15 (`test_D4_meta_rules_hold_on_the_policies`) |
| R-2 | met | Meta-rule 4. `test_R2_…` shows that other attributes and signals are rejected |
| R-3 | met | Core citations come from `data/sources/`, and unknown IDs are rejected (`test_R3_…`). Secondary citations appear where they apply |
| R-4 | met | `test_R4_sop_sections_required` |
| R-5 | not met | Advisory stand-in cold read, by a fresh agent and not a person (G-1, below) |
| R-6 | met | All 56 CISA practices are cited or departed with a reason (meta-rule 9). No automated check is duplicated (`test_R6_…`) |
| R-7 | met | Sandbox kinds carry 2 policies, incubating tools 10, graduated 14, archived 1, research 2 or fewer (`test_R7_…`) |
| R-8 | met | Every automated check names its `reads` and `permission` (`test_R8_…`) |
| R-9 | met | Generated twice, identical, and equal to the committed outputs (`test_R9_…`; `cmp`) |
| R-10 | met | A toy policy set runs with zero code change (`test_R10_…`) |
| R-11 | met | `test_R11_provisional` |
| R-12 | met | ISO citations are clause numbers only. Three distinctive passages are absent from the repo, tracked or untracked (`test_R12_…`) |
| R-13 | met | 16 baseline items adopted and 9 departed with reasons, never both. Removing a departure is caught (`test_R13_…`) |

Full run: `python3 -m unittest discover -s tests` → 28 tests OK.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-5 exist, and every requirement passes | not met | R-5 (G-1) |
| The set includes semantic versioning for tools, maintenance duties and the archive policy | met | `semantic-versioning`; `dependency-management` and `vulnerability-remediation`; `archive-notice` |
| Summary for the supervisor | met | [WP2-summary.md](WP2-summary.md) |

## Outside the scope

- **Out-of-scope changes:** `data/sources/` (the CISA, NIST and OpenSSF citation data). It isn't a named deliverable,
  but it supports D-1 and the R-3, R-6 and R-13 checks.
- **Non-goals touched:** none. No compliance checking runs against real repos (`policies.py` only resolves which
  policies apply), no org policy is written, no CI is added, nothing writes to GitHub, and no ISO text is committed.

## Gaps

- **G-1 (R-5 not met).** The stand-in cold read found six significant problems:
  1. SOPs say who they apply to in terms an owner can't look up ("High-tier repositories", "Graduated tools", "Tools
     from version 1.0"). They don't link to what those mean.
  2. `history-protection.md` asks for more than its policy: "Don't squash or rewrite the published history", which
     is also unclear about squash-merging pull requests.
  3. `archive-notice.md` can't be done as written. It says to archive first, but the attestation is a later README
     commit, and an archived repository is read-only.
  4. `release-integrity.md` suggests GitHub artifact attestations, but the attested check asks for "SLSA Build
     Level 3", which isn't explained and may not be what that method gives.
  5. `workflow-least-privilege.md`'s attested check uses jargon ("untrusted input in run steps", "privileged
     triggers"), and doesn't link the hardening guide it cites.
  6. Undefined terms an owner must act on: "pin its direct dependencies", "security controls", "backported",
     "release workflow" and "CI".
- **G-2 (observations, one item).**
  - `data/sources/` is outside the named deliverables.
  - The 14-day deadline for "promptly" is my choice.
  - `repo-registry` will be red on `change-review` until R3.
  - The checker needs *Administration: read*.
  - The R-12 check probes only three passages.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 (R-5, six SOP problems) | fix before acceptance | Supervisor: "Fix all six". Fixed, then checked on just these items (below) |
| G-2 (a) `data/sources/` outside the deliverables | accept as is | Supervisor: "Accept a and b" |
| G-2 (b) 14-day deadline for critical fixes | accept as is | Supervisor: "Accept a and b" |
| G-2 (c) repo-registry red on change-review until R3 | explicit expected failure | Supervisor: "we can tolerate explicit xfail for work forthcoming in later WPs". Recorded as XF-2 in `data/expected-gaps.yaml`, with an expected-failure test |
| G-2 (d) checker needs *Administration: read* | explicit expected failure | As (c). Recorded as XF-1, closing in WP6 |
| G-2 (e) ISO probe too thin | fix before acceptance | Supervisor: "you should probe the ISO-text more thoroughly". R-12 now checks every 8-word passage (below) |

## Final check after the fixes

| Item | Verdict | Evidence |
|---|---|---|
| G-1.1 who an SOP applies to | met | All 15 SOPs now have an "Applies to" line, generated from the applicability report and linking `registry.yaml`, the stage map and the table |
| G-1.2 history over-reach | met | "Don't squash" is gone. The SOP now says that squash-merging is fine and only rewriting or deleting the default branch is blocked |
| G-1.3 archive order | met | The README note and attestation are committed first, then the repository is archived (steps 1 to 3) |
| G-1.4 SLSA | met | SLSA is defined. The setup now names how to reach Build Level 3 (artifact attestations through a reusable workflow on GitHub-hosted runners), and the attested statement matches it, in the data and the SOP |
| G-1.5 workflow jargon | met | The attested statement is in plain words, and the hardening guide is linked |
| G-1.6 undefined terms | met | Pin, security controls, backport, CI and SBOM are each defined where they are used |
| Data and SOPs agree | met | Every attested statement in `data/policies/` appears word for word in its SOP |
| G-2 (c), (d) | met | `tests/test_forthcoming.py`: 2 expected failures, each tied to an entry in `data/expected-gaps.yaml` that says where it closes |
| G-2 (e) | met | `test_R12_iso_text_not_committed` hashes every 8-word sequence of every tracked or untracked text file. It checks them against 69,019 hashed 8-word sequences of the standard (a fixture with no text), and finds no match |
| All tests | met | `python3 -m unittest discover -s tests` → 31 tests, OK (2 expected failures) |

## Recommendation

**Recommend acceptance with the listed gaps noted.** Every deliverable, requirement and good-enough item is met after
the fixes. G-2 (a) and (b) are accepted as is. G-2 (c) and (d) are explicit expected failures, closing in R3 and WP6.
The policies stay PROVISIONAL until the maintainers approve them (WP0, maintainer approval 2).

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

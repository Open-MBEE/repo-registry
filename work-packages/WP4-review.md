# WP4 — Review report

| | |
|---|---|
| **Scope of work** | [WP4-scope-of-work.md](WP4-scope-of-work.md) |
| **Scope approval verified** | Merge commit aacff77 "Approve WP4 scope of work" by Michael Zargham, parents c0931c3 and 386aa28 (`wp4-scope`) |
| **Work reviewed** | Branch `wp4-work`, commit e3e69e9 |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met, with errors (G-2) | `docs/fit-analysis.md`: coverage, unclassified by reason, spot-checked misfires, archive candidates, five recommendations |
| D-2 | met | `data/pilot-rule.yaml` (categories, quotas, usage weights, must-includes) and `scripts/pilot.py` |
| D-3 | met | `data/pilot.yaml` (33) and `data/exclude.yaml` (149, each with a reason) |
| D-4 | met, with gaps (G-1, G-3) | `docs/pilot-briefing.md` from `scripts/briefing.py` |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `test_R1_usage_snapshot_only_reads`; the selection reads stored data only |
| R-2 | met | `test_R2_selection_and_briefing_replay` |
| R-3 | met | 33, every category, must-includes present (`test_R3_…`) |
| R-4 | met | Partition of the registry, reasons, no private repo (`test_R4_…`) |
| R-5 | met | Every pilot repo has a kind; only the forks category is unclassified, on purpose (`test_R5_…`) |
| R-6 | met | `test_R6_provisional` |
| R-7 | not met | Advisory stand-in read (G-1, G-2, G-3) |

All tests pass (2 expected failures). The privacy scan is clean.

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-4 exist, and every requirement passes | not met | R-7 |
| Summary for the supervisor | met | [WP4-summary.md](WP4-summary.md) |

## Outside the scope

- **Out-of-scope changes:** `scripts/usage_snapshot.py` and `data/snapshots/2026-10-18/usage.json` (the use signals
  D-2 needs). `scripts/briefing.py` generates D-4.
- **Non-goals touched:** none.

## Gaps

- **G-1 (plain language, R-7).**
  - The briefing never explains stages, tiers or which policies a kind carries. It shows only a count, with no link.
  - `policy-basis-review.md` still says sandbox kinds carry 2 policies and incubating tools 10. That went stale when
    WP2a added `license-by-type` (now 3 and 11).
- **G-2 (factual errors).**
  - The fit analysis says the pilot carries six archive candidates. It carries 13: the 6 should-be-archived, plus the
    five `exec-*` tools, `mcf`, and `flexo-sysml2-adapter-experiment`.
  - "Heavily used" over-claims. The quota forced in `mcf` (0 downloads, unreadable clones, no commits since 2021), and
    "consider graduating heavily used tools" points at dormant repositories.
  - The research section says "most active first", but it is sorted by use.
- **G-3 (representativeness).** OpenSysML, by far the most used tool, is sandbox and low, while dormant `exec-*` tools
  are medium. That is by design (A4: below 1.0 stays sandbox), but the briefing doesn't say so.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 plain language | fix before acceptance | Supervisor: "Fix as proposed" |
| G-2 factual errors | fix before acceptance | Supervisor: "Fix as proposed" |
| G-3 OpenSysML explanation | fix before acceptance | Supervisor: "Fix as proposed" (with G-1) |

## Final check after the fixes

| Item | Verdict | Evidence |
|---|---|---|
| G-1 "how to read this" | met | The briefing defines kind (type and stage), the four stages, the four tiers and policies, and links the stage map and the policy table |
| G-1 policies by name | met | Each pilot row lists its policies by name, linked to the SOPs (30 rows with `license-by-type`) |
| G-1 stale counts | met | `policy-basis-review.md` now says sandbox kinds carry 3 policies, incubating tools 11, graduated 15, media 3 or 4, research 3 |
| G-2 archive count | met | The fit analysis says 12 pilot repositories have had no changes in a year (6 chosen as should-be-archived, 6 for other reasons) and names them. The count changed from 13 because the fix moved `mcf` and dropped `bae2_3_1` |
| G-2 heavily used | met | A use threshold (at least 100 release downloads or 20 clone visitors in 14 days) leaves the sixth slot empty. `mcf` is now in should-be-archived. The briefing no longer suggests graduating dormant tools: it calls them a maintenance decision first |
| G-2 ranking wording | met | Every category says "ranked by use". "Most active first" is gone |
| G-3 OpenSysML | met | "Why OpenSysML is sandbox and low": below 1.0, amendment A4, and what changes at 1.0 (incubating, medium, 11 policies) |
| Tests and privacy | met | All tests pass (2 expected failures); the pilot, exclude list and briefing replay exactly; privacy scan clean |

## Recommendation

**Recommend acceptance.** Every deliverable, requirement and good-enough item is met after the fixes. The pilot is 32
repositories, and everything stays PROVISIONAL until the maintainers approve the pilot and the kinds (WP0 approvals 3
and 4).

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

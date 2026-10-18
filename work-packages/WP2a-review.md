# WP2a — Review report

| | |
|---|---|
| **Scope of work** | [WP2a-scope-of-work.md](WP2a-scope-of-work.md) |
| **Scope approval verified** | Merge commit d1dfa2f "Approve WP2a scope of work" by Michael Zargham, parents d25c7db and 9f5bf6d (`wp2a-scope`) |
| **Work reviewed** | Branch `wp2a-work`, commit 2f3b63e |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | "License basis (WP2a)" in `docs/policy-basis-review.md`: the allowed sets with their grounding (OpenSSF charter clause, CISA p. 16), NumFOCUS researched first with no conflict, exceptions, forks, and today's counts |
| D-2 | met | `data/policies/license-by-type.yaml` with `allowed_licenses` per type, and its SOP. `project-files` trimmed to the README |
| D-3 | met | `data/deviations.yaml` (empty, provisional). The report honours it (`test_R4_…`) |
| D-4 | met | `scripts/licenses.py` and `data/reports/license-report.yaml` (115 live, classified repos: 77 green, 38 red). Regenerated applicability table |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | Meta-rules pass, including the plan rule (`test_R1_…`; `python3 scripts/policies.py`) |
| R-2 | met | `test_R2_…`: allowed is green; missing, NOASSERTION and off-list are red; the sets are per type |
| R-3 | met | `test_R3_…`: the sets are keyed by type, and every type has one |
| R-4 | met | `test_R4_…`: an exception is green, marked "accepted exception" |
| R-5 | met | `test_R5_…`: only `license-by-type` reads the license |
| R-6 | met | `test_R6_…`: the report replays exactly |
| R-7 | not met | The advisory stand-in cold read (G-1). Its other finding (project-files' "Applies to" omitting governance) is wrong: the line names `repo-registry` |

All tests: 50, OK (2 expected failures).

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-4 exist, and every requirement passes | not met | R-7 (G-1) |
| Summary for the supervisor | met | [WP2a-summary.md](WP2a-summary.md) |

## Outside the scope

- **Out-of-scope changes:** one assertion in `tests/test_wp2.py` was updated, because sandbox kinds now carry
  `license-by-type` (3 policies). `scripts/licenses.py` is the report D-4 named.
- **Non-goals touched:** none. No repository was relicensed or written to.

## Gaps

- **G-1 (R-7 not met).** The license SOP:
  1. doesn't say what to do when a repository holds both code and writing. GitHub detects one license per repository,
     and a second license file at the root can make it unrecognizable (red);
  2. says "kind" and "type" without saying that the type is the first part of the kind (`tool/sandbox` → `tool`);
  3. doesn't say what applies to unclassified repositories.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 (three SOP items) | fix before acceptance | Supervisor: "Fix all three". Fixed and checked (below) |

## Final check after the fixes

| Item | Verdict | Evidence |
|---|---|---|
| G-1.1 code and writing in one repo | met | Step 4: the main content's license goes in the root `LICENSE`; the rest in its own folder (for example `docs/LICENSE`), noted in the README; never two root license files |
| G-1.2 type vs kind | met | "Applies to" and step 1 say that the type is the part of the kind before the slash (`tool/sandbox` → `tool`) |
| G-1.3 unclassified | met | "Applies to": no license rule applies yet, a license from the table is still right, and the maintainers will give it a kind |
| All tests | met | 50 tests, OK (2 expected failures) |

## Recommendation

**Recommend acceptance.** Every deliverable, requirement and good-enough item is met after the fixes. The policy and
its report stay PROVISIONAL until the maintainers approve the policies (WP0, maintainer approval 2). Three
repositories with off-list licenses await the maintainers' decision (WP2a summary).

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

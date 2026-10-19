# WP5f — Review report

| | |
|---|---|
| **Scope of work** | [WP5f-scope-of-work.md](WP5f-scope-of-work.md), as amended during execution (D-3's timing) |
| **Scope approval verified** | The supervisor's answer, recorded verbatim in [WP5f-decisions.md](WP5f-decisions.md) "Approval": "Approve it" |
| **Work reviewed** | `wp5f-scope` at 76f10c0 (rebased onto `main` at 26da375, after #13), with this report |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's merge, with a merge commit, of the pull request into `main` (scope and work together) |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `docs/maintainer-policy.md`, "How the first owners and maintainers are chosen": a record, not a rule (OD1 to OD4); provisions 1 to 14 unchanged; the org policies unchanged (OD4) |
| D-2 | met | `work-packages/WP5f-decision-brief.md`: what the policies ask, today's counts, the facts to weigh, the choices, a filled example, and how it is recorded; every person invented and labelled HYPOTHETICAL; not the proposed decision; no one's membership or role shown |
| D-3 | met, as amended | `owners` in `data/maintainers.yaml`, declared in `data/schema/model.yaml` (`list(fk(maintainer))`), empty; `scripts/validate.py` accepts it empty or with 2 or 3 maintainers, without repeats. The decision itself is recorded later, in its own small pull request |
| D-4 | met | `docs/status.md` (WP5f ahead of WP6, critical path, the fifth approval first) and `docs/current-state.md`; the README's roadmap begins "Settle who governs" |
| D-5 | met | `tests/test_wp5f.py` (5 tests); the documents above |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `test_R1_the_policy_records_how_the_first_governors_are_chosen` passes |
| R-2 | met | `test_R2_no_owners_are_recorded_yet` and `test_R2_a_recorded_set_is_two_or_three_maintainers` pass (invented maintainers only) |
| R-3 | met | The privacy scans name no concealed member (below); the brief shows no membership or role |
| R-4 | met | `test_R4_the_package_is_on_the_critical_path_ahead_of_wp6` passes |

On the WP5f work (the same tree, before the rebase onto #13's merge): `scripts/validate.py` "valid: every table meets
data/schema/model.yaml, and every view renders, the same twice"; 120 tests OK (expected failures=1); `scripts/audit.py`:
all 16 findings return none; the privacy scans name no concealed member (191 files; 781 blobs and every commit message
on `main`).

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-5 exist, every requirement passes its check, and the existing suite still passes | met | Above |

## Outside the scope

- **Out-of-scope changes:** none.
- **Non-goals touched:** none. No concealed member is named; no organization role is changed; the org policies are
  unchanged.

## Observations (not counted as failures)

1. `maintainers-match` stays as it is, so once owners are recorded, the org's actual owners will differ from them
   until the changes of control are carried out (OD3); that is the error signal (`org-few-owners`, red), as intended.
2. The README's roadmap now has five steps; the first is this package's subject.

## Open decisions (for the supervisor)

OPEN

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| Observations 1 and 2, as one item | DISPOSITION | |

## Recommendation

RECOMMENDATION

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

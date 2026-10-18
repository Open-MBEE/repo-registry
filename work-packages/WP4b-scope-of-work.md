# WP4b — Scope of work: docs sweep and checkpoint

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `repo-registry` (local) |
| **Approval record** | mzargham's `git merge --no-ff -m "<message>"` of the scope branch into `main` ([AGENTS.md](../AGENTS.md)) |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` ([AGENTS.md](../AGENTS.md)) |

## Purpose

Put the repository in a **safe checkpoint state** before the working session's context is compacted, so that any
future session can pick up from a consistent basis. Since WP0, many decisions (amendments A1 to A4, and decisions
during WP1 to WP4) have outpaced the early DRAFT design documents. This package finds and fixes that drift, and
writes one current-state document to start from (supervisor: "we need a consistent basis to pick from and i am sure
there is some drift").

## Goals

- G1. **No document contradicts a recorded decision** without saying so.
- G2. **One place to start:** a current-state document that states what is decided, where it is recorded, and what
  is next.
- G3. **A verified checkpoint:** every check passes, the tree is clean, and everything is on `main`.

## Non-goals

- New policies, or any change to a classification, selection or policy outcome. Documents, comments, links and
  generated *text* may change; fixing a defect in generated text (found by the audit) is in scope.
- Rewriting approved scope documents or decision records. They are the historical record. Current documents point to
  them instead.
- Promoting DRAFT design content to a rule (AGENTS.md).
- Deleting branches, or anything outward-facing.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | A drift report: every place a document lags or contradicts a recorded decision, with file, line and the superseding record | G1 |
| D-2 | The fixes: each drift item fixed in place, or the stale section marked superseded with a pointer, per OD1 | G1 |
| D-3 | `docs/current-state.md`: the decided model (measurements and attestations → type, stage, tier → policies in effect; a kind is a point in that space, and a policy is a region), the decisions and where each is recorded, the packages and their merges, open items, and how to run every check | G2 |
| D-4 | The checkpoint: `docs/status.md` updated, all tests and generators replay, the privacy scan is clean, the working tree is clean | G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every fix traces to a recorded decision or to the current data and code. | The drift report cites the record for each item |
| R-2 | No outcome changes: every repository keeps its kind, every policy applies to the same kinds, and the pilot and exclude list keep the same repositories. Only text may differ. | Compare kinds, applicability and pilot membership before and after; the full test suite |
| R-3 | Every relative link in `docs/`, `README.md` and `AGENTS.md` resolves. | A link check |
| R-4 | DRAFT stays DRAFT: no design document is promoted. | Inspect |
| R-5 | The privacy scan is clean. | `python3 scripts/privacy_check.py` |

## Definition of good

- A new session, reading only `docs/current-state.md` and following its links, has an accurate picture of the project.

## Definition of good enough

- D-1 to D-4 exist, and every requirement passes its check.
- Every drift item in the report is fixed or marked superseded.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- The drift report is `work-packages/WP4b-drift-report.md` (D-1).
- A link check is added to the tests, so that broken links are caught from now on (R-3).
- A short memory note for future sessions points to `docs/current-state.md`.

## Open decisions (for the supervisor)

- **OD1.** Stale text in the early DRAFT design documents. *Decided: edit in place, keeping them DRAFT.*
- **OD2.** The Agent's defaults. *Decided: approved.*
- **OD3** *(raised by the drift audit)*. Merge authority. *Decided: split by change. Kind changes: any maintainer
  merges. The maintainer list and maintainers' powers: an owner merges. Accepted exceptions: an owner merges. The
  documents are made consistent with this in D-2.*

None remain open. Every item was resolved through the decision loop: 3 decided, 0 deferred, 1 raised (OD3). The
records are in [WP4b-decisions.md](WP4b-decisions.md).

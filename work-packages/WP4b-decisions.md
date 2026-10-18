# WP4b — Decision records

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's.

## Origin

- **Supervisor (mzargham, typed by agent):** "we're going to overflow context soon. in order to avoid risks we should
  do a documentation sweep and cleanup now. we need a consistent basis to pick from and i am sure there is some drift"
- **Supervisor (mzargham, typed by agent):** "okay so i need a clean up work package now that ensures the repo is in a
  safe checkpoint state before compact."

## OD1 — Stale text in the early DRAFT design documents

- **Answer (mzargham, typed by agent):** "Edit in place"

## OD2 — Agent's defaults

- **Answer (mzargham, typed by agent):** "Approve all"

## Scope adjustments before approval (agent, from the drift audit)

- The audit found 109 items, including two defects in generated text. `scripts/pilot.py` truncates "why" at the "."
  in "1.0". The fork reason cites "WP0 parked item", but the parked item is in `design.md`. Fixing them changes text,
  not outcomes. The non-goal and R-2 now forbid outcome changes rather than any change to generated output. The audit
  also found inconsistent merge authority, raised as OD3.

## OD3 *(raised by the drift audit)* — Merge authority

- **Answer (mzargham, typed by agent):** "Split by change"
- **Outcome:** Kind changes: any maintainer merges. The maintainer list and maintainers' powers: an owner merges.
  Accepted exceptions: an owner merges.

## Summary

The open list is empty: 3 decided, 0 deferred, 1 raised.

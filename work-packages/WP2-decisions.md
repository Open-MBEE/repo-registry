# WP2 — Decision records

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's.

## Start of scoping

- **Supervisor (mzargham, typed by agent):** "yes to scoping work package two but now i need you to factor in the 3
  additional sources. the 2 open source software frameworks and the ISO standard."
- **Outcome:** The CNCF and OpenSSF project lifecycles, the OpenSSF security baseline by stage, and ISO/IEC/IEEE
  12207:2026 (by reference only) are secondary sources in the scope, beside CISA and NIST RMF (core).

## OD1 — How directly the OpenSSF baseline shapes the policies

- **Answer (mzargham, typed by agent):** "Backbone"
- **Outcome:** By default, our stage-attached policies mirror the OpenSSF baseline items. Each departure is stated
  with a reason (R-13). The non-goal was adjusted.

## OD2 — Agent's defaults

- **Answer (mzargham, typed by agent):** "Approve all"

## Summary

The open list is empty: 2 decided, 0 deferred.

# Acceptance review (WP2-review.md)

## G-1 — R-5 not met (six SOP problems)

- **Answer (mzargham, typed by agent):** "Fix all six"

## G-2 — Observations

- **Answer (mzargham, typed by agent):** "we can tolerate explicit xfail for work forthcoming in later WPs. you should
  probe the ISO-text more thoroughly"
- **Follow-up:** Are (a) data/sources/ outside the named deliverables and (b) the 14-day critical-fix deadline
  accepted as is?
- **Answer (mzargham, typed by agent):** "Accept a and b"
- **Outcome:** (c) and (d) are recorded as explicit expected failures (data/expected-gaps.yaml,
  tests/test_forthcoming.py). (e): R-12 now checks hashed 8-word passages of the whole standard.

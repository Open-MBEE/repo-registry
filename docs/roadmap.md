# Roadmap

> **DRAFT.** Nothing here is locked until mzargham says "lock."

Each stage has an exit test, written as what must be true. The stages are cumulative.

## R1 — Minimum viable for demonstration and socialization

*Purpose: maintainers agree on taxonomy and policy.*

- The loop runs end to end on the hypothetical case ([testing and demonstration](testing-and-demonstration.md)) with
  fixture bindings (FM-11): it classifies, compares and routes, and it emits wiki pages and issue texts as local files.
- Tests for the in-scope requirements pass in Actions on every PR.
- A draft taxonomy and policy exist as data. Changing them and re-running shows the consequences (X-6).
- A read-only fit test against the live inventory shows where the draft taxonomy fits and where it doesn't (TX-4).
- Both demonstrations have been given.
- *Exit:* the maintainers have agreed on a taxonomy and policy, merged by PR.

## R2 — Minimum viable for operationalization

*Turned on and calibrating. Not yet canonical.*

- Runs on a schedule in Actions against the live org, with a read-only sensing credential.
- The wiki is published, and every page says "calibrating, not yet the source of truth."
- Governors have assigned classes to the highlighted repos. Everything else is `unknown`.
- Actuation is limited to issues, capped per run, and enabled per class by a governor (CL-5, CL-6). *(Draft.)*
- Governance is still low friction, so calibration fixes land quickly (IF-9).
- Calibration: wrong classifications and spurious verdicts are logged and fixed through governance PRs.
- *Exit (draft):* agreed calibration targets met, for example owners agree with their repos' classes, and N
  consecutive runs produce no spurious issues. The attestation round trip (IF-5) has worked on real repos.

## R3 — Minimum viable for canonical

*What must be true for this to be the source of truth.*

- Every repo has a class, or is explicitly `unknown`, `unclassified` or excluded (TX-5).
- Every non-archived repo has an owner. Every tool in active development or maintenance has a release officer (PO-3).
- Every control cites the CISA practice or C4 criterion it serves, or is explicitly marked "none" (PO-4).
- Any classification or verdict can be explained from its trace alone (FM-8). Live runs replay exactly (X-2).
- The taxonomy and policy can be changed without code changes, shown by the toy-taxonomy swap (FM-2).
- A newcomer finds the highlighted repos, and who to ask, from the wiki index page (IF-2).
- *Exit:* the maintainers ratify it, and **its first release makes it canonical**. At that release the
  "calibrating" banner is removed, `repo-registry` moves to a class at least as strict as the strictest class (X-9),
  and governance switches to high friction (IF-9).

## R4 — Desired steady state

*The loop identifies gaps between assigned and current state, and resolves them.*

- Each run identifies every gap between assigned and observed values and routes it (FM-5, FM-6).
- The closed-loop behaviors hold (CL-1 to CL-8). Violations fall, unknowns get resolved by attestation,
  residual error is visible and owned, emergent items reach governors, load on humans stays low, compute stays small.

## R5 — Future features

*Deferred nice-to-haves, off the critical path. (Draft placement.)*

- Org Project board aggregating system-written issues (IF-10).
- A GitHub App for event-driven sensing of other repos, in place of scheduled-only sensing.
- Automatic (non-issue) actuation, such as applying a ruleset. Until then the FM-6 *automatic* channel has no
  binding, and those errors go out as change requests.
- Non-binding, deterministic class suggestions from measurements, to speed up initial class assignment.
- A machine-readable inventory export in the code.json shape described by CISA.

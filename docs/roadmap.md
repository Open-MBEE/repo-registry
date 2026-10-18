# Roadmap

> **DRAFT.** Nothing here is locked until mzargham says "lock."
>
> Brought in line with the decision records at the WP4b docs sweep (2026-10-18). Each changed item says
> "(updated: <record>)". R1 is scoped in detail by [WP0](../work-packages/WP0-scope-of-work.md), which wins where
> this file disagrees. The consistent summary is [current-state.md](current-state.md).

Each stage has an exit test, written as what must be true. The stages are cumulative.

## R1 — Minimum viable for demonstration and socialization

*Purpose: the maintainers approve the taxonomy, the policies, the pilot and its kinds, and the named maintainers.*

- The loop runs end to end, read-only, on the pilot of real repos, from stored snapshots: it classifies, compares and
  routes, and it writes wiki pages and sample issue texts as local files. Nothing is written to the pilot repos
  *(updated: WP0 "Change before approval: a pilot of real repos"; WP0 D-5)*.
- Tests for the in-scope requirements pass in Actions on every PR.
- A draft taxonomy and policy exist as data. Changing them and re-running shows the consequences (X-6).
- A read-only fit analysis of all of the org's repos shows where the draft taxonomy fits and where it doesn't (TX-4).
- The policy basis review exists, and the policies put to the maintainers come from it *(updated: WP0 D-9)*.
- This repo moves to Open-MBEE during R1, in WP5, on the supervisor's go-ahead, and a change with invalid data can't
  land on `main` *(updated: WP0-decisions "Remote during R1"; WP0 R-14)*.
- The org governance check has run on the pilot snapshot *(updated: WP0 R-15)*.
- All three demonstration flows (reader, operator, governor) have been given *(updated: WP0-decisions D-5)*.
- *Exit:* the five maintainer approvals, each recorded by a merged PR in this repo: the taxonomy; the policies, based
  on the taxonomy; the pilot subset; each pilot repo's kind; and the named maintainers, who become this repo's
  CODEOWNERS *(updated: WP0 definition of good enough)*.

## R2 — Minimum viable for operationalization

*Turned on and calibrating. Not yet canonical.*

- Runs on a schedule in Actions against the live org, with a read-only sensing credential.
- The wiki is published, and every page says "calibrating, not yet the source of truth." Its first layer, the review
  pack (the what and why of compliance), is published from WP5d; the compliance dashboard (status per repository and
  policy, and how to come into compliance) is WP7 *(updated: WP5d)*.
- Every repo has an inferred initial kind; operators change it by a PR that any maintainer merges *(updated: WP0 OD3;
  WP4b OD3)*.
- Actuation is limited to issues, capped per run, and enabled per kind by a governor (CL-5, CL-6). *(Draft.)*
- Governance is still low friction, so calibration fixes land quickly (IF-9).
- If the maintainers buy in and work together to calibrate it, `repo-registry` is assigned governance/incubating
  (medium) *(updated: WP1 amendment 3)*.
- Calibration: wrong kinds and spurious verdicts are logged and fixed through governance PRs.
- *Exit (draft):* agreed calibration targets met, for example operators agree with their repos' kinds, and N
  consecutive runs produce no spurious issues. The attestation round trip (IF-5) has worked on real repos.

## R3 — Minimum viable for canonical

*What must be true for this to be the source of truth.*

- Every repo has a kind, or is explicitly `unclassified` or excluded (TX-5) *(updated: WP0 OD3; no `unknown` kind)*.
- Every repo in a tier that needs an owner (high, medium, low) has CODEOWNERS. Release authority for incubating and
  graduated tools is recorded in the maintainer list (PO-3) *(updated: WP0 R-17; A4; maintainer-policy item 12)*.
- Every policy cites the CISA practice and the RMF task or SP 800-53 control it serves, or is explicitly marked
  "none" (PO-4) *(updated: WP0 R-16)*.
- Any kind or verdict can be explained from its trace alone (FM-8). Live runs replay exactly (X-2).
- The taxonomy and policy can be changed without code changes, shown by the toy-taxonomy swap (FM-2).
- A newcomer finds the highlighted repos, and who to ask, from the wiki index page (IF-2).
- *Exit:* the maintainers ratify it, and **its first release makes it canonical**. At that release the
  "calibrating" banner is removed and governance switches to high friction (IF-9): merging to `main` then needs
  CODEOWNERS (OpenMBEE maintainers) approval. `repo-registry` is assigned governance/graduated (high) here, having
  passed through governance/incubating while it was calibrated (X-9, expected gap XF-2) *(updated: WP1-decisions G-2;
  A4; WP1 amendment 3)*.

## R4 — Desired steady state

*The loop identifies gaps between assigned and current state, and resolves them.*

- Each run identifies every gap between assigned and observed values and routes it (FM-5, FM-6).
- The closed-loop behaviors hold (CL-1 to CL-8). Violations fall, unknowns get resolved by attestation,
  residual error is visible and owned, emergent items reach governors, load on humans stays low, compute stays small.

## R5 — Future features

*Deferred nice-to-haves, off the critical path. (Draft placement.)*

- Org Project board aggregating system-written issues (IF-10).
- A GitHub App for event-driven sensing of other repos, in place of scheduled-only sensing.
- Automatic (non-issue) actuation, such as applying a ruleset. Until then there is no *automatic* channel, and gaps go
  out as change requests *(updated: WP0 Tension 3)*.
- ~~Non-binding, deterministic kind suggestions from measurements.~~ Done in R1: the recommendation rules in the
  taxonomy infer each repo's initial kind *(updated: WP1 D-2, D-5)*.
- A machine-readable inventory export in the code.json shape described by CISA.

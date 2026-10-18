# Testing and demonstration

> **DRAFT.** Nothing here is locked until mzargham says "lock." This document specifies the case that testing and
> demonstration run on, in prose.
>
> Brought in line with the decision records at the WP4b docs sweep (2026-10-18). The made-up org this file first
> described was replaced by a pilot of real repos before WP0 was approved *(updated: WP0-decisions "Change before
> approval: a pilot of real repos"; WP0 D-5)*. The consistent summary is [current-state.md](current-state.md).

Both testing and demonstration run on the **pilot**: a scoped subset of real Open-MBEE repos, run read-only from
stored snapshots. The live org will show high error, and its taxonomy and policy still need the maintainers'
approval. So correctness (testing) and understanding (demonstration) are established first on the pilot, where
nothing is written to the repos and the sample issues are not posted.

## The pilot

24 to 36 real repos (32 proposed, in [pilot-briefing.md](pilot-briefing.md)), sampled to include heavily used and
actively developed tools, the website and other media, some research repos, and some repos that should be archived.
Every other public repo is on the exclude list with a reason *(updated: WP0 D-5; WP4)*. The pilot runs on the draft
taxonomy and policy through the snapshot bindings (FM-11). It produces the same outputs as a live run (wiki pages and
sample issue texts) as local files, and publishes nothing. Between them, the pilot and the test cases exercise:

- every kind in the taxonomy under test *(updated: WP0 terminology)*;
- one `unclassified` repo (no kind fits); a fact the sensor can't read shows as a yellow "can't tell" check, not as an
  `unknown` kind *(updated: WP0 OD3, R-13)*;
- one excluded repo (TX-5);
- one fork;
- one accepted deviation (PO-8);
- one archived repo, whose instructions must land in this repo (IF-4);
- a mix of conforming and violating repos, including configurations present, absent and unreadable (PO-7);
- a repo in an owned tier whose CODEOWNERS is present, and one where it is missing (PO-9) *(updated: WP0 R-17)*;
- a low-friction repo whose kind page shows which policies deliberately don't apply (PO-10) *(updated: WP0 D-3)*;
- one failed run (X-10).

A small made-up set of kinds and policies survives only for the toy-taxonomy swap (FM-2, WP0 R-6), in
`tests/fixtures/`.

## Testing: did we build what we designed?

Each requirement's "assessed by" column becomes a check against the stored pilot snapshot: expected kinds,
verdicts, routes and action log, plus replay (X-2) and the toy-taxonomy swap (FM-2). Tests run in Actions on every
policy-plane PR.

## Demonstration: can people use it?

A scripted walkthrough on the same pilot, as three flows, one per role *(updated: WP0-decisions D-5)*:

1. **Governors** (maintainers), to approve the taxonomy and policy before going live: "here is what these rules
   would do to these repos." Changing the draft rules and re-running shows the consequences (X-6).
2. **Operators** (each repo's CODEOWNERS) *(updated: WP0 R-17)*: find a sample issue for their own repo, answer an
   attested check in the repo's `ATTESTATIONS.yaml` *(updated: WP0 amendment 3)*, propose a kind change by PR, and close an issue when done.
3. **Readers** (newcomers, contributors, the community manager): navigate the wiki pages and views by kind, tier
   and policy, and follow a repo's links to the repo and its open registry issues.

# Requirements — interfaces

> **DRAFT.** Nothing here is locked until mzargham says "lock." Columns and sources are defined in
> [design.md](../design.md#requirement-conventions).
>
> Brought in line with the decision records at the WP4b docs sweep (2026-10-18); each changed requirement says
> "(updated: <record>)". The consistent summary is [current-state.md](../current-state.md).

There is one interface per role: **reader** → the wiki of this repo; **operator** (the repo's CODEOWNERS) → issues
in their own repo, plus direct edits to it; **governor** → this repo (PRs and its issues), and ideally an org Project
board.

| ID | Requirement | Src | Assessed by |
|---|---|---|---|
| IF-1 | The wiki is generated entirely from controller state each run: an index page; one page per kind, per tier and per policy; and views of the registry by kind, by tier and by policy, with each repo's status and links. No page per repo *(updated: WP0 D-3, "Wiki downscope")*. Hand edits are overwritten. | M | Regenerate from a snapshot and diff |
| IF-2 | The wiki index page shows highlighted repos (incubating or graduated) first, then every repo with its kind and CODEOWNERS, then the exclude list with reasons *(updated: WP0-decisions "README reader section brought in line"; WP1 amendment 2 defaults)*. | M, S | Cold-read navigation task |
| IF-3 | Every instruction for an operator is an issue in the repo it concerns, saying what to do, why (rule + evidence), and who is asked. Items needing a policy decision are issues in this repo. In R1 these are sample issue texts only, not posted *(updated: WP0 D-4)*. | M | Issue template review |
| IF-4 | Where a target repo can't take issues (archived, or issues disabled), the instruction lands in this repo instead, labelled with the target. | E | Fixture with an archived repo |
| IF-5 | Every request for a fact says exactly where to answer and in what format, so the next run can read the answer deterministically: an attestation block in the repo's README, committed by a code owner, out of date once older than the repo's latest release *(updated: WP0 "Compliance", R-13, R-17)*. | M | Round-trip test on the pilot |
| IF-6 | Closing an issue asserts the task is done. *(Draft: for measurable attributes the next sense pass checks, and reopens the issue if the error remains.)* | M | Close-without-fix test |
| IF-7 | Direct edits to registered repos are picked up by sensing. No separate report is needed. | M | Sense after an edit on a fixture |
| IF-8 | No duplicated bureaucracy: each fact is entered once, in one place, inside GitHub. | M | Walkthrough of each request type |
| IF-9 | Governance friction follows the lifecycle. *Before canonical (R1–R2: build, calibrate, ratify):* low friction; in R1 the only restriction is the valid-`main` check (WP0 R-14). *From the first release that makes it canonical (R3):* merging to `main` needs CODEOWNERS (OpenMBEE maintainers) approval; the number of reviews is parked. `repo-registry` is already governance/sandbox (high tier); the friction gap until R3 is expected gap XF-2 *(updated: WP0 non-goals; WP0-decisions "How restrictive this repo is in R1"; WP1-decisions G-2; A4)*. | M | Branch-protection/ruleset settings checked by the system on itself |
| IF-10 | *(Should)* An org Project board aggregates every open issue the system has written, for governors. | M | Board lists all system-written issues |

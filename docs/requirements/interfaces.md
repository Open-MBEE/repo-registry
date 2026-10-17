# Requirements — interfaces

> **DRAFT.** Nothing here is locked until mzargham says "lock." Columns and sources are defined in
> [design.md](../design.md#requirement-conventions).

There is one interface per role: **reader** → the wiki of this repo; **operator** → issues in their own repo,
plus direct edits to it; **governor** → this repo (PRs and its issues), and ideally an org Project board.

| ID | Requirement | Src | Assessed by |
|---|---|---|---|
| IF-1 | The wiki is generated entirely from controller state each run: one index page, one page per class, one page per repo. Hand edits are overwritten. | M | Regenerate from a snapshot and diff |
| IF-2 | The wiki index page shows highlighted repos first, then every repo with its class, owner, release officer and open-issue count, then the exclude list with reasons. | M, S | Cold-read navigation task |
| IF-3 | Every instruction for an operator is an issue in the repo it concerns, saying what to do, why (rule + evidence), and who is asked. Items needing a policy decision are issues in this repo. | M | Issue template review |
| IF-4 | Where a target repo can't take issues (archived, or issues disabled), the instruction lands in this repo instead, labelled with the target. | E | Fixture with an archived repo |
| IF-5 | Every request for a fact says exactly where to answer and in what format, so the next run can read the answer deterministically. | M | Round-trip test on the hypothetical case |
| IF-6 | Closing an issue asserts the task is done. *(Draft: for measurable attributes the next sense pass checks, and reopens the issue if the error remains.)* | M | Close-without-fix test |
| IF-7 | Direct edits to registered repos are picked up by sensing. No separate report is needed. | M | Sense after an edit on a fixture |
| IF-8 | No duplicated bureaucracy: each fact is entered once, in one place, inside GitHub. | M | Walkthrough of each request type |
| IF-9 | Governance friction follows the lifecycle. *Before canonical (R1–R2: build, calibrate, ratify):* low friction. *From the first release that makes it canonical (R3):* only CODEOWNERS (OpenMBEE maintainers) may approve, and merging to `main` needs multiple approving reviews. The self-class change (X-9) happens at the same moment. | M | Branch-protection/ruleset settings checked by the system on itself |
| IF-10 | *(Should)* An org Project board aggregates every open issue the system has written, for governors. | M | Board lists all system-written issues |

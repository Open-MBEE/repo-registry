# WP0 — Decision records

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's.

## Package goal (before drafting)

- **Question:** What should WP1 deliver?
- **Answer (mzargham, typed by agent):** "review the design docs. (all of which should be flagged as draft) and compile
  a zoomed out scope of work for me to approve. this is a critical step to align expectations independent of the
  potentially over detailed design docs"
- **Outcome:** WP0 is a zoomed-out scope of work for the project. The design docs are cited as DRAFT inputs only. All
  ten design docs were checked and already carry a DRAFT flag.

## OD1 — Horizon

- **Question:** What horizon should the WP0 scope cover?
- **Answer (mzargham, typed by agent):** "Through R1"
- **Outcome:** Scope, deliverables, and the definitions of good and good enough were narrowed to R1. R2 to R5 are
  non-goals.

## Agent's defaults: how to review

- **Question:** OD2: approve the Agent's defaults as is, or change some?
- **Answer (mzargham, typed by agent):** "walk me through them and let me decide them one at a time"
- **Outcome:** Each default is decided on its own.

## Default 1 — WP0 name and path

- **Answer (mzargham, typed by agent):** "Keep WP0"

## Default 2 — Design docs are DRAFT inputs only

- **Answer (mzargham, typed by agent):** "Keep"

## Default 3 — Review tensions

- **Answer (mzargham, typed by agent):** "work through each of them with me in their own popups"
- **Outcome:** Each tension was decided below and added to WP0 as direction.

### Tension 1 — Is a repo's kind computed or assigned?

- **Answer (mzargham, typed by agent):** "this is a closed loop system model. governors have the power to assign but we
  will initialize the system with a set of inferred values based on our taxonomy. my instinct is that new repos get
  classified as unknown but may get recommended categories based on their measurable attributes. if possible i'd like
  to make it so the operators decide the designation of their own repos (so it becomes a measured or attested
  attributed) but the governor layer can override the operator assignment"

### Tension 2 — Settings the sensor can't read

- **Answer (mzargham, typed by agent):** "stronger credential but we need a high credential for reading and
  comparatively week credential for writing"
- **Outcome:** Added R-9.

### Tension 3 — The automatic fix channel

- **Answer (mzargham, typed by agent):** "explain this in more detail. the automatic fix channel as i understand it is
  an automated change. i think we're pushing this into future scope. as it assumes we have standard policies and i
  suspect admin level changes violate our weak write credential preference. so for now let's organize this as future
  work: nice to have UX improvements but needing to trade off against security"
- **Outcome:** Automatic fixes are a non-goal (future work). Gaps go out as change requests.

### Tension 4 — The open set of kinds

- **Answer (mzargham, typed by agent):** "First package"

## Default 4 — Requirements and their checks

- **Answer (mzargham, typed by agent):** "walk me through anything that is load bearing so i can approve 1 at a time"
- **Outcome:** R-1 to R-8 were each put to the supervisor. Each answer (mzargham, typed by agent): "Approve".

## Default 5 — Deliverables grouped by part of the system

- **Answer (mzargham, typed by agent):** "keep them grouped by part of the system but make a grid part by requirement
  and ensure we have testing coverage any place a deliverable touches a requirement. there may be some sparsity in the
  matrix but test coverage mapped to the deliverable cross requirements grid will help avoid thrashy iterations"
- **Outcome:** Added the deliverable × requirement coverage grid, R-10 (every marked cell has its check), and a
  good-enough item. The cell contents are an agent default.

## Default 6 — R-9 check, and the meaning of a weak write credential

- **Answer (mzargham, typed by agent):** "it can only open and comment on issues and push the wiki. it can also close
  issues if it has sensed that the task is complete from its read capability."
- **Outcome:** R-9 now states what the write credential may do, including closing an issue once sensing shows the task
  is done. The scope inspection check stays an agent default, and the grid gained a check in D-4.

## Default 7 — Coverage grid cells

- **Answer (mzargham, typed by agent):** "Row by row", then mid-way: "the above makes me think we're sweeping on the
  wrong access can we sweep the deliverables dimension instead of the requirements dimension, its way more intuitive
  for me. also would allow me to cut or clarify scope"
- **Outcome:** The grid is reviewed one deliverable column at a time, and each deliverable can be approved, clarified
  or cut.

### D-1 — Rules as data

- **Answer (mzargham, typed by agent):** "Approve"

### D-2 — Program

- **Answer (mzargham, typed by agent):** "add an idepotency requirement so we don't spam repos full of issues flagging
  the same gap"
- **Outcome:** Added R-11 (idempotent: at most one open issue per gap, and a rerun on an unchanged gap posts nothing
  new) and its grid row.

### D-3 — Wiki pages

- **Answer (mzargham, typed by agent):** "Approve"

### D-4 — Issue texts

- **Answer (mzargham, typed by agent):** "clarification. issue texts are deterministic. template fillable based on on
  our state machine. any issue is specifically a statement that the repo is out of alignement with a specific policy in
  effect for its classification. strictly speaking we expect the primary path is to change repo config to match policy
  but we have an escalation path to request reclassification. my instinct is that a repo owner can self set their
  classification if the classification is unknown but once a classification is set changing it is a governance action.
  we do need to make changing the classification as easy as possible and human readable so the canonical
  classification list should probably a yaml file in the root. with only enough information to dereference relevant
  policy docs. the policy docs likely also need to be yaml so they can be easily checked against sensed data, i am not
  asserting yaml but its a starting point for reasoning about a design that need to be both easily human read and
  machine readable data format"
- **Outcome:** D-4 and D-1 were reworded. The direction on kinds was refined (it replaces the Tension 1 wording):
  owners set a kind only while it is `unknown`, and after that changing it is a governance action. Added a direction
  item on the canonical kind list and policy files, and R-12 (easy, readable reclassification) with its grid row.
  Raised OD3: where an owner sets an `unknown` repo's kind.

### D-5 — Made-up org and demonstrations

- **Answer (mzargham, typed by agent):** "just do one made up org and have 3 demonstration flows, one for each
  stakeholder category)"
- **Outcome:** D-5 is now one made-up org with three demonstration flows (reader, operator, governor). Good enough was
  updated to match.

### D-6 — Fit report

- **Answer (mzargham, typed by agent):** "Approve"

## OD3 *(raised by D-4)* — Where an owner sets a repo's kind

- **Answer (mzargham, typed by agent):** "PR to this repo to set your status. this also reversed a previous decision i
  made. if we use PR to this repo to request a recatigorization then we can use the same approach for any change. and
  we can give every repo an initial value will inviting operators to PR to change to update their status. kind change
  requests are the only operation an operator (repo owner) needs to do on this registry."
- **Follow-up:** Who approves and merges an owner's kind-change PR?
- **Answer (mzargham, typed by agent):** "Governors"
- **Outcome:** Every repo gets an inferred initial kind. Operators propose changes by PR to this repo, and governors
  merge. This replaces "a new repo starts as unknown" and "the owner sets an unknown kind". The issue escalation path
  is a kind-change PR.

## Remaining defaults (R-9 check, R-11 no new comment, R-12 check)

- **Answer (mzargham, typed by agent):** "Approve all three"

## Late grid cells (R-12 under D-1, D-3, D-4)

- **Question:** Approve the three cells added after their columns were approved?
- **Status:** asked, and the supervisor answered with the message below instead. Still open.

## Red / yellow / green status *(raised by supervisor)*

- **Supervisor (mzargham, typed by agent):** "i want to add one more thing. the wiki for this should have a red yellow
  green model so that we can scan for compliance. red means we know its out of compliance yellow means we cannot tell
  and green says we know its in compliance. this is primarily useful to governors but also helpful for readers who
  care about compliance, since they should trust repos in green state."
- **Outcome:** Added to D-3, plus R-13 and its grid row. The roll-up rule and showing the status in words are agent
  defaults.

### R-13 follow-up — Status of an accepted deviation

- **Answer (mzargham, typed by agent):** "Green, marked"
- **Outcome:** A control with an accepted deviation is green, visibly marked as an accepted exception.

## Late grid cells (R-12 and R-13 cells)

- **Answer (mzargham, typed by agent):** "Approve"

## R-13 defaults (roll-up rule; words as well as color)

- **Answer (mzargham, typed by agent):** "yes, and the status status logs should be in git repo (probably another yaml
  file with clean joins to the registry yaml file) so that the compliance history is in the git history"
- **Outcome:** Both defaults approved. Raised: a status log as a data file that joins cleanly to the canonical kind
  list, so the compliance history is in git. Follow-up asked about where it is written, because R-9 limits writing.

### Status log follow-up — Where it lives

- **Answer (mzargham, typed by agent):** "the status logs belong in this repo. furthermore i was planning to use the
  built in wiki on this repo not the openmbee wiki. this wiki has a narrow remit. that other wiki is a repo with a much
  broader remit. its a media repo with relatively permissive kind, whereas this repo needs to be pretty restrictive"
- **Outcome:** Added D-7 (status log in this repo) and its grid column. R-9 widened to allow committing the status
  log. Added a direction item: the wiki is this repo's built-in wiki. Raised: how restrictive this repo is during R1.

### D-7 — Status log

- **Answer (mzargham, typed by agent):** "think of this as a ci/cd pipeline where the wiki being published is the
  deployment. but the ci part checks that no secondary rules are violated. this repo is governing the rules about the
  rules. it describes what kinds repos can be and what controls are necessary by kind, and tracks compliance (measured
  and attested) with those rules. it should not be possible to merge to main an invalid state. to be clear invalid
  means not correctly constructed (violating meta rules) we're explicitly allowing out of compliance as a valid state
  so we can identify and remediate"
- **Outcome:** Added a CI/CD direction item, R-14 (no invalid state reaches `main`; out of compliance is valid; the
  wiki is published only from a valid `main`), its grid row, and a good-enough item.

## Remote during R1 *(raised by R-14)*

- **Question:** This repo has no remote until the first milestone, yet R1 needs tests in Actions and a check that
  blocks invalid merges to `main`. How should R1 handle that?
- **Answer (mzargham, typed by agent):** "Move during R1"
- **Outcome:** The move to Open-MBEE happens within R1, and the move itself waits for the supervisor's go-ahead. The
  non-goal on writing to the live org now excepts this repo, and good enough was updated.

## How restrictive this repo is in R1 *(raised by the status-log answer)*

- **Answer (mzargham, typed by agent):** "valid-main check only BUT explicitly include the swap to codeowners approval
  policy in a later step in the roadmap"
- **Outcome:** In R1 the only restriction is R-14. The switch to CODEOWNERS approval is named as an explicit later step
  in the WP0 non-goals. roadmap.md R3 now names the switch to CODEOWNERS approval explicitly (it said only "high friction").

### R-14 cells in earlier-approved columns

- **Answer (mzargham, typed by agent):** "Approve"

### D-7 — Status log (final)

- **Answer (mzargham, typed by agent):** "Approve"

## Summary

The open list is empty: 39 decided, 0 deferred, 10 raised.

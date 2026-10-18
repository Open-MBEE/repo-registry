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

## Change before approval: a pilot of real repos instead of a made-up org

WP0 had not been merged, so it was revised on the scope branch rather than amended.

- **Supervisor (mzargham, typed by agent):** "i want to make a change. we don't need a made up org, we need to use a
  scoped subset of the openmbee repos. we can exercise our exclusion role so that we only have about 25 repos in our
  initial registry sampled to meet two key requirements heavily used and actively developed tools included, also the
  website and other media examples, some research related repos, some examples of repos that should be archived.
  basically we want to be able to show how the taxonomy and policy system works. in practice. you can create samples
  of the issues it would write but do not write them to the repos yet. these are demonstrations of what would be
  written. the focus is on showing what would happen if we turned it on. what we actually need from the maintainers is
  the following * approve the taxonomy * approve the policies (based on the taxonomy) * approve an initial subset of
  repos to be in the registry * approve the assigned kind for each repo in the registry once we have all of that we can
  move forward with a bounded PoC to calibrate towards a trusted source of truth and bring out repos into policy
  alignment."
- **Follow-up:** With the registry now a subset, what happens to D-6, the fit report on all repos?
- **Answer (mzargham, typed by agent):** "these are two different tasks. we still want the analysis of how it fits all
  183, but the pilot is scoped to something in the 2 to 3 dozen range to balance the level of effort against the need
  to prove value"
- **Outcome:** D-5 is now the pilot: 24 to 36 real repos, everything else excluded, run read-only. The sample issues
  are not posted. D-6 is the fit analysis of all repos, a separate task. Good enough now lists the four maintainer
  approvals, and the R2 proof of concept is named in Purpose. Raised OD4 (three new agent defaults).

## OD4 *(raised by the pilot change)* — Three pilot defaults

- **Answer (mzargham, typed by agent):** "Approve all three"

## Named maintainers *(raised by supervisor)*

- **Supervisor (mzargham, typed by agent):** "almost ready. we need to add one more thing the maintainers need to do,
  and that is figure out who the named maintainers are. they become the codeowners for this repo. as of right now we
  have a leadership but its not necessarily mapped to technical leadership and as far as i can tell from the github
  org configuration we don't have a clear indication of who has admin authority and what powers they have which is
  really important for complying with the cisa guidance"
- **Follow-up:** Should WP0 deliver something about admin authority?
- **Answer (mzargham, typed by agent):** "i think its the codeowner for this repo and the admins for the github org. we
  should apply the same principle for the org as a whole that we applied for repos. we should be clear what the policy
  is and have means of measuring whats measureable and attesting what is not measurable to ensure our state list
  maintainers maps to the list of people with governance power over the github org"
- **Outcome:** Added a fifth maintainer approval (the named maintainers, who become this repo's CODEOWNERS), a direction
  item, D-8 (org governance), R-15 and their grid column and row. Raised OD5 and OD6.

## OD5 *(raised by named maintainers)* — D-8, R-15 and the D-8 column

- **Answer (mzargham, typed by agent):** "Approve"

## OD6 *(raised by named maintainers)* — Two defaults and the R-15 cells

- **Answer (mzargham, typed by agent):** "Approve all"

## Kinds and policies as dimensionality reduction *(raised by supervisor)*

- **Supervisor (mzargham, typed by agent):** "one more thing i want to discuss. in order to keep the complexity of this
  repo from exploding i want to be clear that policies kinds and policies are dimensionality reducing techniques. we do
  not need to directly support all possible policies that can be created in github we need to name policies, document
  the configurations of those policies and clear state which policies are in effect for which kinds. Each policy needs
  to have an SOP for complying with it that covers how to set it up, as well as how what its measurable (and thus
  automatable) checks are and what its attested checks are. to be in compliance a repo needs to pass its automated
  checks and have up to date attestations from an operator (the party accountable for the repo). for exploratory
  research repos these are pretty lax, by design in some cases we have single committers just exploring ideas in
  public, these repos often get archived when they go stale but the point is we don't want to stop that activity.
  furthermore archived repos are read only so they by definition are compliant once they've been transitioned into
  archive state. one of the main goals here is to create rigorous controls on repos that need it while allowing a lot
  of low friction work elsewhere"
- **Follow-up:** What status does a repo get when its automated checks pass but an attestation is out of date or was
  never given?
- **Answer (mzargham, typed by agent):** "red if we compute a missing attestation thats required given a policy. out of
  date is non conformant but my intuition is that we can provide a template for attestation in the readmes of our repos
  as trailers so they don't fall behind releases. updating your attestation becomes part of the SOP. for repos that
  don't require any attestations Green can happen with no attestations present.I suspect the latter will be the case
  for some repo kinds."
- **Outcome:** Added direction items (dimensionality reduction, SOP per policy, compliance, low friction for
  research, archived repos green), a non-goal, a revised D-1, R-13 wording and R-16 with its grid row. Raised OD7.

## OD7 *(raised by named policies)* — R-16, its grid row, revised D-1, the attestation-freshness default

- **Answer (mzargham, typed by agent):** "i approve these. i also want to add a second core citation to our repo
  alongside the cisa guidance. we should be citing NIST RMF 2. and i'd like you to sweep our current scope of work to
  make sure we're not obviously violating or missing anything relevant to what we're doing"
- **Outcome:** OD7 approved. Raised: NIST RMF as a second core citation, and a sweep of WP0.

## Sweep of WP0: small fixes made without a decision

- G5 now lists all five maintainer approvals (it was missing the named maintainers).
- "Class pages" became "Kind pages" in the grid.
- G2 and G4 now say how R1 shows them (on the pilot, and with sample issues).

## NIST RMF as a second core citation

- **Question:** How should WP0 cite NIST SP 800-37 Rev. 2 (RMF) alongside CISA?
- **Answer (mzargham, typed by agent):** "Map plus per policy"
- **Outcome:** Added a direction item with the RMF step map. G2, D-1 and R-16 now cite RMF, and each policy names the
  CISA practice and the RMF task or SP 800-53 control it serves, or "none". The agent read "NIST RMF 2" as
  SP 800-37 Rev. 2, and the supervisor didn't pick the "different document" option.

## Sweep gap 1 — Where each repo's operators are named

- **Answer (mzargham, typed by agent):** "in each repo. the repos are all locally governed by their codeowners, or they
  are low enough tier kind that we don't need formal tracking. we honestly expect to have 4 tiers across our many
  kinds. high, medium, low and none. high is core tools that need rigorous release control. medium for load bearing
  media like the website or tools which are ancillary or experimental, low stuff that needs an owner but has no formal
  controls beyond someone who looks after it and non for archived materials since they are read only once they've been
  verified as archived status."
- **Outcome:** Added a four-tier direction item and an operators-in-each-repo item, revised G3, and added R-17 with its
  grid row. Defaults: where a tier needs an owner, the owner is the repo's CODEOWNERS, and only a CODEOWNER's
  attestation counts.

## Sweep gap 2 — Archiving and CISA end-of-support

- **Answer (mzargham, typed by agent):** "Archive SOP"
- **Outcome:** Added a named archive policy: before archiving, the README states that support has ended and points to
  known forks. Default: repos archived before the policy existed are compliant as they are.

## Sweep gap 3 — Org-wide settings (common controls)

- **Answer (mzargham, typed by agent):** "Include in org policy"
- **Outcome:** The org policy and D-8 now cover a few org-wide settings, inherited by every repo and checked like any
  policy. Which settings is left to the policy drafting. (The agent's question said CISA asks for these. That claim is
  not verified against the CISA text and is not written into WP0.)

## Sweep gap 4 — AGENTS.md and README conflicts

- **Answer (mzargham, typed by agent):** "Update now"
- **Outcome:** AGENTS.md (local until the move during R1; operators' only action here is kind-change PRs; no writes
  to the live org except this repo once moved) and README (the operator's only action here) were edited on the scope
  branch, approved by the same merge.

## R-17, its grid row and three defaults

- **Answer (mzargham, typed by agent):** "yes and our registry repo should be able to read codeowners from the other
  repos tracked in the registry so we have that data in our wiki. its just important that the repos codeowners are the
  authoritative source of truth for a given repo."
- **Outcome:** Approved. WP0 now says the registry reads every tracked repo's CODEOWNERS and shows them in the wiki,
  and that each repo's own CODEOWNERS is the authoritative source.

## README: links to the guidance and the design intent *(raised by supervisor)*

- **Supervisor (mzargham, typed by agent):** "one more thing. we need to include in the readme links to the NIST RMF and
  CISA document. it should be clear that this registry is designed to allow us to come into alignment with this
  guidance through minimum viable policy making, and controls. maximizing ease of demonstrating compliance with our
  policies and minimizing overhead. keep maintainers centralized org level load light and distributing authority to
  repo level code owners, and making it clear what release controls they need to implement by tier."
- **Outcome:** README gained a "The guidance we follow" section with links to the CISA PDF (cisa.gov) and NIST's
  SP 800-37 Rev. 2 page (csrc.nist.gov), the minimum-viable-policy intent, and the four tiers. WP0's citation item now
  links both.

## Wiki downscope, and the chain from kind to tier to policy *(raised by supervisor)*

- **Supervisor (mzargham, typed by agent):** "i think we can downscope D3, registry doesn't need a page for every repo. it
  needs a page for every kind, policy and tier. and it needs to have views on the registry by kind, by policy and by
  tier. it should have color codes by repo, and it should support links to the repos and links to views on the
  outstanding issues in those repos filtered by the tags we used when we wrote the issues programmatically. this wiki
  is specifically for this registry, it covers the registry's status information, and what the kinds and tiers mean,
  and it contains the policies. we'll be classifying kinds from rich data about repos, then kinds map to tiers and
  tiers map to policies. so repos pilot count is dozens but full scope is low hundreds. kinds are a relatively low
  cardinality taxonomy, tiers is 4, and policies are more than 4 since multiple policies can be in effect for the same
  tier but they are defined at a level configurable in github so i suspect it will be important for you to review the
  github security features and documentation, and to cross check that with the NIST and CISA frameworks to ensure we
  have the simplest set of policies that achieves our security objectives."
- **Outcome:** D-3 was downscoped (no page per repo; pages per kind, policy and tier; views by each; color codes and
  links). Added the repo → kind → tier → policies chain, with policies now mapped to tiers rather than kinds (D-1,
  R-16, issues and non-goals updated). Added D-9 (policy basis review) and R-18 (repo and issue links), with their grid
  cells. Raised OD8 and OD9.

## OD8 *(raised by the wiki downscope)* — Revised D-3 and its column

- **Answer (mzargham, typed by agent):** "Approve"

## OD9 *(raised by the wiki downscope)* — D-9, R-18, their cells, the issue-label default

- **Answer (mzargham, typed by agent):** "Approve all"

## Summary

The open list is empty: 55 decided, 0 deferred. Raised items are marked *raised* above.

## README reader section brought in line with the D-3 downscope

- A small fix made without a decision. The README's reader section no longer promises a page per repository. It
  lists pages per kind, tier and policy, plus the views and their red / yellow / green status and links. The index
  shows each repo's CODEOWNERS rather than "owner and release officer".

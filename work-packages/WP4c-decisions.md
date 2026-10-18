# WP4c — Decision records

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's. The scope document carries only the outcomes ([WP4c-scope-of-work.md](WP4c-scope-of-work.md)).

## Why this package exists

- **Supervisor (mzargham, typed by agent):** "i am looking at the policy applicability table
  (/Users/z/Documents/GitHub/repo-registry/docs/policy-applicability.md) and i am a bit confused why governance
  graduated has so many fewer policies than governance sandbox. something feels off. it seems like sandbox should
  have less friction then graduate to a tightly controlled regime one its canonical"
- **Supervisor, on the next step (mzargham, typed by agent):** "Pause WP5 and scope a package to fix the governance
  kinds first."
- **Outcome:** WP5 is paused on `wp5-work` (08b6e3a, nothing written to the org). This package is scoped first.

## OD1 — How the org's administration is told apart from repo-registry

- **Question:** How should the org's administration be told apart from repo-registry, so that the stage axis means
  only maturity? (Options: its own type / not a kind.)
- **Answer (mzargham, typed by agent):** "Its own type"
- **Outcome:** The org's administration gets a type of its own. Applies-if rules still read only type, stage and
  tier.

## OD2 — repo-registry's tier before it is canonical

- **Question:** What tier should repo-registry have before it is canonical (governance/sandbox)? In WP1 you said
  "anything with governance type is tier high" and that governance controls must be "as strict or stricter than
  anything they govern". Now you say "sandbox should have less friction". (Options: low / medium / stays high.)
- **Answer (mzargham, typed by agent):** "Low"
- **Outcome:** governance/sandbox maps to low, with the policies of a sandbox tool. This supersedes "anything with
  governance type is tier high" (WP1 G-2) for the sandbox stage. governance/graduated stays high.

## governance/incubating *(raised by the supervisor during OD3)*

- **Supervisor (mzargham, typed by agent):** "we also expect it to pass through governance incubating during the
  period we're calibrating it so that needs to exist in our model even if its empty today"
- **Outcome:** governance/incubating is defined, not omitted: repo-registry's path is sandbox (R1) → incubating
  (calibration, R2) → graduated (canonical, R3). Its tier and policies are in the Agent's defaults (medium, like
  tool/incubating), which are put to the supervisor again as one item.

## OD1, revisited — the org and repo-registry are one type *(raised by the supervisor's answer on the defaults)*

- **Supervisor, answering the defaults question (mzargham, typed by agent):** "i think the organization and repo
  registry are the same type but they are at different lifecycle points, we don't need to differentiate them on type
  (governance versus organization) just by graduated for open-mbee (the github org) and sandbox for the repo
  registry"
- **Agent, going up a level:** with one type, repo-registry and the org are the same kind once repo-registry
  graduates, and a kind has one set of policies.
- **Question:** Is that the intent: governance/graduated carries the org policies and the repository policies
  together? (Options: yes, one set / no, rethink.)
- **Answer (mzargham, typed by agent):** "agree but let's be clear that for now we're still in sandbox for
  repo-registry and we will transition to incubating if the maintainers buy and in and work together to get it
  calibrated. we wont switch it to graduate until the repo-registry is accepted as the canonical source"
- **Outcome:** OD1's earlier answer ("Its own type") is replaced. One governance type: the org is
  governance/graduated, repo-registry governance/sandbox, and governance/graduated carries both sets of policies.
  repo-registry stays in sandbox; incubating needs the maintainers' buy-in and calibration; graduated needs its
  acceptance as the canonical source. The `organization` type default is dropped.

## Packaging of the attestations change

- **Supervisor (mzargham, typed by agent):** the attestations change (a reserved YAML file in the repository root,
  a pointer in README, attestations bound to the release commit) "needs to land before we ship to open-mbee (wp5)".
- **Question:** Where should it be scoped? (Options: separate package / fold into WP4c.)
- **Answer (mzargham, typed by agent):** "Separate package"
- **Outcome:** WP4d, scoped after WP4c. WP5 resumes after both.

## OD3 — The Agent's defaults

- **Question:** Approve the Agent's defaults, revised for one governance type, as one item?
- **Answer (mzargham, typed by agent):** "Approve all"
- **Outcome:** Approved as written.

## OpenSSF as a core citation *(raised by the supervisor while WP4d was scoped)*

- **Supervisor (mzargham, typed by agent):** "i think we also elevate OpenSSF to a primary source since we use it
  explicitly for our lifecycle model"
- **Question:** Where should that change be scoped? (Options: fold into WP4c / fold into WP4d / separate package.)
- **Answer (mzargham, typed by agent):** "Fold into WP4c"
- **Outcome:** WP4c, not yet approved, is revised on its scope branch: G4, D-5 and R-8 make OpenSSF a core citation
  alongside CISA and NIST; meta-rule 7 also requires `cites.openssf` *(default)*. CNCF and ISO stay secondary.
- **Question:** With OpenSSF core, policy meta-rule 7 also requires `cites.openssf`, and CNCF stays secondary. Approve
  this new default?
- **Answer (mzargham, typed by agent):** "Approve"

## Acceptance review — observations

- **Question:** Every deliverable and requirement is met. Five observations, none affecting good enough or a
  non-goal (D-5 not named in good enough; supporting changes; lifecycle-stage-map unchanged; the org carries
  repository policies, read by WP6; a merge conflict for WP5). Accept these as is, or pick any to act on?
- **Answer (mzargham, typed by agent):** "Accept as is"
- **Outcome:** All five accepted as is. See [WP4c-review.md](WP4c-review.md).

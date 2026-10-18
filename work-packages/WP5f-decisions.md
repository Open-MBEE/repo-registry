# WP5f — Decision records (gathered before the scope)

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's.

## Why this package exists

- **Supervisor (mzargham, typed by agent), on the status pull request after WP5e (#13):** "i think the status PR should
  also surface explicitly a new roadmap item we need to establish owners and maintainers policies first so we can
  determine who the owners and maintainers are since the other policies are governed by that group."
- **Supervisor (typed by agent):** "this addition makes this its own proper work package since we're introducing a
  roadmap item we've identified as critical path"
- **Supervisor (typed by agent):** "my maintainers list is not only provisional its really more of a placeholder. we
  also need to determine who the actual owner should be and make sure its a small set (which may mean pruning owners
  and populating maintainers)"
- **Outcome:** A work package of its own, on the critical path, ahead of WP6. The roadmap item was taken back out of
  the status pull request (#13, reverted there); this package's scope pull request adds it. The named maintainers in
  `data/maintainers.yaml` are a placeholder, not a proposal.

## OD1 — Who decides the first owners and maintainers

- **Question:** Who decides the first owners and maintainers? (The group that will approve everything else doesn't
  exist yet, so someone bootstraps it.) (Options: the supervisor / the current owners / with NumFOCUS.)
- **Answer (mzargham, typed by agent):** "in the end i suspect chris and robert will decide since they are the
  cofounders but there is a good chance i am on the hook for reflecting what they decide in this repo. knowing them it
  emerge from a loose consensus of the most active contributors/informally defined leadership group"
- **Outcome:** The co-founders decide, likely from a loose consensus of the most active contributors and the
  informally defined leadership group; the supervisor records their decision in this repository. This package prepares
  what they need to decide (the policies, and a decision brief), and records the decision; it doesn't make it.

## OD2 — The owners who are not kept

- **Question:** What should happen to the owners who are not kept (16 of 18, if the set is 2 or 3)? (Options: become
  members / leave the organization / person by person.)
- **Answer (mzargham, typed by agent):** "Become members"
- **Outcome:** Owners who are not kept become members of the organization (and maintainers, where chosen), keeping
  their access through teams.

## OD3 — Carrying out the owner changes

- **Question:** Does this package carry out the owner changes in the organization, or only decide and plan them?
  (Options: plan only / carry it out.)
- **Answer (mzargham, typed by agent):** "record first. determine implementation of the changes of control later"
- **Outcome:** This package records the decision (who the owners and maintainers are meant to be). How and when the
  changes of control are carried out in the organization, including a transition plan, is decided later, in another
  package. Until then the organization's actual owners stay as they are, and `org-few-owners` stays red (the error
  signal).

## OD4 — What qualifies a maintainer

- **Question:** What qualifies a maintainer, beyond the maintainer policy as written? (Options: policy as is / plus
  recent activity / plus verification for every maintainer.)
- **Answer (mzargham, typed by agent):** "Policy as is"
- **Outcome:** The maintainer policy as written (`docs/maintainer-policy.md`) defines who qualifies; nothing is added.

## OD5 — The Agent's defaults

- **Question:** Approve the Agent's defaults as one item: (1) the names; (2) the agent writes nothing to the
  organization; (3) the roadmap change rides with this scope pull request; (4) the maintainer policy only records how
  the first owners and maintainers were chosen; (5) the decision brief draws candidates only from public activity and
  never marks anyone's membership or role?
- **Answer (mzargham, typed by agent):** "the decision brief is not responsible for deciding anything about who is an
  owner or maintainer. anything currently in this repo is treated as demonstrative (although drawn from data with
  intent to be realistic). this PR also needs to include its own status update so we don't have a one pr lag"
- **Outcome:** Defaults 1 to 4 approved. Default 5 changed: the brief is a factual summary of public activity for the
  co-founders, with no recommendation, ranking or proposed names. Everything now in the repository, including
  `data/maintainers.yaml`, is demonstrative: drawn from data, meant to be realistic, not a decision. This scope pull
  request carries its own status update.

## The decision brief's form *(a follow-up on OD5)*

- **Question (the agent's clarification):** Should WP5f produce a decision brief for the co-founders at all? (Options:
  keep it, factual / drop it.)
- **Answer (mzargham, typed by agent):** "we're showing the shape of the decision brief with a hypothetical but being
  clear is not the proposed decision just the shape."
- **Outcome:** The brief shows its shape with a hypothetical example, labelled throughout as hypothetical: not the
  proposed decision, and naming no real person as an owner or maintainer. The co-founders' actual decision is recorded
  separately, by the supervisor (D-3).

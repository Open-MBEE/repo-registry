# WP5d — Decision records (gathered before the scope)

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's.

## Why this package exists

- **Supervisor (mzargham, typed by agent):** "where i need to get to close out work for today. i need a list of repos
  mapped to their kind and tier. and i need the list off policies mapped to when (kind and tier) they are in effect.
  together these two tables along with the taxonomy (which defines what the kinds and tiers mean, with heuristics for
  when and how to assign them), summarize the model. i need a clear concise description of these things to support
  the maintainer review and revise cycle required to advance our roadmap. i want you to plan a work package that aims
  at getting me these materials into an easy to review format that. (eg markdown tables with links that can easily be
  navigated in the github web app). i know there may be tasks we need to do before we can do that but at this point i
  want you working backwards from that goal so we can get to something sharable today"

## Where the review pack is published

- **Question:** Where should the maintainer review pack (taxonomy, repositories, policies) be published, so it can be
  read and navigated in GitHub's web app? (Options: GitHub wiki / dated docs/review/ / unmerged review PR.)
- **Answer (mzargham, typed by agent):** "GitHub wiki"
- **Outcome:** The pack is published to this repository's wiki: the first live CD step (writes to this repository
  only), pulling part of WP7 forward.

## How the wiki is published

- **Question:** How is the wiki published in WP5d? (Options: "You run it, today": live mode renders and pushes the
  wiki with the supervisor's git credentials, only from a main that validates; CI automation waits for WP7 / "CI with
  a secret": a fine-grained write token as a repo secret.)
- **Answer (mzargham, typed by agent):** "You run it, today"
- **Outcome:** The supervisor runs the live publish himself, from a validated `main`; automating it in CI waits for
  WP7.

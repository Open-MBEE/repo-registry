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

## Scoping (after WP5c)

- **Supervisor (mzargham, typed by agent):** "green and merged what's net" (WP5c accepted, 42ecec0; scope WP5d next).

## OD1 — How a maintainer asks for a change

- **Question:** After reading the review pack on the wiki, how does a maintainer ask for a change (the
  review-and-revise cycle)? (Options: an issue / a pull request / both.)
- **Answer (mzargham, typed by agent):** "A pull request"
- **Outcome:** A change is a pull request to the model file. Every page links to the file that holds what it shows,
  with GitHub's edit link.

## Sources pages *(raised by the supervisor, answering the defaults question)*

- **Supervisor (mzargham, typed by agent):** "i want make sure we also have clear mapping back to the cited sources. do
  we need a polices by sources table and pages for our sources too. i think this goes a long way to justify our
  choices. and invites maintainers to become informed before going to hard with alternative suggestions without
  first understanding where the policies came from"
- **Outcome:** Added as G6, D-6 and R-7: a Sources page, one page per source with each item's adopting policies or
  departure reason, and each policy's citations linked both ways. The defaults are put again as one item.

## OD2 — The Agent's defaults

- **Question:** With the sources added, approve the defaults (the wiki pages, including Sources and Source-<source>;
  repositories grouped by kind; a policy's tiers from its kinds; the publish commit message; the first wiki page
  created by the supervisor) as one item?
- **Answer (mzargham, typed by agent):** "Approve all"
- **Outcome:** Approved as written.

## Approval *(a verbal approval, in place of the merge, while the runner queue waited)*

- **Supervisor (mzargham, typed by agent):** "i want to merge the PR but its stuck in the queue for a runner again.
  last time it took over 30 min. since all we did was write a scope of work, not edit any content i want you to start
  work on my verbal approval so we don't need to wait on a runner"
- **Outcome:** WP5d's scope (`wp5d-scope`, the content of PR #10) is approved by this statement; execution starts on
  `wp5d-work`, branched from the scope. PR #10 was then merged by the supervisor (fa3cf16), the GitHub record of the
  same approval; `wp5d-work` was rebased onto it.

## WP7 is the compliance dashboard *(raised by the supervisor during execution; documents only)*

- **Supervisor (mzargham, typed by agent):** "i'd also like this PR to include some documentaiton updates in the repo
  since wp7 was the wiki, that now needs to indicate extending the wiki with dashboard functionality aware of
  compliance with controls state. the part we're building now describes the policies so the maintainers can agree on
  what the taxonomy and policies should be. the later wp7 includes status information used to help bring us into
  demonstrable compliance with our policies. that is different work, though it builds on the glossary since the this
  wp5d will determine the what and why of compliance. even if it doesn't provide the current snapshot and how to get
  into compliance we'll have later"
- **Outcome:** Carried under D-5 (the documents and status). WP7 is described as the compliance dashboard: the wiki
  extended with each repository's status against the controls and how to come into compliance, built on WP5d's pack
  (the what and why). Changed: `docs/current-state.md` (the wiki row, the packages table, the architecture row),
  `docs/status.md` (the breakdown, next step) and the README. The approved scopes, the decision records and the DRAFT
  design documents are left as they are.

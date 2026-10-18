# WP5d — Scope of work: the maintainer review pack, on the wiki

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | [Open-MBEE/repo-registry](https://github.com/Open-MBEE/repo-registry), and its wiki |
| **Approval record** | mzargham's merge, with a merge commit, of the pull request that adds this document into `main` (WP5 OD3) |
| **Acceptance record** | mzargham's merge, with a merge commit, of the delivery pull request into `main`, and the first publish of the wiki, run by him |

## Purpose

The supervisor: "i need a list of repos mapped to their kind and tier. and i need the list off policies mapped to when
(kind and tier) they are in effect. together these two tables along with the taxonomy (which defines what the kinds
and tiers mean, with heuristics for when and how to assign them), summarize the model. i need a clear concise
description of these things to support the maintainer review and revise cycle required to advance our roadmap ...
markdown tables with links that can easily be navigated in the github web app ... so we can get to something sharable
today" ([WP5d-decisions.md](WP5d-decisions.md)).

He decided where and how: this repository's GitHub wiki, published by him from a validated `main` ("You run it,
today"). The wiki is a view plane (WP5b): rendered from the model, never edited by hand, and overwritten by each
publish. This is the first live CD step; until now the controller has run in demo mode only (WP5b OD5).

## Goals

- G1. **The taxonomy, in plain words:** every type, stage and tier, and every kind with its meaning, its tier, and how
  a repository gets it: the rules' heuristics in words, a type topic, or a maintainer's decision.
- G2. **The repositories:** every repository with its kind, tier and the source of its kind, linked to the repository
  on GitHub and to its kind on the taxonomy page.
- G3. **The policies:** every policy with the kinds and tiers it is in effect for, linked to its SOP page.
- G4. **Shareable today:** the pages on this repository's wiki, navigable in the GitHub web app, published by the
  supervisor from a validated `main`, each page saying which commit it was rendered from.
- G5. **A review-and-revise cycle:** the pack says how a maintainer asks for a change (OD1).
- G6. **Where the policies came from** *(raised by the supervisor)*: every policy traced to its cited sources, and
  every source item to the policies that adopt it or the reason we departed from it ("this goes a long way to justify
  our choices. and invites maintainers to become informed before going to hard with alternative suggestions").

## Non-goals

- Publishing from CI (WP7, with a write credential); issues in other repositories (WP6).
- Editing the wiki by hand: every publish replaces it.
- Changing any kind, policy or taxonomy rule: the pack shows the model as it is.
- The engine's measured compliance (colors per repository): WP6. The pack shows what applies, not whether it is met.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | A plain-language `explain:` line for every signal in `data/taxonomy/kinds.yaml`, so each kind's rule renders in words | G1 |
| D-2 | The wiki pages, rendered by `scripts/wiki.py` *(default)*: Home (the index, and how to propose a change by a pull request, OD1), Taxonomy, Repositories, Policies, one SOP page per policy, and a sidebar; each row links to the model file that holds it | G1–G3, G5 |
| D-3 | Live mode: `uv run python scripts/render.py --mode live` publishes the wiki pages to `repo-registry.wiki.git`, only from a clean `main` equal to `origin/main` that validates; demo mode renders the same pages into `build/demo/wiki/` | G4 |
| D-4 | Tests: every repository, kind and policy appears; every wiki link resolves within the pages; live mode refuses an unvalidated, dirty or non-main tree; the pages render the same twice | G1–G4 |
| D-5 | The documents and status, in the same pull requests | G4 |
| D-6 | The sources: a Sources page (each core and secondary source, its role, the version read, a link), one page per source (each item with the policies that adopt it, or the departure and its reason), and each policy's citations on the Policies page, linked both ways | G6 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The Repositories page lists every repository once, with its kind, tier and source, and links to it on GitHub and to its kind. | A test against the kind list |
| R-2 | The Policies page lists every policy with the kinds, and the tiers of those kinds, it is in effect for, and its rule in words; each links to its SOP page. | A test against the applicability view |
| R-3 | The Taxonomy page defines every type, stage, tier and kind, and gives each kind's heuristics in words, from the rules. | A test: every kind and signal appears; inspect the wording |
| R-4 | Every link between wiki pages resolves, every page names the `main` commit it was rendered from and says PROVISIONAL, and every row links to the model file that holds it (OD1). | A test |
| R-5 | Live mode writes only to this repository's wiki, and refuses unless the tree is a clean `main` equal to `origin/main` and `scripts/validate.py` passes. | A test of the refusals; the first publish, run by the supervisor |
| R-6 | Nothing in the model changes. | The full suite; `scripts/validate.py` |
| R-7 | Every policy's citations link to their source pages, and every item of every cited source appears on its page with the policies that adopt it or its departure reason (policy meta-rules 8, 9). | A test against `data/sources/`, `_departures.yaml` and the policies |

## Definition of good

- A maintainer opens the wiki, and in a few minutes knows what kinds and tiers mean, what each repository is and why,
  what each policy asks of it, and how to ask for a change.

## Definition of good enough

- D-1 to D-6 exist, every requirement passes its check, and the wiki has been published once from `main`.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- Pages: `Home`, `Taxonomy`, `Repositories`, `Policies`, `SOP-<policy-id>`, `Sources`, `Source-<source>` and `_Sidebar`, as GitHub wiki Markdown
  with links of the form `[text](Page#anchor)`.
- Repositories are grouped by kind on the Repositories page, with the unclassified ones last and their reasons; the
  pilot is marked.
- A policy's tiers are the tiers of the kinds it is in effect for; its rule in words comes from its applies-if rule.
- The live publish commits with the message "Publish from <main commit>" and pushes; nothing else is written.
- The prerequisite: the supervisor creates the wiki's first page once in the web app (GitHub creates the wiki
  repository only then).

## Open decisions (for the supervisor)

- **OD1.** How a maintainer asks for a change. *Decided: a pull request to the model file. Every page links to the
  file that holds what it shows (the kind list entry, the kind in `kinds.yaml`, the policy's file), with the GitHub
  edit link, so a change starts from the page.*
- **OD2.** The Agent's defaults. *Decided: approved, with the sources pages (G6, D-6, R-7) raised by the supervisor.*

None remain open. Every item was resolved through the decision loop: 4 decided (two before the scope, OD1, OD2),
0 deferred, 1 raised (the sources pages). The records are in [WP5d-decisions.md](WP5d-decisions.md).

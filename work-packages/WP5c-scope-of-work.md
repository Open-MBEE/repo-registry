# WP5c — Scope of work: taxonomy refinements from the fit analysis

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | [Open-MBEE/repo-registry](https://github.com/Open-MBEE/repo-registry) |
| **Approval record** | mzargham's merge, with a merge commit, of the pull request that adds this document into `main` (WP5 OD3) |
| **Acceptance record** | mzargham's merge, with a merge commit, of the delivery pull request into `main` (WP5 OD3) |

## Purpose

The supervisor: "my goal now is to refine the taxonomy based on what we learned in the build so far". WP4's fit
analysis ([fit-analysis.md](../docs/fit-analysis.md), its recommendations 1 to 5) found where the draft taxonomy fits
the org's repositories badly: 45 of 182 are unclassified (25 forks, 14 live repositories with no type signal, 6
archived ones with no type), and `.github` is classed as media. The supervisor's answers, given while WP5b was scoped
([WP5c-decisions.md](WP5c-decisions.md)), set the direction:

- **Forks:** "assess whether forks are research ... explorations of integration points ... they could also be media if
  they are primarily works of models rather than forks of tools. its probably worth inspecting the upstream, and our
  diff from the upstream to help classify".
- **Topics:** "introduce github topics as a means of declaring type".
- **Precedence:** "the inference produces a candidate not a decision. tagging repos using topics should supersede
  inference. so the order of priority is inferred->topic->maintainer merged commit."
- **Examples:** "they could appear as either media or research depending on whether the purpose of doing it to learn
  for ourselves or communicate to others".
- **Archived with no type:** "ok" (revisited at OD3). **`.github` as governance:** "yes".

WP5b made the repository a model with declared tables; this package changes the taxonomy's rules and the kind list
through that model, so every change is checked as it lands.

## Goals

- G1. **Precedence is in the model:** a repository's kind comes from a maintainer's merged decision if there is one,
  else from its declared GitHub topic, else from inference, and the source of each kind is visible (OD1).
- G2. **Type can be declared with a GitHub topic,** by each repository's code owners, with a rule for a missing or
  conflicting topic.
- G3. **Fewer repositories unclassified, for stated reasons:** forks classified by inspecting their upstream and our
  diff from it (OD2); live repositories with no type signal given better signals; archived repositories with no type
  stay unclassified, with their reason (OD3).
- G4. **`.github` is governance** (OD4).

## Non-goals

- Writing to any other repository: no topic is set on a repository by this package. The topic convention is published
  for code owners to adopt; until they do, inference is the only source besides maintainer decisions.
- New types, stages or tiers, or new policies. A new kind only if a decision above needs one.
- Approving any kind: the kind list stays provisional until the maintainers' approval 4 (WP0).
- Changing the kept pilot list (`data/pilot.yaml`, a model table). The rule's proposal view may change; the kept list
  changes only by its own governed pull request.
  *(amended at the review, G-1: the mirror `staged-recipes-opensysml` moves from the pilot to the exclude list, as
  OD2 says; the supervisor's "Fix before acceptance". Recorded in WP5c-decisions.md.)*
- The engine (WP6) and the wiki (WP7).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The precedence in the model (OD1), declared in `data/schema/model.yaml`, with the kind list and assignments reshaped to fit, and the effective kind rendered with its source | G1 |
| D-2 | The topic convention: the topics that declare a type, the rule for none or more than one, in `data/taxonomy/kinds.yaml` and `docs/kind-list-format.md`; topics read from the snapshot | G2 |
| D-3 | The fork assessment: a read-only read of each fork's upstream and our diff from it (`data/snapshots/<snapshot>/forks.json` *(default)*), and the rule that classifies a fork from it (OD2) | G3 |
| D-4 | Better signals: `example` as well as `examples`, which alone decides no type; notebook-only and model-only repositories as media unless a research word applies; archived repositories with no type stay unclassified (OD3) | G3 |
| D-5 | `.github` as governance/graduated (OD4), recorded as a maintainer decision (`source: maintainer`) | G4 |
| D-6 | A fit report rendered as a view (the counts before and after, by reason), the documents and status updated in the same pull requests, and a record of the change to the taxonomy, `work-packages/WP1-amendment-6.md` *(default)* | G1–G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every repository's effective kind follows the precedence: maintainer decision, then topic, then inference, and the view states which one gave it. | A test with a repository at each level, and one with two |
| R-2 | A repository with no type topic, or more than one, takes its kind from the next source down, and the view says why. | A test |
| R-3 | Every fork is classified from its upstream and our diff, or unclassified with the reason the assessment gives. | A test over the fork assessment; inspect the rendered fit report |
| R-4 | The fork read and the topic read only read GitHub (GET), and are stored beside the snapshot. | A test on the reading script, as WP1 R-1 |
| R-5 | Every change to a kind is a change of a candidate (inference or topic); no maintainer decision is changed except `.github` (OD4) by an assignment. | Compare the kind list's decisions before and after |
| R-6 | The taxonomy and the model still hold: every meta-rule, every key and join, every view renders the same twice. | `uv run python scripts/validate.py`; the full test suite |
| R-7 | The rendered fit report gives the unclassified count before and after, by reason. | Render; inspect |

## Definition of good

- A maintainer reading a repository's kind can see where it came from and what would change it: a merged decision,
  a topic its code owners set, or the rules' best guess, with the reason when there is none.

## Definition of good enough

- D-1 to D-6 exist, and every requirement passes its check.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- **Topics:** one topic per type, `openmbee-tool`, `openmbee-media`, `openmbee-research` and `openmbee-governance`.
  A repository can carry up to 20 topics on GitHub; exactly one of these declares its type. None, or more than one,
  declares nothing, and the view says which. A topic declares the type only; the stage still comes from the rules
  (for a tool, its releases) or a decision.
- **Examples:** the word "example" alone decides no type, because purpose decides it ("to learn for ourselves or
  communicate to others"); such a repository gets a candidate only from other signals, else is unclassified with that
  reason, and its code owners are pointed to the topic.
- **Refreshing candidates:** a rendered view lists the `inferred` and `topic` entries the rules or topics would change
  today; applying it is an ordinary pull request. Today's 182 entries start as `inferred`, except the assigned ones
  (`maintainer`), which absorb `data/assignments.yaml`'s decisions as their source.
- **Fork reads:** one `GET /repos/{parent}/compare/{base}...Open-MBEE:{head}` per fork (ahead, behind, the files we
  changed), stored in `forks.json` beside the snapshot with when it was read; the rule reads those as declared derived
  columns (WP5b F-15).
- The Python patch release is pinned in `.python-version` (WP5's observation 7).
- Each step lands as a pull request carrying its status update.

## Open decisions (for the supervisor)

- **OD1.** Where the precedence lives. *Decided: source per entry. The kind list keeps every repository; each entry
  has a `source`: `inferred`, `topic` or `maintainer`. Only a maintainer's merged change sets `maintainer`, and the rules
  and topics never change an entry whose source is `maintainer`.*
- **OD2.** A fork with no commits of ours ahead of its upstream. *Decided: a mirror. It stays unclassified, with the
  reason "a copy of <upstream> with no changes of ours", and is excluded from the pilot with that reason. A fork with
  changes of ours is research (an exploration of how tools work together), or media where the files we changed are
  mostly models.*
- **OD3.** An archived repository with no type signal. *Decided: it stays unclassified, with its reason. (This
  replaces the earlier "ok" to WP4's recommendation 4.)*
- **OD4.** `.github`'s stage. *Decided: graduated. It is part of the org's administration, so governance/graduated
  (high): it takes the org policies and the strict repository set, recorded as a maintainer decision.*
- **OD5.** The Agent's defaults. *Decided: approved.*

None remain open. Every item was resolved through the decision loop: 5 decided, 0 deferred, 0 raised. The records are
in [WP5c-decisions.md](WP5c-decisions.md).

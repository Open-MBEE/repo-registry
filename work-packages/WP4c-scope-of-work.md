# WP4c — Scope of work: the governance kinds

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `repo-registry` (local; WP5, the move, is paused on `wp5-work` until this package is accepted) |
| **Approval record** | mzargham's `git merge --no-ff -m "<message>"` of the scope branch into `main` ([AGENTS.md](../AGENTS.md)) |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` ([AGENTS.md](../AGENTS.md)) |

## Purpose

The supervisor, reading the policy applicability table: "i am a bit confused why governance graduated has so many
fewer policies than governance sandbox. something feels off. it seems like sandbox should have less friction then
graduate to a tightly controlled regime one its canonical".

The cause is in WP1 A2 (WP1-decisions, G-2) and WP1-amendment-2. The governance type covers two different things:
`repo-registry`, a repository (governance/sandbox), and the org's administration, which is not a repository
(governance/graduated). The stage axis is therefore used to say *which thing is governed*, not *how mature it is*.
Each repository policy excludes governance/graduated by name, so that it doesn't apply to the org. That leaves the org
5 policies, and `repo-registry` 13. Two consequences:

- When `repo-registry` becomes canonical (R3) and graduates, it would **lose** every repository control and take on
  the org policies instead.
- Sandbox elsewhere means light friction, but governance/sandbox is at the high tier.

The supervisor's model (OD1): the org and `repo-registry` are the same type, governance, at different stages. The
org is graduated; `repo-registry` is in sandbox. So a governance kind carries one set of policies, whatever it is
applied to, and friction rises with the stage: governance/graduated carries the org policies and the repository
policies together. Each check reads the thing it is about: the org's settings for the org, the repository's
settings for `repo-registry`.

`repo-registry` stays in sandbox for now. In the supervisor's words, it moves to incubating "if the maintainers buy
and in and work together to get it calibrated", and "we wont switch it to graduate until the repo-registry is accepted
as the canonical source".

## Goals

- G1. **Friction rises with the stage for governance**, as for every other type: governance/sandbox lightest,
  governance/graduated tightest (OD2).
- G2. **The stages are all there:** governance/incubating exists, for `repo-registry` while it is calibrated, though
  nothing has it today.
- G3. **governance/graduated carries one set:** the org policies and the repository policies together (OD1), so the
  org keeps its org policies and `repo-registry` takes everything when it graduates. No policy names a governance kind
  to exclude the org.

## Non-goals

- Any other kind's outcome: every repository other than `repo-registry` keeps its kind, and every policy applies to the
  same tool, media and research kinds as now.
- New policies, or changes to a policy's checks, SOP body or citations. Only applies-if rules, and the SOP lines that
  state them, change. How a repository policy's check reads the org (for example an org ruleset for `change-review`)
  is for the engine (WP6), not this package.
- Moving `repo-registry` to another stage. It stays in sandbox. Incubating needs the maintainers' buy-in and
  calibration; graduated needs its acceptance as the canonical source. Both are assignments by the maintainers.
- Raising review friction on this repository before R3 (WP0-decisions "How restrictive this repo is in R1").
- The attestations file (WP4d, scoped separately) and the move to Open-MBEE (WP5, resumed after both).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The taxonomy change in `data/taxonomy/kinds.yaml`: governance/sandbox low (OD2), governance/incubating defined (medium), governance/graduated high, each with a meaning that fits both the org and `repo-registry` | G1, G2 |
| D-2 | The applies-if rules changed in `data/policies/`, and the SOP lines that state them, so that each governance kind carries the policies for its stage, and governance/graduated carries the org policies and the repository policies | G1, G3 |
| D-3 | A WP1 amendment record, `work-packages/WP1-amendment-3.md` *(default)*, stating what A2 and amendment 2 said and what replaces them | G1, G2, G3 |
| D-4 | Everything generated replayed (applicability, license report, pilot, briefing), and the current documents updated (`docs/current-state.md`, `docs/kind-list-format.md`, `docs/lifecycle-stage-map.md`, `docs/roadmap.md` R3, README tiers), with the early DRAFT documents edited in place (as WP4b OD1) | G1, G2, G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The org is governance/graduated and `repo-registry` governance/sandbox; governance/incubating is defined, not omitted. | A test on `kinds.yaml`, `registry.yaml` and `data/assignments.yaml` |
| R-2 | governance/graduated takes the 5 org policies and every repository policy governance/sandbox takes today. | A test on the applicability table |
| R-3 | governance/sandbox maps to low and takes the same policies as tool/sandbox (today `codeowners`, `license-by-type`, `project-files`; OD2). governance/incubating maps to medium and takes tool/incubating's repository policies except `semantic-versioning` *(default)*. No org policy applies to governance/sandbox or governance/incubating *(default)*. | A test comparing the three rows |
| R-4 | No applies-if rule excludes governance/graduated. | A test over the policies |
| R-5 | Every other kind keeps exactly its policies, every other repository keeps its kind, and the pilot and exclude list keep the same repositories. | Compare before and after; the full test suite |
| R-6 | The taxonomy and policy meta-rules still hold (kind-list meta-rule 10, policy meta-rules 1-13). | `python3 scripts/policies.py`; the full test suite |
| R-7 | Every document that states the governance kinds, or their tiers, says the new thing, or is marked superseded with a pointer. | `grep -rn "governance/"` over the docs, inspected; the link check |

## Definition of good

- Someone reading the applicability table sees friction rise with the stage for every type, governance included.

## Definition of good enough

- D-1 to D-4 exist, and every requirement passes its check.
- The table shows governance/sandbox, governance/incubating and governance/graduated with friction rising in that
  order.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- Package name WP4c: it fixes accepted WP1/WP2 work before WP5 resumes. The record of the change is
  `work-packages/WP1-amendment-3.md`, following amendment 2.
- governance/incubating maps to medium, like tool/incubating, and takes the repository policies tool/incubating
  takes, except `semantic-versioning`, which is about a tool's releases.
- The org policies apply only to governance/graduated: the org is the only thing at that stage today, and
  `repo-registry` takes them on only when it graduates.
- governance/sandbox takes only the policies a low-tier sandbox kind takes (OD2). The policies that name
  governance/sandbox today are changed to name governance/graduated instead.
- governance/archived stays omitted.
- After this package is accepted, `main` is merged into `wp5-work` (no rebase, so no commit changes). Any WP5 test
  that uses a governance kind is updated then, as part of WP5.

## Open decisions (for the supervisor)

- **OD1.** How the org and `repo-registry` relate. *Decided: the same type, governance, at different stages. The org
  is governance/graduated and `repo-registry` governance/sandbox, and governance/graduated carries the org policies
  and the repository policies together. (This replaces an earlier answer, "Its own type".)*
- **OD2.** `repo-registry`'s tier before it is canonical (governance/sandbox). *Decided: low, like sandbox tools.*
- **OD3.** The Agent's defaults. *Decided: approved (as revised for one governance type).*

None remain open. Every item was resolved through the decision loop: 3 decided (OD1 revisited once), 0 deferred,
1 raised (governance/incubating, folded into the defaults). The records are in
[WP4c-decisions.md](WP4c-decisions.md).

# WP4e — Scope of work: type and stage in the kind list

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `repo-registry` (local; WP5, the move, waits on `wp5-work` until this package is accepted) |
| **Approval record** | mzargham's `git merge --no-ff -m "<message>"` of the scope branch into `main` ([AGENTS.md](../AGENTS.md)) |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` ([AGENTS.md](../AGENTS.md)) |

## Purpose

The supervisor: "looking at our registry yaml schema it seems strange to me that we're using slash to make kind out
of the repo type and lifecycle stage. this should be type and stage. we can compute kind from it where we need to".

Today each entry in `registry.yaml` (and `data/assignments.yaml`) holds one field, `kind: tool/sandbox`, a string
that joins the two attributes people decide. The model is the other way round: type and stage are the attributes,
and a kind is just the point they name (WP0-decisions, "The model, stated precisely"). This package makes the kind
list hold `type` and `stage`, and computes the kind wherever a kind is needed. It lands before WP5, so the repository
published to Open-MBEE already has the new format.

## Goals

- G1. **The kind list holds what people decide:** each entry has a type and a stage, not a joined string.
- G2. **The kind is computed** from type and stage wherever it is used (applicability, tiers, reports), with no
  change to any outcome.
- G3. **A change of stage is still a one-line diff** (WP0 R-12), for example `stage: sandbox` → `stage: incubating`.

## Non-goals

- Any change of outcome: every repository keeps the same type and stage, every policy applies to the same
  repositories, the pilot and exclude list keep the same repositories, and the license report keeps its colors.
- New types, stages, kinds, tiers or policies.
- The move to Open-MBEE (WP5, resumed after this package).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The new kind-list format: `registry.yaml` and `data/assignments.yaml` entries with `type` and `stage` (per OD1, OD2), with `docs/kind-list-format.md`, its meta-rules and `data/schema/kind-list.schema.yaml` updated | G1, G3 |
| D-2 | The attribute `lifecycle` renamed `stage` in `data/taxonomy/kinds.yaml`, the applies-if rules and the code (OD1); and the code that reads or writes the kind list computes the kind from type and stage: `scripts/recommend.py`, `pilot.py`, `licenses.py`, `briefing.py` and their tests; and, on `wp5-work`, `scripts/validate.py` after the next merge | G2 |
| D-3 | Everything generated replayed, and the documents that show a kind-list entry updated (README, `docs/current-state.md`, SOPs that tell an operator how to read their kind, the DRAFT documents edited in place as WP4b OD1), with a short amendment record, `work-packages/WP1-amendment-4.md` *(default)* | G1, G2 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every entry in the kind list has either `type` and `stage`, or `reason` alone (OD2), and no `kind` field. | A test over `registry.yaml` and `data/assignments.yaml` |
| R-2 | Each entry's type and stage name a defined kind (not an omitted one). | A test; the kind-list meta-rules |
| R-3 | No outcome changes: for every repository, the computed kind equals its kind before the change; the applicability table, pilot, exclude list and license report are unchanged. | Compare before and after; the full test suite |
| R-4 | A change of stage is a one-line diff. | A test, as WP1 R-8 does today |
| R-5 | No document shows the old `kind: type/stage` entry as the format to follow. | `grep -rn "kind: [a-z]*/" ` over the docs, inspected; the link check |
| R-6 | No data file or script names the attribute `lifecycle`; the meta-rules (kind-list meta-rule 10, policy meta-rule 4) read `stage`. | `grep -rn "lifecycle"` over `data/` (except sources) and `scripts/`, inspected; the full test suite |

## Definition of good

- A maintainer reading `registry.yaml` sees, for each repository, its type and its stage as two plain facts, and
  changes either with one line.

## Definition of good enough

- D-1 to D-3 exist, and every requirement passes its check.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- Kinds keep their names (`tool/sandbox`) as computed labels: `data/taxonomy/kinds.yaml` still defines each kind
  under that name with its type, stage and tier, and the applicability table and reports still show kinds by name.
- The org's entry becomes `org: {name, type, stage}`.
- Entries keep their order (sorted by repository name), and an entry's fields are written `type` then `stage`.
- Generated files that show a kind (the pilot, the reports, the briefing) keep showing the computed kind.
- After acceptance, `main` is merged into `wp5-work` again, and WP5's `validate.py` and tests follow the new
  format as part of WP5.

## Open decisions (for the supervisor)

- **OD1.** The name of the stage attribute. *Decided: `stage` everywhere in the data and code (the taxonomy, the
  applies-if rules, the code, the kind list). Prose says "stage", "the lifecycle" or "stage in the lifecycle", as fits.*
- **OD2.** A repository the rules can't classify. *Decided: neither type nor stage, only a `reason`. An entry has
  either `type` and `stage`, or `reason` alone.*
- **OD3.** The Agent's defaults. *Decided: approved.*

None remain open. Every item was resolved through the decision loop: 3 decided, 0 deferred, 0 raised. The records
are in [WP4e-decisions.md](WP4e-decisions.md).

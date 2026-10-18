# WP1 and WP2 — Amendment 5: the model as a database (WP5b)

Made by [WP5b](WP5b-scope-of-work.md), approved by mzargham's merge e219b85. Decisions are recorded verbatim in
[WP5b-decisions.md](WP5b-decisions.md); the findings in [WP5b-audit.md](WP5b-audit.md). This record says how the
formats WP1 (the taxonomy and the kind list) and WP2 (the policies) set have changed.

## The architecture

The supervisor: "think of this as a model view controller architecture ... MVC plus CI/CD allows us to treat the wiki
and issues written as view planes (written as part of CD), the repo itself as the model (including asserting
correctly constructed records and rejecting illformed ones via CI)."

- **Model:** every record is a row of a declared table, in [data/schema/model.yaml](../data/schema/model.yaml): its
  key, its columns and their types, its foreign keys. `scripts/validate.py` enforces the declaration on every pull
  request; `scripts/model.py` is the one place that reads the rows.
- **Views:** never committed (OD4). `scripts/render.py` renders every view deterministically, in demo mode (OD5)
  into `build/demo/`: the applicability table, every SOP, the reports, the pilot proposal and briefing, the basis
  tables and the data-model document. CI uploads them and shows a pull request's effect on them.
- **Two kinds of error (F-16):** a construction error is invalid (`data/controls.yaml` lists the construction controls
  and their tests); a compliance error is the error signal, kept (`data/measured-gaps.yaml`). A capability not built
  yet is forthcoming (`data/forthcoming.yaml`), no longer an "expected gap".

## WP1: the taxonomy and the kind list

| Before | Now | Why |
|---|---|---|
| `kinds:` keyed by the name `tool/sandbox`, each row repeating `type` and `stage` | keyed by type, then stage | OD2: the name is derived shorthand (F-01) |
| `registry.yaml` keyed by repository name, with a `snapshot:` path | keyed by GitHub's repository ID, with `name` as a checked column; the snapshot declared once in `model.yaml` | OD3 (F-03, F-14) |
| `repo-registry` assigned but absent from the snapshot | its ID read into the snapshot's `ids.json`, marked `after_snapshot` | F-04 |
| `data/assignments.yaml` keyed by name | keyed by repository ID, with `name` | OD3 |
| `data/pilot.yaml` generated, storing each member's kind, with `why` | a model table (OD6) keyed by ID, with `name`, `category`, `reason`; no kind | OD6, F-09, F-11 |
| `data/exclude.yaml`: one reason repeated in every row | `default_reason`, and rows that state a reason only when it differs | F-10 |
| `data/pilot-rule.yaml`: must-includes by name; a predicate on `kind` | by repository ID; predicates on `type` and `stage` | OD2, OD3 |
| `data/maintainers.yaml` keyed by login | keyed by GitHub's user ID, with `login` as a column; release authority by repository ID | F-05 |
| `data/expected-gaps.yaml` | `data/forthcoming.yaml` (capabilities not built) and `data/measured-gaps.yaml` (known non-passes, the error signal) | F-16 |
| `data/schema/kind-list.schema.yaml` | `data/schema/model.yaml`, for every table | F-12 |

## WP2: the policies

| Before | Now | Why |
|---|---|---|
| `status` and `provisional_until` in every policy file | once, in `data/policies/_set.yaml` | F-13 |
| `sop:` pointing to a hand-written `docs/sops/<id>.md` | no `sop`; the SOP is rendered from the policy (`scripts/sops.py`), its set-up steps stored as `setup:` | answer 6, F-08 |
| — | `scope: repository` or `org` | the basis tables, rendered (F-08) |
| `license-by-type`'s SOP table and "Applies to" prose written by hand | `license_guidance` and `applies_note` in the policy | answer 6 |
| `_future.yaml`'s `would_strengthen` as prose, with one dangling name | `strengthens: [policy ids]`, a `note`, and `reason` for why | F-06, F-11 |
| The basis review's tables written by hand | rendered from the policies and `data/sources/` (`scripts/basis.py`); ISO clause titles in `data/sources/iso12207-clauses.yaml` (number and title only) | F-08 |
| Reports' `status` meaning a color | `color` | F-11 |

No outcome changed: every repository's kind, every policy's applicability, the pilot, the exclude list and the license
and maintainer reports render exactly as they were before WP5b (WP5b R-8; the comparison is in the review).

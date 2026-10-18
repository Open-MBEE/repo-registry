# WP4e — Review report

| | |
|---|---|
| **Scope of work** | [WP4e-scope-of-work.md](WP4e-scope-of-work.md) |
| **Scope approval verified** | merge commit f405aa4 by Michael Zargham (mzargham), parents f27c41a and 06e8c4e (the `wp4e-scope` tip) |
| **Work reviewed** | `wp4e-work`, commit ac77eaa (`git diff f405aa4...wp4e-work`: 58 files) |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of `wp4e-work` into `main` |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `registry.yaml` and `data/assignments.yaml` entries hold `type` and `stage`, or `reason` alone; `docs/kind-list-format.md` and its meta-rules; `data/schema/kind-list.schema.yaml` (oneOf for the two forms) |
| D-2 | met | `stage` in `kinds.yaml`, every applies-if rule and the code; `recommend.kind_of` computes the kind, used by `recommend.py`, `pilot.py`, `licenses.py` |
| D-3 | met | Generated files replayed; SOPs, `policy-format.md`, `AGENTS.md`, DRAFT `formal-model.md` updated; `work-packages/WP1-amendment-4.md` |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `tests/test_wp4e.py` `test_R1_type_and_stage_or_reason_alone` passes |
| R-2 | met | `test_R2_type_and_stage_name_a_defined_kind` passes |
| R-3 | met | Against f405aa4: every repository's computed kind equals its old kind, and the org's; pilot, exclude list, applicability, license, kind-recommendation and maintainers-match reports identical; `pilot-briefing.md` and `policy-applicability.md` unchanged |
| R-4 | met | `test_wp1` `test_R8_reclassification_is_one_entry` passes: `stage: sandbox` → `stage: incubating` is the only changed line |
| R-5 | met | `grep -rn "kind: [a-z]*/\|kind: unclassified"` over README, AGENTS and `docs/`: no hits; link check passes |
| R-6 | met | `test_R6_the_attribute_is_stage` passes; `python3 -m unittest discover -s tests`: 69 tests, OK (expected failures=2) |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-3 exist, and every requirement passes its check | met | Above |

## Outside the scope

- **Out-of-scope changes:** `docs/status.md` and `docs/current-state.md` (status with the delivery).
- **Non-goals touched:** none. No outcome changed; no new type, stage, kind, tier or policy; nothing about the move.

## Observations (not counted as failures)

1. WP5's `validate.py` (on `wp5-work`) still reads `kind`. As the approved default says, it is updated after the next
   merge of `main` into `wp5-work`, as part of WP5.
2. The status documents were updated as support.
3. The prose keeps "lifecycle stage" where it describes the concept, as OD1 says.
4. With no org assignment (toy taxonomies in tests only), the org entry is written without type or stage.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| Observations 1 to 4, as one item | accept as is | Supervisor: "Accept as is" |

## Recommendation

Recommend acceptance, because every deliverable and requirement is met with evidence, no outcome changed, and the
supervisor accepted the observations as is.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

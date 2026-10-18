# WP4d — Review report

| | |
|---|---|
| **Scope of work** | [WP4d-scope-of-work.md](WP4d-scope-of-work.md) |
| **Scope approval verified** | merge commit e8d085e by Michael Zargham (mzargham), parents f694254 and 69d547f (the `wp4d-scope` tip) |
| **Work reviewed** | `wp4d-work`: a8910cd (delivery) and 5b6bbc8 (fix G-1); this review was rerun in full after the fix |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of `wp4d-work` into `main` |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `docs/attestations-format.md`; `data/schema/attestations.schema.yaml`; reserved file `ATTESTATIONS.yaml` |
| D-2 | met | `docs/policy-format.md`, "Reading a check's result": green, red, yellow, exceptions; release, no-release and archived cases |
| D-3 | met | The 10 SOPs with attested checks show YAML entries for every check and the README pointer; no README block remains |
| D-4 | met | `work-packages/WP0-amendment-3.md`; WP0 "Compliance" and R-13 default amended in place; README operator section, `current-state.md` (new Attestations row), `policy-format.md`; DRAFT `design.md`, `requirements/interfaces.md`, `testing-and-demonstration.md` |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `tests/test_wp4d.py` `test_R1_example_meets_the_schema` passes; the entry names policy, check, attested_by, date, release |
| R-2 | met | `test_R2_every_attested_check_can_be_answered` passes for all 14 attested checks |
| R-3 | met | Inspected: green (entry naming the release, last change by a code owner), red (missing, other release, bad schema, not a code owner), yellow (can't read), no release (default branch, no expiry), archived (final commit, after G-1), exceptions green marked; matches WP0 R-13's colors |
| R-4 | met | `test_R4_no_document_says_attest_in_the_readme` passes; the grep finds only amended history in WP0 |
| R-5 | met | Against e8d085e: applicability, kind list, pilot, exclude list and license report identical; `python3 scripts/policies.py` replays with no diff; 65 tests OK (expected failures=2) |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-4 exist, and every requirement passes its check | met | Above |

## Outside the scope

- **Out-of-scope changes:** `docs/status.md` (status with the delivery).
- **Non-goals touched:** none. No checker or live reads (WP6); no new attested check or changed question; nothing
  written to another repository.

## Observations (not counted as failures)

1. 10 SOPs were updated, not the 9 the scope names: `maintainers-match` is included, answered in this repository's file.
2. `docs/status.md` was updated as support.
3. This repository has no `ATTESTATIONS.yaml` yet; the org's attestation is an owner's act, left for later.
4. The schema test uses a small validator for the JSON Schema subset used, so no dependency is added.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1: an archived repository with releases would stay red, since its last attestation follows its last release | fix before acceptance | Supervisor: "Fix before acceptance". Fixed in 5b6bbc8; review rerun |
| Observations 1 to 4, as one item | accept as is | Supervisor: "Accept as is" |

## Recommendation

Recommend acceptance, because every deliverable and requirement is met with evidence after the G-1 fix, no outcome
changed, and the supervisor accepted the observations as is.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

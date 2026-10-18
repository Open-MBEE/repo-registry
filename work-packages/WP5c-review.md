# WP5c — Review report

| | |
|---|---|
| **Scope of work** | [WP5c-scope-of-work.md](WP5c-scope-of-work.md) |
| **Scope approval verified** | mzargham's merge of [#8](https://github.com/Open-MBEE/repo-registry/pull/8), 8197d77 (parents 9e14099 and 8a12fb3) |
| **Work reviewed** | `wp5c-work` at 2ae87fc, with this report; the review was rerun in full after the G-1 fix |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's merge, with a merge commit, of the delivery pull request into `main` |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | Each kind-list entry has `source` (inferred, topic, maintainer) and, for a maintainer entry, `decision`; `data/assignments.yaml` folded in; declared in `data/schema/model.yaml`; the refresh view and `scripts/refresh_kind_list.py` |
| D-2 | met | `type_topics` in `data/taxonomy/kinds.yaml`; `declared_type` derived by `recommend.derive`; documented in `docs/kind-list-format.md`, README and AGENTS.md |
| D-3 | met | `scripts/fork_snapshot.py`, GET only; `data/snapshots/2026-10-18/forks.json` (25 forks, all readable); the fork signals in `kinds.yaml` |
| D-4 | met | `example` as well as `examples`, deciding no type alone; notebook-only and model-only as media; archived with no type unclassified |
| D-5 | met | `.github` governance/graduated, `source: maintainer`, with its decision (OD4) |
| D-6 | met | `scripts/fit.py` (the fit report view); docs and status updated; [WP1-amendment-6.md](WP1-amendment-6.md) |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `test_R1_maintainer_then_topic_then_inference` passes |
| R-2 | met | `test_R2_no_topic_or_two_topics_declare_nothing` passes |
| R-3 | met | `test_R3_forks_are_classified_from_their_upstream` passes: 23 mirrors unclassified (22 already excluded, the 23rd moved there at G-1); `IAlf` research; `sysmlv2-rdf-ontology` media (4 of 6 changed files are models) |
| R-4 | met | `test_R4_the_fork_read_only_reads` passes |
| R-5 | met | Against 8197d77: 7 kinds changed: `.github` (OD4, a decision) and 6 candidates newly classified; `test_R5_rules_never_change_a_maintainer_entry` passes, and the refresh is empty after it was applied |
| R-6 | met | `scripts/validate.py`: "valid: every table meets data/schema/model.yaml, and every view renders, the same twice"; 101 tests OK (expected failures=1); `scripts/audit.py`: all 16 findings return none; privacy scan clean |
| R-7 | met | `test_R7_fit_report_counts_unclassified_by_reason` passes; unclassified 45 before, 39 after |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-6 exist, and every requirement passes its check | met | Above |

## Outside the scope

- **Out-of-scope changes:** the CI view-diff fix (8a12fb3) rode with the scope PR and is on `main`; `WP5d-decisions.md`
  recorded early, for the next package.
- **Non-goals touched:** the kept pilot list, by one row, at G-1, with the supervisor's amendment of that non-goal.

## Observations (not counted as failures)

1. `mms-autocref` and `mms-rdf` (notebook demos of a tool) become media, by the notebook-only rule.
2. `.github` as governance/graduated now carries 18 policies, at the high tier.
3. The pilot rule's forks category still says forks are "kept unclassified to show the taxonomy has no kind"; its
   proposal view now differs from the kept list.
4. The fork read checks the default branch only.
5. Locally, `.python-version` 3.10.22 needs `brew upgrade uv` (this machine's uv 0.10.9 knows up to 3.10.20); CI's
   uv already has it.
6. The license view now covers the 6 newly classified repositories (green 77 → 83).

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1: a mirror (`staged-recipes-opensysml`) in the kept pilot | fix before acceptance | Supervisor: "Fix before acceptance". Moved to the exclude list (2ae87fc); the non-goal amended for it; review rerun |
| Observations 1 to 6, as one item | accept as is | Supervisor: "Accept as is" |

## Recommendation

Recommend acceptance, because every deliverable and requirement is met with evidence after the G-1 fix, the only kind
changes are the decided `.github` and six newly classified candidates, and the supervisor accepted the observations
as is.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

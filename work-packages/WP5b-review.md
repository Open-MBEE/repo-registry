# WP5b — Review report

| | |
|---|---|
| **Scope of work** | [WP5b-scope-of-work.md](WP5b-scope-of-work.md) |
| **Scope approval verified** | mzargham's merge of [#5](https://github.com/Open-MBEE/repo-registry/pull/5), e219b85 (parents 6938aa5 and c96ca98) |
| **Work reviewed** | `wp5b-work` at d231e85, [#6](https://github.com/Open-MBEE/repo-registry/pull/6), with this report added |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's merge, with a merge commit, of [#6](https://github.com/Open-MBEE/repo-registry/pull/6) into `main` |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `data/schema/model.yaml` declares 38 tables (key, columns, foreign keys), with `scripts/model.py` reading each; `docs/data-model.md` is rendered from it (a view) |
| D-2 | met | `work-packages/WP5b-audit.md`, 16 findings, each reproducible with `scripts/audit.py`; every finding disposed at the check-in ([WP5b-decisions.md](WP5b-decisions.md)) |
| D-3 | met | Kinds keyed by type, then stage; repositories by GitHub ID (`ids.json`), people by user ID; no derived value stored (record: [WP1-amendment-5.md](WP1-amendment-5.md)) |
| D-4 | met | `scripts/render.py` (demo mode) renders every view into `build/demo/`; the reports, generated documents and 21 hand-written SOPs are removed; SOPs (`sops.py`) and the basis tables (`basis.py`) are rendered; CI renders, uploads the views and writes the view diff |
| D-5 | met | `scripts/validate.py` enforces `model.yaml`; one test per constraint (`tests/test_wp5b.py`, `data/controls.yaml`); trial [#7](https://github.com/Open-MBEE/repo-registry/pull/7) |
| D-6 | met | README, AGENTS.md, `docs/current-state.md`, `docs/status.md`, `kind-list-format.md`, `policy-format.md`, the basis review, and the record [WP1-amendment-5.md](WP1-amendment-5.md) |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `test_R1_every_file_has_one_class` passes; no rendered view is tracked (it found, and the build untracked, a committed `.pyc`) |
| R-2 | met | `test_R2_every_table_has_a_key_and_declared_columns` passes; `validate.py` checks every row against its table |
| R-3 | met | `uv run python scripts/audit.py`: every finding returns 0 rows; `test_R3_every_audit_finding_is_fixed` passes |
| R-4 | met | `uv run python scripts/validate.py`: "valid: every table meets data/schema/model.yaml, and every view renders, the same twice"; on GitHub, #6's meta-rule step passed (run 39147447397) |
| R-5 | met | `test_R5_views_render_deterministically_and_demo_mode_writes_nowhere_else` passes: two renders identical, the working tree untouched, no render step calls GitHub |
| R-6 | met | `test_R6_no_stored_value_is_derivable` passes: no model table stores the kind name outside prose; the pilot stores no kind |
| R-7 | met | Trial [#7](https://github.com/Open-MBEE/repo-registry/pull/7): the required check failed on the meta-rule step, naming "approved_by: 'nobody-here' is not a maintainer.login", and the PR was BLOCKED; closed unmerged with a comment |
| R-8 | met | Against e219b85, view by view: every repository's kind, the applicability table, the pilot, the exclude list, the license, maintainer and recommendation reports are identical |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-6 exist, and every requirement passes its check | met | Above |
| Every audit finding has the supervisor's disposition | met | The check-in: all 16 to be fixed (F-05 by user ID; F-16 revised) |

## Outside the scope

- **Out-of-scope changes:** none beyond the details recorded in the build commit (d231e85).
- **Non-goals touched:** none. No outcome changed (R-8); no taxonomy refinement (WP5c); no live write to the wiki or
  issues (demo mode only); the model stays YAML and Markdown in git; sources and snapshots unchanged (the IDs are a new
  file beside the snapshot).

## Observations (not counted as failures)

1. Every table that names a repository also stores its name, checked against the snapshot, so a rename is caught.
2. `docs/fit-analysis.md` stays as WP4's dated record, so its counts are exempt from F-08.
3. Found and fixed on the way: a committed `.pyc`; the ISO standard's title (it tripped the licensed-text check, WP2
   R-12); both privacy checks, which would have read the maintainers' new user-ID keys as logins.
4. The test suite takes about 2.5 minutes, mostly the invalid-copy cases.
5. Until `main` has `render.py` (this pull request adds it), the CI view diff lists every view as new.
6. Four trial branches remain on GitHub; the Python patch-version pin (WP5's observation 7) moves to WP5c.
7. #6's first CI run failed only because `docs/status.md` links to this report, which didn't exist yet. This report
   fixes it.

## Open decisions (for the supervisor)

- **Observations 1 to 7, as one item:** accept as is, or pick any to act on. *Open: asked at the review, not yet
  answered.*

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| Observations 1 to 7, as one item | open | Waiting for the supervisor's answer |

## Recommendation

Not yet written: it follows the supervisor's disposition of the observations. Every deliverable and requirement is met
with evidence, and no outcome changed.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

# WP5 — Review report

| | |
|---|---|
| **Scope of work** | [WP5-scope-of-work.md](WP5-scope-of-work.md) |
| **Scope approval verified** | merge commit 0cbe887 by Michael Zargham (mzargham), parents 898cf4d and 8ed4608 (the `wp5-scope` tip) |
| **Work reviewed** | `wp5-work` at e1548ab, the head of [Open-MBEE/repo-registry#1](https://github.com/Open-MBEE/repo-registry/pull/1); rerun in full after the G-1 fix |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's merge, with a merge commit, of [#1](https://github.com/Open-MBEE/repo-registry/pull/1) into `main` (OD3) |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `scripts/validate.py` and `tests/test_wp5.py` |
| D-2 | met | `.github/workflows/check.yml`; it ran on every PR (#1–#4) |
| D-3 | met | `scripts/history_privacy_check.py`; result in the move record, step 0 |
| D-4 | met | `Open-MBEE/repo-registry` created; `main` pushed (78b2c66); ruleset `valid-main` (25334054); delivery PR #1; every write in [WP5-move-record.md](WP5-move-record.md) |
| D-5 | met | #2 (invalid) failed and was blocked; #4 (out of compliance, on the fix) passed and was CLEAN; both closed unmerged with comments |
| D-6 | met | AGENTS.md (remote, gate, OD4), README, `docs/status.md`, `docs/current-state.md`; XF-1's `closes_in` corrected |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `test_R1_each_invalid_file_fails_with_a_named_problem` (13 invalid copies) and `test_R1_the_command_exits_non_zero` pass |
| R-2 | met | `test_R2_out_of_compliance_is_valid` passes; trial #4 passed on GitHub with `arch_model` red |
| R-3 | met | `test_R3_hand_edit_to_a_generated_file_fails` and `test_R2_kind_change_without_regenerating_names_the_files` pass |
| R-4 | met | The workflow: `pull_request` and push to `main`, `permissions: contents: read`, actions pinned by SHA, no secrets; Python 3.10 and PyYAML 6.0.3 from `uv.lock` (after G-1). Run 39106770378 on e1548ab: "Using CPython 3.10.22", "Installed 1 package", `valid`, "Ran 78 tests ... OK (expected failures=2)" |
| R-5 | met | #2: failed, "registry.yaml: OpenSysML: type 'tool' and stage 'beta' name no kind", BLOCKED. #4: passed, CLEAN |
| R-6 | met | `history_privacy_check.py main wp5-work`: 70 concealed members, 523 blobs, 0 paths, 0 commit messages; `test_R6_history_scan_finds_a_name_only_in_an_old_commit` passes |
| R-7 | met | `test_R7_every_cited_commit_resolves` passes (sources' commits excepted, named with their repositories) |
| R-8 | met | The move record lists every write; GitHub's events show only the PRs and comments it lists. Some were run by the agent at the supervisor's request (exceptions to OD4, recorded); see observation 2 |
| R-9 | met | AGENTS.md, `current-state.md` and `status.md` state the remote, the gate (OD3) and the commands; link check passes |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-6 exist, and every requirement passes its check | met | Above |
| `Open-MBEE/repo-registry` exists, `main` requires the check, and the trials behaved as R-5 says | met | Ruleset active, no bypass; #2 blocked; #4 passed |
| The history scan shows no concealed member in what was pushed | met | R-6 |

## Outside the scope

- **Out-of-scope changes:** none beyond the fixes below. WP4c, WP4d and WP4e landed on `main` and were merged into
  `wp5-work`; their outcomes are their own packages'.
- **Non-goals touched:** none. Review friction is unchanged (no review required; XF-2 stays expected); no other
  repository or org setting was written; `data/proposed-codeowners` is not live.

## Observations (not counted as failures)

1. GitHub added a ruleset field that was not sent: `require_extra_approval_for_unattributed_changes: true`.
2. The agent ran some writes to the org at the supervisor's request (closing #2–#4, the pushes, opening #4), and one
   push that wasn't asked for: the G-1 fix, e1548ab, to `wp5-work`. All are recorded.
3. GitHub's audit trail shows the agent's actions under the supervisor's account (it uses his `gh` login); only the
   move record tells them apart.
4. Trial #3 found four tests tied to today's data, which would have failed every kind-change PR. Fixed in 22f75de.
5. Four trial branches remain on GitHub (nothing deletes them).
6. After acceptance, the status update itself must go through a pull request.
7. CI ran Python 3.10.22 and this machine 3.10.5: the lock pins 3.10 and PyYAML exactly, not the Python patch release.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1: no locked environment | fix before acceptance | Supervisor: "Fix before acceptance". Fixed in e1548ab; review rerun |
| Observations 1 to 6, as one item | accept as is | Supervisor: "Accept as is" |
| Observation 7 | noted after the supervisor's answer | Found on the rerun; a candidate for the next package (the consistency audit) |

## Recommendation

Recommend acceptance with the listed gaps noted, because every deliverable and requirement is met with evidence on
GitHub (#2 blocked, #4 passed, #1 CLEAN on the locked environment), G-1 is fixed, and the observations are accepted;
observation 7 is noted for the next package.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

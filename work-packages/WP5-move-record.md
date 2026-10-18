# WP5 — Move record

Every write to the Open-MBEE org in WP5, in order (D-4, D-5, R-8). Each command is run by mzargham, from the
commands below (OD4). The agent writes nothing to the org; it only reads (`gh` GET) to record the evidence.

## Before the push

| Step | What | Command | Evidence |
|---|---|---|---|
| 0 | Publication check of everything `main` publishes (R-6) | `python3 scripts/history_privacy_check.py main` | Clean: `refs: main; concealed members: 70; blobs scanned: 497; paths naming one: 0; commit messages naming one: 0` (run by mzargham, and by the agent read-only) |

## Writes to the org

| Step | What | Command (run by mzargham) | Evidence |
|---|---|---|---|
| 1 | Create the repository, public (Agent's defaults: required checks need a public repository on GitHub Free) | `gh repo create Open-MBEE/repo-registry --public --description "Policy and governance registry for the Open-MBEE GitHub organization (PROVISIONAL)"` | Created https://github.com/Open-MBEE/repo-registry, public, empty |
| 2 | Settings: projects off; merge commits only, so every approval and acceptance is a merge commit (OD3). Wiki and issues stay on | `gh repo edit Open-MBEE/repo-registry --enable-projects=false --enable-merge-commit --enable-squash-merge=false --enable-rebase-merge=false` | Confirmed by GET: `allow_merge_commit: true`, `allow_squash_merge: false`, `allow_rebase_merge: false`, `has_projects: false`; wiki and issues on |
| 3 | Push `main`, with its whole history (only `main`; Agent's defaults) | `git remote add origin https://github.com/Open-MBEE/repo-registry.git` then `git push -u origin main` | Pushed; GitHub's `main` is 78b2c66, as local; the first approval, 1dccb62, resolves on GitHub |
| 4 | The ruleset on `main`: the check `check` required, a pull request needed, merge commits only, no force-push, no deletion, no bypass (OD3; `.github/rulesets/main.json`) | `git switch wp5-work` then `gh api -X POST repos/Open-MBEE/repo-registry/rulesets --input .github/rulesets/main.json` | Ruleset `valid-main`, id 25334054, `enforcement: active`, `bypass_actors: []`, `current_user_can_bypass: never`. GitHub added `require_extra_approval_for_unattributed_changes: true`, which we did not send |
| 5 | Push the WP5 work and open the delivery pull request (the acceptance record) | `git push -u origin wp5-work` then `gh pr create --repo Open-MBEE/repo-registry --base main --head wp5-work --title "WP5: meta-rule checks in CI, and the move to Open-MBEE" --body "Delivery for work-packages/WP5-scope-of-work.md. Acceptance is mzargham's merge of this PR with a merge commit (OD3)."` | [#1](https://github.com/Open-MBEE/repo-registry/pull/1) opened; its check passed on 641a29d, and GitHub reported it CLEAN |
| 6 | Push the two trial branches and open a pull request for each (D-5) | `git push origin wp5-trial-invalid wp5-trial-out-of-compliance` then `gh pr create --repo Open-MBEE/repo-registry --base main --head wp5-trial-invalid --title "WP5 trial: invalid data (do not merge)" --body "WP5 D-5: must fail the required check and be blocked."` and `gh pr create --repo Open-MBEE/repo-registry --base main --head wp5-trial-out-of-compliance --title "WP5 trial: out of compliance (do not merge)" --body "WP5 D-5: must pass the required check."` | [#2](https://github.com/Open-MBEE/repo-registry/pull/2) and [#3](https://github.com/Open-MBEE/repo-registry/pull/3) opened; results below |
| 7 | Close both trial pull requests unmerged, once their checks have finished | `gh pr close <n> --repo Open-MBEE/repo-registry` for each trial PR | Both closed unmerged, with a comment each. **Run by the agent**, at the supervisor's request in chat ("write comments about the successful failures and close with comment those PRs"), an exception to OD4 for this step |
| 8 | Push the test fix and this record to the delivery PR; push the rerun trial and open its PR; close it | `git push` (on `wp5-work`); `git push origin wp5-trial-out-of-compliance-2`; `gh pr create ...` (#4); `gh pr close 4 --comment ...` | Done. **Run by the agent**, at the supervisor's choice in chat ("You run them", and "close #4 with a comment, push the finished move record"), an exception to OD4 for these steps. `wp5-work` 641a29d → 19e7694, then this record |

## The trials (D-5, R-5)

- **`wp5-trial-invalid`:** one change on top of the WP5 work. `registry.yaml` gives OpenSysML the stage `beta`, so
  its type and stage name no kind. Expected: the check fails, naming the problem, and the PR can't be merged.
- **`wp5-trial-out-of-compliance`:** one kind change on top of the WP5 work. `arch_model` becomes type `governance`, stage `sandbox`,
  and the files built from the kind list are regenerated. Its MIT license isn't allowed for governance, so the
  license report shows it red. Expected: the check passes.

| Trial | Pull request | Check | Mergeable |
|---|---|---|---|
| invalid | [#2](https://github.com/Open-MBEE/repo-registry/pull/2), e0fb427 | **failed**, as intended: the meta-rule step reported `registry.yaml: OpenSysML: type 'tool' and stage 'beta' name no kind` | **BLOCKED** by the ruleset |
| out of compliance | [#3](https://github.com/Open-MBEE/repo-registry/pull/3), c1357f9 | meta-rule step **valid**, but the test step **failed**: four tests were tied to today's kind list (see below) | BLOCKED |
| out of compliance, rerun on the fix | [#4](https://github.com/Open-MBEE/repo-registry/pull/4), 9b9b43a | **passed**: meta-rule step valid, all tests pass (run 39106398000); the license report shows `arch_model` red | **CLEAN** (mergeable); closed unmerged with a comment |

## What the trials found

The out-of-compliance trial was valid, but failed the required check, because four tests assumed today's data:
`test_wp1` R-2 (the kind list equal to the rules' draft), `test_wp4e` R-3 (kinds equal to the report before WP4e) and
`test_wp5`'s two R-2 tests (`arch_model` fixed). Left as it was, every kind-change PR would have failed the required
check, against R-2 and WP0 R-12. Fixed on `wp5-work` in 22f75de: the tests now check the rules (the draft covers the
same repositories, pilot kinds match the kind list, and the R-2 subject is chosen from the data). The trial is rerun
on the fix, as `wp5-trial-out-of-compliance-2`.

## Details decided during execution

- The ruleset also blocks force-pushes and deletion of `main`, so the record (every cited merge) can't be rewritten
  (G4, R-7). It requires the branch to be up to date with `main` before merging, so the check always ran on what
  lands: two valid changes can't combine into an invalid `main` (R-14).
- A review is not required (`required_approving_review_count: 0`): review friction stays low until R3, and XF-2
  stays an expected failure (WP5 non-goals).
- The kind list (`registry.yaml`) is not checked against `scripts/recommend.py`, which only drafted it: people edit
  it one entry at a time (WP0 R-12). The files built from it are checked, so a kind change regenerates them (the
  commands are in `docs/current-state.md`, "How to check everything").
- Commits of the cited source repositories (OpenSSF, CNCF, NIST) are not in this history. The cited-commit test
  (R-7) recognises them by their repository in the source tables.

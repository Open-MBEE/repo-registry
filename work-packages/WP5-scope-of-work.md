# WP5 — Scope of work: meta-rule checks in CI, and the move to Open-MBEE

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `repo-registry`: local now; moves to `Open-MBEE/repo-registry` in this package, only on mzargham's explicit go-ahead |
| **Approval record** | mzargham's `git merge --no-ff -m "<message>"` of the scope branch into `main`, locally ([AGENTS.md](../AGENTS.md)) |
| **Acceptance record** | mzargham's merge, with a merge commit, of the WP5 delivery pull request into `main` on `Open-MBEE/repo-registry` (OD3) |

## Purpose

WP0 R-14 says no invalid state can reach `main`: a change whose data breaks a meta-rule must not land, while a change
that leaves a repository out of compliance is valid, because that is how gaps are found (WP0-decisions, D-7). WP0's
definition of good enough asks that "this repo is in Open-MBEE, and a change with invalid data can't land on `main`",
and that the tests pass in Actions on every PR. WP0-decisions "Remote during R1" put the move in R1, waiting for the
supervisor's go-ahead. This package builds one meta-rule check for every data file, runs it and the tests in GitHub
Actions, moves the repository to Open-MBEE, and makes the check required on `main`.

Moving makes the repository and its whole history public (see the Agent's defaults on visibility). Before anything
is pushed, a history scan checks that no commit names a concealed org member. The history is published as is (OD1).

## Goals

- G1. **One meta-rule check.** One deterministic command checks every data file against its meta-rules. Invalid
  data fails, naming each problem; out-of-compliance data passes (WP0 R-14).
- G2. **No invalid state reaches `main`.** The check and the tests run in Actions on every pull request, and `main`
  requires them (WP0 R-14; WP0 definition of good enough).
- G3. **Nothing is published that shouldn't be.** No concealed org member (WP3 OD1) and no licensed text (WP2 R-12),
  in any commit pushed.
- G4. **The repository lives in Open-MBEE**, with its record intact, and the documents say how work is gated there.

## Non-goals

- Review friction on this repository. The switch to CODEOWNERS approval is at R3 (WP0-decisions "How restrictive
  this repo is in R1"). `data/proposed-codeowners` stays not live, and XF-2 stays an expected failure.
- The sensing credential, its setup included, and scheduled runs: WP6 (OD6). XF-1 stays an expected failure. The
  wiki and its publishing (WP7).
- Writing anything to the org beyond this repository, its settings and its ruleset. No other repository, no org
  setting, no issues.
- Changing any outcome: every repository keeps its kind, every policy applies to the same kinds, and the pilot and
  exclude list keep the same repositories (as in WP4b R-2).
- Meta-rules for the status log. WP6 builds the log, and adds its rules to the same check.
- New policies, or changes to the meta-rules themselves. This package enforces the documented ones
  ([kind-list-format.md](../docs/kind-list-format.md), [policy-format.md](../docs/policy-format.md)).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `scripts/validate.py` *(default)*: the meta-rule check for every data file, with `tests/test_wp5.py` *(default)* feeding it deliberately invalid copies and an out-of-compliance case | G1 |
| D-2 | `.github/workflows/check.yml` *(default)*: runs the check and the full test suite on every pull request and every push to `main` | G2 |
| D-3 | The publication check: a full-history scan for concealed members before the push, and the result recorded | G3 |
| D-4 | The move: `Open-MBEE/repo-registry` created, the history up to the approved scope pushed, the WP5 work opened as the delivery pull request, and a ruleset on `main` requiring the check with no bypass (OD3), each org write listed in `work-packages/WP5-move-record.md` *(default)* | G2, G4 |
| D-5 | Two trial pull requests on GitHub: one with deliberately invalid data, which fails and can't merge; one leaving a repository out of compliance, which passes. Both recorded in the move record, then closed unmerged | G2 |
| D-6 | The documents updated for the move: AGENTS.md (remote, gate convention), README, `docs/status.md`, `docs/current-state.md`, and XF-1's `closes_in` note in `data/expected-gaps.yaml` (OD6) | G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `python3 scripts/validate.py` checks every file under `data/` that has meta-rules: the taxonomy, the kind list (`registry.yaml`), assignments, policies, departures, the future list, deviations, maintainers, pilot rule, pilot and exclude list, expected gaps. It exits non-zero and names each problem, or exits 0. It reuses the checks the generators already make, and doesn't copy them. | Tests: for each file, an invalid copy fails with a named problem; the real data passes |
| R-2 | Out of compliance is valid: a change that makes a repository red (for example a kind change that brings in a policy it doesn't meet) passes the check. | A test; trial PR D-5 |
| R-3 | Every generated file matches its generator, replayed from the stored snapshot. A hand edit to a generated file fails. | A test regenerates into a temporary directory and compares |
| R-4 | The workflow runs on every pull request and every push to `main`, with read-only token permissions, Python 3.10 and PyYAML only, actions pinned by commit SHA, and no secrets. | Inspect the workflow; its runs on GitHub |
| R-5 | A pull request with deliberately invalid data fails the required check and can't be merged into `main`. An out-of-compliance pull request passes. | Trial PRs D-5, recorded with links |
| R-6 | Nothing is pushed until the publication check passes: no concealed member in any blob or commit message of the pushed history. | The history scan, run against exactly the refs pushed; output in the move record |
| R-7 | The record still traces: every commit SHA cited in `work-packages/` and `docs/` resolves in the pushed repository (OD1 keeps every SHA). | A test over the cited SHAs |
| R-8 | The only writes to the org are the ones listed in the move record (create the repository, push, set its settings and its ruleset), each run by mzargham from commands the agent handed him (OD4). | Inspect the move record against the repository's audit trail on GitHub |
| R-9 | The documents state the remote, the gate convention after the move (OD3), and how to run the check. | Inspect; the link check |

## Definition of good

- A maintainer can trust that whatever is on `main` is well-formed, because GitHub won't take anything else, and a
  newcomer reading the repository on GitHub sees exactly the record that was built locally, with nothing in it that
  shouldn't be public.

## Definition of good enough

- D-1 to D-6 exist, and every requirement passes its check.
- `Open-MBEE/repo-registry` exists, its `main` requires the check, and the two trial PRs behaved as R-5 says.
- The history scan shows no concealed member in what was pushed.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- **Visibility: public.** OpenMBEE is on GitHub Free, where rulesets and required checks work only on public
  repositories (`data/sources/github-plan.yaml`). A private repository couldn't enforce R-14.
- Paths and names: `scripts/validate.py`, `tests/test_wp5.py`, `.github/workflows/check.yml`, the check's name
  `check`, `work-packages/WP5-move-record.md`, and the repository name `Open-MBEE/repo-registry`.
- What is pushed: `main` only. Every package branch is merged into it, so every cited commit is reachable from
  `main`. The local branches are not pushed, and there are no tags.
- Repository settings: the wiki and issues are left on, projects off, and the default branch is `main`. Nothing else is changed.
- The workflow uses `actions/checkout` and `actions/setup-python`, pinned by SHA, with `permissions: contents: read`.
- The generated-file comparison (R-3) covers the files whose generators replay from the snapshot. The hand-written
  tables in `policy-basis-review.md` stay out of it (a later candidate).
- The privacy check (`scripts/privacy_check.py`) stays a live, local check. It needs org reads that CI doesn't
  have. The history scan (D-3) is a one-off before the push, kept in `scripts/` *(default)* for reruns.

## Open decisions (for the supervisor)

- **OD1.** The history before the push. *Decided: published as is.*
- **OD2.** *Dropped as moot after OD1: the existing tests run in CI unchanged.*
- **OD3.** The gate after the move. *Decided: approval and acceptance are mzargham's merge of a pull request, with a
  merge commit. Nobody can bypass the check: the ruleset has no bypass list.*
- **OD4.** Who runs the writes to the org. *Decided: the agent hands mzargham the exact commands, and he runs them.
  The agent writes nothing to the org itself.*
- **OD5.** The clone counts in the usage snapshot. *Decided: publish as is.*
- **OD6.** The sensing credential (XF-1). *Decided: WP6, where it is first used. The expected-gaps note is corrected.*
- **OD7.** The Agent's defaults. *Decided: approved.*

None remain open. Every item was resolved through the decision loop: 6 decided, 0 deferred, 0 raised, and 1 dropped
as moot (OD2). The records are in [WP5-decisions.md](WP5-decisions.md).

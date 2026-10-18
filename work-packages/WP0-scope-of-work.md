# WP0 — Scope of work: repo-registry, zoomed out

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `repo-registry`: local now, moved to Open-MBEE during R1 |
| **Approval record** | mzargham's `git merge --no-ff` of the scope branch into `main` ([AGENTS.md](../AGENTS.md)) |
| **Acceptance record** | mzargham's `git merge --no-ff` of the work branch into `main` ([AGENTS.md](../AGENTS.md)) |

## Purpose

Agree on what `repo-registry` is for, what it will and won't do, and when it counts as done, at a level above the
detailed design. The design documents in [docs/](../docs/) are **DRAFT inputs, not part of this contract**. They may
be over-detailed, and they stay open to change. This document is the expectation everyone holds the work to.
`work-breakdown` splits it into packages, and each package gets its own scope of work.

This scope runs **through R1**, demonstration and agreement ([roadmap.md](../docs/roadmap.md)). In R1 every goal is
shown on a made-up org, not on the live one. Running on the live org (R2), becoming the source of truth (R3) and
steady state (R4) come later and will need their own scope.

### Direction decided while scoping

These were settled with the supervisor while scoping ([WP0-decisions.md](WP0-decisions.md)). Where they differ from
the DRAFT design docs, these take precedence, and the docs are updated by a later package.

- **Kinds:** every repo gets an initial kind, inferred from its measurable attributes using the taxonomy. Operators
  are invited to change it with a PR to this repo, and governors review and merge every such PR. The same PR path is
  used for any change of kind. A kind-change PR is the only thing an operator ever does in this repo. Changing a kind
  must be as easy as possible and readable by people.
- **Canonical kind list and policies:** the canonical list of kinds per repo is one file at the root of this repo,
  holding only enough to look up the policies that apply. The policies are files too. Both must be easy for people to
  read and easy for the program to check against what it senses. YAML is the starting point for reasoning about the
  format, not a decision.
- **Issues:** each issue states that the repo is out of line with a specific policy in effect for its kind. The main
  path is to change the repo's configuration to match. The escalation path is a kind-change PR to this repo.
- **Credentials:** reading uses a strong credential, so settings are measured rather than asked about. Writing uses a
  comparatively weak one.
- **Automatic fixes** (the system changing a setting itself) are future work: a nice-to-have that makes things easier,
  weighed against security. Until then, gaps go out as change requests.
- **CI/CD:** this repo governs the rules about the rules. It describes what kinds a repo can be, which controls each
  kind needs, and tracks compliance (measured and attested) with them. It works like a CI/CD pipeline. CI checks that
  no meta-rule is broken, and publishing the wiki is the deployment. An **invalid** state (data not correctly
  constructed, breaking a meta-rule) must never reach `main`. An **out-of-compliance** state is valid, because that is
  how gaps are found and fixed.
- **Remote:** this repo moves to Open-MBEE during R1, so its Actions checks and the required check on `main` are real
  before R1 ends. The move itself is done only when the supervisor says so.
- **Status log:** each run's compliance status is written to a data file in this repo that joins cleanly to the
  canonical kind list (keyed by repo), so the compliance history is the git history.
- **Wiki:** the wiki is this repo's own built-in wiki, with a narrow remit. It is not the separate Open-MBEE wiki
  repo, which is a media repo with a broader remit and a more permissive kind.
- **The set of kinds** is drafted in the first package that `work-breakdown` proposes.

## Goals

- G1. **Find your way.** Anyone can see, in one place, every Open-MBEE repo: its kind, who is responsible for it, and
  which repos are highlighted (in active development, or trusted and maintained).
- G2. **Show that we follow our own rules.** Regulated adopters can see that who may change what, and who approves a
  release, follow written rules, aligned with CISA *Open Source Software: Security Principles and Practices* (2026).
- G3. **Add friction only where it's needed, and say so.** Each kind of repo has its own controls: strictest for tools,
  lighter for media and research. For every repo you can see which controls apply, which deliberately don't, and
  whether the ones that apply are really in effect.
- G4. **Find gaps and send them to the right person.** On a schedule, the system checks each repo against its rules
  and tells a named person what needs doing, where they already work.
- G5. **Maintainers agree before it acts on the real org.** The rules are shown working on a made-up org first, and
  the maintainers agree on them before the system touches the live org.

## Non-goals

- An AI agent. No language model takes part in any decision.
- A project tracker, or a replacement for each repo's contributing guide.
- Deleting repositories. It never deletes anything.
- The authority on a repo's status. People decide that: operators propose kinds by PR, and governors merge. The
  system records, infers initial kinds and checks.
- Its own identity or permission system. Everything uses GitHub users, teams, roles, CODEOWNERS and rulesets.
- Writing to the live org, apart from this repo itself once it moves there. The only contact with other repos in R1 is
  a read-only check of how well the draft kinds fit them.
- Automatic fixes, where the system changes a setting itself (future work).
- Review friction on this repo. In R1 its only restriction is the valid-`main` check (R-14). The switch to a
  CODEOWNERS (maintainer) approval policy is an explicit later step on the roadmap, at R3
  ([roadmap.md](../docs/roadmap.md), IF-9).
- R2 to R5: scheduled live runs, the published wiki, issues opened in real repos, becoming the source of truth, and the R5 "later" items.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The rules as data: the canonical kind list (one file at the root of this repo, one entry per repo, with only enough to look up its policies), and the policy files, where each control names the GitHub setting it relies on and the CISA practice it serves. Readable by people and checkable by the program. | G2, G3 |
| D-2 | The program: a small deterministic check that compares each repo with its rules and sends gaps on, run on the made-up org, with its tests running in GitHub Actions on every PR | G4 |
| D-3 | Wiki pages generated by the program as local files: an index page, one page per kind, one page per repo. Each repo shows a red / yellow / green compliance status, so governors and readers can scan for compliance | G1, G3 |
| D-4 | Issue texts generated as local files, filled deterministically from templates by the state machine. Each states which policy in effect for the repo's kind it is out of line with, the main path (change the configuration) and the escalation path (a kind-change PR to this repo). Policy questions go to governors. | G4 |
| D-5 | One made-up example org, with tests and three demonstration flows, one per role: reader, operator, governor | G5 |
| D-6 | A read-only fit report: how well the draft kinds fit the live Open-MBEE repos, and which don't fit | G5 |
| D-7 | The status log: a data file in this repo, one entry per repo per run with its red / yellow / green status, joining cleanly to the canonical kind list, so compliance history is in git. In R1 it is written for the made-up org. | G2, G3 |

## Requirements

R-1 to R-8 are the project's hard constraints, taken from [AGENTS.md](../AGENTS.md) and the cross-cutting table in
[design.md](../docs/design.md), with checks from that table's "assessed by" column. R-9 to R-14 were raised while
scoping. All were approved by the supervisor.

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | No language model in sensing, classifying, deciding or acting (X-1). | Code review; dependency list |
| R-2 | Same inputs give the same outputs, and each run keeps its inputs (X-2). | Replay a stored run and diff the outputs |
| R-3 | Nothing deletes a repo (X-3). | Inspect the list of actions the program can take |
| R-4 | Everything a non-specialist reads is plain language (X-4). | Cold read by a non-specialist |
| R-5 | Identity, permissions, review and audit are GitHub's own, never rebuilt here (X-5, X-7, X-8). | List of mechanisms used: every one is GitHub-native |
| R-6 | Kinds and rules are data. Changing them needs no code change (FM-2). | Swap in a toy set of kinds and rules; zero code change |
| R-7 | If the inputs can't be trusted, the run takes no action, marks the wiki stale, and tells the maintainers (X-10). | Example run with a sensing failure |
| R-8 | Only `gh` and `git` touch GitHub (FM-10). | Code review |
| R-9 | Sensing reads with a strong credential. Writing uses a weak one that can only open, comment on and close issues, push this repo's wiki, and commit the status log to this repo. It closes an issue only when sensing shows the task is done. | Inspect the scopes of each credential the program is configured with *(default)*; example run where a sensed fix closes its issue |
| R-10 | Every cell of the coverage grid below that names a check has that check, as a test run in Actions, or as a named manual check where the check is a review or a reading. | Walk the grid at acceptance: each marked cell points to a test or a manual check that passes |
| R-11 | Idempotent: each gap on a repo has at most one open issue. Rerunning on an unchanged gap opens no new issue and posts nothing new *(default: nothing new)*. | Run twice on the same fixture: the second run's action log is empty |
| R-12 | Changing a repo's kind is a small edit that people can read: one entry in the canonical kind list. | A reclassification diff on the made-up org touches one entry *(default)* |
| R-13 | Every repo, and every control on it, shows a compliance status: **red** = known out of compliance, **yellow** = can't tell, **green** = known in compliance. A control with an accepted deviation is green, marked visibly as an accepted exception. A repo is red if any control is red, yellow if none is red but any is yellow, and green only if every control is green *(default)*. The status is shown in words as well as color *(default)*. | On the made-up org, repos and controls in each state show the expected status |
| R-14 | No invalid state can reach `main`. Every change to this repo's data (kind list, policies, status log), from a person or the program, is checked against the meta-rules before it lands *(default: the program's own status-log commits are checked the same way)*. Out of compliance is valid. The wiki is published only from a valid `main`. | A change with deliberately invalid data fails the check and does not land; an out-of-compliance change passes |

### Coverage grid: deliverable × requirement

A marked cell means the deliverable touches the requirement, and the cell names its check. A blank cell means it
doesn't touch it. The supervisor approved the grid one deliverable column at a time.

| | D-1 Rules | D-2 Program | D-3 Wiki pages | D-4 Issue texts | D-5 Made-up org, tests, 3 demo flows | D-6 Fit report | D-7 Status log |
|---|---|---|---|---|---|---|---|
| **R-1** No LLM | | Dependency list; code review | | | | Dependency list | |
| **R-2** Replayable | | Replay a stored run; diff outputs | Regenerate from a snapshot; diff | Regenerate from a snapshot; diff | Fixture snapshots are stored and versioned | Rerun on the stored inventory; diff | Regenerate from a snapshot; diff |
| **R-3** Never deletes | | Actions list has no delete | | No issue text instructs deletion | | | |
| **R-4** Plain language | Class pages read cold | | Cold read by a non-specialist | Cold read by a non-specialist | Demo script read cold | Cold read by a non-specialist | |
| **R-5** GitHub-native | Every control names its GitHub mechanism | Mechanism inventory | | Issues name GitHub settings, not local ones | | | |
| **R-6** Rules as data | Toy rule set loads | Toy swap: zero code change | Pages change with the rules | Issue texts change with the rules | Toy rule set included | Fit runs against any rule set | Entries follow the rules in force |
| **R-7** Fail safe | | Failure run: no actions | Stale banner with reason | One notification, no other issues | Failed-run fixture included | Aborts with no report on partial sensing | A failed run records only the failure |
| **R-8** Only gh and git | | Code review | | | | Code review | Committed with `git` only |
| **R-9** Strong read, weak write | | Credential scope inspection | | Closes an issue only when its fix is sensed | | Read credential only | The only file the program commits here |
| **R-11** Idempotent | | Second run on the same fixture: empty action log | | One issue text per repo × gap | Repeat-run fixture included | | No change in status → no new commit |
| **R-12** Easy reclassification | One-entry diff | | Pages follow the new kind | Each issue links to the reclassification path | Reclassification case included | | Joins to the kind list on the repo key |
| **R-13** Red / yellow / green | | Status follows from the verdicts | Each fixture repo shows its expected status; index can be scanned by status | | Fixture has red, yellow and green repos, and a green-with-exception control | | Records each repo's status per run |
| **R-14** Valid main | Invalid kind list or policy fails the check | The meta-rule check runs on every change | Published only from a valid `main` | | Invalid-change and out-of-compliance cases included | | Each log commit passes the check before it lands |

## Definition of good

- The maintainers agree on the kinds and rules with confidence, because they saw exactly what those rules would do.
- Anyone who watches a demonstration can explain what the system would do to a repo, and why, without reading code.
- The system is ready to switch on against the live org (R2) with no redesign.

## Definition of good enough

From the R1 exit test in [roadmap.md](../docs/roadmap.md):

- The loop runs end to end on the made-up org: it classifies, compares and routes, and writes the wiki pages and
  issue texts as local files.
- Tests for the requirements above pass in Actions on every PR, and every marked cell of the coverage grid has its
  check (R-10).
- Draft kinds and rules exist as data, and changing them and re-running shows what changes.
- The read-only fit report against the live inventory exists.
- This repo is in Open-MBEE, and a change with invalid data can't land on `main` (R-14).
- All three demonstration flows (reader, operator, governor) have been given.
- The maintainers have agreed on the kinds and rules, merged by PR.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

All defaults were decided by the supervisor (see [WP0-decisions.md](WP0-decisions.md)). The ones that remain in the
text, marked *(default)*:

- R-9's check: inspect the scopes of each credential the program is configured with.
- R-11: a rerun on an unchanged gap posts no new comment, as well as opening no new issue.
- R-12's check: a reclassification on the made-up org changes exactly one entry in the canonical kind list.
- R-13: how a repo's status rolls up from its controls (any red → red; else any yellow → yellow; else green), and
  the status is shown in words as well as color.
- R-14: the program's own status-log commits are checked against the meta-rules the same way as a person's.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop: 39 decided, 0 deferred, 10 raised (R-9, R-10, R-11, R-12,
R-13, R-14, D-7, OD3, the remote during R1, and how restrictive this repo is in R1). The records are in
[WP0-decisions.md](WP0-decisions.md).

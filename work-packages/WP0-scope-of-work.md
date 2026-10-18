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

This scope runs **through R1**, demonstration and agreement ([roadmap.md](../docs/roadmap.md)). R1 shows how the taxonomy and
policy work in practice, on a **pilot**: a scoped subset of real Open-MBEE repos. It shows what would happen if the
system were turned on, and writes nothing to those repos. What R1 needs from the maintainers is five approvals: the
taxonomy, the policies (based on the taxonomy), the pilot subset of repos in the registry, the assigned kind of each
repo in it, and the named maintainers. With those in hand, a bounded proof of concept follows (R2). It calibrates toward a trusted source of truth
and brings repos into line with policy. That, becoming the source of truth (R3) and steady state (R4) come later and
will need their own scope.

### Direction decided while scoping

These were settled with the supervisor while scoping ([WP0-decisions.md](WP0-decisions.md)). Where they differ from
the DRAFT design docs, these take precedence, and the docs are updated by a later package.

- **Two core citations:** CISA [*Open Source Software: Security Principles and Practices*](https://www.cisa.gov/sites/default/files/2026-08/open-source-software-security-principles-and-practices.pdf)
  (2026) and NIST [SP 800-37 Rev. 2](https://csrc.nist.gov/pubs/sp/800/37/r2/final), the *Risk Management Framework*
  (RMF, December 2018). The README links both and states the design intent: minimum viable policy making and controls. RMF is cited for the process, through the map below.
  Each policy also names the CISA practice and the RMF task or SP 800-53 control it serves, or says "none".
  *(amended, WP1 amendment 3: OpenSSF is a third core citation, for its project lifecycle, from which the stages are
  adopted, and its security baseline, the backbone of the policies. Each policy names the baseline items it adopts.)*

  | RMF step | In this system |
  |---|---|
  | Prepare | Org governance: the named maintainers and the org policy (D-8) |
  | Categorize | Assigning each repo a kind |
  | Select | The named policies in effect for each kind. Accepted deviations play the part of tailoring |
  | Implement | Each policy's SOP setup steps, carried out by operators |
  | Assess | Automated checks plus operator attestations |
  | Authorize | The maintainers' approvals, and governors merging kind changes |
  | Monitor | Scheduled runs, red / yellow / green status and the status log |
- **Kinds and policies reduce dimensionality.** The aim is rigorous controls on the repos that need them and low
  friction everywhere else. We don't support every policy GitHub can express. We name a small set of policies,
  document each one's configuration, and state clearly when each policy is in effect. A repo's kind gives it three
  categorical attributes: its **type**, its **lifecycle**, and its **tier** (derived from the kind). Each policy
  attaches to a type, a lifecycle or a tier, so it reduces to a plain rule: *this policy applies if* a condition on
  those three attributes holds. Kinds are classified from rich data about each repo, and they are a fairly small
  taxonomy. Repos are many and policies are few. The rules connecting them are low-dimensional, plain-language,
  deterministic and replayable: categorical feature engineering from repos to three attributes, and from those
  attributes to the policies in effect. *(Amended, A1.)* The lifecycle stages are adopted from the CNCF and OpenSSF
  project lifecycles: Sandbox, Incubating, Graduated, Archived ([lifecycle-stage-map.md](../docs/lifecycle-stage-map.md),
  *amended A4*). Each policy is defined at a level GitHub can configure. The pilot is a few
  dozen repos. The full scope is the low hundreds.
- **Simplest sufficient policy set:** the policies are drawn from a review of GitHub's security features and
  documentation, cross-checked against the NIST RMF and CISA guidance, to find the simplest set of policies that meets
  our security objectives.
- **Governance type.** Besides tool, media and research, there is a **governance** type. Only two things have it:
  this repo (governance/sandbox) and the administration of the GitHub org itself (governance/graduated, *amended A4*). Every
  governance kind maps to the high tier, because controls at the governance level must be as strict as, or stricter
  than, anything they govern. Governance kinds are assigned, not recommended. *(Amended, A2.)*
- **Four tiers across the kinds.** Each kind sits in one of four tiers. **High:** graduated tools, which need
  rigorous release control, and governance. **Medium:** load-bearing media such as the website, and incubating tools
  (version 1.0 or later, not yet graduated). **Low:** repos that need an owner but have no formal controls beyond
  someone who looks after them, including sandbox tools (no release yet, or only 0.x releases). *(Amended, A4.)* **None:**
  archived material, read-only once its archived status has been verified.
- **Operators are named in each repo.** Repos are governed locally by their CODEOWNERS, which the program senses.
  Where a tier needs an owner (high, medium, low), the owner is the repo's CODEOWNERS *(default)*, and only a
  CODEOWNER's attestation counts *(default)*. A repo's own CODEOWNERS is the authoritative source for that repo.
  The registry reads the CODEOWNERS of every tracked repo and shows them in the wiki, but never holds its own copy as
  the source. The canonical kind list stays minimal.
- **Every policy has an SOP** (a standard operating procedure) for complying with it. It covers how to set the policy
  up, its measurable (and so automatable) checks, and its attested checks, including how to keep attestations up
  to date.
- **Compliance:** a repo is in compliance when it passes its automated checks and has up-to-date attestations from its
  operator, the party accountable for the repo. A required attestation that is missing or out of date is
  non-conformant, so red. A repo whose kind requires no attestations can be green with none, which we expect for some
  kinds. Attestations live in the operator's own repo, for example as a trailer in its README filled from a template,
  so they keep up with releases.
- **Low friction where it fits:** exploratory research repos are lax by design. Some are a single committer exploring
  ideas in public, and we don't want to stop that. They are often archived when they go stale. An archived repo is
  read-only, so it is compliant by definition once it has been archived. Archiving follows a named **archive policy**
  with its own SOP, from CISA's end-of-support guidance: before archiving, the README states that support has ended
  and points to known forks. Repos archived before this policy existed count as compliant as they are *(default)*.
- **Kinds:** every repo gets an initial kind, inferred from its measurable attributes using the taxonomy. Operators
  are invited to change it with a PR to this repo, and governors review and merge every such PR. The same PR path is
  used for any change of kind. A kind-change PR is the only thing an operator ever does in this repo. Changing a kind
  must be as easy as possible and readable by people.
- **Canonical kind list and policies:** the canonical list of kinds per repo is one file at the root of this repo,
  holding only enough to look up the policies that apply. The policies are files too. Both must be easy for people to
  read and easy for the program to check against what it senses. YAML is the starting point for reasoning about the
  format, not a decision.
- **Issues:** each issue states that the repo is out of line with a specific policy in effect for it. The main
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
- **Pilot:** the registry starts with 24 to 36 real Open-MBEE repos, a size that balances effort against proving value.
  Every other repo is on the exclude list. The pilot is sampled to include heavily used and actively developed
  tools, the website and other media, some research repos, and some repos that should be archived.
- **Fit analysis:** a separate task from the pilot. It examines how the draft kinds fit all of the org's repos.
- **Named maintainers and the org:** the named maintainers are the people with governance power: this repo's
  CODEOWNERS and the admins of the GitHub org. Today the org's leadership isn't necessarily mapped to technical
  leadership, and it isn't clear who holds admin authority or what powers they have, which matters for CISA. The org
  as a whole gets the same treatment as a repo: a clear policy, with what can be measured measured and the rest
  attested, so that the stated list of maintainers matches the people with governance power over the org. The org policy
  also names a few org-wide settings (for example, requiring two-factor authentication, or the base permission for
  members). These are common controls in RMF's terms: every repo inherits them, and they are checked like any
  policy.
- **Status log:** each run's compliance status is written to a data file in this repo that joins cleanly to the
  canonical kind list (keyed by repo), so the compliance history is the git history.
- **Wiki:** the wiki is this repo's own built-in wiki, with a narrow remit. It covers the registry's status
  information and what the kinds and tiers mean, and it contains the policies. It has a page for every kind, every
  policy and every tier, and views of the registry by kind, by policy and by tier. It has no page per repo. In the
  views, each repo has its color code, a link to the repo, and a link to a view of the repo's outstanding issues,
  filtered by the labels the program put on the issues it wrote. It is not the separate Open-MBEE wiki
  repo, which is a media repo with a broader remit and a more permissive kind.
- **The set of kinds** is drafted in the first package that `work-breakdown` proposes.

## Goals

- G1. **Find your way.** Anyone can see, in one place, every Open-MBEE repo: its kind, who is responsible for it, and
  which repos are highlighted (incubating or graduated; *amended A4*).
- G2. **Show that we follow our own rules.** Regulated adopters can see that who may change what, and who approves a
  release, follow written rules, aligned with CISA *Open Source Software: Security Principles and Practices* (2026) and the NIST Risk
  Management Framework (SP 800-37 Rev. 2). In R1 this
  is shown on the pilot.
- G3. **Add friction only where it's needed, and say so.** Each kind of repo has its own controls, set by its tier: high
  for core tools, then medium, low, and none for archived repos. For every repo you can see which controls apply, which deliberately don't, and
  whether the ones that apply are really in effect.
- G4. **Find gaps and send them to the right person.** On a schedule, the system checks each repo against its rules
  and tells a named person what needs doing, where they already work. In R1 this is shown with sample issues.
- G5. **Maintainers approve before it acts on the real org.** The rules are shown working on the pilot, with nothing
  written to its repos, and the maintainers approve the taxonomy, the policies, the pilot subset, each pilot repo's
  kind and the named maintainers before the system writes anything to the org.

## Non-goals

- An AI agent. No language model takes part in any decision.
- A project tracker, or a replacement for each repo's contributing guide.
- Deleting repositories. It never deletes anything.
- The authority on a repo's status. People decide that: operators propose kinds by PR, and governors merge. The
  system records, infers initial kinds and checks.
- Supporting every policy GitHub can express. Only named policies, each with a rule on type, lifecycle or tier, are checked.
- Its own identity or permission system. Everything uses GitHub users, teams, roles, CODEOWNERS and rulesets.
- Writing to the live org, apart from this repo itself once it moves there. The only contact with other repos in R1 is
  reading them: the pilot repos, and the fit analysis of all repos. The sample issues are not posted.
- Automatic fixes, where the system changes a setting itself (future work).
- Review friction on this repo. In R1 its only restriction is the valid-`main` check (R-14). The switch to a
  CODEOWNERS (maintainer) approval policy is an explicit later step on the roadmap, at R3
  ([roadmap.md](../docs/roadmap.md), IF-9).
- R2 to R5: scheduled live runs, the published wiki, issues opened in real repos, becoming the source of truth, and the R5 "later" items.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The rules as data: the canonical kind list (one file at the root of this repo, one entry per repo, with only enough to look up its kind), the map from kinds to tiers, and the named policies. Each policy documents its GitHub configuration, states its applies-if rule on type, lifecycle or tier, names the CISA practice and the RMF task or SP 800-53 control it serves (or "none"), and has an SOP covering setup, automated checks and attested checks. Readable by people and checkable by the program. | G2, G3 |
| D-2 | The program: a small deterministic check that compares each repo with its rules and works out what it would send, run read-only on the pilot, with its tests running in GitHub Actions on every PR | G4 |
| D-3 | Wiki pages generated by the program as local files: an index page; one page per kind, per policy and per tier (the policy pages hold the policies); and views of the registry by kind, by policy and by tier. No page per repo. In each view, every repo shows its red / yellow / green status, a link to the repo, and a link to its outstanding registry issues, filtered by the labels the program writes on them | G1, G3 |
| D-4 | Sample issue texts, generated as local files: what the system would write, shown for demonstration and not posted. Filled deterministically from templates by the state machine, and carrying the labels the wiki's issue links filter on *(default: a registry label plus one per policy)*. Each states which policy in effect for the repo it is out of line with, the main path (change the configuration) and the escalation path (a kind-change PR to this repo). Policy questions go to governors. | G4 |
| D-5 | The pilot: a proposed subset of 24 to 36 real Open-MBEE repos (everything else on the exclude list), with each one's proposed kind, sampled as in *Direction*; tests on stored snapshots of it; and three demonstration flows, one per role (reader, operator, governor), showing what would happen if the system were turned on | G5 |
| D-6 | A read-only fit analysis of all of the org's repos (about 183): how well the draft kinds fit them, and which don't fit. A separate task from the pilot | G5 |
| D-7 | The status log: a data file in this repo, one entry per repo per run with its red / yellow / green status, joining cleanly to the canonical kind list, so compliance history is in git. In R1 it is written for the pilot. | G2, G3 |
| D-8 | Org governance: the named-maintainer list (a data file in this repo, joining cleanly to this repo's CODEOWNERS); an org policy saying who holds governance power over the org, which powers they have, and which org-wide settings (common controls) are required; and a read-only check that the list matches this repo's CODEOWNERS and the org's admins and that the org-wide settings are in effect, with a red / yellow / green status for the org | G2 |
| D-9 | A policy basis review: GitHub's security features and documentation, cross-checked against the NIST RMF and CISA guidance, proposing the simplest set of named policies that meets our security objectives, each mapped to its GitHub configuration and its citations. It is the input to the policies the maintainers approve | G2, G3 |

## Requirements

R-1 to R-8 are the project's hard constraints, taken from [AGENTS.md](../AGENTS.md) and the cross-cutting table in
[design.md](../docs/design.md), with checks from that table's "assessed by" column. R-9 to R-18 were raised while
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
| R-11 | Idempotent: each gap on a repo has at most one open issue. Rerunning on an unchanged gap opens no new issue and posts nothing new *(default: nothing new)*. | Run twice on the same stored snapshot: the second run's action log is empty |
| R-12 | Changing a repo's kind is a small edit that people can read: one entry in the canonical kind list. | A reclassification diff on the pilot touches one entry *(default)* |
| R-13 | Every repo, and every control on it, shows a compliance status: **red** = known out of compliance, **yellow** = can't tell, **green** = known in compliance. Green means the automated checks pass and every required attestation is present and up to date. A missing or out-of-date required attestation is red. An attestation is out of date once it is older than the repo's latest release *(default)*. An archived repo is green by definition. A repo is archived through the archive policy, and repos archived before it existed are green as they are *(default)*. A control with an accepted deviation is green, marked visibly as an accepted exception. A repo is red if any control is red, yellow if none is red but any is yellow, and green only if every control is green *(default)*. The status is shown in words as well as color *(default)*. | On the pilot snapshot, repos and controls in each state show the expected status |
| R-14 | No invalid state can reach `main`. Every change to this repo's data (kind list, policies, status log), from a person or the program, is checked against the meta-rules before it lands *(default: the program's own status-log commits are checked the same way)*. Out of compliance is valid. The wiki is published only from a valid `main`. | A change with deliberately invalid data fails the check and does not land; an out-of-compliance change passes |
| R-15 | The named-maintainer list matches the people with governance power: this repo's CODEOWNERS and the org's admins. What can be measured (org roles, CODEOWNERS) is sensed. What can't (for example, powers held outside GitHub roles) is attested. Each mismatch is a gap with a status. | On the pilot snapshot, a matching list is green, and a deliberate mismatch is red with a sample issue to governors |
| R-16 | Every policy is named, documents its GitHub configuration, states its applies-if rule on type, lifecycle or tier *(amended, A1)*, cites the CISA practice and the RMF task or SP 800-53 control it serves (or "none"), and has an SOP covering setup, automated checks and attested checks. No check runs that isn't in a named policy. | The meta-rule check (R-14) rejects a policy missing any part; a cold read of each SOP |
| R-17 | Every kind is in exactly one tier (high, medium, low, none). A repo's operators are its CODEOWNERS, sensed from the repo, whose CODEOWNERS file is the authoritative source; the registry reads it and shows it in the wiki. A repo in a tier that needs an owner, with no CODEOWNERS, is red. Only a CODEOWNER's attestation counts *(default)*. | The meta-rule check rejects a kind with no tier; on the pilot snapshot, a repo with no CODEOWNERS in an owned tier is red, and an attestation by a non-CODEOWNER doesn't count |
| R-18 | Every repo shown in a wiki view links to the repo and to a view of its outstanding registry issues, filtered by the labels the program writes. | On the pilot views, every repo has both links, and each issue link's filter matches the labels on that repo's sample issues |

### Coverage grid: deliverable × requirement

A marked cell means the deliverable touches the requirement, and the cell names its check. A blank cell means it
doesn't touch it. The supervisor approved the grid one deliverable column at a time.

| | D-1 Rules | D-2 Program | D-3 Wiki pages | D-4 Issue texts | D-5 Pilot, tests, 3 demo flows | D-6 Fit report | D-7 Status log | D-8 Org governance | D-9 Policy basis |
|---|---|---|---|---|---|---|---|---|---|
| **R-1** No LLM | | Dependency list; code review | | | | Dependency list | | | |
| **R-2** Replayable | | Replay a stored run; diff outputs | Regenerate from a snapshot; diff | Regenerate from a snapshot; diff | Pilot snapshots are stored and versioned | Rerun on the stored inventory of all repos; diff | Regenerate from a snapshot; diff | Rerun on a stored snapshot; diff | |
| **R-3** Never deletes | | Actions list has no delete | | No issue text instructs deletion | | | | | |
| **R-4** Plain language | Kind pages read cold | | Cold read by a non-specialist | Cold read by a non-specialist | Demo script read cold | Cold read by a non-specialist | | Org page read cold | Summary read cold |
| **R-5** GitHub-native | Every control names its GitHub mechanism | Mechanism inventory | | Issues name GitHub settings, not local ones | | | | Uses only GitHub org roles and CODEOWNERS | Only GitHub-native features are proposed |
| **R-6** Rules as data | Toy rule set loads | Toy swap: zero code change | Pages change with the rules | Issue texts change with the rules | Toy rule set included | Fit runs against any rule set | Entries follow the rules in force | Org policy is data | |
| **R-7** Fail safe | | Failure run: no actions | Stale banner with reason | One notification, no other issues | Failed-run case included | Aborts with no report on partial sensing | A failed run records only the failure | Unreadable org roles or settings show yellow, never green | |
| **R-8** Only gh and git | | Code review | | | | Code review | Committed with `git` only | Code review | |
| **R-9** Strong read, weak write | | Credential scope inspection | | Closes an issue only when its fix is sensed | | Read credential only | The only file the program commits here | Read credential only; no org role is changed | |
| **R-11** Idempotent | | Second run on the same snapshot: empty action log | | One issue text per repo × gap | Repeat-run case included | | No change in status → no new commit | One issue per mismatch | |
| **R-12** Easy reclassification | One-entry diff | | Views follow the new kind | Each issue links to the reclassification path | Reclassification case included | | Joins to the kind list on the repo key | | |
| **R-13** Red / yellow / green | | Status follows from the verdicts | Each pilot repo shows its expected color in every view | | Pilot has red, yellow and green repos, and a green-with-exception control | | Records each repo's status per run | The org gets a status | |
| **R-14** Valid main | Invalid kind list or policy fails the check | The meta-rule check runs on every change | Published only from a valid `main` | | Invalid-change and out-of-compliance cases included | | Each log commit passes the check before it lands | Invalid maintainer list fails the check | |
| **R-15** Maintainers match governance power | Maintainer list and org policy are data | Compares the list with CODEOWNERS and org admins | The org page shows the match | Sample issue to governors on a mismatch | Pilot demo includes the org | | Records the org's status per run | Matching list and settings in effect: green; a mismatch or a missing setting: red | |
| **R-16** Named policies with SOPs | Each policy has every required part, citations included; meta-rule check | Runs only the checks the named policies define | Type, lifecycle and tier pages list the policies attached to them; policy pages hold each SOP | Each issue links to its policy's SOP | Pilot has a strict tool, a lax research repo, and an archived repo shown green | | | | Each proposed policy has its GitHub configuration and both citations |
| **R-17** Tiers and operators | Each kind maps to one tier; meta-rule check | Senses CODEOWNERS; counts only CODEOWNER attestations | Views show each repo's tier and CODEOWNERS | Issues go to the repo's CODEOWNERS | Pilot covers all four tiers, and a repo with no CODEOWNERS | | | | |
| **R-18** Repo and issue links | | Builds both links for every repo | Every repo in every view has both links | Issues carry the labels the links filter on | Link check on the pilot views | | | | |

## Definition of good

- The maintainers agree on the kinds and rules with confidence, because they saw exactly what those rules would do.
- Anyone who watches a demonstration can explain what the system would do to a repo, and why, without reading code.
- The system is ready to switch on against the live org (R2) with no redesign.

## Definition of good enough

From the R1 exit test in [roadmap.md](../docs/roadmap.md):

- The loop runs end to end, read-only, on the pilot: it classifies, compares and routes, and writes the wiki pages
  and sample issue texts as local files. Nothing is written to the pilot repos.
- Tests for the requirements above pass in Actions on every PR, and every marked cell of the coverage grid has its
  check (R-10).
- Draft kinds and rules exist as data, and changing them and re-running shows what changes.
- The read-only fit analysis of all of the org's repos exists.
- The policy basis review (D-9) exists, and the policies put to the maintainers come from it.
- This repo is in Open-MBEE, and a change with invalid data can't land on `main` (R-14).
- All three demonstration flows (reader, operator, governor) have been given.
- The maintainers have approved, each recorded by a merged PR in this repo *(default)*:
  - the taxonomy;
  - the policies, based on the taxonomy;
  - the pilot subset of repos in the registry;
  - the assigned kind of each repo in it;
  - the named maintainers (GitHub usernames), who become this repo's CODEOWNERS.
- The org governance check (R-15) has run on the pilot snapshot.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

Every default was decided by the supervisor (see [WP0-decisions.md](WP0-decisions.md)). The ones that remain in the text, marked *(default)*:

- R-9's check: inspect the scopes of each credential the program is configured with.
- R-11: a rerun on an unchanged gap posts no new comment, as well as opening no new issue.
- R-12's check: a reclassification on the pilot changes exactly one entry in the canonical kind list.
- R-13: how a repo's status rolls up from its controls (any red → red; else any yellow → yellow; else green), and
  the status is shown in words as well as color.
- Pilot tests run on stored snapshots of the pilot repos. The failure, repeat-run, invalid-change and
  reclassification cases are built from those snapshots.
- The agent proposes the pilot subset and each repo's kind from read-only data. The supervisor reviews the proposal
  before it goes to the maintainers.
- Each maintainer approval is recorded by a merged PR in this repo.
- The org policy (D-8) is approved as part of "the policies", not as a separate approval.
- The org gets its own wiki page and a row on the index, with its status.
- R-13: an attestation is out of date once it is older than the repo's latest release.
- R-17: where a tier needs an owner, the owner is the repo's CODEOWNERS, and only a CODEOWNER's attestation counts.
- Repos archived before the archive policy existed are compliant as they are, because they can't be edited.
- D-4: each issue carries a registry label plus one label per policy, which the wiki's issue links filter on.
- R-14: the program's own status-log commits are checked against the meta-rules the same way as a person's.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop: 55 decided, 0 deferred, and the items raised along the way
are marked *raised* in [WP0-decisions.md](WP0-decisions.md), which holds every record.

# Design overview

> **DRAFT.** Nothing here is locked until mzargham says "lock." Requirement IDs are stable handles for
> discussion. Their content is not settled.

## Purpose

Keep one authoritative, auditable record of every repo in the `Open-MBEE` GitHub org: its category,
who is responsible for it, and which controls that category implies. Then drive each repo toward
those controls with a deterministic control loop. The record and the loop serve three ends:

1. **Navigability.** Newcomers and the community manager can see which repos are highlighted (in active
   development, or trusted and maintained) and which are exploratory or historical.
2. **Demonstrable oversight.** OpenMBEE can show regulated adopters that permissions and release
   approval follow written rules, aligned with CISA *OSS Security Principles and Practices* (2026-07-30).
3. **Friction only where it is needed, and visibly so.** Media and research stay easy to contribute to. Tools carry the
   strictest controls. For every repo it is clear which controls are in effect and which aren't, and that the prescribed
   ones really are in effect (PO-10).

**Success** is staged ([roadmap](roadmap.md)). The system has succeeded when it is **canonical** (R3), the
source of truth for repo status, and shows the **desired steady-state behavior** (R4). High error at
first deployment is expected, not a failure. Success is measured by the error being visible, owned and
routed. Error being low at the start is not part of the measure.

## Architecture

The **plant** is activity on the Open-MBEE GitHub org. The **controller** is this repo. The model is
represented control-theoretically. What people read is presented in plain language (X-4).

### Four parts

| Part | Role | Stands alone? | Requirements |
|---|---|---|---|
| Formal model | Abstract loop: observe → classify → compare → correct. It has four slots: taxonomy, policy, sensors, actuators. | No. It needs the slots filled. | [formal-model.md](requirements/formal-model.md) |
| Taxonomy | State-space structure: the classes and their membership rules. | No. Data for the model. | [taxonomy.md](requirements/taxonomy.md) |
| Policy | The reference: assigned values per class (references to GitHub-native configurations) and a correction channel per attribute. | No. Data for the model. | [policy.md](requirements/policy.md) |
| Closed-loop behavior | What actually happens. It emerges from the design plus the humans taking part. | Observed, not coded. | [closed-loop.md](requirements/closed-loop.md) |

Interfaces are specified in [interfaces.md](requirements/interfaces.md).

### Assumption (mzargham)

OpenMBEE's organizational policies can be implemented and stored in GitHub. This repo only needs to
define and reference them. Implementation means configuring the policy in GitHub, then checking that it
is in effect on the repos assigned to have it.

### Notation

Measured `y ∈ Y`, asserted `z ∈ Z`, attribute space `U = Y × Z`. The control output (assigned values)
lives in `U` on purpose. Observed and assigned values differ, and the error is the gap. Alignment means
bringing **observed** into line with **assigned**.

### Roles, planes and interfaces

There are three roles, defined by activity, each with its own interface. One person can hold several roles. All
interfaces are inside GitHub, so the system stays self-contained there.

| Role (activity) | Plane | Interface | What happens there |
|---|---|---|---|
| **Reader**: finds and understands repos | — (read-only) | **Wiki** of this repo | Generated from controller state each run: 1 index page, 1 page per class, 1 page per repo. Never hand-edited. |
| **Operator**: brings a repo into conformance | Operations | **Issues in their own repo**, plus **direct edits** to that repo | The system files instructions (change requests, attestation requests) as issues in the repo they concern. Operators act in their own repo: they edit it (sensed on the next pass) and close the issue to assert the task is done. |
| **Governor**: sets and tunes the rules | Policy (controller tuning) | **This repo**: PR → review → merge, its own issues, and *ideally* an org **Project board** aggregating every issue the system has written across the org | Changes to taxonomy, policy and implementation; assigning repos to classes; the exclude list. Items needing a policy decision (`unclassified`, taxonomy review) are issues here. Low friction before canonical (R1–R2). From its first canonical release (R3): CODEOWNERS (OpenMBEE maintainers) only, with multiple approving reviews to merge to `main` (IF-9). |

### Stakeholders → roles (draft, for iteration)

| Stakeholder | Needs | Role(s) |
|---|---|---|
| Newcomers and users | Which repos to trust and use, who to ask | Reader |
| Contributors | How to contribute to a given repo, and how strict it is | Reader |
| Regulated adopters and auditors | Evidence that permissions and releases follow written rules | Reader (wiki, governance history) |
| Repo owners | What their repo must do, and which tasks are open | Operator, Reader |
| Release officers | Which releases they must approve, and under which rules | Operator, Reader |
| Community manager | One place to point people. A view of what's unowned or unknown | Reader; Governor view (Project board) |
| OpenMBEE maintainers | Set and change the rules with an auditable trail, and see org-wide progress | Governor |

## Requirement conventions

Each requirement table has the columns ID · requirement · source · assessed by. Sources:
**M** = mzargham (design sessions), **S** = the Slack post that started this, **E** = org evidence
(below), **C** = CISA guidance (below).

## Cross-cutting requirements

| ID | Requirement | Src | Assessed by |
|---|---|---|---|
| X-1 | No LLM in sensing, classifying, deciding or acting. | M | Code review; dependency list |
| X-2 | Same inputs → same outputs. Each run stores its input snapshot. | M | Replay a stored snapshot and diff the outputs |
| X-3 | No actuator can delete a repo. Archive or make private instead. | S | Actuator list inspection |
| X-4 | Everything a non-specialist reads uses plain language and no notation. | M | Cold read by a non-specialist |
| X-5 | Every input and every action records who made it and when, using git and GitHub's own records (commits, PRs, reviews, issues, comments). | M | Trace back from any assertion or action to a GitHub username |
| X-6 | A policy-plane PR shows a consequence preview before merge: which classes change and which actions would follow. | M | Preview appears on a test PR |
| X-7 | Every actor is a known, named actor identified by a GitHub username: owners, release officers, operators, governors, and the system itself (a named bot or App identity). Roles are assigned to usernames. | M | Every role assignment resolves to an existing GitHub user |
| X-8 | Every permission and authority mechanism (who can do what) is git or GitHub native. The org maintains its permissioned groups (org and repo roles, teams) separately. This system **assumes** they are in use, **may prescribe** how they're used (for example, policy can require CODEOWNERS, required reviews or a given team's access), and **never reimplements** anything git or GitHub already provides. | M | Inventory of mechanisms used: every one is native, and none is duplicated in this repo |
| X-9 | `repo-registry` is a registered repo under its own policy: an exploratory class in R1–R2, then, from its first canonical release (R3), a class at least as strict as the strictest class. | M | Its own wiki page shows its class and verdicts |
| X-10 | **Fail safe.** If a run fails or can't trust its inputs (expired credential, rate limit, partial sensing), it takes no actions. It keeps the last good wiki, marked stale with the reason, and notifies the maintainers through GitHub-native means (an issue in this repo addressed to them). | M | Fixture run with a sensing failure: no actions, stale banner, one notification |

## Design decisions and their justification

| Decision | Why | Reqs |
|---|---|---|
| Assigned values live in the same space as observed values | Conformance becomes a direct comparison, which keeps it legible | FM-5 |
| `unknown` and `unclassified` are distinct and first-class | Missing facts need attestation (no power), while misfit repos need policy change. Different people, different triggers | FM-3, FM-4, FM-6 |
| Taxonomy and policy are data, not code | Tuning shouldn't break the loop | FM-2 |
| Policies are GitHub-native configurations, referenced from here | Nothing is reimplemented, and enforcement is GitHub's own. This repo's job is assignment plus checking that the configuration is in effect | PO-6, PO-7 |
| Identity, permission and audit are git/GitHub native | One trust root that regulated adopters can inspect, with no parallel bureaucracy | X-5, X-7, X-8 |
| Two planes | Day-to-day governance happens in GitHub without editing this repo's taxonomy, policy or code. Rule changes need maintainer review of this repo | FM-9 |
| Scheduled sensing, event-driven policy checks | Actions can't see other repos' events without a GitHub App, and compute is constrained | CL-7, X-6, E |
| Actuation off at start | The initial error is large (E), and a bad initial condition shouldn't spread | CL-6 |
| Wiki generated from controller state | Navigation stays consistent with the controller. One page per repo and per class keeps things legible | IF-1, IF-2 |
| Interfaces split by activity (reader / operator / governor) | Each role gets a UX built for what it does, and nobody has to wade through another role's surface | Roles table above |
| Operator instructions land in the operator's own repo | Operators work where they already are. Closing the issue is the completion signal | IF-3, IF-6 |
| An aggregating Project board for governors | Org-wide progress in one view, without moving issues out of their repos | IF-10 |
| Governance friction rises at the first canonical release (R3), together with the self-class | Calibration needs fast iteration. A source of truth needs high-friction governance. The lifecycle resolves the apparent paradox | IF-9, X-9 |
| Operators are CODEOWNERS where the class requires it | Strict oversight rests on GitHub-native review authority held by the named people, not on a parallel list | PO-9, X-8 |
| Friction is explicit, not universal | Most repos stay low friction. Where friction exists, it is named, justified by the policy, and confirmed to be in effect | PO-10, PO-7 |
| Test and demonstrate on a hypothetical case first | The live system starts with expected high error, and maintainers must agree on the rules before go-live | FM-11, [testing](testing-and-demonstration.md) |

### Scope answers (mzargham)

- **Registry boundary.** By default every repo in `Open-MBEE` is in scope, forks included. An explicit
  **exclude list** is a fail-safe against scope explosion, used only when needed for a repo that doesn't fit the
  taxonomy, and kept transparently. → TX-5.
- **Authority to assign a class.** Governors only. Assigning or changing a repo's class, and putting a repo on the
  exclude list, are governor actions in this repo. → FM-5, TX-5.
- **Accepted deviations.** Governor-approved and standing: recorded in this repo per repo and control, with a reason
  and the approving governor, with no expiry, and reviewable at any time. → PO-8, FM-5.
- **Self-governance.** `repo-registry` is itself a registered repo. It sits in an exploratory class while it is being
  built and calibrated (R1–R2), and at its first canonical release (R3) it moves to a class at least as strict as the
  strictest class. → X-9.
- **Controller failure.** Fail safe: take no actions, mark the wiki as stale, and notify the maintainers. → X-10.

## Evidence (snapshot 2026-10-17, read-only `gh api graphql`)

- 183 repos: 29 archived, 24 forks, 3 private. Of the 154 live repos, about 58 non-fork repos had commits in the last 12 months.
- Out of 154 live repos: CODEOWNERS 7, SECURITY.md 10, CONTRIBUTING 21, CI 46, any release 28, release ≥ 1.0 13.
- Populations: core tools, clients and plugins, packaging, websites, example models, research, agent skills, org
  meta, and 24 forks of upstream projects (`fprime`, `helix`, …). The forks are the first test for TX-4.
- A GitHub wiki is a separate git repo (`<repo>.wiki.git`). `gh` has no wiki commands, so publishing means a
  `git push` from Actions. Wiki editing can be restricted to collaborators.
- Not yet checked: which GitHub-native policy features (for example org-level rulesets) the org's plan provides.
  That bounds PO-6.
- Not yet measured: which repos have issues disabled (needed for IF-4). mzargham's `gh` token lacks the `project`
  scope that IF-10's board would need.
- mzargham is an org `member`. The org defines no custom properties. Branch protection needs admin to read.
- **CISA guidance** (*Open Source Software: Security Principles and Practices*, 2026-07-30, 31 pp.). It is written for
  federal agencies as OSS consumers and producers, so it bears on OpenMBEE in two ways. These are inputs to policy design, not decisions:
  - *How adopters will judge OpenMBEE repos:* the **C4 Framework** (App. A, pp. 24–26) assesses *how* software is
    produced under four categories: Codebase, Community, Conduct, Configuration. It asks for **measurable** criteria,
    often collected by tools such as OpenSSF Scorecard, CHAOSS and Hipcheck. Conduct examples: a vulnerability disclosure
    policy, required code review, whether maintainers merge their own commits, license, code of conduct. Our
    measured attributes can be chosen to match what adopters measure.
  - *Producer practices with direct counterparts here* (pp. 15–18): README, LICENSE, CONTRIBUTING.md and SECURITY.md
    (VDP and security contact); an SBOM with each release; secret detection and dependency scanning in CI; keep commit
    history; keep contribution requirements minimal; and for end-of-support projects, mark them clearly (in GitHub,
    archive) and point to known forks.
  - It also describes machine-readable source-code inventories (pp. 13–15, App. B–C, code.json). The registry is one in
    effect, so an export in that shape is an R5 candidate.

## Parked (content; for later design sessions)

- Where attested facts land and in what format (for example issue-form fields, a comment syntax, or custom
  properties), constrained by IF-5 and IF-8.
- The number of required reviews from R3 on.
- The class set (X-9 needs an exploratory class that `repo-registry` itself fits). Y and Z for R1.
- Calibration targets for the R2 exit.
- The class→controls table and its mapping to C4 criteria and the CISA producer practices.
- `0.x` vs `1.0.0` release review.
- GitHub App vs admin token (the actuator writes issues across the org).
- Which classes forks fall into (they are in scope by default).
- IF-6 draft: whether the next sense pass reopens an issue that was closed without the fix.

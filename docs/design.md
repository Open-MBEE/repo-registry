# Design overview

> **DRAFT.** Nothing here is locked until mzargham says "lock." Requirement IDs are stable handles for
> discussion. Their content is not settled.
>
> Brought in line with the decision records at the WP4b docs sweep (2026-10-18). Each changed item says
> "(updated: <record>)". A1 to A4 are the WP0 amendments ([WP0-decisions](../work-packages/WP0-decisions.md),
> [WP1 amendment 2](../work-packages/WP1-amendment-2.md)). The consistent summary is
> [current-state.md](current-state.md); where anything here disagrees with a decision record, the record wins.

## Purpose

Keep one authoritative, auditable record of every repo in the `Open-MBEE` GitHub org: its kind (its type,
lifecycle stage and tier), who is responsible for it, and which policies are in effect for it. Then drive each
repo toward those policies with a deterministic control loop *(updated: WP0 A1)*. The record and the loop serve
three ends:

1. **Navigability.** Newcomers and the community manager can see which repos are highlighted (incubating or
   graduated) and which are sandbox or archived *(updated: A4)*.
2. **Demonstrable oversight.** OpenMBEE can show regulated adopters that permissions and release
   approval follow written rules, aligned with CISA *OSS Security Principles and Practices* (2026-07-30) and
   NIST SP 800-37 Rev. 2 (the RMF) with SP 800-53 *(updated: WP0 "NIST RMF as a second core citation")*.
3. **Friction only where it is needed, and visibly so.** Media and research stay easy to contribute to. Strictness
   follows the tier: graduated tools and governance are high, incubating tools and media people rely on are medium,
   sandbox tools and research are low, archived repos are none *(updated: A4)*. For every repo it is clear which
   policies are in effect and which aren't, and that the prescribed ones really are in effect (PO-10).

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
| Taxonomy | State-space structure: the kinds (type × lifecycle stage, each in one tier) and the rules that recommend a kind *(updated: WP0 A1, A4)*. | No. Data for the model. | [taxonomy.md](requirements/taxonomy.md) |
| Policy | The reference: named policies, each with an applies-if rule on type, lifecycle stage or tier, referencing GitHub-native configurations. Gaps go out as change requests; there is no automatic channel yet *(updated: WP0 A1, Tension 3)*. | No. Data for the model. | [policy.md](requirements/policy.md) |
| Closed-loop behavior | What actually happens. It emerges from the design plus the humans taking part. | Observed, not coded. | [closed-loop.md](requirements/closed-loop.md) |

Interfaces are specified in [interfaces.md](requirements/interfaces.md).

### Assumption (mzargham)

OpenMBEE's organizational policies can be implemented and stored in GitHub. This repo only needs to
define and reference them. Implementation means configuring the policy in GitHub, then checking that it
is in effect on the repos it applies to.

### Notation

Measured `y ∈ Y`, asserted `z ∈ Z`, attribute space `U = Y × Z`. The control output (assigned values)
lives in `U` on purpose. Observed and assigned values differ, and the error is the gap. Alignment means
bringing **observed** into line with **assigned**.

### The model

*(updated: WP0-decisions "The model, stated precisely")* Measurements and attestations about a repo yield three
categorical attributes: its **type** (tool, media, research, governance), its **lifecycle stage** (Sandbox,
Incubating, Graduated, Archived) and its **tier** (high, medium, low, none), which is set by type and stage. Each
policy's applies-if rule reads only those three, so together they decide which policies are in effect. A **kind** is
a named point in that attribute space, and a **policy** is a region of it; a repo's policies are the regions its
point falls in. "repo → kind → tier → policies" is only the high-level summary.

### Roles, planes and interfaces

There are three roles, defined by activity, each with its own interface. One person can hold several roles. All
interfaces are inside GitHub, so the system stays self-contained there.

| Role (activity) | Plane | Interface | What happens there |
|---|---|---|---|
| **Reader**: finds and understands repos | — (read-only) | **Wiki** of this repo | Generated from controller state each run: an index page, one page per kind, per tier and per policy, and views of the registry by kind, tier and policy, with each repo's red / yellow / green status and links to the repo and its open registry issues. No page per repo *(updated: WP0 D-3, "Wiki downscope")*. Never hand-edited. |
| **Operator**: brings a repo into conformance; the repo's CODEOWNERS *(updated: WP0 R-17)* | Operations | **Issues in their own repo**, plus **direct edits** to that repo | The system files change requests as issues in the repo they concern (in R1, sample issue texts only, not posted). Operators act in their own repo: they edit it (sensed on the next pass), answer attested checks in its README attestation block, and close the issue to assert the task is done *(updated: WP0 "Compliance", R-13)*. A kind-change PR is an operator's only action in this repo (WP0 OD3). |
| **Governor**: sets and tunes the rules; the named maintainers, and the owners among them | Policy (controller tuning) | **This repo**: PR → review → merge, its own issues, and *ideally* an org **Project board** aggregating every issue the system has written across the org | Changes to taxonomy, policy and implementation; the exclude list. Any maintainer merges a kind change; an owner merges changes to the maintainer list and accepted exceptions *(updated: WP4b OD3)*. Items needing a policy decision (`unclassified`, taxonomy review) are issues here. Low friction before canonical (R1–R2): in R1 the only restriction is the valid-`main` check (WP0 R-14). From its first canonical release (R3): CODEOWNERS (OpenMBEE maintainers) approval to merge to `main`; the number of reviews is parked (IF-9). |

### Stakeholders → roles (draft, for iteration)

| Stakeholder | Needs | Role(s) |
|---|---|---|
| Newcomers and users | Which repos to trust and use, who to ask | Reader |
| Contributors | How to contribute to a given repo, and how strict it is | Reader |
| Regulated adopters and auditors | Evidence that permissions and releases follow written rules | Reader (wiki, governance history) |
| Repo operators (its CODEOWNERS) *(updated: WP0 R-17)* | What their repo must do, and which tasks are open | Operator, Reader |
| Holders of release authority (recorded in the maintainer list) *(updated: maintainer-policy item 12)* | Which releases they must approve, and under which rules | Operator, Reader |
| Community manager | One place to point people. A view of what's unowned or can't be told (yellow) | Reader; Governor view (Project board) |
| OpenMBEE maintainers | Set and change the rules with an auditable trail, and see org-wide progress | Governor |

## Requirement conventions

Each requirement table has the columns ID · requirement · source · assessed by. Sources:
**M** = mzargham (design sessions), **S** = the Slack post that started this, **E** = org evidence
(below), **C** = CISA guidance (below). Policies now cite two core sources, CISA and the NIST RMF with SP 800-53,
plus secondary ones: the OpenSSF security baseline (the backbone for policies) and lifecycle, the CNCF lifecycle, and
ISO/IEC/IEEE 12207 by clause *(updated: WP0 "NIST RMF as a second core citation"; WP1-decisions "Secondary
citations")*.

## Cross-cutting requirements

| ID | Requirement | Src | Assessed by |
|---|---|---|---|
| X-1 | No LLM in sensing, classifying, deciding or acting. | M | Code review; dependency list |
| X-2 | Same inputs → same outputs. Each run stores its input snapshot. | M | Replay a stored snapshot and diff the outputs |
| X-3 | No actuator can delete a repo. Archive or make private instead. | S | Actuator list inspection |
| X-4 | Everything a non-specialist reads uses plain language and no notation. | M | Cold read by a non-specialist |
| X-5 | Every input and every action records who made it and when, using git and GitHub's own records (commits, PRs, reviews, issues, comments). | M | Trace back from any assertion or action to a GitHub username |
| X-6 | A policy-plane PR shows a consequence preview before merge: which kinds and policies in effect change and which actions would follow *(updated: WP0 A1)*. | M | Preview appears on a test PR |
| X-7 | Every actor is a known, named actor identified by a GitHub username: operators (each repo's CODEOWNERS), maintainers and owners (governors), holders of release authority, and the system itself (a named bot or App identity). Roles are assigned to usernames *(updated: WP0 R-17; maintainer-policy)*. | M | Every role assignment resolves to an existing GitHub user |
| X-8 | Every permission and authority mechanism (who can do what) is git or GitHub native. The org maintains its permissioned groups (org and repo roles, teams) separately. This system **assumes** they are in use, **may prescribe** how they're used (for example, policy can require CODEOWNERS, required reviews or a given team's access), and **never reimplements** anything git or GitHub already provides. | M | Inventory of mechanisms used: every one is native, and none is duplicated in this repo |
| X-9 | `repo-registry` is a registered repo under its own policy. It is governance/sandbox, which is high tier now. Only its review friction waits: from its first canonical release (R3), merging to `main` needs CODEOWNERS approval (expected gap XF-2) *(updated: WP1-decisions G-2; A4)*. | M | Its entry in the kind list, and its status in the wiki views |
| X-10 | **Fail safe.** If a run fails or can't trust its inputs (expired credential, rate limit, partial sensing), it takes no actions. It keeps the last good wiki, marked stale with the reason, and notifies the maintainers through GitHub-native means (an issue in this repo addressed to them). | M | Fixture run with a sensing failure: no actions, stale banner, one notification |

## Design decisions and their justification

| Decision | Why | Reqs |
|---|---|---|
| Assigned values live in the same space as observed values | Conformance becomes a direct comparison, which keeps it legible | FM-5 |
| `unclassified` is a first-class outcome; `unknown` is a check result (yellow, "can't tell"), not a kind *(updated: WP0 OD3, R-13)* | Every repo gets an inferred kind. A repo no kind fits needs a policy change, while a fact the sensor can't read needs an attestation. Different people, different triggers | FM-3, FM-4, FM-6 |
| Taxonomy and policy are data, not code | Tuning shouldn't break the loop | FM-2 |
| Policies are GitHub-native configurations, referenced from here | Nothing is reimplemented, and enforcement is GitHub's own. This repo's job is the applies-if rules plus checking that the configuration is in effect | PO-6, PO-7 |
| Identity, permission and audit are git/GitHub native | One trust root that regulated adopters can inspect, with no parallel bureaucracy | X-5, X-7, X-8 |
| Two planes | Day-to-day governance happens in GitHub without editing this repo's taxonomy, policy or code. Rule changes need maintainer review of this repo | FM-9 |
| Scheduled sensing, event-driven policy checks | Actions can't see other repos' events without a GitHub App, and compute is constrained | CL-7, X-6, E |
| Actuation off at start | The initial error is large (E), and a bad initial condition shouldn't spread | CL-6 |
| Wiki generated from controller state | Navigation stays consistent with the controller. Pages per kind, tier and policy, with views by each, keep it legible at low hundreds of repos; there is no page per repo *(updated: WP0 D-3)* | IF-1, IF-2 |
| Interfaces split by activity (reader / operator / governor) | Each role gets a UX built for what it does, and nobody has to wade through another role's surface | Roles table above |
| Operator instructions land in the operator's own repo | Operators work where they already are. Closing the issue is the completion signal | IF-3, IF-6 |
| An aggregating Project board for governors | Org-wide progress in one view, without moving issues out of their repos | IF-10 |
| Review friction on this repo rises at the first canonical release (R3); its tier is high from the start *(updated: WP1-decisions G-2; A4; XF-2)* | Calibration needs fast iteration. A source of truth needs high-friction governance. The lifecycle resolves the apparent paradox | IF-9, X-9 |
| Operators are the repo's CODEOWNERS wherever the tier needs an owner (high, medium, low) *(updated: WP0 R-17)* | Strict oversight rests on GitHub-native review authority held by the named people, not on a parallel list | PO-9, X-8 |
| Friction is explicit, not universal | Most repos stay low friction. Where friction exists, it is named, justified by the policy, and confirmed to be in effect | PO-10, PO-7 |
| Test and demonstrate on a pilot of real repos, read-only, with sample issues not posted *(updated: WP0-decisions "Change before approval: a pilot of real repos")* | The live system starts with expected high error, and maintainers must approve the rules on real repos before go-live | FM-11, [testing](testing-and-demonstration.md) |

### Scope answers (mzargham)

- **Registry boundary.** The full scope is every repo in `Open-MBEE`. In R1 the registry is a pilot of 24 to 36 real
  repos (32 proposed), and every other public repo is on the **exclude list** with a reason, kept transparently
  *(updated: WP0 "pilot"; WP4)*. Forks have no kind yet and are `unclassified`; excluding forks by default is a
  fit-analysis candidate. → TX-5.
- **Authority to assign a kind.** Every repo gets an inferred initial kind, which is guidance. Its operators propose a
  change by PR to this repo, and any maintainer merges it; this is an operator's only action here *(updated: WP0 OD3;
  WP4b OD3)*. Putting a repo on the exclude list is a governor action in this repo. → FM-5, TX-5.
- **Accepted deviations.** Approved and standing: recorded in this repo per repo and policy, with a reason and the
  approver, by a PR that an owner merges *(updated: WP4b OD3)*, with no expiry, and reviewable at any time. Its status
  is green, marked as an accepted exception (WP0 R-13). → PO-8, FM-5.
- **Self-governance.** `repo-registry` is itself a registered repo. It is governance/sandbox, which maps to high, while
  it is being built and calibrated (R1–R2). At its first canonical release (R3) its review friction rises to
  CODEOWNERS approval *(updated: WP1-decisions G-2; A4; XF-2)*. → X-9.
- **Controller failure.** Fail safe: take no actions, mark the wiki as stale, and notify the maintainers. → X-10.

## Evidence (snapshot 2026-10-17, read-only `gh api graphql`)

*(updated: the current snapshot is `data/snapshots/2026-10-18/`: 184 repos, 181 public, 3 private counted only; see
[fit-analysis.md](fit-analysis.md). The counts below are from the first snapshot and are kept as the record.)*

- 183 repos: 29 archived, 24 forks, 3 private. Of the 154 live repos, about 58 non-fork repos had commits in the last 12 months.
- Out of 154 live repos: CODEOWNERS 7, SECURITY.md 10, CONTRIBUTING 21, CI 46, any release 28, release ≥ 1.0 13.
- Populations: core tools, clients and plugins, packaging, websites, example models, research, agent skills, org
  meta, and 24 forks of upstream projects (`fprime`, `helix`, …). The forks are the first test for TX-4.
- A GitHub wiki is a separate git repo (`<repo>.wiki.git`). `gh` has no wiki commands, so publishing means a
  `git push` from Actions. Wiki editing can be restricted to collaborators.
- Checked since: OpenMBEE is on GitHub Free. Every policy declares the plans it works on; immutable releases and
  rulesets are confirmed for the org; Enterprise-only features are listed for the future in
  `data/policies/_future.yaml`, never required *(updated: WP3-decisions G-3)*. That bounds PO-6.
- Not yet measured: which repos have issues disabled (needed for IF-4). mzargham's `gh` token lacks the `project`
  scope that IF-10's board would need.
- mzargham is an org `member`. The org defines no custom properties. Branch protection needs admin to read; this is
  expected gap XF-1, closed by a sensing credential with *Administration: read* in WP6 *(updated:
  `data/expected-gaps.yaml`)*.
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

- ~~Where attested facts land and in what format.~~ Resolved: in a README attestation block in the repo, committed by
  a code owner, out of date once older than the latest release *(WP0 "Compliance", R-13, R-17)*.
- The number of required reviews from R3 on.
- ~~The class set.~~ Resolved: the kinds in `data/taxonomy/kinds.yaml` (14 defined, 2 omitted with reasons);
  `repo-registry` is governance/sandbox *(WP1; A2, A4)*. Y and Z for R1: the measurements in the stored snapshot and
  the attestations named in each policy's SOP.
- Calibration targets for the R2 exit.
- ~~The class→controls table.~~ Resolved: the policies and their applies-if rules
  ([policy-applicability.md](policy-applicability.md)), mapped to CISA and the NIST RMF in
  [policy-basis-review.md](policy-basis-review.md) *(WP2; WP0 A1)*.
- ~~`0.x` vs `1.0.0` release review.~~ Resolved: 1.0.0 is the Sandbox → Incubating seam (low → medium) *(A4)*.
- GitHub App vs admin token (the actuator writes issues across the org).
- Which kinds forks fall into: none yet; they are `unclassified`, and excluding them by default is a candidate
  ([fit-analysis.md](fit-analysis.md)).
- IF-6 draft: whether the next sense pass reopens an issue that was closed without the fix.

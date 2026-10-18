# Current state

> The consistent basis to start from. Written at the docs sweep after WP4 (2026-10-18), and kept current with each
> package's pull request. **Where this file and an
> older design document disagree, this file and the decision records it cites win.** The design documents in `docs/`
> (design, roadmap, requirements, testing) are early DRAFT inputs. The docs sweep (WP4b, accepted 3f2c557) edited them in
> place to match the decisions and kept them DRAFT (WP4b OD1).
> Everything below is PROVISIONAL until the OpenMBEE maintainers approve it (the five approvals, below).

## How the work is governed

- Work runs in gated work packages: `work-breakdown` → `scope-of-work` (approval) → `work-execution` →
  `work-acceptance` (acceptance). See [AGENTS.md](../AGENTS.md).
- **Supervisor:** mzargham. Approval and acceptance are his merge, with a merge commit, of the scope or delivery
  pull request into `main` (WP5 OD3). Up to WP5's approval they were his local `git merge --no-ff` commits. Decision
  records quote him verbatim in `work-packages/WPn-decisions.md`.
- Commits carry no AI co-author trailer. The repository is
  [Open-MBEE/repo-registry](https://github.com/Open-MBEE/repo-registry) (public: on GitHub Free, only a public
  repository can require a check). `main` requires the check `check`, with no bypass, so no invalid state reaches it
  (WP0 R-14). Org writes are run by the supervisor from commands an agent hands him (WP5 OD4).

## What is decided, and where

| Topic | Now | Recorded in |
|---|---|---|
| Architecture | **Model, view, controller, with CI/CD** (WP5b). The **model** is the repository's records, declared as the tables of a database in [data/schema/model.yaml](../data/schema/model.yaml): each table's key, columns and foreign keys. Repositories are keyed by GitHub's repository ID, people by GitHub's user ID, kinds by (type, stage); the kind name `type/stage` is derived shorthand. The **controller** is the Python: `scripts/validate.py` admits only correctly constructed records (CI), and the render pipeline builds every **view** from the model. Views are never committed; they are rendered deterministically, in **demo mode** for now, into an ephemeral `build/demo/` (the plant simulated before the controller is turned on). CD publishes them only from a `main` that CI has passed: live mode publishes the wiki (WP5d, run by the supervisor; from CI in WP7), and issues come with WP6 | [WP5b](../work-packages/WP5b-scope-of-work.md), [WP5b-decisions](../work-packages/WP5b-decisions.md) |
| Two kinds of error | A **construction error** (a malformed record, a broken key or join, broken software) is invalid: CI rejects it. A **compliance error** (a repository out of line with a policy) is the controller's error signal: valid, kept, and remediated through the feedback loop; never a CI failure. Construction controls are listed with their tests in `data/controls.yaml`; known compliance non-passes in `data/measured-gaps.yaml`; capabilities not built yet in `data/forthcoming.yaml` | [WP5b-decisions](../work-packages/WP5b-decisions.md) "Check-in" |
| Scope | Through R1: show how the taxonomy and policies work on a pilot of real repositories, writing nothing to them; get five maintainer approvals | [WP0](../work-packages/WP0-scope-of-work.md) |
| Citations | Core: CISA *OSS Security Principles and Practices* (2026), NIST SP 800-37 Rev. 2 (RMF) with SP 800-53, and OpenSSF (its project lifecycle, the source of the stages, and its security baseline, the backbone for policies). Secondary: CNCF lifecycle, ISO/IEC/IEEE 12207:2026 by clause only. Added in WP5e: the DoD CIO memo *Software Development and Open Source Software* (2022), core; OFAC's sanctions, NIST SP 800-218 (SSDF) and NIST SP 800-161 Rev. 1, secondary. Every source is quoted verbatim in `data/sources/`, except ISO/IEC/IEEE 12207 (licensed: clause numbers and titles only) | [WP5e-decisions](../work-packages/WP5e-decisions.md) "OD4", "OD6"; [WP0-decisions](../work-packages/WP0-decisions.md) "NIST RMF as a second core citation"; [WP2](../work-packages/WP2-scope-of-work.md); [WP1-decisions](../work-packages/WP1-decisions.md) "Secondary citations"; [WP1-amendment-3](../work-packages/WP1-amendment-3.md) |
| The model | Measurements and attestations about a repository yield **three categorical attributes**: its **type**, its **lifecycle stage**, and its **tier** (derived from type and stage). Each policy's applies-if rule reads only those three, so together they determine which policies are in effect (A1). A **kind** is a named point in that three-dimensional attribute space; because the tier is determined by type and stage, the defined kinds are a small set of valid points. **A policy is a region of the space** (its applies-if rule), and a repository's policies are the regions its point falls in. "repo → kind → tier → policies" is the high-level summary only; the real dependency isn't that linear | WP0 A1; [WP1](../work-packages/WP1-scope-of-work.md); supervisor at the docs sweep |
| Types | tool, media, research, governance (governance: `repo-registry` and the org's administration, the same type at different stages: the org is graduated, `repo-registry` is in sandbox) | WP0 A2; [WP1-amendment-3](../work-packages/WP1-amendment-3.md) |
| Stages | Sandbox, Incubating, Graduated, Archived, adopted from CNCF and OpenSSF. A tool moves Sandbox → Incubating at 1.0.0. Graduated is never recommended; maintainers assign it | WP0/WP1 A4; [lifecycle-stage-map](lifecycle-stage-map.md) |
| Tiers | high (graduated tools, governance/graduated), medium (incubating tools, media people rely on, governance/incubating), low (named owner only, including governance/sandbox), none (archived). Governance friction rises with the stage; governance/graduated carries the org policies and the repository policies | A4; [WP1-amendment-3](../work-packages/WP1-amendment-3.md); `data/taxonomy/tiers.yaml` |
| Kind assignment | Each kind-list entry has a **source** (WP5c OD1): `inferred` (the rules' candidate), `topic` (its code owners declared the type with one `openmbee-<type>` GitHub topic; the rules give the stage) or `maintainer` (a maintainer's merged decision, with the decision it records). Precedence: inferred, then topic, then maintainer; rules and topics never change a maintainer entry. A kind change is a pull request to this repo, merged by any maintainer; the refresh view lists the candidates the rules would change | [WP5c-decisions](../work-packages/WP5c-decisions.md); [WP1-amendment-6](../work-packages/WP1-amendment-6.md); [WP4b-decisions](../work-packages/WP4b-decisions.md) "OD3" |
| A kind is not a compliance verdict | Lifecycle is a category; whether its duties are done is checked by policies | [WP1-decisions](../work-packages/WP1-decisions.md) |
| Policies | Repository policies (including `license-by-type`) and org policies, each a file in `data/policies/` with its scope, citations, applies-if rule, checks and set-up steps; the set's status is stored once (`_set.yaml`). Each SOP is rendered from its policy, never written by hand | `data/policies/`; [policy-format](policy-format.md); [policy-basis-review](policy-basis-review.md) (narrative; its tables are rendered) |
| Plans | OpenMBEE is on GitHub Free. Every policy declares `available_on`; immutable releases and rulesets are confirmed for the org; Enterprise-only features are listed for the future, never required | [WP3-decisions](../work-packages/WP3-decisions.md); `data/sources/github-plan.yaml`; `data/policies/_future.yaml` |
| Attestations | One `ATTESTATIONS.yaml` per repository, at its root, pointed to from the README. Read at the commit of the latest release; an entry counts only if it names that release and the file's last change was by a code owner. With no release, the default branch counts and doesn't go out of date. The org's attestations are in this repository's file | [WP0-amendment-3](../work-packages/WP0-amendment-3.md); [attestations-format](attestations-format.md) |
| Status colors | green known compliant, yellow can't tell, red known non-compliant; an accepted exception is green, marked | WP0 R-13; `data/deviations.yaml` |
| Org governance | Owners are the root authority, 2 to 3 of them, a subset of the maintainers; maintainers can be more and are checked by the owners | [WP3-decisions](../work-packages/WP3-decisions.md); [maintainer-policy](maintainer-policy.md) |
| Who merges what | A kind change: any maintainer. The maintainer list and maintainers' powers: an owner. An accepted exception (`data/deviations.yaml`): an owner | [WP4b-decisions](../work-packages/WP4b-decisions.md) "OD3" |
| Operators | A repository's operators are its CODEOWNERS, sensed from the repo; every repo in a tier that needs an owner (high, medium, low) needs one, and only a code owner's attestation counts | WP0 R-17; [WP0-decisions](../work-packages/WP0-decisions.md) "Sweep gap 1" |
| Named maintainers | `aftimg` (Chris Delp), `mzargham` (Michael Zargham), `rkarban` (Robert Karban), `HuiJun` (Jason Han; OpenSysML release authority); a starting target of 5 | `data/maintainers.yaml` |
| Verified code owners | High tier only: a code owner of a high-tier repository must be a named maintainer whom an org owner (another person) has verified out of band in the last 12 months: identity; not a sanctioned party, nor located or ordinarily resident in a comprehensively sanctioned jurisdiction; no affiliation with an organization of concern. Not nationality. The record in `data/maintainers.yaml` publishes legal name, country of residence and affiliation, with the maintainer's consent; absence is non-conformance (the error signal, XF-3). Contributors: nothing more now | [WP5e](../work-packages/WP5e-scope-of-work.md); [WP5e-decisions](../work-packages/WP5e-decisions.md) |
| Privacy | Concealed org members are counted, never named; the match check never reveals a concealed role | [WP3-decisions](../work-packages/WP3-decisions.md) "OD1"; `scripts/privacy_check.py` |
| Wiki | Two layers on one wiki, both views. **The review pack (WP5d):** the what and why of compliance, so the maintainers can agree on the taxonomy and the policies: the taxonomy in plain words, every repository's kind, tier and source, every policy with where it is in effect and its SOP, and the sources each policy comes from; every row links to its model file, and a change is a pull request to it. Published by the supervisor from a validated `main` (`scripts/render.py --mode live`). **The compliance dashboard (WP7):** extends the pack with status, aware of each repository's state against the controls (colors per repository and policy, from WP6's sensing), and how to come into demonstrable compliance; it builds on the pack's definitions. Pages per kind, tier and policy, with views by each; no page per repo | [WP0-decisions](../work-packages/WP0-decisions.md) "Wiki downscope"; [WP5d-decisions](../work-packages/WP5d-decisions.md) |
| Pilot | A pilot of real repositories, kept as a model table (`data/pilot.yaml`, WP5b OD6): written once by the pilot rule, changed only by a governed pull request; everything else on the exclude list (`data/exclude.yaml`) with a reason. The rule's current proposal and the pilot briefing are views | [WP4](../work-packages/WP4-scope-of-work.md); `data/pilot-rule.yaml` |

## The five maintainer approvals (WP8)

1. The taxonomy (`data/taxonomy/`). 2. The policies (`data/policies/`). 3. The pilot subset (`data/pilot.yaml`).
4. Each pilot repository's kind (`registry.yaml`). 5. The named maintainers
(`data/maintainers.yaml`), who become this repository's CODEOWNERS (`data/proposed-codeowners`, not live yet).

**The fifth comes first** (WP5f): the owners and maintainers govern every other policy, so who they are is settled
before the other four. Until then `data/maintainers.yaml` is a placeholder, and everything in the repository is
demonstrative: drawn from data with the intent to be realistic, but not a decision.

## Packages

| WP | What | State |
|---|---|---|
| WP0 | Project scope through R1 | approved 1dccb62; amendments 3c72b7d (WP0 A1–A2, WP1 A1–A3), 3edae32 (A4) |
| WP1 | Kinds and tiers | accepted bcb1e73 |
| WP2 | Policies | accepted 1ced09b |
| WP2a | License by type | accepted 61a3db6 |
| WP3 | Org governance | accepted 3c0ba20 |
| WP4 | Fit analysis and pilot | accepted 1408259 |
| WP4b | Docs sweep and checkpoint | accepted 3f2c557 |
| WP4c | The governance kinds; OpenSSF as a core citation | accepted 4cad812 |
| WP4d | The attestations file | accepted caaca38 |
| WP4e | Type and stage in the kind list | accepted 63e270f |
| WP5 | Meta-rule checks in CI; move to Open-MBEE | accepted 6938aa5 ([#1](https://github.com/Open-MBEE/repo-registry/pull/1)) |
| WP5b | The model, its integrity, and views out of the model (MVC, demo mode) | accepted 9e14099 ([#6](https://github.com/Open-MBEE/repo-registry/pull/6)) |
| WP5c | Taxonomy refinements from WP4's fit analysis | accepted 42ecec0 ([#9](https://github.com/Open-MBEE/repo-registry/pull/9)) |
| WP5d | The maintainer review pack, published to the wiki: the what and why of compliance | accepted c0d8979 ([#11](https://github.com/Open-MBEE/repo-registry/pull/11)); first published from 5bb4b61 |
| WP5e | Verified code owners for high-tier repositories; every source quoted verbatim | accepted 5bb4b61 ([#12](https://github.com/Open-MBEE/repo-registry/pull/12)) |
| **WP5f** | Owners and maintainers first (critical path): the co-founders decide who the owners (2 or 3) and maintainers are, and the supervisor records it; carrying out the changes of control is later work | **scoped** ([WP5f-scope-of-work](../work-packages/WP5f-scope-of-work.md)) |
| WP6 | Engine: sensing (credential set up here, WP5 OD6), status, status log, sample issues | planned |
| WP7 | The compliance dashboard: the wiki extended with each repository's status against the controls, and how to come into compliance (builds on WP5d and WP6); and publishing the wiki automatically from CI after each merge (until then an owner runs live mode by hand) | planned |
| WP8 | Demonstrations and the five maintainer approvals | planned |

## Known gaps and candidates

- **Measured gaps** (`data/measured-gaps.yaml`, the error signal): XF-2, `repo-registry` doesn't pass `change-review`
  (no approving review required until R3); XF-3, `.github` doesn't pass `verified-code-owners` (no maintainer has a
  verification yet, WP5e).
- **Forthcoming** (`data/forthcoming.yaml`, capabilities not built): XF-1, the sensing credential with
  *Administration: read* (set up and closed in WP6).
- **Taxonomy:** the fit report view (`build/demo/fit-report.md`) gives the unclassified repositories by reason. After
  WP5c: mirrors (forks with no changes of ours), live repositories with no type signal, and archived ones with no type.
  Code owners can classify theirs with an `openmbee-<type>` topic.
- **Who may approve changes (raised at WP5d as contributor sourcing; WP5e):** the `verified-code-owners` policy for
  the high tier restricts who may approve and merge, not who may contribute: it is where the personnel control
  resolves. `contributing` is about what is contributed, not who contributes.
  Every quoted item of the new sources is cited by a policy (a citation sweep; `contributing` also asks how
  contributions are reviewed and tested, with the supervisor's approval). Candidates for later: counsel's review of
  the sanctions criterion; NIST SP 1326. **A sanctions floor for contributors** (for example, no contributions from
  SDN-listed parties) was raised and declined for now: it is implementable only with a means of screening OpenMBEE is
  prepared to opt into, and control at code review, by verified code owners, is adequate ([WP5e-decisions](../work-packages/WP5e-decisions.md)). For WP6 (the
  engine): turning a verification's age into its color (expired after 12 months), and checking that a maintainer's
  facts were added by their own commit (their consent), from the commit author's GitHub login.
- **Open for the maintainers:** the off-list and missing licenses (the license view); the should-be-archived
  repositories; maintenance of the heavily used `exec-*` tools.

## How to check everything

Everything runs in one locked environment: Python 3.10 and PyYAML 6.0.3, pinned in `pyproject.toml`, `.python-version`
and `uv.lock` (WP5 review, G-1), so every machine and CI run the same thing. Install it once with `uv sync --frozen`.
The required check on every pull request runs these two commands (`.github/workflows/check.yml`):

```bash
uv run python scripts/validate.py
uv run python -m unittest discover -s tests
```

`validate.py` checks every table against `data/schema/model.yaml` (keys, columns and types, foreign keys, disjoint
tables), the rules that span tables, and the taxonomy and policy meta-rules; then it renders every view twice and
fails if the two differ. Invalid fails; out of compliance passes. The tests include a check that every relative link
resolves, that every cited commit resolves, and that every audit finding (`scripts/audit.py`) stays fixed.

To see every view, as it would be published (demo mode writes only into `build/demo/`, ignored by git):

```bash
uv run python scripts/render.py
```

The wiki pages are in `build/demo/wiki/`. To publish them to the wiki (the supervisor runs it, from a clean `main`
equal to `origin/main` that validates; anything else is refused; it fetches `origin/main` first, which writes
nothing to GitHub):

```bash
uv run python scripts/render.py --mode live
```

A change of kind is one edit to `registry.yaml`; nothing needs regenerating, because views are rendered from the model
on every run. `scripts/recommend.py` drafts what the rules alone would give (`build/demo/kind-list-draft.yaml`), a
candidate, never a decision. Live, read-only: `scripts/snapshot.py`, `scripts/org_snapshot.py`,
`scripts/usage_snapshot.py`, `scripts/privacy_check.py` (the working tree), `scripts/history_privacy_check.py`
(everything a push would publish).

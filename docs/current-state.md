# Current state

> The consistent basis to start from. Written at the docs sweep after WP4 (2026-10-18). **Where this file and an
> older design document disagree, this file and the decision records it cites win.** The design documents in `docs/`
> (design, roadmap, requirements, testing) are early DRAFT inputs. The docs sweep (WP4b, accepted 3f2c557) edited them in
> place to match the decisions and kept them DRAFT (WP4b OD1).
> Everything below is PROVISIONAL until the OpenMBEE maintainers approve it (the five approvals, below).

## How the work is governed

- Work runs in gated work packages: `work-breakdown` → `scope-of-work` (approval) → `work-execution` →
  `work-acceptance` (acceptance). See [AGENTS.md](../AGENTS.md).
- **Supervisor:** mzargham. Approval and acceptance are his `git merge --no-ff -m "<message>"` of the scope or work
  branch into `main`. Decision records quote him verbatim in `work-packages/WPn-decisions.md`.
- Commits carry no AI co-author trailer. The repository is local; it moves to Open-MBEE in WP5, only on the
  supervisor's explicit go-ahead.

## What is decided, and where

| Topic | Now | Recorded in |
|---|---|---|
| Scope | Through R1: show how the taxonomy and policies work on a pilot of real repositories, writing nothing to them; get five maintainer approvals | [WP0](../work-packages/WP0-scope-of-work.md) |
| Citations | Core: CISA *OSS Security Principles and Practices* (2026) and NIST SP 800-37 Rev. 2 (RMF) with SP 800-53. Secondary: OpenSSF security baseline (the backbone for policies) and lifecycle, CNCF lifecycle, ISO/IEC/IEEE 12207:2026 by clause only | [WP0-decisions](../work-packages/WP0-decisions.md) "NIST RMF as a second core citation"; [WP2](../work-packages/WP2-scope-of-work.md); [WP1-decisions](../work-packages/WP1-decisions.md) "Secondary citations" |
| The model | Measurements and attestations about a repository yield **three categorical attributes**: its **type**, its **lifecycle stage**, and its **tier** (derived from type and stage). Each policy's applies-if rule reads only those three, so together they determine which policies are in effect (A1). A **kind** is a named point in that three-dimensional attribute space; because the tier is determined by type and stage, the defined kinds are a small set of valid points. **A policy is a region of the space** (its applies-if rule), and a repository's policies are the regions its point falls in. "repo → kind → tier → policies" is the high-level summary only; the real dependency isn't that linear | WP0 A1; [WP1](../work-packages/WP1-scope-of-work.md); supervisor at the docs sweep |
| Types | tool, media, research, governance (governance: only `repo-registry` and the org's administration) | WP0 A2 |
| Stages | Sandbox, Incubating, Graduated, Archived, adopted from CNCF and OpenSSF. A tool moves Sandbox → Incubating at 1.0.0. Graduated is never recommended; maintainers assign it | WP0/WP1 A4; [lifecycle-stage-map](lifecycle-stage-map.md) |
| Tiers | high (graduated tools, governance), medium (incubating tools, media people rely on), low (named owner only), none (archived) | A4; `data/taxonomy/tiers.yaml` |
| Kind assignment | Inferred initial kind (guidance). Changed by a pull request to this repo, merged by any maintainer; an operator's only action here | [WP0-decisions](../work-packages/WP0-decisions.md) "OD3"; WP1 A3; [WP4b-decisions](../work-packages/WP4b-decisions.md) "OD3" |
| A kind is not a compliance verdict | Lifecycle is a category; whether its duties are done is checked by policies | [WP1-decisions](../work-packages/WP1-decisions.md) |
| Policies | 21: 16 repository policies (including `license-by-type`) and 5 org policies; each with an SOP, citations and an applies-if rule | `data/policies/`; [policy-applicability](policy-applicability.md); [policy-basis-review](policy-basis-review.md) |
| Plans | OpenMBEE is on GitHub Free. Every policy declares `available_on`; immutable releases and rulesets are confirmed for the org; Enterprise-only features are listed for the future, never required | [WP3-decisions](../work-packages/WP3-decisions.md); `data/sources/github-plan.yaml`; `data/policies/_future.yaml` |
| Status colors | green known compliant, yellow can't tell, red known non-compliant; an accepted exception is green, marked | WP0 R-13; `data/deviations.yaml` |
| Org governance | Owners are the root authority, 2 to 3 of them, a subset of the maintainers; maintainers can be more and are checked by the owners | [WP3-decisions](../work-packages/WP3-decisions.md); [maintainer-policy](maintainer-policy.md) |
| Who merges what | A kind change: any maintainer. The maintainer list and maintainers' powers: an owner. An accepted exception (`data/deviations.yaml`): an owner | [WP4b-decisions](../work-packages/WP4b-decisions.md) "OD3" |
| Operators | A repository's operators are its CODEOWNERS, sensed from the repo; every repo in a tier that needs an owner (high, medium, low) needs one, and only a code owner's attestation counts | WP0 R-17; [WP0-decisions](../work-packages/WP0-decisions.md) "Sweep gap 1" |
| Named maintainers | `aftimg` (Chris Delp), `mzargham` (Michael Zargham), `rkarban` (Robert Karban), `HuiJun` (Jason Han; OpenSysML release authority); a starting target of 5 | `data/maintainers.yaml` |
| Privacy | Concealed org members are counted, never named; the match check never reveals a concealed role | [WP3-decisions](../work-packages/WP3-decisions.md) "OD1"; `scripts/privacy_check.py` |
| Wiki (WP7) | Pages per kind, tier and policy, and views by each; no page per repo; colors and issue links per repo | [WP0-decisions](../work-packages/WP0-decisions.md) "Wiki downscope" |
| Pilot | 32 real repositories ([pilot-briefing](pilot-briefing.md)); everything else on the exclude list with a reason | [WP4](../work-packages/WP4-scope-of-work.md); `data/pilot.yaml`; `data/exclude.yaml` |

## The five maintainer approvals (WP8)

1. The taxonomy (`data/taxonomy/`). 2. The policies (`data/policies/`). 3. The pilot subset (`data/pilot.yaml`).
4. Each pilot repository's kind (`registry.yaml`, `data/assignments.yaml`). 5. The named maintainers
(`data/maintainers.yaml`), who become this repository's CODEOWNERS (`data/proposed-codeowners`, not live yet).

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
| **WP5** | Meta-rule checks in CI; move to Open-MBEE (explicit go-ahead) | **next**, not yet scoped |
| WP6 | Engine: sensing, status, status log, sample issues | planned |
| WP7 | Wiki | planned |
| WP8 | Demonstrations and the five maintainer approvals | planned |

## Known gaps and candidates

- **Expected failures** (`data/expected-gaps.yaml`): XF-1 sensing credential with *Administration: read* (WP6);
  XF-2 `repo-registry` passes `change-review` (R3).
- **Taxonomy candidates** ([fit-analysis](fit-analysis.md)): exclude forks by default; declare type with a GitHub
  topic; better word and file signals; a default for archived repositories with no type; `.github` as governance.
- **Open for the maintainers:** three off-list licenses and 32 unlicensed repositories (license report); the
  should-be-archived repositories; maintenance of the heavily used `exec-*` tools.

## How to check everything

```bash
python3 -m unittest discover -s tests
```

57 tests (including a check that every relative link resolves), 2 expected failures. Generators (each replays
exactly from the stored snapshot): `scripts/recommend.py`, `scripts/policies.py`, `scripts/licenses.py`,
`scripts/org.py`, `scripts/pilot.py`, `scripts/briefing.py`. Live, read-only: `scripts/snapshot.py`,
`scripts/org_snapshot.py`, `scripts/usage_snapshot.py`, `scripts/privacy_check.py`.

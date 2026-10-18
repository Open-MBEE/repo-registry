> WP4b D-1. Drift report from the read-only audit of 2026-10-18, before the fixes. Each item is fixed in WP4b (see WP4b-review.md).

# Docs sweep: drift report (repo-registry, branch `docs-sweep`, read-only audit, 2026-10-18)

Scope: README.md, AGENTS.md, docs/ (design, roadmap, testing, requirements/*, generated and explanatory docs,
sops/*), data/ header comments, plus WP scope docs where they contradict their own amendments. Each finding gives
file:line, the stale text, what is now true, and the authority. Severity: **H** = contradicts a recorded decision a
reader would act on; **M** = lags or misleads; **L** = terminology, labels, small inconsistencies.

Verification notes (things the brief asked me to check, where the brief itself was off):
- **Policies: 21, not 19.** `data/policies/` holds 21 policy files (16 repository policies incl. `license-by-type`,
  5 org policies: `org-two-factor`, `org-few-owners`, `org-base-permission`, `maintainers-match`,
  `governance-roles-named`), plus `_departures.yaml` and `_future.yaml`. status.md says 16 + 5, which is right.
- **Remote:** confirmed none (`git remote -v` is empty). status.md is correct.
- **Broken relative links:** none. Every `](path)` and `#anchor` link in *.md resolves. Code-formatted paths that
  don't exist are all intentional (`docs/CODEOWNERS`, `docs/LICENSE` as examples; `config/sensing.yaml` as XF-1's
  future evidence).
- **Snapshot:** `meta.json` says 184 repos in all, 181 public, 3 private (counted only).
- **Tests:** 56 `def test` across tests/*.py; XF-1 and XF-2 are the two expected gaps.
- An untracked `docs/current-state.md` appeared during the audit (being written concurrently); see the last section.

---

## 1. docs/requirements/*.md (DRAFT) — 23 findings

These five files are wholesale pre-WP0. Recommend marking them superseded rather than editing row by row.

### policy.md
| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 20 (PO-9) **H** | "operators (its owner and, where assigned, its release officer) ... listed in that repo's CODEOWNERS ... set per class" | Operators **are** the repo's CODEOWNERS, sensed from the repo, authoritative; required wherever the tier needs an owner (high, medium, low) | WP0 Direction "Operators are named in each repo", R-17; WP0-decisions "Sweep gap 1"; `codeowners` policy |
| 13 (PO-2) **H** | "Strictness: tool > media > research." | Strictness follows tier, set by type × stage: tool/sandbox is low (3 policies, same as research), media tops out at medium, governance and graduated tools are high | WP1-amendment-2 A4; data/taxonomy/kinds.yaml; policy-applicability.md |
| 14 (PO-3) **H** | "Tool classes in active development or maintenance also assign a release officer." | Stages are Sandbox/Incubating/Graduated/Archived. Release authority is named for incubating/graduated tools in `data/maintainers.yaml` (`release_authority`) | A4; maintainer-policy.md item 12 |
| 15 (PO-4) **M** | "Every control cites the CISA practice or C4 criterion ... or says none" | Every policy cites CISA **and** the RMF task / SP 800-53 control (or "none"), plus secondary sources | WP0 R-16, "Two core citations"; WP2 R-3; policy-format meta-rule 7 |
| 6, 12 (PO-1) **M** | "For each class: assigned values ... and a correction channel for each constrained attribute" | Policies are named files with an applies-if rule on type, lifecycle or tier; no per-class value table; no automatic channel | WP0 A1; WP0-decisions Tension 3 (automatic fixes are future work) |
| 21 (PO-10) **M** | "Each repo's wiki page shows every prescribed control" | No page per repo; views by kind/policy/tier show each repo's status and links | WP0 D-3; WP0-decisions "Wiki downscope" |
| 16 (PO-5) **L** | "Each class's wiki page" | "kind" | WP0 terminology |

### taxonomy.md
| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 17-19 **H** | "kind ∈ {tool, media, research} × lifecycle ∈ {active development, maintained, exploratory, archived}" | Kind = type × stage; types tool/media/research/governance; stages Sandbox/Incubating/Graduated/Archived; 14 kinds defined, 2 omitted with reasons. Note this line also uses "kind" to mean *type* | WP0 A2, A4; WP1 D-2; kinds.yaml |
| 11 (TX-1) **M** | "(Draft: ≤ 8 classes.)" | Cap dropped | WP1-decisions OD3 follow-up ("i dont think we need at most 8 kinds") |
| 15 (TX-5) **H** | "Excluding a repo is a fail-safe for misfits, used only when needed." | R1 registry is a pilot of 24–36 real repos; **every other repo** is on the exclude list with a reason (150 today) | WP0 Direction "Pilot", D-5; WP4 D-3; data/exclude.yaml |
| 14 (TX-4) **M** | "Validated against the hypothetical case" | Validated by the fit analysis of all public repos and the real pilot | WP0 D-5, D-6; fit-analysis.md |
| 6, 11-12 **L** | "classes" throughout | "kinds" | WP0 |

### interfaces.md
| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 11 (IF-1) **H** | "one page per class, one page per repo" | Pages per kind, per policy, per tier; views by each; no page per repo | WP0 D-3, "Wiki downscope" |
| 12 (IF-2) **M** | "every repo with its class, owner, release officer and open-issue count" | Kind and CODEOWNERS; highlighted = incubating or graduated | WP0-decisions "README reader section brought in line"; WP1-amendment-2 defaults; README L73-74 |
| 15 (IF-5) **M** | "Every request for a fact says exactly where to answer" (implied: in the issue) | Attestations are a README attestation block, committed by a code owner, out of date once older than the latest release | WP0 Direction "Compliance", R-13; every SOP "How to attest" |
| 19 (IF-9) **M** | "merging to main needs multiple approving reviews. The self-class change (X-9) happens at the same moment." | R3 switches to CODEOWNERS approval (number of reviews still parked). repo-registry is already governance/sandbox (high) now; the friction gap is XF-2 | WP0 non-goals; WP0-decisions "How restrictive this repo is in R1"; data/expected-gaps.yaml XF-2 |

### formal-model.md
| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 15 (FM-4) **M** | "exactly one class, or `unknown` (incomplete info), or `unclassified`" | Every repo gets an inferred kind or `unclassified` with a reason; no `unknown` kind | WP0-decisions OD3 (replaces "a new repo starts as unknown"); WP1 R-5; kind-list-format rule 5-6 |
| 17 (FM-6) **M** | "routes to ... automatic, change request, or attestation" | Automatic fixes are a non-goal (future work) | WP0 Non-goals; Tension 3 |
| 18 (FM-7) **M** | "Repo wiki pages show error age" | No repo pages | WP0 D-3 |
| 22 (FM-11) **M** | "a **hypothetical plant**: a fixture org snapshot" | Pilot tests run on stored snapshots of the real pilot repos (toy fixtures survive only for the R-6 swap) | WP0 D-5 and defaults; tests/fixtures/ |
| 14 (FM-2) **L** | "The model names no class, attribute ..." | Code deliberately names the three kind attributes (`KIND_ATTRS = ("type","lifecycle","tier")`, scripts/policies.py:25); WP1 R-7 is "the rule engine names no kind" | WP0 A1; WP1 R-7 |

### closed-loop.md
| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 15 (CL-5) **L** | "one issue per repo × attribute" | At most one open issue per gap, labelled registry + one label per policy | WP0 R-11, D-4 default |
| 16 (CL-6) **L** | "turned on per class" | per kind | WP0 |

---

## 2. docs/design.md (DRAFT) — 20 findings

| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 60 **H** | "1 index page, 1 page per class, 1 page per repo" | No page per repo; pages per kind/policy/tier + views | WP0 D-3, "Wiki downscope" |
| 109 **H** | "One page per repo and per class keeps things legible" | Same | WP0 D-3 |
| 116 **H** | "Test and demonstrate on a hypothetical case first" | Pilot of 24–36 real repos, read-only, sample issues not posted | WP0-decisions "Change before approval: a pilot of real repos" |
| 114 **H** | "Operators are CODEOWNERS where the class requires it" | Operators are the CODEOWNERS wherever the tier needs an owner | WP0 R-17 |
| 94 (X-9), 127-129 **H** | "an exploratory class in R1–R2, then ... a class at least as strict as the strictest class" | repo-registry is governance/sandbox, which maps to **high** now; only its review *friction* waits for R3 (XF-2) | WP1-decisions G-2; WP1-amendment-2 A4; data/assignments.yaml; expected-gaps XF-2 |
| 113 **M** | "together with the self-class" | No self-class change at R3; the change at R3 is the CODEOWNERS approval switch | as above |
| 120-122 **H** | "every repo in Open-MBEE is in scope, forks included. An explicit exclude list ... used only when needed" | Pilot plus everything else excluded. Forks have no kind and are unclassified | WP0 "Pilot"; WP4; kinds.yaml `unclassified_reasons` |
| 123-124 **M** | "Authority to assign a class. Governors only." | Inferred initial kind for every repo; operators propose changes by PR; governors (maintainers) merge; an operator's only action here | WP0-decisions OD3; WP1 A3 |
| 8-9 **M** | "its category ... which controls that category implies" | Kind gives type, stage, tier; policies attach to any of the three | WP0 A1 |
| 12-13 **M** | "highlighted repos (in active development, or trusted and maintained)" | Highlighted = incubating or graduated | WP1-amendment-2 Agent's defaults |
| 15, 80 **M** | Cites only CISA; sources M/S/E/C | CISA **and** NIST SP 800-37 Rev. 2 are core; OpenSSF baseline (backbone), CNCF, ISO 12207 secondary | WP0 "Two core citations"; WP2 Sources |
| 16-17 **M** | "Tools carry the strictest controls" | Only graduated tools and governance are high; sandbox tools are low | A4 |
| 35-36 **M** | "the classes and their membership rules"; "assigned values per class ... correction channel per attribute" | kinds; named policies with applies-if rules | WP0 A1 |
| 61 **M** | "attestation requests" filed as issues | Attestations live in the operator's README | WP0 "Compliance" |
| 62, 72, 92 **M** | "Release officers" as a stakeholder and actor; "assigning repos to classes" | Operators = CODEOWNERS; release authority is a maintainer-policy record | WP0 R-17; maintainer-policy.md 12-13 |
| 102 **L** | "`unknown` and `unclassified` are distinct and first-class" | `unknown` survives only as a check result (yellow, "can't tell"), not as a kind | WP0 R-13, OD3 |
| 134-135 **L** | "183 repos: 29 archived, 24 forks, 3 private ... 154 live" (snapshot 2026-10-17) | Snapshot 2026-10-18: 184 repos, 181 public, 25 forks | data/snapshots/2026-10-18/meta.json; fit-analysis.md |
| 140-141 **M** | "Not yet checked: which GitHub-native policy features ... the org's plan provides" | Org is on GitHub Free; immutable releases and rulesets confirmed; Enterprise-only features in `_future.yaml` | WP3-decisions G-3 and follow-ups; data/sources/github-plan.yaml |
| 144 **L** | "Branch protection needs admin to read." | Now expected gap XF-1 (sensing credential with Administration: read, WP6) | data/expected-gaps.yaml |
| 159-170 (Parked) **M** | "The class set", "class→controls table", "`0.x` vs `1.0.0` release review", "Which classes forks fall into" | Resolved: WP1 kinds; WP2 applicability table; A4 seam Sandbox→Incubating; forks unclassified (fit-analysis rec. 1: exclude by default) | WP1, WP2, A4, WP4 |

---

## 3. README.md — 10 findings

| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 118-119 **H** | "Demonstrate: run on a made-up example organization" | R1 runs read-only on a pilot of real repos (32 proposed) | WP0-decisions "Change before approval"; WP0 Purpose; pilot-briefing.md |
| 92-93 **H** | "the operators (owner and release officer) must also be listed in that repository's CODEOWNERS" | The operators **are** the CODEOWNERS, for every tier that needs an owner | WP0 R-17, "Operators are named in each repo" |
| 3-4 **M** | "This repository currently holds only the design" | It holds provisional data, policies, SOPs, scripts, tests and the pilot proposal | status.md |
| 20-21 **M** | "Tools get the strictest rules. Media ... and research get lighter ones" | Strictness is by tier; sandbox tools are low; governance is high. Contradicts README's own L43-46 | A4; policy-applicability.md |
| 88-90 **M** | "If it asks you a question ... the issue says exactly where to answer" | Attested checks are answered in a README attestation block by a code owner | WP0 "Compliance"; SOPs |
| 129-136 **M** | "Design documents" lists the DRAFT docs as the design | The contract is WP0 and the WP scopes; the DRAFT docs are superseded inputs. No link to status.md, policy-applicability.md, pilot-briefing.md or the SOPs | WP0 "Direction decided while scoping" |
| 76 **L** | "one page per tier, which says which policies are in effect for it" | Policies attach to type, stage or tier, so a tier page can't list all of them (the kind page can) | WP0 A1; WP0 grid R-16 × D-3 |
| 106-108 **L** | "several approvals are needed" | WP0 records only the switch to CODEOWNERS approval at R3; the number of reviews is parked | WP0 non-goals; design.md Parked |
| 51-54 **L** | "It runs in GitHub Actions ... opens GitHub issues" | No remote yet; in R1 issue texts are local files, not posted | WP0 Non-goals; status.md |
| 13-15 **L** | "under active development, ... well maintained ..., experiments" | Plain-language echo of the old lifecycle; could map to the four stages | A4 |

---

## 4. docs/roadmap.md (DRAFT) — 10 findings

| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 11-12 **H** | "runs end to end on the hypothetical case ... with fixture bindings (FM-11)" | Runs read-only on the real pilot, from stored snapshots | WP0 good-enough; D-5 |
| 16 **M** | "Both demonstrations have been given." | Three flows: reader, operator, governor | WP0-decisions D-5; WP0 good-enough |
| 17 **H** | "*Exit:* the maintainers have agreed on a taxonomy and policy" | Five approvals (taxonomy, policies, pilot subset, each pilot repo's kind, named maintainers), each a merged PR; plus repo in Open-MBEE with the valid-main check, the fit analysis, the policy basis review, the org check | WP0 good-enough (which claims to be "From the R1 exit test in roadmap.md", but roadmap was never updated to match) |
| 25 **H** | "Governors have assigned classes to the highlighted repos. Everything else is `unknown`." | Every repo gets an inferred initial kind; changes by PR | WP0-decisions OD3 |
| 63 **H** | R5: "Non-binding, deterministic class suggestions from measurements" | Already done in R1 (WP1 `recommend_when`, registry.yaml) | WP1 D-2, D-5 |
| 37 **M** | "Every tool in active development or maintenance has a release officer (PO-3)" | Stages changed; release authority per maintainer-policy | A4; maintainer-policy 12 |
| 38 **M** | "cites the CISA practice or C4 criterion" | CISA + RMF/SP 800-53 per policy | WP0 R-16 |
| 43 **M** | "`repo-registry` moves to a class at least as strict as the strictest class (X-9)" | Already governance/sandbox (high); R3 changes friction only | WP1 G-2, A4; XF-2 |
| 26, 29, 36 **L** | "per class", "repos' classes", "Every repo has a class" | kind | WP0 |
| (missing) **M** | R1 doesn't mention the move to Open-MBEE | Move during R1, in WP5, on the supervisor's go-ahead | WP0-decisions "Remote during R1"; status.md |

---

## 5. docs/testing-and-demonstration.md (DRAFT) — 5 findings (supersede whole)

| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 6-8 **H** | "run on a **hypothetical case** ... a small made-up org" | Pilot of 24–36 real repos; tests on stored snapshots | WP0-decisions "Change before approval" |
| 12 **H** | "A small fixture org (draft: about 10 repos)" | 32 proposed real repos | WP4; pilot-briefing.md |
| 17 **M** | "one `unknown` repo (missing facts)" | No `unknown` kind | WP0 OD3 |
| 35-40 **M** | "for two audiences"; "repo owners, release officers" | Three flows (reader, operator, governor); operators = CODEOWNERS | WP0 D-5 |
| 16, 29 **L** | "every class" | kind | WP0 |

---

## 6. docs/policy-basis-review.md (PROVISIONAL, WP2 D-1) — 7 findings

L8 claims "The trace tables below are generated from `data/`", but no script writes this file and the tables lag the data.

| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 129, 133 **H** | CISA-P-LICENSE-PERMISSIVE and CISA-P-LICENSE-FILE "carried by project-files" | Carried by `license-by-type`; `project-files` cites only CISA-P-README | WP2a D-2; data/policies/license-by-type.yaml, project-files.yaml |
| 42-44 **H** | "Not confirmed ...: plan availability of immutable releases" | Confirmed by the supervisor for the org; rulesets too | WP3-decisions G-3 final follow-up; github-plan.yaml `confirmed_in_org` |
| 88 **M** | TI-3 "Adopted by workflow-least-privilege" | Also `org-few-owners` and `org-base-permission` | WP3 R-3; their `cites.openssf` |
| 160 **M** | CISA-C4-COMMUNITY "carried by codeowners" | Also `maintainers-match`, `governance-roles-named` | their `cites.cisa` |
| 46-65 **M** | "The proposed policy set": 16 rows | 21 policies; the 5 org policies (WP3) are absent from the set and from the NIST table (AC-6(1), AC-6(5) missing at L171-194) | WP3 D-2; data/policies/ |
| 72-74 **L** | "`change-review` will show red until then" | Recorded as expected gap XF-2; cite it | data/expected-gaps.yaml |
| 246 **L** | "(WP0 PO-8)" | PO-8 is a DRAFT policy.md ID, not WP0's | docs/requirements/policy.md |

---

## 7. docs/lifecycle-stage-map.md (PROVISIONAL) — 4 findings

Every SOP links here ("the stages are explained in ..."), so its staleness reaches operators.

| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 3-4 **M** | "It goes into WP1 through amendment 2, which needs the supervisor's approval." | Approved (3edae32) | status.md; WP1-amendment-2.md |
| 63-67 **H** | "Decisions this map needs (not settled here)": tiers for tool/sandbox and tool/incubating | Settled: tool/sandbox **low**, tool/incubating **medium** | WP1-amendment-2.md decision records |
| 55 **H** | Sandbox rule: "Research and media with no other evidence" | Live media is recommended **Incubating**; media/sandbox is assigned only | WP1-amendment-2 Agent's defaults; kinds.yaml media/incubating |
| 60-61 **M** | "Media keeps the activity guide, Sandbox versus Incubating" | No activity rule for media; live media → incubating | same |

---

## 8. AGENTS.md — 6 findings

| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 50 **M** | "Code names no class and no attribute (FM-2)." | "kind"; code names the three kind attributes on purpose; the rule is "the engine names no kind, type or signal" | WP0 A1; WP1 R-7; kinds.yaml L10; scripts/policies.py:25 |
| 15-16 **M** | "Design lives in docs/"; "Every behavior traces to a requirement ID (X-, FM-, TX-, PO-, IF-, CL-)" | The contract is WP0 + WPn scopes, which override DRAFT docs; tests trace to WPn R-IDs (tests/test_wp*.py) | WP0 "Direction decided while scoping" |
| 68 **M** | "testing-and-demonstration.md: the hypothetical case" | Superseded by the pilot | WP0 |
| 21 **L** | "Everything in `docs/` is DRAFT until mzargham says lock" | docs/ now also holds accepted PROVISIONAL deliverables awaiting maintainer approval; the DRAFT vs PROVISIONAL distinction is unstated | AGENTS item 3; WP1-WP4 acceptances |
| 37 **L** | "until it moves to Open-MBEE during R1 (WP0)" | In WP5 | status.md; WP1-WP4 headers |
| 62-69 **L** | Map omits `work-packages/`, `data/`, and the current docs (policy-applicability, SOPs, pilot-briefing) | — | — |

---

## 9. docs/status.md — 3 findings

| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 35-37 **M** | Code list: snapshot, recommend, policies, org_snapshot, org, privacy_check | Also `licenses.py`, `pilot.py`, `briefing.py`, `usage_snapshot.py` (WP2a, WP4); missing comma after recommend.py | scripts/ |
| 7-9 **L** | "The documents in `docs/` are inputs." | Should say which docs are superseded DRAFT and which are current PROVISIONAL deliverables | WP0 |
| 62 **L** | Names XF-1 only | XF-2 also open (closes at R3) | expected-gaps.yaml |

## 10. docs/policy-format.md — 2 findings

| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 42-61 **H** | Meta-rules 1-11 | Missing the plan rule (`github.available_on` must include the org's plan, scripts/policies.py:102) and the `needs_research` rule (policies.py:99). The doc says WP5 enforces "every meta-rule below", so WP5 would inherit an incomplete list | WP3-decisions G-3 and follow-ups |
| 22-24 **L** | Shape omits `available_on` (and `needs_research`) under `github` | Present in every policy | data/policies/*.yaml |

## 11. docs/kind-list-format.md — 2 findings

| Line | Stale text | Now true | Authority |
|---|---|---|---|
| 8 **M** | "the tier's policies come in WP2" | Policies attach to type, stage or tier; see policy-applicability.md | WP0 A1; WP2 D-5 (the doc's own L7 already says A1) |
| 31 **L** | fprime reason "(WP0 parked item)" | WP0 has no parked items; the item is design.md Parked L169 | design.md |

## 12. Pilot data and pilot-briefing.md — 4 findings

| Location | Stale text | Now true | Authority |
|---|---|---|---|
| data/pilot.yaml (11 entries) **M** | `why: 'tools-heavily-used: tools at 1'`, `'... still below 1'` | Truncated at the "." in "1.0": scripts/pilot.py:65 uses `meaning.split('.')[0]`. A generator bug, visible in a maintainer-facing file | pilot-rule.yaml L27, L33 |
| docs/pilot-briefing.md:104 **M** | "Must include (3): Named by the supervisor" (lists repo-registry) | The supervisor named 6 repos; repo-registry was added by the agent (pilot.yaml also says "must-include (supervisor)" 7 times) | WP4-decisions OD1 |
| data/pilot-rule.yaml:12 **L** | "repo-registry registers itself (WP0 X-9)" | X-9 is a DRAFT design.md ID | design.md |
| docs/pilot-briefing.md:14 vs data **L** | "Kind = type / stage" | Data key is `lifecycle`; docs alternate "stage" and "lifecycle". Pick one in reader docs | kinds.yaml; policy-format.md |

## 13. Merge authority (internal inconsistency across newer docs) — 3 findings

| Location | Text | Conflict |
|---|---|---|
| docs/sops/maintainers-match.md:11 **M** | "pull requests to this repository, which the maintainers merge" | maintainer-policy.md:24-25: "An owner approves and merges it" (WP3-decisions G-2 outcome) |
| data/deviations.yaml:2-3 **M** | "recorded by a pull request that an owner merges" | No recorded decision gives owners the deviation merge. WP2a D-3 says "the approving maintainer", PO-8 says governors |
| docs/maintainer-policy.md:25-27 **L** | "GitHub enforces that approval through code-owner review" | Code-owner review enforces *any* CODEOWNER (all maintainers), not an *owner*. It doesn't enforce the owner-approves rule |

## 14. data/ header comments and generated reasons — 3 findings

| Location | Text | Now true |
|---|---|---|
| data/taxonomy/kinds.yaml:78, 213 → registry.yaml (25 entries), data/reports/kind-recommendations.yaml (25), fit-analysis.md:30 **L** | "The taxonomy has no kind for forks yet (WP0 parked item)." | WP0 has no parked items; it is design.md Parked L169. Fix at the source (kinds.yaml) and regenerate |
| data/deviations.yaml:2 **L** | "(WP0 PO-8)" | PO-8 is DRAFT policy.md (same mislabel in WP2a-scope L53, L79) |
| data/expected-gaps.yaml:6 **L** | XF-1 is repository "Administration: read" | org-governance-review.md L46 says the registry needs **owner-level** org read, "recorded as a known gap". XF-1 doesn't cover org-level reads (2FA requirement, base permission, outside collaborators). Either widen XF-1 or add an XF-3 |

## 15. Work-package scopes (approved records; don't edit, annotate if anything) — 5 findings

| Location | Text | Conflict |
|---|---|---|
| WP1-scope-of-work.md:33 **M** | "A kind maps to a tier. A tier maps to policies. Nothing skips a link." | Its own A1 (L52-53) and WP0 A1: policies attach to type, lifecycle or tier |
| WP1-scope-of-work.md:28-30 **L** | "That gives 12 kinds." | 16 in the cross product with governance; 14 defined, 2 omitted |
| WP1-scope-of-work.md:58 **L** | "WP2 must define it." | Orphaned sentence left by the A3 insertion |
| WP0-scope-of-work.md:226 vs 170 **L** | Grid: "Type, lifecycle and tier pages list the policies" | D-3 lists pages per kind, policy and tier (no type or lifecycle pages) |
| WP0-decisions.md:413-418 **L** | A2: "governance/experimental", "governance/maintained" | Superseded by A4 (governance/sandbox, governance/graduated). A verbatim record, so leave it, but there's no forward pointer. (WP3-scope L28 "kind → tier → policies" has the same pre-A1 wording.) |

## 16. docs/org-governance-review.md, fit-analysis.md, maintainer-policy.md, policy-applicability.md, SOPs

All match the data and decisions except the items above (merge authority; the XF-1 scope; the fork "WP0 parked
item" label). The counts check out: fit-analysis (182 = 137 + 45; tiers 78/37/21/1); pilot-briefing (32 =
6+5+6+4+6+2+3; kinds 1/6/4/8/11/2; tiers 15/14/1/2); policy-applicability (3/11/15/1/3/4/4/1/3/3/3/1/13/5). The
license-report counts (77 green / 38 red of 115) match policy-basis-review L248.

## 17. docs/current-state.md (untracked, appeared mid-audit) — 2 notes

- L48 "3c72b7d (A1–A3)": A3 is a WP1-only amendment (WP1-decisions "Amendment 1 to WP1"). WP0 carries A1, A2, A4.
- It states "where they have been superseded, they say so" (L5). That holds only once the DRAFT docs get the
  superseded banners recommended below.

---

## Counts by file

| File | Findings |
|---|---|
| docs/requirements/*.md (5 files) | 23 |
| docs/design.md | 20 |
| README.md | 10 |
| docs/roadmap.md | 10 |
| docs/policy-basis-review.md | 7 |
| AGENTS.md | 6 |
| docs/testing-and-demonstration.md | 5 |
| WP scope/decision docs | 5 |
| docs/lifecycle-stage-map.md | 4 |
| pilot data + pilot-briefing.md | 4 |
| docs/status.md | 3 |
| merge authority (SOP / deviations / maintainer-policy) | 3 |
| data/ headers and generated reasons | 3 |
| docs/policy-format.md | 2 |
| docs/kind-list-format.md | 2 |
| docs/current-state.md (untracked) | 2 |
| **Total** | **109** |

## Recommended structural actions

1. **Supersede, don't edit, the DRAFT design set.** Put a banner on design.md, roadmap.md, testing-and-demonstration.md
   and docs/requirements/*.md: "SUPERSEDED where it conflicts with WP0–WP4; see docs/current-state.md (or status.md)".
   Keep the requirement IDs as stable handles. testing-and-demonstration.md should be marked superseded in full by
   WP0 D-5 (the pilot), with only the toy-swap idea surviving (tests/fixtures).
2. **One supersession table** (in current-state.md or status.md) mapping each superseded concept to its decision: class→kind;
   lifecycle→stages (A4); unknown kind→inferred kind (OD3); hypothetical org→pilot; page per repo→views (D-3); release
   officer→CODEOWNERS + release_authority; exclude-on-misfit→exclude-all-but-pilot; CISA-only→CISA+RMF.
3. **Edit in place the live, reader-facing docs:** README (roadmap step 1, operators = CODEOWNERS, "only the design",
   strictness by tier, attestation location, Design-documents section), AGENTS (FM-2 wording, trace-ID rule, map),
   lifecycle-stage-map (status line, settled tiers, media rule), policy-format (plan and needs_research meta-rules,
   before WP5 enforces the list), kind-list-format L8, status.md code list.
4. **Make policy-basis-review's trace tables really generated** (or add a test that diffs them against `cites`). Then
   regenerate to pick up WP2a and WP3 (license practices, TI-3, C4-COMMUNITY, the org policies, the NIST controls).
5. **Fix the source, then regenerate:** the fork reason in kinds.yaml ("WP0 parked item"), and the `why` truncation in
   scripts/pilot.py:65. Mark repo-registry's must-include as agent-added in pilot-rule.yaml and the briefing.
6. **Decision gap for the supervisor (problem-level):** who merges deviation PRs and maintainer-list PRs. The
   maintainer policy says an owner; the maintainers-match SOP says the maintainers; deviations.yaml says an owner with
   no recorded decision. Also whether XF-1 should cover owner-level org reads.
7. **Prefix hygiene:** DRAFT IDs (PO-, X-, TX-, IF-, FM-, CL-) are cited as "WP0 PO-8" / "WP0 X-9" in four places. Cite
   them as design-doc IDs, or map them to WP0 R-IDs (PO-8 maps to WP0 R-13's accepted-exception clause).
8. **Leave the verbatim decision records untouched.** At most, add an append-only "superseded by A4" pointer under
   WP0-decisions Amendment 1 and WP1-scope L33.

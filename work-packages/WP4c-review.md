# WP4c — Review report

| | |
|---|---|
| **Scope of work** | [WP4c-scope-of-work.md](WP4c-scope-of-work.md) |
| **Scope approval verified** | merge commit 8fb2070 by Michael Zargham (mzargham), parents 0cbe887 and bc77e83 (the `wp4c-scope` tip) |
| **Work reviewed** | `wp4c-work`, commit 22ad1ee (`git diff 8fb2070...wp4c-work`: 53 files) |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of `wp4c-work` into `main` |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `data/taxonomy/kinds.yaml`: governance/sandbox low, governance/incubating defined and medium, governance/graduated high, each meaning covering the org and `repo-registry`; only governance/archived omitted |
| D-2 | met | 13 applies-if rules rewritten; 17 SOP "Applies to" lines rewritten from the table. `python3 scripts/policies.py`: governance/sandbox 3, governance/incubating 10, governance/graduated 18 |
| D-3 | met | `work-packages/WP1-amendment-3.md` states what A2 and amendment 2 said and what replaces them |
| D-4 | met | Generated files replayed (applicability, kind recommendations, license report, pilot, briefing); current and DRAFT documents updated (see R-7) |
| D-5 | met | OpenSSF core in WP0 (amended in place), README, `current-state.md`, `policy-basis-review.md`, `policy-format.md`, `design.md`, `requirements/policy.md` |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `tests/test_wp4c.py` `test_R1_one_type_at_different_stages` passes |
| R-2 | met | `test_R2_graduated_carries_org_and_repository_policies` passes: the 5 org policies and the 13 that governance/sandbox took before |
| R-3 | met | `test_R3_friction_rises_with_the_stage` passes: tiers low/medium/high; sandbox equals tool/sandbox; incubating is tool/incubating minus `semantic-versioning`; no org policy before graduated |
| R-4 | met | `test_R4_no_rule_excludes_governance_graduated` passes |
| R-5 | met | Against 8fb2070: `registry.yaml`, `data/pilot.yaml`, `data/exclude.yaml` keep the same repositories; no kind changed; only the three governance rows of the applicability table changed; no license status changed; no policy's `cites` changed |
| R-6 | met | `python3 scripts/policies.py` exits 0; `python3 -m unittest discover -s tests`: 62 tests, OK (expected failures=2) |
| R-7 | met | `grep` over README, AGENTS, `docs/` and `docs/requirements/` for governance tier wording finds only the new text; `lifecycle-stage-map.md` names no governance kind or tier; link check passes |
| R-8 | met | `test_R8_openssf_is_a_core_citation` passes: every policy has `cites.openssf`, meta-rule 7 rejects one without it, and the four documents name OpenSSF as core |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-4 exist, and every requirement passes its check | met | Above |
| governance/sandbox, incubating and graduated with friction rising in that order | met | 3, 10, 18 policies; low, medium, high |

## Outside the scope

- **Out-of-scope changes:** `docs/status.md` (status at the gate); `scripts/briefing.py` (tier wording, needed for
  R-7); test updates in `test_wp1.py` and `test_wp3.py`; decision references in `data/assignments.yaml`.
- **Non-goals touched:** none. `repo-registry` stays governance/sandbox; no policy checks, SOP bodies or citations
  changed; nothing about review friction, attestations or the move.

## Observations (not counted as failures)

1. Good enough names D-1 to D-4, but D-5 was delivered too and is checked by R-8.
2. The supporting changes listed above.
3. `lifecycle-stage-map.md`, listed in D-4, is unchanged: it names no governance kind or tier.
4. The org's administration now carries repository policies (for example `codeowners`, `license-by-type`). How the
   engine reads them for an org is left to WP6, as amendment 3 records.
5. Merging `main` into `wp5-work` will conflict in `docs/status.md` and `docs/current-state.md`; WP5 resolves it.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| Observations 1 to 5, as one item | accept as is | Supervisor: "Accept as is" |

## Recommendation

Recommend acceptance, because every deliverable and requirement is met with evidence, friction now rises with the
stage for governance (3, 10, 18), no other outcome changed, and the supervisor accepted the observations as is.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

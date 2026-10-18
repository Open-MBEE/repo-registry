# WP2a — Scope of work: license by type

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `repo-registry` (local; moves to Open-MBEE during R1, in WP5) |
| **Approval record** | mzargham's `git merge --no-ff -m "<message>"` of the scope branch into `main` ([AGENTS.md](../AGENTS.md)) |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` ([AGENTS.md](../AGENTS.md)) |

## Purpose

A small supplement to WP2's policies, done before WP4 so that the pilot is chosen against the complete policy set.
Today `project-files` only requires that some license is detected. Nothing says **which licenses are acceptable for
which content**. The snapshot shows:
- Apache-2.0 dominates;
- MIT is rare;
- 32 live repositories have no license at all;
- a few use other licenses (MPL-2.0, BSD-3-Clause, CC0-1.0).

The policy attaches to a **type** (WP0 A1), so it stays one plain rule per type.

### Sources

- **OpenSSF (backbone)**, project lifecycle at d019efe, citing its charter. Unless the governing body approves
  otherwise:
  - software code: Apache-2.0 or MIT;
  - data: a Community Data License Agreement;
  - specifications: the Community Specification License 1.0;
  - documentation: CC-BY-4.0.
- **CISA** (`CISA-P-LICENSE-PERMISSIVE`, `CISA-P-LICENSE-FILE`, p. 16): prefer a permissive license, always identify
  one, and seek legal review per project.
- **GitHub's license detection** (`license.spdx_id`), and **SPDX** identifiers.
- **NumFOCUS**, OpenMBEE's fiscal sponsor: its public guidance on licensing is researched at the start of execution
  (OD2). If it conflicts with the allowed sets below, execution stops and the conflict comes back as an amendment.

### Allowed licenses (OD1, decided)

| Type | Allowed (SPDX) | Guidance |
|---|---|---|
| tool | Apache-2.0, MIT | Apache-2.0 by default |
| media | CC-BY-4.0, Apache-2.0, MIT | CC-BY-4.0 for documentation and teaching material; Apache-2.0 or MIT where the media is mostly code, such as the website |
| research | Apache-2.0, MIT, CC-BY-4.0, CDLA-Permissive-2.0, CDLA-Sharing-1.0 | Apache-2.0 or MIT for code, CC-BY-4.0 for writing, a CDLA license for data |
| governance | Apache-2.0 | This repository |

Any other license (for example MPL-2.0, BSD-3-Clause, CC0-1.0) needs a recorded exception.

## Goals

- G1. **Clear acceptable licenses for each type of content,** grounded in the sources above.
- G2. **Checkable automatically** from what GitHub already detects.
- G3. **Exceptions are visible, not silent.** A repository with a good reason for another license records it as an
  accepted exception (WP0 PO-8), rather than failing quietly or passing quietly.

## Non-goals

- Relicensing any repository, or writing to any repository.
- Legal advice. The policy names what OpenMBEE accepts. CISA's advice to seek legal review stands.
- Forks. They have no kind, so no policy applies to them, and they keep their upstream license.
- Changing the taxonomy or any other policy, except moving the license check out of `project-files` so that no two
  policies check the same thing (WP2 R-6).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | A short license basis: the allowed sets above, each traced to OpenSSF and CISA, plus a summary of NumFOCUS's public licensing guidance (OD2) and whether it agrees | G1 |
| D-2 | The `license-by-type` policy in WP2's format, with an SOP, and `project-files` trimmed to the README | G1, G2 |
| D-3 | A way to record an accepted exception for one repository and one policy (`data/deviations.yaml`, with the reason and the approving maintainer), which the check honours | G3 |
| D-4 | A license report on the snapshot: each repository's detected license and its result (green, red, or accepted exception), plus the regenerated applicability table | G2 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The policy passes WP2's and WP3's meta-rules (citations, plan availability, SOP sections). | `python3 scripts/policies.py`; tests |
| R-2 | Allowed licenses are SPDX identifiers. A missing license, or one GitHub can't recognize (`NOASSERTION`), is red. | Tests with fixture repositories |
| R-3 | The rule depends only on the repository's type (WP0 A1). | Meta-rule (applies-if) |
| R-4 | An accepted exception turns that one check green, marked visibly as an exception, and names who approved it (WP0 PO-8). | A test with a fixture exception |
| R-5 | No two policies read the license (WP2 R-6). | `test_R6_no_two_policies_read_the_same_thing` |
| R-6 | The report is deterministic and replays from the stored snapshot (WP0 R-2). | Run twice; diff |
| R-7 | Plain language, and PROVISIONAL until the maintainers approve the policies. | Cold read (advisory); inspect |

## Definition of good

- A contributor can tell, in one sentence, what license their kind of repository should use.
- The report makes the 32 unlicensed repositories, and any off-list licenses, easy to act on.

## Definition of good enough

- D-1 to D-4 exist, and every requirement passes its check.
- A short summary for the supervisor: the allowed sets, the counts from the report, and any repositories needing a
  decision *(default)*.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- The package is named **WP2a**, a supplement to WP2, so that WP4 to WP8 keep their numbers.
- The license check moves from `project-files` into `license-by-type`, and `project-files` keeps the README check
  (R-5).
- Exceptions live in `data/deviations.yaml` (repo, policy, reason, approver), PROVISIONAL like everything else (D-3).
- The license basis is a section of `docs/policy-basis-review.md` (D-1).
- The summary for the supervisor (Definition of good enough).

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop: 3 decided (OD1 the allowed sets, OD2 NumFOCUS, OD3 the
defaults), 0 deferred. The records are in [WP2a-decisions.md](WP2a-decisions.md).

# WP4 — Scope of work: fit analysis and pilot

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `repo-registry` (local; moves to Open-MBEE during R1, in WP5) |
| **Approval record** | mzargham's `git merge --no-ff -m "<message>"` of the scope branch into `main` ([AGENTS.md](../AGENTS.md)) |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` ([AGENTS.md](../AGENTS.md)) |

## Purpose

WP4 is the fourth package of the agreed breakdown ([status.md](../docs/status.md)). It does two separate things
(WP0 D-5, D-6):
1. **The fit analysis.** How well the draft taxonomy fits **all** of the org's public repositories, and where it
   doesn't.
2. **The pilot proposal.** The 24 to 36 real repositories that form the initial registry, each with its proposed kind.
   Everything else goes on the exclude list, with a reason.

Two of the five maintainer approvals are "an initial subset of repos to be in the registry" and "the assigned kind for
each repo in the registry" (WP0). WP4 prepares both. The agent proposes the pilot and its kinds from read-only data,
and the supervisor reviews them before they go to the maintainers (WP0 default). The pilot shows how the taxonomy and
the policies work in practice. WP6 computes compliance.

### Direction carried in (already decided)

- **The pilot's sample** (WP0): heavily used and actively developed tools, the website and other media, some research
  repositories, and some repositories that should be archived. Size: 24 to 36, balancing effort against proving value.
- **The exclude list** (WP0, TX-5): every repository outside the pilot is excluded, visibly, with a reason.
- **Must-include (OD1):** `sysml-toolkit`, `OpenSysML`, and Flexo MMS: `flexo-mms-layer1-service`,
  `flexo-mms-deployment`, `flexo-mms.openmbee.org` and `flexo-mms-sysmlv2`. The rest is curated to be **diverse yet
  obviously relevant**, from what is actively developed, what is relevant in media and research, and what has many
  clones (supervisor).
- **Clones:** GitHub's clone counts (the traffic API) are visible only with push access to a repository, and only for
  the last 14 days. They are read where the supervisor's access allows. Elsewhere, stars, forks and release downloads
  stand in, and the briefing says which signal was used *(default)*.
- **Kinds are recommendations;** maintainers assign them (WP1 A3). Graduated is never recommended (A4). Governance
  kinds are assigned (A2).
- Inputs: WP1's provisional kind list (45 unclassified: 25 forks and 20 with no type signal; 74 archive candidates),
  the applicability table (WP2, WP2a, WP3) and the license report (WP2a).

## Goals

- G1. **Know how well the taxonomy fits the whole org,** and what would make it fit better.
- G2. **A pilot that shows the system working on real repositories,** across every type and stage the sample calls
  for.
- G3. **A pilot the maintainers can approve quickly:** each repository's proposed kind, why it was chosen, and which
  policies it would carry.

## Non-goals

- Computing compliance, or opening issues (WP6). The pilot shows which policies *would* apply, not whether they pass.
- Changing the taxonomy or any policy. The fit analysis may *recommend* changes, as candidates for a later package.
- Writing to any repository, or archiving anything.
- The maintainers' approvals themselves (WP8).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The fit analysis: coverage of all public repositories by kind; every unclassified repository with its reason, grouped; where the type rules misfire (spot-checked); the archive candidates; and recommendations for the taxonomy, each as a candidate for later work | G1 |
| D-2 | The pilot selection rule, as data: the categories, how many of each, and the deterministic criteria for picking repositories from the snapshot, plus any must-include repositories you name | G2 |
| D-3 | The proposed pilot (24 to 36 repositories) and the exclude list (every other public repository, each with a reason), generated from D-2, marked PROVISIONAL | G2, G3 |
| D-4 | The pilot briefing, for your review and then the maintainers: each pilot repository with its proposed kind, tier, why it was chosen, the policies it would carry, and its license status | G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Read-only. Built from the stored snapshot and the data files; nothing written to the org. | Code review |
| R-2 | The selection is deterministic and replayable: the same snapshot and rule give the same pilot (WP0 R-2). | Run twice; diff |
| R-3 | The pilot has 24 to 36 repositories and covers every category of the sample. | Test |
| R-4 | Every public repository is either in the pilot or on the exclude list with a reason, never both (TX-5). Private repositories are never named. | Test |
| R-5 | Every pilot repository has a proposed kind, from WP1's recommendation or a recorded decision. None is `unclassified`, unless chosen on purpose to show a gap, and then marked so. | Test |
| R-6 | Everything is PROVISIONAL until the maintainers approve the pilot and the kinds (WP0 approvals 3 and 4). | Inspect |
| R-7 | Plain language in the briefing (WP0 R-4). | Cold read (advisory) |

## Definition of good

- A maintainer reading the briefing understands, in a few minutes, what the registry would do to the org, and agrees
  the pilot is representative.
- The fit analysis points to the few taxonomy changes that would remove most unclassified repositories.

## Definition of good enough

- D-1 to D-4 exist, and every requirement passes its check.
- A short summary for the supervisor: the pilot by category, the main fit findings, and the decisions waiting for the
  maintainers *(default)*.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- The selection rule is `data/pilot-rule.yaml`, the pilot is `data/pilot.yaml`, and the exclude list is
  `data/exclude.yaml` (D-2, D-3). `registry.yaml` stays the provisional kind list for all repositories.
- The fit analysis is `docs/fit-analysis.md`, and the briefing is `docs/pilot-briefing.md` (D-1, D-4).
- "Heavily used" is read from the snapshot's stars, forks and releases, and from clone counts where readable. "Actively developed" is read from commits in
  the last 3 and 12 months. "Should be archived" is WP1's archive-candidate flag (D-2).
- The summary for the supervisor (Definition of good enough).

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop: 4 decided (OD1 must-include, OD2 the mix, OD3
recommendations, OD4 defaults), 0 deferred. The records are in [WP4-decisions.md](WP4-decisions.md).

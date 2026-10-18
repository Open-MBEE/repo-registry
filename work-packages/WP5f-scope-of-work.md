# WP5f — Scope of work: owners and maintainers first

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | [Open-MBEE/repo-registry](https://github.com/Open-MBEE/repo-registry), and the Open-MBEE organization's roles |
| **Approval record** | mzargham's merge, with a merge commit, of the pull request that adds this document into `main` (WP5 OD3) |
| **Acceptance record** | mzargham's merge, with a merge commit, of the delivery pull request into `main` |

## Purpose

The supervisor: "we need to establish owners and maintainers policies first so we can determine who the owners and
maintainers are since the other policies are governed by that group", and "my maintainers list is not only
provisional its really more of a placeholder. we also need to determine who the actual owner should be and make sure
its a small set (which may mean pruning owners and populating maintainers)" ([WP5f-decisions.md](WP5f-decisions.md)).
It is on the critical path: the owners and maintainers approve everything else (the five maintainer approvals).

Today, from the WP3 snapshot: the organization has **18 owners**, 2 with public membership and 16 concealed (counted,
never named); the policy target is 2 to 3 (`org-few-owners`, OpenSSF TI-3). `data/maintainers.yaml` names 4 people,
as a placeholder. Everything now in this repository, that list included, is demonstrative: drawn from data with the
intent to be realistic, but not a decision (OD5).

## Goals

- G1. **The policies that determine who governs:** how owners and maintainers are chosen, what qualifies them, and how
  the set changes, agreed before anything else is approved.
- G2. **The owners, a small set:** who the 2 or 3 owners should be, decided and recorded.
- G3. **The maintainers, a real list:** the people who govern the organization, replacing the placeholder.
- G4. **On the roadmap:** the package appears in the status documents as critical path, ahead of WP6, with the fifth
  maintainer approval (the named maintainers) moved ahead of the other four.

## Non-goals

- Naming any concealed member or owner in this repository (WP3 OD1); the path from 18 owners is described by count.
- The engine's sensing (WP6) and the compliance dashboard (WP7).
- Changing other policies, except as the open decisions below say.
- Carrying out the changes of control in the organization (changing anyone's role), and planning how: decided later,
  in another package (OD3). The organization's owners stay as they are, and `org-few-owners` stays red until then.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The policies that determine who governs: the maintainer policy (`docs/maintainer-policy.md`) and the org policies (`org-few-owners`, `maintainers-match`, `governance-roles-named`, `verified-code-owners`) reviewed and amended as decided, including how owners and maintainers are chosen (OD1) | G1 |
| D-2 | The shape of a decision brief for the co-founders (OD1): what the policies ask of owners and maintainers, the facts to weigh, and the choices to make, shown with a hypothetical example, labelled as hypothetical and not the proposed decision (OD5); then their decision on the owners (2 or 3), recorded by the supervisor. Owners not kept are to become members (OD2); carrying that out is later work (OD3) | G2 |
| D-3 | The maintainers: the co-founders' decision recorded by the supervisor in `data/maintainers.yaml` and `data/proposed-codeowners`, replacing the placeholder, each person with consent to be named (OD4) | G3 |
| D-4 | The roadmap: `docs/status.md` and `docs/current-state.md` (this package, critical path, ahead of WP6; the fifth approval first) | G4 |
| D-5 | Tests and the documents, in the same pull requests | G1–G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The policies say how an owner and a maintainer are chosen, what qualifies them, and how the set changes. | Inspect; the policy meta-rules |
| R-2 | The recorded owners are 2 or 3 of the named maintainers. | `scripts/validate.py` (a rule) |
| R-3 | No concealed member is named anywhere in the repository. | The privacy scans |
| R-4 | The roadmap shows the package as critical path, ahead of WP6, with the fifth approval first. | Inspect `docs/status.md` |

## Definition of good

- A maintainer reading the wiki can see who governs OpenMBEE, how they came to, and how that changes; and who the
  small set of owners is meant to be.

## Definition of good enough

- D-1 to D-5 exist, every requirement passes its check, and the existing suite still passes.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- Names: this package is WP5f; its records are `work-packages/WP5f-*.md`.
- The agent writes nothing to the organization (WP5 OD4).
- The roadmap change, and this package's own status update, ride with its scope pull request (the roadmap item was
  taken out of #13).
- D-1's change to the maintainer policy is a record, not a new rule: it says how the first owners and maintainers were
  chosen (OD1). Otherwise the policies stay as written (OD4).
- The decision brief (`work-packages/WP5f-decision-brief.md`) decides nothing about who is an owner or maintainer,
  and recommends, ranks and proposes no one *(changed by the supervisor, OD5)*. It shows its shape with a
  hypothetical example, labelled as such throughout, naming no real person as an owner or maintainer, and changes no
  record.

## Open decisions (for the supervisor)

- **OD1.** Who decides the first owners and maintainers. *Decided: the co-founders (Chris Delp, Robert Karban), likely
  from a loose consensus of the most active contributors and the informally defined leadership group; the supervisor
  records their decision here. This package prepares the decision and records it.*
- **OD2.** What happens to the owners who are not kept. *Decided: they become members (and maintainers, where
  chosen), keeping their access through teams.*
- **OD3.** Whether this package carries out the owner changes. *Decided: record first; how and when the changes of
  control are carried out is decided later, in another package.*
- **OD4.** What qualifies a maintainer. *Decided: the maintainer policy as written; nothing added.*
- **OD5.** The Agent's defaults. *Decided: approved, with default 5 changed by the supervisor (the brief decides and
  recommends nothing), everything now in the repository treated as demonstrative, and this pull request carrying its
  own status update.*

None remain open. Every item was resolved through the decision loop: 5 decided (OD1 to OD5, OD5 with one
follow-up on the brief's form), 0 deferred, 0 raised.
The records are in [WP5f-decisions.md](WP5f-decisions.md).

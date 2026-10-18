# WP2 — Scope of work: policies

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `repo-registry` (local; moves to Open-MBEE during R1, in WP5) |
| **Approval record** | mzargham's `git merge --no-ff -m "<message>"` of the scope branch into `main` ([AGENTS.md](../AGENTS.md)) |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` ([AGENTS.md](../AGENTS.md)) |

## Purpose

WP2 is the second package of the agreed breakdown ([status.md](../docs/status.md)). It delivers the last link of
WP0's chain: from a repo's three categorical attributes (type, lifecycle stage, tier; WP1) to the **policies in
effect** for it. It does so with the **simplest set of named policies that meets our security objectives**, each
defined at a level GitHub can configure, each with a plain "applies if" rule on type, stage or tier (WP0 A1), and
each with an SOP covering setup, automated checks and attested checks (WP0 R-16). Policies are what the maintainers
approve as WP0's second approval, "the policies, based on the taxonomy".

### Sources

The policies are grounded in five sources. Two are core and three are secondary (WP1 decisions, "Secondary
citations").

| Role | Source | Used for |
|---|---|---|
| Core | CISA, *Open Source Software: Security Principles and Practices* (2026) | Producer practices and C4 criteria each policy serves |
| Core | NIST SP 800-37 Rev. 2, *Risk Management Framework*, with SP 800-53 controls | The RMF task or 800-53 control each policy serves |
| Secondary, **backbone** | OpenSSF project lifecycle and its **security baseline by stage** (`ossf/tac`) | The backbone of the policy set: by default our stage-attached policies mirror its items, departing only with a stated reason (OD1) |
| Secondary | CNCF project lifecycle (`cncf/toc`) | Stage expectations (Sandbox, Incubation, Graduation, Archived), cross-checked against OpenSSF |
| Secondary | ISO/IEC/IEEE 12207:2026, cited **by reference only** (single-user licensed copy, never committed or quoted at length) | §5.4 stages, and the Maintenance (§6.4.13) and Disposal (§6.4.14) processes behind the maintenance and archive policies |

### Direction carried in (already decided)

- **The OpenSSF security baseline by stage is the backbone** (OD1). Each of its items becomes one of our policies, or
  is departed from with a stated reason, for example when it doesn't apply to our kinds or GitHub can't carry it.
- Policies attach to a type, a lifecycle stage or a tier, and nothing else (WP0 A1).
- **Semantic versioning is a policy for tools** (WP1 A1). It also makes the `1.0.0` seam checkable.
- **Maintenance is active work**: tracking dependencies and fixing reported security flaws, as policies attached to
  stages. Whether it happens is a compliance question, never a kind (WP1 decisions).
- **An archive policy** exists (WP0): before archiving, the README states that support has ended and points to known
  forks. Repos archived before the policy existed count as compliant.
- **Low friction where it fits**: sandbox and research stay lightly controlled. A repo is compliant when it passes
  its automated checks and has up-to-date attestations from its CODEOWNERS (WP0).

## Goals

- G1. **A grounded policy basis.** Know which GitHub-native features can carry our security objectives, and which
  CISA, RMF and OpenSSF expectations each would meet.
- G2. **The simplest sufficient set of named policies.** Few policies, each traceable to an objective and a citation,
  with no two doing the same job.
- G3. **Clear applicability.** For every kind, it's obvious and deterministic which policies are in effect, from type,
  stage and tier alone.
- G4. **Policies that operators can follow.** Each policy has an SOP that says how to set it up, what is checked
  automatically, and what must be attested and how.

## Non-goals

- Implementing the compliance checks against real repos (sensing and status are WP6). WP2 defines the checks.
- Org governance: the named maintainers and the org-wide common controls (WP3).
- Enforcing the policy meta-rules in CI (WP5). WP2 states them.
- Changing any repo's settings or writing to any repo other than this one.
- Supporting every GitHub feature, or adopting the CNCF criteria wholesale. The OpenSSF baseline is followed item by
  item, but its foundation-specific parts (for example foundation-funded audits) are departures with reasons.
- Reproducing ISO/IEC/IEEE 12207 text.
- Automatic fixes (WP0 non-goal).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The policy basis review: an inventory of the GitHub security and governance features relevant to repos (from GitHub's documentation), and a cross-check of each against CISA, NIST RMF/SP 800-53, the OpenSSF security baseline by stage, the CNCF stage expectations, and ISO/IEC/IEEE 12207 processes (by reference). It ends with the proposed policy set and why each feature was kept or left out | G1, G2 |
| D-2 | The named policies, as data, marked PROVISIONAL: for each, its name, plain meaning, applies-if rule, GitHub configuration, automated checks, attested checks, and citations (core and secondary) | G2, G3 |
| D-3 | An SOP for each policy, in plain language: setup steps, what's checked automatically, and what to attest and how, including an attestation template where one is needed | G4 |
| D-4 | The policy format and its meta-rules (schema), precise enough for WP5 to enforce | G3 |
| D-5 | The applicability table: for every kind in `data/taxonomy/kinds.yaml`, the policies in effect, generated deterministically from the applies-if rules | G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every policy names the GitHub-native mechanism it relies on, or says it is attested because GitHub has no setting for it (WP0 R-5, PO-6). | Meta-rule check over D-2 |
| R-2 | Every applies-if rule uses only type, lifecycle stage and tier (WP0 A1). | Meta-rule check; the resolver reads nothing else |
| R-3 | Every policy cites the CISA practice and the RMF task or SP 800-53 control it serves, or says "none" (WP0 R-16). Where a secondary source applies (an OpenSSF baseline item, a CNCF stage expectation, a 12207 process), it is cited too. | Meta-rule check; a cold read of the citations |
| R-4 | Every policy has an SOP with all three parts: setup, automated checks and attested checks (WP0 R-16). | Meta-rule check; a cold read of each SOP |
| R-5 | Plain language for everything an operator reads (WP0 R-4). | A cold read (supervisor's rule from WP1: stand-in reads are advisory) |
| R-6 | Simplest sufficient set: every policy traces to at least one security objective in D-1, every objective in D-1 is covered or explicitly left out with a reason, and no two policies check the same thing. | Trace table in D-1 |
| R-7 | Friction follows the tiers: sandbox and research kinds carry the fewest policies, and nothing beyond what the OpenSSF *Sandbox* baseline asks unless D-1 gives a reason; graduated tools carry the most. | The applicability table (D-5) |
| R-8 | Each automated check is something `gh` can read with the strong read credential (WP0 R-9), or is marked as attested. | D-1 lists the GitHub API field or file each check reads |
| R-9 | Applicability is deterministic and replayable: the same taxonomy and policies always give the same table (WP0 R-2). | Generate twice; diff |
| R-10 | Policies are data and can change without a code change (WP0 R-6). | Swap in a toy policy set; zero code change |
| R-11 | Everything is marked PROVISIONAL until the maintainers approve the policies (AGENTS.md). | Inspect the files |
| R-12 | ISO/IEC/IEEE 12207 is cited by clause number only. No text from it is committed. | grep the repo for passages from it; there are none beyond titles and clause numbers |
| R-13 | Every item of the OpenSSF security baseline (every stage) appears in D-1 either as adopted, mapped to one of our policies and the stages it applies to, or as departed, with a reason (OD1). Their stages map to ours by name: Sandbox, Incubating, Graduated. | Trace table in D-1: every baseline item has a row |

## Definition of good

- A maintainer reading the applicability table can explain, for any kind, why each policy applies, in one sentence.
- The set is small enough to hold in your head, yet an adopter can see it lines up with CISA, NIST and OpenSSF.
- Operators find the SOPs easy to follow, and sandbox work stays frictionless.

## Definition of good enough

- D-1 to D-5 exist, and every requirement passes its check.
- The proposed policy set includes semantic versioning for tools, maintenance duties attached to stages, and the
  archive policy (Direction).
- A short summary for the supervisor: the policies, which kinds they apply to, and what was deliberately left out
  and why *(default)*.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- Policies live in `data/policies/<name>.yaml`, and SOPs in `docs/sops/<name>.md` (D-2, D-3).
- The policy basis review is `docs/policy-basis-review.md` (D-1). It records the commit of each `ossf/tac` and
  `cncf/toc` document read.
- The resolver extends `scripts/recommend.py`'s predicate engine, so there is one predicate language (D-5).
- The summary for the supervisor (Definition of good enough).
- The GitHub feature inventory comes from GitHub's public documentation, read during execution (D-1).

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop: 2 decided (OD1 backbone, OD2 defaults), 0 deferred. The
records are in [WP2-decisions.md](WP2-decisions.md).

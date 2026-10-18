# WP3 — Scope of work: org governance

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `repo-registry` (local; moves to Open-MBEE during R1, in WP5) |
| **Approval record** | mzargham's `git merge --no-ff -m "<message>"` of the scope branch into `main` ([AGENTS.md](../AGENTS.md)) |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` ([AGENTS.md](../AGENTS.md)) |

## Purpose

WP3 is the third package of the agreed breakdown ([status.md](../docs/status.md)). It applies to the GitHub
organization itself the same treatment WP1 and WP2 gave repositories (WP0, "Named maintainers and the org"):
- a clear policy;
- what can be measured, measured;
- the rest attested;
- so that the stated list of maintainers matches the people with governance power over the org.

Today the org's leadership isn't necessarily mapped to technical leadership. It also isn't clear who holds admin
authority, or what powers they have, which matters for CISA. The named maintainers are this repo's CODEOWNERS and the
org's admins. Naming them is WP0's fifth maintainer approval.

### Direction carried in (already decided)

- The org's administration has the kind **governance/graduated**, which maps to the **high** tier (WP1 A2, A4).
- Org policies use WP2's format and applies-if rules. They apply to governance/graduated. So the org gets its policies
  through the same chain as a repo: kind → tier → policies.
- **Org-wide common controls** carried from WP2: two-factor authentication (OpenSSF SB-2; NIST IA-2(1)), and few
  owners and admins (OpenSSF TI-3, which asks for two or three organization owners).
- **Public names only, for now (OD1).** Governance-role holders are named only if their org membership is public.
  Concealed holders are counted, never named. The gap is flagged. Accountability calls for naming everyone who holds
  governance power, so WP3 proposes an org policy that requires it (`governance-roles-named`). Until that rule is
  ratified, nobody is named against their choice. People can step down from a governance role, instead of being
  named, if they prefer.
- **The provisional named maintainers (OD2):** `mzargham` (Michael Zargham), `rkarban` (Robert Karban, a founder)
  and `HuiJun` (Jason Han, release authority for OpenSysML). Robert and Jason are publicly named as maintainers
  elsewhere, so naming them in the list is fine. Their GitHub org membership isn't public, though, so the match check
  shows their rows as yellow ("membership not public") and never reveals their org role. Five is a good target size.
  No other names are revealed: others who hold admin powers are noted as a count.
- **Release authority.** Jason Han is the release authority for OpenSysML, and a credentialing process is under way so
  that he can fulfil that role. The maintainer policy (D-5) says how such authority is given and checked.
- Checks are read-only. A setting the current credential can't read is **yellow**, never off. The sensing credential
  with *Administration: read* is expected gap XF-1, closing in WP6.

## Goals

- G1. **Know who holds power over the GitHub org.** From GitHub's own documentation, know every way power over the
  org is held: roles, teams, collaborators and installed apps. Know what each can do, and who or what holds it now.
- G2. **A small, clear org policy.** The common controls the org must have, each in WP2's policy format.
- G3. **Named maintainers that match reality.** A provisional list of named maintainers, and a deterministic check
  that it matches this repo's CODEOWNERS and the org's admins (WP0 R-15).
- G4. **A clear rule for who the maintainers are and what they may do.** A policy that determines how maintainers are
  chosen and what powers they get, including release authority, so that membership and powers follow a written rule.

## Non-goals

- Changing any org setting, role or membership, or writing anything to the org.
- Setting up the sensing credential (XF-1 closes in WP6; the move to Open-MBEE is WP5).
- Turning on review friction for this repo (WP0: the CODEOWNERS approval switch comes at R3).
- Deciding who the maintainers are. The list is drafted as PROVISIONAL, and the maintainers approve it (WP0 approval 5).
- The wiki page for the org (WP7).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | **The GitHub org governance review, from GitHub's documentation.** An exploration of how a GitHub organization is governed. It covers: org roles (owner, member, moderator, security manager, billing manager, custom organization roles); repository roles granted through teams, and outside collaborators; team maintainers; GitHub Apps and other integrations installed on the org, and their permissions; the org settings that bear on security (two-factor requirement, base repository permission, who may create, fork or delete repositories, member privileges, personal access token policy, org-level rulesets, security configurations, Actions policies); and the audit log. For each, it records what powers it confers, how to read it with `gh api` and the permission needed, and a docs link. Also a read-only snapshot of the current holders and the readable settings | G1 |
| D-2 | The org policies: a few policies in `data/policies/` that apply to governance/graduated (for example two-factor authentication, few owners, a least-privilege base permission, the maintainers-match check, and `governance-roles-named`, which requires governance-role holders to make their org membership public), each with an SOP and citations, following WP2's format and meta-rules | G2 |
| D-3 | The provisional named-maintainer list (WP0 D-8), as data, and a proposed CODEOWNERS for this repo that matches it, as data, not yet live | G3 |
| D-4 | The maintainers-match check (WP0 R-15). It compares the list with the proposed CODEOWNERS and the org's admins, deterministically, on the snapshot, and reports each mismatch with a red, yellow or green status | G3 |
| D-5 | The maintainer policy, PROVISIONAL until ratified: how named maintainers are chosen and removed, the target size (five), what powers maintainers get (org roles, CODEOWNERS of this repo), how release authority for a tool (for example OpenSysML) is granted and credentialed, and how governance-role holders are named (`governance-roles-named`). Written as data and plain prose, citing GitHub's role documentation and the OpenSSF and CNCF governance expectations | G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Read-only: only `gh` reads, no writes to the org (WP0 R-8, R-9). | Code review; grep for write methods |
| R-2 | Every role, setting and integration in D-1 is described from GitHub's documentation, each with a link. Anything the docs don't confirm is marked unconfirmed, not filled in. | Inspect D-1; every row has a docs link |
| R-3 | The org policies pass WP2's meta-rules, including core citations and coverage of the OpenSSF baseline (SB-2 and TI-3 move from departed to adopted). | `python3 scripts/policies.py`; tests |
| R-4 | The maintainers-match check is deterministic and replayable on the stored snapshot (WP0 R-2). | Run twice; diff |
| R-5 | A setting or role list the credential can't read is yellow, never treated as off or empty (WP2 policy format). | A test with an unreadable field |
| R-6 | Everything is PROVISIONAL until the maintainers approve it (AGENTS.md). | Inspect |
| R-7 | Plain language for everything a reader sees (WP0 R-4). | Cold read (stand-in reads are advisory) |
| R-8 | No concealed org membership or org role is revealed. A user is named only if their org membership is public, or if the supervisor names them as already publicly known (`rkarban`, `HuiJun`). For those, the check reports "membership not public" (yellow) and never their org role. Every other holder is a count (OD1, OD2). | A test cross-checks every named user against the public members and the supervisor's list, and checks that no concealed holder's role appears |

## Definition of good

- A regulated adopter can see who governs OpenMBEE on GitHub, what powers they hold, and that this matches the stated
  maintainers.
- The org policy is small, and each control in it is clearly worth having.

## Definition of good enough

- D-1 to D-5 exist, and every requirement passes its check.
- The maintainers-match check has run on the snapshot, and the result (green, yellow or red per item) is in the
  summary.
- A short summary for the supervisor: the roles and holders found, the org policies, the match result, and what
  couldn't be read with the current credential *(default)*.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- The org snapshot is `data/snapshots/<date>/org.json` (D-1). The list is `data/maintainers.yaml` and the proposed
  CODEOWNERS is `data/proposed-codeowners` (D-3).
- The check extends `scripts/policies.py` or adds `scripts/org.py`, reusing the predicate engine (D-4).
- The GitHub org-role and settings research reads docs.github.com, as WP2's did (D-1).
- The summary for the supervisor (Definition of good enough).

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop: 3 decided (OD1 privacy, OD2 the list, OD3 the accounts and
defaults), 0 deferred, 1 raised (the scope emphasis on GitHub's documentation). The records are in
[WP3-decisions.md](WP3-decisions.md).

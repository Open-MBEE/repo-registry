# repo-registry

> **Status: PROVISIONAL.** Nothing here is in effect yet. This repository holds the design and provisional data
> (kinds, policies with their SOPs, a proposed pilot), plus the scripts and tests that check them, all waiting for
> the OpenMBEE maintainers' approval. Start with [docs/current-state.md](docs/current-state.md).

`repo-registry` keeps one record of every repository in the
[Open-MBEE](https://github.com/Open-MBEE) GitHub organization. For each one it records what kind of
repository it is, who is responsible for it, and which rules apply to it. It then checks, on a schedule,
whether each repository follows those rules, and it tells the right people when one doesn't.

## Why it exists

- **To help people find their way.** OpenMBEE has a lot of repositories. Some are experiments (Sandbox), some
  are established and versioned (Incubating), some are mature and widely relied on (Graduated), and some are kept
  only for history (Archived). Newcomers, contributors and our community manager need to see which is which at a glance.
- **To show that we follow our own rules.** Many organizations that use OpenMBEE work in regulated
  industries. They need to see that who may change what, and who approves a release, follow written
  rules. We aim to line up with CISA's guidance and NIST's Risk Management Framework (see
  [The guidance we follow](#the-guidance-we-follow)).
- **To add friction only where it is needed, and to be clear about it.** Graduated tools and the governance of
  the organization get the strictest rules. Sandbox tools, media (the website, the wiki, educational material) and
  research get lighter ones, so they stay easy to contribute to. For every repository you can see which controls
  apply, which don't, and whether the ones that apply are really in effect.

## The guidance we follow

This registry is designed to bring OpenMBEE into line with two pieces of guidance:

- CISA, [*Open Source Software: Security Principles and Practices*](https://www.cisa.gov/sites/default/files/2026-08/open-source-software-security-principles-and-practices.pdf)
  (July 2026).
- NIST, [SP 800-37 Rev. 2, *Risk Management Framework for Information Systems and Organizations*](https://csrc.nist.gov/pubs/sp/800/37/r2/final)
  (December 2018).

It does this through **minimum viable policy making and controls**:

- **Easy to show, cheap to run.** Showing that we follow our own policies should be as easy as possible, and the
  overhead as small as possible. We name a small set of policies, and say which apply to which kind of repository.
  We don't try to cover everything GitHub can do.
- **A light load at the center.** The maintainers, who govern the organization as a whole, keep their load light.
  Authority is spread out to each repository's CODEOWNERS, who govern their own repository.
- **Clear release controls by tier.** Every kind of repository sits in one of four tiers, and each tier makes clear
  which release controls its CODEOWNERS need to put in place:
  - **High:** graduated tools that need rigorous release control, and the governance of the organization itself.
  - **Medium:** load-bearing media, such as the website, and incubating tools (version 1.0 or later, not yet graduated).
  - **Low:** repositories that need an owner but have no formal controls beyond someone who looks after them,
    including sandbox tools that are still experimenting.
  - **None:** archived material, which is read-only once archived.

## What it is, and what it is not

**It is** a small, predictable program plus the rules it applies, all kept in this repository. It looks at the
repositories, reads the decisions people have recorded, works out which kind of repository each one is, checks the
rules, and says what needs doing. It is meant to run in GitHub Actions and open GitHub issues. For now (R1) it runs
read-only on stored snapshots, and its issue texts are local files that are not posted.

How it decides which rules apply: measurements of a repository, and attestations by its code owners, give it three
attributes: its **type** (tool, media, research or governance), its **lifecycle stage** (Sandbox, Incubating,
Graduated or Archived) and its **tier** (high, medium, low or none, set by type and stage). Each policy says which
of those it applies to, so the three together decide which policies are in effect. A **kind** is a named
combination of the three, such as tool/incubating. In short: repo → kind → tier → policies (a summary only, since a
policy can attach to the type or stage as well as the tier).

**It is not:**
- an AI agent. No language model takes part in any decision.
- a project tracker.
- a replacement for each repository's own contributing guide.
- a way to delete repositories. It never deletes anything. Repositories are archived or made private instead.
- the authority on a repository's status. People (the governors, below) decide that.
- its own identity or permission system. Everyone is a GitHub user, and permissions are GitHub's own
  (teams, roles, CODEOWNERS, rulesets). This system uses them, and its rules can say how they should be
  used. It never rebuilds what git or GitHub already provides.

## How to use it: pick your role

You may hold more than one role. Each role has one place to go.

### Reader: you want to find or understand a repository

Use the **wiki of this repository**. It is generated automatically and never edited by hand. It has:
- an **index page** that lists the highlighted repositories first (incubating or graduated), then every
  repository with its kind and its CODEOWNERS;
- **one page per kind of repository**, which says what puts a repository in that kind and which tier it is in;
- **one page per tier**, which says which kinds are in it (policies can attach to type, stage or tier, so the kind
  page is where to see every policy in effect for a repository);
- **one page per policy**, which holds the policy and its standard operating procedure;
- **views of the registry by kind, by tier and by policy**. Each repository is shown with a red, yellow or green
  status (out of compliance, can't tell, in compliance), a link to the repository, and a link to its open issues
  from this system.

### Operator: you look after a repository

Look at the **issues in your own repository**. When something needs doing, the system opens an
issue there. The issue says what to do, why (which rule, and what was seen), and who is asked.

- If it asks you to **change something** (for example, add a `SECURITY.md` or turn on required
  reviews), make the change in your repository and close the issue. The next check confirms it.
- If it asks you a **question** (a fact the system can't see for itself), answer it in an attestation block in
  your repository's `README.md`, committed by a code owner. The policy's SOP shows the form. An attestation is out
  of date once it is older than your latest release.

A repository's operators **are** its CODEOWNERS. Every repository in a tier that needs an owner (high, medium or
low) must have a CODEOWNERS file, and only a code owner's attestation counts.

The only thing you ever do in this repository is propose a change to your repository's kind, by a pull
request that any maintainer may merge.

### Governor: you set the rules

Governors are the OpenMBEE maintainers. They work **in this repository**:
- Changes to the kinds of repository, the rules, which kind each repository is, accepted exceptions,
  and the program itself all go through pull requests here. A change of a repository's kind is merged by any
  maintainer. Changes to the list of maintainers or their powers, and accepted exceptions, are merged by an owner
  (one of the two or three maintainers who hold the organization's owner role).
- Questions that need a decision (for example, a repository that fits no kind) come up as issues here.
- Every pull request shows what its change would do to the organization before anyone approves it.

While the design is being built and tested, changes here are deliberately easy to make. From the
first release that makes this the official source of truth, only the OpenMBEE maintainers (as
CODEOWNERS) may approve changes. How many approvals are needed is not decided yet.

## Expect a lot of open items at first

When it is first switched on, many repositories won't yet meet the rules for their kind. That is
expected, not a failure. What matters is that every gap is visible, has a named person responsible,
and has a clear next step.

## Roadmap in brief

1. **Demonstrate:** run read-only on a pilot of real OpenMBEE repositories (32 proposed), so the maintainers can
   see what the proposed rules would do. It ends with five maintainer approvals: the taxonomy, the policies, the
   pilot subset, each pilot repository's kind, and the named maintainers.
2. **Switch on and calibrate:** run against the real organization, marked "calibrating, not yet the
   source of truth," and fix what it gets wrong.
3. **Make it official:** once ratified, the first release makes it the source of truth, and its own
   rules tighten.
4. **Steady state:** every gap between what a repository should be and what it is gets found and routed.
5. **Later:** nice-to-haves that are not on the critical path.

Details: [docs/roadmap.md](docs/roadmap.md).

## Where to read more

- [Current state](docs/current-state.md): **the place to start.** What is decided, where it is recorded, and what
  is next
- [Status](docs/status.md): where the work packages stand
- [Policy applicability](docs/policy-applicability.md): which policies are in effect for each kind, with links to
  each policy's SOP
- [Pilot briefing](docs/pilot-briefing.md): the proposed pilot repositories and their kinds

The scope of record is [WP0](work-packages/WP0-scope-of-work.md) and the later work-package scopes and decision
records in [work-packages/](work-packages/). The early design documents below are DRAFT inputs; where they disagree
with those records, the records win.

- [Design overview](docs/design.md): architecture, roles, decisions, evidence
- [Roadmap](docs/roadmap.md)
- [Testing and demonstration](docs/testing-and-demonstration.md)
- Requirements: [formal model](docs/requirements/formal-model.md) ·
  [taxonomy](docs/requirements/taxonomy.md) · [policy](docs/requirements/policy.md) ·
  [interfaces](docs/requirements/interfaces.md) · [closed-loop behavior](docs/requirements/closed-loop.md)

If you work on this repository with an AI coding assistant, start with [AGENTS.md](AGENTS.md).

# repo-registry

> **Status: DRAFT design.** Nothing here is in effect yet. This repository currently holds only the
> design, and the design is still being agreed. See [Roadmap](docs/roadmap.md).

`repo-registry` keeps one record of every repository in the
[Open-MBEE](https://github.com/Open-MBEE) GitHub organization. For each one it records what kind of
repository it is, who is responsible for it, and which rules apply to it. It then checks, on a schedule,
whether each repository follows those rules, and it tells the right people when one doesn't.

## Why it exists

- **To help people find their way.** OpenMBEE has a lot of repositories. Some are under active
  development, some are well maintained and trusted, some are experiments, and some are kept only for
  history. Newcomers, contributors and our community manager need to see which is which at a glance.
- **To show that we follow our own rules.** Many organizations that use OpenMBEE work in regulated
  industries. They need to see that who may change what, and who approves a release, follow written
  rules. We aim to line up with CISA's *Open Source Software: Security Principles and Practices* (2026).
- **To add friction only where it is needed, and to be clear about it.** Tools get the strictest rules. Media
  (the website, the wiki, educational material) and research get lighter ones, so they stay easy to
  contribute to. For every repository you can see which controls apply, which don't, and whether the
  ones that apply are really in effect.

## What it is, and what it is not

**It is** a small, predictable program plus the rules it applies, all kept in this repository. It
runs in GitHub Actions. It looks at the repositories, reads the decisions people have recorded, works
out which kind of repository each one is, checks the rules, and opens GitHub issues when something
needs doing.

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
- an **index page** that lists the highlighted repositories first (under active development, or
  trusted and maintained), then every repository with its kind, owner and release officer;
- **one page per kind of repository**, which says what puts a repository in that kind, which controls
  apply to it and which deliberately don't, and who is responsible;
- **one page per repository**, which shows which rules it meets, which it doesn't yet, and any
  accepted exceptions.

### Operator: you look after a repository

Look at the **issues in your own repository**. When something needs doing, the system opens an
issue there. The issue says what to do, why (which rule, and what was seen), and who is asked.

- If it asks you to **change something** (for example, add a `SECURITY.md` or turn on required
  reviews), make the change in your repository and close the issue. The next check confirms it.
- If it asks you a **question** (a fact the system can't see for itself), the issue says exactly where
  to answer and in what form.

For the more strictly overseen kinds of repository, the operators (owner and release officer) must also be
listed in that repository's CODEOWNERS, so their review is required by GitHub itself.

You never need to edit this repository to do your part.

### Governor: you set the rules

Governors are the OpenMBEE maintainers. They work **in this repository**:
- Changes to the kinds of repository, the rules, which kind each repository is, accepted exceptions,
  and the program itself all go through pull requests here.
- Questions that need a decision (for example, a repository that fits no kind) come up as issues here.
- Every pull request shows what its change would do to the organization before anyone approves it.

While the design is being built and tested, changes here are deliberately easy to make. From the
first release that makes this the official source of truth, only the OpenMBEE maintainers (as
CODEOWNERS) may approve changes, and several approvals are needed.

## Expect a lot of open items at first

When it is first switched on, many repositories won't yet meet the rules for their kind. That is
expected, not a failure. What matters is that every gap is visible, has a named person responsible,
and has a clear next step.

## Roadmap in brief

1. **Demonstrate:** run on a made-up example organization, so the maintainers can see what proposed
   rules would do and agree on them.
2. **Switch on and calibrate:** run against the real organization, marked "calibrating, not yet the
   source of truth," and fix what it gets wrong.
3. **Make it official:** once ratified, the first release makes it the source of truth, and its own
   rules tighten.
4. **Steady state:** every gap between what a repository should be and what it is gets found and routed.
5. **Later:** nice-to-haves that are not on the critical path.

Details: [docs/roadmap.md](docs/roadmap.md).

## Design documents

- [Design overview](docs/design.md): architecture, roles, decisions, evidence
- [Roadmap](docs/roadmap.md)
- [Testing and demonstration](docs/testing-and-demonstration.md)
- Requirements: [formal model](docs/requirements/formal-model.md) ·
  [taxonomy](docs/requirements/taxonomy.md) · [policy](docs/requirements/policy.md) ·
  [interfaces](docs/requirements/interfaces.md) · [closed-loop behavior](docs/requirements/closed-loop.md)

If you work on this repository with an AI coding assistant, start with [AGENTS.md](AGENTS.md).

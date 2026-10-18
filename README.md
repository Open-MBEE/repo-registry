# repo-registry

`repo-registry` is the proposed governance registry for the [Open-MBEE](https://github.com/Open-MBEE) GitHub
organization. It keeps one record of every repository: what kind of repository it is, how strict its controls should
be, which policies apply to it, and where each policy comes from. Later it will check each repository against those
policies and tell the right people when something needs doing.

> **Status: sandbox, and PROVISIONAL.** This repository is itself at the Sandbox stage. Nothing here is in effect:
> no repository is checked, no issue is opened, and no rule is enforced. What exists is a first draft of the model
> (the taxonomy, the policies with their sources, and each repository's proposed kind), built so the OpenMBEE
> maintainers can understand it, question it and change it before any of it is adopted.

## Start here: the review pack

The review pack is on this repository's **[wiki](https://github.com/Open-MBEE/repo-registry/wiki)**. It is rendered
from the model in this repository and never edited by hand, and it is meant to be read in a few minutes. Each page's
sidebar names the commit it was rendered from:

| Page | What it answers |
|---|---|
| [Taxonomy](https://github.com/Open-MBEE/repo-registry/wiki/Taxonomy) | What the types, stages, tiers and kinds mean, and how a repository gets its kind, in plain words |
| [Repositories](https://github.com/Open-MBEE/repo-registry/wiki/Repositories) | Every repository with its proposed kind and tier, and where that came from |
| [Policies](https://github.com/Open-MBEE/repo-registry/wiki/Policies) | What each policy asks, when it is in effect, and its step-by-step SOP |
| [Sources](https://github.com/Open-MBEE/repo-registry/wiki/Sources) | Where each policy comes from, quoted in the source's own words |

We would like to hear from you, especially before the pack is approved: what is wrong, unclear or missing, and
where a policy asks too much or too little. Reading the sources first helps: each policy cites the guidance it
follows, and the [Sources](https://github.com/Open-MBEE/repo-registry/wiki/Sources) page shows the passages.

If the wiki isn't published yet, render the same pages locally (see [How to check everything](#how-to-check-everything))
and open `build/demo/wiki/`.

## How to take part: branches and pull requests

Every change to the model is a **pull request** to this repository, and the pull request is where it is discussed.
You don't need to be sure you're right to open one: a draft pull request is a good way to start a conversation.

1. **Find the record.** Every row on the wiki links to the file and line that holds it, with an **edit** link.
2. **Propose the change.** Click **edit**, or create a branch, change the record, and open a pull request that says
   why. If you can't push a branch here, GitHub's edit link opens the pull request from your fork for you.
3. **Discuss it in the pull request.** Its required check, `check`, validates the model, so a badly formed change
   can't be merged. The check's summary also shows how the change would alter the rendered pages.
4. **Decide.** The maintainers decide in the pull request. After a merge, an owner republishes the wiki from `main`.

**Publishing the wiki is manual for now.** An owner runs `uv run python scripts/render.py --mode live` from an
up-to-date `main`; it refuses unless the tree is clean, equal to `origin/main`, and valid. So the wiki can lag `main`
until that is run: the sidebar's commit says which version you are reading. Publishing it automatically after each
merge, from CI, is planned for WP7.

What to edit, by kind of change:

| You want to change | Edit | Notes |
|---|---|---|
| **The taxonomy**: a type, stage, tier or kind, its meaning, or the rules that propose a kind | [`data/taxonomy/kinds.yaml`](data/taxonomy/kinds.yaml), [`data/taxonomy/tiers.yaml`](data/taxonomy/tiers.yaml) | The rules are data, read in plain words on the Taxonomy page |
| **A policy**: what it asks, when it applies, its SOP steps or its citations | [`data/policies/<policy>.yaml`](data/policies/) | The SOP is rendered from the same file |
| **A repository's label**: its type and stage (its kind) | [`registry.yaml`](registry.yaml) | Any maintainer may merge a kind change. A repository's code owners can also declare its type with one topic: `openmbee-tool`, `openmbee-media`, `openmbee-research` or `openmbee-governance` |
| **A source**: a quoted passage or a new source | [`data/sources/`](data/sources/) | Quotes are verbatim; the licensed ISO standard is cited by clause number only |
| **The maintainers**, or their powers | [`data/maintainers.yaml`](data/maintainers.yaml) | Merged by an owner |

For a question that isn't ready to be a proposal, open an issue here.

## Why it exists

- **To help people find their way.** OpenMBEE has many repositories: some are experiments (Sandbox), some are
  established and versioned (Incubating), some are mature and widely relied on (Graduated), and some are kept for
  history (Archived). Newcomers and contributors need to see which is which.
- **To show that we follow our own rules.** Many organizations that use OpenMBEE work in regulated industries,
  including aerospace and defense. They need to see that who may change what, and who approves a release, follow
  written rules.
- **To add friction only where it is needed.** Graduated tools and the governance of the organization get the
  strictest controls; experiments, media and research stay easy to contribute to. Each policy says where it applies
  and why.

## The guidance we follow

Every policy cites its sources, and every source is quoted in its own words in [`data/sources/`](data/sources/):

- **Core:** CISA, *Open Source Software: Security Principles and Practices* (2026); NIST SP 800-37 Rev. 2 (the Risk
  Management Framework) with SP 800-53; OpenSSF, the project lifecycle (our stages) and the security baseline (the
  backbone of our policies); the DoD CIO memorandum *Software Development and Open Source Software* (2022).
- **Secondary:** the CNCF project lifecycle; ISO/IEC/IEEE 12207:2026, by clause number only; OFAC's sanctions
  regulations; NIST SP 800-218 (SSDF); NIST SP 800-161 Rev. 1.

The approach is **minimum viable policy**: a small set of policies, each cheap to show compliance with, using what
GitHub already provides on the Free plan; authority spread to each repository's code owners, with a light load on
the maintainers.

## How it works, in brief

A repository has a **type** (tool, media, research or governance) and a **stage** in its lifecycle (Sandbox,
Incubating, Graduated or Archived). Together they name its **kind**, and the kind gives its **tier** (high, medium,
low or none), which says how strict its controls are. Each policy says, with a rule over type, stage and tier, where
it is in effect. A kind says what a repository is, not whether its duties are done; that is what the policies check.

The repository is built as a model, a controller and views:

- **The model** is the YAML records, declared as database tables in
  [`data/schema/model.yaml`](data/schema/model.yaml).
- **The controller** is the Python in [`scripts/`](scripts/). `scripts/validate.py` admits only well-formed records,
  on every pull request.
- **The views** are rendered from the model and never committed. They include the wiki pages and, later, the issues
  the registry will open.

A repository out of line with a policy is not an error in the model; it is what the registry exists to find.

**It is not** an AI agent (no language model takes part in any decision), a project tracker, a replacement for each
repository's own contributing guide, or its own permission system: it uses GitHub's teams, roles, CODEOWNERS and
rulesets. It never deletes a repository.

## Roadmap in brief

1. **Agree on the model** (now): the maintainers review the pack and give five approvals: the taxonomy, the policies,
   the pilot (31 repositories), each pilot repository's kind, and the named maintainers.
2. **Sense and show status**: read the organization (read-only), show each repository's status against its policies
   on the wiki (a compliance dashboard), publish the wiki automatically from CI, and draft the issues it would open.
3. **Switch on and calibrate**, marked "calibrating, not yet the source of truth", and fix what it gets wrong.
4. **Make it official**: the first release makes this the source of truth, and its own rules tighten.

Details: [docs/status.md](docs/status.md) and [docs/roadmap.md](docs/roadmap.md).

## How to check everything

Everything runs in one locked environment (Python 3.10, PyYAML). Install it once with `uv sync --frozen`. The
required check on every pull request runs:

```bash
uv run python scripts/validate.py
uv run python -m unittest discover -s tests
```

To render every view, including the wiki pages, into `build/demo/` (ignored by git; nothing is written anywhere
else):

```bash
uv run python scripts/render.py
```

## Where to read more

- [docs/current-state.md](docs/current-state.md): **what is decided, and where it is recorded.** The place to start
  for anyone working on this repository.
- [docs/status.md](docs/status.md): where the work packages stand.
- [work-packages/](work-packages/): each package's scope, its decision records (the supervisor's answers, quoted)
  and its review.
- The early design documents ([design](docs/design.md), [roadmap](docs/roadmap.md),
  [testing](docs/testing-and-demonstration.md), [requirements](docs/requirements/)) are DRAFT inputs; where they
  disagree with the records, the records win.

If you work on this repository with an AI coding assistant, start with [AGENTS.md](AGENTS.md).

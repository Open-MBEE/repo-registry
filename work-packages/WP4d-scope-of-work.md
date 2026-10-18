# WP4d — Scope of work: the attestations file

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `repo-registry` (local; WP5, the move, is paused on `wp5-work` until WP4c and this package are accepted) |
| **Approval record** | mzargham's `git merge --no-ff -m "<message>"` of the scope branch into `main` ([AGENTS.md](../AGENTS.md)) |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` ([AGENTS.md](../AGENTS.md)) |

## Purpose

The supervisor, on the README's operator guidance (answer an attested check "in an attestation block in your
repository's `README.md`, committed by a code owner ... An attestation is out of date once it is older than your
latest release"): "this feels sloppy and a bit confusing i think we need a seperate attestations file, reserved
filename in root and simply have a pointer to it in the readme,md. it can even be yaml instead of markdown to improve
the ability to check that the required attestations are fresh. we need a way to bind the attestations file to the
release commit so a release always comes with attestations bound to it rather than a potentially stale file".

Today, WP0's direction item puts attestations "as a trailer in its README filled from a template", WP0 R-13's default
says "an attestation is out of date once it is older than the repo's latest release", and 9 SOPs show a Markdown
comment block for the README. This package replaces that with one machine-checkable file per repository, read at the
commit a release points to, so that what a release attests is fixed with the release. It lands before WP5, so the
repository published to Open-MBEE already says the new thing.

## Goals

- G1. **One attestations file per repository**, at a reserved path in its root, in YAML, with a pointer to it from
  the README.
- G2. **Attestations are bound to the release.** For a repository with releases, what counts is the file as it is at
  the commit of the latest release (OD1). The rule for a repository without releases is stated (OD2).
- G3. **The rule is checkable:** a format with a schema, and a statement of exactly when an attested check is green,
  red or yellow.

## Non-goals

- A checker for the file, and reading any repository's attestations live or opening issues about them: WP6, the
  engine (OD3).
- New attested checks, or changing what any check asks. Only where and how an operator answers changes.
- Writing to any other repository: the file is specified here; operators add it in their own repositories later.
- The governance kinds (WP4c) and the move (WP5).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The format: `docs/attestations-format.md` *(default)*, and a schema, `data/schema/attestations.schema.yaml` *(default)*, for the reserved file `ATTESTATIONS.yaml` *(default)* | G1, G3 |
| D-2 | The rule: in `docs/policy-format.md` ("Reading a check's result"), when an attested check is green, red or yellow, given the release binding (OD1) and the no-release rule (OD2) | G2, G3 |
| D-3 | The 9 SOPs with attested checks show the YAML entry for each check, and the README pointer line, in place of the README block | G1 |
| D-4 | A WP0 amendment record, `work-packages/WP0-amendment-3.md` *(default)*, replacing the direction item's "trailer in its README" and R-13's freshness default, with the current documents (README operator section, `docs/current-state.md`, `docs/policy-format.md`) and the early DRAFT documents (`design.md`, `requirements/`) edited in place (as WP4b OD1) | G1, G2 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The format names one reserved path, is YAML, and has a schema. Each entry names the policy, the check, who attests, the date, and the release it was made for (OD1). | Inspect; a test that the example in the format document meets the schema |
| R-2 | Every attested check in `data/policies/` can be answered in the file: each `policy`/`check` pair is one the policies define. | A test over the policies and the schema |
| R-3 | The rule says, for every case, whether the check is green, red or yellow: a release whose commit has the file with the entry, naming that release, by a code owner (green); the entry missing, naming another release, or by someone who isn't a code owner (red); the file can't be read (yellow); and, with no release, the file on the default branch, which doesn't go out of date (OD2). | Inspect the rule against the WP0 R-13 colors |
| R-4 | No document still tells an operator to attest in the README, except as superseded history. | `grep -rn -i "attestation block\|trailer in its README"` over `docs/`, `README.md` and `AGENTS.md`, inspected |
| R-5 | No policy's applicability, and no other outcome, changes. | The full test suite; `python3 scripts/policies.py` replays unchanged |

## Definition of good

- An operator knows in one reading where to put an attestation and when it must be renewed, and a program can tell
  from one file at one commit whether a release came with the attestations it needs.

## Definition of good enough

- D-1 to D-4 exist, and every requirement passes its check.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- Names and paths: the reserved file is `ATTESTATIONS.yaml` in the repository root; the format is
  `docs/attestations-format.md` with `data/schema/attestations.schema.yaml`; the record is
  `work-packages/WP0-amendment-3.md`.
- Each entry has `policy`, `check`, `attested_by` (a GitHub login), `date`, `release` (the release's tag, OD1, or `none`,
  OD2), and an optional `note`. Who committed it
  is read from git, not from the file: an entry counts only if the last commit that changed the file, up to the
  commit being read, is by a code owner (as WP0 R-17 says now).
- The README pointer is a recommended line in each SOP ("Attestations: see `ATTESTATIONS.yaml`"). It is not a check.
- The org's own attested check (`maintainers-match`, `other-powers-declared`) is answered in this repository's
  `ATTESTATIONS.yaml`, since this repository is where the org is governed.
- The format document says how a release binds the file with GitHub's own release and tag (a release names a tag, the
  tag names a commit), with nothing added to the release.

## Open decisions (for the supervisor)

- **OD1.** What binds an attestation to a release. *Decided: named per release. The entry is in the file at the
  release's commit, committed by a code owner, and names that release (its tag), so every release is attested afresh.*
- **OD2.** A repository with attested checks but no release. *Decided: read the file on the default branch; with no
  release it never goes out of date. Its entries name the release as `none`.*
- **OD3.** What WP4d builds beyond the specification. *Decided: nothing: the specification only. WP6 builds the
  checker.*
- **OD4.** The Agent's defaults. *Decided: approved.*

None remain open. Every item was resolved through the decision loop: 4 decided, 0 deferred, 0 raised. The records
are in [WP4d-decisions.md](WP4d-decisions.md).

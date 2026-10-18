# WP5b — Scope of work: data consistency and integrity audit

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | [Open-MBEE/repo-registry](https://github.com/Open-MBEE/repo-registry) |
| **Approval record** | mzargham's merge, with a merge commit, of the pull request that adds this document into `main` (WP5 OD3). It can merge only after WP5's delivery PR (#1), which brings the required check to `main` |
| **Acceptance record** | mzargham's merge, with a merge commit, of the delivery pull request into `main` (WP5 OD3) |

## Purpose

The supervisor, after WP4e: "i see other inconsistencies in how our registry works, we've seperated stage and type in
the registry but we use kind (the combined name) in many other places. i made the change so we had two fields in our
yaml but the inconsitency with the other yaml where it seems like kind (the combined one) is being used as a key. we
need to do a serious audit for data and schema consistency, integrity, etc. this needs to be the next work package".
And, scoping it: "address the data consistency and integrity concerns i flagged about inconsistency keys, joins, etc
across our yaml files. even though this is a git repo. for the purpose of this analysis let's treat it like a
database".

So this package treats the repository's data files as the tables of a database: each file (or family of files, such
as one policy per file) is a table with rows, columns, a primary key, foreign keys into other tables, and integrity
constraints. A first survey, for scale:

- **Kinds as a combined key.** After WP4e the kind list stores `type` and `stage`, but the combined kind name
  (`tool/sandbox`) is still a key or a stored value in `data/taxonomy/kinds.yaml` (the kinds are keyed by it),
  `data/pilot.yaml`, `data/pilot-rule.yaml` and three reports: about 530 occurrences outside the kind list.
- **Repository names** are the join key across at least seven files (the kind list, assignments, pilot, exclude list,
  deviations, three reports, and the snapshot's `repos.json` and `usage.json`), with no stated rule about case,
  renames, or repositories that leave the org.
- **Logins** join `data/maintainers.yaml`, `data/deviations.yaml` and `data/proposed-codeowners`; **policy and source
  IDs** join the policies to `data/sources/` and `_departures.yaml`.
- **Schemas:** 2 of about 40 data files have one (the kind list and attestations). The rest are checked only by code
  in `scripts/validate.py` (WP5), or not at all.
- **Stored derived values:** the pilot and the reports store values computed from other tables (kind, tier), which can
  disagree with their source.

## Goals

- G1. **A data model:** every table, its columns, its primary key, its foreign keys, and which values are stored and
  which are derived, written down in one place.
- G2. **An audit against that model:** every inconsistency in keys, joins, naming, redundancy, schema coverage and
  integrity, each with its location and its consequence.
- G3. **Integrity that holds:** per OD1, the findings fixed, and the model enforced on every pull request, so that a
  broken key or join is invalid state and can't reach `main` (WP0 R-14).

## Non-goals

- Changing any outcome: every repository keeps its type and stage, every policy applies to the same repositories, and
  the pilot, exclude list and license results stay the same. Only how the data is keyed, joined, stored and checked
  may change.
- New policies, kinds, types, stages or tiers.
- Moving the data out of YAML into a database engine. The files stay YAML in git; "database" is the lens.
- The engine's sensing and status log (WP6). Their tables join the model when WP6 builds them.
- The text of the stored sources (`data/sources/`, snapshots), which are external facts: they are modelled as
  read-only source tables, not rewritten.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The data model: `docs/data-model.md` *(default)*, with an entity–relationship diagram, and a machine-readable form, `data/schema/model.yaml` *(default)*: each table's file, primary key, columns, foreign keys and derived columns | G1 |
| D-2 | The audit report: `work-packages/WP5b-audit.md` *(default)*, every finding with its table, column, rows affected, the constraint it breaks, and a proposed fix | G2 |
| D-3 | Per OD1: the fixes, with no outcome changed | G3 |
| D-4 | Per OD1: the model enforced, by `scripts/validate.py` reading `data/schema/model.yaml` (primary keys unique, foreign keys resolve, derived values match their source), with a test per constraint and a deliberately broken join that fails | G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every data file under `data/` and `registry.yaml` is a table in the model, or listed as outside it with a reason. | A test: the model's files equal the data files |
| R-2 | Every table has a primary key; every column that refers to another table is declared as a foreign key to that table's key. | Inspect the model; a test that every declared foreign key names a table and a key that exist |
| R-3 | Every finding in the audit names its table, its column, the rows affected and the constraint broken, and is reproducible by a command or a query over the files. | Inspect; rerun each finding's command |
| R-4 | Per OD1: in the data on `main`, every primary key is unique, every foreign key resolves, and every stored derived value equals the value derived from its source. | `scripts/validate.py`; the full test suite |
| R-5 | Per OD1: a pull request that breaks a key or a join fails the required check. | A trial PR with a deliberately broken join, as WP5 D-5 |
| R-6 | No outcome changes (see non-goals). | Compare the kind list's computed kinds, the applicability table, pilot, exclude list and license report before and after |

## Definition of good

- Someone who knows databases, reading `docs/data-model.md`, can say for any fact where it is stored once, how every
  other place that shows it joins to it, and which check would fail if it drifted.

## Definition of good enough

- D-1 and D-2 exist, and, per OD1, D-3 and D-4; every requirement passes its check.
- Every finding in the audit has a disposition agreed with the supervisor.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- Package name WP5b: it follows WP5 and comes before WP6, which builds on the data.
- Paths: `docs/data-model.md`, `data/schema/model.yaml`, `work-packages/WP5b-audit.md`, `tests/test_wp5b.py`.
- The audit covers, at least: primary keys and their uniqueness; foreign keys and orphans; composite keys stored as
  joined strings (the kind name); case and spelling of keys (repository names, logins); stored derived values that
  can drift (kind, tier in the pilot and reports); naming of the same attribute in different files; files with no
  schema; nullable or optional columns with no stated meaning; ordering rules; and the snapshot's role as a source
  table.
- The model's machine-readable form is plain YAML read by `validate.py`, using only PyYAML (no new dependency).
- Generated files (the pilot, exclude list and reports) are modelled as views: derived tables that must equal what
  their generator writes from the source tables (WP5 R-3), whatever OD2 decides about storing derived columns in them.
- The work is built on a branch and delivered as a pull request; the trial PR for R-5 is closed unmerged, with a
  comment, as in WP5.

## Open decisions (for the supervisor)

- **OD1.** What this package delivers. — options: the audit only (the model and the findings, D-1 and D-2); fixes
  are a later package scoped from the findings / the audit, then the fixes and enforcement in this package, with a
  mid-package check-in where the supervisor disposes each finding before any fix is made.
- **OD2.** The combined kind name. — options: no file stores or keys by it; `kinds.yaml` is keyed by type and stage,
  and every view stores type and stage, deriving the name only for display / the name stays as a derived label and
  `kinds.yaml`'s key, with type and stage the stored columns everywhere else / decide from the audit's findings.
- **OD3.** Repository identity. Repositories are joined by name, which can change and differs in case. — options:
  name stays the key, with case and rename rules stated and checked / GitHub's numeric repository ID becomes the
  key, with the name as a column / decide from the audit's findings.
- **OD4.** The Agent's defaults above.

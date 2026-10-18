# WP5b — Scope of work: the model, its integrity, and views out of the model

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | [Open-MBEE/repo-registry](https://github.com/Open-MBEE/repo-registry) |
| **Approval record** | mzargham's merge, with a merge commit, of the pull request that adds this document into `main` (WP5 OD3) |
| **Acceptance record** | mzargham's merge, with a merge commit, of the delivery pull request into `main` (WP5 OD3) |

## Purpose

The supervisor: "we need to do a serious audit for data and schema consistency, integrity, etc." and "for the purpose
of this analysis let's treat it like a database". The architecture he set for it ([WP5b-decisions.md](WP5b-decisions.md)):
model, view, controller, with CI/CD. This is the software pattern, a different reading of "control" from the formal
model's control loop.

- **Model:** the repository's records (the kind list, taxonomy, policies, maintainers, deviations, sources and
  snapshots), with their schemas and constraints. Only correctly constructed records enter it; CI rejects the rest
  (WP0 R-14, WP5).
- **Controller:** the Python. It checks the model's invariants, and renders views from it, deterministically.
- **Views:** what people read: the wiki, the issue texts, and every generated document and report. "views are not
  committed. they are generated": each is rendered by a CD step that runs only if CI passes, and a deterministic
  pipeline "uniquely determine[s] what views they output so we don't need to store the outputs locally".

Today the model breaks that shape in several ways (a first survey):

- **A composite key stored as a string.** The kind name (`tool/sandbox`) is "useful shorthand but shorthand
  nonetheless", yet `data/taxonomy/kinds.yaml` is keyed by it, and the pilot and three reports store it, about 530
  times outside the kind list.
- **A weak key.** Repositories are joined by name, which can change, across at least seven files. GitHub's numeric
  repository ID is the stronger key ("our solution is tied to github so we should use its affordances").
- **Views stored in the model.** Four reports, the applicability table, the briefing, and
  parts of the SOPs and the basis review are generated or derived, yet committed, some of them by hand.
- **Undeclared joins.** Logins join maintainers, deviations and CODEOWNERS; policy and source IDs join the policies to
  `data/sources/`. None of these is declared; 2 of about 40 data files have a schema.

## Goals

- G1. **A declared model:** every table, its primary key, its columns, its foreign keys, in one machine-readable place.
- G2. **An audit against it,** each finding disposed by the supervisor at a check-in before anything is fixed.
- G3. **A normalized model:** type and stage stored and keyed everywhere, the kind name derived only for display;
  repositories keyed by GitHub's repository ID; no derived value stored in the model.
- G4. **Views out of the model:** every view rendered by a deterministic controller pipeline, none committed, and the
  hand-written markdown that carries derived facts generated from schema-compliant data wherever possible.
- G5. **The controller enforces the model** on every pull request: unique keys, resolving joins, schema-valid rows.

## Non-goals

- Changing any outcome: every repository keeps its type and stage, every policy applies to the same repositories, and
  the pilot, exclude list and license results are the same, as rendered views.
- The taxonomy refinements from WP4's fit analysis: WP5c.
- Writing issues (WP6), and deploying the wiki (WP7). The render pipeline's live mode, which would write them, is
  added there, gated on CI and on an explicit switch; this package builds demo mode only (OD5).
- A database engine: the model stays YAML and Markdown in git; "database" is the lens.
- Rewriting the stored sources (`data/sources/`, snapshots): they are read-only source tables.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The model: `data/schema/model.yaml` *(default)*, each table's file, primary key, columns, foreign keys; a schema per table; `docs/data-model.md` *(default)* rendered from it, with an entity–relationship diagram | G1 |
| D-2 | The audit: `work-packages/WP5b-audit.md` *(default)*, each finding with its table, column, rows, the constraint broken and a proposed fix, reproducible by a command; then a check-in where the supervisor disposes each finding | G2 |
| D-3 | The normalization, per the dispositions: kinds keyed by type and stage; the kind list and every table that names a repository keyed by its GitHub ID; derived values out of the model | G3 |
| D-4 | The views: a deterministic render pipeline with a mode toggle, demo mode only (OD5), that builds every view from the model into an ephemeral directory; generated files removed from the repository; the SOPs' derived parts and the basis review's tables generated; CI renders the views in demo mode on every run | G4 |
| D-5 | The enforcement: `scripts/validate.py` reads `data/schema/model.yaml` and checks keys, joins and schemas; a test per constraint; a trial PR that breaks a join fails, closed unmerged, as WP5 D-5 | G5 |
| D-6 | The documents and status updated, in the same PRs (the supervisor's process rule); a record of the change to WP1 and WP2 formats | G1, G3, G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every file in the repository is a model table, a controller, a view template, or a hand-written document, as the model declares; nothing else. | A test: every tracked file falls in one class |
| R-2 | Every table has a primary key and a schema; every column that refers to another table is a declared foreign key. | A test over `model.yaml`; inspect |
| R-3 | Every audit finding names its table, column, rows and constraint, and reproduces by a command. | Rerun each finding's command |
| R-4 | On `main`, every primary key is unique, every foreign key resolves, and every row meets its table's schema. | `validate.py`; the full test suite |
| R-5 | No view is committed; each renders deterministically (twice, identical), from the model alone; in demo mode the pipeline writes only inside its ephemeral directory, never to GitHub. | A test (including that demo mode makes no GitHub call); the CI render step |
| R-6 | No stored value can be derived from another table. The kind name appears only in rendered views. | A test over the model's columns |
| R-7 | A pull request that breaks a key or a join fails the required check. | The trial PR |
| R-8 | No outcome changes. | Render the pilot, exclude list, applicability and license views before and after, and compare |

## Definition of good

- Someone who knows databases can read the model, say where each fact is stored once and how every view is derived
  from it, and trust that `main` can't hold a broken key or join.

## Definition of good enough

- D-1 to D-6 exist, every requirement passes its check, and every audit finding has the supervisor's disposition.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- Package names: WP5b (this), WP5c (the taxonomy). Paths as named in the deliverables, plus `tests/test_wp5b.py`.
- **Repository IDs:** the stored snapshot has no IDs, so one read-only `gh` GET per repository records the ID for each
  name in the snapshot (`data/snapshots/2026-10-18/ids.json`, with when it was read), and `snapshot.py` records the ID
  from now on. `repo-registry`'s own ID is read the same way. The kind list keys each entry by ID, with `name`, `type`
  and `stage` as columns, so a change of stage is still one line.
- **The pilot list** (OD6) is a model table keyed by repository ID, with its category and reason; it stores no kind
  (that is derived). What the pilot rule would propose today is rendered as a view, so a difference between the rule
  and the kept list is visible, not an error.
- **Views:** a single render command (`uv run python scripts/render.py --mode demo`, demo the default and the only
  mode for now) writes every view into an ephemeral directory (`build/demo/`, ignored by git, emptied on each run).
  CI uploads it as the run's artifact. CI runs it on every pull request, and writes the views' differences from
  `main` into the run's job summary, so a pull request still shows what its change would do (README, governor role).
  WP5's replay check (R-3) becomes the determinism check (R-5).
- **SOPs:** the parts derived from a policy's data (what it applies to, its checks, its citations, its attestation
  entries) are generated from the policy's YAML; the hand-written parts stay, in a template per SOP.
- The audit covers at least: keys and their uniqueness; foreign keys and orphans; composite keys as strings; case and
  spelling of keys; stored derived values; the same attribute named differently in different files; files with no
  schema; optional columns with no stated meaning; ordering rules; the snapshot as a source table.
- The model's machine-readable form is plain YAML read with PyYAML; no new dependency.
- Each step lands as a pull request with its status update; the trial PR is closed unmerged with a comment.

## Open decisions (for the supervisor)

- **OD1.** Audit only, or audit plus fixes. *Decided: audit plus fixes, with a check-in where the supervisor disposes
  each finding before any fix.*
- **OD2.** The kind name. *Decided: type and stage stored and keyed everywhere; the name is derived shorthand, for
  display.*
- **OD3.** Repository identity. *Decided: GitHub's numeric repository ID is the key; the name is a column.*
- **OD4.** Are views committed. *Decided: no. Views are rendered by deterministic CD steps gated on CI.*
- **OD5** *(raised by OD4)*. Where people read the views before the wiki exists. *Decided: a demo mode. The render
  pipeline has a toggle; in demo mode it writes every view (and, once WP6 and WP7 add them, the wiki pages and issue
  texts) to an ephemeral directory, showing what would be written if the writes were turned on. Only demo mode exists
  in this package. In control terms: simulating the plant to test the controller before turning it on, so its
  behaviour can be approved first.*
- **OD6** *(raised by OD4)*. The pilot list. *Decided: a model table. The pilot rule writes it once; then it is kept
  and changed only by a governed pull request, so the approved list is stored and a later change to the rule can't
  silently move it.*
- **OD7.** The Agent's defaults. *Decided: approved.*

None remain open. Every item was resolved through the decision loop: 7 decided, 0 deferred, 2 raised (OD5, OD6). The
records are in [WP5b-decisions.md](WP5b-decisions.md).

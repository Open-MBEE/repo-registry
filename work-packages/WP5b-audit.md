# WP5b — Data audit (D-2)

> The repository's records audited as the tables of a database, against the declared target model
> [`data/schema/model.yaml`](../data/schema/model.yaml). Each finding reproduces with
> `uv run python scripts/audit.py F-nn`, which prints its rows; a fixed finding prints none (WP5b R-3).
> Dispositions are the supervisor's, at the check-in (WP5b OD1), recorded in [WP5b-decisions.md](WP5b-decisions.md).

## What already holds

Before the findings, the integrity that today's data already has, checked by the same queries:

- No orphans: every repository named in the pilot, exclude list, usage, reports, pilot rule and release authority is in
  the kind list. No two repository names differ only in case.
- The proposed CODEOWNERS lists exactly the maintainers. Check IDs are unique across all 21 policies (40 checks).
- Every policy's citations resolve to `data/sources/` (WP5 meta-rule 7), and every baseline item and CISA practice is
  adopted or departed, not both (meta-rules 8 and 9).

## Findings

| ID | Finding | Rows | Constraint broken | Proposed fix | Settled by |
|---|---|---|---|---|---|
| F-01 | The kind table is keyed by the kind name, a composite key stored as one string; each row also stores `type` and `stage`, so the key repeats two columns | 16 (15 kinds, 1 omitted) | A composite key is its columns; no column is stored twice | Key `kinds` and `omitted` by type, then stage (nested maps); the name is derived | OD2 |
| F-02 | The kind name is stored as a value outside the kind table | 5 files, about 530 values (the pilot, the pilot rule's predicate, 3 reports) | Store the key's columns, not a derived label | Pilot and rule use `type` and `stage`; the reports become views (F-07) | OD2 |
| F-03 | Repositories are keyed and joined by name in 11 places; no table has GitHub's repository ID | 11 tables or columns | The strongest key GitHub offers | Read each repository's ID once into the snapshot (`ids.json`); key every repository column by it, with `name` as a column | OD3 |
| F-04 | `repo-registry` is in the kind list but has no source row: the snapshot predates it | 1 | Every foreign key resolves | Its ID is read with the others; the snapshot gets a row for it, marked as read after the snapshot | OD3 |
| F-05 | People are keyed and joined by login, which a user can change; no table has GitHub's user ID | maintainers (4), proposed CODEOWNERS, deviations' `approved_by` | The strongest key GitHub offers (OD3's reasoning, applied to people) | Key maintainers by user ID, with `login` as a column; CODEOWNERS and `approved_by` join to the login, which a check ties to the ID | check-in: fix |
| F-06 | A foreign key held in prose: `_future.yaml`'s `would_strengthen` lists policies in a sentence, and one name (`maintainer-policy`) is a document, not a policy | 5 rows, 1 dangling | Every foreign key resolves | `strengthens: [policy ids]` plus a `note`; the document reference moves to the note | check-in: fix |
| F-07 | Views are committed: 4 reports and 2 generated documents | 6 files | Views are not committed (OD4) | Remove them; `render.py` builds them in demo mode (OD5) | OD4 |
| F-08 | Hand-written documents state derived facts that can drift: every SOP's "Applies to" line and attestation entries, the basis review's tables, and counts in 4 documents | 43 places | One fact, one place; views are rendered (answer 6) | Generate the SOPs' derived parts and the basis tables; replace counts in hand-written documents with links to the rendered views | answer 6 |
| F-09 | The pilot list (a model table, OD6) stores each member's kind, a derived value | 32 | No stored value is derivable (R-6) | Drop `kind` from the pilot list; the briefing derives it | OD6 |
| F-10 | The exclude list stores the same reason in all 150 rows | 150 | A constant isn't stored per row | A table-level `default_reason`; a row stores a reason only when it differs | check-in: fix |
| F-11 | Columns named inconsistently: `status` means a lifecycle mark in model files and a color in reports; a row's reason is `reason`, `why`, a bare value, `decision` or `basis` | 3 patterns | One name, one domain | `status` only for the lifecycle mark, `color` for a check's result; `reason` everywhere for why a row is as it is, except `decision` (the record that set it) and `basis` (why a person is listed), which mean other things and stay | check-in: fix |
| F-12 | Only the kind list has a schema; the other 41 data files are checked by code, or not at all | 41 | Every table has a schema (R-2) | A schema per table, generated from `model.yaml`, and checked by `validate.py` | R-2 |
| F-13 | Every policy file repeats `status` and `provisional_until`, a fact about the whole policy set | 21 | A table-level fact is stored once | One `data/policies/_set.yaml` holds the set's status; policy files drop the two fields | check-in: fix |
| F-14 | The snapshot path is stored as a string in 5 files | 5 | A foreign key is declared, and stored once | `model.yaml` names the current snapshot once; tables refer to it | check-in: fix |
| F-15 | Predicates read columns declared nowhere: 4 derived from the snapshot (`has_semver_release`, `latest_semver_major`, and the pilot's `kind`, `type`, `tier`, `archive_candidate`, `clone_uniques_14d`) | 7 columns | Every column a predicate reads is declared | Declare the derived columns, and which controller derives them, in `model.yaml`; `validate.py` rejects a predicate that reads an undeclared column | check-in: fix |
| F-16 | An undeclared join by naming convention: expected gap `XF-n` ↔ test `test_XFn` | 2 | Joins are declared | Revised: every control names its test, in two classes. **Construction controls** (meta-rules) fail CI when violated. **Compliance controls** (policy checks) never fail CI; a known non-pass (like XF-2) is kept as a measurement, the error signal the feedback loop remediates. A capability not built yet (like XF-1) is tracked separately as forthcoming | check-in: fix, revised |

## Dispositions

Every finding is to be fixed (the check-in, [WP5b-decisions.md](WP5b-decisions.md)): none is accepted as is or moved
to a later package. F-16 is fixed as revised by the supervisor: two kinds of error are never mixed. A **construction
error** (a malformed record, a broken rule of the model, broken software) is invalid and CI rejects it. A **compliance
error** (a measured gap between a policy and the governed system) is the controller's error signal: valid, kept, and
remediated through the feedback loop, never a CI failure.

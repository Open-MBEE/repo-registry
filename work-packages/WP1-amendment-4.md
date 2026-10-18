# WP1 — Amendment 4: type and stage in the kind list

Made by [WP4e](WP4e-scope-of-work.md), approved by mzargham's merge f405aa4. Decisions are recorded verbatim in
[WP4e-decisions.md](WP4e-decisions.md).

## What WP1 said

WP1 D-4 defined the kind list with one field per entry, `kind: type/lifecycle` (for example `kind: tool/sandbox`),
or `kind: unclassified` with a `reason`; the org's entry had `name` and `kind`. The taxonomy, the applies-if rules
and the code called the stage attribute `lifecycle`.

## Why it changes

The supervisor: "looking at our registry yaml schema it seems strange to me that we're using slash to make kind out
of the repo type and lifecycle stage. this should be type and stage. we can compute kind from it where we need to".

## What replaces it

- Each entry of `registry.yaml` and `data/assignments.yaml` holds `type` and `stage`, or, for a repository the rules
  can't classify, a `reason` alone (WP4e OD2). The org's entry holds `name`, `type` and `stage`.
- The kind is computed from type and stage (`scripts/recommend.py`, `kind_of`). Kinds keep their names, such as
  `tool/sandbox`, as computed labels in `data/taxonomy/kinds.yaml`, the applicability table and the reports.
- The attribute is called `stage` everywhere in the data and code: `stages` in the taxonomy, `stage` in each kind
  and in every applies-if rule (WP4e OD1). Prose says "stage", "the lifecycle" or "stage in the lifecycle", as fits.
- A change of kind is still one line: the stage (or the type).
- No outcome changed: every repository's computed kind equals its kind before, and the applicability table, pilot,
  exclude list and every report are identical.

## Updated

`registry.yaml`, `data/assignments.yaml`, `data/taxonomy/kinds.yaml`, the applies-if rules of the policies,
`data/pilot-rule.yaml` (attribute list), `data/schema/kind-list.schema.yaml`; `scripts/recommend.py`, `policies.py`,
`pilot.py`, `licenses.py`; `docs/kind-list-format.md`, `docs/policy-format.md`, the SOPs' "Applies to" lines and the
license-by-type SOP, `AGENTS.md`, and the DRAFT `docs/requirements/formal-model.md`; tests `test_wp1.py`,
`test_wp2.py`, `test_wp2a.py`, `test_wp4c.py`, the test fixtures, and the new `test_wp4e.py`.

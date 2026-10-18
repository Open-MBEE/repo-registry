# Canonical kind list format

> **PROVISIONAL** until the maintainers approve the taxonomy (WP0, maintainer approval 1). WP1 D-4.

The canonical kind list is the one file that says what each repo is. It is `registry.yaml`, at the root of this
repo: a model table (WP5b). For each repo it holds the two attributes people decide, its **type** and its **stage** in
the lifecycle, and the same for the organization's own administration. The kind is computed from them: a kind is the
point that a type and a stage name, written `type/stage` (for example `tool/sandbox`) as shorthand, and it gives the
repo its tier. Policies attach to the type, the stage or the tier (WP0 A1; WP4e). The rest lives elsewhere: the
kind's tier is in [kinds.yaml](../data/taxonomy/kinds.yaml), and which policies are in effect for each kind is the
applicability view (WP2 D-5). Evidence for a recommended kind is the recommendation view, never the kind list.

Each entry is keyed by **GitHub's numeric repository ID** (WP5b OD3), the strongest key GitHub offers: a repository
can be renamed, its ID never changes. The name is a column, checked against the snapshot, so a rename shows up as an
invalid entry rather than a silent broken join. The kind list's rows, and every other table, are declared in
[data/schema/model.yaml](../data/schema/model.yaml), which `scripts/validate.py` enforces on every pull request.

## Shape

```yaml
# PROVISIONAL. NOT APPROVED. ...            # first line, only while status is provisional
status: provisional                         # provisional | approved
provisional_until: "WP0 maintainer approval 4: the assigned kind of each repo in the registry"
org:
  name: Open-MBEE
  type: governance                          # the administration of the GitHub org itself (WP1 A2, A4, amendment 3)
  stage: graduated
repos:
  160235647:                                # GitHub's repository ID (WP5b OD3)
    name: "exec-mms"
    type: tool
    stage: incubating
  1424079165:
    name: "repo-registry"
    type: governance                        # assigned by decision, see data/assignments.yaml (low until calibrated)
    stage: sandbox
  1422498382:
    name: "fprime"
    reason: "A fork of an upstream project. The taxonomy has no kind for forks yet (a parked item in design.md; ..."
```

## Meta-rules

These are the rules a valid kind list must meet, enforced in CI (WP0 R-14; WP5; WP5b). A kind list that breaks one
is **invalid** and must not reach `main`. A repo being out of compliance with its policies is still **valid**.

1. **One file.** The kind list is `registry.yaml` at the repo root. Its top-level keys are exactly `status`, `org`,
   `repos`, and optionally `provisional_until`. `org` has exactly `name`, `type` and `stage`, and they name a kind
   defined in `data/taxonomy/kinds.yaml`. The snapshot it was drafted from is declared once, in `model.yaml`.
2. **Status.** `status` is `provisional` or `approved`.
3. **Provisional is marked.** If `status` is `provisional`, then `provisional_until` is a non-empty string naming the
   maintainer approval that lifts the mark, and the file's first line starts with `# PROVISIONAL` (WP1 R-10). If
   `status` is `approved`, there is no `provisional_until`.
4. **One entry per repo.** `repos` maps each repository's ID to one entry, and every repository in the snapshot (or
   read after it) has one. An entry's `name` is the repository's name in the snapshot.
5. **A type and a stage.** An entry has `type` and `stage`, and together they name a kind defined in
   `data/taxonomy/kinds.yaml` (not an omitted one). An entry never names a kind, a tier or a policy: those follow
   from the type and stage.
6. **Unclassified says why.** An entry the rules can't classify has a non-empty `reason` and neither `type` nor
   `stage` (WP4e OD2). Its kind is `unclassified`.
7. **No other fields.** An entry has no keys other than `name`, `type`, `stage` and `reason`.
8. **Sorted.** Entries are sorted by repo name, ignoring case, so that every change is a small, local diff.
9. **Public repos only.** No private repo appears (WP1 OD2): the snapshot holds public repositories only.
10. **The taxonomy is complete.** Every kind in `kinds.yaml` names a tier in `data/taxonomy/tiers.yaml`, and every
    tier is used by at least one kind (WP1 R-6). Every kind in the type × stage cross product is either defined
    or listed under `omitted` with a reason (WP1 R-3).

## Changing a repo's kind

A change of kind is a one-line edit to one entry (WP0 R-12): its stage, or its type. It is proposed by a PR to this
repo and merged by any maintainer (WP4b OD3). Nothing else needs regenerating: the views are rendered from the kind
list on every run, never stored (WP5b OD4).
For example, when a tool releases `1.0.0` and moves from Sandbox to Incubating:

```diff
   1318945311:
     name: "OpenSysML"
     type: tool
-    stage: sandbox
+    stage: incubating
```

Moving an unclassified repo into a kind replaces its `reason` line with a `type` and a `stage` line. That is still one
entry, and the change is just as readable.

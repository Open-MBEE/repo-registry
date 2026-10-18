# Canonical kind list format

> **PROVISIONAL** until the maintainers approve the taxonomy (WP0, maintainer approval 1). WP1 D-4.

The canonical kind list is the one file that says which kind each repo is. It is `registry.yaml`, at the root of
this repo. It holds only enough to look up each repo's kind, and the kind of the organization's own administration.
A kind gives a repo its type, lifecycle and tier, and policies attach to those (WP0 A1). The rest of the chain lives elsewhere: the kind's tier
is in [kinds.yaml](../data/taxonomy/kinds.yaml), and the tier's policies come in WP2. Evidence for a recommended kind
goes in the recommendation report (`data/reports/kind-recommendations.yaml`), never in the kind list.

YAML is the starting point (WP0), not a decision. The machine-readable schema is
[kind-list.schema.yaml](../data/schema/kind-list.schema.yaml).

## Shape

```yaml
# PROVISIONAL. NOT APPROVED. ...            # first line, only while status is provisional
status: provisional                         # provisional | approved
provisional_until: "WP0 maintainer approval 4: the assigned kind of each repo in the registry"
org:
  name: Open-MBEE
  kind: governance/maintained              # the administration of the GitHub org itself (WP1 A2)
snapshot: data/snapshots/2026-10-18         # the snapshot the recommendations came from (optional)
repos:
  "exec-mms":
    kind: tool/maintained
  "repo-registry":
    kind: governance/experimental           # assigned by decision, see data/assignments.yaml
  "fprime":
    kind: unclassified
    reason: "A fork of an upstream project. The taxonomy has no kind for forks yet (WP0 parked item)."
```

## Meta-rules

These are the rules a valid kind list must meet. WP5 enforces them in CI (WP0 R-14). A kind list that breaks one
is **invalid** and must not reach `main`. A repo being out of compliance with its policies is still **valid**.

1. **One file.** The kind list is `registry.yaml` at the repo root. Its top-level keys are exactly `status`, `org`,
   `repos`, and optionally `snapshot` and `provisional_until`. `org` has exactly `name` and `kind`, and `org.kind`
   is a kind defined in `data/taxonomy/kinds.yaml`.
2. **Status.** `status` is `provisional` or `approved`.
3. **Provisional is marked.** If `status` is `provisional`, then `provisional_until` is a non-empty string naming the
   maintainer approval that lifts the mark, and the file's first line starts with `# PROVISIONAL` (WP1 R-10). If
   `status` is `approved`, there is no `provisional_until`.
4. **One entry per repo.** `repos` maps each repo's name, exactly as in the org, to one entry. No two names are equal
   when compared without case.
5. **A kind, and nothing else.** Each entry has `kind`. Its value is a kind defined in `data/taxonomy/kinds.yaml`, or
   `unclassified`. An entry never names a type, lifecycle, tier or policy: those all follow from the kind.
6. **Unclassified says why.** An entry has a non-empty `reason` if and only if its kind is `unclassified`.
7. **No other fields.** An entry has no keys other than `kind` and `reason`.
8. **Sorted.** Entries are sorted by repo name, ignoring case, so that every change is a small, local diff.
9. **Public repos only.** No private repo's name appears (WP1 OD2).
10. **The taxonomy is complete.** Every kind in `kinds.yaml` names a tier in `data/taxonomy/tiers.yaml`, and every
    tier is used by at least one kind (WP1 R-6). Every kind in the type × lifecycle cross product is either defined
    or listed under `omitted` with a reason (WP1 R-3).

## Changing a repo's kind

A change of kind is a one-line edit to one entry (WP0 R-12), proposed by a PR to this repo and merged by governors.
For example, when a tool reaches `1.0.0`:

```diff
   "OpenSysML":
-    kind: tool/experimental
+    kind: tool/active-development
```

Moving an unclassified repo into a kind also removes its `reason` line. That is still one entry, and the change is
just as readable.

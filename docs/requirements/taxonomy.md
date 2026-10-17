# Requirements — taxonomy

> **DRAFT.** Nothing here is locked until mzargham says "lock." Columns and sources are defined in
> [design.md](../design.md#requirement-conventions).

The taxonomy is the state-space structure: the classes, and the rule that puts a repo in each one. It defines no
controls (those are in [policy.md](policy.md)).

| ID | Requirement | Src | Assessed by |
|---|---|---|---|
| TX-1 | Small: every class page fits on one screen. *(Draft: ≤ 8 classes.)* | M, S | Count; page length |
| TX-2 | Defines only classes and membership rules over `U`. No controls. | M | Doc review |
| TX-3 | Membership rules are mutually exclusive and decidable from attributes. | M | Overlap check over the inventory |
| TX-4 | Validated against the hypothetical case and against the live inventory (read-only). `unclassified` repos trigger a taxonomy review, not a force fit. | M, E | Fit-test report |
| TX-5 | Scope is every repo in `Open-MBEE`, forks included, minus an explicit exclude list. Excluding a repo is a fail-safe for misfits, used only when needed. Every exclusion is visible, with its reason. Only governors may exclude. | M | Inventory diff: org repos − registry = exclude list exactly |

**Draft starting point (from the Slack post; not decided):** kind ∈ {tool, media, research} × lifecycle ∈
{active development, maintained, exploratory, archived}, sparsely populated. Open: the final class set, and an
exploratory class that `repo-registry` itself fits (X-9).

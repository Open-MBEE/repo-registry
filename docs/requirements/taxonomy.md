# Requirements — taxonomy

> **DRAFT.** Nothing here is locked until mzargham says "lock." Columns and sources are defined in
> [design.md](../design.md#requirement-conventions).
>
> Brought in line with the decision records at the WP4b docs sweep (2026-10-18); each changed requirement says
> "(updated: <record>)". The consistent summary is [current-state.md](../current-state.md).

The taxonomy is the state-space structure: the kinds, and the rules that recommend a kind for a repo. A kind is a
named point in the space of three categorical attributes: type, lifecycle stage and tier (the tier set by type and
stage) *(updated: WP0-decisions "The model, stated precisely")*. It defines no controls (those are in
[policy.md](policy.md)).

| ID | Requirement | Src | Assessed by |
|---|---|---|---|
| TX-1 | Small: every kind page fits on one screen. *(The draft cap of 8 was dropped; updated: WP1-decisions OD3 follow-up.)* | M, S | Count; page length |
| TX-2 | Defines only kinds and their recommendation rules over `U`. No controls *(updated: WP0 terminology)*. | M | Doc review |
| TX-3 | Recommendation rules are mutually exclusive and decidable from attributes: no repo is recommended two kinds *(updated: WP1 R-5)*. | M | Overlap check over the inventory |
| TX-4 | Validated by the read-only fit analysis of all of the org's public repos and by the pilot of real repos *(updated: WP0 D-5, D-6)*. `unclassified` repos trigger a taxonomy review, not a force fit. | M, E | [Fit analysis](../fit-analysis.md) |
| TX-5 | The full scope is every repo in `Open-MBEE`, forks included, minus an explicit exclude list. In R1 the registry is a pilot of 24 to 36 real repos, and every other public repo is on the exclude list with a reason *(updated: WP0 "pilot"; WP4 D-3; `data/exclude.yaml`)*. Every exclusion is visible, with its reason. Only governors may exclude. | M | Inventory diff: org repos − registry = exclude list exactly |

**Draft starting point (from the Slack post), now decided:** type ∈ {tool, media, research} × lifecycle ∈
{active development, maintained, exploratory, archived}. *(updated: WP0 A2, A4; WP1 D-2)* The types are now tool,
media, research and governance; the stages are Sandbox, Incubating, Graduated and Archived; 14 kinds are defined and
2 omitted with reasons, in `data/taxonomy/kinds.yaml`. `repo-registry` itself is governance/sandbox (X-9).

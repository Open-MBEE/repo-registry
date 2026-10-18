# WP1 — Amendment 2: adopt the CNCF and OpenSSF lifecycle stages

Raised during the WP1 acceptance, after amendment 1 (approval 3c72b7d). It needs a new approval: mzargham's
`git merge --no-ff` of branch `amend-2` into `main`. The evidence is [lifecycle-stage-map.md](../docs/lifecycle-stage-map.md).
Records are typed by the agent (Claude). The decisions are mzargham's.

## Decision records

- **Supervisor (mzargham, typed by agent):** "we should probably adopt their model directly for stages rather than roll
  our own"
- **Question:** Adopt the CNCF and OpenSSF stages (Sandbox, Incubating, Graduated, Archived) as our lifecycle, through
  an amendment and a rework of the WP1 delivery?
- **Answer (mzargham, typed by agent):** "adopt theirs and refactor ours as needed but don't do so blindly. make sure to
  pull the relevant resources and do the map rigorously not from memory. i am agreeing to use the established precedent
  but then we actually need to use it, not just hand wave at it"
- **Agent's work:** pulled CNCF-LC (commit d815451), CNCF-AR, OSSF-LC (commit d019efe) and OSSF-SB, and wrote the map
  from their text. The findings changed the earlier sketch: stages are maturity signals, not versions. The 1.0.0 seam
  is Sandbox → Incubating (semantic versioning, plus CNCF's "more stable, versioned APIs" for Incubation). Graduated
  needs adoption and governance evidence, so the maintainers assign it.
- **Question:** tool/sandbox now holds tools with no release (low before) and 0.x tools (medium before). Which tier?
- **Answer (mzargham, typed by agent):** "Low"
- **Question:** tool/incubating holds every tool at 1.0 or later (high before). Which tier?
- **Answer (mzargham, typed by agent):** "Medium"

## What changes

- **A4 (WP0 and WP1).** The lifecycle is Sandbox, Incubating, Graduated, Archived, adopted from CNCF and OpenSSF. It
  replaces experimental, active development, maintained and archived, and the `unreleased` departure.
  - The 1.0.0 seam is Sandbox → Incubating.
  - Graduated is assigned only, never recommended.
  - Maintenance duties attach to stages as policies (WP2, following the OpenSSF baseline by stage).
  - Tiers: tool/graduated high, tool/incubating medium, tool/sandbox low, archived none, governance high.
  - repo-registry is governance/sandbox, and the org's administration is governance/graduated.
  - Updated: WP0 (citation of the stages, the governance kinds, the tier descriptions, the G1 "highlighted" wording),
    WP1 (Direction, D-2, R-3, R-6, R-9) and README (tier list and index page).

## Agent's defaults (for approval as one item)

- media: live media is recommended Incubating (medium, as live media was before). media/sandbox and media/graduated
  are assigned only. media/graduated maps to medium, because media tops out at medium.
- research: live research is recommended Sandbox (low). research/incubating and research/graduated are assigned only,
  and every research kind maps to low (research stays low-friction).
- governance/incubating is omitted (only two things have the governance type).
- Highlighted repos (WP0 G1) are those that are incubating or graduated.

## Open decisions

None. Every item was resolved through the decision loop: 4 decided (adopt the stages, the tool/sandbox tier, the
tool/incubating tier, the Agent's defaults), 0 deferred.

- **OD-A2-1 (Agent's defaults), answer (mzargham, typed by agent):** "Approve all"

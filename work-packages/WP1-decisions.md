# WP1 — Decision records

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's.

## Breakdown (work-breakdown, before WP1 was scoped)

- **Question:** OK to proceed with the WP1–WP8 breakdown, starting by scoping WP1 (Kinds and tiers)?
- **Answer (mzargham, typed by agent):** "OK, scope WP1"

## Release maturity and semantic versioning *(raised by supervisor)*

- **Supervisor (mzargham, typed by agent):** "i want to provide a more detailed recommendation to the design. we're
  allowing 0.X releases to stay in medium tier and escalating to high at 1.0.0. it also occurred to me that we need to
  include semantic versioning as a policy required for medium and high because we're going to need it as a dependency
  to make other policies checkable."
- **Follow-up:** WP0's approved R-17 says each kind sits in exactly one tier. How should the version escalation work?
- **Answer (mzargham, typed by agent):** "we need to split the kinds but experimental exists to cover this"
- **Outcome:** Tools split into an experimental tool kind (below `1.0.0`, medium) and a core tool kind (`1.0.0` or
  later, high). WP0 R-17 is unchanged. Added a direction item and R-9. Semantic versioning as a policy for medium and
  high is carried to WP2.

## OD1 — How far WP1's classification goes

- **Question:** Should WP1 also write each repo's recommended kind into a first draft of the canonical kind list, or
  stop at defining the kinds and rules?
- **Answer (mzargham, typed by agent):** "also draft the kinds list but be clear that its provisional and that
  authority to initialize the kinds list belongs with the maintainers. this will be one of many chicken and egg
  problems where our approach needs data, we should always draft provisional data but clearly demarcate it as
  provision until we pass the maintainer acceptance milestone associated with that data"
- **Outcome:** Added D-5 (the provisional kind list), R-10 (a checkable provisional mark), a direction item on
  provisional data, and a non-goal. Default: the provisional-data rule also goes into AGENTS.md.

## OD2 — Private repos in the committed snapshot

- **Answer (mzargham, typed by agent):** "Leave out entirely"
- **Outcome:** Private repos are left out of the snapshot and the provisional kind list, named nowhere, and recorded
  only as a count. Added to D-1, R-1 and the non-goals.

## OD3 — Agent's defaults

- **Answer (mzargham, typed by agent):** "a tool can be in the low or archived status without semver. we don't assume
  media or research needs semver."
- **Outcome:** Default 9 (a non-semver tool is unclassified) was replaced. R-9 now applies the `1.0.0` rule only to
  semver tools, lets a tool without semver sit in the low tier or be archived, and doesn't assume semver for media or
  research. Follow-up asked about the other eight defaults.

### Follow-up — The other eight defaults

- **Answer (mzargham, typed by agent):** "i dont think we need at most 8 kinds. right now i think we're trending toward
  kinds as the cross product of the sets type = (tool, media, research) and a lifecycle model that covers archived as
  terminal state (experimental, active-development, maintained, archived). that's not a final decision, but roughly
  matches the intuition in the slack message. it gives us 12 kinds and should give is an interpretable mapping to
  tiered policy sets. actively developed and maintained tools map to high. this repo would fall in high and controls
  over the organization itself need to be high. anything archived is read only so it should be inert. everything else
  would map to low or medium. ideally we can keep it that sparse. obviously in the future the taxonomy could change but
  this keeps everything pretty simple for a human to follow. jumping the 0. to 1.0 semver is a seam aligned with going
  from experimental to active development."
- **Outcome:** The 8-kind cap was dropped. Added direction items: type × lifecycle (12 kinds) as the starting point,
  and the fixed parts of the kind → tier map. The `0.x` → `1.0.0` seam is now experimental → active development
  (replacing "experimental tool → core tool"). R-3, R-6, R-9 and D-2 were updated. Controls over the org are high,
  carried to WP3. The other seven defaults are still to be confirmed.

## repo-registry's kind and the WP0 friction lifecycle

- **Question:** "This repo would fall in high" meets the approved WP0, which keeps repo-registry low-friction in R1.
  What do you mean for repo-registry's kind?
- **Answer (mzargham, typed by agent):** "now you are confusing high tier with a kind. please don't mess up our
  concepts. itll get really messy in the code if you don't preserve the factoring we created to reduce dimensionality
  and make policy making legible"
- **Outcome:** The agent had conflated a kind with a tier. The wording was fixed: repo-registry's kind maps to the high
  tier. Added a direction item (repo → kind → tier → policies, nothing skips a link) and a check in R-6 that no repo is
  given a tier directly. The question about friction was not pursued. Under the provisional-data rule, repo-registry's
  kind stays provisional until the maintainers approve the kind list, so WP0's R1 friction lifecycle stands unchanged.

## Remaining defaults

- **Answer (mzargham, typed by agent):** "Approve all"
- **Outcome:** All defaults approved. The provisional-data rule was added to AGENTS.md ("How work proceeds", item 3)
  on the scope branch, approved by the same merge.

## Summary

The open list is empty: 8 decided, 0 deferred, 2 raised.

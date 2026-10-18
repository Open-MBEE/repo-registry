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

# Acceptance review (WP1-review.md)

## G-3 — R-4 not met (plain language)

- **Answer (mzargham, typed by agent):** "Fix before acceptance"

## G-1 — tiers.yaml names a policy (semantic versioning)

- **Answer (mzargham, typed by agent):** "fix before acceptance. semantic versioning policies only apply to tools. this
  brings into question whether policies can actually be fully specified by tier or whether we need to know whether its
  research, media or tool in order to uniquely determine which policies apply"
- **Follow-up:** Whether policies follow from the tier alone, or from the tier plus the type, changes WP0's approved
  chain. Where should that be decided?
- **Answer (mzargham, typed by agent):** "the decision i want is that policies can be attached to type, lifecycle or
  tier (even if tier is derived from type x lifecycle) each of this provides a well defined scope that reduces to this
  policy applies if predicate that is human interpretable. i am open to some minor redesign to support this change.
  keeping the top level goal in tact of plan language explainability a minimizing dimensionality of the policy making.
  its still a small collection of policies, and simple low dimensional rules about which policies are in effect. this
  is a dimensionality reduction that connects repos (many) to policies (few) according to human interpretable,
  deterministically replayable rules. we're essentially doing categorical feature engineering so we can get from repos
  to 3 categorical attributes, then determine which polices are in effect from just those attributes."
- **Outcome:** Fix: remove the policy statement from tiers.yaml. The chain decision changes the approved WP0 and WP1, so
  it goes to an amendment (scope-of-work section 6), approved by a new merge.

## G-2 — repo-registry's own kind isn't in the data

- **Answer (mzargham, typed by agent):** "let's create a type governance and the only two things governed as governance
  (as opposed to tool, research or media) are this repo and the administration of the github org itself. this one is
  experimental but the governance of the org itself is in maintained (on the lifecycle axis) and anything with
  governance type is tier high. best practices say the governance level controls need to be as strict or stricter than
  anything they govern"
- **Outcome:** Fix, after the amendment: a governance type, with repo-registry as governance/experimental and the
  org's administration as governance/maintained, every governance kind mapping to high. This changes WP1's type list,
  so it goes into the same amendment.

## G-4 — Remaining observations and out-of-scope files

- **Answer (mzargham, typed by agent):** "Accept as is"

## 0.x tools in active development *(raised by supervisor)*

- **Supervisor (mzargham, typed by agent):** "active development should include at least opensysml and sysml-toolkit"
- **Follow-up:** OpenSysML and sysml-toolkit are 0.x, tool/active-development maps to high, and the approved seam says
  0.x stays medium. How should these fit?
- **Answer (mzargham, typed by agent):** "governor assigns them but activity goes into guidance for how to set them. and
  now i am realizing i may have contradicted my own rule since both of the repos i named as active development are pre
  1.0 making them experimental. which is probably good because i don't want to stop the rapid development occurring
  right now but we do want those repos to cross a line into 1.0 state at which point we'll need to tighten controls"
- **Outcome (agent's reading, stated to the supervisor):** both stay tool/experimental. Recommendations, activity
  included, are guidance for governors, who assign. At 1.0.0 they move to active development and their controls
  tighten. Recorded as amendment A3.

# Amendment 1 to WP1 (with WP0 amendment 1)

The WP1 scope is approved (merge 3bb8ee8). These changes need a new approval by merge.

- **A1.** Semantic versioning is a policy for tools (it was "for medium and high"). Policies can attach to type,
  lifecycle or tier.
- **A2.** The governance type: repo-registry is governance/experimental, the org's administration is
  governance/maintained, every governance kind maps to high, and the other governance kinds are omitted with a reason.
  R-3 now allows omitted kinds, with a reason. R-6 and D-2 were updated.
- **A3.** Recommendations are guidance and governors assign. OpenSysML and sysml-toolkit stay experimental until 1.0.0.

## Third review pass — R-4's stopping point (raised by the agent, a level up)

- **Question:** R-4 is checked by a cold read, and a model stand-in finds a new, smaller layer each pass. What should
  count as meeting R-4 for WP1?
- **Answer (mzargham, typed by agent):** "Fix 1-5, then stop"
- **Outcome:** Fix the third pass's five items, accept the two minor ones (version numbers, "controls"), and treat
  stand-in reads as advisory. The real cold read by a person happens at the WP8 demonstrations.

## Maintained means active upkeep *(raised by supervisor, during the fixes)*

- **Supervisor (mzargham, typed by agent):** "maintenance is active not passive"
- **Supervisor (mzargham, typed by agent):** "repos being maintained need to be aware of their dependencies. as well as
  CVEs and other ongoing work to keep their stable software safe and reliable"
- **Outcome:** The meaning of maintained now says it is actively looked after: tracking dependencies, watching for
  publicly reported security flaws (CVEs) and fixing them. Recommendation rules (agent's inner-loop detail): active
  development means changes in the last 3 months, and maintained means changes in the last 12 months but not the last
  3. A 1.0-or-later tool, or media, with no changes in a year is unclassified, with the reason "isn't being maintained:
  archive it, or a maintainer says who looks after it". Carried to WP2: policies attached to the maintained lifecycle
  for dependency tracking and vulnerability (CVE) handling (WP0 A1 allows lifecycle-attached policies).

## Lifecycle is a category, not compliance *(raised by supervisor)*

- **Supervisor (mzargham, typed by agent):** "you also may be confusing the lifecycle category with compliance to
  controls. these repos wouldn't be in compliance with controls that don't exist"
- **Outcome:** The agent had made "no changes in a year" leave a repo unclassified as "not maintained". That judged
  compliance through the kind. Reverted: lifecycle recommendations use the 12-month split again (changes in the last
  year means active development, otherwise maintained), and the "not maintained" reason is gone. The maintained
  meaning now states the category and its expected upkeep, and says that whether the upkeep happens is checked by the
  maintained-lifecycle policies (WP2), not by the kind.

# WP3 — Decision records

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's.

## Scope emphasis *(raised by supervisor while drafting)*

- **Supervisor (mzargham, typed by agent):** "to be clear this is governance of the github org and probably merits
  github documentation exploration"
- **Outcome:** D-1 is an explicit exploration of GitHub's documentation on organization governance: roles, teams,
  outside collaborators, installed GitHub Apps, security-relevant org settings and the audit log, each with its
  powers, how to read it, and a docs link. G1 and R-2 were updated to match.

## OD1 — Usernames and privacy

- **Answer (mzargham, typed by agent):** "public only for now but flag the gap because we should be mandating
  governance-role holders are named. per the accountability clause. we shouldn't dox people now because that rule
  isn't ratified and people should have the option to step down to not be doxed if that is their preference"
- **Outcome:** Only holders with public org membership are named, and concealed holders are counted (R-8). D-2 adds a
  proposed `governance-roles-named` policy, which requires public membership for governance-role holders. It is
  provisional until ratified, and people may step down rather than be named.

## OD2 — Who drafts the first maintainer list

- **Supervisor (mzargham, typed by agent):** "tell me who is the list of public owners and admins and i will propose
  adjustments"
- **Agent's read-only lookup:** 18 org owners. 2 have public membership (`ablack-jpl`, `aftimg`), and 16 are
  concealed (counted only). The org has 5 public members. mzargham is a member, not an owner, with public membership.
- **Supervisor (mzargham, typed by agent):** "i can get the permissions if i need them i am admin on several of our
  other platforms and have been doing a lot of interfacing on behalf of openmbee including with numfocus (our fiscal
  sponsor). you can put me in there, and i think at minumum you should include robert karban as he is a founder and
  public named as an admin elsewhere. its provisional so if you include robert and myself its fine for now"
- **Supervisor (mzargham, typed by agent):** "actually you should include jason han. also named publicly as a
  maintainer elsewhere 5 ins a good number. otherwise we can note there are others with various admin powers. we
  don't reveal any additional names except the people have noted are already publicly known. ideally we establish a
  policy which can be used to determine what powers maintainers get and how we determine who the maintainers are. one
  reason for including jason is that he's the release authority for opensysml and were currently going through a
  credentialling process to ensure he can fulfill that role"
- **Agent's account lookup:** Robert Karban is `rkarban` (GitHub full-name search). Jason Han is `HuiJun` (public
  profile name "Jason Han"; author of 20 OpenSysML releases). Neither has public Open-MBEE membership.
- **Outcome:**
  - Provisional list: `mzargham`, `rkarban`, `HuiJun`. Target size five.
  - Others with admin powers are counted, not named.
  - Concealed memberships show yellow in the match check.
  - D-5 (maintainer policy) and G4 were added.

## OD3 — The accounts and the Agent's defaults

- **Answer (mzargham, typed by agent):** "Approve both"
- **Outcome:** `rkarban` (Robert Karban) and `HuiJun` (Jason Han) are confirmed, and the defaults stand. R-8 was
  restated: names appear only for public members or the people the supervisor named as publicly known, and no
  concealed role is revealed.

## Summary

The open list is empty: 3 decided, 0 deferred, 1 raised.

## Provenance of the list *(raised by supervisor, before approval)*

- **Supervisor (mzargham, typed by agent):** "i have not personally encountered aaron black and i am not sure if he is
  still active may be worth flagging the hole list as provisional on the grounds that its sourced from a mix github
  current public data and my own experiences working as part of the orgs current leadership"
- **Outcome:** A direction item now states the list's provenance and that it is provisional as a whole, and names
  `ablack-jpl`'s activity as unverified. New agent default: D-1 records the last public activity in the org of
  publicly named governance-role holders, as a hint only.
- **Question:** Approve the new default (last public activity, recorded as a hint)?
- **Answer (mzargham, typed by agent):** "Approve"

# During execution

## Chris Delp added *(raised by supervisor)*

- **Supervisor (mzargham, typed by agent):** "you lost chris delp from your list. he was in your original pull and he
  was the cofounder with robert"
- **Agent's check:** `aftimg` is Chris Delp (public profile name "Chris Delp", linking his Caltech educator page). He
  is one of the two org owners with public membership. The agent had not checked the public owners' profile names.
- **Outcome:** `aftimg` was added to `data/maintainers.yaml` and the proposed CODEOWNERS (4 of the target 5).

## Owners are a subset of the maintainers (agent's reading, flagged for acceptance)

- OpenSSF baseline TI-3 asks for two or three org owners. The supervisor set a target of five maintainers. Both hold if
  every org owner is a named maintainer but not every maintainer is an owner. The match check and the maintainer
  policy use that reading. Flagged for the supervisor at the acceptance review.

## Cross-check of the maintainer policy *(raised by supervisor)*

- **Supervisor (mzargham, typed by agent):** "make sure that we cross check our maintainer policies and priviledges
  with the openSSF framework backbone and other sources were using as out references"
- **Outcome:** `docs/maintainer-policy.md` ends with a cross-check of every provision against OpenSSF (lifecycle at
  d019efe, baseline at 098faba), CNCF (lifecycle at d815451, graduation criteria at 6119a69), CISA, NIST SP 800-53 and
  ISO/IEC/IEEE 12207 clauses.

# Acceptance review (WP3-review.md)

## G-2 — Owners are a subset of the maintainers

- **Answer (mzargham, typed by agent):** "owners should be a subset of maintainer. they are the root most authority we
  expect 2 to 3 owners and maintainers can be more. we are able to have a larger number of maintainers because we are
  actually maintaining quite a few pieces of software under the openmbee umbrella but we need to make sure the
  maintainers power is checked by the owners and the owners set is appropriately small"
- **Outcome:** The reading stands. Fix: the maintainer policy now says owners check the maintainers' powers (an owner
  approves adding a maintainer or changing their powers, and the owners run the annual review), and that five
  maintainers is a starting point that can grow with the number of maintained tools.

## G-1 — R-7 not met (five plain-language items)

- **Answer (mzargham, typed by agent):** "Fix all five"

## G-3 — Observations

- **Answer (mzargham, typed by agent):** "accept as is but don't make policies that require the use of features
  openmbee cannot use. can always flag it for future if we get enough funding to upgrade to an enterprise plan"
- **Agent's check:** Open-MBEE is on GitHub's Free plan (`GET /orgs/Open-MBEE` returns plan.name `free`). GitHub's
  plans page says Free for organizations gives public repositories the full feature set, and lists code owners,
  protected branches and required reviewers as paid features for private repositories only. Not confirmed for Free:
  immutable releases, and rulesets (the about-rulesets page names Team and Enterprise).
- **Outcome:** Accepted as is. New, applied to every policy: no policy requires a feature OpenMBEE's plan doesn't
  have.
  - It is a meta-rule: each policy declares the plans it works on, which must include the org's plan, recorded in
    `data/sources/github-plan.yaml`.
  - Enterprise-only or unconfirmed features go in `data/policies/_future.yaml`, flagged for a future upgrade.
  - `release-integrity` no longer checks immutable releases.
  - `history-protection` and `change-review` accept classic branch protection (confirmed on Free) or rulesets.

### Follow-up — immutable releases and rulesets *(supervisor)*

- **Supervisor (mzargham, typed by agent):** "we need immutable releases and rulesets so let's keep those in our
  policies but flag a need for further research. i don't think those are paid features because they are needed in
  other oss"
- **Outcome:** Both are kept. `release-integrity` checks immutable releases again. Rulesets are the preferred
  mechanism in `history-protection` and `change-review`, and classic branch protection is still accepted. Each such
  policy names the feature under `github.needs_research`, and a meta-rule requires it to be listed in
  `_future.yaml`'s `needs_research` section, with the open question. Enterprise-only features stay under `features`,
  and no policy requires them.

### Follow-up — immutable releases and rulesets confirmed *(supervisor)*

- **Supervisor (mzargham, typed by agent):** "i have confirmed independently that github supports immutable releases
  and rulesets in the openmbee org"
- **Outcome:** Both are recorded as confirmed for the org in `data/sources/github-plan.yaml`. The `needs_research`
  flags and the "being confirmed" notes in the SOPs are gone. Rulesets are the recommended mechanism, and a classic
  branch-protection rule that does the same job still passes. `_future.yaml` keeps only Enterprise-only features.

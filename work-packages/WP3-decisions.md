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

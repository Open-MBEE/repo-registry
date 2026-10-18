# WP3 — Summary for the supervisor

> Everything here is **PROVISIONAL**. The org policies wait for maintainer approval 2, and the named maintainers and
> the maintainer policy wait for approval 5 (WP0). This summary meets WP3's Definition of good enough.

## Who holds power over the GitHub org (D-1)

[org-governance-review.md](../docs/org-governance-review.md) describes, from GitHub's documentation, every way power
over the org is held:
- the owner role, and the narrower org roles: security manager, CI/CD admin, moderator, App Manager, and
  all-repository roles;
- repository roles granted through teams;
- team maintainers;
- outside collaborators;
- installed apps;
- the security-relevant settings.

Each comes with how to read it and the permission needed. The read-only snapshot shows:

- **18 owners,** far above OpenSSF's 2 to 3. Only 2 have public membership: `aftimg` (Chris Delp) and `ablack-jpl`.
- **Owner-only information is yellow.** That covers the two-factor requirement, the base permission, outside
  collaborators, installed apps, holders of the narrower roles, security configurations and org rulesets. With
  owner-level permissions, they would become real values.
- **Members can create public repositories, change visibility and invite outside collaborators.** That is recorded as
  low friction, not judged.
- **Activity hints:** `ablack-jpl`'s last public commit in the org was 2017-09-25. For Robert Karban, none was found.

## Org policies (D-2)

They apply only to the org's administration (governance/graduated, high):

| Policy | Asks | Status today |
|---|---|---|
| org-two-factor | two-factor authentication for everyone | yellow (owner-only setting) |
| org-few-owners | 2 or 3 owners | red (18) |
| org-base-permission | read-only base permission | yellow (owner-only setting) |
| maintainers-match | the maintainers are this repo's code owners, and every owner is a maintainer | red (see below) |
| governance-roles-named | governance-role holders make their membership public | red (16 concealed owners) |

Two-factor authentication (OpenSSF SB-2) has moved from departed to adopted.

## Named maintainers and the match check (D-3, D-4)

- **Provisional list:** `aftimg` (Chris Delp), `mzargham` (Michael Zargham), `rkarban` (Robert Karban), `HuiJun`
  (Jason Han, release authority for OpenSysML). That is 4, against a starting target of 5 that can grow. Its provenance is public GitHub data plus
  your experience, so it is provisional as a whole.
- **Match result (overall red):**
  - *Green:* Chris is an owner and listed. You're a maintainer without the owner role, which is fine.
  - *Yellow:* Robert and Jason, whose memberships aren't public, so their role isn't shown; the 16 concealed owners, as
    a total; and 4 of 5 named.
  - *Red:* `ablack-jpl` is a public owner who isn't on the list.

## Maintainer policy (D-5)

[maintainer-policy.md](../docs/maintainer-policy.md) covers:
- who maintainers are;
- adding them, stepping down, and emeritus;
- inactivity, which leads to a question, never automatic removal;
- an annual review;
- least-privilege powers;
- named, credentialed release authority;
- named security response.

Each provision is cross-checked against OpenSSF (lifecycle and baseline), CNCF's graduation criteria, CISA, NIST SP
800-53 and ISO/IEC/IEEE 12207 clauses.

## For your attention

1. **Owners are a subset of the maintainers (confirmed by you).** Owners are the root authority, 2 to 3 of them.
   Maintainers can be more, and the owners check the maintainers' powers.
2. **Privacy holds.** No concealed member is named anywhere (the live check covers all 71 concealed members). The
   match check never reveals the role of a listed person whose membership isn't public. A test shows its output
   doesn't change either way.

## Plans and features

OpenMBEE is on GitHub Free. Every policy works on it. Immutable releases and rulesets are confirmed available in the
Open-MBEE org (you checked independently), and recorded in `data/sources/github-plan.yaml`.
Enterprise-only features are listed there for a future upgrade, and no policy requires them.

## Checks

`python3 -m unittest discover -s tests` runs 43 tests, all OK (2 expected failures). `python3
scripts/privacy_check.py` is the live, read-only privacy check.

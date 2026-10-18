# Few owners

> **PROVISIONAL** until the maintainers approve the policies. Policy `org-few-owners` (`data/policies/org-few-owners.yaml`).

The organization has two or three owners, no more. Owners can do anything to every repository and to the organization itself, so the role is kept small.

**Applies to:** the administration of the Open-MBEE GitHub organization (kind governance/graduated). See [policy-applicability.md](../policy-applicability.md).

## Set up

1. List the owners: organization People page, filtered by role Owner.
2. Decide, under the maintainer policy, which two or three people keep the owner role.
3. Give everyone else the power they actually need instead, for example admin on specific repositories through a team, or the security manager role (a GitHub organization role that can manage security settings and alerts on every repository without owning the organization; see https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization).
4. An owner changes the others' role to Member.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **owner-count**: `GET /orgs/{org}/members?role=admin -> between 2 and 3 members` (needs organization member (Members: read))

## Attested checks

None.

## Why

- CISA: none
- NIST SP 800-53: AC-6(5)
- OpenSSF security baseline: TI-3

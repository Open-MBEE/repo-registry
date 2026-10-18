# Least-privilege base permission

> **PROVISIONAL** until the maintainers approve the policies. Policy `org-base-permission` (`data/policies/org-base-permission.yaml`).

Members of the organization get only read access to its repositories by default. More access is granted per repository, through teams.

**Applies to:** governance at graduated: the administration of the Open-MBEE GitHub organization, and repo-registry once it is accepted as the canonical source. See [policy-applicability.md](../policy-applicability.md).

## Set up

1. First, make sure everyone who needs to write keeps that access: give each repository's contributors write (or
   admin) through a team on that repository. Otherwise, lowering the base permission cuts them off.
2. Then an organization owner opens Settings, then Member privileges.
3. Set Base permissions to Read (or No permission).

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **base-permission-read**: `GET /orgs/{org} -> default_repository_permission in (read, none) (returned only to owners: yellow otherwise)` (needs organization owner (Administration: read))

## Attested checks

None.

## Why

- CISA: none
- NIST SP 800-53: AC-6
- OpenSSF security baseline: TI-3

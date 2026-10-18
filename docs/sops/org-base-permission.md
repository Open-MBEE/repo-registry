# Least-privilege base permission

> **PROVISIONAL** until the maintainers approve the policies. Policy `org-base-permission` (`data/policies/org-base-permission.yaml`).

Members of the organization get only read access to its repositories by default. More access is granted per repository, through teams.

**Applies to:** the administration of the Open-MBEE GitHub organization (kind governance/graduated). See [policy-applicability.md](../policy-applicability.md).

## Set up

1. An organization owner opens Settings, then Member privileges.
2. Set Base permissions to Read (or No permission).
3. Grant write or admin to the people who need it through teams on the repositories they work on.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **base-permission-read**: `GET /orgs/{org} -> default_repository_permission in (read, none) (returned only to owners: yellow otherwise)` (needs organization owner (Administration: read))

## Attested checks

None.

## Why

- CISA: none
- NIST SP 800-53: AC-6
- OpenSSF security baseline: TI-3

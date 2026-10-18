# Governance roles are held openly

> **PROVISIONAL** until the maintainers approve the policies. Policy `governance-roles-named` (`data/policies/governance-roles-named.yaml`).

Everyone who holds governance power over the organization makes their organization membership public, so that who governs OpenMBEE is visible. Until this policy is ratified, nobody is named against their choice, and anyone may step down instead.

**Applies to:** the administration of the Open-MBEE GitHub organization (kind governance/graduated). See [policy-applicability.md](../policy-applicability.md).

## Set up

1. Each owner, and each named maintainer, opens the organization's People page, finds their own name, and sets their membership to Public.
2. Anyone who prefers not to be named publicly can step down from the governance role instead. That is a choice, not a failure.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **owners-public**: `GET /orgs/{org}/members?role=admin compared with GET /orgs/{org}/public_members -> no owner has concealed membership (reported as a count only)` (needs organization member (Members: read))

## Attested checks

None.

## Why

- CISA: CISA-C4-COMMUNITY
- NIST SP 800-53: none

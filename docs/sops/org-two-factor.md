# Two-factor authentication for everyone

> **PROVISIONAL** until the maintainers approve the policies. Policy `org-two-factor` (`data/policies/org-two-factor.yaml`).

The organization requires two-factor authentication for every member and outside collaborator.

**Applies to:** the administration of the Open-MBEE GitHub organization (kind governance/graduated). See [policy-applicability.md](../policy-applicability.md).

## Set up

1. An organization owner opens the organization's Settings, then Authentication security.
2. Turn on Require two-factor authentication for everyone in the organization, after steps 3 and 4.
3. Before turning it on, find who hasn't set it up yet: on the organization's People page (and the Outside
   collaborators page), filter by "2FA" to list those without two-factor authentication. Owners can see this list.
4. Ask each of them to turn it on (on GitHub: their profile picture, then Settings, then Password and authentication),
   and give them a date. When the requirement starts, GitHub removes outside collaborators who still haven't, and
   members without it lose access until they set it up.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **two-factor-required**: `GET /orgs/{org} -> two_factor_requirement_enabled == true (returned only to owners: yellow otherwise)` (needs organization owner (Administration: read))

## Attested checks

None.

## Why

- CISA: none
- NIST SP 800-53: IA-2(1)
- OpenSSF security baseline: SB-2

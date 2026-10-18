# Block secrets from being pushed

> **PROVISIONAL** until the maintainers approve the policies. Policy `secret-protection` (`data/policies/secret-protection.yaml`).

Tools from version 1.0, and the registry, turn on push protection, so that GitHub blocks a push that contains a password, key or token.

## Set up

1. Go to the repository's Settings, then Advanced Security (or Code security).
2. Turn on Secret Protection, if it is offered, and Push protection.
3. Push protection then blocks any push that contains a detected password, key or token.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **push-protection-on**: `GET /repos/{owner}/{repo} -> security_and_analysis.secret_scanning_push_protection.status == enabled (the block is absent without admin read: yellow, not off)` (needs Administration: read)

## Attested checks

None.

## Why

- CISA: CISA-P-SECRET-DETECT, CISA-P-PREPUB-REVIEW (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: IA-5(7) (see `data/sources/nist-800-53.yaml`)
- OpenSSF security baseline: TI-2 (see `data/sources/openssf-security-baseline.yaml`)

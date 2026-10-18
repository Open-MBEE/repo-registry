# Know and watch your dependencies

> **PROVISIONAL** until the maintainers approve the policies. Policy `dependency-management` (`data/policies/dependency-management.yaml`).

Tools from version 1.0, and the registry, turn on Dependabot alerts and publish a short dependency policy: how new dependencies are chosen and how they are kept up to date. Services the project provides pin their direct dependencies.

**Applies to:** tool at incubating, tool at graduated, governance at incubating (nothing yet), governance at graduated (the administration of the Open-MBEE GitHub organization, and repo-registry once it is accepted as the canonical source). Your repository's kind is in [registry.yaml](../../registry.yaml); the stages are explained in [lifecycle-stage-map.md](../lifecycle-stage-map.md), and the full table is in [policy-applicability.md](../policy-applicability.md).

## Set up

1. Go to Settings, then Advanced Security (or Code security), and turn on Dependabot alerts.
2. Write a short dependency policy, in `CONTRIBUTING.md` or its own file: how new dependencies are chosen and how they are kept up to date.
3. If the project provides a service, pin its direct dependencies: name an exact version for each (for example 2.4.1, not 2.x).
4. Record the attestations below.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **dependabot-alerts-on**: `GET /repos/{owner}/{repo}/vulnerability-alerts -> 204 (404 means off only when the caller has admin read; otherwise yellow)` (needs Administration: read)

## Attested checks

- **dependency-policy**: A dependency policy is published (in CONTRIBUTING or its own file) and followed.
- **service-pins**: If the project provides an internet or infrastructure service, its direct dependencies are pinned: each one names an exact version (for example 2.4.1, not 2.x).

How to attest: add a block like this to the end of your `README.md`, one per attested check, and update it with each
release. An attestation counts only if a code owner of the repository committed it, and it is out of date once it
is older than the repository's latest release.

```markdown
<!-- repo-registry attestation
policy: dependency-management
check: dependency-policy
attested-by: @your-github-username
date: YYYY-MM-DD
release: vX.Y.Z (or none)
-->
```


## Why

- CISA: CISA-P-DEP-SCAN, CISA-P-CI-PATCH-AUTO (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: RA-5, CM-8 (see `data/sources/nist-800-53.yaml`)
- OpenSSF security baseline: TI-5, TI-6 (see `data/sources/openssf-security-baseline.yaml`)
- ISO/IEC/IEEE 12207:2026 clause 6.4.13 (cited by reference)

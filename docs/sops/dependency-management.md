# Know and watch your dependencies

> **PROVISIONAL** until the maintainers approve the policies. Policy `dependency-management` (`data/policies/dependency-management.yaml`).

Tools from version 1.0, and the registry, turn on Dependabot alerts and publish a short dependency policy: how new dependencies are chosen and how they are kept up to date. Services the project provides pin their direct dependencies.

## Set up

1. Go to Settings, then Advanced Security (or Code security), and turn on Dependabot alerts.
2. Write a short dependency policy, in `CONTRIBUTING.md` or its own file: how new dependencies are chosen and how they are kept up to date.
3. If the project provides a service, pin its direct dependencies to exact versions.
4. Record the attestations below.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **dependabot-alerts-on**: `GET /repos/{owner}/{repo}/vulnerability-alerts -> 204 (404 means off only when the caller has admin read; otherwise yellow)` (needs Administration: read)

## Attested checks

- **dependency-policy**: A dependency policy is published (in CONTRIBUTING or its own file) and followed.
- **service-pins**: If the project provides an internet or infrastructure service, its direct dependencies are pinned.

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

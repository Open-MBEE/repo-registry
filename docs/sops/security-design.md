# Documented security design

> **PROVISIONAL** until the maintainers approve the policies. Policy `security-design` (`data/policies/security-design.yaml`).

High-tier repositories keep a short design document that describes the security controls of what they build, and keep it current.

## Set up

1. Write a short design document (for example `docs/design.md`) that describes the security controls of what the repository builds.
2. Update it whenever those controls change.
3. Record the attestation below.

## Automated checks

None. This policy is checked by attestation only.

## Attested checks

- **design-current**: A design document describes the security controls and is updated when they change.

How to attest: add a block like this to the end of your `README.md`, one per attested check, and update it with each
release. An attestation counts only if a code owner of the repository committed it, and it is out of date once it
is older than the repository's latest release.

```markdown
<!-- repo-registry attestation
policy: security-design
check: design-current
attested-by: @your-github-username
date: YYYY-MM-DD
release: vX.Y.Z (or none)
-->
```


## Why

- CISA: CISA-C4-CONFIG (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: SA-8, SA-17, PL-8 (see `data/sources/nist-800-53.yaml`)
- OpenSSF security baseline: TG-1 (see `data/sources/openssf-security-baseline.yaml`)
- ISO/IEC/IEEE 12207:2026 clause 6.4.4 (cited by reference)

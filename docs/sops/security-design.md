# Documented security design

> **PROVISIONAL** until the maintainers approve the policies. Policy `security-design` (`data/policies/security-design.yaml`).

High-tier repositories keep a short design document that describes the security controls of what they build, and keep it current.

**Applies to:** tool at graduated, governance at graduated (the administration of the Open-MBEE GitHub organization, and repo-registry once it is accepted as the canonical source). Your repository's type and stage are in [registry.yaml](../../registry.yaml); the stages are explained in [lifecycle-stage-map.md](../lifecycle-stage-map.md), and the full table is in [policy-applicability.md](../policy-applicability.md).

## Set up

1. Write a short design document (for example `docs/design.md`) that describes the security controls of what the repository builds: the measures that protect it and its users, such as who can sign in, how data is protected, and how input is checked.
2. Update it whenever those controls change.
3. Record the attestation below.

## Automated checks

None. This policy is checked by attestation only.

## Attested checks

- **design-current**: A design document describes the security controls (the measures that protect the software and its users, such as who can sign in, how data is protected, and how input is checked) and is updated when they change.

How to attest: add this entry to your repository's `ATTESTATIONS.yaml`, at its root, and renew it for each release
([attestations-format.md](../attestations-format.md)). An entry counts only if its `release` names the release being
checked (or `none` before the first release), and the last change to the file was committed by a code owner of the repository. Point to
the file from the README: "Attestations: see `ATTESTATIONS.yaml`."

```yaml
attestations:
  - policy: security-design
    check: design-current
    attested_by: your-github-username
    date: YYYY-MM-DD
    release: vX.Y.Z           # the release this is made for, or none if there is no release yet
```


## Why

- CISA: CISA-C4-CONFIG (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: SA-8, SA-17, PL-8 (see `data/sources/nist-800-53.yaml`)
- OpenSSF security baseline: TG-1 (see `data/sources/openssf-security-baseline.yaml`)
- ISO/IEC/IEEE 12207:2026 clause 6.4.4 (cited by reference)

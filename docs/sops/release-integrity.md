# Trustworthy releases

> **PROVISIONAL** until the maintainers approve the policies. Policy `release-integrity` (`data/policies/release-integrity.yaml`).

Graduated tools publish each release with a software bill of materials (SBOM), sign it, publish build provenance, and keep built executables out of the source repository.

**Applies to:** tool at graduated. Your repository's kind is in [registry.yaml](../../registry.yaml); the stages are explained in [lifecycle-stage-map.md](../lifecycle-stage-map.md), and the full table is in [policy-applicability.md](../policy-applicability.md).

## Set up

1. Build releases in CI (continuous integration: the automated build that runs on GitHub Actions). If you don't have a release workflow yet, start from GitHub's Actions guide for your language.
2. In that workflow, generate an SBOM (a software bill of materials: a list of everything the release contains, in SPDX or CycloneDX format), and attach it to each release.
3. Turn on Immutable releases (Settings, then General), so published releases can't be changed.
4. Sign release artifacts and publish their build record (provenance) with GitHub artifact attestations, built through a reusable workflow on GitHub-hosted runners. That combination meets SLSA Build Level 3. SLSA (Supply-chain Levels for Software Artifacts) is a standard for how far a build record can be trusted. See https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations
5. Keep built executables out of the source repository. Build them from source in CI.
6. Record the attestations below.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **sbom-attached**: `GET /repos/{owner}/{repo}/releases/latest -> assets include a file named like *.spdx.json, *.spdx, *.cdx.json or *bom*.json` (needs Contents: read)
- **release-immutable**: `GET /repos/{owner}/{repo}/releases/latest -> immutable == true` (needs Contents: read)

## Attested checks

- **signed-with-provenance**: Release artifacts are signed, and a build record (provenance) is published with them that meets SLSA Build Level 3: built by GitHub Actions on GitHub-hosted runners through a reusable workflow, with GitHub artifact attestations.
- **no-built-executables**: The source repository holds no built executables, except test fixtures that are documented as such.

How to attest: add a block like this to the end of your `README.md`, one per attested check, and update it with each
release. An attestation counts only if a code owner of the repository committed it, and it is out of date once it
is older than the repository's latest release.

```markdown
<!-- repo-registry attestation
policy: release-integrity
check: signed-with-provenance
attested-by: @your-github-username
date: YYYY-MM-DD
release: vX.Y.Z (or none)
-->
```


## Why

- CISA: CISA-P-SBOM-RELEASE, CISA-P-RELEASE-MARK (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: SR-4, SA-10(1), SA-10(6) (see `data/sources/nist-800-53.yaml`)
- OpenSSF security baseline: TG-5, TG-6, TG-7, TG-8 (see `data/sources/openssf-security-baseline.yaml`)

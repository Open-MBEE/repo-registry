# Version numbers that mean something

> **PROVISIONAL** until the maintainers approve the policies. Policy `semantic-versioning` (`data/policies/semantic-versioning.yaml`).

Tools from version 1.0 number their releases with semantic versioning, so that the version says whether an update is a fix, a feature or a breaking change. Graduated tools also say which releases get fixes, and for how long.

**Applies to:** tool at incubating, tool at graduated. Your repository's type and stage are in [registry.yaml](../../registry.yaml); the stages are explained in [lifecycle-stage-map.md](../lifecycle-stage-map.md), and the full table is in [policy-applicability.md](../policy-applicability.md).

## Set up

1. Tag each release as `vMAJOR.MINOR.PATCH` (semver.org): raise PATCH for fixes, MINOR for new features, and MAJOR for breaking changes.
2. For graduated tools, publish a short policy saying which releases are supported and how fixes are backported (copied into those older supported releases), then record the attestation below.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **semver-tags**: `GET /repos/{owner}/{repo}/releases -> every non-draft release tag in the last 12 months matches vMAJOR.MINOR.PATCH (semver.org)` (needs Contents: read)

## Attested checks

- **stable-release-policy**: For graduated tools: a published policy says which releases are supported, and how fixes are backported (copied into those older supported releases).

How to attest: add this entry to your repository's `ATTESTATIONS.yaml`, at its root, and renew it for each release
([attestations-format.md](../attestations-format.md)). An entry counts only if its `release` names the release being
checked (or `none` before the first release), and the last change to the file was committed by a code owner of the repository. Point to
the file from the README: "Attestations: see `ATTESTATIONS.yaml`."

```yaml
attestations:
  - policy: semantic-versioning
    check: stable-release-policy
    attested_by: your-github-username
    date: YYYY-MM-DD
    release: vX.Y.Z           # the release this is made for, or none if there is no release yet
```


## Why

- CISA: CISA-P-RELEASE-MARK (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: SA-10 (see `data/sources/nist-800-53.yaml`)
- ISO/IEC/IEEE 12207:2026 clause 6.3.5 (cited by reference)
- OpenSSF asks Incubating projects to follow a version schema and Graduated projects to adhere to semantic versioning with a stable-release policy (project lifecycle).

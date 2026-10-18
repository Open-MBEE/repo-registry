# Contribution guide

> **PROVISIONAL** until the maintainers approve the policies. Policy `contributing` (`data/policies/contributing.yaml`).

Tools from version 1.0, media in use, and the registry itself publish a contribution guide that keeps demands on contributors small, says what kinds of contribution are welcome, and asks for tests with code.

**Applies to:** tool at incubating, tool at graduated, media at incubating, media at graduated, governance at incubating (nothing yet), governance at graduated (the administration of the Open-MBEE GitHub organization, and repo-registry once it is accepted as the canonical source). Your repository's kind is in [registry.yaml](../../registry.yaml); the stages are explained in [lifecycle-stage-map.md](../lifecycle-stage-map.md), and the full table is in [policy-applicability.md](../policy-applicability.md).

## Set up

1. Add `CONTRIBUTING.md` at the root (or in `.github/`).
2. Say what kinds of contribution you welcome (for example bug reports, documentation, code).
3. Keep the demands on contributors small. If you accept code, ask for tests with each change.
4. Record the attestation below.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **contributing-present**: `GET /repos/{owner}/{repo}/community/profile -> files.contributing is not null` (needs Contents: read)

## Attested checks

- **contributing-content**: The contribution guide keeps requirements on contributors minimal, says which kinds of contribution are accepted, and (for code) asks for tests with each change.

How to attest: add this entry to your repository's `ATTESTATIONS.yaml`, at its root, and renew it for each release
([attestations-format.md](../attestations-format.md)). An entry counts only if its `release` names the release being
checked (or `none` before the first release), and the last change to the file was committed by a code owner of the repository. Point to
the file from the README: "Attestations: see `ATTESTATIONS.yaml`."

```yaml
attestations:
  - policy: contributing
    check: contributing-content
    attested_by: your-github-username
    date: YYYY-MM-DD
    release: vX.Y.Z           # the release this is made for, or none if there is no release yet
```


## Why

- CISA: CISA-P-CONTRIBUTING, CISA-P-CONTRIB-MINIMAL, CISA-P-CONTRIB-TYPES, CISA-P-CONTRIB-TESTS (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: SA-11 (see `data/sources/nist-800-53.yaml`)
- OpenSSF requires a contributor guide to enter Incubating (project lifecycle).

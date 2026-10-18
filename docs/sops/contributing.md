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

How to attest: add a block like this to the end of your `README.md`, one per attested check, and update it with each
release. An attestation counts only if a code owner of the repository committed it, and it is out of date once it
is older than the repository's latest release.

```markdown
<!-- repo-registry attestation
policy: contributing
check: contributing-content
attested-by: @your-github-username
date: YYYY-MM-DD
release: vX.Y.Z (or none)
-->
```


## Why

- CISA: CISA-P-CONTRIBUTING, CISA-P-CONTRIB-MINIMAL, CISA-P-CONTRIB-TYPES, CISA-P-CONTRIB-TESTS (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: SA-11 (see `data/sources/nist-800-53.yaml`)
- OpenSSF requires a contributor guide to enter Incubating (project lifecycle).

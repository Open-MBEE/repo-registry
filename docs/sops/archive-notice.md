# Clear end of support

> **PROVISIONAL** until the maintainers approve the policies. Policy `archive-notice` (`data/policies/archive-notice.yaml`).

Before a repository is archived, its README says that support has ended and points to any known active forks. Repositories archived before this policy existed count as compliant as they are.

**Applies to:** tool at archived, media at archived, research at archived. Your repository's type and stage are in [registry.yaml](../../registry.yaml); the stages are explained in [lifecycle-stage-map.md](../lifecycle-stage-map.md), and the full table is in [policy-applicability.md](../policy-applicability.md).

## Set up

1. Before archiving, add a note at the top of the README saying that support has ended, with the date, and naming any known active forks.
2. In the same commit, add the attestation entry below to the repository's `ATTESTATIONS.yaml`. Once a repository is archived, nobody can commit to it, so this has to come first. An archived repository is read at this final commit, so no release is needed for it.
3. Then archive the repository (Settings, then General, then Archive this repository).
4. Repositories archived before this policy existed need nothing more.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **archived**: `GET /repos/{owner}/{repo} -> archived == true` (needs Metadata: read)

## Attested checks

- **end-of-support-note**: The README says that support has ended, and names any known active forks. (Repositories archived before this policy existed are exempt.)

How to attest: add this entry to your repository's `ATTESTATIONS.yaml`, at its root, and renew it for each release
([attestations-format.md](../attestations-format.md)). An entry counts only if its `release` names the release being
checked (or `none` before the first release), and the last change to the file was committed by a code owner of the repository. Point to
the file from the README: "Attestations: see `ATTESTATIONS.yaml`."

```yaml
attestations:
  - policy: archive-notice
    check: end-of-support-note
    attested_by: your-github-username
    date: YYYY-MM-DD
    release: vX.Y.Z           # the release this is made for, or none if there is no release yet
```


## Why

- CISA: CISA-P-EOS-MARK, CISA-P-EOS-FORKS, CISA-P-EOS-PUBLISH (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: SA-22 (see `data/sources/nist-800-53.yaml`)
- ISO/IEC/IEEE 12207:2026 clause 6.4.14 (cited by reference)

# Clear end of support

> **PROVISIONAL** until the maintainers approve the policies. Policy `archive-notice` (`data/policies/archive-notice.yaml`).

Before a repository is archived, its README says that support has ended and points to any known active forks. Repositories archived before this policy existed count as compliant as they are.

## Set up

1. Before archiving, add a note at the top of the README saying that support has ended, with the date, and naming any known active forks.
2. Then archive the repository (Settings, then General, then Archive this repository).
3. Repositories archived before this policy existed need nothing more.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **archived**: `GET /repos/{owner}/{repo} -> archived == true` (needs Metadata: read)

## Attested checks

- **end-of-support-note**: The README says that support has ended, and names any known active forks. (Repositories archived before this policy existed are exempt.)

How to attest: add a block like this to the end of your `README.md`, one per attested check, and update it with each
release. An attestation counts only if a code owner of the repository committed it, and it is out of date once it
is older than the repository's latest release.

```markdown
<!-- repo-registry attestation
policy: archive-notice
check: end-of-support-note
attested-by: @your-github-username
date: YYYY-MM-DD
release: vX.Y.Z (or none)
-->
```


## Why

- CISA: CISA-P-EOS-MARK, CISA-P-EOS-FORKS, CISA-P-EOS-PUBLISH (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: SA-22 (see `data/sources/nist-800-53.yaml`)
- ISO/IEC/IEEE 12207:2026 clause 6.4.14 (cited by reference)

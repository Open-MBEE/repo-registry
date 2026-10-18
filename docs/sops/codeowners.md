# Named owners

> **PROVISIONAL** until the maintainers approve the policies. Policy `codeowners` (`data/policies/codeowners.yaml`).

Every live repository names the people who look after it, in a CODEOWNERS file. That file is the authoritative list of the repository's operators.

## Set up

1. Create `.github/CODEOWNERS` (or `CODEOWNERS` at the root, or `docs/CODEOWNERS`).
2. Name at least one person who looks after the repository, for example a line `* @your-github-username`. The people named here are the repository's operators.
3. Open the file on GitHub. If GitHub shows an error banner, fix the lines it points to.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **codeowners-present**: `GET /repos/{owner}/{repo}/contents/{.github/CODEOWNERS|CODEOWNERS|docs/CODEOWNERS} -> first of these returns 200` (needs Contents: read)
- **codeowners-valid**: `GET /repos/{owner}/{repo}/codeowners/errors -> errors is empty` (needs Contents: read)

## Attested checks

None.

## Why

- CISA: CISA-C4-COMMUNITY (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: CM-5 (see `data/sources/nist-800-53.yaml`)
- OpenSSF requires at least one maintainer at Sandbox (project lifecycle).

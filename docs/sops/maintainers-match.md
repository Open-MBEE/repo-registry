# Named maintainers match governance power

> **PROVISIONAL** until the maintainers approve the policies. Policy `maintainers-match` (`data/policies/maintainers-match.yaml`).

The named maintainers (data/maintainers.yaml) are exactly this repository's code owners, and every owner of the organization is a named maintainer. Owners are a small subset of the maintainers.

**Applies to:** governance at graduated: the administration of the Open-MBEE GitHub organization, and repo-registry once it is accepted as the canonical source. See [policy-applicability.md](../policy-applicability.md).

## Set up

1. Keep data/maintainers.yaml up to date through pull requests to this repository, which an owner merges.
2. Make this repository's CODEOWNERS list the same people.
3. Make sure every owner of the organization is a named maintainer. Owners are only two or three of them (see org-few-owners).
4. Declare any other admin powers under `other_powers` in data/maintainers.yaml, by a pull request that an owner merges (see below).

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **match**: `GET /orgs/{org}/members?role=admin and GET /orgs/{org}/public_members, compared by scripts/org.py with data/maintainers.yaml and this repository's CODEOWNERS (rows for people whose membership isn't public are yellow)` (needs organization member (Members: read))

## Attested checks

- **other-powers-declared**: Anyone else who holds admin power over the organization or its repositories outside GitHub's owner role (for example through installed apps or other platforms) is declared under `other_powers` in data/maintainers.yaml, by a pull request that an owner merges. The merge is the record.

How to attest: add this entry to the `ATTESTATIONS.yaml` of this repository, `repo-registry`, where the org is governed (the org has no repository of its own), and renew it for each release
([attestations-format.md](../attestations-format.md)). An entry counts only if its `release` names the release being
checked (or `none` before the first release), and the last change to the file was committed by a code owner of `repo-registry`. Point to
the file from the README: "Attestations: see `ATTESTATIONS.yaml`."

```yaml
attestations:
  - policy: maintainers-match
    check: other-powers-declared
    attested_by: your-github-username
    date: YYYY-MM-DD
    release: vX.Y.Z           # the release this is made for, or none if there is no release yet
```


## Why

- CISA: CISA-C4-COMMUNITY
- NIST SP 800-53: AC-6(1)

# Attestations format

> **PROVISIONAL** until the maintainers approve the policies (WP0, maintainer approval 2). WP4d D-1. Schema:
> [`data/schema/attestations.schema.yaml`](../data/schema/attestations.schema.yaml).

Some checks are facts the registry can't see for itself, such as "the design document is current". A repository's
code owners answer them in **one file**, `ATTESTATIONS.yaml`, at the root of the repository. Each policy's SOP lists
the attested checks it asks for, with the entry to copy.

## The file

```yaml
# Attestations for the OpenMBEE repo-registry policies (docs/attestations-format.md in Open-MBEE/repo-registry).
attestations:
  - policy: security-design
    check: design-current
    attested_by: your-github-username
    date: 2026-10-18
    release: v1.2.0
    note: Design reviewed for the new export API.
```

- `policy` and `check`: the policy and the attested check, exactly as the SOP names them. One entry per check.
- `attested_by`: the GitHub login of the code owner who attests.
- `date`: the day of the attestation, as YYYY-MM-DD.
- `release`: the tag of the release this attestation is made for, such as `v1.2.0`. A repository with no release
  yet writes `none`.
- `note`: optional, a short remark.

Point to it from the README with one line, for example: "Attestations: see `ATTESTATIONS.yaml`."
The pointer helps readers; it is not checked.

## How a release carries its attestations

A release names a tag, and the tag names a commit. That is GitHub's own binding, and nothing is added to the release.
The registry reads `ATTESTATIONS.yaml` **as it is at that commit**, so what a release attests is fixed with the
release, and a later edit can't change it.

Every release is attested afresh: an entry counts for a release only if its `release` names that release. So, when
you prepare a release:

1. Review each attested check your SOPs list.
2. Update its entry: set `release` to the tag you are about to create, and `date` to today.
3. Commit the file (a code owner must make that commit), then create the release from a commit that includes it.

A repository with no release yet keeps its entries on the default branch, with `release: none`. They don't go out of
date until there is a release; from the first release on, the release rule applies.

An archived repository is read at its final commit on the default branch, whatever its releases: its last
attestation (for example that its README says support has ended) is made in the commit just before it is archived.

## When an entry counts

An entry counts only if the last commit that changed `ATTESTATIONS.yaml`, up to the commit being read, was made by
a code owner of the repository at that commit (WP0 R-17). Who committed is read from git, not from the file. The
full rule, with the colors, is in [policy-format.md](policy-format.md), "Reading a check's result".

## The org's attestations

The org's administration (governance/graduated) has no repository of its own. Its attested checks are answered in
`ATTESTATIONS.yaml` in this repository, `repo-registry`, where the org is governed.

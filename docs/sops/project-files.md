# README

> **PROVISIONAL** until the maintainers approve the policies. Policy `project-files` (`data/policies/project-files.yaml`).

Every live repository has a README that says what it is and how to use it. (Its license is covered by [license-by-type](license-by-type.md).)

**Applies to:** tool at sandbox, tool at incubating, tool at graduated, media at sandbox, media at incubating, media at graduated, research at sandbox, research at incubating, research at graduated, the registry (repo-registry). Your repository's kind is in [registry.yaml](../../registry.yaml); the stages are explained in [lifecycle-stage-map.md](../lifecycle-stage-map.md), and the full table is in [policy-applicability.md](../policy-applicability.md).

## Set up

1. Add a `README.md` at the root that says what the project is and how to use it.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **readme-present**: `GET /repos/{owner}/{repo}/community/profile -> files.readme is not null` (needs Contents: read)
- **license-detected**: `GET /repos/{owner}/{repo} -> license.spdx_id is not null` (needs Metadata: read)

## Attested checks

None.

## Why

- CISA: CISA-P-README (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: none (see `data/sources/nist-800-53.yaml`)

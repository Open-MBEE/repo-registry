# README and license

> **PROVISIONAL** until the maintainers approve the policies. Policy `project-files` (`data/policies/project-files.yaml`).

Every live repository has a README that says what it is, and a license file that says how it may be used.

**Applies to:** tool at sandbox, tool at incubating, tool at graduated, media at sandbox, media at incubating, media at graduated, research at sandbox, research at incubating, research at graduated, the registry (repo-registry). Your repository's kind is in [registry.yaml](../../registry.yaml); the stages are explained in [lifecycle-stage-map.md](../lifecycle-stage-map.md), and the full table is in [policy-applicability.md](../policy-applicability.md).

## Set up

1. Add a `README.md` at the root that says what the project is and how to use it.
2. Add a `LICENSE` file at the root. Prefer a permissive license (for example Apache-2.0 or MIT), as CISA recommends, unless there is a reason not to.
3. Check that GitHub detects it: the repository's main page shows the license name next to the About box.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **readme-present**: `GET /repos/{owner}/{repo}/community/profile -> files.readme is not null` (needs Contents: read)
- **license-detected**: `GET /repos/{owner}/{repo} -> license.spdx_id is not null` (needs Metadata: read)

## Attested checks

None.

## Why

- CISA: CISA-P-README, CISA-P-LICENSE-FILE, CISA-P-LICENSE-PERMISSIVE (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: none (see `data/sources/nist-800-53.yaml`)
- OpenSSF and CNCF both require legal and license clearance from the Sandbox stage on (project lifecycles).

# Least-privilege automation

> **PROVISIONAL** until the maintainers approve the policies. Policy `workflow-least-privilege` (`data/policies/workflow-least-privilege.yaml`).

Tools from version 1.0, and the registry, give their GitHub Actions workflows read-only access by default, and set up workflows following GitHub's hardening guidance.

**Applies to:** tool at incubating, tool at graduated, governance at incubating (nothing yet), governance at graduated (the administration of the Open-MBEE GitHub organization, and repo-registry once it is accepted as the canonical source). Your repository's kind is in [registry.yaml](../../registry.yaml); the stages are explained in [lifecycle-stage-map.md](../lifecycle-stage-map.md), and the full table is in [policy-applicability.md](../policy-applicability.md).

## Set up

1. Go to Settings, then Actions, then General.
2. Under Workflow permissions, choose Read repository contents and packages permissions.
3. In each workflow, give each job only the permissions it needs, using the `permissions:` key.
4. Follow GitHub's security hardening guide for Actions (https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions), then record the attestation below.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **default-token-read**: `GET /repos/{owner}/{repo}/actions/permissions/workflow -> default_workflow_permissions == read` (needs Administration: read)

## Attested checks

- **workflows-hardened**: Workflows follow GitHub's security hardening guide for Actions: text that outside contributors control (such as pull request titles) is never run as a command, code from outside contributors' pull requests is never run with write access or secrets, and each job asks only for the permissions it needs.

How to attest: add a block like this to the end of your `README.md`, one per attested check, and update it with each
release. An attestation counts only if a code owner of the repository committed it, and it is out of date once it
is older than the repository's latest release.

```markdown
<!-- repo-registry attestation
policy: workflow-least-privilege
check: workflows-hardened
attested-by: @your-github-username
date: YYYY-MM-DD
release: vX.Y.Z (or none)
-->
```


## Why

- CISA: CISA-P-SSDF (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: AC-6 (see `data/sources/nist-800-53.yaml`)
- OpenSSF security baseline: TI-3, OI-1 (see `data/sources/openssf-security-baseline.yaml`)

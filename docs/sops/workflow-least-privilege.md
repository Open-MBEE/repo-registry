# Least-privilege automation

> **PROVISIONAL** until the maintainers approve the policies. Policy `workflow-least-privilege` (`data/policies/workflow-least-privilege.yaml`).

Tools from version 1.0, and the registry, give their GitHub Actions workflows read-only access by default, and set up workflows following GitHub's hardening guidance.

## Set up

1. Go to Settings, then Actions, then General.
2. Under Workflow permissions, choose Read repository contents and packages permissions.
3. In each workflow, give each job only the permissions it needs, using the `permissions:` key.
4. Follow GitHub's security hardening guide for Actions, then record the attestation below.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **default-token-read**: `GET /repos/{owner}/{repo}/actions/permissions/workflow -> default_workflow_permissions == read` (needs Administration: read)

## Attested checks

- **workflows-hardened**: Workflows follow GitHub's hardening guidance: no untrusted input in run steps, no checkout of untrusted pull request code in privileged triggers, and only the permissions each job needs.

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

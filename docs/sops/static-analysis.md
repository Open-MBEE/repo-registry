# Code scanning

> **PROVISIONAL** until the maintainers approve the policies. Policy `static-analysis` (`data/policies/static-analysis.yaml`).

Tools from version 1.0, and the registry, run code scanning on every change and fix critical findings promptly.

**Applies to:** tool at incubating, tool at graduated, the registry (repo-registry). Your repository's kind is in [registry.yaml](../../registry.yaml); the stages are explained in [lifecycle-stage-map.md](../lifecycle-stage-map.md), and the full table is in [policy-applicability.md](../policy-applicability.md).

## Set up

1. Go to Settings, then Advanced Security, and set up Code scanning with the CodeQL default setup (or your own workflow).
2. Make sure it runs on pull requests and on the default branch.
3. Fix critical findings within 14 days.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **code-scanning-configured**: `GET /repos/{owner}/{repo}/code-scanning/default-setup -> state == configured, or GET .../code-scanning/analyses is not empty` (needs Administration: read; Code scanning alerts: read)
- **no-open-critical**: `GET /repos/{owner}/{repo}/code-scanning/alerts?state=open -> none with security_severity_level == critical older than 14 days` (needs Code scanning alerts: read)

## Attested checks

None.

## Why

- CISA: CISA-P-MAINT-SCANS, CISA-P-SECURITY-REVIEW (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: SA-11(1) (see `data/sources/nist-800-53.yaml`)
- OpenSSF security baseline: OI-2 (see `data/sources/openssf-security-baseline.yaml`)

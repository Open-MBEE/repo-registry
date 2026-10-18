# Reviewed changes

> **PROVISIONAL** until the maintainers approve the policies. Policy `change-review` (`data/policies/change-review.yaml`).

High-tier repositories (graduated tools, and the registry) need at least one approving review from a code owner, and passing checks, before a change is merged to the default branch.

**Applies to:** tool at graduated, the registry (repo-registry). Your repository's kind is in [registry.yaml](../../registry.yaml); the stages are explained in [lifecycle-stage-map.md](../lifecycle-stage-map.md), and the full table is in [policy-applicability.md](../policy-applicability.md).

## Set up

1. In the default branch's ruleset (see history-protection), turn on Require a pull request before merging.
2. Set Required approvals to at least 1, and turn on Require review from Code Owners.
3. Turn on Require status checks to pass, and pick the checks that must pass.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **review-required**: `GET /repos/{owner}/{repo}/rules/branches/{default_branch} -> a pull_request rule with required_approving_review_count >= 1 and require_code_owner_review == true` (needs Metadata: read)
- **checks-required**: `GET /repos/{owner}/{repo}/rules/branches/{default_branch} -> a required_status_checks rule` (needs Metadata: read)

## Attested checks

None.

## Why

- CISA: CISA-P-CODE-REVIEW, CISA-C4-CONDUCT (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: CM-5(4), SA-11(4), CM-3 (see `data/sources/nist-800-53.yaml`)
- OpenSSF security baseline: TG-4 (see `data/sources/openssf-security-baseline.yaml`)

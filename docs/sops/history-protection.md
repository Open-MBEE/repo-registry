# Keep the history

> **PROVISIONAL** until the maintainers approve the policies. Policy `history-protection` (`data/policies/history-protection.yaml`).

Tools from version 1.0, and the registry, protect the default branch from force pushes and deletion, so that its history stays complete for review and audit.

**Applies to:** tool at incubating, tool at graduated, the registry (repo-registry). Your repository's kind is in [registry.yaml](../../registry.yaml); the stages are explained in [lifecycle-stage-map.md](../lifecycle-stage-map.md), and the full table is in [policy-applicability.md](../policy-applicability.md).

## Set up

1. Go to Settings, then Rules, then Rulesets, and create a branch ruleset that targets the default branch.
2. Turn on Block force pushes and Restrict deletions, and set enforcement to Active.
3. That is all this policy asks. Squash-merging pull requests is fine: what it prevents is rewriting or deleting the default branch's published history.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **no-force-push**: `GET /repos/{owner}/{repo}/rules/branches/{default_branch} -> includes a rule of type non_fast_forward (classic branch protection needs admin read: yellow if only that is set and unreadable)` (needs Metadata: read)
- **no-deletion**: `GET /repos/{owner}/{repo}/rules/branches/{default_branch} -> includes a rule of type deletion` (needs Metadata: read)

## Attested checks

None.

## Why

- CISA: CISA-P-NO-SQUASH, CISA-P-HISTORY-ASSET (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: CM-3 (see `data/sources/nist-800-53.yaml`)

# WP2 — Summary for the supervisor

> Everything here is **PROVISIONAL** until the maintainers approve the policies (WP0, maintainer approval 2). This
> summary meets WP2's Definition of good enough, last item.

## The policies

Fifteen named policies, each GitHub-native, each with a plain "applies if" rule on type, stage or tier, an SOP, and
citations: CISA and NIST SP 800-53 (core), and the OpenSSF baseline, the CNCF and OpenSSF lifecycles, and ISO/IEC/IEEE
12207 clauses (secondary). Full table: [policy-applicability.md](https://github.com/Open-MBEE/repo-registry/blob/6938aa5/docs/policy-applicability.md). Grounding:
[policy-basis-review.md](../docs/policy-basis-review.md).

| Policy | In effect for | What it asks |
|---|---|---|
| project-files | every live repo | README and a license |
| codeowners | every live repo | named owners in CODEOWNERS |
| contributing | tools and media from Incubating, and the registry | a short contribution guide |
| secret-protection | tools from Incubating, and the registry | push protection on |
| workflow-least-privilege | tools from Incubating, and the registry | read-only workflow tokens by default; hardened workflows |
| dependency-management | tools from Incubating, and the registry | Dependabot alerts on; a dependency policy |
| security-policy | tools from Incubating, and the registry | SECURITY.md; private vulnerability reporting on |
| static-analysis | tools from Incubating, and the registry | code scanning; critical findings fixed in 14 days |
| history-protection | tools from Incubating, and the registry | no force pushes or deletion of the default branch |
| semantic-versioning | tools from Incubating | semver release tags; graduated tools also state a stable-release policy |
| change-review | high tier (graduated tools, and the registry) | an approving code-owner review and passing checks before merging |
| vulnerability-remediation | high tier | critical in 14 days, medium and high in 60 days |
| security-design | high tier | a current security design document |
| release-integrity | graduated tools | SBOM, signed releases, provenance, no built executables in source |
| archive-notice | archived repos | end-of-support note and known forks, before archiving |

Counts per kind: sandbox 2, incubating tools 10, graduated tools 14, archived 1, media 2 to 3, research 2. The
registry (governance/sandbox) gets 12. The org's administration gets none here, because it belongs to WP3.

## What was deliberately left out, and why

- **OpenSSF backbone departures (9 of 25 items):**
  - Memory-safe language: a design choice, not a repository setting.
  - Two-factor authentication: moves to the org policy in WP3.
  - The Scorecard Action and SECURITY_INSIGHTS.yml: they would duplicate this registry.
  - Five items about services the foundation runs (encryption in transit, logging, monitoring, audits): OpenMBEE
    repos hold software others deploy.
- **CISA practices left out (26 of 56):**
  - federal-only duties (inventory, usage types, staff accounts, contracts);
  - the consumer's C4 evaluation steps;
  - practices about contributing to other projects.
- **Each reason is in `data/policies/_departures.yaml`,** and a test fails if any item is unaccounted for.

## Things worth your attention

1. **The checker needs *Administration: read*.** Push protection, Dependabot on/off, workflow-token defaults and
   classic branch protection are hidden from plain readers. GitHub also answers 404 for both "off" and "can't see".
   Without that permission, those checks show yellow. This is WP0's strong read credential, and its setup is WP3/WP5
   work.
2. **`repo-registry` will show red on `change-review` until R3,** because WP0 keeps its review friction low until
   then. That is an expected, visible gap, not enforcement.
3. **Deadlines I set:**
   - "Promptly" for critical findings is 14 days.
   - The 60-day deadline for medium and high comes from the OpenSSF baseline.
   - The 14 days is my choice and is easy to change in the data.
4. **The dependency-graph SBOM endpoint closes after 2026-11-13,** so `release-integrity` checks release assets
   instead.

## Checks

`python3 -m unittest discover -s tests` runs 31 checks (16 for WP1, 12 for WP2, and 3 for forthcoming work, 2 of which are expected failures tied to
`data/expected-gaps.yaml`). All pass. `python3
scripts/policies.py` re-checks every meta-rule and regenerates the table. Needs a person: R-5, the cold read of the
SOPs.

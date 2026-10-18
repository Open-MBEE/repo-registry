# Policy basis review

> **PROVISIONAL** until the maintainers approve the policies (WP0, maintainer approval 2). WP2 D-1.

This review grounds the policy set. It inventories what GitHub can carry, takes the OpenSSF security baseline by
stage as the backbone (WP2 OD1), cross-checks against CISA, NIST SP 800-53, the CNCF stage expectations and
ISO/IEC/IEEE 12207:2026 (by reference), and ends with the proposed set and why each item was kept or left out.
The policy table and the trace tables below were regenerated from `data/` at the docs sweep (WP4b). No script
writes this file, so they must be regenerated when `data/` changes. `scripts/policies.py` re-checks the same
coverage on every change.

## Sources

| Role | Source | Version read |
|---|---|---|
| Core | CISA, *Open Source Software: Security Principles and Practices* (2026-07-30), `data/sources/cisa-practices.yaml` | PDF fetched 2026-10-17, page numbers from its footers |
| Core | NIST SP 800-53 Rev. 5 (release 5.2.0), OSCAL catalog, `data/sources/nist-800-53.yaml` | `usnistgov/oscal-content` commit 78650f0 |
| Core | NIST SP 800-37 Rev. 2 (RMF) | official PDF; the step map is in WP0 |
| Core, backbone | OpenSSF security baseline by stage, `data/sources/openssf-security-baseline.yaml` | `ossf/tac` commit 098faba |
| Core | OpenSSF project lifecycle (the stages) | `ossf/tac` commit d019efe |
| Secondary | CNCF project lifecycle | `cncf/toc` commit d815451 |
| Secondary | ISO/IEC/IEEE 12207:2026, clause numbers only (single-user licensed copy; no text committed) | 2026-04 edition |
| Platform | GitHub documentation (docs.github.com), each page linked from the policy that uses it | read 2026-10-17 |
| Core, candidate (WP5e) | DoD CIO, *Software Development and Open Source Software*, memorandum, Attachment 2 §2.C(1), (2), (5), (6) and §3.H; [PDF](https://dodcio.defense.gov/Portals/0/Documents/Library/SoftwareDev-OpenSource.pdf) | 2022-01-24, cleared for open publication 2022-01-26; read in full 2026-10-18 |
| Secondary, candidate (WP5e) | OFAC sanctions regulations, 31 CFR Chapter V (for example §560.204 Iran, §515.505 Cuba), and the SDN list: the sanctions floor, by location or residence and listed-party status, not nationality | eCFR, current; from the research spike, not yet read in full |
| Secondary, candidate (WP5e) | GitHub, *GitHub and trade controls* (how the platform applies OFAC rules: by location, not nationality) | docs.github.com, current; from the research spike |
| Secondary, candidate (WP5e) | NIST SP 800-218, SSDF v1.1, PS.1 to PS.3 (protect code, verify integrity, keep provenance) | 2022-02; from the research spike |
| Secondary, candidate (WP5e) | NIST SP 800-161 Rev. 1, SR-4 (provenance) and SR-6 (supplier assessment), with NIST SP 1326, *Due Diligence Assessment Quick-Start Guide* (foreign ownership, control or influence) | revision label and SP 1326 date to verify; from the research spike |
| Context, candidate (WP5e) | EAR §734.3(b)(3) and §734.7: published open-source software is not subject to the EAR (published encryption, ECCN 5D002, still notifies under §742.15(b)); why the policy controls contributors, not exports | eCFR, current; from the research spike |
| Context, candidate (WP5e) | Secretary of Defense, *Enhancing Security Protocols for the Department of Defense*: no procurement of software open to adversarial foreign influence; motivation only, no rule for OSS contributors | 2025-07-18; seen only in a press copy, to verify |

Rows marked *candidate (WP5e)* are tracked for the contributor-sourcing package ([WP5e-decisions.md](../work-packages/WP5e-decisions.md));
its scope decides which are adopted. Read and set aside: EPA's EPAAR 1552.239-71 (an EPA contract clause, binding EPA
contractors only) and EAR Part 732 (the procedure for deciding whether the EAR applies).

## What GitHub can carry, and what it takes to read it

Every automated check reads a GitHub API field. What matters most for the design is the permission needed:

- **Any reader** (*Metadata* or *Contents: read*) sees repository metadata, the license, archived state, the community
  profile (README, CONTRIBUTING), CODEOWNERS and its errors, the effective branch rules (rulesets), releases (including
  `immutable`), private vulnerability reporting, and the security policy (GraphQL `isSecurityPolicyEnabled`).
- **Alert readers** (*Dependabot alerts: read*, *Code scanning alerts: read*) see the alert lists and their ages.
- **Administration: read** is needed for the security settings: push protection (`security_and_analysis`),
  Dependabot alerts on/off (`vulnerability-alerts`), CodeQL default setup, workflow token defaults, and classic
  branch protection.

Two hazards shape how checks are read:

1. Several endpoints answer **404 both for "off" and for "you may not see this"**, and `security_and_analysis` is simply
   absent for non-admins. So a check the credential can't read is **yellow**, never "off". This is why WP0's strong
   read credential is a read-only token with *Administration: read*.
2. `rules/branches/{branch}` shows rulesets, but not classic branch protection. The SOPs therefore recommend
   **rulesets**; a classic branch-protection rule that does the same job still passes (WP3 G-3 follow-ups).

Immutable releases and rulesets are confirmed for the Open-MBEE org, which is on GitHub Free
(`data/sources/github-plan.yaml`, `confirmed_in_org`; WP3 G-3 follow-ups). Not confirmed in GitHub's
documentation, so not relied on: whether `isSecurityPolicyEnabled` counts an organization-default `SECURITY.md`,
and the permission needed for some GraphQL fields. The dependency-graph SBOM endpoint closes after 2026-11-13, so
`release-integrity` checks release assets instead.

## The proposed policy set

Repository policies (WP2, and `license-by-type` from WP2a) and org policies (WP3), each stating its scope.
The org policies apply to governance/graduated: the administration of the GitHub org itself, and `repo-registry`
once it is accepted as the canonical source (WP4c).

The table is a view, rendered from the policies and `data/sources/` (WP5b F-08): run `uv run python scripts/render.py` and read `build/demo/policy-basis-tables.md`.

**Friction follows the tiers (WP2 R-7).** Sandbox kinds carry only `project-files` (a README), `codeowners` and
`license-by-type` (added in WP2a). Those come from the OpenSSF and CNCF lifecycle entry expectations (license and IP
clearance, at least one maintainer), not from the Sandbox security baseline, whose two items are departed or moved
(two-factor authentication is an org policy since WP3). Friction then rises with the stage: incubating tools carry
more, graduated tools the most, and archived repositories only the archive notice (the applicability view gives the
exact sets).
Governance friction rises with the stage, as for tools (WP4c). `repo-registry` (governance/sandbox, low) carries
the policies of a sandbox tool while it is being set up. governance/incubating (medium), for when the maintainers
calibrate it together, carries an incubating tool's policies except `semantic-versioning`. governance/graduated
(high) carries the org policies and the strict repository set: the org's administration has it today,
and `repo-registry` takes it on when it is accepted as the canonical source. Its review friction rises only then
(XF-2 in `data/measured-gaps.yaml`).

**Simplest set (WP2 R-6).** Each policy carries one job. No two automated checks read the same thing (a test checks
this). Items that GitHub can't check and that serve the same goal are folded into one policy's attested checks, for
example signing, provenance and no built executables in `release-integrity`.

## Trace: OpenSSF security baseline (backbone, WP2 R-13)

The table is a view, rendered from the policies and `data/sources/` (WP5b F-08): run `uv run python scripts/render.py` and read `build/demo/policy-basis-tables.md`.

## Trace: CISA practices (WP2 R-6)

The table is a view, rendered from the policies and `data/sources/` (WP5b F-08): run `uv run python scripts/render.py` and read `build/demo/policy-basis-tables.md`.

## NIST SP 800-53 controls cited

The table is a view, rendered from the policies and `data/sources/` (WP5b F-08): run `uv run python scripts/render.py` and read `build/demo/policy-basis-tables.md`.

Also in the sources file, but cited by no policy: `CM-10(1)`, `CM-14`, `SI-7`, `AC-2`, `AC-2(3)`, `AC-2(7)`,
`AC-5`, `AC-6(7)`, `IR-7`, `PS-9`.
`CM-14` and `SI-7` are the consumer-side counterparts of `release-integrity`. `CM-10(1)` (open-source software)
is the consumer-side counterpart of `project-files`. The others are cited by items of the maintainer policy
([maintainer-policy.md](maintainer-policy.md), WP3), not by a policy file.

## ISO/IEC/IEEE 12207:2026, by clause

The table is a view, rendered from the policies and `data/sources/` (WP5b F-08): run `uv run python scripts/render.py` and read `build/demo/policy-basis-tables.md`.

§5.4 (life cycle stages) underlies the stage map in WP1 ([lifecycle-stage-map.md](lifecycle-stage-map.md)). No text
from the standard is committed (WP2 R-12).

## CNCF cross-check

CNCF's lifecycle asks less of each stage in writing than OpenSSF does, but points the same way. Sandbox expects
breaking changes and light process. Incubation expects stable, versioned APIs and adopters. Graduation expects
production use and comprehensive security. CNCF's archiving guidance separates a mature, feature-complete project
from an inactive one, which matches keeping maintenance duties (`dependency-management`, `vulnerability-remediation`)
as policies on incubating and graduated kinds, not as a lifecycle stage. No CNCF expectation contradicts the set.

## License basis (WP2a)

`license-by-type` sets which licenses OpenMBEE accepts for each type of content. It was added after WP2, because
`project-files` only required that some license existed.

| Type | Allowed (SPDX) | Grounded in |
|---|---|---|
| tool | Apache-2.0, MIT | OpenSSF charter: software code is Apache-2.0 or MIT. CISA: prefer a permissive license (p. 16) |
| media | CC-BY-4.0, Apache-2.0, MIT | OpenSSF charter: documentation is CC-BY-4.0. Apache-2.0 or MIT where the media is mostly code |
| research | Apache-2.0, MIT, CC-BY-4.0, CDLA-Permissive-2.0, CDLA-Sharing-1.0 | OpenSSF charter: code Apache-2.0 or MIT, documentation CC-BY-4.0, data a Community Data License Agreement |
| governance | Apache-2.0 | As for tools. This repository is code and data |

- **OpenSSF:** the charter clause is quoted in the project lifecycle (`ossf/tac` d019efe): "unless otherwise approved by
  the Governing Board". Specifications under the Community Specification License 1.0 aren't a separate type here. A
  repository that is a specification can record an exception.
- **NumFOCUS,** OpenMBEE's fiscal sponsor, was researched first (WP2a OD2). Its project-support page
  (numfocus.org/projects-overview, read 2026-10-18):
  - expects projects to be "published under a standard open source license", and lists an OSI-approved license among
    the signs of an open project;
  - gives, as an example of a project not approved, one whose repositories use different licenses, some unlicensed;
  - says nothing about documentation or data licenses, and its application form only asks for the license.

  Apache-2.0 and MIT are OSI-approved, so there is no conflict. NumFOCUS's concern about mixed and missing licenses is
  one more reason for this policy.
- **Exceptions:** any other license, for example MPL-2.0, BSD-3-Clause or CC0-1.0, needs an accepted exception in
  `data/deviations.yaml`, with the reason and who approved it, by a pull request that an owner merges (WP4b OD3;
  the design ID is PO-8 in [requirements/policy.md](requirements/policy.md)).
- **Forks** have no kind, so the policy doesn't apply to them, and they keep their upstream license.
- **Today:** the license view (`build/demo/reports/license-report.yaml`, rendered by `uv run python
  scripts/render.py`) gives each live, classified repository's color; at WP2a most red ones had no license, a few a
  license GitHub can't recognize, and three an off-list license (`architecture-based-risk-analysis` MPL-2.0,
  `enhancement-proposals` BSD-3-Clause, `oosem.github.io` CC0-1.0).

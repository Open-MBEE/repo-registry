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

21 policies: 16 repository policies (WP2, and `license-by-type` from WP2a) and 5 org policies (WP3).
The org policies apply to governance/graduated: the administration of the GitHub org itself, and `repo-registry`
once it is accepted as the canonical source (WP4c).

| Policy | Scope | In effect for | GitHub mechanism | Automated / attested checks |
|---|---|---|---|---|
| [archive-notice](sops/archive-notice.md) | repository | tool/archived, media/archived, research/archived | Repository archiving, with an end-of-support note in the README | 1 / 1 |
| [change-review](sops/change-review.md) | repository | tool/graduated, governance/graduated | A ruleset (preferred) or a branch protection rule requiring an approving code-owner review and passing status checks | 2 / 0 |
| [codeowners](sops/codeowners.md) | repository | every live kind | CODEOWNERS file at .github/CODEOWNERS, CODEOWNERS or docs/CODEOWNERS | 2 / 0 |
| [contributing](sops/contributing.md) | repository | tool/incubating, tool/graduated, media/incubating, media/graduated, governance/incubating, governance/graduated | CONTRIBUTING file, detected by GitHub's community profile | 1 / 1 |
| [dependency-management](sops/dependency-management.md) | repository | tool/incubating, tool/graduated, governance/incubating, governance/graduated | Dependabot alerts (with the dependency graph, always on for public repos) | 1 / 2 |
| [governance-roles-named](sops/governance-roles-named.md) | org | governance/graduated | Public organization membership | 2 / 0 |
| [history-protection](sops/history-protection.md) | repository | tool/incubating, tool/graduated, governance/incubating, governance/graduated | A ruleset (preferred) or a branch protection rule that blocks force pushes and deletion on the default branch | 2 / 0 |
| [license-by-type](sops/license-by-type.md) | repository | every live kind | A LICENSE file, detected by GitHub's license detection (SPDX identifier) | 1 / 0 |
| [maintainers-match](sops/maintainers-match.md) | org | governance/graduated | Organization owner role and this repository's CODEOWNERS | 1 / 1 |
| [org-base-permission](sops/org-base-permission.md) | org | governance/graduated | Organization setting: base permissions for members | 1 / 0 |
| [org-few-owners](sops/org-few-owners.md) | org | governance/graduated | Organization owner role | 1 / 0 |
| [org-two-factor](sops/org-two-factor.md) | org | governance/graduated | Organization setting: require two-factor authentication | 1 / 0 |
| [project-files](sops/project-files.md) | repository | every live kind | A README file, detected by GitHub's community profile | 1 / 0 |
| [release-integrity](sops/release-integrity.md) | repository | tool/graduated | Release assets, immutable releases and artifact attestations | 2 / 2 |
| [secret-protection](sops/secret-protection.md) | repository | tool/incubating, tool/graduated, governance/incubating, governance/graduated | Secret scanning push protection (repository security settings) | 1 / 0 |
| [security-design](sops/security-design.md) | repository | tool/graduated, governance/graduated | None: a document in the repository, attested by its code owners | 0 / 1 |
| [security-policy](sops/security-policy.md) | repository | tool/incubating, tool/graduated, governance/incubating, governance/graduated | SECURITY.md security policy and private vulnerability reporting | 2 / 1 |
| [semantic-versioning](sops/semantic-versioning.md) | repository | tool/incubating, tool/graduated | Release tags | 1 / 1 |
| [static-analysis](sops/static-analysis.md) | repository | tool/incubating, tool/graduated, governance/incubating, governance/graduated | Code scanning (CodeQL default or advanced setup) | 2 / 0 |
| [vulnerability-remediation](sops/vulnerability-remediation.md) | repository | tool/graduated, governance/graduated | Dependabot alerts and code scanning alerts, with their ages | 2 / 1 |
| [workflow-least-privilege](sops/workflow-least-privilege.md) | repository | tool/incubating, tool/graduated, governance/incubating, governance/graduated | Actions default workflow permissions set to read | 1 / 1 |

**Friction follows the tiers (WP2 R-7).** Sandbox kinds carry only `project-files` (a README), `codeowners` and
`license-by-type` (added in WP2a). Those come from the OpenSSF and CNCF lifecycle entry expectations (license and IP
clearance, at least one maintainer), not from the Sandbox security baseline, whose two items are departed or moved
(two-factor authentication is an org policy since WP3). Incubating tools carry 11 policies, graduated tools 15,
archived repositories 1. Media carries 3 or 4, and research 3.
Governance friction rises with the stage, as for tools (WP4c). `repo-registry` (governance/sandbox, low) carries
the 3 policies of a sandbox tool while it is being set up. governance/incubating (medium), for when the maintainers
calibrate it together, carries an incubating tool's policies except `semantic-versioning`: 10. governance/graduated
(high) carries the 5 org policies and the strict repository set, 18 in all: the org's administration has it today,
and `repo-registry` takes it on when it is accepted as the canonical source. Its review friction rises only then
(XF-2 in `data/expected-gaps.yaml`).

**Simplest set (WP2 R-6).** Each policy carries one job. No two automated checks read the same thing (a test checks
this). Items that GitHub can't check and that serve the same goal are folded into one policy's attested checks, for
example signing, provenance and no built executables in `release-integrity`.

## Trace: OpenSSF security baseline (backbone, WP2 R-13)

| Item | Stage | Baseline item (paraphrased) | Adopted by | Or departed because |
|---|---|---|---|---|
| SB-1 | sandbox (once) | New projects or components use a memory-safe language (or C/C++ compiler hardening) |  | A language is a design choice for each tool, not a repository setting that GitHub can carry. Most OpenMBEE code is already in memory-safe languages (Java, Kotlin, Python, TypeScript, Go, Rust). Revisit if new C or C++ components appear. |
| SB-2 | sandbox (once) | Two-factor authentication for interactive repository access | org-two-factor |  |
| TI-1 | incubating (to-become) | Onboard to OpenSSF Scorecard (Scorecard GitHub Action) |  | Scorecard is OpenSSF's measuring tool. The registry measures the controls we adopted directly, and anyone can run Scorecard against a public repository without the repository adding a workflow. Requiring the Scorecard Action on every repository would add a workflow with extra write permissions and duplicate this registry's job. |
| TI-2 | incubating (to-become) | No hard-coded active secrets in the repository | secret-protection |  |
| TI-3 | incubating (to-become) | Credentials have minimal permissions (least privilege, workflow tokens, few owners and admins) | org-base-permission, org-few-owners, workflow-least-privilege |  |
| TI-4 | incubating (to-become) | Security insights metadata file (SECURITY_INSIGHTS.yml) |  | A SECURITY_INSIGHTS.yml file in each repository would duplicate the record this registry already keeps, and add overhead to every repository. Revisit if adopters ask for it in that format. |
| TI-5 | incubating (to-become) | A dependencies policy is published, maintained and followed | dependency-management |  |
| TI-6 | incubating (to-become) | Direct dependencies are pinned in services the project provides | dependency-management |  |
| OI-1 | incubating (once) | GitHub Actions workflows are set up securely | workflow-least-privilege |  |
| OI-2 | incubating (once) | Static code analysis runs in CI and critical exploitable findings are fixed promptly | static-analysis |  |
| OI-3 | incubating (once) | A security policy for vulnerability disclosure and response is published and followed; private vulnerability reporting enabled | security-policy |  |
| OI-4 | incubating (once) | Data in transit is protected cryptographically |  | It is about services the foundation runs. OpenMBEE repositories hold software that others deploy, and encryption in transit is a property of a deployment, not of a repository setting. |
| TG-1 | graduated (to-become) | An architecture design with up-to-date security controls is maintained | security-design |  |
| TG-2 | graduated (to-become) | No medium or higher severity findings from static analysis | vulnerability-remediation |  |
| TG-3 | graduated (to-become) | Known vulnerabilities fixed: critical promptly, medium or high within 60 days | vulnerability-remediation |  |
| TG-4 | graduated (to-become) | Merging to the main branch needs at least one maintainer approval and passing status checks | change-review |  |
| TG-5 | graduated (to-become) | No generated executable artifacts in the source repository | release-integrity |  |
| TG-6 | graduated (to-become) | An SBOM is generated and published with each release | release-integrity |  |
| TG-7 | graduated (to-become) | Release artifacts are cryptographically signed | release-integrity |  |
| TG-8 | graduated (to-become) | SLSA v1.0 Build Level 3 provenance is published with releases | release-integrity |  |
| TG-9 | graduated (to-become) | Security events are logged (for internet or infrastructure services run for the foundation) |  | It is for internet or infrastructure services run on behalf of the foundation. OpenMBEE repositories don't run such services, so there is nothing in a repository to log. |
| TG-10 | graduated (to-become) | Security events are monitored (for internet or infrastructure services run for the foundation) |  | It is for internet or infrastructure services run on behalf of the foundation. OpenMBEE repositories don't run such services, so there is nothing in a repository to monitor. |
| TG-11 | graduated (to-become) | An initial third-party security audit, with findings addressed (for services run for the foundation) |  | It is a foundation-funded audit of services the foundation runs. OpenMBEE has no such services or funding process. A tool's security design is covered by the security-design policy. |
| OG-1 | graduated (once) | Known vulnerabilities are fixed and released in coordination with consumers, within the same deadlines | vulnerability-remediation |  |
| OG-2 | graduated (once) | Security audits as needed after the initial one (for services run for the foundation) |  | It follows from TG-11, which is left out for the same reason. |

## Trace: CISA practices (WP2 R-6)

| Practice | p. | Carried by | Or left out because |
|---|---|---|---|
| CISA-P-DEFAULT-OPEN | 13 |  | Federal agency policy on deciding to publish code. OpenMBEE repositories are open by default. |
| CISA-P-OPEN-PRACTICES | 12-13 |  | A development habit (work in the open from the start), not a repository control. |
| CISA-P-HISTORY-ASSET | 12 | history-protection |  |
| CISA-P-INVENTORY | 13 |  | A federal source-code inventory. This registry plays that role for OpenMBEE (a code.json export is an R5 candidate). |
| CISA-P-USAGE-TYPE | 14 |  | Federal usage types (open source, reuse, exemptions). Every OpenMBEE repository is open source. |
| CISA-P-USAGE-REVIEWS | 15 |  | Federal reviews per usage type. They don't apply to an open source foundation. |
| CISA-P-METADATA | 15 |  | Federal inventory metadata. The registry's own data serves this purpose. |
| CISA-P-METADATA-FILE | 15, 30 |  | The federal code.json file. An export in that shape is an R5 candidate, not a repository control. |
| CISA-P-METADATA-FIELDS | 27-31 |  | Fields of the federal metadata schema. As for CISA-P-METADATA-FILE. |
| CISA-P-PREPUB-REVIEW | 15-16 | secret-protection |  |
| CISA-P-LIFECYCLE-RESOURCES | 16 |  | Planning resources for a project's life is a governance matter for the maintainers, not a repository control. The lifecycle stages make it visible. |
| CISA-P-SECRET-DETECT | 16 | secret-protection |  |
| CISA-P-DEP-SCAN | 16 | dependency-management |  |
| CISA-P-SECURITY-REVIEW | 16 | static-analysis |  |
| CISA-P-NO-SQUASH | 16 | history-protection |  |
| CISA-P-LICENSE-PERMISSIVE | 16 | license-by-type |  |
| CISA-P-PUBLIC-HOST | 16 |  | OpenMBEE already publishes on GitHub. |
| CISA-P-STAFF-ACCOUNTS | 16 |  | Federal staff account naming. It doesn't apply to an open community. |
| CISA-P-README | 16 | project-files |  |
| CISA-P-LICENSE-FILE | 16 | license-by-type |  |
| CISA-P-CONTRIBUTING | 16 | contributing |  |
| CISA-P-SECURITY-MD | 16 | security-policy |  |
| CISA-P-SBOM-RELEASE | 17 | release-integrity |  |
| CISA-P-VDP-BOD | 17 | security-policy |  |
| CISA-P-VDP-AI-REPORTS | 10-11 | security-policy |  |
| CISA-P-SECURITY-CONTACT | 10 | security-policy |  |
| CISA-P-CONTRIB-MINIMAL | 17 | contributing |  |
| CISA-P-CONTRIB-TYPES | 17 | contributing |  |
| CISA-P-CONTRIB-TESTS | 17 | contributing |  |
| CISA-P-CODE-REVIEW | 17 | change-review |  |
| CISA-P-RELEASE-MARK | 17 | release-integrity, semantic-versioning |  |
| CISA-P-MAINT-SCANS | 17 | static-analysis, vulnerability-remediation |  |
| CISA-P-ACTIVE-DEF | 17 | vulnerability-remediation |  |
| CISA-P-EOS-MARK | 17 | archive-notice |  |
| CISA-P-EOS-PUBLISH | 17 | archive-notice |  |
| CISA-P-EOS-FORKS | 18 | archive-notice |  |
| CISA-P-CONTRACT-RIGHTS | 18 |  | Federal contracting terms. |
| CISA-P-SSDF | 18 | workflow-least-privilege |  |
| CISA-P-CI-PATCH-AUTO | 10 | dependency-management |  |
| CISA-P-DEV-GUIDES | 5, 13 |  | A pointer to other guides. Their content enters through the OpenSSF baseline (the backbone). |
| CISA-C-UPSTREAM | 9, 11 |  | About contributing to other projects. It isn't a control on OpenMBEE's own repositories. |
| CISA-C-INTERNAL-REVIEW | 11 |  | An agency's review of its staff's outside contributions. Not a repository control. |
| CISA-C-LEGAL | 11-12 |  | An agency's legal review before contributing elsewhere. Not a repository control. |
| CISA-C-PRIVACY | 12 |  | An agency's privacy review before contributing elsewhere. Secrets in OpenMBEE repositories are covered by secret-protection. |
| CISA-C-INCENTIVES | 11 |  | An agency's incentives for staff contributions. Not a repository control. |
| CISA-C4-CODEBASE | 24 |  | How consumers judge a codebase. It is served indirectly, by dependency-management and vulnerability-remediation, rather than being a control itself. |
| CISA-C4-COMMUNITY | 24 | codeowners, governance-roles-named, maintainers-match |  |
| CISA-C4-CONDUCT | 24 | change-review |  |
| CISA-C4-CONFIG | 24 | security-design |  |
| CISA-C4-HOLISTIC | 24-25 |  | Guidance on how consumers weigh criteria. Not a control. |
| CISA-C4-S1-CRITERIA | 25 |  | A consumer's evaluation step. The registry is meant to make our repositories easy to evaluate, and its checks are measurable, as this step asks. |
| CISA-C4-S2-TOLERANCE | 25 |  | A consumer's evaluation step. Not a producer control. |
| CISA-C4-S3-OBSERVE | 25 |  | A consumer's evaluation step. Not a producer control. |
| CISA-C4-S4-EVALUATE | 25-26 |  | A consumer's evaluation step. Not a producer control. |
| CISA-C4-S5-COMPARE | 26 |  | A consumer's evaluation step. Not a producer control. |
| CISA-C4-REEVAL | 7-8, 10 |  | How often consumers re-evaluate. The registry's scheduled runs serve this, from R2. |

## NIST SP 800-53 controls cited

| Control | Title | Cited by |
|---|---|---|
| AC-6 | Least Privilege | org-base-permission, workflow-least-privilege |
| CM-3 | Configuration Change Control | change-review, history-protection |
| CM-5 | Access Restrictions for Change | codeowners |
| CM-5(4) | Dual Authorization | change-review |
| CM-8 | System Component Inventory | dependency-management |
| IA-2(1) | Multi-factor Authentication to Privileged Accounts | org-two-factor |
| IA-5(7) | No Embedded Unencrypted Static Authenticators | secret-protection |
| PL-8 | Security and Privacy Architectures | security-design |
| RA-5 | Vulnerability Monitoring and Scanning | dependency-management, vulnerability-remediation |
| RA-5(11) | Public Disclosure Program | security-policy |
| SA-8 | Security and Privacy Engineering Principles | security-design |
| SA-10 | Developer Configuration Management | semantic-versioning |
| SA-10(1) | Software and Firmware Integrity Verification | release-integrity |
| SA-10(6) | Trusted Distribution | release-integrity |
| SA-11 | Developer Testing and Evaluation | contributing |
| SA-11(1) | Static Code Analysis | static-analysis |
| SA-11(4) | Manual Code Reviews | change-review |
| SA-17 | Developer Security and Privacy Architecture and Design | security-design |
| SA-22 | Unsupported System Components | archive-notice |
| SI-2 | Flaw Remediation | vulnerability-remediation |
| SR-4 | Provenance | release-integrity |
| AC-6(1) | Authorize Access to Security Functions | maintainers-match |
| AC-6(5) | Privileged Accounts | org-few-owners |

Also in the sources file, but cited by no policy: `CM-10(1)`, `CM-14`, `SI-7`, `AC-2`, `AC-2(3)`, `AC-2(7)`,
`AC-5`, `AC-6(7)`, `IR-7`, `PS-9`.
`CM-14` and `SI-7` are the consumer-side counterparts of `release-integrity`. `CM-10(1)` (open-source software)
is the consumer-side counterpart of `project-files`. The others are cited by items of the maintainer policy
([maintainer-policy.md](maintainer-policy.md), WP3), not by a policy file.

## ISO/IEC/IEEE 12207:2026, by clause

| Clause (title from the table of contents) | Used by |
|---|---|
| 6.3.5 Configuration management process | semantic-versioning |
| 6.4.4 System architecture definition process | security-design |
| 6.4.13 Maintenance process | dependency-management, vulnerability-remediation |
| 6.4.14 Disposal process | archive-notice |

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
- **Today** (`data/reports/license-report.yaml`): of 115 live, classified repositories, 77 are green and 38 red. The red
  ones are 32 with no license, 3 with a license GitHub can't recognize, and 3 with an off-list license
  (`architecture-based-risk-analysis` MPL-2.0, `enhancement-proposals` BSD-3-Clause, `oosem.github.io` CC0-1.0).

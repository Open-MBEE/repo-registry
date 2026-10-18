# Maintainer policy

> **PROVISIONAL** until the maintainers ratify it (WP0, maintainer approval 5, with the named maintainers). WP3 D-5.
> Every provision below is cross-checked against the OpenSSF backbone and our other references (see the table at the
> end).

## Who the maintainers are

1. **The maintainers are the people who govern OpenMBEE's GitHub organization.** They are named in
   [`data/maintainers.yaml`](../data/maintainers.yaml), and this repository's CODEOWNERS lists the same people.
2. **Every organization owner is a maintainer, but not every maintainer is an owner.** The owner role is held by two or
   three maintainers ([org-few-owners](sops/org-few-owners.md)). The others hold the narrower powers they need.
3. **Target size: five maintainers,** from more than one organization, so that governance survives any one person or
   employer leaving.
4. **Governance is held openly.** Each maintainer makes their organization membership public
   ([governance-roles-named](sops/governance-roles-named.md)). Until this policy is ratified, nobody is named against
   their choice, and anyone may step down instead.

## How maintainers are added and removed

5. **Adding:** any maintainer proposes a new maintainer by a pull request to `data/maintainers.yaml` that also updates
   CODEOWNERS. The other maintainers review and merge it. From R3, code-owner review is required (WP0).
6. **Stepping down:** a maintainer may step down at any time, by the same kind of pull request, and becomes emeritus.
   Emeritus maintainers are thanked in the list but hold no powers.
7. **Inactivity:** long inactivity is a reason to *ask* a maintainer whether they want to continue, never to remove
   them automatically. The registry records each named holder's last public activity as a hint.
8. **Review:** once a year, the maintainers review the list, who holds which powers, and how many organizations the
   maintainers come from.

## What powers maintainers get

9. **Least privilege.** Each maintainer gets only the powers their responsibilities need, granted through GitHub teams
   and repository roles rather than the owner role ([org-base-permission](sops/org-base-permission.md)).
10. **Two-factor authentication** is required for everyone in the organization ([org-two-factor](sops/org-two-factor.md)).
11. **Other powers are declared.** Any admin power over OpenMBEE held outside GitHub's owner role (installed apps,
    other platforms, the fiscal sponsor relationship) is declared in `data/maintainers.yaml`
    ([maintainers-match](sops/maintainers-match.md)).

## Release authority

12. **A tool's release authority is named.** For each tool in the incubating or graduated stage, a maintainer or a named
    release officer holds release authority. It is recorded as `release_authority` in `data/maintainers.yaml`, and that
    person is a code owner of the tool's repository.
13. **Release authority is credentialed before it is exercised.** The credentialing step (for example, an institution's
    approval to publish releases) is recorded as an attestation in the tool's repository. Jason Han's release
    authority for OpenSysML is the first case, with credentialing under way.
14. **Security response.** For graduated tools, the security policy names who triages and responds to vulnerability
    reports ([security-policy](sops/security-policy.md)).

## Cross-check against our references

| Provision | OpenSSF (backbone) | CNCF | CISA | NIST SP 800-53 | ISO/IEC/IEEE 12207 (clause) |
|---|---|---|---|---|---|
| 1 Maintainers named, CODEOWNERS match | Lifecycle: document the current list of maintainers (Incubating) | Graduation: complete maintainer list; "code and doc ownership in GitHub and elsewhere matches documented governance roles" | C4 Community: number of maintainers | AC-2, PS-9 | 6.2.4 |
| 2 Owners are 2 or 3 maintainers | Baseline TI-3: 2 to 3 organization owners, and the same for repository admins | — | — | AC-6(5), AC-2(7) | — |
| 3 Five maintainers from more than one organization | Lifecycle: 3 maintainers from 2 organizations (Incubating); 5 from 3 (Graduated) | Graduation: maintainers from at least 2 organizations; an org-balance mechanism | C4 Community: maintainer affiliation | — | — |
| 4 Governance held openly | Lifecycle: documented governance (Incubating), shown in action (Graduated) | Graduation: clear, discoverable governance documentation | C4 Conduct | — | — |
| 5–6 Adding, stepping down, emeritus | Lifecycle: contributor guide with a path to maintainership (Incubating) | Graduation: a complete maintainer lifecycle (onboarding, offboarding, emeritus), with evidence | — | AC-2 | 6.2.4 |
| 7 Inactivity asks, never removes | Lifecycle (for projects): dormancy makes a candidate for review, decided by vote | Archiving (for projects): inactivity triggers review, decided by vote | C4 re-evaluation | AC-2(3) *(not adopted: no automatic disabling)* | — |
| 8 Annual review | Baseline TI-3: owners audit member and token permissions periodically | Graduation: annual governance health check on maintainer organizational composition | — | AC-6(7) | 6.2.1 |
| 9 Least privilege through teams | Baseline TI-3: least privilege; manage permissions through teams | — | — | AC-6, AC-5 | — |
| 10 Two-factor authentication | Baseline SB-2 | — | — | IA-2(1) | — |
| 11 Other powers declared | Baseline TI-3: minimal permissions for credentials and apps | Graduation: ownership "in GitHub and elsewhere" matches governance roles | — | AC-2 | — |
| 12 Named release authority | Lifecycle: declared release practices (Graduated) | Graduation: documented roles for sub-teams | Release marking; SBOM per release | AC-5, SA-10 | 6.3.5 |
| 13 Credentialed before exercised | — | — | — | AC-2, PS-9 | 6.2.4 |
| 14 Named security response | Baseline OI-3; Lifecycle: vulnerability point of contact | Graduation: documented security-response roles | VDP and security contact | RA-5(11), IR-7 | — |

Sources: OpenSSF `ossf/tac` (lifecycle at d019efe, security baseline at 098faba); CNCF `cncf/toc` (lifecycle at
d815451, graduation criteria at 6119a69); CISA *Open Source Software: Security Principles and Practices*
(`data/sources/cisa-practices.yaml`); NIST SP 800-53 Rev. 5 (`data/sources/nist-800-53.yaml`); ISO/IEC/IEEE
12207:2026, clause numbers only.

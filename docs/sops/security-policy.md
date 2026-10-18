# Vulnerability reporting

> **PROVISIONAL** until the maintainers approve the policies. Policy `security-policy` (`data/policies/security-policy.yaml`).

Tools from version 1.0, and the registry, publish a security policy that says how to report a vulnerability and who responds, and turn on GitHub's private vulnerability reporting.

**Applies to:** tool at incubating, tool at graduated, governance at incubating (nothing yet), governance at graduated (the administration of the Open-MBEE GitHub organization, and repo-registry once it is accepted as the canonical source). Your repository's type and stage are in [registry.yaml](../../registry.yaml); the stages are explained in [lifecycle-stage-map.md](../lifecycle-stage-map.md), and the full table is in [policy-applicability.md](../policy-applicability.md).

## Set up

1. Add `SECURITY.md` (at the root, in `.github/` or in `docs/`) saying how to report a vulnerability and who responds.
2. Go to Settings, then Advanced Security, and turn on Private vulnerability reporting.
3. Say in the policy what reporters can expect, including for automated or AI-assisted reports.
4. Record the attestation below.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **security-policy-present**: `GraphQL repository { isSecurityPolicyEnabled } == true` (needs Metadata: read)
- **private-reporting-on**: `GET /repos/{owner}/{repo}/private-vulnerability-reporting -> enabled == true` (needs Metadata: read)

## Attested checks

- **disclosure-followed**: Reports are answered following the published process, which also says what to expect for automated or AI-assisted reports.

How to attest: add this entry to your repository's `ATTESTATIONS.yaml`, at its root, and renew it for each release
([attestations-format.md](../attestations-format.md)). An entry counts only if its `release` names the release being
checked (or `none` before the first release), and the last change to the file was committed by a code owner of the repository. Point to
the file from the README: "Attestations: see `ATTESTATIONS.yaml`."

```yaml
attestations:
  - policy: security-policy
    check: disclosure-followed
    attested_by: your-github-username
    date: YYYY-MM-DD
    release: vX.Y.Z           # the release this is made for, or none if there is no release yet
```


## Why

- CISA: CISA-P-SECURITY-MD, CISA-P-VDP-BOD, CISA-P-VDP-AI-REPORTS, CISA-P-SECURITY-CONTACT (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: RA-5(11) (see `data/sources/nist-800-53.yaml`)
- OpenSSF security baseline: OI-3 (see `data/sources/openssf-security-baseline.yaml`)

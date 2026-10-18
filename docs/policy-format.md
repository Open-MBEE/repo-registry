# Policy format

> **PROVISIONAL** until the maintainers approve the policies (WP0, maintainer approval 2). WP2 D-4.

Each policy is one YAML file in `data/policies/`, named after its id, with a plain-language SOP in `docs/sops/`.
`scripts/policies.py` checks every meta-rule below, then generates the applicability table
([policy-applicability.md](policy-applicability.md)). WP5 runs the same check in CI, so an invalid policy can't reach
`main`. A repository being out of compliance with a policy is still a **valid** state.

## Shape

```yaml
status: provisional                      # provisional | approved
provisional_until: "WP0 maintainer approval 2: the policies"
id: secret-protection                    # equals the file name
name: Block secrets from being pushed    # short, plain
meaning: >-                              # one or two plain sentences, for anyone
  ...
applies_if:                              # a rule on type, lifecycle and tier only (WP0 A1)
  any:
    - all: [{attr: type, eq: tool}, {attr: lifecycle, in: [incubating, graduated]}]
github:
  mechanism: Secret scanning push protection (repository security settings)
  docs: [https://docs.github.com/...]
  available_on: [free, team, enterprise]  # GitHub plans that provide the mechanism
  needs_research: [...]                   # optional: features whose availability isn't confirmed yet
checks:
  automated:                             # what the registry reads, and the permission it needs
    - {id: push-protection-on, reads: "GET /repos/{owner}/{repo} -> ...", permission: "Administration: read"}
  attested:                              # what a code owner states, in the repository's ATTESTATIONS.yaml
    - {id: ..., statement: ...}
cites:
  cisa: [CISA-P-SECRET-DETECT]           # or "none"
  nist: [IA-5(7)]                        # or "none"
  openssf: [TI-2]                        # OpenSSF security-baseline items this policy adopts
  iso12207: ["6.4.13"]                   # clause numbers only, never text
secondary_notes: ...                     # optional: CNCF or OpenSSF lifecycle expectations
sop: docs/sops/secret-protection.md
```

One policy, `license-by-type`, also carries `allowed_licenses`: for each type, the SPDX identifiers it accepts.
`scripts/licenses.py` reads it, and `tests/test_wp2a.py` checks that it has an entry for every type in the taxonomy
(WP2a R-3).

`applies_if` uses the predicate language of `data/taxonomy/kinds.yaml` (`all`, `any`, `not`, and `attr` with `eq` or
`in`), over exactly three attributes of a kind: `type`, `lifecycle` and `tier`.

## Meta-rules

1. **One file per policy.** `id` equals the file name and is lower-case words joined by hyphens.
2. **Every field is present:** `status`, `id`, `name`, `meaning`, `applies_if`, `github`, `checks`, `cites`, `sop`.
3. **Provisional is marked.** `provisional_until` is present exactly when `status` is `provisional`.
4. **Applies-if reads only type, lifecycle and tier,** and names only values that exist in the taxonomy. It uses no
   signals.
5. **GitHub-native.** `github` names the mechanism (or says it is attested because GitHub has no setting for it) and
   links at least one GitHub documentation page.
6. **Checks.** There is at least one check. Each automated check has an `id`, the exact `reads` (endpoint and field)
   and the `permission` it needs. Each attested check has an `id` and a `statement`.
7. **Core citations.** `cites.cisa` and `cites.nist` are present: either a list of IDs that exist in
   `data/sources/cisa-practices.yaml` and `data/sources/nist-800-53.yaml`, or `"none"`. `cites.openssf` is present
   too, the third core citation (WP4c): a list of OpenSSF security-baseline items, empty when the policy adopts none.
8. **OpenSSF baseline coverage.** Every item in `data/sources/openssf-security-baseline.yaml` is adopted by at least
   one policy (`cites.openssf`) or listed in `data/policies/_departures.yaml` with a reason, but not both.
9. **CISA coverage.** Every practice in `data/sources/cisa-practices.yaml` is cited by at least one policy or listed in
   `_departures.yaml` with a reason, but not both.
10. **ISO by reference only.** `cites.iso12207` holds clause numbers only. No text from the standard is committed.
11. **SOP.** The file at `sop` exists and has the three sections `## Set up`, `## Automated checks` and
    `## Attested checks`.
12. **The org's plan.** `github.available_on` includes the org's plan (`plan` in `data/sources/github-plan.yaml`,
    today `free`). A feature the plan lacks belongs in `data/policies/_future.yaml` `features`, never in a policy
    (WP3 G-3).
13. **Unconfirmed features are listed.** Every feature named in `github.needs_research` is listed under
    `needs_research` in `data/policies/_future.yaml` (empty today: immutable releases and rulesets are confirmed for
    the org, see `confirmed_in_org` in `github-plan.yaml`; WP3 G-3 follow-ups).

## Reading a check's result

- An automated check that the registry's credential can't read is **yellow** (can't tell), never "off". Several GitHub
  endpoints return 404 both for "off" and for "you may not see this", so the checker needs *Administration: read*.
- An attested check is answered in the repository's `ATTESTATIONS.yaml` ([attestations-format.md](attestations-format.md);
  WP4d). The registry reads the file at one commit: the commit of the latest release's tag (published, not a draft or
  pre-release), or, for a repository with no release, the latest commit on the default branch. An archived
  repository is read at its final commit on the default branch, whatever its releases, since its last attestation
  is made just before it is archived (WP4d review, G-1). Then:
  - **green:** the file has one entry for the policy and check, its `release` names that release (or is `none` when
    there is no release; for an archived repository, any value), and the last commit that changed the file, up to that commit, was made by a code owner of
    the repository at that commit. With no release, the entry doesn't go out of date.
  - **red:** there is a release but its commit has no such entry, or the entry names another release; the entry is
    missing; the file doesn't meet its schema; or the last change to the file wasn't made by a code owner. A
    required attestation that is missing or out of date is non-conformant (WP0 R-13).
  - **yellow:** the file, the release, the commit history or the CODEOWNERS can't be read, so the registry can't tell.
  - An accepted exception (`data/deviations.yaml`) is green, marked as an exception, as for any check.
- A repository archived before the archive policy existed passes `archive-notice` as it is.

# Requirements — policy

> **DRAFT.** Nothing here is locked until mzargham says "lock." Columns and sources are defined in
> [design.md](../design.md#requirement-conventions).
>
> Brought in line with the decision records at the WP4b docs sweep (2026-10-18); each changed requirement says
> "(updated: <record>)". The consistent summary is [current-state.md](../current-state.md).

The policy is the reference. It is a set of named policies. Each states an applies-if rule on a repo's type,
lifecycle stage or tier, and references a GitHub-native configuration; a policy is a region of the (type, stage,
tier) space, and a repo's policies are the regions its kind falls in *(updated: WP0 A1)*. Policies are defined and
referenced here. They are configured and enforced in GitHub.

| ID | Requirement | Src | Assessed by |
|---|---|---|---|
| PO-1 | Each policy is a named file with an applies-if rule on type, lifecycle stage or tier, its GitHub configuration, its citations and an SOP. There is no per-kind value table and no automatic correction channel; gaps go out as change requests *(updated: WP0 A1, R-16; Tension 3)*. | M | Schema check |
| PO-2 | Strictness follows the tier, which is set by type × stage: high for graduated tools and governance, medium for incubating tools and incubating or graduated media (media tops out at medium), low for sandbox tools, sandbox media and all research, none for archived repos *(updated: A4; `data/taxonomy/kinds.yaml`)*. | M, S | Side-by-side table of policies ([policy-applicability](../policy-applicability.md)) |
| PO-3 | Every repo in a tier that needs an owner (high, medium, low) has its operators named in its CODEOWNERS. Release authority for incubating and graduated tools is recorded as `release_authority` in `data/maintainers.yaml` *(updated: WP0 R-17; A4; maintainer-policy item 12)*. | M | Schema check |
| PO-4 | Every policy cites the CISA practice and the RMF task or SP 800-53 control it serves (section and page), or says "none", plus any secondary sources *(updated: WP0 R-16; WP0-decisions "NIST RMF as a second core citation")*. | M, C | Traceability table ([policy-basis-review](../policy-basis-review.md)) |
| PO-5 | Each kind's wiki page states, in plain language, generated from the taxonomy plus the policy: what puts a repo here, what we assert, and who is responsible *(updated: WP0 terminology)*. | M | Pages regenerate identically |
| PO-6 | **Policies are defined and referenced, not reimplemented.** Each control is a GitHub-native configuration (for example a ruleset, branch protection, required reviews, CODEOWNERS, a security setting, or a required file). It is configured in GitHub, and the policy here references it. | M | Every control in the policy names its GitHub-native mechanism |
| PO-7 | **Conformance means "in effect".** For each repo, the loop checks that the configurations of the policies in effect for it are in effect on that repo. A configuration that is missing or not applied is red. One the sensor can't read is yellow ("can't tell") *(updated: WP0 R-13)*. | M | Fixture repos with a configuration present, absent and unreadable |
| PO-8 | **Deviations.** A justified exception to one policy on one repo is recorded in this repo by a PR that an owner merges, with a reason and the approver (a GitHub username via the PR approval) *(updated: WP4b OD3)*. It doesn't expire and can be reviewed at any time. Its status is green, visibly marked as an accepted exception, in the wiki views *(updated: WP0 R-13, D-3)*. It is never hidden as plain green. | M | Fixture with a deviation; it shows, marked, in the views |
| PO-9 | **Operators are the repo's CODEOWNERS.** A repo's operators are its CODEOWNERS, sensed from the repo, whose CODEOWNERS file is the authoritative source. Wherever the tier needs an owner (high, medium, low), a repo with no CODEOWNERS is red, and only a CODEOWNER's attestation counts *(updated: WP0 R-17; WP0-decisions "Sweep gap 1")*. | M | Fixture repos where CODEOWNERS is present and missing |
| PO-10 | **Friction is explicit, not universal.** Each kind's page states both the policies in effect and, plainly, the policies that are not. No policy applies to a repo unless its applies-if rule covers the repo's kind. The wiki views show each repo's status with links to the repo and its open registry issues, so the friction in effect is confirmed and documented; there is no page per repo *(updated: WP0 A1, D-3, R-18)*. | M | Kind pages list policies in effect and not in effect; each view traces a repo's status to the policies |

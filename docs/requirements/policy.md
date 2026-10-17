# Requirements — policy

> **DRAFT.** Nothing here is locked until mzargham says "lock." Columns and sources are defined in
> [design.md](../design.md#requirement-conventions).

The policy is the reference. For each class it gives the assigned values, which are references to GitHub-native
configurations, and a correction channel for each constrained attribute. Policies are defined and referenced here.
They are configured and enforced in GitHub.

| ID | Requirement | Src | Assessed by |
|---|---|---|---|
| PO-1 | For each class: assigned values in `U` and a correction channel for each constrained attribute. | M | Schema check |
| PO-2 | Strictness: tool > media > research. | M, S | Side-by-side table of controls |
| PO-3 | Every non-archived class assigns an owner. Tool classes in active development or maintenance also assign a release officer. | M | Schema check |
| PO-4 | Every control cites the CISA practice or C4 criterion it serves (section and page), or says "none". | M, C | Traceability table |
| PO-5 | Each class's wiki page states, in plain language, generated from the taxonomy plus the policy: what puts a repo here, what we assert, and who is responsible. | M | Pages regenerate identically |
| PO-6 | **Policies are defined and referenced, not reimplemented.** Each control is a GitHub-native configuration (for example a ruleset, branch protection, required reviews, CODEOWNERS, a security setting, or a required file). It is configured in GitHub, and the policy here references it. | M | Every control in the policy names its GitHub-native mechanism |
| PO-7 | **Conformance means "in effect".** For each repo, the loop checks that the configurations its class references are in effect on that repo. A configuration that is missing or not applied is a `violation`. One the sensor can't read is `unknown`. | M | Fixture repos with a configuration present, absent and unreadable |
| PO-8 | **Deviations.** A justified exception to one control on one repo is recorded in this repo by governors, with a reason and the approver (a GitHub username via the PR approval). It doesn't expire and can be reviewed at any time. Its verdict is `deviation`, shown on the repo's wiki page. It is never hidden as `ok`. | M | Fixture with a deviation; it shows on the wiki page |
| PO-9 | **Operators are CODEOWNERS where the class requires it.** A class can require that a repo's named operators (its owner and, where assigned, its release officer) are listed in that repo's CODEOWNERS. This is expected at least for the stricter classes. Which classes require it is set per class. The loop checks the match. | M | Fixture repos where CODEOWNERS matches, differs and is missing |
| PO-10 | **Friction is explicit, not universal.** Each class states both the controls it requires and, plainly, the controls it does not require. No control applies to a repo unless its class's policy names it. Each repo's wiki page shows every prescribed control with its verdict and evidence, so the friction in effect is confirmed and documented. | M | Class pages list required and not-required controls; a repo page traces each control to the policy |

# WP4e — Decision records

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's. The scope document carries only the outcomes ([WP4e-scope-of-work.md](WP4e-scope-of-work.md)).

## Why this package exists

- **Supervisor (mzargham, typed by agent):** "i actually have another concern before push. looking at our registry
  yaml schema it seems strange to me that we're using slash to make kind out of the repo type and lifecycle stage.
  this should be type and stage. we can compute kind from it where we need to"
- **Question:** Where should it be scoped? (Options: separate package / fold into WP5.)
- **Answer (mzargham, typed by agent):** "Separate package"
- **Outcome:** WP4e, on `main`. WP5 waits on `wp5-work` (d7686e5, `main` merged in after WP4d) until it is accepted.

## OD1 — The name of the stage attribute

- **Question:** What should the stage attribute be called? The kind list would say `stage`, but the taxonomy, the
  policies' applies-if rules and the code call it `lifecycle`. (Options: stage everywhere / stage in kind list only.)
- **Answer (mzargham, typed by agent):** "the full description is stage of the lifecycle. use stage, lifecycle or
  state in the lifecycle as appropriate"
- **Follow-up:** To confirm: the attribute in the data and code is named `stage` everywhere, and the prose says
  "stage", "the lifecycle" or "stage in the lifecycle" as fits?
- **Answer (mzargham, typed by agent):** "Yes"
- **Outcome:** The attribute is `stage` everywhere in the data and code. D-2 and R-6 cover the rename.

## OD2 — A repository the rules can't classify

- **Question:** How should the kind list record a repository the rules can't classify? (Options: reason only /
  whatever is known.)
- **Answer (mzargham, typed by agent):** "Reason only"
- **Outcome:** An entry has either `type` and `stage`, or `reason` alone.

## OD3 — The Agent's defaults

- **Question:** Approve the Agent's defaults (kind names kept as computed labels; the org entry with type and stage;
  ordering; generated files show the computed kind; WP1-amendment-4.md; main merged into wp5-work again) as one item?
- **Answer (mzargham, typed by agent):** "Approve all"
- **Outcome:** Approved as written.

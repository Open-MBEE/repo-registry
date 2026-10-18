# WP5b — Decision records

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's. The scope document carries only the outcomes ([WP5b-scope-of-work.md](WP5b-scope-of-work.md)).

## Why this package exists

- **Supervisor (mzargham, typed by agent):** "i see other inconsistencies in how our registry works, we've seperated
  stage and type in the registry but we use kind (the combined name) in many other places. i made the change so we
  had two fields in our yaml but the inconsitency with the other yaml where it seems like kind (the combined one) is
  being used as a key. we need to do a serious audit for data and schema consistency, integrity, etc. this needs to
  be the next work package"
- **Ordering (recorded in WP5-decisions.md):** "After WP5".
- **Supervisor, asking for the scope (mzargham, typed by agent):** "i need to go to sleep. i will review and merge PR 1
  in the morning. in the mean time i need you to scope the work package that addresses the data consistency and
  integrity concerns i flagged about inconsistency keys, joins, etc across our yaml files. even though this is a git
  repo. for the purpose of this analysis let's treat it like a database"
- **Outcome:** Drafted while the supervisor was away. OD1 to OD4 are open, for the decision loop in the morning.

## The supervisor's framing: model, view, controller *(raised by the supervisor)*

- **Supervisor (mzargham, typed by agent):** "my goal now is to refine the taxonomy based on what we learned in the
  build so far. tighten it up so it can be functionally like a database even though its a collection of yaml files and
  markdown files with python based controls to force alignment with our world model and build views. one
  recommendation i'd like to make is that you think of this as a model view controller architecture. this is a
  distinct reading of the term control from our control theory formal model it emphasizes the software engineering
  pattern. MVC plus CI/CD allows us to treat the wiki and issues written as view planes (written as part of CD), the
  repo itself as the model (including asserting correctly constructed records and rejecting illformed ones via CI)."
- **Outcome:** The scope is written in MVC terms: the repository's records are the model, the Python is the
  controller, and the wiki, the issues and every generated document are views, rendered by CD only after CI passes.

## Answers to the walk-through (one message)

The agent walked through six recommendations; the supervisor answered them together:

- **1. One package or two:** "two packages". WP5b is the model and controller; WP5c is the taxonomy refinements.
- **2. Audit only, or audit plus fixes (OD1):** "ok" (to the recommendation: audit plus fixes, with a check-in where
  the supervisor disposes each finding before any fix).
- **3. The kind name (OD2):** "yes this is better database management; the combined name is shorthand; useful
  shorthand but shorthand nonetheless". Type and stage are stored and keyed everywhere; the name is derived, for
  display.
- **4. Repository identity (OD3):** "i like using the stronger key. plus our solution is tied to github so we should use
  its affordances". GitHub's numeric repository ID is the key; the name is a column.
- **5. Are views committed:** "views are not committed. they are generated; so we have the piping that produces them
  (writes issues, or doesn't write them because they are sensed as already present); generates and deploys the
  registry wiki. i view these each as CD steps that occur only if the CI passes. we prevent writing bad data to issues
  or to the wiki by ensuring those write processes are gated on the conformance checks and any other gates that ensure
  our internal model is right before we act on it. as long as the view / write pipelines are deterministic, those
  pipelines uniquely determine what views they output so we don't need to store the outputs locally"
- **6. Hand-written markdown that holds derived facts:** "remove handwritten markdown wherever possible. though i
  suspect we wont be able to get around it for part of the SOPs. though i am happy to programatically generate from
  schema compliant data wherever possible"
- **Process (feedback):** "in the future please bundle the status updates with the PRs so they don't lag one work
  package." The WP5 status update rides with this scope's PR.

## OD5 — Where people read the views before the wiki exists *(raised by OD4)*

- **Question:** With views no longer committed, where do people read them (the applicability table, pilot briefing,
  reports) until the wiki exists in WP7? (Options: CI artifact / wiki now / commit until WP7.)
- **Answer (mzargham, typed by agent):** "we need a toggle for demo mode that writes the views to an ephemerate
  directory specifically for showing what would be written to the wiki and what would be written to repos issue
  boards, if they were turned on. in controls terms we are simulating the plant to test the controller before we turn
  the thing on. i we cannot approve turning this system on if we cannot test how it will behave and approve that
  behaviore"
- **Outcome:** The render pipeline gets a mode toggle. Demo mode writes every view to an ephemeral directory; it is the
  only mode in WP5b. Live mode (writing the wiki and issues) comes with WP6 and WP7, gated on CI and an explicit switch.

## OD6 — The pilot list *(raised by OD4)*

- **Question:** The pilot list (data/pilot.yaml, data/exclude.yaml) is generated, but it's what the maintainers
  approve (WP0 approval 3). Is it a view or a model table? (Options: a view / a model table.)
- **Answer (mzargham, typed by agent):** "A model table"
- **Outcome:** The pilot list and exclude list are model tables, written once by the rule and then kept; what the rule
  would propose today is a view.

## OD7 — The Agent's defaults

- **Question:** Approve the Agent's defaults (repository IDs read once into the snapshot and keyed everywhere; the
  pilot list keyed by ID with no stored kind; `render.py --mode demo` into `build/demo/`, a CI artifact and the view
  diff in the job summary; SOPs generated from the policy YAML with hand-written templates; the audit checklist;
  PyYAML only; one PR per step with its status update) as one item?
- **Answer (mzargham, typed by agent):** "Approve all"
- **Outcome:** Approved as written.

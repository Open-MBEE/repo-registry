# WP5c — Decision records (gathered before the scope)

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's. WP5c (the taxonomy refinements from WP4's fit analysis) is scoped after WP5b; these answers were given
early, while WP5b was being scoped.

- **Packaging:** "two packages" (WP5b the model and controller; WP5c the taxonomy).
- **1. Forks:** "assess whether forks are research. my gut is they are explorations of integration points. covering how
  tools work together or don't. they could also be media if they are primarily works of models rather than forks of
  tools. its probably worth inspecting the upstream, and our diff from the upstream to help classify"
- **2. Topics:** "introduce github topics as a means of declaring type. can a repo have more than one topic? i do like
  using topic to label research, media and tool distinction."
- **3. Signals and precedence:** "yes examples are good check terms, but i think they could appear as either media or
  research depending on whether the purpose of doing it to learn for ourselves or communicate to others. i think its
  worth keeping it clear that the initial tag up of the repos is provisional and the inference produces a candidate
  not a decision. tagging repos using topics should supersede inference. so the order of priority is
  inferred->topic->maintainer merged commit."
- **4. Archived with no type:** "ok"
- **5. `.github` as governance:** "yes"

## Scoping (after WP5b)

- **Supervisor (mzargham, typed by agent):** "ready" (to scope WP5c).

## OD1 — Where the precedence lives

- **Question:** Where should the precedence (inferred → topic → maintainer-merged commit) live? (Options: decisions
  only / source per entry.)
- **Answer (mzargham, typed by agent):** "Source per entry"
- **Outcome:** Every kind-list entry carries a `source` (inferred, topic, maintainer). Only a maintainer's merged change
  sets `maintainer`; rules and topics never change such an entry.

## OD2 — A fork with no commits of ours

- **Question:** A fork the assessment finds with no commits of ours ahead of its upstream (a plain copy). How is it
  classified? (Options: excluded mirror / research / archive candidate.)
- **Answer (mzargham, typed by agent):** "Excluded mirror"
- **Outcome:** Unclassified, with the reason that it is a copy with no changes of ours, and excluded from the pilot
  with that reason. A fork with our changes is research, or media where our changes are mostly models (the
  supervisor's first answer).

## OD3 — An archived repository with no type signal

- **Question:** How should an archived repository with no type signal (6 today) be classified? (Options:
  tool/archived / new untyped kind / stay unclassified.)
- **Answer (mzargham, typed by agent):** "Stay unclassified"
- **Outcome:** They stay unclassified with their reason. This replaces the earlier "ok" to WP4's recommendation 4.

## OD4 — `.github`'s stage

- **Question:** As governance, what stage is the org's `.github` repository (its profile and default community
  files)? (Options: graduated / sandbox.)
- **Answer (mzargham, typed by agent):** "Graduated"
- **Outcome:** governance/graduated, recorded as a maintainer decision.

## OD5 — The Agent's defaults

- **Question:** Approve the Agent's defaults (one `openmbee-<type>` topic per type, none or several declaring nothing;
  "example" alone deciding no type; a refresh view for inferred and topic entries; one read-only compare per fork into
  `forks.json`; Python's patch release pinned; one PR per step with its status) as one item?
- **Answer (mzargham, typed by agent):** "Approve all"
- **Outcome:** Approved as written.

# WP5 — Decision records

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's. The scope document carries only the outcomes ([WP5-scope-of-work.md](WP5-scope-of-work.md)).

## OD1 — The history before the push

- **Question and answer:** withheld from this record at the supervisor's request.
- **Outcome:** The history is published as is.

## OD2 — Moot after OD1

- **Question and answer:** withheld with OD1. The supervisor's answer was "Drop OD2".
- **Outcome:** Dropped. The existing tests run in CI unchanged.

## OD3 — The gate after the move

- **Question:** Once `main` requires the check, it takes changes only through pull requests. After the move, how
  are approval and acceptance recorded? (Options: PR merge, no bypass / PR merge, owner bypass / local merge, bypass.)
- **Answer (mzargham, typed by agent):** "PR merge, no bypass"
- **Outcome:** Approval and acceptance become mzargham's merge of a PR with a merge commit. The ruleset on `main`
  has no bypass list. WP5's own acceptance is the merge of its delivery PR on GitHub.

## OD4 — Who runs the writes to the org

- **Question:** Who runs the writes to the live org: creating the repository, the push, and the ruleset? (Options:
  "You run them": the agent hands mzargham the exact commands and he runs them / "Agent runs them": the agent runs
  them with gh after his go-ahead in chat, one step at a time.)
- **Answer (mzargham, typed by agent):** "You run them"
- **Outcome:** mzargham runs every org write himself, from exact commands the agent hands him. The agent writes
  nothing to the org.

## OD5 — Clone counts in the usage snapshot

- **Question:** The usage snapshot holds 14-day clone counts that only people with push access can see, and the
  pilot rule uses them. Moving makes them public. What should happen to them? (Options: publish as is / drop clone
  counts / ask maintainers first.)
- **Answer (mzargham, typed by agent):** "Publish as is"
- **Outcome:** Published with the rest of the snapshot. The pilot is unchanged.

## OD6 — The sensing credential (XF-1)

- **Question:** XF-1 is the sensing credential with "Administration: read". `data/expected-gaps.yaml` says it is set
  up with the move in WP5, and WP6 is where it is first used. Where does setting it up belong? (Options: WP6 / WP5,
  with the move.)
- **Answer (mzargham, typed by agent):** "WP6"
- **Outcome:** The setup is a non-goal here. D-6 corrects XF-1's `closes_in` note.

## OD7 — The Agent's defaults

- **Question:** Approve the Agent's defaults (public visibility, file names, push `main` only, settings, pinned
  read-only actions, the generated-file comparison's coverage, the local privacy check and kept history-scan script)
  as one item?
- **Answer (mzargham, typed by agent):** "Approve all"
- **Outcome:** Approved as written.

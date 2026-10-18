# WP4d — Decision records

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's. The scope document carries only the outcomes ([WP4d-scope-of-work.md](WP4d-scope-of-work.md)).

## Why this package exists

- **Supervisor (mzargham, typed by agent):** "one more change i want to make that needs to land before we ship to
  open-mbee (wp5). \"If it asks you a question (a fact the system can't see for itself), answer it in an attestation
  block in your repository's `README.md`, committed by a code owner. The policy's SOP shows the form. An attestation is
  out of date once it is older than your latest release.\" this feels sloppy and a bit confusing i think we need a
  seperate attestations file, reserved filename in root and simply have a pointer to it in the readme,md. it can even
  be yaml instead of markdown to improve the ability to check that the required attestations are fresh. we need a way
  to bind the attestations file to the release commit so a release always comes with attestations bound to it rather
  than a potentially stale file"
- **Packaging:** "Separate package" (recorded in `WP4c-decisions.md`, on the `wp4c-scope` branch until WP4c is approved).

## OD1 — What binds an attestation to a release

- **Question:** What binds an attestation to a release? (Options: in the release commit / named per release.)
- **Answer (mzargham, typed by agent):** "Named per release"
- **Outcome:** An entry counts for a release only if it is in `ATTESTATIONS.yaml` at the release's commit, was
  committed by a code owner, and names that release. Every release is attested afresh.

## OD2 — A repository with attested checks but no release

- **Question:** A repository has attested checks but no release (live media, archived repositories, the org). What
  counts for it? (Options: default branch, no expiry / default branch, expires / release required.)
- **Answer (mzargham, typed by agent):** "Default branch, no expiry"
- **Outcome:** With no release, the file on the default branch counts and doesn't go out of date. Its entries name
  the release as `none`.

## OD3 — What WP4d builds beyond the specification

- **Question:** What should WP4d build beyond the specification? (Options: specification only / also an offline
  checker.)
- **Answer (mzargham, typed by agent):** "Specification only"
- **Outcome:** WP4d delivers the format, schema, rule and SOPs. The checker is WP6's; D-5 is dropped.

## OD4 — The Agent's defaults

- **Question:** Approve the Agent's defaults (ATTESTATIONS.yaml and its format and schema, the entry fields, the
  committer read from git, the README pointer as a recommendation, the org's attestations in this repository, the
  binding through GitHub's release, tag and commit) as one item?
- **Answer (mzargham, typed by agent):** "Approve all"
- **Outcome:** Approved as written.

## Acceptance review — G-1, archived repositories with releases

- **Question:** archive-notice asks for an attestation in the last commit before archiving, which usually comes after
  the last release, but the rule read the file at the latest release's commit, so a repository with releases archived
  later would stay red unless it cut a final release. How should this be handled? (Options: fix before acceptance /
  follow-up package / accept as is.)
- **Answer (mzargham, typed by agent):** "Fix before acceptance"
- **Outcome:** Fixed under the same scope: an archived repository is read at its final commit on the default branch,
  whatever its releases (`docs/policy-format.md`, `docs/attestations-format.md`, the archive-notice SOP, WP0
  amendment 3). The whole review is rerun.

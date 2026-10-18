# WP0 — Amendment 3: the attestations file

Made by [WP4d](WP4d-scope-of-work.md), approved by mzargham's merge e8d085e. Decisions are recorded verbatim in
[WP4d-decisions.md](WP4d-decisions.md). WP0's earlier amendments were A1 to A4; this record says what WP0 said
about attestations and what replaces it.

## What WP0 said

- The direction item "Compliance": "Attestations live in the operator's own repo, for example as a trailer in its
  README filled from a template, so they keep up with releases."
- R-13's default: "an attestation is out of date once it is older than the repo's latest release."
- From these, each SOP showed a Markdown comment block to add to the end of the README.

## Why it changes

The supervisor: "this feels sloppy and a bit confusing i think we need a seperate attestations file, reserved
filename in root and simply have a pointer to it in the readme,md. it can even be yaml instead of markdown to improve
the ability to check that the required attestations are fresh. we need a way to bind the attestations file to the
release commit so a release always comes with attestations bound to it rather than a potentially stale file".

## What replaces it

- **One file:** `ATTESTATIONS.yaml` at the root of the repository, in YAML, with a schema
  (`data/schema/attestations.schema.yaml`), and a pointer from the README, which is recommended, not checked.
  The format is [attestations-format.md](../docs/attestations-format.md).
- **Bound to the release:** the file is read as it is at the commit the latest release's tag names. That is GitHub's
  own binding; nothing is added to the release.
- **Named per release (WP4d OD1):** an entry counts for a release only if its `release` names that release, so every
  release is attested afresh.
- **No release (WP4d OD2):** the file on the default branch counts, with `release: none`, and doesn't go out of date.
- **Archived (WP4d review, G-1):** an archived repository is read at its final commit on the default branch, whatever
  its releases, because its last attestation is made just before it is archived.
- **Who:** an entry counts only if the last commit that changed the file, up to the commit read, was made by a code
  owner (WP0 R-17, unchanged). Who committed is read from git.
- **The org:** its attested checks are answered in this repository's `ATTESTATIONS.yaml`.
- The colors are in [policy-format.md](../docs/policy-format.md), "Reading a check's result". The checker is built in
  WP6 (WP4d OD3).

## Updated

WP0's "Compliance" item and R-13 default (amended in place, with a marker); the 10 SOPs with attested checks;
`docs/policy-format.md`; README (operator section); `docs/current-state.md`; the DRAFT `docs/design.md`,
`docs/requirements/interfaces.md` and `docs/testing-and-demonstration.md` (edited in place, as WP4b OD1).

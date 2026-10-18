# Status

*Updated 2026-10-18, with the WP5d scope (status updates ride with each package's PRs). Update this at each acceptance gate.*

Start with [current-state.md](current-state.md): what is decided, where it is recorded, and what is next.

## Where we are

- **Design:** the contract is [WP0](../work-packages/WP0-scope-of-work.md), the project scope through R1, approved
  in 1dccb62 and amended twice (3c72b7d, 3edae32), with the later work-package scopes and decision records. The early
  design documents (`design.md`, `roadmap.md`, `testing-and-demonstration.md`, `requirements/`) are DRAFT inputs,
  brought in line with the decisions by WP4b (they stay DRAFT). The other documents in `docs/` are PROVISIONAL deliverables of
  accepted packages, waiting for the maintainers' approval.
- **Work packages:**
  - **WP0** (project scope through R1): approved.
  - **WP1** (kinds and tiers): accepted in bcb1e73. Review: [WP1-review.md](../work-packages/WP1-review.md).
  - **WP2** (policies): accepted in 1ced09b. Review: [WP2-review.md](../work-packages/WP2-review.md).
  - **WP3** (org governance): accepted in 3c0ba20. Review: [WP3-review.md](../work-packages/WP3-review.md).
  - **WP2a** (license by type, a supplement to WP2): accepted in 61a3db6. Review:
    [WP2a-review.md](../work-packages/WP2a-review.md).
  - **WP4** (fit analysis and pilot): accepted in 1408259. Review: [WP4-review.md](../work-packages/WP4-review.md).
  - **WP4b** (docs sweep and checkpoint): accepted in 3f2c557. Review:
    [WP4b-review.md](../work-packages/WP4b-review.md); drift report:
    [WP4b-drift-report.md](../work-packages/WP4b-drift-report.md).
  - **WP4c** (the governance kinds, and OpenSSF as a core citation): accepted in 4cad812. Review:
    [WP4c-review.md](../work-packages/WP4c-review.md); the change is recorded in
    [WP1-amendment-3.md](../work-packages/WP1-amendment-3.md).
  - **WP4d** (the attestations file): accepted in caaca38. Review:
    [WP4d-review.md](../work-packages/WP4d-review.md); the change is recorded in [WP0-amendment-3.md](../work-packages/WP0-amendment-3.md).
  - **WP4e** (type and stage in the kind list): accepted in 63e270f. Review:
    [WP4e-review.md](../work-packages/WP4e-review.md); the change is recorded in [WP1-amendment-4.md](../work-packages/WP1-amendment-4.md).
  - **WP5** (meta-rule checks in CI, and the move to Open-MBEE): accepted by mzargham's merge of
    [#1](https://github.com/Open-MBEE/repo-registry/pull/1), 6938aa5. Review:
    [WP5-review.md](../work-packages/WP5-review.md); the move is recorded in [WP5-move-record.md](../work-packages/WP5-move-record.md).
  - **WP5b** (the model, its integrity, and views out of the model): accepted by mzargham's merge of
    [#6](https://github.com/Open-MBEE/repo-registry/pull/6), 9e14099 ([WP5b-scope-of-work.md](../work-packages/WP5b-scope-of-work.md)). Audit: [WP5b-audit.md](../work-packages/WP5b-audit.md); review: [WP5b-review.md](../work-packages/WP5b-review.md).
  - **WP5c** (the taxonomy refinements from WP4's fit analysis): accepted by mzargham's merge of
    [#9](https://github.com/Open-MBEE/repo-registry/pull/9), 42ecec0 ([WP5c-scope-of-work.md](../work-packages/WP5c-scope-of-work.md)).
    Review: [WP5c-review.md](../work-packages/WP5c-review.md). The change is recorded in [WP1-amendment-6.md](../work-packages/WP1-amendment-6.md).
  - **WP5d** (the maintainer review pack, published to the wiki): accepted by mzargham's merge of
    [#11](https://github.com/Open-MBEE/repo-registry/pull/11), c0d8979
    ([WP5d-scope-of-work.md](../work-packages/WP5d-scope-of-work.md)). Review: [WP5d-review.md](../work-packages/WP5d-review.md).
  - **WP5e** (verified code owners for high-tier repositories; every source quoted verbatim): scope approved by the
    supervisor's statement ([WP5e-decisions.md](../work-packages/WP5e-decisions.md) "Approval"); the scope and the
    work reach `main` together, in its delivery pull request ([WP5e-scope-of-work.md](../work-packages/WP5e-scope-of-work.md)).
  - **WP6 to WP8:** planned (see the breakdown below), not yet scoped.
- **Model (all PROVISIONAL until the maintainers approve it):** the repository's records, declared as tables in
  [data/schema/model.yaml](../data/schema/model.yaml) (WP5b): the stored snapshot of the org's public repositories
  (keyed by GitHub's repository ID); the taxonomy (types, stages adopted from CNCF and OpenSSF, tiers, kinds keyed by
  type and stage); the kind list (`registry.yaml`); the policies (`data/policies/`, the set's status in `_set.yaml`),
  grounded in [policy-basis-review.md](policy-basis-review.md) (CISA, NIST and OpenSSF core; CNCF and
  ISO/IEC/IEEE 12207 secondary); the named maintainers (keyed by GitHub user ID), the proposed CODEOWNERS and the
  maintainer policy ([maintainer-policy.md](maintainer-policy.md)), with concealed org members counted, never named;
  the pilot and exclude list, kept as tables; the construction controls (`data/controls.yaml`), the measured gaps
  (`data/measured-gaps.yaml`) and the forthcoming capabilities (`data/forthcoming.yaml`).
- **Views (never committed, WP5b OD4):** rendered by `uv run python scripts/render.py` into `build/demo/` (demo mode,
  OD5): the applicability table, every SOP, the pilot proposal and briefing, the reports, the basis tables, the
  data-model document, the fit report, and the wiki pages (`build/demo/wiki/`, WP5d). Live mode
  (`--mode live`) publishes the wiki pages to this repository's wiki, only from a clean, validated `main` equal to
  `origin/main`. The fit analysis ([fit-analysis.md](fit-analysis.md)) is WP4's dated record.
- **Controller:** `scripts/validate.py` enforces the model (CI); `scripts/render.py` runs the view steps
  (`recommend.py`, `policies.py`, `licenses.py`, `org.py`, `pilot.py`, `briefing.py`, `sops.py`, `basis.py`,
  `datamodel.py`, `fit.py`, `wiki.py`); `scripts/audit.py` reproduces the WP5b audit; read-only sensing in `snapshot.py`,
  `org_snapshot.py`, `usage_snapshot.py`, with `privacy_check.py` and `history_privacy_check.py`. The required check:
  `uv run python scripts/validate.py` and `uv run python -m unittest discover -s tests`, in the environment locked in
  `uv.lock`.
- **Remote:** [Open-MBEE/repo-registry](https://github.com/Open-MBEE/repo-registry), public. `main` takes changes
  only through pull requests that pass the required check, with no bypass (WP5 OD3).

## Breakdown (agreed plan, revisited at each gate)

1. WP1, kinds and tiers: **accepted**.
2. WP2, policies: **accepted**. WP2a, license by type: **accepted**.
3. WP3, org governance: **accepted**.
4. WP4, fit analysis and pilot: **accepted**. WP4b, docs sweep and checkpoint: **accepted**. WP4c, the governance
   kinds: **accepted**. WP4d, the attestations file: **accepted**.
   WP4e, type and stage in the kind list: **accepted**.
5. WP5, meta-rule checks in CI, and the move to Open-MBEE: **accepted**. WP5b, the model and views: **accepted** by
   the merge of its delivery pull request. WP5c, the taxonomy refinements: **accepted** by the merge of its delivery pull request. **WP5d, the maintainer
   review pack: accepted ([#11](https://github.com/Open-MBEE/repo-registry/pull/11)). WP5e, verified code owners: in delivery.**
6. WP6, the engine: compare, status, status log, sample issues.
7. WP7, the compliance dashboard: the wiki that WP5d publishes, extended with status, aware of each repository's
   state against the controls (from WP6's sensing), and how to come into demonstrable compliance. WP5d gives the
   what and why of compliance; WP7 gives the current snapshot and the way there. WP7 also publishes the wiki
   automatically from CI after each merge; until then an owner runs live mode by hand.
8. WP8, demonstrations and the five maintainer approvals.

## Next step

Publish the wiki (WP5d's acceptance record): create its first page once in the web app, then run
`uv run python scripts/render.py --mode live` from the validated `main`. Review and accept **WP5e** by merging its
delivery pull request (its scope rides with it), then republish. After that, the owners record the first
verifications (XF-3), and WP6 (the engine) follows.

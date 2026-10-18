# Status

*Updated 2026-10-18, at the WP4c acceptance gate. Update this at each acceptance gate.*

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
  - **WP4d** (the attestations file): scope on `wp4d-scope`, waiting for approval.
  - **WP5** (meta-rule checks in CI, and the move): in progress, paused on `wp5-work` until WP4c and WP4d are
    accepted. Nothing has been written to the org.
  - **WP6 to WP8:** planned (see the breakdown below), not yet scoped.
- **Data (all PROVISIONAL until the maintainers approve it):**
  - a read-only snapshot of the org's 181 public repos (`data/snapshots/2026-10-18`);
  - kinds as type × lifecycle stage, with stages adopted from CNCF and OpenSSF
    ([lifecycle-stage-map.md](lifecycle-stage-map.md));
  - four tiers;
  - the provisional kind list (`registry.yaml`);
  - 16 repository policies (including `license-by-type`) with SOPs (`data/policies/`, `docs/sops/`). Each has an
    applies-if rule on type, stage or tier, and is grounded in [policy-basis-review.md](policy-basis-review.md)
    (CISA and NIST core; the OpenSSF baseline as backbone; CNCF and ISO/IEC/IEEE 12207 secondary);
  - five org policies, a provisional named-maintainer list (`data/maintainers.yaml`: Chris Delp, Michael Zargham,
    Robert Karban, Jason Han), a proposed CODEOWNERS, and the maintainer policy
    ([maintainer-policy.md](maintainer-policy.md)); concealed org members are counted, never named;
  - the fit analysis ([fit-analysis.md](fit-analysis.md)) and the proposed pilot of 32 repositories
    ([pilot-briefing.md](pilot-briefing.md), `data/pilot.yaml`), with every other public repository on the exclude
    list (`data/exclude.yaml`);
  - known gaps that later work closes, as explicit expected failures (`data/expected-gaps.yaml`).
- **Code:** `scripts/snapshot.py` (read-only sensing), `scripts/recommend.py` (deterministic kind recommendations),
  `scripts/policies.py` (policy meta-rules and applicability), `scripts/licenses.py` (license report, WP2a),
  `scripts/org_snapshot.py`, `scripts/org.py` and `scripts/privacy_check.py` (org governance), and
  `scripts/usage_snapshot.py`, `scripts/pilot.py` and `scripts/briefing.py` (usage, pilot and briefing, WP4).
  Tests: `python3 -m unittest discover -s tests`.
- **Remote:** none yet. The repo moves to Open-MBEE during R1, in WP5, on the supervisor's say-so.

## Breakdown (agreed plan, revisited at each gate)

1. WP1, kinds and tiers: **accepted**.
2. WP2, policies: **accepted**. WP2a, license by type: **accepted**.
3. WP3, org governance: **accepted**.
4. WP4, fit analysis and pilot: **accepted**. WP4b, docs sweep and checkpoint: **accepted**. WP4c, the governance
   kinds: **accepted**. WP4d, the attestations file: **scoped**.
5. **WP5, meta-rule checks in CI, and the move to Open-MBEE.**
6. WP6, the engine: compare, status, status log, sample issues.
7. WP7, the wiki.
8. WP8, demonstrations and the five maintainer approvals.

## Next step

Approve and build **WP4d** (the attestations file). Then
resume **WP5** on `wp5-work`: merge `main` into it, update any WP5 test that uses a governance kind, and give the
supervisor the move commands (WP5 OD4).

# Status

*Updated 2026-10-18, at the WP4 acceptance gate. Update this at each acceptance gate.*

## Where we are

- **Design:** DRAFT. The documents in `docs/` are inputs. The contract is
  [WP0](../work-packages/WP0-scope-of-work.md), the project scope through R1, approved in 1dccb62 and amended twice
  (3c72b7d, 3edae32).
- **Work packages:**
  - **WP0** (project scope through R1): approved.
  - **WP1** (kinds and tiers): accepted in bcb1e73. Review: [WP1-review.md](../work-packages/WP1-review.md).
  - **WP2** (policies): accepted in 1ced09b. Review: [WP2-review.md](../work-packages/WP2-review.md).
  - **WP3** (org governance): accepted in 3c0ba20. Review: [WP3-review.md](../work-packages/WP3-review.md).
  - **WP2a** (license by type, a supplement to WP2): accepted in 61a3db6. Review:
    [WP2a-review.md](../work-packages/WP2a-review.md).
  - **WP4** (fit analysis and pilot): accepted in 1408259. Review: [WP4-review.md](../work-packages/WP4-review.md).
  - **WP5 to WP8:** planned (see the breakdown below), not yet scoped.
- **Data (all PROVISIONAL until the maintainers approve it):**
  - a read-only snapshot of the org's 181 public repos (`data/snapshots/2026-10-18`);
  - kinds as type × lifecycle stage, with stages adopted from CNCF and OpenSSF
    ([lifecycle-stage-map.md](lifecycle-stage-map.md));
  - four tiers;
  - the provisional kind list (`registry.yaml`);
  - 16 repository policies (including `license-by-type`) with SOPs (`data/policies/`, `docs/sops/`). Each has an applies-if rule on type, stage or tier, and
    is grounded in [policy-basis-review.md](policy-basis-review.md) (CISA and NIST core; the OpenSSF baseline as
    backbone; CNCF and ISO/IEC/IEEE 12207 secondary);
  - five org policies, a provisional named-maintainer list (`data/maintainers.yaml`: Chris Delp, Michael Zargham,
    Robert Karban, Jason Han), a proposed CODEOWNERS, and the maintainer policy
    ([maintainer-policy.md](maintainer-policy.md)); concealed org members are counted, never named;
  - the fit analysis ([fit-analysis.md](fit-analysis.md)) and the proposed pilot of 32 repositories
    ([pilot-briefing.md](pilot-briefing.md), `data/pilot.yaml`), with every other public repository on the exclude
    list (`data/exclude.yaml`);
  - known gaps that later work closes, as explicit expected failures (`data/expected-gaps.yaml`).
- **Code:** `scripts/snapshot.py` (read-only sensing), `scripts/recommend.py` (deterministic kind recommendations)
  `scripts/policies.py` (policy meta-rules and applicability), and `scripts/org_snapshot.py`, `scripts/org.py` and
  `scripts/privacy_check.py` (org governance).
  Tests: `python3 -m unittest discover -s tests`.
- **Remote:** none yet. The repo moves to Open-MBEE during R1, in WP5, on the supervisor's say-so.

## Breakdown (agreed plan, revisited at each gate)

1. WP1, kinds and tiers: **accepted**.
2. WP2, policies: **accepted**. WP2a, license by type: **accepted**.
3. WP3, org governance: **accepted**.
4. WP4, fit analysis and pilot: **accepted**.
5. **WP5, meta-rule checks in CI, and the move to Open-MBEE.**
6. WP6, the engine: compare, status, status log, sample issues.
7. WP7, the wiki.
8. WP8, demonstrations and the five maintainer approvals.

## Next step

Scope **WP5 (meta-rule checks in CI, and the move to Open-MBEE)** with `scope-of-work`. It is the first package that
writes to the org (creating this repository there), so the move happens only on the supervisor's explicit go-ahead.
Inputs carried to it:
- the meta-rules to enforce: the kind list (`docs/kind-list-format.md`), the policies (`docs/policy-format.md`), and
  the data files that must stay valid (WP0 R-14: an invalid state never reaches `main`);
- the tests to run in GitHub Actions on every pull request;
- the proposed CODEOWNERS (`data/proposed-codeowners`) stays not live until the maintainers approve it, and review
  friction rises only at R3;
- expected gap XF-1 (the sensing credential) closes in WP6, and its setup may start with the move.

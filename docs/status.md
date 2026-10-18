# Status

*Updated 2026-10-18, at the WP2 acceptance gate. Update this at each acceptance gate.*

## Where we are

- **Design:** DRAFT. The documents in `docs/` are inputs. The contract is
  [WP0](../work-packages/WP0-scope-of-work.md), the project scope through R1, approved in 1dccb62 and amended twice
  (3c72b7d, 3edae32).
- **Work packages:**
  - **WP0** (project scope through R1): approved.
  - **WP1** (kinds and tiers): accepted in bcb1e73. Review: [WP1-review.md](../work-packages/WP1-review.md).
  - **WP2** (policies): accepted in 1ced09b. Review: [WP2-review.md](../work-packages/WP2-review.md).
  - **WP3 to WP8:** planned (see the breakdown below), not yet scoped.
- **Data (all PROVISIONAL until the maintainers approve it):**
  - a read-only snapshot of the org's 181 public repos (`data/snapshots/2026-10-18`);
  - kinds as type × lifecycle stage, with stages adopted from CNCF and OpenSSF
    ([lifecycle-stage-map.md](lifecycle-stage-map.md));
  - four tiers;
  - the provisional kind list (`registry.yaml`);
  - 15 policies with SOPs (`data/policies/`, `docs/sops/`). Each has an applies-if rule on type, stage or tier, and
    is grounded in [policy-basis-review.md](policy-basis-review.md) (CISA and NIST core; the OpenSSF baseline as
    backbone; CNCF and ISO/IEC/IEEE 12207 secondary);
  - known gaps that later work closes, as explicit expected failures (`data/expected-gaps.yaml`).
- **Code:** `scripts/snapshot.py` (read-only sensing), `scripts/recommend.py` (deterministic kind recommendations)
  and `scripts/policies.py` (policy meta-rules and applicability).
  Tests: `python3 -m unittest discover -s tests`.
- **Remote:** none yet. The repo moves to Open-MBEE during R1, in WP5, on the supervisor's say-so.

## Breakdown (agreed plan, revisited at each gate)

1. WP1, kinds and tiers: **accepted**.
2. WP2, policies: **accepted**.
3. **WP3, org governance:** the named maintainers and the org-wide common controls.
4. WP4, fit analysis of all repos, and the pilot of 24 to 36 repos.
5. WP5, meta-rule checks in CI, and the move to Open-MBEE.
6. WP6, the engine: compare, status, status log, sample issues.
7. WP7, the wiki.
8. WP8, demonstrations and the five maintainer approvals.

## Next step

Scope **WP3 (org governance)** with `scope-of-work`. Inputs carried to it:
- the named maintainers: this repo's CODEOWNERS and the org's admins (WP0 D-8, R-15);
- org-wide common controls, including two-factor authentication (OpenSSF SB-2 and NIST IA-2(1), handed on by WP2)
  and a small number of owners and admins (OpenSSF TI-3);
- the org's administration is governance/graduated (high tier);
- the sensing credential with *Administration: read* (expected gap XF-1, which closes in WP6).

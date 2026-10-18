# Status

*Updated 2026-10-18, at the WP1 acceptance gate. Update this at each acceptance gate.*

## Where we are

- **Design:** DRAFT. The documents in `docs/` are inputs. The contract is
  [WP0](../work-packages/WP0-scope-of-work.md), the project scope through R1, approved in 1dccb62 and amended twice
  (3c72b7d, 3edae32).
- **Work packages:**
  - **WP0** (project scope through R1): approved.
  - **WP1** (kinds and tiers): accepted in bcb1e73. Review: [WP1-review.md](../work-packages/WP1-review.md).
  - **WP2 to WP8:** planned (see the breakdown below), not yet scoped.
- **Data (all PROVISIONAL until the maintainers approve it):**
  - a read-only snapshot of the org's 181 public repos (`data/snapshots/2026-10-18`);
  - kinds as type × lifecycle stage, with stages adopted from CNCF and OpenSSF
    ([lifecycle-stage-map.md](lifecycle-stage-map.md));
  - four tiers;
  - the provisional kind list (`registry.yaml`).
- **Code:** `scripts/snapshot.py` (read-only sensing) and `scripts/recommend.py` (deterministic kind recommendations).
  Tests: `python3 -m unittest discover -s tests`.
- **Remote:** none yet. The repo moves to Open-MBEE during R1, in WP5, on the supervisor's say-so.

## Breakdown (agreed plan, revisited at each gate)

1. WP1, kinds and tiers: **accepted**.
2. **WP2, policies.** The policy basis review (GitHub security features cross-checked against CISA and NIST RMF), then
   named policies, each with an applies-if rule on type, stage or tier and an SOP.
3. WP3, org governance: the named maintainers and the org-wide common controls.
4. WP4, fit analysis of all repos, and the pilot of 24 to 36 repos.
5. WP5, meta-rule checks in CI, and the move to Open-MBEE.
6. WP6, the engine: compare, status, status log, sample issues.
7. WP7, the wiki.
8. WP8, demonstrations and the five maintainer approvals.

## Next step

Scope **WP2 (policies)** with `scope-of-work`. Inputs carried to it from WP1
([WP1-decisions.md](../work-packages/WP1-decisions.md)):
- semantic versioning as a policy for tools;
- maintenance duties (tracking dependencies, fixing reported security flaws) as policies attached to stages;
- the OpenSSF security baseline by stage as the precedent for stage-attached policies;
- secondary citations: ISO/IEC/IEEE 12207:2026 §5.4 (cited by reference only), and the CNCF and OpenSSF project
  lifecycles.

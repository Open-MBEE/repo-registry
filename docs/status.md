# Status

*Updated 2026-10-18, at the WP3 acceptance gate. Update this at each acceptance gate.*

## Where we are

- **Design:** DRAFT. The documents in `docs/` are inputs. The contract is
  [WP0](../work-packages/WP0-scope-of-work.md), the project scope through R1, approved in 1dccb62 and amended twice
  (3c72b7d, 3edae32).
- **Work packages:**
  - **WP0** (project scope through R1): approved.
  - **WP1** (kinds and tiers): accepted in bcb1e73. Review: [WP1-review.md](../work-packages/WP1-review.md).
  - **WP2** (policies): accepted in 1ced09b. Review: [WP2-review.md](../work-packages/WP2-review.md).
  - **WP3** (org governance): accepted in 3c0ba20. Review: [WP3-review.md](../work-packages/WP3-review.md).
  - **WP4 to WP8:** planned (see the breakdown below), not yet scoped.
- **Data (all PROVISIONAL until the maintainers approve it):**
  - a read-only snapshot of the org's 181 public repos (`data/snapshots/2026-10-18`);
  - kinds as type × lifecycle stage, with stages adopted from CNCF and OpenSSF
    ([lifecycle-stage-map.md](lifecycle-stage-map.md));
  - four tiers;
  - the provisional kind list (`registry.yaml`);
  - 15 policies with SOPs (`data/policies/`, `docs/sops/`). Each has an applies-if rule on type, stage or tier, and
    is grounded in [policy-basis-review.md](policy-basis-review.md) (CISA and NIST core; the OpenSSF baseline as
    backbone; CNCF and ISO/IEC/IEEE 12207 secondary);
  - five org policies, a provisional named-maintainer list (`data/maintainers.yaml`: Chris Delp, Michael Zargham,
    Robert Karban, Jason Han), a proposed CODEOWNERS, and the maintainer policy
    ([maintainer-policy.md](maintainer-policy.md)); concealed org members are counted, never named;
  - known gaps that later work closes, as explicit expected failures (`data/expected-gaps.yaml`).
- **Code:** `scripts/snapshot.py` (read-only sensing), `scripts/recommend.py` (deterministic kind recommendations)
  `scripts/policies.py` (policy meta-rules and applicability), and `scripts/org_snapshot.py`, `scripts/org.py` and
  `scripts/privacy_check.py` (org governance).
  Tests: `python3 -m unittest discover -s tests`.
- **Remote:** none yet. The repo moves to Open-MBEE during R1, in WP5, on the supervisor's say-so.

## Breakdown (agreed plan, revisited at each gate)

1. WP1, kinds and tiers: **accepted**.
2. WP2, policies: **accepted**.
3. WP3, org governance: **accepted**.
4. **WP4, fit analysis of all repos, and the pilot of 24 to 36 repos.**
5. WP5, meta-rule checks in CI, and the move to Open-MBEE.
6. WP6, the engine: compare, status, status log, sample issues.
7. WP7, the wiki.
8. WP8, demonstrations and the five maintainer approvals.

## Next step

Scope **WP4 (fit analysis and pilot)** with `scope-of-work`. Inputs carried to it:
- the provisional kind list from WP1, with 45 unclassified repos (25 forks; 20 with no type signal) and 74 flagged as
  archive candidates;
- the fit analysis of all of the org's repos is a separate task from the pilot (WP0 D-6);
- the pilot: 24 to 36 repos, sampled to include heavily used and actively developed tools, the website and other
  media, research repos, and repos that should be archived (WP0); everything else goes on the exclude list;
- the applicability table from WP2 and WP3 shows which policies each pilot repo would carry.

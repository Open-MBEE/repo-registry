# Lifecycle stages: adopting the CNCF and OpenSSF model

> **PROVISIONAL** until the maintainers approve the taxonomy (WP0, maintainer approval 1). It went into WP1 through
> amendment 2, approved by the supervisor (3edae32; [WP1-amendment-2.md](../work-packages/WP1-amendment-2.md)). It
> was written from the source documents listed below, not from memory.

## Sources

| Ref | Document | Version read |
|---|---|---|
| CNCF-LC | CNCF TOC, *CNCF Project Lifecycle & Process* v1.6, `cncf/toc/process/README.md` | commit d815451, 2026-10-01 |
| CNCF-AR | CNCF TOC, *CNCF Project Archiving Process* v1.1, `cncf/toc/process/archiving.md` | read 2026-10-18 |
| OSSF-LC | OpenSSF TAC, *Becoming an OpenSSF Project*, `ossf/tac/process/project-lifecycle.md` | commit d019efe, 2026-08-05 |
| OSSF-SB | OpenSSF TAC, *Security Baseline* (by stage), `ossf/tac/process/security_baseline.md` | read 2026-10-18 |
| SEMVER | *Semantic Versioning 2.0.0*, items 4 and 5 (semver.org) | standard text |

Both foundations use the same four stages: **Sandbox, Incubating (CNCF: Incubation), Graduated, Archived**. What
follows paraphrases them. See the sources for the exact wording.

## What each stage means in the sources

| Stage | CNCF-LC | OSSF-LC | OSSF-SB (security expected) |
|---|---|---|---|
| **Sandbox** | Experimental or innovative, early in development. Failure is possible. Significant and breaking changes are expected. | Entry point for early-stage projects, to encourage experimentation. One maintainer is enough to enter, and growth is expected. Dormant for 6 months makes it a candidate for archiving. | Light: two-factor authentication, and a memory-safe language for new code |
| **Incubating** | Past the experimental phase and starting to show stability. Fewer breaking changes, and more stable, versioned APIs. Adoption is now assessed. | An established technical vision and a working project, still refining. At least 3 maintainers from 2 or more organizations, adoption by multiple parties, initial governance, a contact for vulnerability reports, and "following a version schema". | Adds a published dependency policy, pinned dependencies, least-privilege credentials, no hard-coded secrets, Scorecard, then a security policy, static analysis, and hardened CI |
| **Graduated** | The most mature and robust stage. Wide adoption, shown by production deployments. Comprehensive security. | Highest maturity, with sustained contribution. At least 5 maintainers from 3 or more organizations, wide adoption, a consistent release cadence, governance shown in action, a third-party security audit where applicable, and **adherence to semantic versioning with a declared policy for stable releases and backported fixes**. | Adds prompt fixes for critical known vulnerabilities, fixes within 60 days for medium and high, required review before merging, SBOMs, signed releases, and SLSA provenance |
| **Archived** | Inactive or low activity, or no longer recommended. CNCF-AR notes that a mature, nearly feature-complete project is different from an inactive one. | No longer in active development, or no longer recommended. 6 or 9 months dormant makes a candidate, never an automatic archive. Decided by vote. | — |

## What the sources show (and how they differ from the earlier sketch)

1. **A stage is a signal of maturity, not a version number.** OSSF-LC says so directly. Promotion depends on technical
   vision, adoption, and how sustainable the governance and contributor base are. Neither foundation defines a stage
   by version.
2. **Our 1.0 seam lands between Sandbox and Incubating, not between Incubating and Graduated.** Under SEMVER, major
   version zero is initial development, where anything may change, and 1.0.0 defines the public API. That matches
   CNCF's line exactly: Sandbox expects breaking changes, and Incubation has "more stable, versioned APIs". A tool with
   no release, or with only 0.x releases, reads as **Sandbox**. A tool at 1.0 or later reads as at least
   **Incubating**.
3. **Graduated can't be read from the snapshot.** It turns on wide production adoption, maintainers from several
   organizations, governance in action and audits. Our snapshot has none of that evidence. So the rules never
   recommend Graduated. The OpenMBEE maintainers assign it on evidence, exactly as a foundation's oversight body votes
   on it.
4. **There is no "maintained" stage, and there doesn't need to be one.** In both sources, a stable project with few
   new features stays Incubating or Graduated (CNCF-AR: feature-complete isn't inactive). Maintenance duties are
   **requirements attached to stages**, not a stage of their own. OSSF-SB attaches a dependency policy at Incubating,
   and fix deadlines for known vulnerabilities at Graduated. That matches amendment A1 (policies attach to a
   lifecycle) and the supervisor's point that maintenance is active.
5. **Archived means GitHub's archived state for us.** The foundations archive by vote. Ours is the repo's
   own read-only state, and dormancy (6 or 9 months in OSSF-LC) is only a *candidate* flag, which matches our
   archive-candidate flag.

## Proposed map

| Our earlier lifecycle | Adopted stage | Recommendation rule (guidance only; maintainers assign) |
|---|---|---|
| experimental (research; tools with no release; 0.x tools) | **Sandbox** | Not archived, and no semver release at or above 1.0.0 (for tools). Live research. Never recommended for media (assigned only) |
| active development / maintained (1.0 or later tools) | **Incubating** | Not archived, and a tool with a semver release at 1.0.0 or later. Live media |
| — | **Graduated** | Never recommended. The maintainers assign it on adoption and governance evidence |
| archived | **Archived** | Archived on GitHub |

The `unreleased` departure goes away: tools with no release are Sandbox. Media has no versions, so there is no
activity rule for it: live media is recommended Incubating, and media/sandbox is assigned only. Research is
recommended Sandbox; research/incubating and research/graduated are assigned only (WP1 amendment 2, Agent's
defaults).

## Decisions on this map (settled in WP1 amendment 2)

- **Tier for tool/sandbox: low.** Sandbox holds both tools with no release (low before) and 0.x tools (medium
  before), and one kind has one tier. The supervisor chose low.
- **Tier for tool/incubating: medium.** It holds every tool at 1.0 or later (high before). The supervisor chose
  medium. Graduated tools stay high.
- **Media and research (Agent's defaults, approved).** Live media is recommended Incubating (medium); media tops out
  at medium. Live research is recommended Sandbox, and every research kind is low.

The records are in [WP1-amendment-2.md](../work-packages/WP1-amendment-2.md); the tiers are in
[kinds.yaml](../data/taxonomy/kinds.yaml).

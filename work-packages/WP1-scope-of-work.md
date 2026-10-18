# WP1 — Scope of work: kinds and tiers

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `repo-registry` (local; moves to Open-MBEE during R1, in WP5) |
| **Approval record** | mzargham's `git merge --no-ff -m "<message>"` of the scope branch into `main` ([AGENTS.md](../AGENTS.md)) |
| **Acceptance record** | mzargham's `git merge --no-ff -m "<message>"` of the work branch into `main` ([AGENTS.md](../AGENTS.md)) |

## Purpose

WP1 is the first package from the breakdown of the approved [WP0](WP0-scope-of-work.md) (approval merge 1dccb62). It
fixes the taxonomy that every later package classifies against. In WP0's chain, **repo → kind → tier → policies**,
WP1 delivers the first two links: the set of kinds, and the map from kinds to the four tiers. It builds them from rich
data about the org's repos, gathered read-only. It also fixes the format of the canonical kind list. Policies (WP2),
org governance (WP3), and the fit analysis and pilot (WP4) come later.

### Direction decided while scoping

- **Lifecycle stages are adopted, not invented (amended A4).** The lifecycle is the CNCF and OpenSSF project-lifecycle
  stage set: Sandbox, Incubating, Graduated, Archived. The map from their documents is in
  [lifecycle-stage-map.md](../docs/lifecycle-stage-map.md). This replaces experimental, active development, maintained
  and archived, and the `unreleased` departure. A stage is a signal of maturity. The 1.0.0 seam is the step from
  Sandbox to Incubating, following semantic versioning. Graduated is never recommended by rule: the maintainers assign
  it on evidence of adoption and governance. Maintenance duties attach to stages as policies (WP2, following the
  OpenSSF security baseline by stage).
- **Starting point for the kinds: type × lifecycle.** Kinds are trending toward the cross product of a type (tool,
  media, research, and governance, *amended A2*) and a lifecycle, with archived as the
  terminal state. That gives 12 kinds. It is not a final decision, but it roughly matches the intuition in the Slack
  post, and it should give an interpretable mapping to tiered policy sets that is simple for a person to follow. The
  taxonomy may change in the future.
- **Kind and tier stay separate concepts.** A repo has a kind. A kind maps to a tier. A tier maps to policies. Nothing
  skips a link in that chain. This factoring keeps policy making legible and the code simple.
- **Fixed parts of the kind → tier map.** *(Amended A4.)* tool/graduated → **high**, tool/incubating → **medium**,
  tool/sandbox → **low**. Anything archived
  maps to **none**: it is read-only, so it should be inert. Every governance kind maps to high: `repo-registry` is
  governance/sandbox, and the administration of the org itself is governance/graduated (carried to WP3).
  Governance kinds are assigned, not recommended, and only these two are needed. Any other governance kind is omitted,
  with that reason. *(Amended, A2.)* Everything else maps to **low** or **medium**, as
  sparsely as possible. WP1 drafts which.

- **The `0.x` → `1.0.0` seam is the step from Sandbox to Incubating** *(amended A4; it was experimental → active
  development, high)*. A tool with no release, or only `0.x` releases, is a sandbox tool. At `1.0.0` it becomes an
  incubating tool, a kind that maps to the medium tier. One tier per kind
  still holds (WP0 R-17), so reaching `1.0.0` is a change of kind. The system recommends that change, and it lands
  through the usual governed kind-change PR *(default)*.
- **Provisional data, clearly marked.** Our approach needs data before the maintainers have approved it. So we always
  draft provisional data, but mark it clearly as provisional until we pass the maintainer acceptance milestone for
  that data. Here, WP1 drafts every repo's recommended kind into a first kind list. It is provisional: the authority to
  initialize the kind list belongs with the maintainers (WP0's fourth approval).
- **Semantic versioning is a policy for tools (carried to WP2).** *(Amended, A1: it was "for medium and high".)*
  Policies can attach to a type, a lifecycle or a tier (WP0 A1), and semantic versioning attaches to the tool type.
  Other policies, and the `1.0.0` rule above, depend on it to be checkable.
- **Recommendations are guidance; governors assign.** The recommendation rules, activity included, are guidance for
  how governors set a repo's kind. For example, OpenSysML and sysml-toolkit are busy but still `0.x`, so they stay
  in Sandbox. That keeps their rapid development unblocked. When they cross `1.0.0`, they move to
  Incubating and their controls tighten. *(Amended, A3.)* WP2 must define it. WP1 only reads versions from the snapshot. A tool can be in the low tier, or archived,
  without semantic versioning, and media and research aren't assumed to need it.

## Goals

- G1. **A rich, replayable picture of the org.** A read-only snapshot of data about every Open-MBEE repo, from which
  kinds can be told apart.
- G2. **A small set of kinds that people understand.** Each kind has a plain-language meaning and a deterministic
  rule, over the snapshot's data, for recommending it as a repo's initial kind (WP0: "inferred from its measurable
  attributes using the taxonomy").
- G3. **Every kind in exactly one tier.** The kind → tier map, using WP0's four tiers (high, medium, low, none).
- G4. **A canonical kind list that is easy to change.** Its format: one file at the root of this repo, one entry per
  repo, readable by people and checkable by the program, where changing a repo's kind is a one-entry edit.

## Non-goals

- Policies, controls or SOPs (WP2). Tiers here say what they mean, not which policies apply.
- Org governance and the named maintainers (WP3).
- The fit analysis report and the pilot selection (WP4). WP4 builds them from WP1's provisional kind list.
- Initializing the kind list with authority. That belongs to the maintainers.
- The meta-rule checks in CI, and the move to Open-MBEE (WP5). WP1 states the kind list's meta-rules. WP5 enforces them.
- Sensing of security settings, such as branch protection. That is compliance data for WP6, not data for telling
  kinds apart.
- Writing anything to any repo other than this one, or to the org.
- Private repos. They are left out of everything committed here, named nowhere, and recorded only as a count.
- Any language model in the classification rules (WP0 R-1).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The inventory snapshot: a dated, read-only snapshot of all of the org's public repos (private repos are left out entirely, recorded only as a count), committed under `data/snapshots/` *(default)*, together with the `gh` script that produced it | G1 |
| D-2 | The kinds: for each kind, its name, its plain-language meaning, its recommendation rule over snapshot attributes, and its tier. It covers forks, archived repos, `repo-registry` itself (governance/sandbox) and the org's administration (governance/graduated). It starts from type × lifecycle (the adopted stages, amended A4) and states the reason for any departure *(default)*. The `0.x` → `1.0.0` seam separates sandbox tools from incubating tools | G2, G3 |
| D-3 | The tiers: the four tiers, with WP0's meanings, as data the kinds refer to | G3 |
| D-4 | The canonical kind list format: a schema, the meta-rules it must satisfy, and a few example entries. YAML is the starting point (WP0), not a decision | G4 |
| D-5 | The provisional kind list: every repo in the snapshot with its recommended kind (or unclassified, with a reason), in the D-4 format, marked provisional throughout and naming the maintainer approval that would lift that mark | G2, G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The snapshot is read-only. The script uses only `gh` reads (WP0 R-8, R-9). Private repos are left out, recorded only as a count. | Code review of the script; no private repo's name appears in any committed file |
| R-2 | The snapshot is replayable: the rules applied to the stored snapshot give the same recommendations every time (WP0 R-2). | Run twice; diff |
| R-3 | The kinds start from type × lifecycle (tool, media, research, governance × Sandbox, Incubating, Graduated, Archived; amended A4). Any departure from it, a kind added or a kind omitted, is stated with a reason *(default)*. Each kind's meaning fits on one screen. | Compare D-2 with the cross product; every difference has a reason; read |
| R-4 | Every kind's meaning is plain language (WP0 R-4). | Cold read by a non-specialist |
| R-5 | The recommendation rules are deterministic, involve no language model, and are mutually exclusive: on the snapshot, no repo is recommended two kinds (TX-3). A repo that fits none is shown as unclassified, not forced into a kind (TX-4). | Apply the rules to the snapshot; no repo has two kinds; unclassified repos are listed with a reason |
| R-6 | Every kind maps to exactly one tier (WP0 R-17). tool/graduated maps to high, tool/incubating to medium, tool/sandbox to low, archived kinds to none, every governance kind to high (`repo-registry` is governance/sandbox) *(amended A4)*, and every other kind maps to low or medium. Every tier is used by at least one kind *(default)*. | Inspect the map; no data file or text gives a repo a tier directly |
| R-7 | Kinds, tiers and rules are data, not code: the rule engine names no kind (WP0 R-6, FM-2). | Swap in a toy set of kinds; zero code change |
| R-8 | In the kind list format, changing a repo's kind is a one-entry edit (WP0 R-12), and the format's meta-rules are stated precisely enough for WP5 to enforce them. | A sample reclassification diff touches one entry; the meta-rules read as checkable statements |
| R-9 | The release-maturity rule applies only to tools with semantic-versioned releases: below `1.0.0`, or no release, recommends Sandbox, and `1.0.0` or later recommends Incubating. Graduated is never recommended by rule *(amended A4)*. Semantic versioning is not assumed for media or research kinds. | On the snapshot, sample tools on each side of `1.0.0`, a tool without semver, and an archived tool get the expected result |
| R-10 | Provisional data can't be mistaken for approved data. The provisional kind list is marked provisional in a way the program can check, and it names the maintainer approval that lifts the mark *(default: a file-level field naming the approval, plus the word PROVISIONAL in its header)*. | Inspect the file; the D-4 meta-rules include the provisional mark |

## Definition of good

- The kinds feel obvious to maintainers: each repo's recommended kind matches what they would have said.
- Few repos are unclassified, and each one that is shows a real gap in the taxonomy rather than a weak rule.
- The tiers make the strictness of each kind easy to explain to a regulated adopter.

## Definition of good enough

- The snapshot (D-1) exists, with its script, and replays (R-1, R-2).
- The kinds (D-2) and tiers (D-3) exist as data, and every requirement above passes its check.
- The kind list format (D-4) exists, with its meta-rules and example entries.
- The provisional kind list (D-5) covers every snapshot repo and is marked provisional (R-10).
- A short summary for the supervisor: each kind with its tier and how many snapshot repos it would recommend, plus
  the unclassified repos and why *(default)*.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- The snapshot is committed under `data/snapshots/<date>/`, with the script in `scripts/` (D-1).
- The snapshot is taken with mzargham's current `gh` token (`repo`, `read:org`, member of the org). That is enough for
  repo metadata, activity, releases, files present, topics, languages and fork and archive status. Security settings
  that need admin access are out of scope (Non-goals).
- Any departure from type × lifecycle is stated with a reason (R-3).
- Every tier is used by at least one kind (R-6).
- The summary for the supervisor (Definition of good enough).
- The provisional mark is a file-level field naming the approval that lifts it, plus PROVISIONAL in the header (R-10).
- The provisional-data rule is also added to [AGENTS.md](../AGENTS.md), because it applies to every package.
- Reaching `1.0.0` is recommended as a kind change, and it lands through the usual governed kind-change PR (Direction).

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop: 8 decided, 0 deferred, 2 raised (release maturity and
semantic versioning; repo-registry's kind and the friction lifecycle). The records are in
[WP1-decisions.md](WP1-decisions.md).

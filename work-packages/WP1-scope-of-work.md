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

- **Starting point for the kinds: type × lifecycle.** Kinds are trending toward the cross product of a type (tool,
  media, research) and a lifecycle (experimental, active development, maintained, archived), with archived as the
  terminal state. That gives 12 kinds. It is not a final decision, but it roughly matches the intuition in the Slack
  post, and it should give an interpretable mapping to tiered policy sets that is simple for a person to follow. The
  taxonomy may change in the future.
- **Kind and tier stay separate concepts.** A repo has a kind. A kind maps to a tier. A tier maps to policies. Nothing
  skips a link in that chain. This factoring keeps policy making legible and the code simple.
- **Fixed parts of the kind → tier map.** Tools in active development or maintained map to **high**. Anything archived
  maps to **none**: it is read-only, so it should be inert. `repo-registry`'s own kind maps to the high tier, and the
  org policy's controls over the organization itself are high-tier controls too (carried to WP3). Everything else maps to **low** or **medium**, as
  sparsely as possible. WP1 drafts which.

- **The `0.x` → `1.0.0` seam is the step from experimental to active development.** A tool with only `0.x` releases
  is an experimental tool. At `1.0.0` it becomes a tool in active development, a kind that maps to the high tier. One tier per kind
  still holds (WP0 R-17), so reaching `1.0.0` is a change of kind. The system recommends that change, and it lands
  through the usual governed kind-change PR *(default)*.
- **Provisional data, clearly marked.** Our approach needs data before the maintainers have approved it. So we always
  draft provisional data, but mark it clearly as provisional until we pass the maintainer acceptance milestone for
  that data. Here, WP1 drafts every repo's recommended kind into a first kind list. It is provisional: the authority to
  initialize the kind list belongs with the maintainers (WP0's fourth approval).
- **Semantic versioning is a policy for medium and high (carried to WP2).** Other policies, and the `1.0.0` rule
  above, depend on it to be checkable. WP2 must define it. WP1 only reads versions from the snapshot. A tool can be in the low tier, or archived,
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
| D-2 | The kinds: for each kind, its name, its plain-language meaning, its recommendation rule over snapshot attributes, and its tier. It covers forks, archived repos, and `repo-registry` itself (WP0 X-9: an exploratory kind while it is built). It starts from type × lifecycle (12 kinds) and states the reason for any departure *(default)*. The `0.x` → `1.0.0` seam separates experimental tools from tools in active development | G2, G3 |
| D-3 | The tiers: the four tiers, with WP0's meanings, as data the kinds refer to | G3 |
| D-4 | The canonical kind list format: a schema, the meta-rules it must satisfy, and a few example entries. YAML is the starting point (WP0), not a decision | G4 |
| D-5 | The provisional kind list: every repo in the snapshot with its recommended kind (or unclassified, with a reason), in the D-4 format, marked provisional throughout and naming the maintainer approval that would lift that mark | G2, G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The snapshot is read-only. The script uses only `gh` reads (WP0 R-8, R-9). Private repos are left out, recorded only as a count. | Code review of the script; no private repo's name appears in any committed file |
| R-2 | The snapshot is replayable: the rules applied to the stored snapshot give the same recommendations every time (WP0 R-2). | Run twice; diff |
| R-3 | The kinds start from type × lifecycle (tool, media, research × experimental, active development, maintained, archived). Any departure from it is stated with a reason *(default)*. Each kind's meaning fits on one screen. | Compare D-2 with the cross product; every difference has a reason; read |
| R-4 | Every kind's meaning is plain language (WP0 R-4). | Cold read by a non-specialist |
| R-5 | The recommendation rules are deterministic, involve no language model, and are mutually exclusive: on the snapshot, no repo is recommended two kinds (TX-3). A repo that fits none is shown as unclassified, not forced into a kind (TX-4). | Apply the rules to the snapshot; no repo has two kinds; unclassified repos are listed with a reason |
| R-6 | Every kind maps to exactly one tier (WP0 R-17). Tools in active development or maintained map to high, archived kinds map to none, `repo-registry`'s kind maps to high, and every other kind maps to low or medium. Every tier is used by at least one kind *(default)*. | Inspect the map; no data file or text gives a repo a tier directly |
| R-7 | Kinds, tiers and rules are data, not code: the rule engine names no kind (WP0 R-6, FM-2). | Swap in a toy set of kinds; zero code change |
| R-8 | In the kind list format, changing a repo's kind is a one-entry edit (WP0 R-12), and the format's meta-rules are stated precisely enough for WP5 to enforce them. | A sample reclassification diff touches one entry; the meta-rules read as checkable statements |
| R-9 | The release-maturity rule applies only to tools with semantic-versioned releases: below `1.0.0` recommends experimental, and `1.0.0` or later recommends active development (or maintained, by the lifecycle rule). A tool without semantic versioning can still be recommended a low-tier kind, or archived. Semantic versioning is not assumed for media or research kinds. | On the snapshot, sample tools on each side of `1.0.0`, a tool without semver, and an archived tool get the expected result |
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

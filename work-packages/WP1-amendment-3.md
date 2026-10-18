# WP1 — Amendment 3: the governance kinds, and OpenSSF as a core citation

Made by [WP4c](WP4c-scope-of-work.md), approved by mzargham's merge 8fb2070. Decisions are recorded verbatim in
[WP4c-decisions.md](WP4c-decisions.md). This record says what earlier decisions said and what replaces them.

## The governance kinds

**What WP1 said.** WP1-decisions G-2 (A2) made governance a type with two members, `repo-registry` and the
administration of the GitHub org, "and anything with governance type is tier high". [WP1-amendment-2](WP1-amendment-2.md)
put `repo-registry` at governance/sandbox and the org at governance/graduated, both high, and omitted
governance/incubating ("only two things have the governance type"). WP2 and WP3 then excluded governance/graduated by
name from every repository policy, so that it carried only the 5 org policies, while governance/sandbox carried 13.

**What was wrong.** The stage said *which thing* was governed, not *how mature* it was. When `repo-registry` graduated
it would have lost every repository control, and sandbox governance was at the strictest tier.

**What replaces it.**
- One governance type, at different stages (WP4c OD1). The org's administration is governance/graduated;
  `repo-registry` is governance/sandbox.
- Friction rises with the stage (WP4c OD2): governance/sandbox is **low**, governance/incubating is **defined** and
  **medium**, governance/graduated is **high**. governance/archived stays omitted.
- governance/sandbox carries a sandbox tool's policies (3). governance/incubating carries an incubating tool's
  policies except `semantic-versioning` (10). governance/graduated carries the 5 org policies and the strict
  repository set (18). No applies-if rule excludes governance/graduated any more.
- `repo-registry`'s path, in the supervisor's words: "for now we're still in sandbox for repo-registry and we will
  transition to incubating if the maintainers buy and in and work together to get it calibrated. we wont switch it to
  graduate until the repo-registry is accepted as the canonical source". Each move is an assignment by the
  maintainers.
- Repository policies in effect for the org's administration (for example `change-review`) are read, in WP6, from
  the org's own settings where GitHub has one (for example an org ruleset). That is the engine's concern; this
  amendment changes only which policies are in effect.

The governance tier statement "anything with governance type is tier high" is superseded for the sandbox and
incubating stages. "Whatever governs must be at least as strict as what it governs" now holds for graduated
governance, which governs once it is canonical.

## OpenSSF as a core citation

**What was said.** WP0 named two core citations, CISA and the NIST RMF (with SP 800-53). WP1-decisions "Secondary
citations" and WP2 made OpenSSF secondary, with its security baseline as the backbone of the policies.

**What replaces it.** The supervisor: "i think we also elevate OpenSSF to a primary source since we use it explicitly
for our lifecycle model". OpenSSF is a third core citation, for its project lifecycle (the source of the stages,
with CNCF) and its security baseline. Policy meta-rule 7 also requires `cites.openssf`: a list of baseline items,
empty when a policy adopts none. CNCF and ISO/IEC/IEEE 12207 stay secondary.

## Updated

`data/taxonomy/kinds.yaml`; the applies-if rules of 13 policies and the "Applies to" line of 17 SOPs;
`scripts/policies.py` (meta-rule 7); `scripts/briefing.py` (tier wording); the generated reports, applicability
table and briefing; WP0's citations (amended in place); `README.md`, `docs/current-state.md`,
`docs/policy-basis-review.md`, `docs/policy-format.md`, `docs/kind-list-format.md`, `docs/roadmap.md`, and the
DRAFT `docs/design.md` and `docs/requirements/` (edited in place, as WP4b OD1); `data/assignments.yaml` (decision
references); tests `test_wp1.py`, `test_wp3.py`, and the new `test_wp4c.py`.

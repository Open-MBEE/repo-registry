# WP5d — Review report

| | |
|---|---|
| **Scope of work** | [WP5d-scope-of-work.md](WP5d-scope-of-work.md) |
| **Scope approval verified** | The supervisor's verbal approval, recorded verbatim in [WP5d-decisions.md](WP5d-decisions.md) "Approval"; then mzargham's merge of [#10](https://github.com/Open-MBEE/repo-registry/pull/10), fa3cf16 |
| **Work reviewed** | `wp5d-work` at 525805d (rebased onto fa3cf16), with this report. Reviewed at aedb4ca; rerun after the browser review's fixes (0d33a5e); rerun in full after the six observations were fixed (525805d) |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's merge, with a merge commit, of the delivery pull request into `main`, and the first publish of the wiki, run by him |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `explain:` in `data/taxonomy/kinds.yaml`, 23 lines for 23 signals; declared as the table `signal_explanation` in `data/schema/model.yaml`; `scripts/validate.py` fails a signal with no explanation (tried: removing `live` gives "signal live has no explanation") |
| D-2 | met | `scripts/wiki.py`: Home (the index, what we ask of the maintainers, and how to propose a change by pull request), Taxonomy, Repositories, Policies (a summary, and a section per policy), 21 SOP pages, and `_Sidebar`; every model row links to its file at its line, with GitHub's edit link |
| D-3 | met | `scripts/render.py --mode live` refuses off `main`, on a dirty tree, when HEAD is not `origin/main`, or when `validate.py` fails (run on `wp5d-work`: the first three refusals, exit 1); then clones only `repo-registry.wiki.git`, replaces its pages, commits "Publish from <sha>" and pushes. Demo mode renders the same pages into `build/demo/wiki/` (31 pages) |
| D-4 | met | `tests/test_wp5d.py`, 8 tests |
| D-5 | met | `docs/current-state.md`, `docs/status.md`, README, in this pull request; WP7 described as the compliance dashboard (supervisor, during execution: [WP5d-decisions.md](WP5d-decisions.md)) |
| D-6 | met | The Sources page (7 sources, role, version read, link) and 4 source pages: CISA (56 practices), NIST SP 800-53 (33 controls), OpenSSF baseline (25 items), ISO/IEC/IEEE 12207 (4 clauses, number and title only); each item with its adopting policies (SOP links) or its departure and reason; each citation on the Policies page and the SOPs links to its item |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `test_R1_every_repository_once_with_kind_tier_source` passes: all 182 entries once, with kind, tier and source (or reason), linked to GitHub and the kind |
| R-2 | met | `test_R2_every_policy_with_its_kinds_tiers_and_sop` passes, against the applicability view: one summary row per policy (what it asks, its rule in words, its tiers) and one section (its kinds, SOP link, file and edit link) |
| R-3 | met | `test_R3_taxonomy_defines_everything_and_gives_the_heuristics` passes; wording inspected (sample: tool/sandbox reads "Its type is tool: its code owners declared it with the openmbee-tool topic, or, with no type topic, it started here, GitHub reports a programming language for it, and it has no media or research words. It is not archived. Not: its latest numbered release is version 1.0 or later.") |
| R-4 | met | `test_R4_links_resolve_and_pages_name_their_commit` passes: every wiki link resolves to a page and anchor; every page says PROVISIONAL, and the sidebar, shown on every page, names the commit (observation 3); every model row has its edit link |
| R-5 | met for the refusals; the first publish is the supervisor's, at acceptance | `test_R5_refuses_off_main_dirty_ahead_or_invalid` and `test_R5_writes_only_to_this_repositorys_wiki` pass. The first publish is part of the acceptance record above |
| R-6 | met, as amended | The supervisor's decision to fix observations 1 and 6 amends R-6 for two wording edits to the model: a link in `license-by-type`'s set-up step, and the record references in the unclassified reasons (`kinds.yaml`, `registry.yaml`); observation 2 adds a `context` column to the NIST source file. No kind, rule or policy's applicability changed. Against `origin/main`: the pilot, exclude list, tiers and maintainers unchanged; `kinds.yaml`: the `explain:` block added (D-1), and two reasons reworded (observation 6). On 525805d: `scripts/validate.py` "valid: every table meets data/schema/model.yaml, and every view renders, the same twice"; 109 tests OK (expected failures=1); `scripts/audit.py`: all 16 findings return none; both privacy scans name no concealed member |
| R-7 | met | `test_R7_citations_link_both_ways` passes: OpenSSF and CISA items are each adopted or departed from; NIST and ISO items are adopted, or (NIST) cited by no policy with their context, required by `validate.py` (observation 2) |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-5 exist, and every requirement passes its check | met | Above |
| The wiki has been published once from `main` | at acceptance | The supervisor's act after the merge (the acceptance record) |

## Browser review (the definition of good)

The supervisor asked for a review loop in the browser with the local deployment. The rendered pages were served
locally (`build/`, a preview page rendering GitHub-flavoured Markdown with wiki links) and read as a maintainer
would: Home → Taxonomy → a kind → Repositories → Policies → a policy → its citation → the source item, following the
links by clicking. Findings, each fixed in 0d33a5e, then a second pass found none left:

| Finding | Fix |
|---|---|
| H1. Home didn't say what is asked of the maintainers | "What we ask of you": the five approvals, and where in the pack each is read |
| H2. The sidebar named sources by id (`cisa`, `nist`) | Short names (CISA practices, NIST SP 800-53, ...) |
| H3. The sidebar listed SOPs by file id, so it read as unsorted | Ordered by name, as on the Policies page |
| T1. A kind's rule ended at "its type is media, by its topic, or by the rules", without saying what the rules read | The three type explanations (`is_tool`, `is_media`, `is_research`) say it in full (D-1 data) |
| R1. `openmbee-<type>` lost `<type>` in table cells (GitHub strips it as HTML) | Table cells escape `<` and `>` outside code spans |
| R3. A maintainer's entry didn't show why | Its source cell shows the recorded decision |
| P1. The Policies table had seven columns: too wide to read, its edit links off screen, and no "what it asks" | A summary (policy, what it asks, when, tiers), then a section per policy (governs, when, kinds, tiers, SOP, file, citations by source) |
| S1. An SOP page carried two PROVISIONAL banners | One (the wiki's) |
| S2. An SOP's table link was labelled `policy-applicability.md` but went to the Policies page | Labelled "Policies" (the demo SOPs are unchanged) |
| SO1. A source page with 25 to 56 items had no overview | An item table at the top: item, title, adopted by or departed (the policies-by-source table the supervisor asked for) |

**Against the definition of good** ("in a few minutes knows what kinds and tiers mean, what each repository is and
why, what each policy asks of it, and how to ask for a change"): met in the walk. The kinds and tiers are on one page,
each kind with its rule in words; each repository's row gives its kind, tier and source, with the decision where a
maintainer made it and the reason where it is unclassified; the Policies summary says what each asks and when; Home
says how to propose a change, and every row has its edit link.

## Outside the scope

- **Out-of-scope changes:** the WP7 description in the documents (asked for by the supervisor during execution,
  carried under D-5); `scripts/render.py` skips a view step that the rendered tree's own controller lacks, so CI's view
  diff can render a `main` without `wiki.py` (found by `test_R5_renders_another_tree_given_by_a_relative_path`);
  `scripts/sops.py` takes a table link and a citation formatter (the demo SOPs are unchanged, byte for byte).
- **Non-goals touched:** none. No kind, policy or taxonomy rule changed (R-6).
- **Raised during execution, outside the scope:** a policy on contributor and maintainer sourcing for sanctioned
  jurisdictions (aerospace and defense users); a research spike for canonical sources is under way. A candidate for a
  later package, recorded in `docs/current-state.md`.

## Observations (not counted as failures)

All six were fixed before acceptance, by the supervisor's decision (see Gap dispositions).

1. The demo SOP for `license-by-type` has a broken relative link (`../../registry.yaml`, written relative to
   `data/policies/`). The wiki rewrites it to the GitHub link; the policy text is unchanged.
2. Ten NIST controls in `data/sources/nist-800-53.yaml` are cited by no policy, only by `docs/maintainer-policy.md` or
   `docs/policy-basis-review.md`. Their source page says so; they are not departures.
3. Every page names its commit, so every pull request's view diff shows each wiki page's header line as changed.
4. Live mode runs `git fetch origin main` before comparing (a local read of the remote; nothing is written there).
5. The DRAFT design documents (`docs/design.md`, `docs/roadmap.md`) still describe a single wiki package; they are
   left as DRAFT inputs.
6. Some unclassified reasons in `kinds.yaml` cite records ("(WP5c OD2)", "(WP5c)"), which mean little to a maintainer
   reading the Repositories page (found in the browser review, R2). The text is model data, left unchanged (R-6).

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop: 1 decided (the observations: fix all six, after one
follow-up question), 0 deferred, 1 raised (the contributor-sourcing policy, recorded for WP5e).

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| Observations 1 to 6 | fix before acceptance | Supervisor: "1, 2, 3, 6,4 and 5". Fixed in 525805d: (1) the link is absolute; (2) each uncited NIST control states its context, required by `validate.py` and shown on the wiki; (3) the commit is named once, in the sidebar; (4) the fetch is documented in `render.py` and `current-state.md`; (5) `design.md` and `roadmap.md` describe the two wiki layers; (6) the reasons cite no records. The review was rerun in full, with a browser pass over the changed pages |
| The browser review's findings (H1 to SO1) | fixed in execution | Found and fixed before the report was first written (0d33a5e); a second pass found none |

## Recommendation

Recommend acceptance. Every deliverable and requirement is met with evidence (R-6 as the supervisor amended it). The
browser review on a local deployment met the definition of good, and its findings were fixed. All six observations
were fixed before acceptance, by the supervisor's decision, and the review was rerun in full. What remains is the
acceptance act itself: the merge of #11, then the first publish of the wiki from `main`, run by the supervisor.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

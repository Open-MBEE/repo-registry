# WP5e — Review report

| | |
|---|---|
| **Scope of work** | [WP5e-scope-of-work.md](WP5e-scope-of-work.md) |
| **Scope approval verified** | The supervisor's statement, recorded verbatim in [WP5e-decisions.md](WP5e-decisions.md) "Approval": "let's keep the scope of work approved locally and then merge it with the PR that implements it" |
| **Work reviewed** | `wp5e-work` at 932f920 (rebased onto `main` at c0d8979, WP5d's acceptance; the tree is the one reviewed), with this report |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | mzargham's merge, with a merge commit, of the delivery pull request into `main` (which also brings the scope to `main`) |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `data/sources/dod-cio-oss-memo.yaml`: Attachment 2 §2.C, 2.C(1), (2), (5), (6) and §3.H quoted verbatim with printed pages; declared as `dodcio_section`, cited as `dodcio`. The PDF's OCR layer corrected against its page images ("Chief Information", "reference (l)"); each quote checked word for word against the text |
| D-2 | met | `data/sources/ofac.yaml` (the SDN list's definition, from OFAC's page, read 2026-10-18; 31 CFR 560.204 from the eCFR as of 2026-10-01), `data/sources/nist-800-218.yaml` (PS.1 to PS.3, pp. 9–10), `data/sources/nist-800-161.yaml` (SR-4, SR-6, pp. 159–160, NIST.SP.800-161r1-upd1); each quote checked word for word. The candidates not adopted stay in `docs/policy-basis-review.md` as candidates |
| D-3 | met | `data/policies/verified-code-owners.yaml`: tier high; identity, sanctions (OFAC's tests) and affiliation (OD1); an owner who is not the person; 12 months; cites CISA C4 Community, NIST PS-3, the memo §2.C, (2), (6), OFAC SDN and 560.204, SSDF PS.1, SP 800-161 SR-4 and SR-6 |
| D-4 | met | The `verification` entry in `data/maintainers.yaml`, declared as `maintainer_verification` (legal name, country of residence, affiliation, verifier, date, policy version); `scripts/validate.py` rejects a missing or extra column, an unknown verifier and a self-verification |
| D-5 | met | XF-3 in `data/measured-gaps.yaml`: `.github`, `verified-code-owners`, `verified-owners`, red, with its reason and when it closes |
| D-6 | met | The wiki: the policy's row and section on Policies, its SOP page, a Source page for the memo, OFAC, SSDF and SP 800-161, and their rows on Sources (36 pages) |
| D-7 | met | `tests/test_wp5e.py` (6 tests); `docs/current-state.md`, `docs/status.md`, `docs/policy-basis-review.md` |
| D-8 | met | `data/sources/cisa-practices.yaml`: 56 practices as 98 verbatim quotes with printed pages (5 across a page break, verified as two halves); Table 1's cells and the SCIP fields not quoted described in a labelled note. `data/sources/openssf-security-baseline.yaml`: each of the 25 items gains the baseline's own words (`quote`; CC-BY 4.0, from ossf/tac's LICENSE), verified against `process/security_baseline.md` at 098faba. No ID changed |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `test_R1_in_effect_for_exactly_the_high_tier` passes; the applicability view gives tool/graduated and governance/graduated |
| R-2 | met | `test_R2_every_citation_names_a_quoted_source_item` passes; the schema's foreign keys by source check every cited ID |
| R-3 | met | `test_R3_a_well_formed_record_is_valid` and `test_R3_malformed_records_are_rejected` pass |
| R-4 | met | `test_R4_non_conformance_is_a_measured_gap_not_a_failure` passes |
| R-5 | met | `test_R5_the_record_holds_only_the_published_facts` passes; no verification record exists yet, so no person's facts are in the repository; test records use placeholders; the privacy scans are clean (below) |
| R-6 | met | The WP5d tests pass with the new pages (every link resolves; every row links to its file); the browser review below |
| R-7 | met | Every quote checked word for word against its document's text: the memo 6, OFAC 560.204, SSDF 3 practices with 4 tasks, SP 800-161 2, CISA 98, OpenSSF 25; the SDN definition copied from OFAC's page. ISO/IEC/IEEE 12207 stays clause numbers and titles; the licensed-text test passes |

On a61f4d8: `scripts/validate.py` "valid: every table meets data/schema/model.yaml, and every view renders, the same
twice"; 115 tests OK (expected failures=1); `scripts/audit.py`: all 16 findings return none; the privacy scans name no
concealed member (186 files; 675 blobs and every commit message on `main`).

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| D-1 to D-8 exist, every requirement passes its check, and the existing suite still passes | met | Above |

## Browser review (the definition of good)

The new and changed pages were read in the local preview, as a maintainer would: the policy's SOP, the memo's Source
page, the CISA page's C4 Community criterion, following links from the SOP's citations. Findings, fixed in 4e91e4c:

| Finding | Fix |
|---|---|
| F1. The SOP's "Applies to" described governance/graduated as the org's administration "and repo-registry once it is accepted", leaving out `.github`, governance/graduated since WP5c OD4 and the one high-tier repository today | The note in `scripts/sops.py` names `.github` (every governance/graduated SOP) |
| F2. The memo's §2.C and §3.H had titles of ours beside its own titles | They carry the memo's headings ("2. USE OF OPEN SOURCE SOFTWARE, paragraph C"), marked as such |

**Against the definition of good:** a maintainer reading the SOP learns who may be a code owner of a high-tier
repository, what an owner checks, and why; each citation opens the source's own words. An owner records a verification
by one pull request (the SOP's set-up steps).

## Outside the scope

- **Out-of-scope changes:** NIST SP 800-53 PS-3 (Personnel Screening) added to `data/sources/nist-800-53.yaml` as the
  policy's core NIST citation; a `date` column type implemented (the schema already listed it); the validator's
  "an uncited item states its context" rule generalized from NIST to every quoted source; F1's note, which changes the
  governance/graduated text in every SOP in effect for that kind (19).
- **Two tests changed** (found by the full suite): `test_wp4c`'s set for governance/graduated adds
  `verified-code-owners`; and the licensed-text guard (`test_wp2` R-12) now exempts eight-word runs wholly inside one
  public title, NIST SP 800-218's, which the verbatim CISA quotes contain (CISA-P-SSDF, CISA-C4-S1-CRITERIA) and the
  standard also cites. The guard is otherwise unchanged.
- **Non-goals touched:** none. No other policy, kind or the taxonomy changed; contributors, the medium and low tiers
  and sensing are untouched.

## Observations (not counted as failures)

1. The verification's 12-month expiry is a compliance matter: the validator checks a record's form, not its age; the
   engine (WP6) will turn age into color.
2. That a maintainer's facts were added by their own commit (consent) is checked in review until WP6 senses commit
   authors.
3. The CISA PDF's extracted text drops a hyphen where a line breaks inside a word. One quote had it
   (CISA-C4-REEVAL, "immediate reevaluation"); the printed page 8 reads "re-evaluation", and the quote now does too.
4. Three of the memo's sections, and SSDF PS.2 and PS.3, are cited by no policy; each states its context, and citing
   them in `release-integrity` or `contributing` is a later candidate.
5. Matching the quotes found seven old CISA paraphrases that misstated their source (for example "OpenSSF Scorecard"
   for "Scorecard"); the verbatim quotes replace them.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop: 3 decided (the observations, sorted by package at the
supervisor's request; the uncited items addressed now; §3.H, after one follow-up), 0 deferred, 0 raised.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| Observation 3: a dropped hyphen in a verbatim quote | fix before acceptance | Supervisor: "fix some first. sort through what is this wp versus wp6. or later". Fixed against the printed page; the quote checks rerun |
| Observations 1 and 2: the verification's age as a color; consent checked from the commit author | follow-up work package (WP6) | Both need the engine: a run against today's date, and the commit author's GitHub login from the API. Recorded in `docs/current-state.md` |
| Observation 4: memo sections and SSDF practices cited by no policy | fix before acceptance | Supervisor: "i think we should address the cited by no policy gap now". A citation sweep: existing policies cite the new sources where they already ask for what a source says (memo §2.C(3) and §2.C(4) newly quoted for it); one policy change, with his explicit approval: `contributing` also asks how contributions are reviewed and tested, and cites §3.H. Every quoted item is now cited |
| Observation 5: the old paraphrases replaced | accept as is | A result, not a gap |
| The browser review's findings (F1, F2) | fixed in execution | Fixed in 4e91e4c |

## Recommendation

Recommend acceptance. Every deliverable and requirement is met with evidence: every quote checked word for word
against its document, and the full suite, audit and privacy scans pass. The browser review met the definition of good,
and its two findings were fixed. The observations were sorted as the supervisor asked: one fixed, two left to WP6,
one addressed now by the citation sweep with his explicit approval for the one policy change, and one accepted as
is. No verification is recorded yet, so XF-3 stays red until the owners make the first ones.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.

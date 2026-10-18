# WP5e — Scope of work: verified code owners for high-tier repositories

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | [Open-MBEE/repo-registry](https://github.com/Open-MBEE/repo-registry) |
| **Approval record** | mzargham's merge, with a merge commit, of the pull request that adds this document into `main` (WP5 OD3) |
| **Acceptance record** | mzargham's merge, with a merge commit, of the delivery pull request into `main` |

## Purpose

OpenMBEE's tools are used in aerospace and defense, including federally regulated settings. The supervisor: "we cannot
export control but we can control our contributor base to avoid sanctioned countries. though in order to add this to
our policy model we need canonical sources" ([WP5d-decisions.md](WP5d-decisions.md), "A candidate policy").

After the research spike, he set the design: "open-mbee maintainers should have a high bar for identity disclosure
and we check their disclosed facts against a policy and we reject maintainer who do not provide identity verfication
(out of band) owners attest to maintainer qualifying attributes which get written to a yaml on their authority that
our scripts can check for conformance. absense is non conformance. for now we can limit this policy to high tier
restriction who codeowners can be [...] as simple as possible but clearly cited to relevant sources"
([WP5e-decisions.md](WP5e-decisions.md)).

The DoD CIO memo *Software Development and Open Source Software* (2022) is the core source he chose to back it
("Next package's PR"). It asks a project's consumers to weigh foreign-government influence, the project's review of
contributions, and whether the software comes from an established, trusted source (Attachment 2, §2.C(2), (6)).
Verified code owners on the high tier are how OpenMBEE shows that.

## Goals

- G1. **The policy:** only maintainers verified by an owner may be code owners of a high-tier repository (graduated
  tools and governance/graduated). An owner verifies identity; that the maintainer is not a sanctioned party, nor
  located or ordinarily resident in a comprehensively sanctioned jurisdiction (OFAC's tests); and that they have no
  affiliation with an organization of concern (CISA's C4 "Community" criterion) (OD1). Stated in the policy and cited.
- G2. **The record:** each owner's verification is a record in this repository, written on an owner's authority, that
  the scripts check; an absent or incomplete record is non-conformance.
- G3. **The sources, in their own words:** the DoD CIO memo as a core source; as secondary sources (OD4), OFAC's
  sanctions regulations (31 CFR Chapter V) with the SDN list, NIST SP 800-218 (SSDF) and NIST SP 800-161 Rev. 1; each
  cited passage quoted verbatim with its section and page, and shown on the wiki like the other sources. The existing
  CISA practices, and the OpenSSF baseline items if their license allows, are requoted verbatim too (OD6). The
  supervisor: "why are we not citing the memo verbatim, same with the earlier cisa doc. it seems like we should be
  quoting verbatim citations".
- G4. **Transparent:** the wiki's review pack shows the policy, its SOP and its sources, so maintainers can read what is
  asked and why before it is approved.

## Non-goals

- Contributors who are not code owners: no screening and no attestation; review by a verified code owner is the
  control (OD3).
- Medium- and low-tier repositories, and org membership: the policy is high tier only ("for now").
- Sensing each high-tier repository's CODEOWNERS from GitHub: that is the engine (WP6). This package records the
  policy, the verification records and their checks; the compliance colors come with WP6.
- Legal advice: what OFAC requires of an open-source project accepting code is unsettled (the spike); the policy states
  OpenMBEE's rule, and counsel's review is a candidate for later.
- ISO/IEC/IEEE 12207 text: it is licensed, and stays clause numbers and titles only (WP2 R-12).
- Changing any other policy, kind or the taxonomy. (Citing the memo's §3.H in `contributing` is a later candidate.)
- Publishing any personal fact beyond a maintainer's legal name, country of residence and affiliation (OD2): no
  identity document, nationality, address or other detail is written to this public repository. Nationality is not a
  criterion (OD1).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The DoD CIO memo as a core source: `data/sources/dod-cio-oss-memo.yaml` *(default)*, each cited section quoted verbatim with its number and page, declared as a source table; citable from policies as `dodcio` *(default)* | G3 |
| D-2 | The secondary sources (OD4), each a source file of the sections or controls cited: OFAC, 31 CFR Chapter V and the SDN list; NIST SP 800-218 (SSDF) PS.1 to PS.3; NIST SP 800-161 Rev. 1 SR-4 and SR-6. The candidates not adopted stay in `docs/policy-basis-review.md` as candidates | G3 |
| D-3 | The policy `verified-code-owners` *(default)*: in effect for tier high; its meaning, what is verified (OD1: identity, sanctions, affiliation), its checks, its set-up steps, and its citations | G1 |
| D-4 | The verification record: a `verification` entry per maintainer in `data/maintainers.yaml` *(default)*, with the published facts (OD2: legal name, country of residence, affiliation), the verifying owner, the date and the policy version; declared in `data/schema/model.yaml` and checked by `scripts/validate.py` (construction) | G2 |
| D-5 | The non-conformance, kept as the error signal: the named maintainers without a valid verification, as a measured gap of this policy (`data/measured-gaps.yaml`), never a CI failure (WP5b). Which people are each high-tier repository's code owners is sensed in WP6 | G2 |
| D-6 | The wiki shows it: the policy's row and SOP, the memo's Source page, the sources table (no change to the wiki's design) | G4 |
| D-7 | Tests; the documents and status, in the same pull requests | G1–G4 |
| D-8 | The existing sources requoted verbatim (OD6): each CISA practice in `data/sources/cisa-practices.yaml` as the guide's own words, with its page and section; the OpenSSF baseline items likewise if the baseline's license allows quotation (else they stay paraphrased, with the reason recorded). The IDs, and so every policy's citations, are unchanged | G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The policy is in effect for exactly the high-tier kinds, and says what is verified, by whom, and how often. | The applicability view; a test |
| R-2 | Every claim the policy makes cites a source: the DoD CIO memo by section, and the adopted secondary sources. | Policy meta-rules (every cited ID exists); a test |
| R-3 | A verification record holds the maintainer's legal name, country of residence and affiliation, the owner who verified them (another person), the date and the policy version; a missing or extra column is rejected. | `scripts/validate.py`; a test with a malformed record |
| R-4 | Until each named maintainer has a valid verification, the policy's non-conformance on the high-tier repositories (today `.github`, governance/graduated; no tool is graduated yet) is listed as a measured gap, and CI still passes. | A test; `data/measured-gaps.yaml` |
| R-5 | No personal fact beyond OD2's (legal name, country of residence, affiliation) is written in the repository, and a maintainer's facts are published only with their consent. | A test over the record's columns; the privacy scan; review of each record's commit |
| R-6 | The wiki renders the policy, its SOP and the memo's Source page, with every link resolving. | The WP5d tests, extended |
| R-7 | Every quoted passage is the source's exact text, with its section and page; no source's ID changes, and no licensed text (ISO) is committed. | A review against each source document, recorded in the review report; the existing tests (IDs, the licensed-text check) |

## Definition of good

- A maintainer reading the wiki understands who may be a code owner of a high-tier repository, what an owner checks,
  and why, with the sources one click away; and an owner can record a verification by one pull request.

## Definition of good enough

- D-1 to D-8 exist, every requirement passes its check, and the existing suite still passes.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- Names: the policy `verified-code-owners`; the source file `data/sources/dod-cio-oss-memo.yaml`, cited as `dodcio`;
  the record a `verification` field on each entry of `data/maintainers.yaml` (already merged only by an owner, WP4b
  OD3), rather than a new file.
- The verifier is a named maintainer who is an org owner, and not the person verified. With two or three owners, each
  owner is verified by another.
- A verification is renewed every 12 months, at the maintainers' annual review (maintainer policy, provision 8); an
  expired one counts as absent.
- The policy's version is its file's last commit; a record names the version it was made under.
- Quotes: only the passages cited are quoted, each whole, with its section and page, from the version named in the
  source file; U.S. government works (CISA, DoD CIO, OFAC, NIST) carry no copyright (17 U.S.C. §105), and each is
  released for public distribution.
- The wiki gets a Source page for the memo and for each adopted secondary source, and rows on the Sources page; the
  candidates not adopted (GitHub's trade-controls page, NIST SP 1326, the EAR sections, the 2025 SecDef memo) stay
  listed as candidates. GitHub's trade-controls page is cited as platform documentation in the policy's `github` docs.
- A maintainer's consent is their own commit adding their facts; the owner's verification is in the same entry,
  merged by an owner. The commit's author is checked in review (sensing commit authors waits for WP6).
- The sanctions criterion is checked by the owner against OFAC's SDN list and OFAC's list of comprehensively
  sanctioned jurisdictions, as of the verification date; the record doesn't copy either list.

## Open decisions (for the supervisor)

- **OD1.** What an owner verifies. *Decided: identity; not a sanctioned party, nor located or ordinarily resident in
  a comprehensively sanctioned jurisdiction; and no affiliation with an organization of concern. Not nationality.*
- **OD2.** What the public record holds. *Decided: the facts: legal name, country of residence and affiliation, each
  published with the maintainer's consent (no consent means not verified); no identity documents or other details.*
- **OD3.** Contributors who are not code owners. *Decided: nothing more now.*
- **OD4.** The secondary sources. *Decided: OFAC, NIST SP 800-218 (SSDF) and NIST SP 800-161 Rev. 1.*
- **OD5.** The Agent's defaults. *Decided: approved, with default 5 reversed by the supervisor (verbatim quotes, as
  written above) and the CISA quotes made verbatim (D-8).*
- **OD6.** *(raised by the supervisor)* Where converting the existing sources to verbatim goes. *Decided: in WP5e
  (D-8).*

None remain open. Every item was resolved through the decision loop: 6 decided (OD1 to OD6; OD2 after one follow-up),
0 deferred, 1 raised (OD6). The records are in [WP5e-decisions.md](WP5e-decisions.md).

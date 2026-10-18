# WP5e — Decision records (gathered before the scope)

Each record quotes the supervisor's answer verbatim. Records are typed by the agent (Claude); the decisions are
mzargham's. The package's origin is recorded in [WP5d-decisions.md](WP5d-decisions.md), "A candidate policy:
contributor sourcing".

## The design, after the research spike

- **Supervisor (mzargham, typed by agent):** "my understanding is that this implies that open-mbee maintainers should
  have a high bar for identity disclosure and we check their disclosed facts against a policy and we reject maintainer
  who do not provide identity verfication (out of band) owners attest to maintainer qualifying attributes which get
  written to a yaml on their authority that our scripts can check for conformance. absense is non conformance. for now
  we can limit this policy to high tier restriction who codeowners can be. do we need a lighter weight self
  attestation for contribors to medium repos or org members? i don't want to make this any more complicated than it
  needs to be. as simple as possible but clearly cited to relevant sources. [...] my gut is that we can put the wiki
  without this but then our next PR should be to add it"
- **Outcome (to be confirmed in the scope):** a policy restricting who may be a code owner of a high-tier repository
  to maintainers whom an owner has verified out of band; the owners' attestations kept in a YAML file the scripts
  check, absence being non-conformance. The agent's answer on contributors: no self-attestation now (it verifies
  nothing; CISA asks that requirements on contributors stay minimal; the control is who can merge). Open for the
  scope: whether to accept that answer, and that the public file records only that a verification was done, never
  the facts verified.

## The DoD CIO memo as a core source

- **Supervisor (mzargham, typed by agent):** "i got it from the link you provided so you can add it as a core source
  and provide the link. its flagged for public distribution we need at least source to back up the new policy we're
  adding"
- **Question:** Where should the DoD CIO memo be added as a core source? (Options: the next package's PR / in #11 now.)
- **Answer (mzargham, typed by agent):** "Next package's PR"
- **Outcome:** a new core citation, added in WP5e with the policy it backs: DoD Chief Information Officer (John B.
  Sherman), "Software Development and Open Source Software", memorandum of 2022-01-24, cleared for open publication
  2022-01-26, https://dodcio.defense.gov/Portals/0/Documents/Library/SoftwareDev-OpenSource.pdf. Paraphrased by
  section in `data/sources/`, as the CISA practices are. The sections that bear on the policy (Attachment 2):
  2.C(1) long-term support ("who is contributing"), 2.C(2) trusted sources, 2.C(5) component integrity, 2.C(6)
  influence of foreign governments (OSS exempt from PL 115-232 §1655, but consumers weigh the project's review of
  contributions), and 3.H (publish how submissions are assessed). #11 (WP5d) is unchanged.

## The research spike's other sources, kept

- **Supervisor (mzargham, typed by agent):** "if there are other secondary sources we should keep from your research
  spike let's make sure to track them with the other secondary sources and not lose them"
- **Outcome:** Tracked in the sources table of `docs/policy-basis-review.md`, each marked *candidate (WP5e)* with what
  was and wasn't verified: OFAC 31 CFR Chapter V and the SDN list; GitHub's trade-controls page; NIST SP 800-218
  (SSDF) PS.1 to PS.3; NIST SP 800-161 Rev. 1 SR-4 and SR-6, with SP 1326; EAR §734.3(b)(3) and §734.7 (context); the
  2025 SecDef memo (context, to verify). Set aside, with the reason: EPAAR 1552.239-71 and EAR Part 732. The WP5e
  scope decides which are adopted.

## OD1 — What an owner verifies

- **Question:** What does an owner verify before a maintainer may be a code owner of a high-tier repository?
  (Options: identity + sanctions / + affiliation / + nationality.)
- **Answer (mzargham, typed by agent):** "+ affiliation"
- **Outcome:** Identity; not a sanctioned party, nor located or ordinarily resident in a comprehensively sanctioned
  jurisdiction (OFAC's tests); and no affiliation with an organization of concern (CISA's C4 "Community" criterion).
  Nationality is not a criterion.

## OD2 — What the public record holds

- **Question:** What does the public verification record in this repository hold? (Options: fact of verification /
  + criteria met / the facts.)
- **Answer (mzargham, typed by agent):** "The facts"
- **Follow-up** (the answer conflicted with the standing privacy rule, WP3 OD1, and the repository is public): Which
  facts go in the public record? (Options: name, residence, affiliation, with each maintainer's consent / name and
  affiliation / criteria met only.)
- **Answer (mzargham, typed by agent):** "Name, residence, affil."
- **Outcome:** The record publishes the maintainer's legal name, country of residence and affiliation, each with the
  maintainer's consent; no consent means not verified. No identity documents or other details are written. The WP3
  rule (concealed members are never named) is unchanged: a maintainer who verifies consents to being named.

## OD3 — Contributors who are not code owners

- **Question:** What applies to contributors who are not code owners? (Options: nothing more now / DCO on high tier /
  self-attestation.)
- **Answer (mzargham, typed by agent):** "Nothing more now"
- **Outcome:** No contributor requirement in this package; review by a verified code owner is the control.

## OD4 — The secondary sources

- **Question:** Which secondary sources are adopted with the DoD CIO memo? (Options: OFAC only / OFAC + NIST / none
  beyond.)
- **Answer (mzargham, typed by agent):** "OFAC + NIST"
- **Outcome:** OFAC's sanctions regulations (31 CFR Chapter V) and the SDN list; NIST SP 800-218 (SSDF) PS.1 to PS.3;
  NIST SP 800-161 Rev. 1 SR-4 and SR-6. The other candidates stay listed as candidates.

## OD6 — Verbatim citations *(raised by the supervisor, during the defaults)*

- **Supervisor (mzargham, typed by agent):** "why are we not citing the memo verbatim, same with the earlier cisa doc.
  it seems like we should be quoting verbatim citations"
- **Agent's answer, in brief:** no recorded decision chose paraphrase; it was a default carried from WP2. CISA, the DoD
  CIO, OFAC and NIST publish U.S. government works (no copyright, 17 U.S.C. §105), released for public distribution.
  ISO/IEC/IEEE 12207 stays clause numbers only (licensed, WP2 R-12).
- **Question:** Converting the existing sources (CISA's practices, and the OpenSSF baseline if its license allows) from
  paraphrase to verbatim quotes: where does that work go? (Options: in WP5e / its own package.)
- **Answer (mzargham, typed by agent):** "In WP5e"
- **Outcome:** WP5e quotes its new sources verbatim (default 5 changed) and adds D-8, requoting the CISA practices and,
  if licensed for it, the OpenSSF items; R-7 checks the quotes against the documents.

## OD5 — The Agent's defaults

- **Question:** Approve the eight Agent's defaults as one item (default 5 now: cited passages quoted verbatim, whole,
  with section and page)? (Asked after a walkthrough of each default, at the supervisor's request: "walk me through".)
- **Answer (mzargham, typed by agent):** "i just reversed 5, and am requesting an update on cisa quotes to be verbatim
  but i accept the others."
- **Outcome:** Defaults 1 to 4 and 6 to 8 approved; default 5 reversed from paraphrase to verbatim quotes (as written
  in the scope); the CISA quotes made verbatim (D-8).

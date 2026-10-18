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

## Approval *(stated by the supervisor; the scope reaches `main` with the delivery)*

- **Supervisor (mzargham, typed by agent):** "let's keep the scope of work approved locally and then merge it with the
  PR that implements it"
- **Outcome:** WP5e's scope (7dbe813 after the rebase onto `main`, with this record) is approved by this statement. There is no separate scope pull
  request; the scope and its records go to `main` in the delivery pull request, whose merge is also the acceptance
  record. Execution runs on `wp5e-work`.

## The review's observations *(the acceptance gate)*

- **Question:** How should the five observations of the WP5e review be disposed of, as one item? (Options: accept as
  is / fix some first / follow-up package.)
- **Answer (mzargham, typed by agent):** "fix some first. sort through what is this wp versus wp6. or later"
- **Outcome (the agent's sort, as asked):** this package: observation 3 (a dropped hyphen in a verbatim quote), fixed;
  WP6: observations 1 and 2 (a verification's age as a color; consent from the commit author); later: observation 4
  (citing the uncited sections in other policies); observation 5 is a result, accepted as is.

## Observation 4: the source items cited by no policy *(the acceptance gate)*

- **Supervisor (mzargham, typed by agent):** "i think we should address the cited by no policy gap now"
- **Supervisor, on the scope of that (typed by agent):** "we're not changing the policies we're sweeping for where our
  existing policies can cite our new sources", then "wait we can make policy changes but only with explicit approval
  like i just gave you.", then "solo you just add appropriate citaiton crossref"
- **Question (on the memo's §3.H, which the contributing policy didn't ask for):** How should §3.H be handled?
  (Options: add to contributing / stay uncited.)
- **Answer (mzargham, typed by agent):** "Add to contributing"
- **Follow-up (his later messages left it unclear):** For the memo's §3.H and the contributing policy, which do you
  want? (Options: change + cite / cite only.)
- **Answer (mzargham, typed by agent):** "Change + cite"
- **Outcome:** The agent's standing authority is citations only: a sweep adds a citation where an existing policy
  already asks for what the source says. A change to what a policy asks needs the supervisor's explicit approval, as
  given here for `contributing` (its guide also says how contributions are reviewed and tested before merging; cites
  §3.H). The sweep's citations: `change-review` (§2.C(6), SSDF PS.1), `history-protection`, `org-base-permission` and
  `workflow-least-privilege` (SSDF PS.1), `dependency-management` (§2.C(3), newly quoted), `static-analysis`,
  `vulnerability-remediation` and `security-policy` (§2.C(4), newly quoted), `release-integrity` (§2.C(5), SSDF PS.2
  and PS.3, SP 800-161 SR-4), `verified-code-owners` (§2.C(1)). Every quoted item is now cited by a policy. This
  amends WP5e's non-goal "changing any other policy" for these citations and the one approved change.

## Two policies: the contribution guide, and who may approve *(raised by the supervisor before the push)*

- **Supervisor (mzargham, typed by agent):** "one more sanity check is whether we actually should have split out two
  different policies for contributors, something that seperates having a contributors guidelines file from have a
  restrictions on who can contribute. those seem like two different policies. i think i introduced that conflation and
  i want to remediate it before we push"
- **Asked to choose a remediation, the supervisor answered (typed by agent):** "reread the primary sources and propose
  a maximully faithful two policy solution for me to review"
- **The agent's proposal, from the sources:** Policy A, `contributing`, the guide: it publishes that submissions are
  accepted and which kinds (memo §3.H; CISA CONTRIB-TYPES), every requirement on contributors, kept minimal (CISA
  CONTRIB-MINIMAL), how submissions are assessed, tested and evaluated (memo §3.H), and tests with code (CISA
  CONTRIB-TESTS); it restricts no one. Policy B, `verified-code-owners`: on the high tier, only verified maintainers
  approve and merge (SSDF PS.1; CISA CODE-REVIEW, C4 Conduct and Community; memo §2.C(2), (6); SP 800-161 SR-6;
  NIST PS-3; OFAC for the verification); it restricts approvers, not contributors. The memo's §2.C(1) moves to
  `codeowners`. Left open by the sources: a sanctions floor for contributors.

## No sanctions floor for contributors, at this time

- **Question (from the proposal):** a sanctions floor for contributors: (a) none / (b) a floor as a policy choice
  (no contributions from SDN-listed parties or persons in comprehensively sanctioned jurisdictions).
- **Answer (mzargham, typed by agent):** "no contributor floor (at this time) but capture the fact that the subject was
  raised and that setting a floor (such as excluding contributions on the basis of SDN listed parties in an option but
  it would only be implementable if we had a means of screening we were prepared to opt into. at this time i chose no
  floor on the basis of unrealistic to implement the screening and adequacy of control at the code review level
  (controlling codeowners not code contributors)"
- **Outcome:** No floor on contributors. Recorded as considered and declined, with the reasons: screening contributors
  (for example against the SDN list) is unrealistic to implement without a screening means OpenMBEE is prepared to
  opt into; and control at code review, by verified code owners, is adequate. A floor stays an option if such a means
  is adopted. Stated in `verified-code-owners` and listed among the candidates in `docs/current-state.md`.

## The split, as applied *(the supervisor's correction)*

- **Question:** Apply the two-policy split as proposed (A: contributing also lists every requirement on contributors;
  B: verified-code-owners states it restricts approvers, not contributors, and that no contributor floor is set)?
- **Answer (mzargham, typed by agent):** "Apply both"
- **Then, before the change was committed (typed by agent):** "strike that let's not overload contributing. that is
  about what is contributed not who contributes. that would a different policy and i think we just determined we don't
  have a contributors floor so we don't have another policy yet. the verified code-owners is where the personnel
  control resolves"
- **Outcome:** `contributing` is unchanged by the split: it governs what is contributed (its §3.H change, approved
  earlier, stands). A policy on who may contribute would be a separate policy, and with no contributor floor there is
  none yet. `verified-code-owners` is where the personnel control resolves: it states that it restricts who may
  approve and merge, not who may contribute, and records the declined floor. The memo's §2.C(1) moves to
  `codeowners` (a citation).

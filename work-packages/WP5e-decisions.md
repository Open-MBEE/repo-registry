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

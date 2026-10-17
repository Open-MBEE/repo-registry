# Testing and demonstration

> **DRAFT.** Nothing here is locked until mzargham says "lock." This document specifies the hypothetical case in
> prose. Fixtures and code come later.

Both testing and demonstration run on a **hypothetical case**. The live org will show high error, and its
taxonomy and policy are still under discussion. So correctness (testing) and understanding (demonstration) are
established first on a small made-up org, where every outcome is known in advance.

## The hypothetical case

A small fixture org (draft: about 10 repos), run on a draft or toy taxonomy and policy through the fixture
bindings (FM-11). It produces the same outputs as a live run (wiki pages and issue texts) as local files, and
publishes nothing. It exercises:

- every class in the taxonomy under test;
- one `unknown` repo (missing facts) and one `unclassified` repo (no class fits);
- one excluded repo (TX-5);
- one fork;
- one accepted deviation (PO-8);
- one archived repo, whose instructions must land in this repo (IF-4);
- a mix of conforming and violating repos, including configurations present, absent and unreadable (PO-7);
- one failed run (X-10).

## Testing: did we build what we designed?

Each requirement's "assessed by" column becomes a check against the hypothetical case: expected classes,
verdicts, routes and action log, plus replay (X-2) and the toy-taxonomy swap (FM-2). Tests run in Actions on every
policy-plane PR.

## Demonstration: can people use it?

A scripted walkthrough on the same case, for two audiences:

1. **Governors** (maintainers), to agree on the taxonomy and policy before going live: "here is what these rules
   would do to these repos." Changing the draft rules and re-running shows the consequences (X-6).
2. **Readers and operators** (community manager, repo owners, release officers): how to navigate the wiki, find a
   system-written issue in their own repo, answer an attestation, and close an issue when done.

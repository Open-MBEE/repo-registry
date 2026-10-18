# WP2a — Summary for the supervisor

> **PROVISIONAL** until the maintainers approve the policies (WP0, maintainer approval 2). This summary meets WP2a's
> Definition of good enough.

## The policy

`license-by-type` ([SOP](../docs/sops/license-by-type.md)) applies to every live repository except forks:

| Type | Allowed |
|---|---|
| tool | Apache-2.0 (default), MIT |
| media | CC-BY-4.0 for documentation and teaching material; Apache-2.0 or MIT where it's mostly code |
| research | Apache-2.0 or MIT for code, CC-BY-4.0 for writing, CDLA-Permissive-2.0 or CDLA-Sharing-1.0 for data |
| governance | Apache-2.0 |

Any other license needs an accepted exception in `data/deviations.yaml`, which is empty today. `project-files` now
checks only the README, so no two policies read the license.

## Grounding

- **OpenSSF charter clause:** code Apache-2.0 or MIT, documentation CC-BY-4.0, data CDLA.
- **CISA:** prefer a permissive license.
- **NumFOCUS** (researched first, as you asked) expects a standard, OSI-approved open source license, and counts mixed
  or missing licenses against a project. It says nothing about documents or data. No conflict.

## Today (`data/reports/license-report.yaml`)

115 live, classified repositories: **77 green, 38 red**.
- **32 have no license.** NumFOCUS's own example of a project it did not approve is one with some unlicensed
  repositories.
- **3 have a license GitHub can't recognize** (NOASSERTION).
- **3 have an off-list license, and need a decision** (a license change or an exception):
  - `architecture-based-risk-analysis` (tool, MPL-2.0);
  - `enhancement-proposals` (media, BSD-3-Clause);
  - `oosem.github.io` (media, CC0-1.0).

## Checks

`python3 -m unittest discover -s tests` passes, with 2 expected failures. `python3 scripts/policies.py` and
`python3 scripts/licenses.py --snapshot data/snapshots/2026-10-18` regenerate the table and the report.

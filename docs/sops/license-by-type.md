# The right license for the content

> **PROVISIONAL** until the maintainers approve the policies. Policy `license-by-type` (`data/policies/license-by-type.yaml`).

Every live repository has a license that OpenMBEE accepts for its type of content: Apache-2.0 or MIT for tools; CC-BY-4.0, Apache-2.0 or MIT for media; Apache-2.0, MIT, CC-BY-4.0 or a CDLA license for research; Apache-2.0 for governance. Any other license needs a recorded exception.

**Applies to:** every live repository (not archived ones, and not forks, which keep their upstream license). Your repository's kind is in [registry.yaml](../../registry.yaml).

| Your repository's type | Use | Also accepted |
|---|---|---|
| tool | Apache-2.0 | MIT |
| media | CC-BY-4.0 for documentation and teaching material | Apache-2.0 or MIT where the media is mostly code, such as the website |
| research | Apache-2.0 or MIT for code; CC-BY-4.0 for writing | CDLA-Permissive-2.0 or CDLA-Sharing-1.0 for data |
| governance | Apache-2.0 | — |

## Set up

1. Look up your repository's type in [registry.yaml](../../registry.yaml) and pick the license from the table above.
2. Add it as a `LICENSE` file at the root. On GitHub: Add file, then Create new file, name it `LICENSE`, and choose the license template GitHub offers. CC-BY-4.0 and the CDLA licenses aren't in GitHub's template list, so paste their official text instead (creativecommons.org, cdla.dev).
3. Check that GitHub detects it: the repository's main page shows the license name in the About box.
4. If you need a different license (for example because you depend on code under another license), ask the maintainers for an exception. They record it in `data/deviations.yaml` with the reason, and the check then shows green, marked as an exception.
5. Changing a license that contributors have already used can need their agreement. If in doubt, get legal advice, as CISA recommends.

## Automated checks

The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.

- **license-allowed**: `GET /repos/{owner}/{repo} -> license.spdx_id is in allowed_licenses for the repository's type (missing or NOASSERTION is red; an accepted exception in data/deviations.yaml is green, marked as an exception)` (needs Metadata: read)

## Attested checks

None.

## Why

- CISA: CISA-P-LICENSE-FILE, CISA-P-LICENSE-PERMISSIVE (see `data/sources/cisa-practices.yaml`)
- NIST SP 800-53: none
- OpenSSF's charter, via its project lifecycle (ossf/tac d019efe): code Apache-2.0 or MIT, data a Community Data License Agreement, specifications the Community Specification License 1.0, documentation CC-BY-4.0. NumFOCUS, OpenMBEE's fiscal sponsor, expects a standard open source (OSI-approved) license, and counts mixed or missing licenses against a project.

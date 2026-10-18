# Fit analysis

> **PROVISIONAL.** WP4 D-1. How well the draft taxonomy (WP1, with amendments A2 and A4) fits all of the org's
> public repositories, and what would make it fit better. Recommendations are candidates for later work, never
> applied here (WP4 OD3).

Data: the snapshot of 181 public repositories (`data/snapshots/2026-10-18`; 3 private repositories are
counted only), plus `repo-registry` itself, assigned. Kinds are the rules' recommendations (`registry.yaml`).

## Coverage

| Kind | Repos |
|---|---|
| tool/sandbox | 72 |
| tool/incubating | 15 |
| tool/archived | 21 |
| media/incubating | 22 |
| research/sandbox | 6 |
| governance/sandbox | 1 |
| unclassified | 45 |

By tier: low 78, unclassified 45, medium 37, none 21, high 1.

**137 of 182 repositories (75%) get a kind.** No repository gets two kinds (the rules are
mutually exclusive, a WP1 test). Graduated and the other assigned-only kinds have no repositories yet, because only the
maintainers give them.

## Unclassified repositories, by reason

- **A fork of an upstream project. The taxonomy has no kind for forks yet (WP0 parked item).** (25): `fprime`, `helix`, `IAlf`, `L4YAML`, `langserver.github.io`, `language-server-protocol`, `lsp-mode`, `lsp4ij`, `mason-registry`, `mms-python-client-feedstock`, `nvim-lspconfig`, `openapi-generator`, `opencode`, `opentelemetry-demo`, `opentelemetry-proto`, `opentelemetry-specification`, `PropertyKindCalculus`, `sbt-license-plugin`, `sbt-pack`, `staged-recipes`, `staged-recipes-opensysml`, `swagger-codegen`, `sysmlv2-rdf-ontology`, `syson`, `winget-pkgs`
- **No type signal. No media or research words, and no programming language.** (14): `apv-mdk`, `flexo-mms-ontology`, `flexo-pr-manager`, `flexo-sysmlv2-swagger`, `jl_scxml`, `md-cst-rabbitmq`, `mms-autocref`, `mms-migration`, `mms-rdf`, `starkit`, `structured-use-cases`, `sysmod-sysmlv2-api`, `trafo-v2-v1`, `websysml-core`
- **Archived, with no type signal. Inert whatever its type.** (6): `amazonaws`, `ems-config`, `mathematica-mdk-core`, `mms-mathematica-client`, `mvn-repo`, `zzProjectWiki`

## Where the type rules misfire (spot-checked)

Every live assignment was read by hand against its name and description. Most are right. These are not:

| Repository | Recommended | Better | Why the rule missed |
|---|---|---|---|
| `exec-mms-python-client-example` | tool/sandbox | media | It is an example. The word rule matches "examples", not "example" |
| `SysML-LoRD` | tool/sandbox | media | A SysML v2 example model (a game), though written in Go |
| `.github` | media/incubating | governance | The org's profile and default community files: it is about governing the org |
| `OpenSE-Cookbook`, `SysML-v2-Applications-and-Examples` | media | media (right) | Right, but only by name. Notebook-only repositories with no telling name fall to "no type signal" (for example `mms-rdf`, `mms-autocref`) |
| `concept-definition-stage`, `sysmlv2-testing` | tool/sandbox | tool or research | Borderline: research-like work written as code. The maintainers should choose |

## Archive candidates

74 live repositories have had no commits in the last 12 months. This is a hint, never a verdict (WP1). The pilot carries
six of them (`should-be-archived`), so that the maintainers can decide a few in the open. A notable group is the
heavily used `exec-*` tools (for example `exec-mms`, `exec-ve`, `exec-cameo-mdk`). They are still downloaded and
cloned, yet unchanged for a year. That is a maintenance question, not an archiving one.

## Recommendations (candidates for later work)

1. **Forks.** 25 repositories are forks, and the taxonomy has no kind for them. Recommend putting forks on the
   exclude list by default, with the reason "fork of an upstream project". Add a kind only for a fork OpenMBEE actively
   maintains (for example `staged-recipes-opensysml`, which packages OpenSysML). That would remove 25 of the
   45 unclassified repositories.
2. **Declare the type with a GitHub topic.** Almost no repository sets topics today (26 distinct topics across the org).
   One topic per type (for example `openmbee-tool`, `openmbee-media`, `openmbee-research`), set by each repository's
   CODEOWNERS, would make the type explicit, and the word rules a fallback. The kind itself would still be assigned by a
   governed pull request.
3. **Better word and file signals:** match "example" as well as "examples", and treat notebook-only and model-only
   repositories (`.ipynb`, `.sysml` files at the root) as media unless a research word applies. That would classify most
   of the 14 live repositories with no type signal.
4. **Archived repositories with no type** (6). Their tier is none whatever their type, so let an archived repository
   with no type signal take `tool/archived` by default, or add an archived kind that needs no type.
5. **The org's `.github` repository** belongs to the governance type, alongside `repo-registry`.

Recommendations 1 and 3 would together take the unclassified count from 45 to about 10.

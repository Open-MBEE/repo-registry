# WP4 — Summary for the supervisor

> Everything here is **PROVISIONAL** until the maintainers approve the pilot and the kinds (WP0 approvals 3 and 4).
> This summary meets WP4's Definition of good enough.

## The pilot ([pilot-briefing.md](../docs/pilot-briefing.md))

**32 repositories**, chosen by `data/pilot-rule.yaml` around your six must-includes:

| Category | Repos |
|---|---|
| Tools actively developed | OpenSysML, sysml-toolkit, flexo-mms-layer1-service, sysmlv2-python-client, sysmlv2-web-modeler, mtip-cameo |
| Tools heavily used (only those with clear evidence of use) | exec-cameo-mdk, exec-ve, exec-mms, exec-mmsri, exec-mdk-systems-reasoner |
| Media | open-mbee.github.io, opensysml.github.io, flexo-mms.openmbee.org, openmbee-graphic-assets, toaster (tutorial), TMT-SysML-Model |
| Research | flexo-conflict-resolution-policy-research, aircraftengine-simulation, lunar-lander-simulation, flexo-sysml2-adapter-experiment |
| Should be archived | mcf, K, mtip-sparx, openapi-graph-extractor, util, ve-confluence |
| Forks (unclassified on purpose) | staged-recipes-opensysml, sysmlv2-rdf-ontology |
| Other must-includes | flexo-mms-deployment, flexo-mms-sysmlv2, repo-registry |

The other 150 public repositories are on the exclude list (`data/exclude.yaml`), each with a reason.

**Use.** Clone counts were readable for 47 repositories, where you have push access. OpenSysML leads by far, with 3,869
clone visitors in 14 days and 9,338 release downloads. The `exec-*` tools are still downloaded and cloned, though
unchanged for a year.

## The fit analysis ([fit-analysis.md](../docs/fit-analysis.md))

- **137 of 182 repositories (75%) get a kind.** The 45 unclassified are 25 forks, 14 live repositories with no type
  signal, and 6 archived ones with no type signal.
- **Misfires found by spot-check:** `exec-mms-python-client-example` and `SysML-LoRD` are really media; `.github` is
  really governance; notebook-only repositories fall to "no type signal".
- **Recommendations, candidates for later work:**
  1. exclude forks by default, unless OpenMBEE actively maintains one;
  2. declare each repository's type with a GitHub topic;
  3. improve the word and file signals;
  4. give archived repositories with no type a default kind;
  5. move `.github` to governance.

  Recommendations 1 and 3 would take unclassified from 45 to about 10.

## For your attention

1. **7 pilot repositories are red on licensing today,** including `mtip-cameo` (unrecognized license) and
   `openmbee-graphic-assets` (none).
2. **The heavily used `exec-*` tools haven't changed in a year.** They are graduation candidates by use, but a
   maintenance question first.
3. **`mtip-cameo` counts as actively developed** (commits in the last 3 months). Its release tag is 1.0.9, so it is
   tool/incubating.

## Checks

`python3 -m unittest discover -s tests` passes (2 expected failures). The pilot, the exclude list and the briefing
regenerate exactly from the snapshot and the rule.

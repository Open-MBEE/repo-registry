# WP1 — Amendment 6: taxonomy refinements from the fit analysis (WP5c)

Made by [WP5c](WP5c-scope-of-work.md), approved by mzargham's merge 8197d77. Decisions are recorded verbatim in
[WP5c-decisions.md](WP5c-decisions.md). This record says how the taxonomy and the kind list changed.

## Where a kind comes from (OD1)

Each kind-list entry has a `source`: `inferred` (the rules' candidate), `topic` (its code owners declared the type
with exactly one `openmbee-<type>` topic) or `maintainer` (a maintainer's merged decision, stated as `decision`). The
supervisor: "the inference produces a candidate not a decision ... the order of priority is inferred->topic->
maintainer merged commit." Rules and topics never change a `maintainer` entry. `data/assignments.yaml` is folded in:
its decisions (the org, `repo-registry`) are now the kind list's `maintainer` entries.

## The rules

- **Type topics** (`type_topics` in `kinds.yaml`): `openmbee-tool`, `openmbee-media`, `openmbee-research`,
  `openmbee-governance`. Exactly one declares the type; none, or more than one, declares nothing. The stage still
  comes from the rules. A governance topic gives no candidate: governance kinds are assigned only.
- **Forks** (OD2), by our diff from the upstream (`forks.json`, one read-only compare per fork): with changes of ours,
  research, or media where our changes are mostly models; with none on the default branch, a mirror, left
  unclassified with that reason and excluded from the pilot with it.
- **Examples:** "examples" is no longer a media word. "example" alone decides no type: the purpose does (to show
  others, media; to learn for ourselves, research). Such a repository is unclassified with that reason unless other
  signals decide.
- **Notebook-only and model-only** repositories (no programming language; a Jupyter notebook, or `.ipynb`, `.sysml`,
  `.kerml`, `.xmi` or `.mdzip` files at the root) are media, unless a research word applies.
- **Archived with no type** (OD3) stay unclassified, with their reason.
- **`.github`** (OD4) is governance/graduated, a maintainer's decision.

## What changed

The refresh (`scripts/refresh_kind_list.py`) applied the new rules to the candidate entries: 6 repositories gained a
kind (`IAlf` research/sandbox; `sysmlv2-rdf-ontology`, `md-cst-rabbitmq`, `mms-autocref`, `mms-rdf`, `starkit`
media/incubating), the 23 mirrors and 10 live repositories with no type signal got their new reasons, and `.github`
became governance/graduated by decision. Unclassified: 45 before, 39 after (the fit report view gives them by reason).
The kept pilot list is unchanged.

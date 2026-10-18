#!/usr/bin/env python3
"""Render the maintainer review pack: this repository's wiki pages, from the model (WP5d D-2, D-6).

A view (WP5b): rendered, never committed, never edited by hand. Demo mode writes the pages into <out>/wiki/; live
mode (scripts/render.py --mode live) publishes the same pages to this repository's wiki. The pages: Home, Taxonomy,
Repositories, Policies, one SOP-<policy> page per policy, Sources, one Source-<source> page per cited source, and
_Sidebar. Every row links to the model file that holds it, with GitHub's edit link: a change is a pull request to
that file (WP5d OD1). Every page says PROVISIONAL; the sidebar, shown on every page, names the commit rendered.

Links between pages are wiki links, `[text](Page#anchor)`; anchors are GitHub's heading anchors (`anchor()`).

Usage: python3 scripts/wiki.py [--out build/demo]   (reads build/demo/reports/policy-applicability.yaml)
"""
import argparse
import pathlib
import re
import subprocess
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model  # noqa: E402
import policies as P  # noqa: E402
import sops  # noqa: E402

GITHUB = "https://github.com/Open-MBEE"
REPO = f"{GITHUB}/repo-registry"
BLOB, EDIT = f"{REPO}/blob/main", f"{REPO}/edit/main"

# The cited sources, in the order and with the roles of docs/policy-basis-review.md ("The sources"). Those with an
# item file in data/sources/ get a page; the rest are cited as a whole, and link to the document that reads them.
SOURCES = [
    {"id": "cisa", "short": "CISA practices", "file": "data/sources/cisa-practices.yaml", "items": "practices", "role": "Core",
     "name": "CISA, Open Source Software: Security Principles and Practices"},
    {"id": "nist", "short": "NIST SP 800-53", "file": "data/sources/nist-800-53.yaml", "items": "controls", "role": "Core",
     "name": "NIST SP 800-53 Rev. 5, the controls cited"},
    {"id": "nist-rmf", "role": "Core", "name": "NIST SP 800-37 Rev. 2, the Risk Management Framework",
     "read": "Official PDF; the step map is in WP0", "doc": "work-packages/WP0-scope-of-work.md"},
    {"id": "openssf", "short": "OpenSSF baseline", "file": "data/sources/openssf-security-baseline.yaml", "items": "items", "role": "Core, backbone",
     "name": "OpenSSF security baseline, by stage"},
    {"id": "openssf-lifecycle", "role": "Core", "name": "OpenSSF project lifecycle (the stages)",
     "read": "ossf/tac commit d019efe", "doc": "docs/lifecycle-stage-map.md"},
    {"id": "cncf-lifecycle", "role": "Secondary", "name": "CNCF project lifecycle (the stages)",
     "read": "cncf/toc commit d815451", "doc": "docs/lifecycle-stage-map.md"},
    {"id": "iso12207", "short": "ISO/IEC/IEEE 12207", "file": "data/sources/iso12207-clauses.yaml", "items": "clauses", "role": "Secondary",
     "name": "ISO/IEC/IEEE 12207:2026, by clause number and title only (no text of the standard is committed)"},
]
ITEM_WORD = {"cisa": "practice", "nist": "control", "openssf": "item", "iso12207": "clause"}


def anchor(heading):
    """GitHub's anchor for a heading: lower case, punctuation dropped, spaces to hyphens."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def cell(text):
    """One table cell: on one line, its pipes escaped, and `<` and `>` escaped outside code spans (GitHub strips
    them as HTML, so `openmbee-<type>` would lose its `<type>`)."""
    parts = " ".join(str(text).split()).replace("|", "\\|").split("`")
    return "`".join(p if i % 2 else p.replace("<", "&lt;").replace(">", "&gt;") for i, p in enumerate(parts))


def commit(root):
    run = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
    return run.stdout.strip() if run.returncode == 0 else "unknown"


def line_of(root, rel, *patterns):
    """The line number of the first line matching the last pattern, after lines matching each earlier one in turn."""
    lines, start = (pathlib.Path(root) / rel).read_text().splitlines(), 0
    for pat in patterns:
        start = next(i for i in range(start, len(lines)) if re.match(pat, lines[i])) + 1
    return start


def held_in(rel, line=None, label=None):
    """Where a row is held: the model file (at its line), and GitHub's edit link for a pull request."""
    where = f"{BLOB}/{rel}" + (f"#L{line}" if line else "")
    return f"[{label or rel.split('/')[-1]}]({where}) · [edit]({EDIT}/{rel})"


def header(title, what):
    """A page's title and banner. The commit a publish was rendered from is named once, in the sidebar, which GitHub
    shows on every page, so a change to the commit alone alters one page (WP5d, observation 3)."""
    return [f"# {title}", "",
            "> **PROVISIONAL** until the OpenMBEE maintainers approve it. Rendered by `scripts/wiki.py` from the commit "
            f"named in the sidebar; never edit this wiki by hand: each publish replaces it. {what} To "
            "propose a change, open a pull request to the model file linked on each row "
            "([how](Home#how-to-propose-a-change)).", ""]


def kind_link(name):
    return f"[{name}](Taxonomy#{anchor(name)})"


def in_words(pred, explain, depth=0):
    """A predicate of the kinds.yaml language, as nested Markdown bullets of plain words."""
    pad = "  " * depth
    if pred is False:
        return [f"{pad}- Never: the rules never give this kind; only a maintainer's decision does."]
    if "all" in pred or "any" in pred:
        key = "all" if "all" in pred else "any"
        out = [f"{pad}- {'All' if key == 'all' else 'Any'} of these:"]
        for p in pred[key]:
            out += in_words(p, explain, depth + 1)
        return out
    if "not" in pred:
        inner = pred["not"]
        if "signal" in inner:
            text = explain[inner["signal"]]
            return [f"{pad}- Not: {text[0].lower()}{text[1:]}"]
        return [f"{pad}- None of this holds:"] + in_words(inner, explain, depth + 1)
    if "signal" in pred:
        return [f"{pad}- {explain[pred['signal']]}"]
    if "attr" in pred:
        return [f"{pad}- {attr_words(pred)}"]
    raise ValueError(f"bad predicate: {pred!r}")


def attr_words(pred):
    attr = pred["attr"]
    op = next(k for k in pred if k != "attr")
    arg = pred[op]
    if op == "eq":
        return f"its {attr} is {arg}" if arg is not None else f"it has no {attr}"
    if op == "in":
        return f"its {attr} is {' or '.join(map(str, arg))}"
    return f"its {attr} {dict(gt='is more than', gte='is at least', lt='is less than', matches='matches')[op]} {arg}"


def rule_words(pred):
    """An applies-if rule (type, stage and tier only), as one sentence."""
    if pred is True:
        return "always"
    if "all" in pred:
        return " and ".join(rule_words(p) for p in pred["all"])
    if "any" in pred:
        return "(" + " or ".join(rule_words(p) for p in pred["any"]) + ")"
    if "not" in pred:
        inner = pred["not"]
        if "attr" in inner and "eq" in inner:
            return f"its {inner['attr']} is not {inner['eq']}"
        return f"not ({rule_words(inner)})"
    return attr_words(pred)


class Pack:
    def __init__(self, root, out):
        self.root, self.out = pathlib.Path(root), pathlib.Path(out)
        self.sha = commit(self.root)
        self.kinds_doc = model.load("data/taxonomy/kinds.yaml", self.root)
        self.kinds = model.kinds(self.kinds_doc)
        self.tiers = model.load("data/taxonomy/tiers.yaml", self.root)["tiers"]
        self.registry = model.load("registry.yaml", self.root)
        self.repos = model.repos(self.root)
        self.pilot = set(model.load("data/pilot.yaml", self.root)["repos"])
        self.pols, self.departures = P.load_policies(self.root / "data/policies")
        self.by_policy = yaml.safe_load((self.out / "reports/policy-applicability.yaml").read_text())["policies"]
        self.explain = self.kinds_doc["explain"]
        self.sources = {s["id"]: s for s in SOURCES}
        self.items = {s["id"]: {str(k): v for k, v in model.load(s["file"], self.root)[s["items"]].items()}
                      for s in SOURCES if "file" in s}

    def tier_of(self, name):
        return self.kinds[name]["tier"]

    def cite(self, source, ref):
        return f"[{ref}](Source-{source}#{anchor(ref)})" if source in self.items else ref

    def cited_by(self, source):
        out = {}
        for pid, p in sorted(self.pols.items()):
            refs = p["cites"].get(source)
            for ref in (refs if isinstance(refs, list) else []):
                out.setdefault(str(ref), []).append(pid)
        return out

    # --- pages ---------------------------------------------------------------------------------------------------
    def home(self):
        n_repos = len(self.registry["repos"])
        L = header("OpenMBEE repository registry: the review pack",
                   "The model it shows is in [Open-MBEE/repo-registry](" + REPO + ").")
        L += ["This wiki summarizes the registry's model for the maintainers' review: what kinds and tiers mean, what "
              "each repository is and why, what each policy asks and of whom, and where each policy comes from.", "",
              "| Page | What it shows |", "|---|---|",
              "| [Taxonomy](Taxonomy) | The types, stages and tiers; every kind, its tier, and how a repository gets it "
              "(the rules' heuristics in words, a type topic, or a maintainer's decision) |",
              f"| [Repositories](Repositories) | All {n_repos} repositories, and the organization's administration, "
              "grouped by kind, with tier, source of the kind, and the pilot marked |",
              f"| [Policies](Policies) | All {len(self.pols)} policies: the kinds and tiers each is in effect for, its "
              "rule in words, its citations, and its SOP page |",
              "| [Sources](Sources) | The cited sources, and for each item the policies that adopt it, or why we "
              "depart from it |", "",
              "## What we ask of you", "",
              "Read the pack, and either agree or propose a change. The OpenMBEE maintainers approve, in turn: the "
              "taxonomy ([Taxonomy](Taxonomy)), the policies ([Policies](Policies) and their SOPs), the pilot "
              "(marked on [Repositories](Repositories)), each pilot repository's kind, and the named maintainers. "
              "Until then everything here is PROVISIONAL.", "",
              "## How the model fits together", "",
              "A repository has a **type** and a **stage** in its lifecycle. Together they name its **kind**, and the "
              "kind gives its **tier**, which says how strict the controls are. Each policy says, with a rule over "
              "type, stage and tier, where it is in effect. So a repository's kind decides which policies apply to "
              "it. A kind says what a repository is, not whether its duties are done: that is checked by the "
              "policies, later (WP6).", "",
              "## How to propose a change", "",
              "Every row on these pages links to the file in the repository that holds it, with an **edit** link. A "
              "change is a pull request to that file:", "",
              "1. Read the row's source first: the [Taxonomy](Taxonomy) says how a kind is given, and the "
              "[Sources](Sources) say where each policy comes from.",
              "2. Click **edit** on the row, change the record, and open a pull request with your reason.",
              "3. The check `check` validates the model on every pull request; an invalid change can't be merged. The "
              "pull request's checks also show how the change would alter these pages.",
              "4. Who merges: a kind change, any maintainer; the maintainer list and maintainers' powers, an owner "
              f"([current-state.md]({BLOB}/docs/current-state.md)). The wiki is republished from `main` after the "
              "merge.", "",
              "A repository's code owners can also declare its type themselves, with one `openmbee-<type>` GitHub "
              "topic ([Taxonomy](Taxonomy#how-a-type-is-declared))."]
        return L

    def taxonomy(self):
        kd = self.kinds_doc
        L = header("Taxonomy", "From `data/taxonomy/kinds.yaml` and `data/taxonomy/tiers.yaml`.")
        L += ["## Types", "", "| Type | Meaning | Held in |", "|---|---|---|"]
        L += [f"| {t} | {cell(m)} | {held_in('data/taxonomy/kinds.yaml', line_of(self.root, 'data/taxonomy/kinds.yaml', '^types:', f'^  {t}:'))} |"
              for t, m in kd["types"].items()]
        L += ["", "## Stages", "", "Adopted from the CNCF and OpenSSF project lifecycles ([Sources](Sources)).", "",
              "| Stage | Meaning | Held in |", "|---|---|---|"]
        L += [f"| {s} | {cell(m)} | {held_in('data/taxonomy/kinds.yaml', line_of(self.root, 'data/taxonomy/kinds.yaml', '^stages:', f'^  {s}:'))} |"
              for s, m in kd["stages"].items()]
        L += ["", "## Tiers", "", "A tier says how strict the controls are. A kind gives the tier.", "",
              "| Tier | Meaning | Kinds | Held in |", "|---|---|---|---|"]
        for t, row in sorted(self.tiers.items(), key=lambda kv: kv[1]["order"]):
            ks = ", ".join(kind_link(k) for k, v in self.kinds.items() if v["tier"] == t)
            L.append(f"| {t} | {cell(row['meaning'])} | {ks} | "
                     f"{held_in('data/taxonomy/tiers.yaml', line_of(self.root, 'data/taxonomy/tiers.yaml', '^tiers:', f'^  {t}:'))} |")
        counts = {}
        for e in self.registry["repos"].values():
            if "reason" not in e:
                counts[model.kind_of(e)] = counts.get(model.kind_of(e), 0) + 1
        L += ["", "## Kinds", "", "| Kind | Tier | Given by the rules? | Repositories |", "|---|---|---|---|"]
        for k, v in self.kinds.items():
            L.append(f"| {kind_link(k)} | {v['tier']} | {'no, a decision only' if v['recommend_when'] is False else 'yes'} "
                     f"| [{counts.get(k, 0)}](Repositories#{anchor(k)}) |")
        L.append("")
        for k, v in self.kinds.items():
            line = line_of(self.root, "data/taxonomy/kinds.yaml", "^kinds:", f"^  {v['type']}:", f"^    {v['stage']}:")
            L += [f"### {k}", "", f"**Tier:** {v['tier']}. **Held in:** {held_in('data/taxonomy/kinds.yaml', line)}", "",
                  cell(v["meaning"]), "", "**How a repository gets it:**", ""]
            if v["recommend_when"] is False:
                L.append("- The rules never give this kind; only a maintainer's decision does.")
            else:
                rule = v["recommend_when"]
                if "all" in rule:
                    L.append("- The rules give it when all of these hold:")
                    for p in rule["all"]:
                        L += in_words(p, self.explain, 1)
                else:
                    L.append("- The rules give it when:")
                    L += in_words(rule, self.explain, 1)
                if v["type"] != "governance":
                    L.append(f"- Or its code owners declare the type {v['type']} with the `openmbee-{v['type']}` topic, "
                             "and the rules give the stage.")
            L += ["- Or a maintainer decides it, by a merged pull request to `registry.yaml`, which no rule or topic "
                  "changes afterwards.", ""]
        omitted = model.omitted(kd)
        if omitted:
            L += ["## Not defined", "", "| Type and stage | Why no kind | Held in |", "|---|---|---|"]
            for name, reason in omitted.items():
                t, s = name.split("/")
                line = line_of(self.root, "data/taxonomy/kinds.yaml", "^omitted:", f"^  {t}:", f"^    {s}:")
                L.append(f"| {name} | {cell(reason)} | {held_in('data/taxonomy/kinds.yaml', line)} |")
            L.append("")
        L += ["## How a type is declared", "",
              "A repository's code owners can declare its type with exactly one of these GitHub topics. A topic "
              "declares the type only; the stage still comes from the rules or a maintainer's decision. None, or more "
              "than one, declares nothing. Precedence: the rules, then the topic, then a maintainer's decision.", "",
              "| Topic | Type | Held in |", "|---|---|---|"]
        L += [f"| `{topic}` | {t} | "
              f"{held_in('data/taxonomy/kinds.yaml', line_of(self.root, 'data/taxonomy/kinds.yaml', '^type_topics:', f'^  {topic}:'))} |"
              for topic, t in kd["type_topics"].items()]
        L += ["", "## Why a repository is unclassified", "",
              "The rules leave a repository unclassified when no kind, or more than one, matches. The first reason "
              "below that holds is the one given.", "", "| Reason | Held in |", "|---|---|"]
        reasons_at = line_of(self.root, "data/taxonomy/kinds.yaml", "^unclassified_reasons:")
        L += [f"| {cell(r['reason'])} | {held_in('data/taxonomy/kinds.yaml', reasons_at)} |"
              for r in kd["unclassified_reasons"]]
        L += ["", "## Signals", "", "The building blocks of the rules above, in words. The exact rule of each is in "
              "`data/taxonomy/kinds.yaml`.", "", "| Signal | In words | Held in |", "|---|---|---|"]
        for s in kd["signals"]:
            line = line_of(self.root, "data/taxonomy/kinds.yaml", "^explain:", f"^  {s}:")
            L.append(f"| `{s}` | {cell(self.explain[s])} | {held_in('data/taxonomy/kinds.yaml', line)} |")
        return L

    def repositories(self):
        reg = self.registry["repos"]
        groups = {k: [] for k in self.kinds}
        unclassified = []
        for rid, e in reg.items():
            (unclassified if "reason" in e else groups[model.kind_of(e)]).append((rid, e))
        L = header("Repositories", "From the kind list, `registry.yaml`, and the pilot, `data/pilot.yaml`.")
        L += [f"Every repository of the organization ({len(reg)}), grouped by kind, with the unclassified ones last. "
              "**Source** says where the kind came from: `inferred` (the rules), `topic` (its code owners' "
              "`openmbee-<type>` topic) or `maintainer` (a maintainer's merged decision). **Pilot** marks the "
              f"{len(self.pilot)} repositories in the pilot.", "",
              "| Kind | Tier | Repositories |", "|---|---|---|"]
        L += [f"| [{k}](#{anchor(k)}) | {self.tier_of(k)} | {len(rows) + (k == model.kind_of(self.registry['org']))} |"
              for k, rows in groups.items()]
        L += [f"| [unclassified](#unclassified) | none yet | {len(unclassified)} |", ""]
        reg_line = {int(m.group(1)): i + 1 for i, ln in enumerate((self.root / "registry.yaml").read_text().splitlines())
                    if (m := re.match(r"^  (\d+):", ln))}
        org = self.registry["org"]
        for k, rows in groups.items():
            L += [f"## {k}", "", f"{kind_link(k)}, tier {self.tier_of(k)}.", ""]
            if k == model.kind_of(org):
                rows = [(None, org)] + rows
            if not rows:
                L += ["None.", ""]
                continue
            L += ["| Repository | Kind | Tier | Source | Pilot | Entry |", "|---|---|---|---|---|---|"]
            for rid, e in rows:
                if rid is None:
                    name = f"[{org['name']}]({GITHUB}) (the organization's administration)"
                    entry = held_in("registry.yaml", line_of(self.root, "registry.yaml", "^org:"), "registry.yaml")
                else:
                    name = f"[{e['name']}]({GITHUB}/{e['name']})"
                    entry = held_in("registry.yaml", reg_line[rid], "registry.yaml")
                source = e["source"] + (f": {cell(e['decision'])}" if e.get("decision") else "")
                L.append(f"| {name} | {k} | {self.tier_of(k)} | {source} | "
                         f"{'pilot' if rid in self.pilot else ''} | {entry} |")
            L.append("")
        L += ["## unclassified", "",
              "No kind yet, so no tier and no policies. The reason says why "
              "([Taxonomy](Taxonomy#why-a-repository-is-unclassified)); a type topic or a maintainer's decision can "
              "give one.", "", "| Repository | Reason | Source | Pilot | Entry |", "|---|---|---|---|---|"]
        for rid, e in unclassified:
            L.append(f"| [{e['name']}]({GITHUB}/{e['name']}) | {cell(e['reason'])} | {e['source']} | "
                     f"{'pilot' if rid in self.pilot else ''} | {held_in('registry.yaml', reg_line[rid], 'registry.yaml')} |")
        return L

    def policies(self):
        order = {t: r["order"] for t, r in self.tiers.items()}
        L = header("Policies", "From `data/policies/`, and which kinds each is in effect for.")
        L += [f"The {len(self.pols)} policies. Each is in effect for the kinds its rule selects, over type, stage and "
              "tier only; its tiers are the tiers of those kinds. Below the summary, each policy has its kinds, its "
              "citations (linked to the [Sources](Sources)), its SOP (how to set it up and how it is checked) and the "
              "file that holds it.", "",
              "| Policy | What it asks | In effect when | Tiers |", "|---|---|---|---|"]
        rows, sections = [], []
        for pid, p in sorted(self.pols.items(), key=lambda kv: kv[1]["name"].lower()):
            ks = self.by_policy.get(pid, [])
            tiers = ", ".join(sorted({self.tier_of(k) for k in ks}, key=order.get)) or "—"
            rule = rule_words(p["applies_if"])
            rows.append(f"| [{cell(p['name'])}](#{anchor(p['name'])}) | {cell(p['meaning'])} | {cell(rule)} | {tiers} |")
            cites = []
            for s in ("cisa", "nist", "openssf", "iso12207"):
                refs = p["cites"].get(s)
                if isinstance(refs, list) and refs:
                    cites.append(f"- {self.sources[s]['short']}: " + ", ".join(self.cite(s, str(r)) for r in refs))
            sections += [f"## {p['name']}", "", cell(p["meaning"]), "",
                         f"- **Governs:** {'the organization' if p['scope'] == 'org' else 'a repository'}",
                         f"- **In effect when:** {cell(rule)}",
                         f"- **Kinds:** {', '.join(kind_link(k) for k in ks) or '—'}",
                         f"- **Tiers:** {tiers}",
                         f"- **SOP:** [{cell(p['name'])}](SOP-{pid})",
                         f"- **Held in:** {held_in(f'data/policies/{pid}.yaml')}",
                         "- **Citations:**"] + ["  " + c for c in cites] + [""]
        L += rows + ["", "## By kind", "", "| Kind | Tier | Policies in effect |", "|---|---|---|"]
        for k in self.kinds:
            ps = [q for q in sorted(self.pols) if k in self.by_policy.get(q, [])]
            links = ", ".join(f"[{cell(self.pols[q]['name'])}](SOP-{q})" for q in ps) or "—"
            L.append(f"| {kind_link(k)} | {self.tier_of(k)} | {links} |")
        return L + [""] + sections

    def sop(self, pid):
        text = sops.render(self.pols[pid], self.by_policy.get(pid, []), table=("Policies", "Policies"), cite=self.cite,
                          banner=False)
        body = text.split("\n")
        body = body[1:] if body[0].startswith("# ") else body
        return header(f"SOP: {self.pols[pid]['name']}",
                      f"From [`data/policies/{pid}.yaml`]({BLOB}/data/policies/{pid}.yaml) "
                      f"([edit]({EDIT}/data/policies/{pid}.yaml)).") + body

    def sources_page(self):
        L = header("Sources", "From `data/sources/` and `data/policies/_departures.yaml`.")
        L += ["Where the policies come from. Each core and secondary source, the version read, and, for those cited "
              "item by item, a page with each item and the policies that adopt it, or why we depart from it. The "
              f"narrative is [policy-basis-review.md]({BLOB}/docs/policy-basis-review.md).", "",
              "| Source | Role | Version read | Items | Held in |", "|---|---|---|---|---|"]
        for s in SOURCES:
            if "file" in s:
                n = len(self.items[s["id"]])
                name = f"[{s['name']}](Source-{s['id']})"
                L.append(f"| {name} | {s['role']} | {cell(self.version(s))} | {n} {ITEM_WORD[s['id']]}s | "
                         f"{held_in(s['file'])} |")
            else:
                L.append(f"| {s['name']} | {s['role']} | {s['read']} | cited as a whole | "
                         f"[{s['doc'].split('/')[-1]}]({BLOB}/{s['doc']}) |")
        return L

    def version(self, s):
        head = model.load(s["file"], self.root).get("source") or {}
        if s["id"] == "cisa":
            return f"[{head['date']}]({head['url']}); {head.get('note', '')}"
        if s["id"] == "nist":
            return (f"{head['catalog']}, [{head['repo']} {head['commit'][:7]}]"
                    f"(https://github.com/{head['repo']}/blob/{head['commit']}/{head['path']})")
        if s["id"] == "openssf":
            return f"[{head['repo']} {head['commit']}](https://github.com/{head['repo']}/blob/{head['commit']}/{head['path']})"
        return f"{head.get('standard')}, edition {head.get('edition')}"

    def source_page(self, sid):
        s, items = self.sources[sid], self.items[sid]
        adopted, departed = self.cited_by(sid), self.departures.get(sid) or {}
        word = ITEM_WORD[sid]
        L = header(f"Source: {s['name']}", f"From `{s['file']}`.")
        L += [f"{s['role']} source. Version read: {self.version(s)}. Back to [Sources](Sources).", "",
              f"{len(items)} {word}s: {sum(1 for i in items if i in adopted)} adopted by a policy, "
              f"{sum(1 for i in items if i in departed)} departed from with a reason"
              + (f", {sum(1 for i in items if i not in adopted and i not in departed)} cited by no policy, each with its context"
                 if any(i not in adopted and i not in departed for i in items) else "") + ".", ""]
        L += [f"| {word.capitalize()} | {'Section' if sid == 'cisa' else 'Title'} | Adopted by, or departed |", "|---|---|---|"]
        for ref, row in items.items():
            what = row["section"] if sid == "cisa" else row["title"]
            by = (", ".join(f"[{cell(self.pols[q]['name'])}](SOP-{q})" for q in adopted[ref]) if ref in adopted
                  else "departed from, with a reason" if ref in departed else "no policy (context below)")
            L.append(f"| [{ref}](#{anchor(ref)}) | {cell(what)} | {by} |")
        L.append("")
        for ref, row in items.items():
            pat = re.compile(rf'^  "?{re.escape(ref)}"?:')
            line = next(i + 1 for i, ln in enumerate((self.root / s["file"]).read_text().splitlines()) if pat.match(ln))
            L += [f"### {ref}", "", self.describe(sid, row), "", f"Held in: {held_in(s['file'], line)}", ""]
            if ref in adopted:
                L.append("**Adopted by:** " + ", ".join(f"[{self.pols[q]['name']}](SOP-{q})" for q in adopted[ref]))
            elif ref in departed:
                dl = line_of(self.root, "data/policies/_departures.yaml", f"^{sid}:", rf"^  {re.escape(ref)}:")
                L.append(f"**Departed from:** {cell(departed[ref])} ({held_in('data/policies/_departures.yaml', dl)})")
            else:
                L.append(f"**Cited by no policy:** {cell(row.get('context') or 'no context stated')}")
            L.append("")
        return L

    def describe(self, sid, row):
        if sid == "cisa":
            return f"{cell(row['practice'])} (page {row['page']}, {cell(row['section'])})"
        if sid == "openssf":
            return f"{cell(row['title'])} (stage {row['stage']}, {row['when']})"
        if sid == "nist":
            return cell(row["title"]) + (f" (an enhancement of {row['parent']})" if row.get("parent") else "")
        return cell(row["title"])

    def sidebar(self):
        L = ["**[Home](Home)**", "", "- [Taxonomy](Taxonomy)", "- [Repositories](Repositories)",
             "- [Policies](Policies)", "- [Sources](Sources)", "", "**SOPs**", ""]
        L += [f"- [{self.pols[q]['name']}](SOP-{q})" for q in sorted(self.pols, key=lambda q: self.pols[q]["name"].lower())]
        L += ["", "**Sources**", ""] + [f"- [{s['short']}](Source-{s['id']})" for s in SOURCES if "file" in s]
        L += ["", f"Rendered from [`{self.sha[:7]}`]({REPO}/tree/{self.sha}). PROVISIONAL."]
        return L

    def pages(self):
        out = {"Home": self.home(), "Taxonomy": self.taxonomy(), "Repositories": self.repositories(),
               "Policies": self.policies(), "Sources": self.sources_page(), "_Sidebar": self.sidebar()}
        out.update({f"SOP-{q}": self.sop(q) for q in sorted(self.pols)})
        out.update({f"Source-{s}": self.source_page(s) for s in self.items})
        return {name: "\n".join(lines).rstrip() + "\n" for name, lines in out.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="build/demo")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    out = pathlib.Path(args.out)
    pages = Pack(args.root, out).pages()
    (out / "wiki").mkdir(parents=True, exist_ok=True)
    for name, text in pages.items():
        (out / "wiki" / f"{name}.md").write_text(text)
    print(f"wrote {len(pages)} wiki pages to {out / 'wiki'}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Write the pilot briefing for the supervisor and then the maintainers (WP4 D-4).

Deterministic and offline: reads data/pilot.yaml, the taxonomy, the policy applicability report, the license report
and the usage snapshot. Plain language (WP4 R-7).

Usage: python3 scripts/briefing.py [--out build/demo]   (a view, rendered, never committed: WP5b OD4; it reads the
views policies.py, licenses.py and recommend.py wrote into --out)
"""
import argparse
import collections
import json
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="build/demo")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root, out = pathlib.Path(args.root), pathlib.Path(args.out)
    view = lambda p: yaml.safe_load((out / p).read_text())  # noqa: E731
    registry = model.load("registry.yaml", root)["repos"]
    pilot = {rid: {**e, "kind": model.kind_of(registry[rid])} for rid, e in model.load("data/pilot.yaml", root)["repos"].items()}
    rule = model.load("data/pilot-rule.yaml", root)
    kinds = model.kinds(model.load("data/taxonomy/kinds.yaml", root))
    appl = view("reports/policy-applicability.yaml")["kinds"]
    lic = view("reports/license-report.yaml")["repos"]
    usage = json.loads((model.snapshot_dir(root) / "usage.json").read_text())["repos"]
    meanings = {c["id"]: " ".join(c["meaning"].split()) for c in rule["categories"]}

    def use(name):
        u = usage.get(name)
        if not u:
            return "not measured"
        c = u["clones_14d"]
        clones = f"{c['uniques']} clone visitors in 14 days" if c["readable"] else "clones not readable"
        return f"{clones}; {u['release_downloads'] or 0} release downloads"

    by_cat = collections.defaultdict(list)
    for rid, p in pilot.items():
        by_cat[p["category"]].append(rid)
    order = [c["id"] for c in rule["categories"]] + ["must-include"]
    L = ["# Pilot briefing", "",
         "> **PROVISIONAL.** WP4 D-4. A view, rendered by `scripts/briefing.py` (WP5b OD4). The proposed pilot, for the",
         "> supervisor's review and then the maintainers' approval of the pilot subset and of each repository's kind",
         "> (WP0 approvals 3 and 4). It shows which policies each repository would carry. Whether it meets them is WP6.", "",
         f"**{len(pilot)} repositories** are proposed (target 24 to 36). Every other public repository is on the exclude list",
         "(`data/exclude.yaml`), with a reason. Must-includes were named by the supervisor. The rest were chosen by the rule",
         "in `data/pilot-rule.yaml`: most used first, where use means release downloads, clone visitors (readable only",
         "where the supervisor has push access), stars and forks.", "",
         "## How to read this", "",
         "- **Kind** = type / stage. The type is what a repository is: tool, media (website, documentation, teaching",
         "  material, example models), research, or governance. The stage comes from the CNCF and OpenSSF project",
         "  lifecycles ([lifecycle-stage-map.md](lifecycle-stage-map.md)):",
         "  - **sandbox** means early and experimental; for a tool, no release yet or releases below 1.0;",
         "  - **incubating** means stabilizing and in use; for a tool, version 1.0 or later;",
         "  - **graduated** means mature and widely used, given only by the maintainers;",
         "  - **archived** means read-only.",
         "- **Tier** = how strict the controls are: **high** (graduated tools, and established governance such as the",
         "  org's administration), **medium** (tools at incubating, and media people rely on), **low** (a named owner and",
         "  little else; this registry while it is being set up), **none** (archived).",
         "- **Policies** = the named policies a repository would carry, linked to their plain-language SOPs. The full",
         "  table is [policy-applicability.md](policy-applicability.md). This briefing shows what *would* apply, not",
         "  whether a repository meets it yet.",
         "- **Why OpenSysML is sandbox and low.** It is by far the most used tool, but its releases are still below",
         "  1.0. By the maintainers' rule (amendment A4), a tool stays in sandbox, with light controls, until it",
         "  releases 1.0, so that fast development isn't slowed. At 1.0 it becomes incubating (medium) and carries 11",
         "  policies instead of 3. The same holds for sysml-toolkit and the Flexo MMS tools.", ""]
    for cat in order:
        rids = sorted(by_cat.get(cat, []), key=lambda r: pilot[r]["name"].lower())
        if not rids:
            continue
        title = cat.replace("-", " ").capitalize()
        L += [f"## {title} ({len(rids)})", ""]
        if cat in meanings:
            L += [meanings[cat], ""]
        else:
            L += ["Named by the supervisor, outside the categories above.", ""]
        L += ["| Repository | Proposed kind | Tier | Policies it would carry | License | Use |", "|---|---|---|---|---|---|"]
        for rid in rids:
            n, kind = pilot[rid]["name"], pilot[rid]["kind"]
            tier = kinds[kind]["tier"] if kind in kinds else "—"
            pol = (", ".join(f"[{p}](sops/{p}.md)" for p in appl.get(kind, [])) or "—") if kind in kinds else \
                "none (forks have no kind)"
            l = lic.get(rid)
            licence = (f"{l['license'] or 'none'} ({l['color']})" if l else "not covered")
            must = (" (must-include)" if pilot[rid]["reason"].startswith("must-include")
                    else " (registers itself)" if pilot[rid]["reason"].startswith("registers itself") else "")
            L.append(f"| `{n}`{must} | {kind} | {tier} | {pol} | {licence} | {use(n)} |")
        L.append("")
    kinds_count = collections.Counter(p["kind"] for p in pilot.values())
    tiers = collections.Counter(kinds[k]["tier"] if k in kinds else "unclassified" for k in
                                (p["kind"] for p in pilot.values()))
    reds = sorted(pilot[r]["name"] for r in pilot if lic.get(r, {}).get("color") == "red")
    flags = view("reports/kind-recommendations.yaml")["repos"]
    dormant = sorted((pilot[r]["name"] for r in pilot if "archive-candidate" in flags.get(r, {}).get("flags", [])),
                     key=str.lower)
    L += ["## At a glance", "",
          f"- **Kinds in the pilot:** {', '.join(f'{k} {c}' for k, c in sorted(kinds_count.items()))}.",
          f"- **Tiers:** {', '.join(f'{t} {c}' for t, c in tiers.most_common())}.",
          f"- **License red today:** {len(reds)} ({', '.join('`'+n+'`' for n in reds) or 'none'}).",
          f"- **No changes in a year:** {len(dormant)} pilot repositories ({', '.join('`'+n+'`' for n in dormant)}). "
          "This includes the heavily used `exec-*` tools: they are still downloaded and cloned, so they need a",
          "  maintenance decision (who looks after them) before any thought of graduating them.",
          "- **Decisions for the maintainers:** approve this pilot (approval 3) and each repository's kind (approval 4),",
          "  and decide the should-be-archived repositories.", ""]
    (out / "pilot-briefing.md").write_text("\n".join(L) + "\n")
    print(f"wrote {out / 'pilot-briefing.md'}")


if __name__ == "__main__":
    main()

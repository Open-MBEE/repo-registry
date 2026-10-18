#!/usr/bin/env python3
"""Render the policy basis review's tables from the model: a view, rendered, never committed (WP5b F-08).

The tables in docs/policy-basis-review.md were written by hand and could drift from the policies. They are now
rendered from data/policies/, data/policies/_departures.yaml and data/sources/: the policy set, the OpenSSF baseline
trace, the CISA trace, the NIST controls cited and the ISO/IEC/IEEE 12207 clauses cited. The narrative stays in the
hand-written document.

Usage: python3 scripts/basis.py [--out build/demo]   (reads build/demo/reports/policy-applicability.yaml)
"""
import argparse
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model  # noqa: E402
import policies as P  # noqa: E402


def cited_by(pols, source):
    out = {}
    for pid, p in sorted(pols.items()):
        refs = p["cites"].get(source)
        for ref in (refs if isinstance(refs, list) else []):
            out.setdefault(str(ref), []).append(pid)
    return out


def render(root, out):
    pols, departures = P.load_policies(root / "data/policies")
    by_policy = yaml.safe_load((out / "reports/policy-applicability.yaml").read_text())["policies"]
    kinds = model.kinds(model.load("data/taxonomy/kinds.yaml", root))
    live = [k for k, v in kinds.items() if v["stage"] != "archived"]
    src = lambda rel: model.load(f"data/sources/{rel}", root)  # noqa: E731
    L = ["# Policy basis tables", "",
         "> **PROVISIONAL.** A view (WP5b F-08), rendered by `scripts/basis.py` from `data/policies/` and",
         "> `data/sources/`; never committed. The narrative is in `docs/policy-basis-review.md`.", "",
         f"## The proposed policy set ({len(pols)} policies)", "",
         "| Policy | Scope | In effect for | GitHub mechanism | Automated / attested checks |", "|---|---|---|---|---|"]
    for pid, p in sorted(pols.items()):
        ks = by_policy.get(pid, [])
        where = "every live kind" if ks == live else ", ".join(ks)
        n_auto, n_att = len(p["checks"].get("automated") or []), len(p["checks"].get("attested") or [])
        L.append(f"| [{pid}](sops/{pid}.md) | {p['scope']} | {where} | {' '.join(p['github']['mechanism'].split())} | "
                 f"{n_auto} / {n_att} |")
    adopted = cited_by(pols, "openssf")
    L += ["", "## Trace: OpenSSF security baseline (backbone, WP2 R-13)", "",
          "| Item | Stage | Baseline item (our title; its words are in the source file) | Adopted by | Or departed because |", "|---|---|---|---|---|"]
    for item, row in src("openssf-security-baseline.yaml")["items"].items():
        why = " ".join(str((departures.get("openssf") or {}).get(item, "")).split())
        L.append(f"| {item} | {row['stage']} ({row['when']}) | {row['title']} | {', '.join(adopted.get(item, []))} | {why} |")
    carried = cited_by(pols, "cisa")
    L += ["", "## Trace: CISA practices (WP2 R-6)", "", "| Practice | p. | Carried by | Or left out because |",
          "|---|---|---|---|"]
    for ref, row in src("cisa-practices.yaml")["practices"].items():
        why = " ".join(str((departures.get("cisa") or {}).get(ref, "")).split())
        L.append(f"| {ref} | {row['page']} | {', '.join(carried.get(ref, []))} | {why} |")
    nist = cited_by(pols, "nist")
    controls = src("nist-800-53.yaml")["controls"]
    L += ["", "## NIST SP 800-53 controls cited", "", "| Control | Title | Cited by |", "|---|---|---|"]
    for ref in sorted(nist, key=lambda r: (r.split("-")[0], r)):
        L.append(f"| {ref} | {controls.get(ref, {}).get('title', '')} | {', '.join(nist[ref])} |")
    iso = cited_by(pols, "iso12207")
    clauses = src("iso12207-clauses.yaml")["clauses"]
    L += ["", "## ISO/IEC/IEEE 12207:2026, by clause", "", "| Clause (title from the table of contents) | Used by |",
          "|---|---|"]
    for ref in sorted(iso, key=lambda r: [int(x) for x in r.split(".")]):
        L.append(f"| {ref} {clauses.get(ref, {}).get('title', '')} | {', '.join(iso[ref])} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="build/demo")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    out = pathlib.Path(args.out)
    (out / "policy-basis-tables.md").write_text(render(pathlib.Path(args.root), out))
    print(f"wrote {out / 'policy-basis-tables.md'}")


if __name__ == "__main__":
    main()

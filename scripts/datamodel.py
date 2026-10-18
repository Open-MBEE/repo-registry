#!/usr/bin/env python3
"""Render the data model document from data/schema/model.yaml: a view, rendered, never committed (WP5b D-1).

One section per table (its role, where its rows live, its key, its foreign keys and columns), and an
entity-relationship diagram drawn from the foreign keys, as a Mermaid block.

Usage: python3 scripts/datamodel.py [--out build/demo]
"""
import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model  # noqa: E402


def targets(spec):
    """The tables a foreign-key spec points to: fk(table) or fk(table.column), possibly inside list(...)."""
    return re.findall(r"fk\(([a-z_]+)(?:\.[a-z_]+)?\)", str(spec))


def render(m):
    tables = m["tables"]
    L = ["# Data model", "",
         "> **PROVISIONAL.** A view (WP5b D-1), rendered by `scripts/datamodel.py` from `data/schema/model.yaml`;",
         "> never committed. The repository's records are the tables of a database (WP5b): `source` tables are",
         "> read-only facts, `model` tables are what people decide, and views are rendered, never stored.", "",
         f"Current snapshot: `{m['snapshot']}`.", "", "```mermaid", "erDiagram"]
    for name, t in tables.items():
        for col, spec in (t.get("foreign") or {}).items():
            for target in targets(spec):
                L.append(f"    {target} ||--o{{ {name} : \"{col}\"")
        for col, spec in (t.get("columns") or {}).items():
            for target in targets(spec):
                L.append(f"    {target} ||--o{{ {name} : \"{col}\"")
    L += ["```", ""]
    for role in ("source", "model"):
        L += [f"## {role.capitalize()} tables", ""]
        for name, t in tables.items():
            if t["role"] != role:
                continue
            key = ", ".join(t.get("key") or []) or "(one row)"
            L += [f"### `{name}`", "", f"- **Rows:** `{t['rows']}`", f"- **Key:** {key}"]
            for u in t.get("unique") or []:
                L.append(f"- **Unique:** {', '.join(u)}")
            for col, spec in (t.get("foreign") or {}).items():
                L.append(f"- **Foreign key:** {col} → {spec}")
            for col, spec in (t.get("columns") or {}).items():
                L.append(f"- `{col}`: {spec}")
            for k in ("disjoint_from", "rule"):
                if t.get(k):
                    L.append(f"- **{k.replace('_', ' ').capitalize()}:** {t[k]}")
            L.append("")
    L += ["## Derived columns", "", "Columns a predicate may read that no table stores; each is derived by a controller.", ""]
    for col, spec in (m.get("derived") or {}).items():
        L.append(f"- `{col}`: {spec}")
    L += ["", "## Views", ""] + [f"- `{v}`: {spec}" for v, spec in m["views"].items()]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="build/demo")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "data-model.md").write_text(render(model.declared(pathlib.Path(args.root))))
    print(f"wrote {out / 'data-model.md'}")


if __name__ == "__main__":
    main()

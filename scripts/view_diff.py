#!/usr/bin/env python3
"""Say, in Markdown, how a change would alter the views: the rendered views of the base against those of the head.

Views are never committed (WP5b OD4), so a pull request's diff no longer shows what its change would do to the
organization (README, the governor's role). CI renders the views for main and for the pull request, in demo mode,
and this script writes the difference into the run's job summary. Deterministic, offline, read-only.

Usage: python3 scripts/view_diff.py BASE_DIR HEAD_DIR [--max-lines 600]   (prints Markdown)
"""
import argparse
import difflib
import pathlib


def files(d):
    d = pathlib.Path(d)
    return {str(p.relative_to(d)): p for p in d.rglob("*") if p.is_file()} if d.exists() else {}


def summary(base, head, max_lines=600):
    a, b = files(base), files(head)
    if not a:
        return "## Views\n\nThe base has no rendered views to compare with, so every view below is new.\n\n" + \
            "\n".join(f"- `{n}`" for n in sorted(b)) + "\n"
    added, removed = sorted(set(b) - set(a)), sorted(set(a) - set(b))
    changed = sorted(n for n in set(a) & set(b) if a[n].read_bytes() != b[n].read_bytes())
    if not (added or removed or changed):
        return "## Views\n\nThis change alters no view (demo mode: what would be written to the wiki and issues).\n"
    lines = ["## Views", "", "How this change alters what would be written (demo mode, WP5b OD5):", ""]
    lines += [f"- added: `{n}`" for n in added] + [f"- removed: `{n}`" for n in removed]
    lines += [f"- changed: `{n}`" for n in changed]
    diff = []
    for n in changed:
        diff += difflib.unified_diff(a[n].read_text().splitlines(), b[n].read_text().splitlines(),
                                     f"main/{n}", f"this change/{n}", lineterm="")
    if diff:
        shown = diff[:max_lines]
        lines += ["", "```diff", *shown, "```"]
        if len(diff) > max_lines:
            lines.append(f"\n({len(diff) - max_lines} more lines: download the rendered views artifact.)")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("base")
    ap.add_argument("head")
    ap.add_argument("--max-lines", type=int, default=600)
    args = ap.parse_args()
    print(summary(args.base, args.head, args.max_lines), end="")


if __name__ == "__main__":
    main()

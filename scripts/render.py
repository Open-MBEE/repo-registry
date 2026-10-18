#!/usr/bin/env python3
"""Render every view from the model, in order (WP5b D-4; MVC: the controller renders, CD publishes).

Views are never committed (WP5b OD4). This one command renders them all, deterministically, from the model alone.
It has a mode toggle (OD5); only demo mode exists so far. Demo mode writes every view into an ephemeral directory,
emptied on each run, and touches nothing outside it: no GitHub call, no wiki, no issue. It shows what would be
written if the writes were turned on, so the behaviour can be reviewed and approved first ("simulating the plant to
test the controller before we turn the thing on"). Live mode, which would publish the wiki and write issues, comes
with WP6 and WP7, gated on CI and an explicit switch.

Usage: python3 scripts/render.py [--mode demo] [--out build/demo] [--root .]
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
STEPS = ["recommend.py", "policies.py", "licenses.py", "org.py", "pilot.py", "briefing.py", "sops.py", "basis.py",
         "datamodel.py", "fit.py"]  # each later step may read the views written by earlier ones


def render(out, root=".", quiet=True):
    out, root = pathlib.Path(out).resolve(), pathlib.Path(root).resolve()  # absolute: each step runs with cwd=root
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for step in STEPS:
        script = root / "scripts" / step  # the controller of the tree being rendered
        run = subprocess.run([sys.executable, str(script if script.exists() else HERE / step), "--out", str(out),
                              "--root", str(root)],
                             cwd=root, capture_output=True, text=True)
        if run.returncode:
            raise SystemExit(f"render: {step} failed:\n{(run.stderr or run.stdout).strip()}")
        if not quiet:
            print(run.stdout.rstrip())
    return sorted(str(p.relative_to(out)) for p in out.rglob("*") if p.is_file())


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mode", choices=["demo"], default="demo")
    ap.add_argument("--out", default="build/demo")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    files = render(args.out, args.root)
    print(f"demo mode: rendered {len(files)} views into {args.out} (nothing was written anywhere else)")


if __name__ == "__main__":
    main()

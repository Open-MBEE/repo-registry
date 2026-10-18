#!/usr/bin/env python3
"""Render every view from the model, in order (WP5b D-4; MVC: the controller renders, CD publishes).

Views are never committed (WP5b OD4). This one command renders them all, deterministically, from the model alone.
It has a mode toggle (OD5); only demo mode exists so far. Demo mode writes every view into an ephemeral directory,
emptied on each run, and touches nothing outside it: no GitHub call, no wiki, no issue. It shows what would be
written if the writes were turned on, so the behaviour can be reviewed and approved first ("simulating the plant to
test the controller before we turn the thing on").

Live mode (WP5d D-3) publishes one view plane: the wiki pages (scripts/wiki.py) to this repository's wiki, and
nothing else. The supervisor runs it, with his own git credentials ("You run it, today"). It refuses unless the tree
is a clean `main`, equal to `origin/main`, and `scripts/validate.py` passes (WP5d R-5). To compare with `origin/main`
it first runs `git fetch origin main`, which updates only this clone's remote-tracking ref; nothing is written to
GitHub until the publish. It then renders every view,
replaces the wiki's pages with the rendered ones, and commits "Publish from <main commit>" and pushes. Writing issues
waits for WP6, and publishing from CI for WP7.

Usage: python3 scripts/render.py [--mode demo|live] [--out build/demo] [--root .]
"""
import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
STEPS = ["recommend.py", "policies.py", "licenses.py", "org.py", "pilot.py", "briefing.py", "sops.py", "basis.py",
         "datamodel.py", "fit.py", "wiki.py"]  # each later step may read the views written by earlier ones


def render(out, root=".", quiet=True):
    out, root = pathlib.Path(out).resolve(), pathlib.Path(root).resolve()  # absolute: each step runs with cwd=root
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for step in STEPS:
        script = root / "scripts" / step  # the controller of the tree being rendered
        if not script.exists() and (root / "scripts").is_dir():
            continue  # that tree's controller has no such view yet (an older base, in CI's view diff)
        run = subprocess.run([sys.executable, str(script if script.exists() else HERE / step), "--out", str(out),
                              "--root", str(root)],
                             cwd=root, capture_output=True, text=True)
        if run.returncode:
            raise SystemExit(f"render: {step} failed:\n{(run.stderr or run.stdout).strip()}")
        if not quiet:
            print(run.stdout.rstrip())
    return sorted(str(p.relative_to(out)) for p in out.rglob("*") if p.is_file())


WIKI = "https://github.com/Open-MBEE/repo-registry.wiki.git"  # the only place live mode writes (WP5d R-5)


def git(root, *args):
    run = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    return run.returncode, run.stdout.strip()


def live_refusals(root, validate=None, fetch=True):
    """Why live mode must not publish from this tree; empty when it may (WP5d R-5)."""
    root, out = pathlib.Path(root).resolve(), []
    if git(root, "branch", "--show-current")[1] != "main":
        out.append("not on main: live mode publishes only from main")
    code, status = git(root, "status", "--porcelain")
    if code or status:
        out.append("the working tree is not clean: commit or remove the changes first")
    if fetch:  # a read: updates this clone's origin/main only, so the comparison below is with GitHub's main
        git(root, "fetch", "--quiet", "origin", "main")
    head, origin = git(root, "rev-parse", "HEAD"), git(root, "rev-parse", "--verify", "--quiet", "origin/main")
    if origin[0] or head[1] != origin[1]:
        out.append("HEAD is not origin/main: pull, or push through a pull request, first")
    cmd = validate or [sys.executable, str(root / "scripts" / "validate.py")]
    run = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    if run.returncode:
        out.append("scripts/validate.py fails: invalid state is never published")
    return out


def publish(pages, sha):
    """Replace the wiki's pages with the rendered ones, commit and push. Writes to WIKI only."""
    with tempfile.TemporaryDirectory() as t:
        wiki = pathlib.Path(t) / "wiki"
        code, _ = git(t, "clone", "--quiet", WIKI, str(wiki))
        if code:
            raise SystemExit(f"live: can't clone {WIKI}; create the wiki's first page in the web app once")
        for old in wiki.glob("*.md"):
            old.unlink()
        for page in sorted(pathlib.Path(pages).glob("*.md")):
            shutil.copy(page, wiki / page.name)
        git(wiki, "add", "-A")
        if not git(wiki, "status", "--porcelain")[1]:
            return "the wiki already shows this commit's pages: nothing to publish"
        code, msg = git(wiki, "commit", "--quiet", "-m", f"Publish from {sha}")
        if code:
            raise SystemExit(f"live: commit failed: {msg}")
        code, msg = git(wiki, "push", "--quiet", "origin", "HEAD")
        if code:
            raise SystemExit(f"live: push failed: {msg}")
        return f"published {len(list(wiki.glob('*.md')))} pages to {WIKI}, from {sha}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mode", choices=["demo", "live"], default="demo")
    ap.add_argument("--out", default="build/demo")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    if args.mode == "live":
        refusals = live_refusals(args.root)
        if refusals:
            raise SystemExit("live mode refused:\n" + "\n".join(f"  - {r}" for r in refusals))
        with tempfile.TemporaryDirectory() as t:
            render(t, args.root)
            print(publish(pathlib.Path(t) / "wiki", git(args.root, "rev-parse", "HEAD")[1]))
        return
    files = render(args.out, args.root)
    print(f"demo mode: rendered {len(files)} views into {args.out} (nothing was written anywhere else)")


if __name__ == "__main__":
    main()

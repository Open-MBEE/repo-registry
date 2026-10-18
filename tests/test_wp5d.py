"""WP5d checks: the maintainer review pack, on the wiki. Run with: python3 -m unittest discover -s tests

Each test names the WP5d requirement it checks (work-packages/WP5d-scope-of-work.md).
"""
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import model  # noqa: E402
import render  # noqa: E402
import wiki  # noqa: E402

LINK = re.compile(r"\]\(([^)\s]+)\)")
PAGES, APPLIES, OUT = {}, {}, tempfile.TemporaryDirectory()


def setUpModule():
    render.render(OUT.name, ROOT)
    out = pathlib.Path(OUT.name)
    PAGES.update({p.stem: p.read_text() for p in (out / "wiki").glob("*.md")})
    APPLIES.update(yaml.safe_load((out / "reports/policy-applicability.yaml").read_text())["policies"])


def tearDownModule():
    OUT.cleanup()


def rows(page):
    return [ln for ln in PAGES[page].splitlines() if ln.startswith("| ") and not ln.startswith("|---")]


def anchors(text):
    return {wiki.anchor(m.group(1)) for m in re.finditer(r"^#+ (.+)$", text, re.M)}


class PageTests(unittest.TestCase):
    def test_R1_every_repository_once_with_kind_tier_source(self):
        """R-1: every kind-list entry appears once, with its kind (or reason), tier and source, linked to GitHub and
        to its kind on the Taxonomy page."""
        reg = model.load("registry.yaml")["repos"]
        kinds = model.kinds(model.load("data/taxonomy/kinds.yaml"))
        text = PAGES["Repositories"]
        for e in reg.values():
            with self.subTest(repo=e["name"]):
                link = f"[{e['name']}](https://github.com/Open-MBEE/{e['name']})"
                found = [ln for ln in rows("Repositories") if ln.startswith(f"| {link} |")]
                self.assertEqual(len(found), 1)
                cells = [c.strip() for c in found[0].strip("|").split(" | ")]
                if "reason" in e:
                    self.assertEqual(cells[2], e["source"])
                else:
                    k = model.kind_of(e)
                    self.assertEqual(cells[1:3], [k, kinds[k]["tier"]])
                    self.assertEqual(cells[3].split(":")[0], e["source"])
                    if e.get("decision"):  # a maintainer's entry shows its decision: the why
                        self.assertIn(wiki.cell(e["decision"]), cells[3])
        for k in kinds:
            self.assertIn(f"[{k}](Taxonomy#{wiki.anchor(k)})", text)

    def test_R2_every_policy_with_its_kinds_tiers_and_sop(self):
        """R-2: every policy has one summary row (what it asks, its rule in words, its tiers) and one section, with the
        kinds the applicability view gives, their tiers, its rule in words, and a link to its SOP page."""
        kinds = model.kinds(model.load("data/taxonomy/kinds.yaml"))
        pols = {pid: yaml.safe_load((ROOT / f"data/policies/{pid}.yaml").read_text()) for pid in APPLIES}
        text = PAGES["Policies"]
        for pid, p in pols.items():
            with self.subTest(policy=pid):
                name, tiers = p["name"], {kinds[k]["tier"] for k in APPLIES[pid]}
                found = [ln for ln in rows("Policies") if ln.startswith(f"| [{wiki.cell(name)}](#{wiki.anchor(name)}) |")]
                self.assertEqual(len(found), 1)
                cells = [c.strip() for c in found[0].strip("|").split(" | ")]
                self.assertEqual(cells[1], wiki.cell(p["meaning"]))
                self.assertEqual(cells[2], wiki.cell(wiki.rule_words(p["applies_if"])))
                self.assertEqual(set(cells[3].split(", ")) - {"—"}, tiers)
                section = text.split(f"\n## {name}\n")[1].split("\n## ")[0]
                kinds_line = next(ln for ln in section.splitlines() if ln.startswith("- **Kinds:**"))
                self.assertEqual(re.findall(r"\[([^\]]+)\]\(Taxonomy", kinds_line), APPLIES[pid])
                self.assertIn(f"](SOP-{pid})", section)
                self.assertIn(f"/edit/main/data/policies/{pid}.yaml", section)
                self.assertIn(f"SOP-{pid}", PAGES)

    def test_R3_taxonomy_defines_everything_and_gives_the_heuristics(self):
        """R-3: every type, stage, tier, kind and signal appears, and each kind says how a repository gets it."""
        kd = model.load("data/taxonomy/kinds.yaml")
        text = PAGES["Taxonomy"]
        for name in list(kd["types"]) + list(kd["stages"]) + list(model.load("data/taxonomy/tiers.yaml")["tiers"]):
            self.assertTrue(re.search(rf"^\| {re.escape(name)} \|", text, re.M), name)
        for k in model.kinds(kd):
            self.assertIn(f"### {k}\n", text)
            section = text.split(f"### {k}\n")[1].split("\n### ")[0]
            self.assertIn("**How a repository gets it:**", section)
        for s in kd["signals"]:
            self.assertIn(f"| `{s}` | {wiki.cell(kd['explain'][s])} |", text)

    def test_R4_links_resolve_and_pages_name_their_commit(self):
        """R-4: every link between pages resolves to a page and an anchor on it; every page names the commit it was
        rendered from (in the sidebar, shown on every page) and says PROVISIONAL; every table row of the model links to
        its file, with the edit link."""
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        for name, text in PAGES.items():
            with self.subTest(page=name):
                self.assertIn("PROVISIONAL", text)
                if name == "_Sidebar":  # shown on every page: the one place the commit is named (observation 3)
                    self.assertIn(f"/tree/{sha})", text)
                else:
                    self.assertIn("from the commit named in the sidebar", text)
                    self.assertNotIn(sha, text)
                for target in LINK.findall(text):
                    if "://" in target:
                        continue
                    page, _, frag = target.partition("#")
                    page = page or name
                    self.assertIn(page, PAGES, target)
                    if frag:
                        self.assertIn(frag, anchors(PAGES[page]), target)
        heads = ("| Type |", "| Stage |", "| Tier |", "| Kind |", "| Topic |", "| Reason |", "| Repository |",
                 "| Policy |", "| Signal |", "| Type and stage |")
        for name in ("Taxonomy", "Repositories", "Policies"):
            for ln in rows(name):
                first = ln.split(" | ")[0]
                if ln.startswith(heads) or re.search(r"\]\((\w+)?#", first):
                    continue  # a header, or an index row: its first cell links to the section holding the record
                with self.subTest(page=name, row=ln[:60]):
                    self.assertIn("/edit/main/", ln)

    def test_R7_citations_link_both_ways(self):
        """R-7: every policy citation links to its item on the source's page; every item of each source appears there
        with the policies that adopt it, its departure reason, or (NIST) the context of a control no policy cites;
        OpenSSF and CISA leave none out (meta-rules 8, 9)."""
        pack = wiki.Pack(ROOT, pathlib.Path(OUT.name))
        for sid, items in pack.items.items():
            page = PAGES[f"Source-{sid}"]
            adopted = pack.cited_by(sid)
            for ref in items:
                with self.subTest(source=sid, item=ref):
                    section = page.split(f"### {ref}\n")[1].split("\n### ")[0]
                    if ref in adopted:
                        for pid in adopted[ref]:
                            self.assertIn(f"](SOP-{pid})", section)
                            self.assertIn(f"[{ref}](Source-{sid}#{wiki.anchor(ref)})", PAGES["Policies"])
                    elif sid in ("openssf", "cisa"):
                        self.assertIn("**Departed from:**", section)
                    else:
                        self.assertIn(f"**Cited by no policy:** {wiki.cell(items[ref]['context'])}", section)

    def test_pages_render_the_same_twice(self):
        """D-4: the pages are deterministic."""
        with tempfile.TemporaryDirectory() as t:
            render.render(t, ROOT)
            again = {p.stem: p.read_text() for p in (pathlib.Path(t) / "wiki").glob("*.md")}
        self.assertEqual(again, PAGES)


class LiveModeTests(unittest.TestCase):
    def repo(self, t, branch="main"):
        """A git repository with an origin, on `branch`, equal to origin/main."""
        origin, work = pathlib.Path(t) / "origin.git", pathlib.Path(t) / "work"
        subprocess.run(["git", "init", "--quiet", "--bare", str(origin)], check=True)
        subprocess.run(["git", "init", "--quiet", "-b", "main", str(work)], check=True)
        g = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=work,  # noqa: E731
                                      check=True, capture_output=True)
        (work / "f").write_text("x")
        g("add", "f")
        g("commit", "--quiet", "-m", "c")
        g("remote", "add", "origin", str(origin))
        g("push", "--quiet", "origin", "main")
        g("fetch", "--quiet", "origin")
        if branch != "main":
            g("switch", "--quiet", "-c", branch)
        return work

    PASS, FAIL = [sys.executable, "-c", "pass"], [sys.executable, "-c", "raise SystemExit(1)"]

    def test_R5_refuses_off_main_dirty_ahead_or_invalid(self):
        """R-5: live mode refuses a tree that is not main, not clean, not origin/main, or not valid; it allows only
        a clean, valid main equal to origin/main."""
        with tempfile.TemporaryDirectory() as t:
            work = self.repo(t)
            self.assertEqual(render.live_refusals(work, self.PASS), [])
            self.assertEqual(len(render.live_refusals(work, self.FAIL)), 1)
            (work / "g").write_text("dirty")
            self.assertTrue(any("not clean" in r for r in render.live_refusals(work, self.PASS)))
            (work / "g").unlink()
            subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "--quiet", "--allow-empty",
                            "-m", "ahead"], cwd=work, check=True)
            self.assertTrue(any("origin/main" in r for r in render.live_refusals(work, self.PASS)))
        with tempfile.TemporaryDirectory() as t:
            work = self.repo(t, branch="wp-x")
            self.assertTrue(any("not on main" in r for r in render.live_refusals(work, self.PASS)))

    def test_R5_writes_only_to_this_repositorys_wiki(self):
        """R-5: the only clone and push target is this repository's wiki; demo mode writes no git at all."""
        src = (ROOT / "scripts/render.py").read_text()
        self.assertEqual(render.WIKI, "https://github.com/Open-MBEE/repo-registry.wiki.git")
        self.assertEqual(re.findall(r'"push"[^)]*', src), ['"push", "--quiet", "origin", "HEAD"'])
        self.assertEqual(re.findall(r'"clone", [^\n]*', src), ['"clone", "--quiet", WIKI, str(wiki))'])
        self.assertNotIn("push", (ROOT / "scripts/wiki.py").read_text())


if __name__ == "__main__":
    unittest.main()

"""WP1 checks: kinds and tiers. Run with: python3 -m unittest discover -s tests

Each test names the WP1 requirement it checks (work-packages/WP1-scope-of-work.md).
"""
import difflib
import json
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
import recommend  # noqa: E402

SNAPSHOT = ROOT / "data/snapshots/2026-10-18"
KINDS = ROOT / "data/taxonomy/kinds.yaml"
TIERS = ROOT / "data/taxonomy/tiers.yaml"
REGISTRY = ROOT / "registry.yaml"
FIXTURES = ROOT / "tests/fixtures"


def load(path):
    return yaml.safe_load(pathlib.Path(path).read_text())


def run_recommend(tmp, kinds=KINDS, tiers=TIERS, registry=REGISTRY):
    """The rules' draft kind list and the recommendation report: views, rendered into tmp (WP5b OD4)."""
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/recommend.py"), "--out", str(tmp), "--kinds", str(kinds),
         "--tiers", str(tiers), "--registry", str(registry or "")],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    return (pathlib.Path(tmp) / "kind-list-draft.yaml").read_text(), load(pathlib.Path(tmp) / "reports/kind-recommendations.yaml")


def by_name(report):
    return {r["name"]: r for r in report["repos"].values()}


class SnapshotTests(unittest.TestCase):
    def test_R1_read_only_gh(self):
        """R-1: the snapshot script only reads, through gh."""
        src = (ROOT / "scripts/snapshot.py").read_text()
        self.assertNotIn("mutation", src)
        self.assertEqual(set(re.findall(r'"gh", "api", "(\w+)"', src)), {"graphql"})

    def test_R1_private_repos_count_only(self):
        """R-1, OD2: private repos are counted, never listed."""
        meta = json.loads((SNAPSHOT / "meta.json").read_text())
        repos = json.loads((SNAPSHOT / "repos.json").read_text())
        self.assertEqual(meta["public_repos"], len(repos))
        self.assertEqual(meta["all_repos_count"], meta["public_repos"] + meta["private_repos_count_only"])


class TaxonomyTests(unittest.TestCase):
    def setUp(self):
        self.kinds, self.tiers = load(KINDS), load(TIERS)

    def test_R3_type_x_stage_with_stated_departures(self):
        """R-3: kinds start from type x stage; every added or omitted kind states a reason."""
        cross = {f"{t}/{s}" for t in self.kinds["types"] for s in self.kinds["stages"]}
        defined, omitted = set(model.kinds(self.kinds)), model.omitted(self.kinds)
        self.assertEqual(defined - cross, set(), "a kind outside the cross product")
        self.assertEqual(cross - defined, set(omitted), "a cross-product kind is neither defined nor omitted")
        for name, reason in omitted.items():
            self.assertTrue(reason.strip(), name)
        self.assertEqual(set(self.kinds["stages"]), {"sandbox", "incubating", "graduated", "archived"})

    def test_R6_one_tier_per_kind_and_fixed_map(self):
        """R-6: each kind has one tier; the fixed parts of the map hold; every tier is used."""
        recommend.check_taxonomy(self.kinds, self.tiers)
        k = model.kinds(self.kinds)
        self.assertEqual(k["tool/graduated"]["tier"], "high")
        self.assertEqual(k["tool/incubating"]["tier"], "medium")
        self.assertEqual(k["tool/sandbox"]["tier"], "low")
        for name, kind in k.items():
            if kind["stage"] == "graduated":
                self.assertIs(kind["recommend_when"], False, f"{name}: graduated is assigned only")
        for name, kind in k.items():
            if kind["type"] == "governance":  # friction rises with the stage (WP4c OD2; WP1 amendment 3)
                expected = {"sandbox": "low", "incubating": "medium", "graduated": "high"}[kind["stage"]]
                self.assertEqual(kind["tier"], expected, name)
                self.assertIs(kind["recommend_when"], False, name)
            elif kind["stage"] == "archived":
                self.assertEqual(kind["tier"], "none", name)
            elif name != "tool/graduated":
                self.assertIn(kind["tier"], ("low", "medium"), name)

    def test_R6_governance_assignments(self):
        """R-6 (A2, A4): repo-registry is governance/sandbox and the org is governance/graduated."""
        doc = yaml.safe_load(REGISTRY.read_text())
        entry = next(e for e in doc["repos"].values() if e["name"] == "repo-registry")
        self.assertEqual(model.kind_of(entry), "governance/sandbox")
        self.assertEqual(model.kind_of(doc["org"]), "governance/graduated")

    def test_R4_every_kind_has_a_meaning(self):
        """R-4 (part): every kind and tier has a plain meaning. The cold read itself is a manual check."""
        for name, kind in model.kinds(self.kinds).items():
            self.assertTrue(kind["meaning"].strip(), name)
        for name, tier in self.tiers["tiers"].items():
            self.assertTrue(tier["meaning"].strip(), name)


class EngineTests(unittest.TestCase):
    def test_R2_replay(self):
        """R-2: the rules applied to the stored snapshot give the same result every time, and cover registry.yaml.

        Since WP5 the kind list is edited by people, one entry at a time (WP0 R-12), so it no longer has to equal
        what the rules draft; it has to cover the same repositories.
        """
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            reg_a, rep_a = run_recommend(a)
            reg_b, rep_b = run_recommend(b)
        self.assertEqual(reg_a, reg_b)
        self.assertEqual(rep_a, rep_b)
        self.assertEqual(set(yaml.safe_load(reg_a)["repos"]), set(yaml.safe_load(REGISTRY.read_text())["repos"]))

    def test_R5_rules_are_exclusive_on_the_snapshot(self):
        """R-5: no repo matches two kinds; unclassified repos carry a reason."""
        with tempfile.TemporaryDirectory() as t:
            _, report = run_recommend(t)
        for name, r in by_name(report).items():
            self.assertLessEqual(len(r["matched"]), 1, name)
            if r["kind"] == "unclassified":
                self.assertTrue(r["reason"], name)

    def test_R5_overlap_is_reported_not_hidden(self):
        """R-5: if two kinds' rules overlap, the repo is unclassified and the overlap is named."""
        with tempfile.TemporaryDirectory() as t:
            _, report = run_recommend(t, kinds=FIXTURES / "overlap-kinds.yaml", tiers=FIXTURES / "toy-tiers.yaml",
                                      registry=None)
        first = next(iter(report["repos"].values()))
        self.assertEqual(first["kind"], "unclassified")
        self.assertIn("more than one kind", first["reason"])

    def test_R7_toy_taxonomy_swap_needs_no_code_change(self):
        """R-7: a different taxonomy runs through the same engine, and the engine names no kind, type or tier."""
        with tempfile.TemporaryDirectory() as t:
            _, report = run_recommend(t, kinds=FIXTURES / "toy-kinds.yaml", tiers=FIXTURES / "toy-tiers.yaml",
                                      registry=None)
        self.assertEqual({r["kind"] for r in report["repos"].values()}, {"thing/busy", "thing/quiet"})
        src = (ROOT / "scripts/recommend.py").read_text()
        kinds = load(KINDS)
        names = set(model.kinds(kinds)) | set(kinds["types"]) | set(load(TIERS)["tiers"])
        quoted = set(re.findall(r'"([^"]+)"', src)) | set(re.findall(r"'([^']+)'", src))
        self.assertEqual(names & quoted, set())

    def test_R9_release_maturity_rule(self):
        """R-9 (A4): below 1.0.0 or no release is Sandbox; 1.0.0 or later is Incubating; Graduated never by rule."""
        with tempfile.TemporaryDirectory() as t:
            report = by_name(run_recommend(t)[1])
        expected = {
            "OpenSysML": "tool/sandbox",                # v0.10.1
            "sysml-toolkit": "tool/sandbox",            # v0.10.10
            "mtip-cameo": "tool/incubating",            # v1.0.9
            "exec-mms": "tool/incubating",              # 4.0.20
            "flexo-cli-client": "tool/sandbox",         # no semver release
            "EMS-Repo": "tool/archived",                # archived tool
        }
        for name, kind in expected.items():
            self.assertEqual(report[name]["kind"], kind, name)

    def test_R9_semver_parsing(self):
        """R-9: only non-prerelease MAJOR.MINOR.PATCH tags count; the highest wins."""
        repo = {"releases": [
            {"tag": "v2.0.0-rc1", "prerelease": True},
            {"tag": "release-7", "prerelease": False},
            {"tag": "0.9.3", "prerelease": False},
            {"tag": "v1.4.0", "prerelease": False},
        ]}
        d = recommend.derive(repo)
        self.assertEqual((d["has_semver_release"], d["latest_semver"], d["latest_semver_major"]), (True, "v1.4.0", 1))

        self.assertFalse(recommend.derive({"releases": [{"tag": "nightly", "prerelease": False}]})["has_semver_release"])


class KindListTests(unittest.TestCase):
    def setUp(self):
        self.text = REGISTRY.read_text()
        self.doc = yaml.safe_load(self.text)

    def test_R10_provisional_mark(self):
        """R-10: the provisional kind list (and the taxonomy) can't be mistaken for approved data."""
        self.assertTrue(self.text.startswith("# PROVISIONAL"))
        self.assertEqual(self.doc["status"], "provisional")
        self.assertTrue(self.doc["provisional_until"].strip())
        for path in (KINDS, TIERS):
            self.assertEqual(load(path)["status"], "provisional", path)

    def test_D4_meta_rules(self):
        """D-4 meta-rules 1-8 and 10 hold on the provisional kind list (entries hold type and stage, WP4e)."""
        kinds = model.kinds(load(KINDS))
        self.assertLessEqual(set(self.doc), {"status", "org", "repos", "provisional_until"})
        self.assertEqual(set(self.doc["org"]), {"name", "type", "stage", "source", "decision"})
        self.assertIn(model.kind_of(self.doc["org"]), kinds)
        names = [e["name"] for e in self.doc["repos"].values()]
        self.assertEqual(len({n.lower() for n in names}), len(names))
        self.assertEqual(names, sorted(names, key=str.lower))
        for rid, entry in self.doc["repos"].items():
            self.assertIsInstance(rid, int)  # keyed by GitHub's repository ID (WP5b OD3)
            self.assertIn(set(entry) - {"source", "decision"}, ({"name", "type", "stage"}, {"name", "reason"}),
                          entry["name"])  # source and decision: WP5c OD1
            kind = model.kind_of(entry)
            self.assertTrue(kind in kinds or kind == "unclassified", entry["name"])
        recommend.check_taxonomy(load(KINDS), load(TIERS))

    def test_D5_covers_every_snapshot_repo(self):
        """D-5: every repository has an entry, by ID: the snapshot's, and any read after it (WP5b F-04)."""
        self.assertEqual(set(self.doc["repos"]), set(model.repos(ROOT)))

    def test_R8_reclassification_is_one_entry(self):
        """R-8: changing a repo's kind is a one-line edit (its stage, WP4e)."""
        after = self.text.replace('    name: "OpenSysML"\n    type: tool\n    stage: sandbox\n',
                                  '    name: "OpenSysML"\n    type: tool\n    stage: incubating\n')
        self.assertNotEqual(after, self.text)
        changed = [l for l in difflib.unified_diff(self.text.splitlines(), after.splitlines(), lineterm="", n=0)
                   if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        self.assertEqual(changed, ["-    stage: sandbox", "+    stage: incubating"])


if __name__ == "__main__":
    unittest.main()

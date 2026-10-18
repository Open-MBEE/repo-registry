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
import recommend  # noqa: E402

SNAPSHOT = ROOT / "data/snapshots/2026-10-18"
KINDS = ROOT / "data/taxonomy/kinds.yaml"
TIERS = ROOT / "data/taxonomy/tiers.yaml"
REGISTRY = ROOT / "registry.yaml"
FIXTURES = ROOT / "tests/fixtures"
ASSIGNMENTS = ROOT / "data/assignments.yaml"


def load(path):
    return yaml.safe_load(pathlib.Path(path).read_text())


def run_recommend(tmp, kinds=KINDS, tiers=TIERS, assignments=ASSIGNMENTS):
    reg, rep = pathlib.Path(tmp) / "registry.yaml", pathlib.Path(tmp) / "report.yaml"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/recommend.py"), "--snapshot", str(SNAPSHOT.relative_to(ROOT)),
         "--kinds", str(kinds), "--tiers", str(tiers), "--assignments", str(assignments or ""),
         "--registry", str(reg), "--report", str(rep)],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    return reg.read_text(), load(rep)


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

    def test_R3_type_x_lifecycle_with_stated_departures(self):
        """R-3: kinds start from type x lifecycle; every added or omitted kind states a reason."""
        cross = {f"{t}/{l}" for t in self.kinds["types"] for l in self.kinds["lifecycles"]}
        defined, omitted = set(self.kinds["kinds"]), self.kinds.get("omitted", {})
        self.assertEqual(defined - cross, set(), "a kind outside the cross product")
        self.assertEqual(cross - defined, set(omitted), "a cross-product kind is neither defined nor omitted")
        for name, reason in omitted.items():
            self.assertTrue(reason.strip(), name)
        self.assertTrue(self.kinds["kinds"]["tool/unreleased"].get("departure"))

    def test_R6_one_tier_per_kind_and_fixed_map(self):
        """R-6: each kind has one tier; the fixed parts of the map hold; every tier is used."""
        recommend.check_taxonomy(self.kinds, self.tiers)
        k = self.kinds["kinds"]
        self.assertEqual(k["tool/active-development"]["tier"], "high")
        self.assertEqual(k["tool/maintained"]["tier"], "high")
        for name, kind in k.items():
            if kind["type"] == "governance":
                self.assertEqual(kind["tier"], "high", name)
                self.assertIs(kind["recommend_when"], False, name)
            elif kind["lifecycle"] == "archived":
                self.assertEqual(kind["tier"], "none", name)
            elif not name.startswith("tool/") or kind["lifecycle"] not in ("active-development", "maintained"):
                self.assertIn(kind["tier"], ("low", "medium"), name)

    def test_R6_governance_assignments(self):
        """R-6 (A2): repo-registry is governance/experimental and the org is governance/maintained."""
        doc = yaml.safe_load(REGISTRY.read_text())
        self.assertEqual(doc["repos"]["repo-registry"]["kind"], "governance/experimental")
        self.assertEqual(doc["org"]["kind"], "governance/maintained")

    def test_R4_every_kind_has_a_meaning(self):
        """R-4 (part): every kind and tier has a plain meaning. The cold read itself is a manual check."""
        for name, kind in self.kinds["kinds"].items():
            self.assertTrue(kind["meaning"].strip(), name)
        for name, tier in self.tiers["tiers"].items():
            self.assertTrue(tier["meaning"].strip(), name)


class EngineTests(unittest.TestCase):
    def test_R2_replay(self):
        """R-2: the rules applied to the stored snapshot give the same result every time, and match registry.yaml."""
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            reg_a, rep_a = run_recommend(a)
            reg_b, rep_b = run_recommend(b)
        self.assertEqual(reg_a, reg_b)
        self.assertEqual(rep_a, rep_b)
        self.assertEqual(reg_a, REGISTRY.read_text())

    def test_R5_rules_are_exclusive_on_the_snapshot(self):
        """R-5: no repo matches two kinds; unclassified repos carry a reason."""
        with tempfile.TemporaryDirectory() as t:
            _, report = run_recommend(t)
        for name, r in report["repos"].items():
            self.assertLessEqual(len(r["matched"]), 1, name)
            if r["kind"] == "unclassified":
                self.assertTrue(r["reason"], name)

    def test_R5_overlap_is_reported_not_hidden(self):
        """R-5: if two kinds' rules overlap, the repo is unclassified and the overlap is named."""
        with tempfile.TemporaryDirectory() as t:
            _, report = run_recommend(t, kinds=FIXTURES / "overlap-kinds.yaml", tiers=FIXTURES / "toy-tiers.yaml",
                                      assignments=None)
        first = next(iter(report["repos"].values()))
        self.assertEqual(first["kind"], "unclassified")
        self.assertIn("more than one kind", first["reason"])

    def test_R7_toy_taxonomy_swap_needs_no_code_change(self):
        """R-7: a different taxonomy runs through the same engine, and the engine names no kind, type or tier."""
        with tempfile.TemporaryDirectory() as t:
            _, report = run_recommend(t, kinds=FIXTURES / "toy-kinds.yaml", tiers=FIXTURES / "toy-tiers.yaml",
                                      assignments=None)
        self.assertEqual({r["kind"] for r in report["repos"].values()}, {"thing/busy", "thing/quiet"})
        src = (ROOT / "scripts/recommend.py").read_text()
        kinds = load(KINDS)
        names = set(kinds["kinds"]) | set(kinds["types"]) | set(load(TIERS)["tiers"])
        quoted = set(re.findall(r'"([^"]+)"', src)) | set(re.findall(r"'([^']+)'", src))
        self.assertEqual(names & quoted, set())

    def test_R9_release_maturity_rule(self):
        """R-9: the 1.0.0 seam for semver tools; tools without semver can be low or archived."""
        report = load(ROOT / "data/reports/kind-recommendations.yaml")["repos"]
        expected = {
            "OpenSysML": "tool/experimental",           # v0.10.1, active
            "mtip-cameo": "tool/active-development",    # v1.0.9, commits in the last 12 months
            "exec-mms": "tool/maintained",              # 4.0.20, stable; whether upkeep happens is a policy check
            "flexo-cli-client": "tool/unreleased",      # no semver release, low tier
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
        for path in (KINDS, TIERS, ASSIGNMENTS):
            self.assertEqual(load(path)["status"], "provisional", path)

    def test_D4_meta_rules(self):
        """D-4 meta-rules 1-8 and 10 hold on the provisional kind list (WP5 will enforce them in CI)."""
        kinds = load(KINDS)["kinds"]
        self.assertLessEqual(set(self.doc), {"status", "org", "repos", "snapshot", "provisional_until"})
        self.assertEqual(set(self.doc["org"]), {"name", "kind"})
        self.assertIn(self.doc["org"]["kind"], kinds)
        names = list(self.doc["repos"])
        self.assertEqual(len({n.lower() for n in names}), len(names))
        self.assertEqual(names, sorted(names, key=str.lower))
        for name, entry in self.doc["repos"].items():
            self.assertLessEqual(set(entry), {"kind", "reason"}, name)
            self.assertTrue(entry["kind"] in kinds or entry["kind"] == "unclassified", name)
            self.assertEqual("reason" in entry, entry["kind"] == "unclassified", name)
        recommend.check_taxonomy(load(KINDS), load(TIERS))

    def test_D5_covers_every_snapshot_repo(self):
        """D-5: every snapshot repo has an entry, plus the assigned repos not yet in the org."""
        repos = json.loads((SNAPSHOT / "repos.json").read_text())
        assigned = set(load(ASSIGNMENTS)["repos"])
        self.assertEqual(set(self.doc["repos"]), {r["name"] for r in repos} | assigned)

    def test_R8_reclassification_is_one_entry(self):
        """R-8: changing a repo's kind is a one-line edit."""
        after = self.text.replace('  "OpenSysML":\n    kind: tool/experimental\n',
                                  '  "OpenSysML":\n    kind: tool/active-development\n')
        changed = [l for l in difflib.unified_diff(self.text.splitlines(), after.splitlines(), lineterm="", n=0)
                   if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        self.assertEqual(changed, ["-    kind: tool/experimental", "+    kind: tool/active-development"])


if __name__ == "__main__":
    unittest.main()

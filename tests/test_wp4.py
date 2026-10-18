"""WP4 checks: fit analysis and pilot. Run with: python3 -m unittest discover -s tests

Each test names the WP4 requirement it checks (work-packages/WP4-scope-of-work.md).
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


def load(path):
    return yaml.safe_load((ROOT / path).read_text())


PILOT = load("data/pilot.yaml")
EXCLUDE = load("data/exclude.yaml")
RULE = load("data/pilot-rule.yaml")


class PilotTests(unittest.TestCase):
    def test_R1_usage_snapshot_only_reads(self):
        """R-1: the usage snapshot only makes GET requests through gh."""
        src = (ROOT / "scripts/usage_snapshot.py").read_text()
        self.assertEqual(re.findall(r'"-X", "(\w+)"', src), ["GET"])

    def test_R2_selection_and_briefing_replay(self):
        """R-2: the same snapshot and rule give the same proposal and briefing, twice; and today the rule's proposal
        is the kept pilot list (a model table since WP5b OD6; a later difference would be shown, not an error)."""
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            render.render(a, ROOT)
            render.render(b, ROOT)
            for view in ("pilot-proposal.yaml", "pilot-briefing.md"):
                self.assertEqual((pathlib.Path(a) / view).read_text(), (pathlib.Path(b) / view).read_text(), view)
            proposal = yaml.safe_load((pathlib.Path(a) / "pilot-proposal.yaml").read_text())
        self.assertEqual(proposal["pilot"], PILOT["repos"])
        self.assertEqual(set(proposal["excluded"]), set(EXCLUDE["repos"]))

    def test_R3_size_and_every_category(self):
        """R-3: 24 to 36 repositories, every category represented, and the must-includes present."""
        repos = PILOT["repos"]
        self.assertGreaterEqual(len(repos), 24)
        self.assertLessEqual(len(repos), 36)
        cats = {r["category"] for r in repos.values()}
        for cat in RULE["categories"]:
            self.assertIn(cat["id"], cats)
        named = {r["repo_id"] for r in RULE["must_include"] + RULE.get("self_registered", [])}
        self.assertLessEqual(named, set(repos))

    def test_R4_every_public_repo_in_pilot_or_excluded(self):
        """R-4: pilot and exclude list partition the registry; every exclusion has a reason; no private repo."""
        registry = set(load("registry.yaml")["repos"])
        pilot, excluded = set(PILOT["repos"]), set(EXCLUDE["repos"])
        self.assertEqual(pilot | excluded, registry)
        self.assertEqual(pilot & excluded, set())
        self.assertTrue(EXCLUDE["default_reason"].strip())
        for rid, row in EXCLUDE["repos"].items():
            self.assertTrue(str(row.get("reason", EXCLUDE["default_reason"])).strip(), row["name"])
        self.assertLessEqual(pilot | excluded, set(model.repos(ROOT)))  # public repositories only, by ID

    def test_R5_every_pilot_repo_has_a_kind(self):
        """R-5: every pilot repository has a kind, except forks chosen on purpose to show the gap."""
        registry = load("registry.yaml")["repos"]
        kinds = model.kinds(load("data/taxonomy/kinds.yaml"))
        for rid, r in PILOT["repos"].items():
            kind = model.kind_of(registry[rid])  # derived, not stored (WP5b F-09)
            if kind == "unclassified":
                self.assertEqual(r["category"], "forks", r["name"])
            else:
                self.assertIn(kind, kinds, r["name"])

    def test_R6_provisional(self):
        """R-6: the rule, the pilot, the exclude list and the briefing are PROVISIONAL."""
        for doc in (RULE, PILOT, EXCLUDE):
            self.assertEqual(doc["status"], "provisional")
        with tempfile.TemporaryDirectory() as t:
            render.render(t, ROOT)
            self.assertIn("PROVISIONAL", (pathlib.Path(t) / "pilot-briefing.md").read_text())
        self.assertIn("PROVISIONAL", (ROOT / "docs/fit-analysis.md").read_text())


if __name__ == "__main__":
    unittest.main()

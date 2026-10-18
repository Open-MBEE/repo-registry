"""WP4 checks: fit analysis and pilot. Run with: python3 -m unittest discover -s tests

Each test names the WP4 requirement it checks (work-packages/WP4-scope-of-work.md).
"""
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SNAP = "data/snapshots/2026-10-18"


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
        """R-2: the same snapshot and rule give the same pilot, exclude list and briefing."""
        with tempfile.TemporaryDirectory() as t:
            p, e, b = (pathlib.Path(t) / x for x in ("p.yaml", "e.yaml", "b.md"))
            subprocess.run([sys.executable, "scripts/pilot.py", "--snapshot", SNAP, "--pilot", str(p),
                            "--exclude", str(e)], cwd=ROOT, check=True, capture_output=True)
            self.assertEqual(p.read_text(), (ROOT / "data/pilot.yaml").read_text())
            self.assertEqual(e.read_text(), (ROOT / "data/exclude.yaml").read_text())
            subprocess.run([sys.executable, "scripts/briefing.py", "--snapshot", SNAP, "--out", str(b)], cwd=ROOT,
                           check=True, capture_output=True)
            self.assertEqual(b.read_text(), (ROOT / "docs/pilot-briefing.md").read_text())

    def test_R3_size_and_every_category(self):
        """R-3: 24 to 36 repositories, every category represented, and the must-includes present."""
        repos = PILOT["repos"]
        self.assertGreaterEqual(len(repos), 24)
        self.assertLessEqual(len(repos), 36)
        cats = {r["category"] for r in repos.values()}
        for cat in RULE["categories"]:
            self.assertIn(cat["id"], cats)
        self.assertLessEqual(set(RULE["must_include"]) | set(RULE.get("self_registered", [])), set(repos))

    def test_R4_every_public_repo_in_pilot_or_excluded(self):
        """R-4: pilot and exclude list partition the registry; every exclusion has a reason; no private repo."""
        registry = set(load("registry.yaml")["repos"])
        pilot, excluded = set(PILOT["repos"]), set(EXCLUDE["repos"])
        self.assertEqual(pilot | excluded, registry)
        self.assertEqual(pilot & excluded, set())
        for name, reason in EXCLUDE["repos"].items():
            self.assertTrue(reason.strip(), name)
        public = {r["name"] for r in json.loads((ROOT / SNAP / "repos.json").read_text())}
        self.assertLessEqual(pilot | excluded, public | {"repo-registry"})

    def test_R5_every_pilot_repo_has_a_kind(self):
        """R-5: every pilot repository has a kind, except forks chosen on purpose to show the gap."""
        for name, r in PILOT["repos"].items():
            if r["kind"] == "unclassified":
                self.assertEqual(r["category"], "forks", name)
            else:
                self.assertIn(r["kind"], load("data/taxonomy/kinds.yaml")["kinds"], name)

    def test_R6_provisional(self):
        """R-6: the rule, the pilot, the exclude list and the briefing are PROVISIONAL."""
        for doc in (RULE, PILOT, EXCLUDE):
            self.assertEqual(doc["status"], "provisional")
        self.assertIn("PROVISIONAL", (ROOT / "docs/pilot-briefing.md").read_text())
        self.assertIn("PROVISIONAL", (ROOT / "docs/fit-analysis.md").read_text())


if __name__ == "__main__":
    unittest.main()

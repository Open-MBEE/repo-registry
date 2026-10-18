"""Expected failures for work that later packages close (data/expected-gaps.yaml).

Run with: python3 -m unittest discover -s tests. These show as "expected failure". When one starts passing, unittest
reports an "unexpected success": remove the gap from data/expected-gaps.yaml and the decorator here.
"""
import importlib
import pathlib
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


class ForthcomingTests(unittest.TestCase):
    def test_every_gap_has_a_test_and_a_closing_point(self):
        gaps = yaml.safe_load((ROOT / "data/expected-gaps.yaml").read_text())["gaps"]
        tested = {name.split("_")[1] for name in dir(self) if name.startswith("test_XF")}
        self.assertEqual({g.replace("-", "") for g in gaps}, tested)
        for gid, g in gaps.items():
            self.assertTrue(g["closes_in"].strip(), gid)

    @unittest.expectedFailure
    def test_XF1_sensing_credential_has_administration_read(self):
        """XF-1, closes in WP6: the sensing credential is declared with Administration: read."""
        config = yaml.safe_load((ROOT / "config/sensing.yaml").read_text())
        self.assertIn("Administration: read", config["credential"]["permissions"])

    @unittest.expectedFailure
    def test_XF2_repo_registry_passes_change_review(self):
        """XF-2, closes at R3: the engine reports change-review green for repo-registry."""
        engine = importlib.import_module("engine")
        self.assertEqual(engine.status_of("repo-registry", "change-review"), "green")


if __name__ == "__main__":
    unittest.main()

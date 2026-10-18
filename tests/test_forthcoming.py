"""Capabilities not built yet (data/forthcoming.yaml; WP5b F-16, revised by the supervisor).

Run with: python3 -m unittest discover -s tests. Each forthcoming capability names its test, an expected failure until
the capability is built. When one starts passing, unittest reports an "unexpected success": remove the capability
from data/forthcoming.yaml and the decorator here.

A capability not built is a gap in the software. It is not a compliance error: a measured non-pass of a policy is the
controller's error signal, kept in data/measured-gaps.yaml, and it is never a failing test (WP5b F-16).
"""
import pathlib
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


class ForthcomingTests(unittest.TestCase):
    def test_every_capability_names_its_expected_failure(self):
        """F-16: each forthcoming capability names a test here, marked as an expected failure, and a closing point."""
        rows = yaml.safe_load((ROOT / "data/forthcoming.yaml").read_text())["forthcoming"]
        source = pathlib.Path(__file__).read_text()
        for gid, row in rows.items():
            self.assertTrue(row["closes_in"].strip(), gid)
            path, cls, method = row["test"].split("::")
            self.assertEqual(path, "tests/test_forthcoming.py", gid)
            self.assertIn(f"    @unittest.expectedFailure\n    def {method}(", source, gid)

    def test_measured_gaps_are_not_tests(self):
        """F-16: a measured non-pass (the error signal) is data with its policy and check, never an expected failure."""
        rows = yaml.safe_load((ROOT / "data/measured-gaps.yaml").read_text())["measured"]
        source = pathlib.Path(__file__).read_text()
        for gid, row in rows.items():
            self.assertIn(row["color"], ("red", "yellow"), gid)
            self.assertNotIn(f"test_{gid.replace('-', '')}", source, gid)

    @unittest.expectedFailure
    def test_XF1_sensing_credential_has_administration_read(self):
        """XF-1, closes in WP6: the sensing credential is declared with Administration: read."""
        config = yaml.safe_load((ROOT / "config/sensing.yaml").read_text())
        self.assertIn("Administration: read", config["credential"]["permissions"])


if __name__ == "__main__":
    unittest.main()

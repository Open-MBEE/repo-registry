"""WP2a checks: license by type. Run with: python3 -m unittest discover -s tests

Each test names the WP2a requirement it checks (work-packages/WP2a-scope-of-work.md).
"""
import pathlib
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import licenses  # noqa: E402
import policies as P  # noqa: E402


def load(path):
    return yaml.safe_load(pathlib.Path(path).read_text())


KINDS = load(ROOT / "data/taxonomy/kinds.yaml")["kinds"]
POLICY = load(ROOT / "data/policies/license-by-type.yaml")


def run(repo_license, kind="tool/incubating", deviations=()):
    repos = {"r": {"name": "r", "license": repo_license}}
    return licenses.evaluate(repos, {"r": {"kind": kind}}, KINDS, POLICY, list(deviations))["repos"]["r"]


class LicenseTests(unittest.TestCase):
    def test_R1_policy_passes_meta_rules(self):
        """R-1: license-by-type passes every meta-rule and declares the org's plan."""
        pols, _ = P.load_policies(ROOT / "data/policies")
        self.assertIn("license-by-type", pols)
        self.assertIn("free", pols["license-by-type"]["github"]["available_on"])

    def test_R2_allowed_missing_unrecognized_and_off_list(self):
        """R-2: allowed is green; missing, NOASSERTION and off-list licenses are red."""
        self.assertEqual(run("Apache-2.0")["status"], "green")
        self.assertEqual(run("MIT")["status"], "green")
        self.assertEqual(run(None)["status"], "red")
        self.assertEqual(run("NOASSERTION")["status"], "red")
        self.assertEqual(run("MPL-2.0")["status"], "red")
        self.assertEqual(run("CC-BY-4.0", kind="media/incubating")["status"], "green")
        self.assertEqual(run("CC-BY-4.0", kind="tool/incubating")["status"], "red")
        self.assertEqual(run("MIT", kind="governance/sandbox")["status"], "red")

    def test_R3_rule_depends_only_on_type(self):
        """R-3: allowed sets are keyed by type, and every type in the taxonomy has one."""
        types = {k["type"] for k in KINDS.values()}
        self.assertEqual(set(POLICY["allowed_licenses"]), types)
        for kind in ("tool/sandbox", "tool/incubating", "tool/graduated"):
            self.assertEqual(run("MIT", kind=kind)["status"], "green", kind)

    def test_R4_exception_is_green_and_visible(self):
        """R-4: an accepted exception turns the check green, marked as an exception."""
        dev = {"repo": "r", "policy": "license-by-type", "reason": "depends on MPL code", "approved_by": "mzargham"}
        row = run("MPL-2.0", deviations=[dev])
        self.assertEqual(row["status"], "green")
        self.assertIn("accepted exception", row["detail"])

    def test_R5_only_one_policy_reads_the_license(self):
        """R-5: no other policy reads the license field."""
        pols, _ = P.load_policies(ROOT / "data/policies")
        readers = [pid for pid, p in pols.items() for c in (p["checks"]["automated"] or [])
                   if "license" in c["reads"]]
        self.assertEqual(readers, ["license-by-type"])

    def test_R6_report_replays(self):
        """R-6: the report is deterministic and matches the committed one."""
        with tempfile.TemporaryDirectory() as t:
            rep = pathlib.Path(t) / "r.yaml"
            subprocess.run([sys.executable, "scripts/licenses.py", "--snapshot", "data/snapshots/2026-10-18",
                            "--report", str(rep)], cwd=ROOT, check=True, capture_output=True)
            self.assertEqual(rep.read_text(), (ROOT / "data/reports/license-report.yaml").read_text())

    def test_R7_provisional(self):
        """R-7: the policy, the exceptions file and the report are PROVISIONAL."""
        self.assertEqual(POLICY["status"], "provisional")
        self.assertEqual(load(ROOT / "data/deviations.yaml")["status"], "provisional")
        self.assertEqual(load(ROOT / "data/reports/license-report.yaml")["status"], "provisional")


if __name__ == "__main__":
    unittest.main()

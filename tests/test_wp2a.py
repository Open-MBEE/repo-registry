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
import model  # noqa: E402
import policies as P  # noqa: E402


def load(path):
    return yaml.safe_load(pathlib.Path(path).read_text())


KINDS = model.kinds(load(ROOT / "data/taxonomy/kinds.yaml"))
POLICY = load(ROOT / "data/policies/license-by-type.yaml")


def run(repo_license, kind="tool/incubating", deviations=()):
    repos = {1: {"repo_id": 1, "name": "r", "license": repo_license}}
    type_, stage = kind.split("/")
    return licenses.evaluate(repos, {1: {"name": "r", "type": type_, "stage": stage}}, KINDS, POLICY,
                             list(deviations))["repos"][1]


class LicenseTests(unittest.TestCase):
    def test_R1_policy_passes_meta_rules(self):
        """R-1: license-by-type passes every meta-rule and declares the org's plan."""
        pols, _ = P.load_policies(ROOT / "data/policies")
        self.assertIn("license-by-type", pols)
        self.assertIn("free", pols["license-by-type"]["github"]["available_on"])

    def test_R2_allowed_missing_unrecognized_and_off_list(self):
        """R-2: allowed is green; missing, NOASSERTION and off-list licenses are red."""
        self.assertEqual(run("Apache-2.0")["color"], "green")
        self.assertEqual(run("MIT")["color"], "green")
        self.assertEqual(run(None)["color"], "red")
        self.assertEqual(run("NOASSERTION")["color"], "red")
        self.assertEqual(run("MPL-2.0")["color"], "red")
        self.assertEqual(run("CC-BY-4.0", kind="media/incubating")["color"], "green")
        self.assertEqual(run("CC-BY-4.0", kind="tool/incubating")["color"], "red")
        self.assertEqual(run("MIT", kind="governance/sandbox")["color"], "red")

    def test_R3_rule_depends_only_on_type(self):
        """R-3: allowed sets are keyed by type, and every type in the taxonomy has one."""
        types = {k["type"] for k in KINDS.values()}
        self.assertEqual(set(POLICY["allowed_licenses"]), types)
        for kind in ("tool/sandbox", "tool/incubating", "tool/graduated"):
            self.assertEqual(run("MIT", kind=kind)["color"], "green", kind)

    def test_R4_exception_is_green_and_visible(self):
        """R-4: an accepted exception turns the check green, marked as an exception."""
        dev = {"repo_id": 1, "name": "r", "policy": "license-by-type", "reason": "depends on MPL code",
               "approved_by": "mzargham"}
        row = run("MPL-2.0", deviations=[dev])
        self.assertEqual(row["color"], "green")
        self.assertIn("accepted exception", row["detail"])

    def test_R5_only_one_policy_reads_the_license(self):
        """R-5: no other policy reads the license field."""
        pols, _ = P.load_policies(ROOT / "data/policies")
        readers = [pid for pid, p in pols.items() for c in (p["checks"]["automated"] or [])
                   if "license" in c["reads"]]
        self.assertEqual(readers, ["license-by-type"])

    def test_R6_report_replays(self):
        """R-6: the report is deterministic (a view, never committed: WP5b OD4)."""
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            for t in (a, b):
                subprocess.run([sys.executable, "scripts/licenses.py", "--out", t], cwd=ROOT, check=True,
                               capture_output=True)
            rep = lambda t: (pathlib.Path(t) / "reports/license-report.yaml").read_text()  # noqa: E731
            self.assertEqual(rep(a), rep(b))
            self.assertEqual(yaml.safe_load(rep(a))["counts"], {"green": 77, "red": 38})

    def test_R7_provisional(self):
        """R-7: the policy set, the exceptions file and the rendered report are PROVISIONAL."""
        self.assertEqual(load(ROOT / "data/policies/_set.yaml")["status"], "provisional")
        self.assertEqual(load(ROOT / "data/deviations.yaml")["status"], "provisional")
        with tempfile.TemporaryDirectory() as t:
            subprocess.run([sys.executable, "scripts/licenses.py", "--out", t], cwd=ROOT, check=True, capture_output=True)
            self.assertEqual(load(pathlib.Path(t) / "reports/license-report.yaml")["status"], "provisional")


if __name__ == "__main__":
    unittest.main()

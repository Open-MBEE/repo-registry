"""WP4e checks: type and stage in the kind list. Run with: python3 -m unittest discover -s tests

Each test names the WP4e requirement it checks (work-packages/WP4e-scope-of-work.md).
"""
import pathlib
import re
import subprocess
import sys
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import recommend  # noqa: E402


def load(rel):
    return yaml.safe_load((ROOT / rel).read_text())


def entries():
    reg, asg = load("registry.yaml"), load("data/assignments.yaml")
    yield "registry.yaml org", reg["org"], {"name", "type", "stage"}
    for n, e in reg["repos"].items():
        yield f"registry.yaml {n}", e, None
    yield "data/assignments.yaml org", asg["org"], {"type", "stage", "decision"}
    for n, e in asg["repos"].items():
        yield f"data/assignments.yaml {n}", e, {"type", "stage", "decision"}


class KindListTests(unittest.TestCase):
    def test_R1_type_and_stage_or_reason_alone(self):
        """R-1: every entry has type and stage, or reason alone (OD2), and no kind field."""
        for where, e, fields in entries():
            self.assertNotIn("kind", e, where)
            if fields:
                self.assertEqual(set(e), fields, where)
            else:
                self.assertIn(set(e), ({"type", "stage"}, {"reason"}), where)

    def test_R2_type_and_stage_name_a_defined_kind(self):
        """R-2: each entry's type and stage name a defined kind, not an omitted one."""
        kinds = load("data/taxonomy/kinds.yaml")
        for where, e, _ in entries():
            if "type" in e:
                kind = recommend.kind_of(e)
                self.assertIn(kind, kinds["kinds"], where)
                self.assertNotIn(kind, kinds.get("omitted", {}), where)
                self.assertEqual((kinds["kinds"][kind]["type"], kinds["kinds"][kind]["stage"]),
                                 (e["type"], e["stage"]), where)

    def test_R3_every_repository_keeps_its_kind(self):
        """R-3: the computed kind of every repository equals the kind recorded before WP4e (the recommendation
        report, which still shows kinds by name, and the pilot)."""
        reg = load("registry.yaml")["repos"]
        report = load("data/reports/kind-recommendations.yaml")["repos"]
        self.assertEqual({n: recommend.kind_of(e) for n, e in reg.items()}, {n: r["kind"] for n, r in report.items()})
        for n, p in load("data/pilot.yaml")["repos"].items():
            self.assertEqual(recommend.kind_of(reg[n]), p["kind"], n)

    def test_R6_the_attribute_is_stage(self):
        """R-6: no data file or script names the attribute lifecycle; the taxonomy lists stages."""
        kinds = load("data/taxonomy/kinds.yaml")
        self.assertIn("stages", kinds)
        self.assertNotIn("lifecycles", kinds)
        for name, k in kinds["kinds"].items():
            self.assertIn("stage", k, name)
            self.assertNotIn("lifecycle", k, name)
        files = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "data", "scripts"],
                               cwd=ROOT, capture_output=True, text=True).stdout.split()
        hits = []
        for f in files:
            if f.startswith(("data/sources/", "data/snapshots/")) or not f.endswith((".py", ".yaml")):
                continue
            text = (ROOT / f).read_text()
            if re.search(r"attr: lifecycle|[\"']lifecycle[\"']|^\s*lifecycles?:", text, re.M):
                hits.append(f)
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()

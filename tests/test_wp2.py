"""WP2 checks: policies. Run with: python3 -m unittest discover -s tests

Each test names the WP2 requirement it checks (work-packages/WP2-scope-of-work.md).
"""
import copy
import gzip
import hashlib
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import policies as P  # noqa: E402

TOY = ROOT / "tests/fixtures/toy-policies"


def load(path):
    return yaml.safe_load(pathlib.Path(path).read_text())


def real():
    pols, deps = P.load_policies(ROOT / "data/policies")
    return dict(
        policies=pols, departures=deps,
        kinds_doc=load(ROOT / "data/taxonomy/kinds.yaml"), tiers_doc=load(ROOT / "data/taxonomy/tiers.yaml"),
        baseline=load(ROOT / "data/sources/openssf-security-baseline.yaml"), root=ROOT,
        cisa=set(load(ROOT / "data/sources/cisa-practices.yaml")["practices"]),
        nist=set(load(ROOT / "data/sources/nist-800-53.yaml")["controls"]),
        org_plan=load(ROOT / "data/sources/github-plan.yaml")["plan"],
        future=load(ROOT / "data/policies/_future.yaml"),
    )


def run(tmp, *extra):
    table, report = pathlib.Path(tmp) / "table.md", pathlib.Path(tmp) / "report.yaml"
    out = subprocess.run([sys.executable, str(ROOT / "scripts/policies.py"), "--table", str(table), "--report",
                          str(report), *extra], cwd=ROOT, capture_output=True, text=True)
    return out, table, report


class MetaRuleTests(unittest.TestCase):
    def test_D4_meta_rules_hold_on_the_policies(self):
        """D-4, R-1 to R-4, R-13 and R-6 (coverage): the real policy set breaks no meta-rule."""
        self.assertEqual(P.check(**real()), [])

    def test_R2_applies_if_rejects_other_attributes(self):
        """R-2: an applies-if rule reading anything but type, lifecycle or tier is rejected."""
        args = real()
        bad = copy.deepcopy(args["policies"]["codeowners"])
        bad["applies_if"] = {"attr": "stars", "gt": 10}
        args["policies"] = {"codeowners": bad}
        self.assertTrue(any("only type, lifecycle, tier" in p for p in P.check(**args)))
        bad["applies_if"] = {"signal": "is_tool"}
        self.assertTrue(any("may not use signals" in p for p in P.check(**args)))

    def test_R3_unknown_citations_rejected(self):
        """R-3: a policy can cite only CISA practices and NIST controls that exist in data/sources/."""
        args = real()
        bad = copy.deepcopy(args["policies"]["codeowners"])
        bad["cites"]["nist"] = ["XX-99"]
        bad["cites"]["cisa"] = ["CISA-P-NOT-REAL"]
        args["policies"]["codeowners"] = bad
        problems = P.check(**args)
        self.assertTrue(any("XX-99" in p for p in problems))
        self.assertTrue(any("CISA-P-NOT-REAL" in p for p in problems))

    def test_R4_sop_sections_required(self):
        """R-4: every SOP has Set up, Automated checks and Attested checks."""
        for pid, p in real()["policies"].items():
            text = (ROOT / p["sop"]).read_text()
            for heading in P.SOP_HEADINGS:
                self.assertIn(heading, text, pid)

    def test_R13_every_baseline_item_accounted_for(self):
        """R-13: each OpenSSF baseline item is adopted by a policy or departed with a reason, never both."""
        args = real()
        adopted = {i for p in args["policies"].values() for i in (p["cites"].get("openssf") or [])}
        departed = set(args["departures"]["openssf"])
        self.assertEqual(adopted | departed, set(args["baseline"]["items"]))
        self.assertEqual(adopted & departed, set())
        # removing a departure is caught
        args["departures"] = copy.deepcopy(args["departures"])
        args["departures"]["openssf"].pop("TI-1")
        self.assertTrue(any("TI-1" in p for p in P.check(**args)))

    def test_R6_no_two_policies_read_the_same_thing(self):
        """R-6: no automated check is duplicated across policies."""
        reads = [c["reads"] for p in real()["policies"].values() for c in (p["checks"]["automated"] or [])]
        self.assertEqual(len(reads), len(set(reads)))

    def test_R8_every_automated_check_names_its_permission(self):
        """R-8: each automated check says what it reads and the permission it needs."""
        for pid, p in real()["policies"].items():
            for c in p["checks"]["automated"] or []:
                self.assertTrue(c["reads"].startswith(("GET ", "GraphQL ")), pid)
                self.assertTrue(c["permission"].strip(), pid)

    def test_R11_provisional(self):
        """R-11: every policy, and the generated table, is marked PROVISIONAL."""
        for pid, p in real()["policies"].items():
            self.assertEqual(p["status"], "provisional", pid)
        self.assertIn("PROVISIONAL", (ROOT / "docs/policy-applicability.md").read_text())

    def test_R12_iso_text_not_committed(self):
        """R-12: ISO/IEC/IEEE 12207 is cited by clause number only, and no 8-word passage of it is in the repo.

        tests/fixtures/iso12207-2026-shingles.txt.gz holds truncated SHA-256 hashes of every 8-word sequence of the
        standard's text (lower-cased, letters and digits only), built once from the supervisor's licensed copy. It
        holds no text. Every tracked or untracked text file is hashed the same way and must share no hash with it.
        """
        for p in real()["policies"].values():
            for clause in p["cites"].get("iso12207") or []:
                self.assertRegex(str(clause), r"^\d+(\.\d+)*$")
        hashes = set(gzip.open(ROOT / "tests/fixtures/iso12207-2026-shingles.txt.gz", "rt").read().split())
        self.assertGreater(len(hashes), 60000)
        files = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT,
                               capture_output=True, text=True).stdout.split()
        hits = {}
        for name in files:
            if name.endswith(".gz"):
                continue
            try:
                words = re.findall(r"[a-z0-9]+", (ROOT / name).read_text(encoding="utf-8").lower())
            except (UnicodeDecodeError, FileNotFoundError):
                continue
            for i in range(len(words) - 7):
                if hashlib.sha256(" ".join(words[i:i + 8]).encode()).hexdigest()[:16] in hashes:
                    hits.setdefault(name, 0)
                    hits[name] += 1
        self.assertEqual(hits, {})


class ApplicabilityTests(unittest.TestCase):
    def test_R7_friction_follows_the_tiers(self):
        """R-7: sandbox carries the fewest policies, graduated the most; archived carries only the archive notice."""
        table = P.applicability(real()["policies"], load(ROOT / "data/taxonomy/kinds.yaml"))
        n = {k: len(v) for k, v in table.items()}
        self.assertLess(n["tool/sandbox"], n["tool/incubating"])
        self.assertLess(n["tool/incubating"], n["tool/graduated"])
        for k, v in table.items():
            if k.endswith("/archived"):
                self.assertEqual(v, ["archive-notice"], k)
            if k.endswith("/sandbox") and not k.startswith("governance"):
                self.assertEqual(set(v), {"codeowners", "project-files"}, k)
        self.assertLessEqual(max(n[k] for k in n if k.startswith("research/")), 2)

    def test_R9_applicability_replays(self):
        """R-9: the same taxonomy and policies always give the same table, matching the committed one."""
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            out_a, table_a, rep_a = run(a)
            out_b, table_b, rep_b = run(b)
            self.assertEqual(out_a.returncode, 0, out_a.stderr)
            self.assertEqual(table_a.read_text(), table_b.read_text())
            self.assertEqual(rep_a.read_text(), rep_b.read_text())
            self.assertEqual(table_a.read_text(), (ROOT / "docs/policy-applicability.md").read_text())
            self.assertEqual(rep_a.read_text(), (ROOT / "data/reports/policy-applicability.yaml").read_text())

    def test_R10_toy_policy_swap_needs_no_code_change(self):
        """R-10: a different policy set and taxonomy run through the same code."""
        with tempfile.TemporaryDirectory() as t:
            out, _, report = run(t, "--policies", str(TOY / "policies"), "--root", str(TOY),
                                 "--kinds", str(ROOT / "tests/fixtures/toy-kinds.yaml"),
                                 "--tiers", str(ROOT / "tests/fixtures/toy-tiers.yaml"),
                                 "--baseline", str(TOY / "baseline.yaml"), "--cisa", str(TOY / "cisa.yaml"),
                                 "--nist", str(TOY / "nist.yaml"))
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertEqual(load(report)["kinds"], {"thing/busy": ["only-rule"], "thing/quiet": []})


if __name__ == "__main__":
    unittest.main()

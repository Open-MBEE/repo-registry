"""WP4c checks: the governance kinds, and OpenSSF as a core citation. Run with: python3 -m unittest discover -s tests

Each test names the WP4c requirement it checks (work-packages/WP4c-scope-of-work.md).
"""
import pathlib
import sys
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import model  # noqa: E402
import policies as P  # noqa: E402

ORG = {"org-two-factor", "org-few-owners", "org-base-permission", "maintainers-match", "governance-roles-named"}


def load(rel):
    return yaml.safe_load((ROOT / rel).read_text())


def table():
    pols, _ = P.load_policies(ROOT / "data/policies")
    return pols, P.applicability(pols, load("data/taxonomy/kinds.yaml"))


class GovernanceKindTests(unittest.TestCase):
    def test_R1_one_type_at_different_stages(self):
        """R-1: the org is governance/graduated, repo-registry governance/sandbox; governance/incubating is defined."""
        kinds = load("data/taxonomy/kinds.yaml")
        self.assertIn("governance/incubating", model.kinds(kinds))
        self.assertNotIn("governance/incubating", kinds.get("omitted", {}))
        gov = lambda e: (e["type"], e["stage"])  # noqa: E731 (the kind list holds type and stage, WP4e)
        self.assertEqual(gov(load("registry.yaml")["org"]), ("governance", "graduated"))
        entry = next(e for e in load("registry.yaml")["repos"].values() if e["name"] == "repo-registry")
        self.assertEqual(gov(entry), ("governance", "sandbox"))
        self.assertEqual(gov(next(iter(load("data/assignments.yaml")["repos"].values()))), ("governance", "sandbox"))

    def test_R2_graduated_carries_org_and_repository_policies(self):
        """R-2: governance/graduated takes the 5 org policies and every policy governance/sandbox took before WP4c."""
        before = {"change-review", "codeowners", "contributing", "dependency-management", "history-protection",
                  "license-by-type", "project-files", "secret-protection", "security-design", "security-policy",
                  "static-analysis", "vulnerability-remediation", "workflow-least-privilege"}
        _, t = table()
        self.assertEqual(set(t["governance/graduated"]), ORG | before)

    def test_R3_friction_rises_with_the_stage(self):
        """R-3: sandbox like tool/sandbox; incubating like tool/incubating minus semantic-versioning; no org policy
        before graduated."""
        kinds = model.kinds(load("data/taxonomy/kinds.yaml"))
        self.assertEqual([kinds[f"governance/{s}"]["tier"] for s in ("sandbox", "incubating", "graduated")],
                         ["low", "medium", "high"])
        _, t = table()
        self.assertEqual(t["governance/sandbox"], t["tool/sandbox"])
        self.assertEqual(set(t["governance/incubating"]), set(t["tool/incubating"]) - {"semantic-versioning"})
        for stage in ("sandbox", "incubating"):
            self.assertEqual(set(t[f"governance/{stage}"]) & ORG, set(), stage)
        sizes = [len(t[f"governance/{s}"]) for s in ("sandbox", "incubating", "graduated")]
        self.assertEqual(sizes, sorted(sizes))
        self.assertLess(sizes[0], sizes[1])
        self.assertLess(sizes[1], sizes[2])

    def test_R4_no_rule_excludes_governance_graduated(self):
        """R-4: no applies-if rule excludes governance/graduated (or any governance kind) by name."""
        pols, _ = table()

        def excludes(pred, negated=False):
            if isinstance(pred, dict):
                if "not" in pred:
                    return excludes(pred["not"], not negated)
                if pred.get("attr") == "type" and (pred.get("eq") == "governance"):
                    return negated
                return any(excludes(p, negated) for k in ("all", "any") for p in pred.get(k, []))
            return False
        self.assertEqual([pid for pid, p in pols.items() if excludes(p["applies_if"])], [])


class CitationTests(unittest.TestCase):
    def test_R8_openssf_is_a_core_citation(self):
        """R-8: every policy has cites.openssf, and meta-rule 7 rejects a policy without it."""
        pols, deps = P.load_policies(ROOT / "data/policies")
        for pid, p in pols.items():
            self.assertIsInstance(p["cites"].get("openssf"), list, pid)
        args = dict(kinds_doc=load("data/taxonomy/kinds.yaml"), tiers_doc=load("data/taxonomy/tiers.yaml"),
                    baseline=load("data/sources/openssf-security-baseline.yaml"), root=ROOT,
                    cisa=set(load("data/sources/cisa-practices.yaml")["practices"]),
                    nist=set(load("data/sources/nist-800-53.yaml")["controls"]),
                    org_plan=load("data/sources/github-plan.yaml")["plan"], future=load("data/policies/_future.yaml"))
        self.assertEqual(P.check(pols, deps, **args), [])
        del pols["codeowners"]["cites"]["openssf"]
        self.assertTrue(any("cites.openssf is required" in p for p in P.check(pols, deps, **args)))
        for doc in ("README.md", "docs/current-state.md", "docs/policy-basis-review.md", "docs/policy-format.md"):
            text = (ROOT / doc).read_text()
            self.assertRegex(text, r"(?is)(core|three pieces of guidance).{0,400}openssf|openssf.{0,200}core", doc)


if __name__ == "__main__":
    unittest.main()

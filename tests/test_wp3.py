"""WP3 checks: org governance. Run with: python3 -m unittest discover -s tests

Each test names the WP3 requirement it checks (work-packages/WP3-scope-of-work.md). All offline: they read the stored
snapshot and data files. scripts/privacy_check.py does the live, read-only privacy cross-check.
"""
import copy
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
import org  # noqa: E402
import policies as P  # noqa: E402

SNAP = ROOT / "data/snapshots/2026-10-18/org.json"


def load(path):
    return yaml.safe_load(pathlib.Path(path).read_text())


def snapshot():
    return json.loads(SNAP.read_text())


class ReadOnlyTests(unittest.TestCase):
    def test_R1_snapshot_only_reads(self):
        """R-1: the org snapshot only makes GET requests through gh."""
        src = (ROOT / "scripts/org_snapshot.py").read_text()
        self.assertIn('["gh", "api", "-X", "GET"]', src)
        self.assertEqual(re.findall(r'"-X", "(\w+)"', src), ["GET"])
        self.assertNotIn("mutation", src)


class PolicyTests(unittest.TestCase):
    def test_R3_org_policies_pass_meta_rules_and_adopt_SB2(self):
        """R-3: org policies meet WP2's meta-rules, apply only to the org's administration, and SB-2 is adopted."""
        pols, deps = P.load_policies(ROOT / "data/policies")
        table = P.applicability(pols, load(ROOT / "data/taxonomy/kinds.yaml"))
        org_ids = {"org-two-factor", "org-few-owners", "org-base-permission", "maintainers-match",
                   "governance-roles-named"}
        self.assertEqual(set(table["governance/graduated"]), org_ids)
        for kind, ids in table.items():
            if kind != "governance/graduated":
                self.assertEqual(set(ids) & org_ids, set(), kind)
        self.assertNotIn("SB-2", deps["openssf"])
        self.assertIn("SB-2", pols["org-two-factor"]["cites"]["openssf"])


class PlanTests(unittest.TestCase):
    """G-3: no policy requires a feature OpenMBEE's plan lacks; unconfirmed features are flagged for research."""

    def test_every_policy_works_on_the_org_plan(self):
        plan = load(ROOT / "data/sources/github-plan.yaml")["plan"]
        pols, _ = P.load_policies(ROOT / "data/policies")
        for pid, p in pols.items():
            self.assertIn(plan, p["github"]["available_on"], pid)

    def test_needs_research_is_flagged_and_listed(self):
        future = load(ROOT / "data/policies/_future.yaml")
        pols, _ = P.load_policies(ROOT / "data/policies")
        flagged = {f for p in pols.values() for f in (p["github"].get("needs_research") or [])}
        self.assertEqual(flagged, {"immutable-releases", "rulesets"})
        self.assertLessEqual(flagged, set(future["needs_research"]))
        for fid, f in future["needs_research"].items():
            self.assertTrue(f["question"].strip(), fid)

    def test_enterprise_only_features_are_not_required(self):
        future = load(ROOT / "data/policies/_future.yaml")
        pols, _ = P.load_policies(ROOT / "data/policies")
        for pid, p in pols.items():
            self.assertEqual(set(p["github"].get("needs_research") or []) & set(future["features"]), set(), pid)


class MatchTests(unittest.TestCase):
    def run_check(self, snap=None, codeowners=None):
        maint = load(ROOT / "data/maintainers.yaml")
        owners = codeowners if codeowners is not None else org.codeowners_logins(
            (ROOT / "data/proposed-codeowners").read_text())
        return org.check(snap or snapshot(), maint, owners)

    def test_D3_proposed_codeowners_match_the_list(self):
        """D-3: the proposed CODEOWNERS names exactly the listed maintainers."""
        owners = org.codeowners_logins((ROOT / "data/proposed-codeowners").read_text())
        self.assertEqual(owners, set(load(ROOT / "data/maintainers.yaml")["maintainers"]))

    def test_R4_check_replays(self):
        """R-4: the match check is deterministic and matches the committed report."""
        with tempfile.TemporaryDirectory() as t:
            rep = pathlib.Path(t) / "r.yaml"
            for _ in range(2):
                subprocess.run([sys.executable, "scripts/org.py", "--snapshot", str(SNAP.relative_to(ROOT)),
                                "--report", str(rep)], cwd=ROOT, check=True, capture_output=True)
                self.assertEqual(rep.read_text(), (ROOT / "data/reports/maintainers-match.yaml").read_text())

    def test_R5_unreadable_is_yellow_not_off(self):
        """R-5: if the owner list can't be read, the check says yellow; unreadable settings are stored as unreadable."""
        snap = snapshot()
        snap["owners"] = {"readable": False, "value": None, "reason": "test"}
        rows = self.run_check(snap)["rows"]
        self.assertTrue(any(r["check"] == "owners-readable" and r["status"] == "yellow" for r in rows))
        self.assertFalse(any(r["check"] == "owner-is-listed" for r in rows))
        for field, v in snapshot()["settings"].items():
            if not v["readable"]:
                self.assertIsNone(v["value"], field)
                self.assertTrue(v["reason"], field)

    def test_R6_provisional(self):
        """R-6: the list, the proposed CODEOWNERS, the maintainer policy and the org policies are PROVISIONAL."""
        self.assertEqual(load(ROOT / "data/maintainers.yaml")["status"], "provisional")
        self.assertIn("PROVISIONAL", (ROOT / "data/proposed-codeowners").read_text().splitlines()[0])
        self.assertIn("PROVISIONAL", (ROOT / "docs/maintainer-policy.md").read_text())
        self.assertEqual(load(ROOT / "data/reports/maintainers-match.yaml")["status"], "provisional")


class PrivacyTests(unittest.TestCase):
    def test_R8_snapshot_names_only_public_owners(self):
        """R-8: the snapshot names owners only if their membership is public, and records no role for others."""
        snap = snapshot()
        public = set(snap["public_members"]["value"])
        self.assertLessEqual(set(snap["owners"]["value"]["public_logins"]), public)
        self.assertEqual(set(snap["owners"]["value"]), {"count", "public_logins", "concealed_count"})
        for login, rec in snap["listed_maintainers"].items():
            self.assertEqual(set(rec), {"membership_public", "last_public_commit_in_org"}, login)
        self.assertLessEqual(set(snap["public_owner_activity"]), public)

    def test_R8_check_reveals_nothing_about_concealed_roles(self):
        """R-8: the check's output is identical whether or not a listed concealed member is an owner."""
        maint = load(ROOT / "data/maintainers.yaml")
        owners_file = set(maint["maintainers"])
        snap = snapshot()
        concealed = [l for l, r in snap["listed_maintainers"].items() if not r["membership_public"]]
        self.assertTrue(concealed)
        # The check sees only public logins and a concealed total, so model "is an owner" as the total including them
        # or not: the total is reported as-is, never minus the listed people, so the rows are the same.
        base = org.check(snap, maint, owners_file)["rows"]
        for r in base:
            if r["subject"] in concealed and r["check"] == "is-org-owner":
                self.assertEqual(r["status"], "yellow")
                self.assertNotIn("owner", r["detail"].replace("org role", ""))
        concealed_rows = [r for r in base if r["check"] == "concealed-owners"]
        self.assertEqual(len(concealed_rows), 1)
        self.assertIn(str(snap["owners"]["value"]["concealed_count"]), concealed_rows[0]["detail"])
        self.assertFalse(any("not listed" in r["detail"] or "unlisted" in r["detail"] for r in base))

    def test_R8_names_in_repo_are_public_or_supervisor_named(self):
        """R-8: every GitHub login the governance data names is a public member or one the supervisor named."""
        snap = snapshot()
        allowed = set(snap["public_members"]["value"]) | set(load(ROOT / "data/maintainers.yaml")["maintainers"])
        named = set(snap["owners"]["value"]["public_logins"]) | set(snap["listed_maintainers"])
        named |= org.codeowners_logins((ROOT / "data/proposed-codeowners").read_text())
        self.assertLessEqual(named, allowed)


if __name__ == "__main__":
    unittest.main()

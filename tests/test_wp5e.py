"""WP5e checks: verified code owners for high-tier repositories. Run with: python3 -m unittest discover -s tests

Each test names the WP5e requirement it checks (work-packages/WP5e-scope-of-work.md). Test records use placeholder
values only: no real person's facts are written here (R-5).
"""
import pathlib
import sys
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
import model  # noqa: E402
import validate  # noqa: E402
from test_wp5 import copy_repo, edit  # noqa: E402

POLICY = "data/policies/verified-code-owners.yaml"
ANCHOR = "    basis: A founder, publicly named as an admin elsewhere (supervisor).\n"
RECORD = ("    verification:\n      legal_name: TEST-NAME\n      country_of_residence: TEST-COUNTRY\n"
          "      affiliation: TEST-AFFILIATION\n      verified_by: {by}\n      date: 2026-10-18\n"
          "      policy_version: abc1234\n")


def problems_with(record):
    with copy_repo() as tmp:
        edit(tmp, "data/maintainers.yaml", ANCHOR, ANCHOR + record)
        return validate.check(pathlib.Path(tmp))


class PolicyTests(unittest.TestCase):
    def test_R1_in_effect_for_exactly_the_high_tier(self):
        """R-1: the policy is in effect for exactly the high-tier kinds, and says what is verified, by whom, how often."""
        kinds = model.kinds(model.load("data/taxonomy/kinds.yaml"))
        policy = yaml.safe_load((ROOT / POLICY).read_text())
        self.assertEqual(policy["applies_if"], {"attr": "tier", "eq": "high"})
        self.assertTrue({k for k, v in kinds.items() if v["tier"] == "high"})
        meaning = " ".join(policy["meaning"].split())
        for words in ("identity", "sanctioned party", "ordinarily resident", "organization of concern",
                      "organization owner", "12 months"):
            self.assertIn(words, meaning)
        self.assertNotIn("nationality", meaning.lower())

    def test_R2_every_citation_names_a_quoted_source_item(self):
        """R-2: the policy cites the DoD CIO memo by section and the adopted secondary sources, and every ID exists."""
        cites = yaml.safe_load((ROOT / POLICY).read_text())["cites"]
        for key in ("dodcio", "ofac", "ssdf", "c_scrm"):
            self.assertTrue(cites.get(key), key)
        self.assertIn("2.C(6)", cites["dodcio"])
        self.assertEqual(validate.check(ROOT), [])  # the schema's foreign keys by source: every cited ID exists


class RecordTests(unittest.TestCase):
    def test_R3_a_well_formed_record_is_valid(self):
        """R-3: a record with the published facts, another maintainer as verifier, a date and a version is valid."""
        self.assertEqual(problems_with(RECORD.format(by=6760647)), [])

    def test_R3_malformed_records_are_rejected(self):
        """R-3: a missing column, an extra column, an unknown verifier, or a self-verification is rejected."""
        cases = [
            (RECORD.format(by=6760647).replace("      affiliation: TEST-AFFILIATION\n", ""), "affiliation: missing"),
            (RECORD.format(by=6760647) + "      passport_number: X\n", "column 'passport_number' is not declared"),
            (RECORD.format(by=1), "verified_by: 1 is not a maintainer"),
            (RECORD.format(by=60184290), "can't verify themself"),
        ]
        for record, named in cases:
            with self.subTest(named=named):
                self.assertTrue(any(named in p for p in problems_with(record)))

    def test_R5_the_record_holds_only_the_published_facts(self):
        """R-5 (OD2): the record's declared columns are the three published facts and the verification's own data."""
        columns = set(model.declared()["tables"]["maintainer_verification"]["columns"])
        self.assertEqual(columns, {"user_id", "legal_name", "country_of_residence", "affiliation", "verified_by", "date",
                                   "policy_version"})


class GapTests(unittest.TestCase):
    def test_R4_non_conformance_is_a_measured_gap_not_a_failure(self):
        """R-4: while a named maintainer has no verification, the policy's non-conformance on the high-tier repository
        is a measured gap, and the model is still valid."""
        verified = {r["user_id"] for r in model.rows("maintainer_verification", ROOT)}
        unverified = {r["user_id"] for r in model.rows("maintainer", ROOT)} - verified
        gaps = model.load("data/measured-gaps.yaml")["measured"]
        ours = [g for g in gaps.values() if g["policy"] == "verified-code-owners"]
        if unverified:
            self.assertTrue(ours)
            self.assertEqual({g["name"] for g in ours}, {".github"})
        self.assertEqual(validate.check(ROOT), [])


if __name__ == "__main__":
    unittest.main()

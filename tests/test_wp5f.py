"""WP5f checks: owners and maintainers first. Run with: python3 -m unittest discover -s tests

Each test names the WP5f requirement it checks (work-packages/WP5f-scope-of-work.md). Test records use invented
maintainers only (IDs 1 to 4, logins test-a to test-d): no real person is recorded as an owner here.
"""
import pathlib
import re
import sys
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
import model  # noqa: E402
import validate  # noqa: E402
from test_wp5 import copy_repo, edit  # noqa: E402

FAKE = {1: "test-a", 2: "test-b", 3: "test-c", 4: "test-d"}


def problems_with_owners(owners):
    """Validate a copy with four invented maintainers added, and `owners` set to the given IDs."""
    with copy_repo() as tmp:
        root = pathlib.Path(tmp)
        entries = "".join(f"  {uid}:\n    login: {login}\n    name: Test {login}\n    basis: A test record.\n"
                          for uid, login in FAKE.items())
        edit(tmp, "data/maintainers.yaml", "\nmaintainers:", "\nmaintainers:\n" + entries.rstrip("\n"))
        codeowners = root / "data/proposed-codeowners"
        codeowners.write_text(codeowners.read_text().rstrip("\n") + "".join(f" @{x}" for x in FAKE.values()) + "\n")
        edit(tmp, "data/maintainers.yaml", "owners: []", f"owners: {owners}")
        return validate.check(root)


class PolicyTests(unittest.TestCase):
    def test_R1_the_policy_records_how_the_first_governors_are_chosen(self):
        """R-1: the maintainer policy says who chooses the first owners and maintainers, what qualifies them, what
        happens to owners not kept, and that carrying it out comes later."""
        text = (ROOT / "docs/maintainer-policy.md").read_text()
        section = text.split("## How the first owners and maintainers are chosen")[1].split("\n## ")[0]
        for words in ("co-founders", "this policy as written", "2 or 3", "become members", "decided later",
                      "placeholder"):
            self.assertIn(words, section)


class OwnerRecordTests(unittest.TestCase):
    def test_R2_no_owners_are_recorded_yet(self):
        """R-2: until the co-founders' decision is recorded, `owners` is empty, and the model is valid."""
        self.assertEqual(model.load("data/maintainers.yaml")["owners"], [])
        self.assertEqual(validate.check(ROOT), [])

    def test_R2_a_recorded_set_is_two_or_three_maintainers(self):
        """R-2: two or three named maintainers are valid; one, four, a repeat or a non-maintainer is rejected."""
        self.assertEqual(problems_with_owners([1, 2]), [])
        self.assertEqual(problems_with_owners([1, 2, 3]), [])
        for owners, named in (([1], "2 or 3"), ([1, 2, 3, 4], "2 or 3"), ([1, 1], "listed twice"),
                              ([1, 99], "is not a maintainer")):
            with self.subTest(owners=owners):
                self.assertTrue(any(named in p for p in problems_with_owners(owners)))


class BriefTests(unittest.TestCase):
    def test_the_brief_is_a_labelled_hypothetical(self):
        """D-2 (OD5): the brief shows its shape with invented people, says it is not the proposed decision, names no
        real maintainer, and shows no one's membership or role."""
        text = (ROOT / "work-packages/WP5f-decision-brief.md").read_text()
        self.assertIn("HYPOTHETICAL", text)
        self.assertIn("not the proposed decision", text)
        for m in model.load("data/maintainers.yaml")["maintainers"].values():
            self.assertNotIn(m["login"], text)
            self.assertNotIn(m["name"], text)
        facts = text.split("## The facts to weigh")[1].split("\n## ")[0]
        self.assertNotRegex(facts, r"(?i)\| *(owner|member) *\|")


class RoadmapTests(unittest.TestCase):
    def test_R4_the_package_is_on_the_critical_path_ahead_of_wp6(self):
        """R-4: the status puts WP5f ahead of WP6, as critical path, with the fifth approval first."""
        status = (ROOT / "docs/status.md").read_text()
        self.assertLess(status.index("WP5f, owners and maintainers first"), status.index("WP6, the engine"))
        self.assertIn("critical path", status)
        self.assertRegex(status, r"fifth maintainer\s+approval")


if __name__ == "__main__":
    unittest.main()

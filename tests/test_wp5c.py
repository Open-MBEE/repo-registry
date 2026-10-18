"""WP5c checks: taxonomy refinements from the fit analysis. Run with: python3 -m unittest discover -s tests

Each test names the WP5c requirement it checks (work-packages/WP5c-scope-of-work.md).
"""
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
import model  # noqa: E402
import recommend  # noqa: E402
import render  # noqa: E402

KINDS = model.load("data/taxonomy/kinds.yaml")
REPOS = model.repos(ROOT)


def by_name(name):
    return next(rid for rid, r in REPOS.items() if r["name"] == name)


def candidate(repo, decided=None):
    """The rules' candidate for one repository row, with the given maintainer decisions."""
    rid = repo["repo_id"]
    return recommend.recommend({rid: repo}, KINDS, decided or {})[rid]


class PrecedenceTests(unittest.TestCase):
    def test_R1_maintainer_then_topic_then_inference(self):
        """R-1: a maintainer's decision beats a topic, a topic beats inference, and the source says which."""
        repo = dict(REPOS[by_name("OpenSysML")])  # a tool by inference (Python, releases below 1.0)
        self.assertEqual((candidate(repo)["kind"], candidate(repo)["source"]), ("tool/sandbox", "inferred"))
        repo["topics"] = ["sysml", "openmbee-research"]
        self.assertEqual((candidate(repo)["kind"], candidate(repo)["source"]), ("research/sandbox", "topic"))
        decided = {repo["repo_id"]: {"name": "OpenSysML", "type": "tool", "stage": "incubating", "source": "maintainer",
                                     "decision": "test"}}
        self.assertEqual((candidate(repo, decided)["kind"], candidate(repo, decided)["source"]),
                         ("tool/incubating", "maintainer"))

    def test_R2_no_topic_or_two_topics_declare_nothing(self):
        """R-2: none, or more than one, type topic declares nothing; the next source down gives the kind."""
        repo = dict(REPOS[by_name("OpenSysML")])
        repo["topics"] = ["openmbee-media", "openmbee-research"]
        r = candidate(repo)
        self.assertEqual((r["kind"], r["source"], r["declared_type"]), ("tool/sandbox", "inferred", None))

    def test_R5_rules_never_change_a_maintainer_entry(self):
        """R-5: the refresh never lists a maintainer entry; the maintainer entries are the org, repo-registry and
        .github (OD4), and nothing else."""
        reg = model.load("registry.yaml")
        decided = sorted(e["name"] for e in reg["repos"].values() if e["source"] == "maintainer")
        self.assertEqual(decided, [".github", "repo-registry"])
        self.assertEqual(reg["org"]["source"], "maintainer")
        github = reg["repos"][by_name(".github")]
        self.assertEqual((github["type"], github["stage"]), ("governance", "graduated"))
        with tempfile.TemporaryDirectory() as t:
            render.render(t, ROOT)
            changes = yaml.safe_load((pathlib.Path(t) / "kind-list-refresh.yaml").read_text())["changes"] or {}
        self.assertEqual(changes, {})  # the refresh is applied: nothing left to change
        self.assertFalse(any(reg["repos"][rid]["source"] == "maintainer" for rid in changes))


class ForkTests(unittest.TestCase):
    def test_R3_forks_are_classified_from_their_upstream(self):
        """R-3 (OD2): a fork with changes of ours is research, or media where they are mostly models; a mirror is
        unclassified with the mirror reason, and excluded from the pilot with it where it is excluded."""
        forks = json.loads((model.snapshot_dir() / "forks.json").read_text())["forks"]
        reg = model.load("registry.yaml")["repos"]
        exclude = model.load("data/exclude.yaml")["repos"]
        for rid, f in forks.items():
            rid = int(rid)
            with self.subTest(fork=f["name"]):
                self.assertTrue(f["readable"])
                entry = reg[rid]
                if f["ahead_by"] == 0:
                    self.assertIn("A mirror", entry["reason"])
                    if rid in exclude:
                        self.assertIn("a mirror", exclude[rid]["reason"])
                elif 2 * f["model_files_changed"] > f["files_changed"]:
                    self.assertEqual(entry["type"], "media")
                else:
                    self.assertEqual(entry["type"], "research")

    def test_R4_the_fork_read_only_reads(self):
        """R-4: the fork read makes only GET requests through gh, and is stored beside the snapshot."""
        src = (ROOT / "scripts/fork_snapshot.py").read_text()
        self.assertEqual(re.findall(r'"-X", "(\w+)"', src), ["GET"])
        self.assertNotIn("mutation", src)
        self.assertTrue((model.snapshot_dir() / "forks.json").exists())


class SignalTests(unittest.TestCase):
    def test_example_alone_decides_no_type(self):
        """Default: "example" alone decides no type; a repository with only that is unclassified with its reason."""
        repo = {**REPOS[by_name("OpenSysML")], "name": "foo-example", "description": "", "primary_language": None,
                "root_files": ["README.md"], "topics": []}
        r = candidate(repo)
        self.assertEqual(r["kind"], "unclassified")
        self.assertIn("An example", r["reason"])

    def test_notebook_or_model_only_is_media(self):
        """Fit analysis 3: a notebook-only or model-only repository is media, unless a research word applies."""
        repo = {**REPOS[by_name("OpenSysML")], "name": "foo", "description": "", "primary_language": None,
                "root_files": ["demo.ipynb"], "topics": []}
        self.assertEqual(candidate(repo)["kind"].split("/")[0], "media")

    def test_archived_with_no_type_stays_unclassified(self):
        """OD3: an archived repository with no type signal stays unclassified, with its reason."""
        reg = model.load("registry.yaml")["repos"]
        archived = [e for rid, e in reg.items() if REPOS[rid].get("archived") and "reason" in e
                    and not REPOS[rid].get("fork")]
        self.assertTrue(archived)
        for e in archived:
            self.assertIn("Archived, with no type signal", e["reason"])


class FitTests(unittest.TestCase):
    def test_R7_fit_report_counts_unclassified_by_reason(self):
        """R-7: the rendered fit report gives the unclassified repositories by reason, for the kind list and the
        rules' draft."""
        with tempfile.TemporaryDirectory() as t:
            render.render(t, ROOT)
            text = (pathlib.Path(t) / "fit-report.md").read_text()
        self.assertIn("| Unclassified because | Repositories |", text)
        unclassified = sum(1 for e in model.load("registry.yaml")["repos"].values() if "reason" in e)
        self.assertIn(f"{unclassified} unclassified", text)


if __name__ == "__main__":
    unittest.main()

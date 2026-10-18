"""WP5 checks: the meta-rule check that keeps invalid data off main. Run with: python3 -m unittest discover -s tests

Each test names the WP5 requirement it checks (work-packages/WP5-scope-of-work.md).
"""
import contextlib
import io
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import history_privacy_check  # noqa: E402
import validate  # noqa: E402

SNAPSHOT = "data/snapshots/2026-10-18"


def copy_repo():
    tmp = tempfile.TemporaryDirectory()
    for f in validate.files(ROOT):
        (pathlib.Path(tmp.name) / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / f, pathlib.Path(tmp.name) / f)
    subprocess.run(["git", "init", "-q"], cwd=tmp.name, check=True)  # validate lists files with git
    return tmp


def edit(root, rel, old, new):
    path = pathlib.Path(root) / rel
    text = path.read_text()
    assert old in text, (rel, old)
    path.write_text(text.replace(old, new, 1))


def regenerate(root, *scripts):
    args = {"licenses.py": ["--snapshot", SNAPSHOT], "pilot.py": ["--snapshot", SNAPSHOT],
            "briefing.py": ["--snapshot", SNAPSHOT], "policies.py": []}
    for s in scripts:
        subprocess.run([sys.executable, f"scripts/{s}", *args[s]], cwd=root, check=True, capture_output=True)


# One deliberately invalid change per data file: (file, text to replace, replacement, words the problem names).
INVALID = [
    ("data/taxonomy/kinds.yaml", "status: provisional", "status: draft", "status must be"),
    ("data/taxonomy/tiers.yaml", "# PROVISIONAL", "# Draft", "first line"),
    ("registry.yaml", '  "OpenSysML":\n    kind: tool/sandbox', '  "OpenSysML":\n    kind: tool/beta',
     "OpenSysML: kind 'tool/beta' is not a kind"),
    ("registry.yaml", '  "OpenSysML":\n    kind: tool/sandbox', '  "OpenSysML":\n    kind: tool/sandbox\n    tier: low',
     "no fields other than kind and reason"),
    ("data/assignments.yaml", "    kind: governance/sandbox", "    kind: governance/graduated",
     "repo-registry: assigned governance/graduated"),
    ("data/policies/codeowners.yaml", "\nsop:", "\nsop_moved:", "data/policies"),
    ("data/maintainers.yaml", "  rkarban:", "  rkarban!:", "is not a GitHub login"),
    ("data/proposed-codeowners", " @HuiJun", "", "must list exactly the maintainers"),
    ("data/deviations.yaml", "deviations: []",
     "deviations:\n  - {repo: OpenSysML, policy: license-by-type, reason: test, approved_by: someone-else}",
     "someone-else is not a maintainer"),
    ("data/pilot-rule.yaml", "{attr: type, eq: tool}", "{attr: type, equals: tool}", "exactly one operator"),
    ("data/pilot.yaml", "  aircraftengine-simulation:", "  no-such-repo:", "no-such-repo is not in registry.yaml"),
    ("data/exclude.yaml", "  apv: ", "  apv-renamed: ", "apv is neither in the pilot nor excluded"),
    ("data/expected-gaps.yaml", "    closes_in: \"R3", "    closes: \"R3", "XF-2: needs"),
]


class ValidTests(unittest.TestCase):
    def test_D1_real_data_is_valid_and_replays(self):
        """D-1, R-1, R-3: the data on this branch meets every meta-rule, and every generated file replays."""
        self.assertEqual(validate.check(ROOT), [])
        self.assertEqual(validate.replay(ROOT), [])


class InvalidTests(unittest.TestCase):
    def test_R1_each_invalid_file_fails_with_a_named_problem(self):
        """R-1: for each data file, a deliberately invalid copy fails, and the problem names what is wrong."""
        for rel, old, new, named in INVALID:
            with self.subTest(file=rel, named=named):
                with copy_repo() as tmp:
                    edit(tmp, rel, old, new)
                    problems = validate.check(pathlib.Path(tmp))
                    self.assertTrue(any(named in p for p in problems), problems)

    def test_R1_the_command_exits_non_zero(self):
        """R-1: the command a pull request runs exits non-zero on invalid data, and names the problem."""
        with copy_repo() as tmp:
            edit(tmp, *INVALID[2][:3])
            run = subprocess.run([sys.executable, "scripts/validate.py", "--no-replay"], cwd=tmp, capture_output=True,
                                 text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("tool/beta", run.stderr)

    def test_R3_hand_edit_to_a_generated_file_fails(self):
        """R-3: a hand edit to a generated file fails the replay."""
        with copy_repo() as tmp:
            edit(tmp, "docs/pilot-briefing.md", "# Pilot briefing", "# Pilot briefing (edited)")
            self.assertEqual(validate.check(pathlib.Path(tmp)), [])
            self.assertTrue(any(p.startswith("docs/pilot-briefing.md:") for p in validate.replay(pathlib.Path(tmp))))


class ComplianceTests(unittest.TestCase):
    def test_R2_out_of_compliance_is_valid(self):
        """R-2: a kind change that leaves a repository red (its MIT license isn't allowed for governance) is valid."""
        with copy_repo() as tmp:
            report = lambda: yaml.safe_load((pathlib.Path(tmp) / "data/reports/license-report.yaml").read_text())  # noqa: E731
            self.assertEqual(report()["repos"]["arch_model"]["status"], "green")
            edit(tmp, "registry.yaml", '  "arch_model":\n    kind: media/incubating',
                 '  "arch_model":\n    kind: governance/sandbox')
            regenerate(tmp, "licenses.py", "pilot.py", "briefing.py")
            self.assertEqual(report()["repos"]["arch_model"]["status"], "red")
            self.assertEqual(validate.check(pathlib.Path(tmp)), [])
            self.assertEqual(validate.replay(pathlib.Path(tmp)), [])

    def test_R2_kind_change_without_regenerating_names_the_files(self):
        """R-2, R-3: a kind change whose derived files weren't regenerated fails, and says which files to regenerate."""
        with copy_repo() as tmp:
            edit(tmp, "registry.yaml", '  "arch_model":\n    kind: media/incubating',
                 '  "arch_model":\n    kind: tool/sandbox')
            self.assertEqual(validate.check(pathlib.Path(tmp)), [])
            stale = {p.split(":")[0] for p in validate.replay(pathlib.Path(tmp))}
            self.assertIn("data/reports/license-report.yaml", stale)


class HistoryPrivacyTests(unittest.TestCase):
    def test_R6_history_scan_finds_a_name_only_in_an_old_commit(self):
        """R-6: a concealed login in an earlier commit, since removed, is found; the scan prints no login."""
        H = history_privacy_check
        with tempfile.TemporaryDirectory() as tmp:
            git = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=tmp,  # noqa: E731
                                            check=True, capture_output=True)
            git("init", "-q", "-b", "main")
            (pathlib.Path(tmp) / "data").mkdir()
            (pathlib.Path(tmp) / "data/maintainers.yaml").write_text("maintainers: {known-person: {}}\n")
            (pathlib.Path(tmp) / "notes.md").write_text("met hidden-person today\n")
            git("add", "-A"); git("commit", "-q", "-m", "first")  # noqa: E702
            (pathlib.Path(tmp) / "notes.md").write_text("nothing here\n")
            git("commit", "-q", "-am", "second")
            members = {"orgs/x/members?per_page=100": {"hidden-person", "known-person", "public-person"},
                       "orgs/x/public_members?per_page=100": {"public-person"}}
            out, cwd = io.StringIO(), pathlib.Path.cwd()
            try:
                os.chdir(tmp)
                with unittest.mock.patch.object(H, "logins", members.__getitem__), \
                        unittest.mock.patch.object(sys, "argv", ["h", "--org", "x", "main"]), \
                        contextlib.redirect_stdout(out), self.assertRaises(SystemExit):
                    H.main()
            finally:
                os.chdir(cwd)
            self.assertIn("paths naming one: 1", out.getvalue())
            self.assertIn("notes.md", out.getvalue())
            self.assertNotIn("hidden-person", out.getvalue())


class RecordTests(unittest.TestCase):
    def test_R7_every_cited_commit_resolves(self):
        """R-7: every commit SHA cited in work-packages/ and docs/ resolves in this repository's history."""
        # Commits of other repositories (the cited sources) are named, with their repository, in the source tables.
        external = set()
        for doc in ("docs/lifecycle-stage-map.md", "docs/policy-basis-review.md", "docs/maintainer-policy.md"):
            for para in re.split(r"\n\s*\n|\n(?=\|)", (ROOT / doc).read_text()):  # paragraphs and table rows
                if re.search(r"[a-z-]+/[a-z-]+", para):
                    external |= set(re.findall(r"(?:commit|at) ([0-9a-f]{7})\b", para))
        cited = set()
        for path in list((ROOT / "work-packages").glob("*.md")) + list((ROOT / "docs").rglob("*.md")):
            for word in re.findall(r"(?<![\w/.-])[0-9a-f]{7}(?![\w-])", path.read_text()):
                if re.search(r"[a-f]", word) and re.search(r"[0-9]", word):
                    cited.add(word)
        unresolved = sorted(s for s in cited - external if subprocess.run(
            ["git", "cat-file", "-e", f"{s}^{{commit}}"], cwd=ROOT, capture_output=True).returncode)
        self.assertEqual(unresolved, [])
        self.assertGreater(len(cited), 10)


if __name__ == "__main__":
    unittest.main()

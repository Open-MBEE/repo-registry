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

OPENSYSML = '    name: "OpenSysML"\n    type: tool\n    stage: sandbox'


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


# One deliberately invalid change per table: (file, text to replace, replacement, words the problem names). Each is
# a construction error: the model's rules (data/schema/model.yaml) reject it (WP0 R-14; WP5b D-5).
INVALID = [
    ("data/taxonomy/kinds.yaml", "status: provisional", "status: draft", "status must be"),
    ("data/taxonomy/tiers.yaml", "# PROVISIONAL", "# Draft", "first line"),
    ("registry.yaml", OPENSYSML, OPENSYSML.replace("sandbox", "beta"), "stage: 'beta' is not a stage"),
    ("registry.yaml", OPENSYSML, OPENSYSML + "\n    tier: low", "column 'tier' is not declared"),
    ("registry.yaml", OPENSYSML, OPENSYSML.replace('"OpenSysML"', '"OpenSysML2"'), "renamed?"),
    ("registry.yaml", "    source: maintainer\n    decision:", "    source: maintainer\n    note:",
     "a decision is stated exactly when the source is maintainer"),
    ("data/policies/codeowners.yaml", "\nsetup:", "\nset_up:", "column 'set_up' is not declared"),
    ("data/maintainers.yaml", "  60184290:", "  rkarban:", "user_id: 'rkarban' is not a id"),
    ("data/proposed-codeowners", " @HuiJun", "", "must list exactly the maintainers"),
    ("data/deviations.yaml", "deviations: []",
     "deviations:\n  - {repo_id: 1318945311, name: OpenSysML, policy: license-by-type, reason: test, approved_by: x}",
     "approved_by: 'x' is not a maintainer.login"),
    ("data/pilot-rule.yaml", "{attr: type, eq: tool}", "{attr: type, equals: tool}", "exactly one operator"),
    ("data/pilot-rule.yaml", "{attr: archived, eq: false}", "{attr: nosuch, eq: false}", "which no table stores"),
    ("data/pilot.yaml", "  1318945311:", "  1:", "repo_id: 1 is not a repo"),
    ("data/exclude.yaml", '    name: "apv"\n', '    name: "apv"\n    note: x\n', "column 'note' is not declared"),
    ("data/policies/_future.yaml", "strengthens: [org-two-factor]", "strengthens: [org-three-factor]",
     "'org-three-factor' is not a policy"),
    ("data/forthcoming.yaml", "    closes_in:", "    closes:", "closes_in: missing"),
    ("data/measured-gaps.yaml", "check: review-required", "check: no-such-check", "is not a policy_check"),
    ("data/controls.yaml", "test: tests/", "test: nowhere/", "is not a test"),
]


class ValidTests(unittest.TestCase):
    def test_D1_real_data_is_valid_and_renders(self):
        """D-1, R-1, R-3: the data on this branch meets the declared model, and every view renders, the same twice."""
        self.assertEqual(validate.check(ROOT), [])
        self.assertEqual(validate.renders(ROOT), [])


class InvalidTests(unittest.TestCase):
    def test_R1_each_invalid_file_fails_with_a_named_problem(self):
        """R-1: for each table, a deliberately invalid copy fails, and the problem names what is wrong."""
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
            run = subprocess.run([sys.executable, "scripts/validate.py", "--no-render"], cwd=tmp, capture_output=True,
                                 text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("stage: 'beta' is not a stage", run.stderr)

    def test_R3_broken_view_software_fails(self):
        """R-3 (now WP5b R-5): views aren't stored, so a hand edit can't drift; a render step that breaks fails."""
        with copy_repo() as tmp:
            edit(tmp, "scripts/briefing.py", "def main():", "def main():\n    raise RuntimeError('broken')")
            self.assertEqual(validate.check(pathlib.Path(tmp)), [])
            self.assertTrue(any("briefing.py failed" in p for p in validate.renders(pathlib.Path(tmp))))


def green_non_apache(root):
    """A classified repository whose license is green but not Apache-2.0, so that making it governance (which allows
    only Apache-2.0) turns it red. Chosen from the rendered license view, so the test holds after any kind change."""
    with tempfile.TemporaryDirectory() as t:
        subprocess.run([sys.executable, "scripts/licenses.py", "--out", t, "--root", str(root)], cwd=root, check=True,
                       capture_output=True)
        report = yaml.safe_load((pathlib.Path(t) / "reports/license-report.yaml").read_text())["repos"]
    entries = yaml.safe_load((pathlib.Path(root) / "registry.yaml").read_text())["repos"]
    rid = next(r for r, row in sorted(report.items()) if row["color"] == "green" and row["license"] != "Apache-2.0"
               and "type" in entries.get(r, {}))
    return rid, entries[rid]


def to_governance_sandbox(root, entry):
    edit(root, "registry.yaml", f'    name: "{entry["name"]}"\n    type: {entry["type"]}\n    stage: {entry["stage"]}\n',
         f'    name: "{entry["name"]}"\n    type: governance\n    stage: sandbox\n')


class ComplianceTests(unittest.TestCase):
    def test_R2_out_of_compliance_is_valid(self):
        """R-2: a kind change that leaves a repository red (its license isn't allowed for governance) is valid, as one
        edit: nothing is regenerated, because views aren't stored (WP5b OD4); the rendered view shows it red."""
        with copy_repo() as tmp:
            rid, entry = green_non_apache(tmp)
            to_governance_sandbox(tmp, entry)
            self.assertEqual(validate.check(pathlib.Path(tmp)), [])
            with tempfile.TemporaryDirectory() as t:
                subprocess.run([sys.executable, "scripts/licenses.py", "--out", t, "--root", tmp], cwd=tmp, check=True,
                               capture_output=True)
                report = yaml.safe_load((pathlib.Path(t) / "reports/license-report.yaml").read_text())["repos"]
            self.assertEqual(report[rid]["color"], "red")


class EnvironmentTests(unittest.TestCase):
    def test_R4_environment_is_locked(self):
        """R-4 (WP5 review, G-1): Python 3.10 and PyYAML 6.0.3 are pinned and locked, and CI runs the locked set."""
        pyproject = (ROOT / "pyproject.toml").read_text()
        self.assertIn('requires-python = "==3.10.*"', pyproject)
        self.assertIn('dependencies = ["pyyaml==6.0.3"]', pyproject)
        self.assertRegex((ROOT / ".python-version").read_text().strip(), r"^3\.10\.\d+$")  # patch pinned (WP5c)
        lock = (ROOT / "uv.lock").read_text()
        self.assertRegex(lock, r'name = "pyyaml"\nversion = "6\.0\.3"')
        workflow = (ROOT / ".github/workflows/check.yml").read_text()
        self.assertIn("uv sync --frozen", workflow)
        self.assertGreaterEqual(len(re.findall(r"uv run --frozen python", workflow)), 2)
        self.assertNotIn("pip install", workflow)


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

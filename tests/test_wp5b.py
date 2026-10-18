"""WP5b checks: the declared model, its integrity, and views out of the model. Run with:
python3 -m unittest discover -s tests

Each test names the WP5b requirement or constraint it checks (work-packages/WP5b-scope-of-work.md). The construction
controls in data/controls.yaml name these tests.
"""
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
import audit  # noqa: E402
import model  # noqa: E402
import render  # noqa: E402
import validate  # noqa: E402
from test_wp5 import OPENSYSML, copy_repo, edit  # noqa: E402

DECLARED = model.declared(ROOT)
KIND_NAME = re.compile(r"\b(tool|media|research|governance)/(sandbox|incubating|graduated|archived)\b")


def problems_after(rel, old, new):
    with copy_repo() as tmp:
        edit(tmp, rel, old, new)
        return validate.check(pathlib.Path(tmp))


class ModelTests(unittest.TestCase):
    def test_R1_every_file_has_one_class(self):
        """R-1: every tracked file is a model table, a source, a controller, a test, a view template, configuration, or
        a hand-written document; nothing else, and no rendered view is committed."""
        classes = [
            ("source", r"^data/(snapshots|sources)/"),
            ("model", r"^(registry\.yaml|data/[^/]+\.yaml|data/proposed-codeowners|data/(taxonomy|policies)/.+\.yaml)$"),
            ("schema", r"^data/schema/"),
            ("controller", r"^scripts/.+\.py$"),
            ("test", r"^tests/"),
            ("config", r"^(\.github/|\.gitignore|\.python-version|pyproject\.toml|uv\.lock)"),
            ("document", r"^(README\.md|AGENTS\.md|CLAUDE\.md|docs/.+\.md|work-packages/.+\.md)$"),
        ]
        tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
        unclassified = [f for f in tracked if not any(re.search(p, f) for _, p in classes)]
        self.assertEqual(unclassified, [])
        with tempfile.TemporaryDirectory() as t:
            views = render.render(t, ROOT)
        committed = [v for v in views if v in tracked or f"docs/{v}" in tracked or f"data/{v}" in tracked]
        self.assertEqual(committed, [])

    def test_R2_every_table_has_a_key_and_declared_columns(self):
        """R-2: every table with more than one row has a primary key and columns; every foreign key names a table."""
        tables = DECLARED["tables"]
        for name, t in tables.items():
            with self.subTest(table=name):
                if "one row" not in str(t["rows"]):
                    self.assertTrue(t.get("key"), name)
                for spec in list((t.get("columns") or {}).values()) + list((t.get("foreign") or {}).values()):
                    for target in re.findall(r"fk\(([a-z_]+)", str(spec)) + ([spec] if spec in tables else []):
                        self.assertIn(target, tables, name)
        for name in tables:  # rows() reads every declared table
            model.rows(name, ROOT)

    def test_primary_key_is_unique(self):
        """Constraint: a primary key is unique."""
        row = "  - {repo_id: 1318945311, name: OpenSysML, policy: license-by-type, reason: test, approved_by: mzargham}"
        p = problems_after("data/deviations.yaml", "deviations: []", "deviations:\n" + row + "\n" + row)
        self.assertTrue(any("is not unique" in x for x in p), p)

    def test_foreign_key_resolves(self):
        """Constraint: a foreign key names a row of its table (a broken join is invalid)."""
        p = problems_after("data/pilot.yaml", "  1318945311:", "  1:")
        self.assertTrue(any("repo_id: 1 is not a repo" in x for x in p), p)

    def test_composite_foreign_key_resolves(self):
        """Constraint: type and stage together name a kind (governance/archived is omitted, so it is not a kind)."""
        p = problems_after("registry.yaml", OPENSYSML, OPENSYSML.replace("type: tool", "type: governance")
                           .replace("stage: sandbox", "stage: archived"))
        self.assertTrue(any("('governance', 'archived') is not a kind" in x for x in p), p)

    def test_one_of(self):
        """Constraint: a kind-list entry has type and stage, or a reason alone (WP4e OD2)."""
        p = problems_after("registry.yaml", OPENSYSML, OPENSYSML + '\n    reason: "both"')
        self.assertTrue(any("needs exactly one of type+stage or reason" in x for x in p), p)

    def test_undeclared_column(self):
        """Constraint: a column the model doesn't declare is rejected (the kind name may not be stored, F-02)."""
        p = problems_after("registry.yaml", OPENSYSML, OPENSYSML + "\n    kind: tool/sandbox")
        self.assertTrue(any("column 'kind' is not declared" in x for x in p), p)

    def test_name_agrees_with_the_id(self):
        """Constraint: a repository's name, where a table states it, is its name in the snapshot (detects renames)."""
        p = problems_after("data/pilot.yaml", '    name: "OpenSysML"', '    name: "opensysml"')
        self.assertTrue(any("renamed?" in x for x in p), p)

    def test_disjoint_tables(self):
        """Constraint: a repository is in the pilot or excluded, never both."""
        p = problems_after("data/exclude.yaml", "repos:\n", 'repos:\n  1318945311:\n    name: "OpenSysML"\n')
        self.assertTrue(any("is also in pilot_member" in x for x in p), p)

    def test_coverage(self):
        """Constraint: every repository has a kind-list entry, and is in the pilot or excluded (TX-5)."""
        p = problems_after("registry.yaml", f"  1318945311:\n{OPENSYSML}\n", "")
        self.assertTrue(any("OpenSysML (1318945311) has no entry" in x for x in p), p)

    def test_predicates_read_declared_columns(self):
        """Constraint (F-15): a predicate reads only stored or declared derived columns."""
        p = problems_after("data/pilot-rule.yaml", "{attr: archived, eq: false}", "{attr: kind, eq: tool/sandbox}")
        self.assertTrue(any("reads 'kind'" in x for x in p), p)


class ViewTests(unittest.TestCase):
    def test_R5_views_render_deterministically_and_demo_mode_writes_nowhere_else(self):
        """R-5 (OD4, OD5): every view renders from the model alone, the same twice, only inside the ephemeral
        directory; no render step calls GitHub."""
        self.assertEqual(validate.renders(ROOT), [])
        before = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout
        with tempfile.TemporaryDirectory() as t:
            render.render(t, ROOT)
        after = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout
        self.assertEqual(before, after)
        for step in render.STEPS:
            src = (ROOT / "scripts" / step).read_text()
            self.assertNotRegex(src, r'"gh"|api\.github\.com|requests\.', step)

    def test_R6_no_stored_value_is_derivable(self):
        """R-6: no model table stores the kind name, or a column the model doesn't declare; the pilot stores no kind."""
        for name, t in DECLARED["tables"].items():
            if t["role"] != "model":
                continue
            for r in model.rows(name, ROOT):
                for col, v in r.items():
                    if col in ("meaning", "reason", "decision", "note", "why", "basis", "statement", "known_from",
                               "closes_in", "capability", "evidence_when_closed", "setup", "applies_note"):
                        continue  # prose may mention a kind by its shorthand
                    with self.subTest(table=name, column=col):
                        self.assertIsNone(KIND_NAME.search(yaml.safe_dump(v)), f"{name}.{col}")
        for r in model.rows("pilot_member", ROOT):
            self.assertNotIn("kind", r)

    def test_R3_every_audit_finding_is_fixed(self):
        """R-3, D-2: each audit finding reproduces by its query, and every fixed finding now returns no rows."""
        for fid, find in audit.FINDINGS.items():
            with self.subTest(finding=fid):
                self.assertEqual(find(), [], fid)


if __name__ == "__main__":
    unittest.main()

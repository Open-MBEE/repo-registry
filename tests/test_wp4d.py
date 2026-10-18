"""WP4d checks: the attestations file. Run with: python3 -m unittest discover -s tests

Each test names the WP4d requirement it checks (work-packages/WP4d-scope-of-work.md).
"""
import datetime
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import render  # noqa: E402
SCHEMA = ROOT / "data/schema/attestations.schema.yaml"
FORMAT = ROOT / "docs/attestations-format.md"


def load(path):
    return yaml.safe_load(pathlib.Path(path).read_text())


def problems(value, schema, where="file"):
    """The subset of JSON Schema the attestations schema uses (type, required, properties, additionalProperties,
    items, pattern, minLength, format: date). PyYAML reads an unquoted date as a date; the format allows either."""
    out = []
    t = schema.get("type")
    if t == "object":
        if not isinstance(value, dict):
            return [f"{where}: not a mapping"]
        for key in schema.get("required", []):
            if key not in value:
                out.append(f"{where}: missing {key}")
        props = schema.get("properties", {})
        for key, v in value.items():
            if key in props:
                out += problems(v, props[key], f"{where}.{key}")
            elif schema.get("additionalProperties") is False:
                out.append(f"{where}: unknown key {key}")
    elif t == "array":
        if not isinstance(value, list):
            return [f"{where}: not a list"]
        for i, item in enumerate(value):
            out += problems(item, schema.get("items", {}), f"{where}[{i}]")
    elif t == "string":
        if schema.get("format") == "date":
            if isinstance(value, datetime.date):
                return []
            if not (isinstance(value, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", value)):
                return [f"{where}: not a date"]
            return []
        if not isinstance(value, str):
            return [f"{where}: not a string"]
        if len(value) < schema.get("minLength", 0):
            out.append(f"{where}: empty")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            out.append(f"{where}: doesn't match {schema['pattern']}")
    return out


def attested_checks():
    pairs = {}
    for f in sorted((ROOT / "data/policies").glob("[a-z]*.yaml")):
        p = load(f)
        for c in p["checks"].get("attested") or []:
            pairs[(p["id"], c["id"])] = p["id"]
    return pairs


class FormatTests(unittest.TestCase):
    def test_R1_example_meets_the_schema(self):
        """R-1: one reserved YAML path, a schema, and the format's example meets it; a bad entry fails."""
        schema = load(SCHEMA)
        text = FORMAT.read_text()
        self.assertIn("`ATTESTATIONS.yaml`, at the root", text)
        example = yaml.safe_load(re.search(r"```yaml\n(.*?)```", text, re.S).group(1))
        self.assertEqual(problems(example, schema), [])
        self.assertEqual(set(schema["properties"]["attestations"]["items"]["required"]),
                         {"policy", "check", "attested_by", "date", "release"})
        bad = {"attestations": [{"policy": "security-design", "check": "design-current", "date": "2026-10-18",
                                 "release": "v1.0.0", "attested-by": "x"}]}
        self.assertTrue(any("missing attested_by" in p for p in problems(bad, schema)))
        self.assertTrue(any("unknown key attested-by" in p for p in problems(bad, schema)))

    def test_R2_every_attested_check_can_be_answered(self):
        """R-2: every attested check in data/policies/ appears in its rendered SOP's YAML entry, which meets the schema
        (SOPs are rendered from the policy data since WP5b)."""
        schema = load(SCHEMA)
        with tempfile.TemporaryDirectory() as t:
            render.render(t, ROOT)
            for (pid, cid), _ in attested_checks().items():
                with self.subTest(policy=pid, check=cid):
                    text = (pathlib.Path(t) / "sops" / f"{pid}.md").read_text()
                    blocks = re.findall(r"```yaml\n(.*?)```", text, re.S)
                    self.assertTrue(blocks, pid)
                    entries = yaml.safe_load(blocks[-1].replace("YYYY-MM-DD", "2026-10-18"))["attestations"]
                    self.assertIn((pid, cid), {(e["policy"], e["check"]) for e in entries})
                    self.assertEqual(problems({"attestations": entries}, schema), [])


class DocumentTests(unittest.TestCase):
    def test_R4_no_document_says_attest_in_the_readme(self):
        """R-4: no document tells an operator to attest in the README, except as superseded (amended) history."""
        files = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "README.md",
                                "AGENTS.md", "docs"], cwd=ROOT, capture_output=True, text=True).stdout.split()
        hits = []
        for name in files:
            if not name.endswith(".md"):
                continue
            for n, line in enumerate((ROOT / name).read_text().splitlines(), 1):
                if re.search(r"(?i)attestation block|trailer in its README|repo-registry attestation", line):
                    hits.append(f"{name}:{n}")
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()

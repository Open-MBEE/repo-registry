"""Every relative link in the repository's Markdown resolves (WP4b R-3). Run with: python3 -m unittest discover -s tests
"""
import pathlib
import re
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINK = re.compile(r"\]\(([^)\s]+)\)")


class LinkTests(unittest.TestCase):
    def test_relative_links_resolve(self):
        files = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.md"], cwd=ROOT,
                               capture_output=True, text=True, check=True).stdout.split()
        broken = []
        for name in files:
            path = ROOT / name
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            text = re.sub(r"```.*?```", "", text, flags=re.S)  # links inside code blocks are examples
            text = re.sub(r"`[^`\n]*`", "", text)  # and so are links inside inline code
            for target in LINK.findall(text):
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    continue
                file_part = target.split("#", 1)[0]
                if file_part and not (path.parent / file_part).resolve().exists():
                    broken.append(f"{name}: {target}")
        self.assertEqual(broken, [])


if __name__ == "__main__":
    unittest.main()

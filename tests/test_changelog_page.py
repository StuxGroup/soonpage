"""changelog.html renders CHANGELOG.md in the browser. Its parser runs here under Node.js
(skipped without it) with a stand-in document and fetch."""
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from helpers import ROOT

PAGE = (ROOT / "changelog.html").read_text(encoding="utf-8")
ORDER = ["Added", "Changed", "Fixed", "Removed", "Security", "Deprecated"]
COLOURS = {"added": "#2ecc71", "changed": "#3ba7ff", "fixed": "#ffa64d",
           "removed": "#ff4d4d", "security": "#b06bff", "deprecated": "#8a8a94"}

HARNESS = """
const fs = require('fs');
const [script, mdFile] = process.argv.slice(2);
const target = { innerHTML: '' };
global.document = { getElementById: () => target };
global.fetch = () => Promise.resolve({ ok: true, text: () => Promise.resolve(fs.readFileSync(mdFile, 'utf8')) });
eval(fs.readFileSync(script, 'utf8'));
setTimeout(() => process.stdout.write(target.innerHTML), 50);
"""


def parser_script() -> str:
    for body in re.findall(r"<script>(.*?)</script>", PAGE, re.S):
        if "changelog-body" in body:
            return body
    raise AssertionError("no changelog parser script in changelog.html")


@unittest.skipUnless(shutil.which("node"), "Node.js isn't installed")
class ChangelogPageTest(unittest.TestCase):
    def render(self, markdown: str) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "harness.js").write_text(HARNESS, encoding="utf-8")
            (tmp / "parser.js").write_text(parser_script(), encoding="utf-8")
            (tmp / "CHANGELOG.md").write_text(markdown, encoding="utf-8")
            out = subprocess.run(["node", str(tmp / "harness.js"), str(tmp / "parser.js"), str(tmp / "CHANGELOG.md")],
                                 capture_output=True, text=True, encoding="utf-8", check=True)
            return out.stdout

    def versions(self, rendered: str) -> list:
        return re.findall(r'<h3 class="changelog-version">([^<]*)</h3>', rendered)

    def test_date_version_headings_are_releases(self):
        rendered = self.render("# Changelog\n\nIntro.\n\n## v26.10.23-1\n\n### Fixed\n\n- b\n\n"
                               "## v26.10.23\n\n### Added\n\n- a\n\n## v1.4.4\n\n### Changed\n\n- c\n")
        self.assertEqual(["v26.10.23-1", "v26.10.23", "v1.4.4"], self.versions(rendered))

    def test_sections_are_sorted_into_the_fixed_order(self):
        md = "## v26.10.23\n\n" + "".join(f"### {s}\n\n- {s.lower()} item\n\n" for s in reversed(ORDER)) + "### Notes\n\n- n\n"
        rendered = self.render(md)
        labels = re.findall(r'changelog-label changelog-label-([a-z]+)">', rendered)
        self.assertEqual([s.lower() for s in ORDER], labels)
        self.assertGreater(rendered.index("Notes"), rendered.index("changelog-label-deprecated"), "unknown types go last")

    def test_links_render_and_markup_is_escaped(self):
        rendered = self.render("## v26.10.23\n\n### Added\n\n- [Date Versioning](https://datevers.ing) <b>x</b>\n")
        self.assertIn('<a href="https://datevers.ing">Date Versioning</a>', rendered)
        self.assertIn("&lt;b&gt;x&lt;/b&gt;", rendered)

    def test_the_real_changelog_leads_with_the_current_version(self):
        version = (ROOT / "VERSION.md").read_text(encoding="utf-8").strip()
        rendered = self.render((ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertEqual("v" + version, self.versions(rendered)[0])


class ChangelogBadgeTest(unittest.TestCase):
    def test_order_and_colours(self):
        self.assertIn("var CATEGORIES = " + json.dumps(ORDER).replace('"', "'") + ";", parser_script())
        for name, hex_ in COLOURS.items():
            self.assertRegex(PAGE, r"\.changelog-label-" + name + r"\s*\{\s*--cl:\s*" + hex_ + ";")


if __name__ == "__main__":
    unittest.main()

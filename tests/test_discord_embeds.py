"""The Discord link previews (component embeds) pre-built into each page's <head> by
scripts/build-discord-embeds.py, checked against Discord's rules: one Container at the root,
link buttons using only allowed keys, at most 40 components, and 3,000 bytes at most.
https://docs.discord.com/developers/link-previews/component-embeds"""
import json
import re
import unittest

from helpers import ROOT, html_pages, load_script

embeds = load_script("build-discord-embeds")

OPEN = '<script id="discord:component-embed" type="application/json">'
CLOSE = "</script>"
TAG = re.compile(re.escape(OPEN) + r"(.*?)</script>", re.S)
BUTTON_KEYS = {"id", "type", "url", "style", "label", "emoji", "disabled"}


def flatten(component: dict) -> list:
    """Every component in the tree, the root included."""
    found = [component]
    children = list(component.get("components", [])) + ([component["accessory"]] if "accessory" in component else [])
    for child in children:
        found += flatten(child)
    return found


def headline(payload: dict) -> str:
    """The text of the first section, where every preview puts its title and description."""
    return payload["component"]["components"][0]["components"][0]["content"]


def decode(tag: str) -> dict:
    return json.loads(tag[len(OPEN):-len(CLOSE)])


class DiscordEmbedTest(unittest.TestCase):
    def assert_valid(self, tag: str, label: str = "") -> dict:
        self.assertTrue(tag.startswith(OPEN) and tag.endswith(CLOSE), label + ": preview left out or malformed")
        raw = tag[len(OPEN):-len(CLOSE)]
        self.assertLessEqual(len(raw.encode("utf-8")), 3000, label + ": over 3,000 bytes")
        self.assertNotIn("</", raw, label + ": could close the <script> early")
        payload = json.loads(raw)
        self.assertEqual(["component"], list(payload), label)
        root = payload["component"]
        self.assertEqual(17, root["type"], label + ": the root is one Container")
        self.assertEqual(int(embeds.SITE_COLOUR.lstrip("#"), 16), root["accent_color"], label)
        everything = flatten(root)
        self.assertLessEqual(len(everything), 40, label)
        for c in everything:
            self.assertIn(c["type"], (1, 2, 9, 10, 11, 12, 14, 17), label)
            if c["type"] == 17:
                self.assertIs(root, c, label + ": no nested Containers")
            if c["type"] == 2:
                self.assertEqual(5, c["style"], label + ": link buttons only")
                self.assertLessEqual(set(c), BUTTON_KEYS, label)
                self.assertRegex(c["url"], r"^https?://", label)
        return payload

    def test_every_committed_preview_is_valid_and_current(self):
        sources = {src for _path, src, *_ in embeds.PAGES}
        for path, src, label, *_ in embeds.PAGES:
            page = (ROOT / src).read_text(encoding="utf-8")
            tags = [m.group(0) for m in TAG.finditer(page)]
            self.assertEqual(1, len(tags), src + ": one preview")
            self.assertIn(tags[0], page[:page.index("</head>")], src + ": the preview belongs in <head>")
            payload = self.assert_valid(tags[0], src)
            self.assertEqual(tags[0], embeds.embed_for(path, label, page),
                             src + ": out of date, run python scripts/build-discord-embeds.py")
            if path != "/":
                self.assertIn("## [" + embeds.discord_md(label) + "](" + embeds.BASE_URL + path + ")", headline(payload), src)
        for page in html_pages():
            if page.relative_to(ROOT).as_posix() not in sources:
                self.assertNotIn("discord:component-embed", page.read_text(encoding="utf-8"),
                                 page.name + ": no preview on error pages")

    def test_home_preview_says_what_the_page_is(self):
        page = (ROOT / "index.html").read_text(encoding="utf-8")
        payload = self.assert_valid(embeds.embed_for("/", "Home", page), "home")
        self.assertIn("**Coming soon**", headline(payload))
        labels = [c["label"] for c in flatten(payload["component"]) if c["type"] == 2]
        self.assertTrue(1 <= len(labels) <= 5, labels)

    def test_legal_hub_preview_links_every_legal_page(self):
        page = (ROOT / "legal.html").read_text(encoding="utf-8")
        payload = self.assert_valid(embeds.embed_for("/legal", "Boring Legal Stuff", page), "legal")
        text = json.dumps(payload, ensure_ascii=False)
        for slug in ("privacy", "terms", "cookies", "imprint", "disclaimer", "opt-out"):
            self.assertIn(embeds.BASE_URL + "/legal/" + slug + ")", text)

    def test_markdown_in_data_is_escaped(self):
        # One backslash before each special character, never a literal "$1"
        self.assertEqual(r"\*\*bold\*\* a\_b", embeds.discord_md("**bold** a_b"))
        self.assertEqual(r"\*\*bold\*\* \[x\](y) a\_b \~\~s\~\~ \`c\` \|\|p\|\| \\",
                         embeds.discord_md("**bold** [x](y) a_b ~~s~~ `c` ||p|| \\"))
        self.assertEqual("\\# heading\n\\- list\n\\> quote\nmid # - > stays",
                         embeds.discord_md("# heading\n- list\n> quote\nmid # - > stays"))
        self.assertNotIn("$1", embeds.discord_md("**bold** a_b"))

    def test_escaped_data_reaches_the_preview_intact(self):
        payload = self.assert_valid(embeds.page_embed("A_b *c*", "# not a heading", "https://example.com/x"), "escaped")
        self.assertIn("## [A\\_b \\*c\\*](https://example.com/x)\n\\# not a heading", headline(payload))
        self.assertNotIn("$1", headline(payload))

    def test_script_cant_be_closed_early(self):
        tag = embeds.page_embed("</script><b>x", "d", "https://example.com/x")
        self.assertEqual(1, tag.count(CLOSE), "only the tag's own closing")
        # JSON's <\/ decodes back to </, so Discord still shows the title as written
        self.assertIn("## [</script><b>x](", headline(decode(tag)))

    def test_over_the_limit_falls_back_to_the_page_title_and_description(self):
        tag = embeds.page_embed("T", "Long description. " * 300, "https://example.com/x")
        self.assertTrue(tag.startswith("<!-- discord:component-embed left out"), tag[:80])


if __name__ == "__main__":
    unittest.main()

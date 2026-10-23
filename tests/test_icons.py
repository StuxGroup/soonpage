"""The icon set: favicon.ico, apple-touch-icon.png and site.webmanifest at the site root, and
the same four tags in every page's <head>."""
import json
import re
import struct
import unittest

from helpers import ROOT, html_pages

PNG = b"\x89PNG\r\n\x1a\n"
TAGS = [
    '<link rel="icon" href="/favicon.ico" sizes="48x48">',
    '<link rel="icon" type="image/png" sizes="512x512" href="/assets/img/icon-512.png">',
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
    '<link rel="manifest" href="/site.webmanifest">',
]
ICON_LINK = re.compile(r'<link rel="(?:icon|apple-touch-icon|manifest)"[^>]*>')


def png_info(data: bytes) -> tuple:
    """(width, height, colour type) from a PNG's IHDR; colour types 4 and 6 have alpha."""
    assert data[:8] == PNG, "not a PNG"
    width, height, _depth, colour = struct.unpack(">IIBB", data[16:26])
    return width, height, colour


def site_file(url: str):
    return ROOT / url.lstrip("/")


class IconTest(unittest.TestCase):
    def test_favicon_ico_holds_16_32_and_48px_pngs(self):
        data = (ROOT / "favicon.ico").read_bytes()
        _reserved, kind, count = struct.unpack("<HHH", data[:6])
        self.assertEqual(1, kind)
        sizes = []
        for i in range(count):
            w, h, _c, _r, _p, _b, size, offset = struct.unpack("<BBBBHHII", data[6 + 16 * i:22 + 16 * i])
            self.assertEqual(PNG, data[offset:offset + 8], "%dpx entry is a PNG" % w)
            self.assertEqual((w, h), png_info(data[offset:offset + size])[:2])
            sizes.append(w)
        self.assertEqual([16, 32, 48], sorted(sizes))

    def test_apple_touch_icon_is_180px_and_opaque(self):
        w, h, colour = png_info((ROOT / "apple-touch-icon.png").read_bytes())
        self.assertEqual((180, 180), (w, h))
        self.assertIn(colour, (0, 2), "opaque: iOS fills transparency with black")

    def test_manifest(self):
        manifest = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
        for key in ("name", "short_name", "theme_color", "background_color"):
            self.assertTrue(manifest.get(key), key)
        self.assertEqual("/", manifest["start_url"])
        self.assertEqual("browser", manifest["display"])
        found = {}
        for icon in manifest["icons"]:
            w, h, colour = png_info(site_file(icon["src"]).read_bytes())
            self.assertEqual(icon["sizes"], "%dx%d" % (w, h), icon["src"])
            found[(icon["sizes"], icon.get("purpose", "any"))] = colour
        self.assertIn(("192x192", "any"), found)
        self.assertIn(("512x512", "any"), found)
        self.assertIn(found.get(("512x512", "maskable")), (0, 2), "a 512px maskable icon on an opaque background")

    def test_every_page_lists_the_same_icons(self):
        pages = html_pages()
        self.assertIn(ROOT / "404.html", pages)
        for page in pages:
            text = page.read_text(encoding="utf-8")
            head = text[:text.index("</head>")]
            self.assertEqual(TAGS, ICON_LINK.findall(head), page.relative_to(ROOT).as_posix())
        for url in ("/favicon.ico", "/assets/img/icon-512.png", "/apple-touch-icon.png", "/site.webmanifest"):
            self.assertTrue(site_file(url).is_file(), url)


if __name__ == "__main__":
    unittest.main()

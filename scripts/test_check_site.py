"""Exercise the checker using in-memory changes; never modify site files."""

from pathlib import Path
import unittest
from unittest.mock import patch

from check_site import ROOT, check


class SiteCheckTests(unittest.TestCase):
    def failures_with(self, filename, old, new):
        read_text = Path.read_text

        def edited_read(path, *args, **kwargs):
            source = read_text(path, *args, **kwargs)
            if path == ROOT / filename:
                self.assertIn(old, source)
                return source.replace(old, new)
            return source

        with patch.object(Path, "read_text", edited_read):
            return "\n".join(check()[1])

    def test_current_site(self):
        paths, failures = check()
        self.assertGreaterEqual(len(paths), 4)
        self.assertEqual(failures, [])

    def test_missing_link(self):
        self.assertIn("missing internal destination", self.failures_with(
            "index.html", 'href="/insights.html"', 'href="/missing.html"'))

    def test_missing_anchor(self):
        self.assertIn("missing anchor", self.failures_with(
            "index.html", 'href="#about"', 'href="#missing"'))

    def test_missing_css(self):
        self.assertIn("missing shared stylesheet", self.failures_with(
            "index.html", 'href="styles.css"', 'href="missing.css"'))

    def test_sharing_title(self):
        self.assertIn("og:title differs", self.failures_with(
            "index.html", 'property="og:title" content="Alex Palmer | Sales, GTM and AI"',
            'property="og:title" content="Wrong title"'))

    def test_unfinished_template(self):
        self.assertIn("unreplaced template token", self.failures_with(
            "index.html", "Building better commercial systems with AI.", "{{TITLE}}"))

    def test_bad_redirect(self):
        self.assertIn("legacy index must redirect", self.failures_with(
            "essays.html", "0; url=/insights.html", "0; url=/missing.html"))


if __name__ == "__main__":
    unittest.main()

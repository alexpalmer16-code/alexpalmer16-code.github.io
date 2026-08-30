#!/usr/bin/env python3
"""Dependency-free static checks, not a browser or a full HTML validator."""

from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://alexpalmer16-code.github.io"
FORMATS = {"Analysis", "Playbook", "Experiment", "Prediction"}
PILLARS = {
    "AI-native commercial systems", "Commercial judgment",
    "Leadership and adoption", "Emerging GTM shifts",
}


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.refs = []
        self.ids = []
        self.meta = {}
        self.meta_keys = []
        self.styles = []
        self.canonicals = []
        self.headings = 0
        self.title = ""
        self.in_title = False
        self.lang = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.headings += 1
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "meta":
            key = a.get("name") or a.get("property") or a.get("http-equiv")
            if key:
                self.meta_keys.append(key)
                self.meta[key] = a.get("content", "")
        if tag == "link":
            if "canonical" in a.get("rel", "").split():
                self.canonicals.append(a.get("href", ""))
            if "stylesheet" in a.get("rel", "").split():
                self.styles.append(a.get("href", ""))
        for attr in ("href", "src"):
            if a.get(attr):
                self.refs.append(a[attr])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def check(root=ROOT):
    errors = []
    paths = sorted(p for p in root.rglob("*.html")
                   if not any(part.startswith(("_", "."))
                              for part in p.relative_to(root).parts))
    pages = {p.resolve(): Page(p.read_text(encoding="utf-8")) for p in paths}

    def require(condition, path, message):
        if not condition:
            errors.append(f"{path.relative_to(root)}: {message}")

    def local_target(path, url):
        parsed = urlsplit(url)
        if parsed.netloc and parsed.netloc != urlsplit(ORIGIN).netloc:
            return None, None
        if parsed.scheme and parsed.scheme not in {"https", "http"}:
            return None, None
        urlpath = unquote(parsed.path)
        target = ((root / urlpath.lstrip("/")) if urlpath.startswith("/")
                  else (path.parent / urlpath if urlpath else path))
        if target.is_dir():
            target = target / "index.html"
        return target.resolve(), unquote(parsed.fragment)

    for path, page in pages.items():
        source = path.read_text(encoding="utf-8")
        require(not re.search(r"\{\{[^}]+\}\}", source), path, "unreplaced template token")
        require(page.lang == "en", path, "missing English language declaration")
        require(page.headings == 1, path, "expected exactly one h1")
        require(bool(page.title.strip()), path, "missing title")
        require(bool(page.meta.get("viewport")), path, "missing mobile viewport")
        require(len(page.ids) == len(set(page.ids)), path, "duplicate element id")
        require(len(page.meta_keys) == len(set(page.meta_keys)), path, "duplicate metadata key")
        require(len(page.canonicals) == 1, path, "expected one canonical URL")
        require(any(local_target(path, url)[0] == (root / "styles.css").resolve()
                    for url in page.styles), path, "missing shared stylesheet")

        for url in page.refs:
            target, fragment = local_target(path, url)
            if target is None:
                continue
            require(target.is_relative_to(root.resolve()), path, f"link escapes site: {url}")
            require(target.is_file(), path, f"missing internal destination: {url}")
            if fragment:
                require(target in pages and fragment in pages[target].ids,
                        path, f"missing anchor: {url}")

        relative = path.relative_to(root).as_posix()
        if relative == "essays.html":
            require(page.meta.get("refresh") == "0; url=/insights.html",
                    path, "legacy index must redirect to Insights")
            require(page.canonicals == [ORIGIN + "/insights.html"], path,
                    "legacy index canonical must point to Insights")
            continue

        expected_url = ORIGIN + ("/" if relative == "index.html" else "/" + relative)
        require(page.canonicals == [expected_url], path, "canonical does not match page URL")
        require(page.meta.get("og:url") == expected_url, path, "Open Graph URL mismatch")
        for key in ("description", "og:title", "og:description", "og:type",
                    "og:site_name", "twitter:title", "twitter:description"):
            require(bool(page.meta.get(key)), path, f"missing {key}")
        for prefix in ("og:", "twitter:"):
            require(page.meta.get(prefix + "title") == page.title.strip(), path,
                    f"{prefix}title differs from title")
            require(page.meta.get(prefix + "description") == page.meta.get("description"),
                    path, f"{prefix}description differs from description")
        require(page.meta.get("twitter:card") == "summary", path, "expected summary card")
        if path.parent != root:
            require(page.meta.get("og:type") == "article", path, "expected article metadata")
            require(page.meta.get("article:tag") in FORMATS, path, "invalid article format")
            require(page.meta.get("article:section") in PILLARS, path, "invalid subject")
            try:
                date.fromisoformat(page.meta.get("article:published_time", ""))
            except ValueError:
                require(False, path, "invalid publication date")
        else:
            require(page.meta.get("og:type") == "website", path, "expected website metadata")

    home = pages.get((root / "index.html").resolve())
    require(home is not None, root / "index.html", "missing homepage")
    if home:
        require("https://www.linkedin.com/in/alex-palmer/" in home.refs,
                root / "index.html", "missing Alex's LinkedIn profile link")
    require((root / "insights.html").resolve() in pages,
            root / "insights.html", "missing Insights index")
    return paths, errors


if __name__ == "__main__":
    checked, failures = check()
    if failures:
        print("FAIL\n" + "\n".join(failures))
        sys.exit(1)
    print(f"PASS: {len(checked)} public HTML pages; internal links, anchors, shared CSS and metadata.")
    print("Still required: browser/mobile review, source verification and Alex's publication approval.")

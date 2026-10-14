#!/usr/bin/env python3
"""Static gate for a single-file HTML report. Standard library only.

FAIL lines block delivery; WARN lines are judgment calls to review.
Thresholds are calibrated heuristics, not research constants.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser

SKIP = {"script", "style", "template", "noscript", "title"}
STRUCTURED = {
    "table", "ul", "ol", "dl", "pre", "code", "svg", "figure", "details",
    "button", "label", "select", "meter", "progress", "kbd", "time", "nav",
}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
VISUAL = {"svg", "canvas", "meter", "progress"}
CONTROLS = {"button", "input", "select", "textarea", "details"}
BLOCKS = {"p", "div", "section", "article", "aside", "blockquote", "header",
          "footer", "main", "body", "li", "td", "dd", "figcaption"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "source", "track", "wbr"}
CSS_BAR = re.compile(r"(width|height|inline-size|block-size)\s*:\s*[\d.]+%|--[\w-]+\s*:\s*[\d.]+")
REMOTE = re.compile(r"^\s*(https?:)?//", re.I)
CSS_REMOTE = re.compile(r"(@import|url\()\s*['\"]?\s*(https?:)?//", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")

# ponytail: fixed thresholds; tune here if real reports show false positives.
MIN_TEXT_FOR_SHARE = 1200
MAX_PROSE_SHARE = 0.55
WARN_PROSE_SHARE = 0.40
MAX_BLOCK_FAIL = 100  # words
MAX_BLOCK_WARN = 60  # words
MAX_LEAD = 900
LONG_REPORT = 3000


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.blocks = []  # prose words per open block
        self.prose_blocks = []
        self.visible = self.prose = 0
        self.lead = 0
        self.seen_structure = False
        self.title = self.viewport = self.h1 = False
        self.visuals = self.css_visuals = self.tables = self.controls = 0
        self.remote = []
        self.css = []
        self.missing_alt = 0
        self.emoji_headings = 0
        self.unlabeled_svg = 0
        self.graphics = 0

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "title" and "svg" not in self.stack:
            self.title = True
        if tag == "h1":
            self.h1 = True
        if tag == "meta" and a.get("name", "").lower() == "viewport":
            self.viewport = True
        if tag in VISUAL:
            self.visuals += 1
            self.graphics += 1
        if tag == "svg" and not (a.get("aria-label") or a.get("role") == "img" or a.get("aria-hidden") == "true"):
            self.unlabeled_svg += 1
        if tag == "title" and "svg" in self.stack:
            self.unlabeled_svg = max(0, self.unlabeled_svg - 1)
        if tag == "table":
            self.tables += 1
        if tag in CONTROLS:
            self.controls += 1
        if tag == "img" and "alt" not in a:
            self.missing_alt += 1
        if tag in VISUAL or tag in STRUCTURED:
            self.seen_structure = True
        if CSS_BAR.search(a.get("style", "")):
            self.css_visuals += 1
            self.seen_structure = True
        if a.get("role") == "img" and a.get("aria-label"):
            self.graphics += 1
            self.seen_structure = True
        if a.get("style"):
            self.css.append(a["style"])
        for key in ("src", "href"):
            url = a.get(key, "")
            if url and REMOTE.match(url) and not (tag == "a" and key == "href"):
                self.remote.append(f"<{tag} {key}={url}>")
        if tag in VOID:
            return
        self.stack.append(tag)
        if tag in BLOCKS:
            self.blocks.append(0)

    def handle_endtag(self, tag):
        if tag not in self.stack:
            return
        while self.stack:
            top = self.stack.pop()
            if top in BLOCKS and self.blocks:
                n = self.blocks.pop()
                if n:
                    self.prose_blocks.append(n)
            if top == tag:
                break

    def handle_data(self, data):
        if "style" in self.stack:
            self.css.append(data)
        if any(t in SKIP for t in self.stack):
            return
        n = len(" ".join(data.split()))
        if not n:
            return
        self.visible += n
        if any(t in HEADINGS for t in self.stack) and EMOJI.search(data):
            self.emoji_headings += 1
        if any(t in STRUCTURED or t in HEADINGS for t in self.stack):
            return
        self.prose += n
        if self.blocks:
            self.blocks[-1] += len(data.split())
        if not self.seen_structure:
            self.lead += n


def check(html):
    s = Scan()
    s.feed(html)
    s.close()
    css = "\n".join(s.css)
    if CSS_REMOTE.search(css):
        s.remote.append("CSS @import/url() to a remote host")
    share = s.prose / s.visible if s.visible else 0.0
    longest = max(s.prose_blocks, default=0)
    fails, warns = [], []
    if not s.title:
        fails.append("no <title>")
    if not s.viewport:
        fails.append("no <meta name=viewport>; the page breaks on narrow screens")
    if s.remote:
        fails.append("not self-contained, loads remote resources: " + ", ".join(sorted(set(s.remote))[:5]))
    if not (s.visuals or s.css_visuals or s.tables):
        fails.append("no visual encoding: no chart, gauge, bar, or table")
    if s.visible >= MIN_TEXT_FOR_SHARE and share > MAX_PROSE_SHARE:
        fails.append(f"text dump: prose is {share:.0%} of visible text (max {MAX_PROSE_SHARE:.0%}); move parallel facts into tables, lists, or charts")
    elif s.visible >= MIN_TEXT_FOR_SHARE and share > WARN_PROSE_SHARE:
        warns.append(f"prose is {share:.0%} of visible text; reports that read well stay under {WARN_PROSE_SHARE:.0%}")
    if longest > MAX_BLOCK_FAIL:
        fails.append(f"a prose block has {longest} words (max {MAX_BLOCK_FAIL}); split it or turn it into structure")
    elif longest > MAX_BLOCK_WARN:
        warns.append(f"longest prose block has {longest} words; aim for {MAX_BLOCK_WARN} or fewer")
    if s.lead > MAX_LEAD:
        fails.append(f"{s.lead} characters of prose before the first visual or structured element; lead with the headline and the overview")
    if not s.h1:
        warns.append("no <h1> headline")
    if "prefers-color-scheme" not in css:
        warns.append("no dark mode (prefers-color-scheme)")
    if "@media print" not in css:
        warns.append("no print styles (@media print)")
    if s.visible >= LONG_REPORT and not s.controls:
        warns.append("long report with no filter, toggle, or disclosure; add details-on-demand")
    if not s.graphics and s.css_visuals < 3:
        warns.append("no data graphic (svg, canvas, meter, progress, labeled role=img, or CSS bars); numbers and statuses are only text")
    if s.emoji_headings:
        warns.append(f"{s.emoji_headings} headings use emoji as markers")
    if s.unlabeled_svg:
        warns.append(f"{s.unlabeled_svg} <svg> without aria-label, role=img, or <title>")
    if re.search(r"(animation|transition)\s*:", css) and "prefers-reduced-motion" not in css:
        warns.append("motion without a prefers-reduced-motion override")
    if s.missing_alt:
        warns.append(f"{s.missing_alt} <img> without alt text")
    metrics = {
        "visibleChars": s.visible, "proseShare": round(share, 2),
        "longestProseBlock": longest, "leadProse": s.lead,
        "graphics": s.graphics, "cssBars": s.css_visuals, "tables": s.tables, "controls": s.controls,
    }
    return fails, warns, metrics


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("report")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    with open(args.report, encoding="utf-8") as fh:
        fails, warns, metrics = check(fh.read())
    if args.json:
        print(json.dumps({"fail": fails, "warn": warns, "metrics": metrics}, ensure_ascii=False, indent=2))
    else:
        for line in fails:
            print("FAIL", line)
        for line in warns:
            print("WARN", line)
        print("metrics", json.dumps(metrics))
        print("RESULT", "FAIL" if fails else "PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

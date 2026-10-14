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

# Text in these is not shown or not prose.
HIDDEN = {"script", "style", "template", "noscript", "title"}
# Text in these is structure, not prose; it does not count toward the prose share.
STRUCTURED = {"table", "ul", "ol", "dl", "pre", "code", "svg", "button", "label",
              "select", "meter", "progress", "kbd", "time", "nav", "summary"}
# Text in these is exempt from the paragraph-length check.
VERBATIM = {"pre", "code", "svg"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
GRAPHIC = {"svg", "canvas", "meter", "progress"}
CONTROLS = {"button", "input", "select", "textarea", "details"}
LEAD_BREAK = STRUCTURED | GRAPHIC | {"figure", "details"}
BLOCKS = {"p", "div", "section", "article", "aside", "blockquote", "header", "footer",
          "main", "body", "li", "td", "th", "dd", "dt", "figure", "figcaption", "details"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "source", "track", "wbr"}
# A resource attribute must be inline (data:) or a fragment; anything else is a file or host dependency.
RESOURCE_ATTRS = {"src", "srcset", "poster", "data", "background"}
INLINE = re.compile(r"^\s*(data:|#|$)", re.I)
BAR_STYLE = re.compile(r"(^|;)\s*(width|height|inline-size|block-size)\s*:\s*[\d.]+%|--[\w-]+\s*:\s*[\d.]+")
CSS_DEPENDENCY = re.compile(r"(@import|url\()\s*['\"]?\s*(?!data:|#)[^'\")\s]", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")

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
        self.stack = []  # (tag, info dict)
        self.blocks = []  # words per open block
        self.block_words = []
        self.visible = self.prose = self.lead = 0
        self.seen_structure = False
        self.title = self.viewport = self.h1 = False
        self.graphics = self.bars = self.tables = self.controls = 0
        self.deps = []
        self.css = []
        self.missing_alt = self.emoji_headings = self.unlabeled_svg = 0

    def inside(self, tags):
        return any(t in tags for t, _ in self.stack)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        rendered = not self.inside({"template", "noscript"})
        style = a.get("style", "")
        if style:
            self.css.append(style)
        if tag == "title" and not self.inside({"svg"}):
            self.title = True
        if tag == "meta" and a.get("name", "").lower() == "viewport":
            self.viewport = True
        if tag == "link" and a.get("href") and not INLINE.match(a["href"]):
            rel = a.get("rel", "").lower()
            if any(r in rel for r in ("stylesheet", "icon", "preload", "modulepreload", "manifest")):
                self.deps.append(f"<link rel={rel} href={a['href']}>")
        for key in RESOURCE_ATTRS & a.keys():
            if not INLINE.match(a[key]):
                self.deps.append(f"<{tag} {key}={a[key]}>")
        if rendered:
            if tag == "h1":
                self.h1 = True
            if tag in GRAPHIC or (a.get("role") == "img" and a.get("aria-label")):
                self.graphics += 1
                self.seen_structure = True
            if tag == "table":
                self.tables += 1
            if tag in CONTROLS:
                self.controls += 1
            if tag == "img" and "alt" not in a:
                self.missing_alt += 1
            if tag in LEAD_BREAK:
                self.seen_structure = True
        if tag in VOID:
            return
        info = {
            "bar": rendered and bool(BAR_STYLE.search(style)), "text": False,
            "label": bool(a.get("aria-label") or a.get("role") == "img" or a.get("aria-hidden") == "true"),
            "rendered": rendered,
        }
        if tag == "title" and self.stack and self.stack[-1][0] == "svg":
            self.stack[-1][1]["label"] = True
        self.stack.append((tag, info))
        if tag in BLOCKS:
            self.blocks.append(0)

    def handle_endtag(self, tag):
        if tag not in (t for t, _ in self.stack):
            return
        while self.stack:
            top, info = self.stack.pop()
            if top in BLOCKS and self.blocks:
                n = self.blocks.pop()
                if n:
                    self.block_words.append(n)
            if info["bar"] and not info["text"]:
                # A percentage- or custom-property-sized element with no text inside is a bar.
                self.bars += 1
                self.seen_structure = True
            if top == "svg" and info["rendered"] and not info["label"]:
                self.unlabeled_svg += 1
            if top == tag:
                break

    def handle_data(self, data):
        if self.inside({"style"}):
            self.css.append(data)
        if self.inside(HIDDEN):
            return
        words = data.split()
        n = len(" ".join(words))
        if not n:
            return
        for _, info in self.stack:
            info["text"] = True
        self.visible += n
        if self.inside(HEADINGS):
            if EMOJI.search(data):
                self.emoji_headings += 1
            return
        if self.blocks and not self.inside(VERBATIM):
            self.blocks[-1] += len(words)
        if self.inside(STRUCTURED):
            return
        self.prose += n
        if not self.seen_structure:
            self.lead += n


def check(html):
    s = Scan()
    s.feed(html)
    s.close()
    css = "\n".join(s.css)
    if CSS_DEPENDENCY.search(css):
        s.deps.append("CSS @import or url() to a file or host")
    share = s.prose / s.visible if s.visible else 0.0
    longest = max(s.block_words, default=0)
    fails, warns = [], []
    if not s.title:
        fails.append("no <title>")
    if not s.viewport:
        fails.append("no <meta name=viewport>; the page breaks on narrow screens")
    if s.deps:
        fails.append("not self-contained, depends on files or hosts: " + ", ".join(sorted(set(s.deps))[:5]))
    if not (s.graphics or s.bars or s.tables):
        fails.append("no visual encoding: no chart, gauge, bar, or table")
    if s.visible >= MIN_TEXT_FOR_SHARE and share > MAX_PROSE_SHARE:
        fails.append(f"text dump: prose is {share:.0%} of visible text (max {MAX_PROSE_SHARE:.0%}); move parallel facts into tables, lists, or charts")
    elif s.visible >= MIN_TEXT_FOR_SHARE and share > WARN_PROSE_SHARE:
        warns.append(f"prose is {share:.0%} of visible text; reports that read well stay under {WARN_PROSE_SHARE:.0%}")
    if longest > MAX_BLOCK_FAIL:
        fails.append(f"a text block has {longest} words (max {MAX_BLOCK_FAIL}); split it or turn it into structure")
    elif longest > MAX_BLOCK_WARN:
        warns.append(f"longest text block has {longest} words; aim for {MAX_BLOCK_WARN} or fewer")
    if s.lead > MAX_LEAD:
        fails.append(f"{s.lead} characters of prose before the first visual or structured element; lead with the verdict and the overview")
    if not s.h1:
        warns.append("no <h1> headline")
    if "prefers-color-scheme" not in css:
        warns.append("no dark mode (prefers-color-scheme)")
    if "@media print" not in css:
        warns.append("no print styles (@media print)")
    if s.visible >= LONG_REPORT and not s.controls:
        warns.append("long report with no filter, toggle, or disclosure; add details on demand")
    if not s.graphics and s.bars < 3:
        warns.append("no data graphic (svg, canvas, meter, progress, labeled role=img, or bars); numbers and statuses are only text")
    if s.emoji_headings:
        warns.append(f"{s.emoji_headings} headings use emoji as markers")
    if s.unlabeled_svg:
        warns.append(f"{s.unlabeled_svg} <svg> without aria-label, role=img, or <title>")
    if re.search(r"(animation|transition)\s*:", css) and "prefers-reduced-motion" not in css:
        warns.append("motion without a prefers-reduced-motion override")
    if s.missing_alt:
        warns.append(f"{s.missing_alt} <img> without alt text")
    metrics = {
        "visibleChars": s.visible, "proseShare": round(share, 2), "longestBlockWords": longest,
        "leadProse": s.lead, "graphics": s.graphics, "bars": s.bars, "tables": s.tables, "controls": s.controls,
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

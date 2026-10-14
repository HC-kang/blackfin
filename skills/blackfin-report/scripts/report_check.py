#!/usr/bin/env python3
"""Static gate for a single-file HTML report. Standard library only.

FAIL lines block delivery; WARN lines are judgment calls to review.
Thresholds are calibrated heuristics, not research constants.
Scope: visibility comes from the hidden attribute, aria-hidden, and inline
styles; stylesheet rules are not evaluated, so the render check covers them.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser

# Text in these is never shown as page text.
HIDDEN = {"script", "style", "template", "noscript", "title"}
# Text in these is structure, not prose; it does not count toward the prose share.
STRUCTURED = {"table", "ul", "ol", "dl", "pre", "code", "svg", "button", "label",
              "select", "meter", "progress", "kbd", "time", "nav", "summary"}
# Text in these is exempt from the paragraph-length check.
VERBATIM = {"pre", "code", "svg"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
CONTROLS = {"button", "input", "select", "textarea", "details"}
# Block structure that ends the opening prose; inline code, time, or kbd does not.
LEAD_BREAK = {"table", "ul", "ol", "dl", "pre", "figure", "details", "button", "select",
              "canvas", "meter", "progress"}
BLOCKS = {"p", "div", "section", "article", "aside", "blockquote", "header", "footer",
          "main", "body", "li", "td", "th", "dd", "dt", "figure", "figcaption", "details"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "source", "track", "wbr"}
SVG_SHAPES = {"rect", "circle", "ellipse", "line", "polyline", "polygon", "path", "text", "use", "image"}
# A resource attribute must be inline (data:) or a fragment; anything else is a file or host dependency.
RESOURCE_ATTRS = {"src", "poster", "data", "background"}
# href loads a resource on these tags (SVG image and use, filter images).
HREF_RESOURCE = {"image", "use", "feimage", "script"}
INLINE = re.compile(r"^\s*(data:|#|$)", re.I)
SRCSET_DESCRIPTOR = re.compile(r"^\d+(\.\d+)?[wxh]$")
# A bar is sized by a unitless numeric custom property or by a percentage above 0 and below 100.
BAR_STYLE = re.compile(
    r"(^|;)\s*(width|height|inline-size|block-size)\s*:\s*(?!0+(\.0+)?%)(\d{1,2}(\.\d+)?|0?\.\d+)%"
    r"|--[\w-]+\s*:\s*[\d.]+%?\s*(;|$)")
CSS_COMMENT = re.compile(r"/\*.*?\*/", re.S)
CSS_DEPENDENCY = re.compile(r"url\(\s*['\"]?\s*(?!data:|#)[^'\")\s]|@import\s+['\"](?!data:)", re.I)
JS_COMMENT = re.compile(r"/\*.*?\*/|(^|\s)//[^\n]*", re.S)
JS_IMPORT = re.compile(
    r"(^|[;{}\n])\s*import\s+(?:[^;'\"]*?\bfrom\s*)?['\"](?!data:)([^'\"]+)['\"]"
    r"|\bimport\s*\(\s*['\"](?!data:)([^'\"]+)['\"]\s*\)")
PRINT_MEDIA = re.compile(r"@media[^{]*\bprint\b", re.I)
HIDDEN_STYLE = re.compile(r"display\s*:\s*none|visibility\s*:\s*hidden", re.I)
# ASD-STE100 caps descriptive sentences at 25 words.
SENTENCE_END = re.compile(r"(?<=[.!?。])\s+")
MAX_SENTENCE_WORDS = 25
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")

# ponytail: fixed thresholds; tune here if real reports show false positives.
MIN_TEXT_FOR_SHARE = 1200
MAX_PROSE_SHARE = 0.55
WARN_PROSE_SHARE = 0.40
MAX_BLOCK_FAIL = 100  # words
MAX_BLOCK_WARN = 60  # words
MAX_LEAD = 900
LONG_REPORT = 3000


def srcset_urls(value):
    for token in value.split():
        token = token.strip(",")
        if token and not SRCSET_DESCRIPTOR.match(token):
            yield token


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # (tag, info dict)
        self.blocks = []  # text fragments per open block
        self.block_words = []
        self.visible = self.prose = self.lead = 0
        self.seen_structure = False
        self.title = self.viewport = self.h1 = False
        self.graphics = self.bars = self.tables = self.controls = 0
        self.deps = []
        self.css = []
        self.scripts = []
        self.missing_alt = self.emoji_headings = self.unlabeled_svg = 0
        self.long_sentences = []

    def inside(self, tags):
        return any(t in tags for t, _ in self.stack)

    def close_block(self, shown=True):
        text = " ".join("".join(self.blocks.pop()).split())
        words = len(text.split())
        self.long_sentences += [s for s in SENTENCE_END.split(text) if len(s.split()) > MAX_SENTENCE_WORDS]
        if words:
            self.block_words.append(words)
        if self.blocks and shown:  # text after a shown nested block starts a new word
            self.blocks[-1].append(" ")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        style = a.get("style", "")
        rendered = not self.inside({"template", "noscript"})
        parent_shown = not self.stack or self.stack[-1][1]["shown"]
        shown = (rendered and parent_shown and "hidden" not in a and a.get("aria-hidden") != "true"
                 and not HIDDEN_STYLE.search(style))
        if style:
            self.css.append(style)
        if tag == "title" and rendered and not self.inside({"svg"}):
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
        for url in srcset_urls(a.get("srcset", "")):
            if not INLINE.match(url):
                self.deps.append(f"<{tag} srcset={url}>")
        if tag in HREF_RESOURCE:
            for key in ("href", "xlink:href"):
                if a.get(key) and not INLINE.match(a[key]):
                    self.deps.append(f"<{tag} {key}={a[key]}>")
        if shown:
            if tag == "h1":
                self.h1 = True
            if tag in {"canvas", "meter", "progress"} or (tag != "svg" and a.get("role") == "img" and a.get("aria-label")):
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
            if tag in SVG_SHAPES:
                for t, info in reversed(self.stack):
                    if t == "svg":
                        info["shapes"] = True
                        break
        if tag == "br" and shown and self.blocks:
            self.blocks[-1].append(" ")
        if tag in VOID:
            return
        info = {"bar": shown and bool(BAR_STYLE.search(style)), "text": False, "shapes": False,
                "label": bool(a.get("aria-label") or a.get("role") == "img"), "shown": shown}
        if tag == "title" and self.stack and self.stack[-1][0] == "svg":
            self.stack[-1][1]["label"] = True
        self.stack.append((tag, info))
        if tag in BLOCKS:
            self.blocks.append([])

    def handle_endtag(self, tag):
        if tag not in (t for t, _ in self.stack):
            return
        while self.stack:
            top, info = self.stack.pop()
            if top in BLOCKS and self.blocks:
                self.close_block(info["shown"])
            if info["bar"] and not info["text"]:
                # A sized element with no text inside is a bar.
                self.bars += 1
                self.seen_structure = True
            if top == "svg" and info["shown"]:
                # A labeled svg with shapes is a data graphic; anything else is decoration or an accessibility gap.
                if info["label"] and info["shapes"]:
                    self.graphics += 1
                    self.seen_structure = True
                elif not info["label"]:
                    self.unlabeled_svg += 1
            if top == tag:
                break

    def handle_data(self, data):
        if self.inside({"style"}):
            self.css.append(data)
        if self.inside({"script"}):
            self.scripts.append(data)
        if self.inside(HIDDEN) or (self.stack and not self.stack[-1][1]["shown"]):
            return
        n = len(" ".join(data.split()))
        if self.blocks and not self.inside(VERBATIM | HEADINGS):
            self.blocks[-1].append(data)
        if not n:
            return
        for _, info in self.stack:
            info["text"] = True
        self.visible += n
        if self.inside(HEADINGS):
            if EMOJI.search(data):
                self.emoji_headings += 1
            return
        if self.inside(STRUCTURED):
            return
        self.prose += n
        if not self.seen_structure:
            self.lead += n

    def finish(self):
        self.close()
        while self.blocks:  # blocks left open at the end of the file, such as an unclosed <p>
            self.close_block()


def check(html):
    s = Scan()
    s.feed(html)
    s.finish()
    css = CSS_COMMENT.sub("", "\n".join(s.css))
    if CSS_DEPENDENCY.search(css):
        s.deps.append("CSS @import or url() to a file or host")
    for m in JS_IMPORT.finditer(JS_COMMENT.sub(" ", "\n".join(s.scripts))):
        s.deps.append(f"script import {m.group(2) or m.group(3)}")
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
    if not PRINT_MEDIA.search(css):
        warns.append("no print styles (@media print)")
    if s.visible >= LONG_REPORT and not s.controls:
        warns.append("long report with no filter, toggle, or disclosure; add details on demand")
    if not s.graphics and s.bars < 3:
        warns.append("no data graphic (labeled svg, canvas, meter, progress, labeled role=img, or bars); numbers and statuses are only text")
    if s.emoji_headings:
        warns.append(f"{s.emoji_headings} headings use emoji as markers")
    if s.unlabeled_svg:
        warns.append(f"{s.unlabeled_svg} <svg> without aria-label, role=img, or <title>")
    if re.search(r"(animation|transition)\s*:", css) and "prefers-reduced-motion" not in css:
        warns.append("motion without a prefers-reduced-motion override")
    if s.long_sentences:
        warns.append(f"{len(s.long_sentences)} sentences exceed {MAX_SENTENCE_WORDS} words (ASD-STE100); split them, first: {s.long_sentences[0][:80]}")
    if s.missing_alt:
        warns.append(f"{s.missing_alt} <img> without alt text")
    metrics = {
        "visibleChars": s.visible, "proseShare": round(share, 2), "longestBlockWords": longest,
        "leadProse": s.lead, "longSentences": len(s.long_sentences), "graphics": s.graphics, "bars": s.bars, "tables": s.tables, "controls": s.controls,
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

---
name: blackfin-report
description: Turn finished work into a self-contained HTML report a developer can scan, filter, and act on. Use when the user asks for an HTML or visual report, or when a result is too large to scan in chat (many items, compared metrics, several decisions); not for short answers.
---

# Blackfin / Report

A report earns its place only when it answers the reader's questions faster than chat. Before writing markup, list those questions: what needs me, did it work, what changed, how sure are we, what comes next. Chat still carries the headline and the open decisions in three lines; the page carries the rest.

## The page, in this order

1. Verdict: a status word with an icon, one sentence that states the outcome, and a unit bar or count of the items behind it. All of it fits on the first screen.
2. Needs you: each open decision with its options and the consequence of each, as controls that compose a reply line the user can copy. If nothing is open, say so in one line.
3. Overview: the three to six numbers that matter, each beside its comparison (before → after, done of total, target).
4. Detail: the items as a table the reader can filter by status and sort, or as small multiples; anything over about eight rows gets filter chips.
5. Evidence and gaps: each command with its observed output inside a disclosure whose summary shows the result; what was not verified stays visible.

## Encoding

Choose the visual from the shape of the data, using [the visual grammar](references/visual-grammar.md). Position and length beat angle, area, and color, so prefer bars, dots, and aligned tables. Every chart answers a question named in its heading. Status always pairs color with an icon and a word.

Prose holds only what structure cannot: a reason, a trade-off, a caveat. A paragraph is at most three sentences; a sentence that lists three or more parallel things becomes a list or a table.

Most readers scroll and never click, so the static page carries the verdict, the decisions, and the gaps. Interaction answers a further question: filter, sort, compare, reveal evidence, or decide. A verdict, blocker, decision, or unverified claim never sits behind hover, a closed disclosure, or a non-default tab.

Models fall back on a few default looks. The grammar names them (paragraph cards, gradients, emoji markers, pill buttons, monospace labels, and more); leave them out by name, because asking for a page that does not look generic only swaps one default for another.

## Build, check, deliver

- Start from [the template](assets/report-template.html): it carries tokens, dark mode, print styles, status chips, unit bars, comparison bars, a sortable and filterable table, a decision picker, and a timeline. Replace its content; keep its structure unless the data needs another shape.
- One file, inline CSS, JavaScript, and SVG, no network: it must render offline and print legibly. Numbers come from observed output, and unverified values say so.
- Run `python3 <skill-directory>/scripts/report_check.py <report.html>` and fix every FAIL. Then look at the rendered page: under Orca, open it in the built-in browser (`orca tab create --url file://<absolute-path>`) and take a screenshot; elsewhere, use a headless browser screenshot. Confirm the render checklist at the end of the grammar and fix what fails; your own impression of the page is not the check.
- Save it under `.blackfin/reports/<yyyy-mm-dd>-<slug>.html` unless the user names a place, and keep that directory out of commits (`.git/info/exclude`). Open it for the user and give the path; under Orca, also put the path in the worktree note. Publish a public link only when the user asks.

Example: a dependency audit of 30 packages becomes a verdict line with a 30-unit bar, one decision picker for the risky major upgrade, severity counts as bars, a filterable package table, and the audit commands behind disclosures.

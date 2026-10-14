# Visual grammar

Read this when choosing how to show a piece of data, when adding interaction, or before the render check.

## Data shape to encoding

Position on a common scale beats length, and both beat angle, area, and color (Cleveland & McGill; Heer & Bostock 2010). Draw to scale and label values directly.

| Shape of the data | Encoding | HTML, CSS, or SVG |
| --- | --- | --- |
| Status of N items | Unit bar for the count; table sorted by severity with status chips | `.units`; `<table>` with `.st` chips (icon, word, color) |
| One number that matters | Value beside its comparison | `.kpi` with two `.track` bars, or done of total |
| Trend over time | Sparkline with labeled end, min, and max; a line chart for many points | inline `<svg>` `<polyline>` with `role="img"` and `aria-label` |
| Part of a whole | One 100% stacked bar with direct labels | flex children with `width:%` |
| Compare categories | Sorted horizontal bars with values | `.bars` rows, or bars inside table cells |
| Distribution | Strip plot or histogram; a value list for a few samples | SVG `circle` or `rect` |
| Sequence or flow | Ordered list with step status; nodes and arrows only for branches | `<ol class="timeline">`, SVG for branches |
| Before and after | Before, after, delta table; slope chart; diff block for code | `<table>`, two-point SVG lines, `<pre>` with `<del>` and `<ins>` |
| Hierarchy | Collapsible tree; a treemap only when size matters | nested `<details>` |
| Many attributes per item | Table with sticky header; small multiples of one chart | `th { position: sticky }`, CSS grid |
| Reasoning behind a result | One visible summary line, the rest folded | `<details>` |

## Interaction

Most readers scroll and do not click, so the static page must already carry the verdict, the decisions, and the gaps (Tse, NYT 2016; Aisch 2017). Interaction serves a reader who wants more:

- Filter and sort a list longer than about eight rows.
- Toggle a comparison, such as before and after.
- Reveal evidence such as command output, at most two disclosure levels deep.
- Decide: an option picker that composes a reply line to copy back to the agent.

Never hide a verdict, a blocker, a decision, or an unverified claim behind a tooltip, hover, closed disclosure, or non-default tab. Every control works with a keyboard.

## Leave out

These are model default styles, so name them rather than asking for a page that does not look generic (Opus 5.5 guide; OpenAI frontend guidance; Anthropic design guidance):

- Paragraphs poured into HTML, paragraph-only cards, nested cards, identical rounded cards with one soft shadow.
- Purple or indigo-to-blue gradients, gradient text, glow blobs, glass blur; cream backgrounds with serif display type and terracotta accents.
- Emoji section markers, "01 / 02 / 03" labels on content that has no order, all-caps eyebrows above every heading, one italic or colored accent word in a heading.
- Monospace used for labels instead of code, "A · B · C" metadata strings, pill-shaped buttons, everything centered.
- Fade-and-slide entrances, count-up numbers, pie, donut, gauge, or 3D charts for precise comparison, status dots that use color alone.
- Big-number tiles when the numbers are not the point, invented figures, promotional wording.

## Accessibility and robustness

- Semantic elements: `table` with `th`, `ol`, `dl`, `details`, `button`.
- Contrast of at least 4.5:1 for text and 3:1 for graphics in both color schemes (WCAG 2.2: 1.4.3, 1.4.11). Status never relies on color alone (1.4.1).
- `prefers-color-scheme`, `prefers-reduced-motion`, visible focus, `@media print` that opens disclosures and hides controls.
- Running text stays near 65 to 75 characters wide.
- Status hues come from the Okabe-Ito set, which stays distinct under common color-vision deficiencies.
- The page reads without JavaScript; scripts only add sorting, filtering, and copying.

## Render check

Models detect visualization problems less reliably than they fix them, so the script detects and the rendered page confirms (arXiv 2602.20084; VisJudge-Bench). Look at the screenshot and confirm each item:

1. The first screen shows the verdict, the item count or unit bar, and the open decisions.
2. Every number on the page matches its observed source, and each chart is drawn to scale.
3. Nothing in "Leave out" appears, and no important item is hidden.
4. At a 390-pixel width nothing overflows sideways except tables inside their scroll container.
5. Dark mode keeps every status and chart readable.

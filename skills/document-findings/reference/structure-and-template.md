# Findings Doc Structure and Template

Backs the `<findings-doc-structure>` knowledge entry; used by **author-findings-doc**. A findings doc keeps a fixed section order so readers and agents navigate by position.

## Section order

| # | Section | Purpose |
|---|---|---|
| — | Metadata block | Machine-readable header (area, spike, scope, status, related areas) |
| 1 | Orientation | Resource index: component → purpose → entry point → key files |
| 2..N | Topic blocks | One per question — TL;DR, diagram/table, claims with `file:line` |
| N+1 | Evidence & Verification | Consolidated ledger, searched-negatives, coverage |

## Template

````markdown
<!-- findings-doc
area: <area-slug>
spike: <spike-name>
status: investigating | complete
scope: <one line>
related-areas: [<area-slug>]
-->

# Findings: <Area name>

## 1. Orientation

| Component | Purpose | Entry point | Key files |
|---|---|---|---|

## 2. <Question?> <!-- id: <area>/<topic-slug> -->
**TL;DR:** <one-line answer>

<diagram(s) — or a comparison table, or short prose>

**Claims**
- <atomic fact> — `<path:line>` ✅ Verified

## N. Evidence & Verification

| Claim ID | Claim | Verdict | Evidence (file:line) | Confidence |
|---|---|---|---|---|

### Searched-negatives

| Search (pattern/query) | Result | Next step |
|---|---|---|

### Coverage

| In-scope question | Investigated | Not investigated / Gaps |
|---|---|---|
````

## Rendering rules
- Number topics from 2; Evidence & Verification is last with the next number.
- Every topic block: question heading, TL;DR, a primary artifact (diagram / table / prose), claim bullets.
- Diagram-first: a flow, structure, or branch is a diagram; a comparison is a table (rows = items) per **reference/table-guidelines.md**.
- Multiple diagrams per topic are allowed.
- Use tables for structured facts and fenced Mermaid for diagrams.
- Keep the metadata block first and the section order fixed across every area.
- One doc per area; the filename `findings-<area-slug>.md` matches the metadata `area` and the ID prefix.

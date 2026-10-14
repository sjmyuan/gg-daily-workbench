# Human Findings Doc Structure and Template

Used by **author-findings-doc**. The human doc keeps a fixed section order and is self-contained — claims and coverage live in `evidence-<area>.md`, with no link to it.

## Section order

| # | Section | Purpose |
|---|---|---|
| — | YAML frontmatter | Publication metadata (title, area, status) |
| — | Summary | 2–4 sentence human intro under the title |
| 1 | Orientation | Resource index with a "Start here" pointer |
| 2 | Glossary (optional) | Domain terms defined once |
| 3..N | Topic blocks | One per question — TL;DR, diagram/table, short prose |

## Template

````markdown
---
title: Findings: <Area name>
area: <area-slug>
status: investigating | complete
---

# Findings: <Area name>

**Summary:** <2–4 sentences: what this area is, its boundary, why it matters.>

## 1. Orientation

| Component | Purpose | Entry point | Key files |
|---|---|---|---|
| | | | |

Start here: <the file:line to read first>.

## 2. Glossary

| Term | Meaning |
|---|---|

## 3. <Question?>
**TL;DR:** <one-line answer>

> <optional one-line framing: scope or assumption the artifact relies on>

<diagram(s) — or a comparison table, or short prose>

... one block per question; end after the last topic — no evidence section ...
````

## Rendering rules
- Open with YAML frontmatter and a `**Summary:**` (2–4 sentences); number topics from 3.
- Every topic block: question heading, TL;DR, a primary artifact (diagram / table / prose).
- Diagram-first: a flow, structure, or branch is a diagram.
- A comparison is a table (rows = items) per **reference/table-guidelines.md**.
- Multiple diagrams per topic are allowed.
- Annotate diagram elements with `file:line` so a reader can jump to code.
- Cite code as `<reference> (file:line)`: `Class#member` for members, `module.function` for free functions.
- Glossary is optional; include it when a term repeats, else define terms on first mention.
- Never place claim IDs, confidence tags, the claim ledger, or a link to `evidence-<area>.md` in the human doc.
- End after the last topic block; keep the section order fixed across every area.
- One human doc per area; the filename `findings-<area-slug>.md` matches the metadata `area` and the ID prefix.

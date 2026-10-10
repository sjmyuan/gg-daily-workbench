# Findings Doc Structure and Template

Used by **author-findings-doc**. A findings doc keeps a fixed section order so readers and agents navigate by position.

## Section order

| # | Section | Purpose |
|---|---|---|
| — | Metadata block | Machine-readable header (area, spike, scope, status, related areas) |
| — | Summary | 2–4 sentence human intro under the title |
| 1 | Orientation | Resource index with a "Start here" pointer |
| 2 | Glossary (optional) | Domain terms defined once |
| 3..N | Topic blocks | One per question — TL;DR, diagram/table, claims with `file:line` |
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

**Summary:** <2–4 sentences: what this area is, its boundary, why it matters.>

## 1. Orientation

| Component | Purpose | Entry point | Key files |
|---|---|---|---|

Start here: <the file:line to read first>.

## 2. Glossary

| Term | Meaning |
|---|---|

## 3. <Question?> <!-- id: <area>/<topic-slug> -->
**TL;DR:** <one-line answer>

> <optional one-line framing: scope or assumption the artifact relies on>

<diagram(s) — or a comparison table, or short prose>

**Claims**
- <atomic fact> — `<reference> (file:line)` ✅ Verified

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
- Open with the metadata block and a `**Summary:**` (2–4 sentences); number topics from 3.
- Every topic block: question heading, TL;DR, a primary artifact (diagram / table / prose), claim bullets.
- Diagram-first: a flow, structure, or branch is a diagram.
- A comparison is a table (rows = items) per **reference/table-guidelines.md**.
- Multiple diagrams per topic are allowed.
- Annotate diagram elements with `file:line`.
- Cite code as `<reference> (file:line)` on first mention.
- Use `Class#member` for class members and `module.function` for free functions — e.g. `ChargeService#authorize (ChargeService.java:88)`, `charge.authorize (charge.py:88)`.
- Glossary is optional; include it when a term repeats, else define terms on first mention.
- End with Evidence & Verification; keep the section order fixed across every area.
- One doc per area; the filename `findings-<area-slug>.md` matches the metadata `area` and the ID prefix.

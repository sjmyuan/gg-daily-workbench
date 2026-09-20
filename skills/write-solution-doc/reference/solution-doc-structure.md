# Solution Document Structure

Backs the `<solution-doc-structure>` knowledge entry and the **structure-solution-doc** capability. A complete solution document has 9 sections, produced in order.

## Canonical sections and titles

Use these exact titles. Sub-sections are numbered `N.M` when a section has multiple items; single-table sections take no sub-number.

| # | Section title | Sub-sections |
|---|---|---|
| 1 | Business Context & Solution Background | — |
| 2 | System Topology (C4 Model) | 2.1 C2 — Container Diagram; 2.2 C3 — Component Diagram |
| 3 | Interaction Details | 3.1, 3.2, … one per critical flow |
| 4 | API / Event Schema | 4.1, 4.2, … one per API or event |
| 5 | Related Documents | — |
| 6 | External Dependencies | — |
| 7 | Maintainers | — |
| 8 | RAID Analysis | 8.1 Risks; 8.2 Assumptions; 8.3 Issues; 8.4 Dependencies |
| 9 | RACI Matrix | — |

Current-state documents keep the same numbering but substitute §8 → **Constraints & Pain Points** and §9 → **Raw Data & Metrics** (see **current-state-mode.md**).

## Markdown Template

Every `##` section opens with a `**Takeaway:**` line (≤15 words). Every diagram/table caption is its own one-line takeaway.

````markdown
# Solution Document: [Solution Name]

## 1. Business Context & Solution Background
**Takeaway:** [problem + why this solution]

[ ≤3 sentences: context and decision rationale ]

## 2. System Topology (C4 Model)
**Takeaway:** [the system's shape in one line]
### 2.1 C2 — Container Diagram
[Mermaid `C4Container` — caption is the takeaway]
### 2.2 C3 — Component Diagram
[Mermaid `C4Component` — caption is the takeaway]

## 3. Interaction Details
**Takeaway:** [the interaction picture in one line]
### 3.1 [Flow name]
[Mermaid sequence/flowchart — caption is the takeaway]

## 4. API / Event Schema
**Takeaway:** [contract surface in one line]
### 4.1 [Endpoint / topic]
[Contract table + schema code block — no prose walkthrough]

## 5. Related Documents
**Takeaway:** [reference set in one line]
[Table]

## 6. External Dependencies
**Takeaway:** [dependency risk in one line]
[Table with owning teams, contacts, SLA, fallback]

## 7. Maintainers
**Takeaway:** [ownership picture in one line]
[Table with maintainer teams and contacts]

## 8. RAID Analysis
**Takeaway:** [top risk in one line]
### 8.1 Risks
[Table]
### 8.2 Assumptions
[Table]
### 8.3 Issues
[Table]
### 8.4 Dependencies
[Table]

## 9. RACI Matrix
**Takeaway:** [accountability picture in one line]
[Matrix table — one A per row]
````

## Rendering Rules (apply concise-writing)

- Every `##` section opens with a bolded one-line takeaway (≤15 words).
- Number sub-sections `N.M`; never invent alternate titles or numbering.
- Use tables for structured data and fenced code blocks for Mermaid/JSON/YAML. Never restate what a table or diagram shows.
- For any section explicitly skipped, mark it as `[Skipped]`.
- Ensure all Mermaid diagrams use correct syntax and are renderable.

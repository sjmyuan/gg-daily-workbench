# Findings Doc Pair Quality Checklist

Loaded by **validate-findings-doc**. Report each failed item by severity.

## Human doc
- [ ] YAML frontmatter present (title, area, status).
- [ ] A `**Summary:**` (2–4 sentences) follows the title.
- [ ] Section order: Summary → Orientation → Glossary → topic blocks.
- [ ] Orientation has a "Start here" pointer.
- [ ] Repeated domain terms are in the Glossary; others are defined on first mention.
- [ ] A flow, structure, or branch topic uses a **diagram**, not a table.
- [ ] A cross-flow comparison uses a **comparison table** (rows = items) with an `Evidence` column.
- [ ] Diagrams label every element and annotate key elements with `file:line`.
- [ ] Failure/edge behavior is covered where it changes the answer.
- [ ] Tables follow **reference/table-guidelines.md**.
- [ ] Every topic is a single reader question, ordered orientation → depth.
- [ ] Every topic has a `**TL;DR:**` line (≤15 words) and renders its diagram/table.
- [ ] Every Mermaid diagram passes `draw-mermaid-diagrams` validation (0 errors).
- [ ] No claim IDs, confidence tags, claim ledger, or reference to the evidence doc appear in the human doc.
- [ ] Conciseness: sentences ≤20 words; no banned phrases; no table or diagram restated in prose.

## Evidence doc
- [ ] Metadata block present and first (area, spike, scope, status, related-areas, human-doc).
- [ ] Section order: Topic map → Claim ledger → Searched-negatives → Coverage → Cross-area references.
- [ ] Topic map covers every human-doc heading and links its anchor.
- [ ] Every human-doc topic claim is one ledger row.
- [ ] Every claim has a confidence tag; no 🔶 Inferred or 💭 Assumption presented as ✅ Verified.
- [ ] Every ✅ Verified or 🔶 Inferred claim cites an inline `file:line`.
- [ ] Searched-negatives and Coverage tables are present and honest.
- [ ] Topic and claim IDs use the `<area>/<topic-slug>#cN` scheme; unique and unrenumbered.

## Cross-consistency & scope
- [ ] Every human-doc topic claim appears in the ledger (no orphans).
- [ ] Every ledger row links back to a human topic.
- [ ] Citation format is valid for downstream docs.
- [ ] Current-state only — no target-state or decision content, no version markers or changelogs.

## Severity
- 🚫 Blocker: a required section is missing, or any ✅/🔶 claim lacks `file:line`.
- 🔴 Major: a ledger claim missing from the human doc, an ID renumbered, or target-state content leaked.
- 🟡 Minor: missing searched-negatives/coverage, or a non-rendering diagram.
- 🟢 Nit: wording or ordering polish.

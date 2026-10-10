# Findings Doc Quality Checklist

Loaded by **validate-findings-doc**. Report each failed item by severity.

## Structure
- [ ] Metadata block present and first (area, spike, scope, status, related areas).
- [ ] A `**Summary:**` (2–4 sentences) follows the title.
- [ ] Section order: Summary → Orientation → Glossary → topic blocks → Evidence & Verification.
- [ ] One doc per area; filename matches the area slug.

## Orientation & terms
- [ ] Orientation has a "Start here" pointer.
- [ ] Repeated domain terms are in the Glossary; others are defined on first mention.

## Representation
- [ ] A flow, structure, or branch topic uses a **diagram**, not a table.
- [ ] A cross-flow comparison uses a **comparison table** (rows = items) with `Evidence` and `Confidence` columns.
- [ ] Multiple diagrams are used when each flow's shape matters.
- [ ] Diagrams label every element, annotate key elements with `Symbol (file:line)`, and use no unexplained abbreviations.
- [ ] Claims cite `Symbol#method (file:line)`.
- [ ] Failure/edge behavior is covered where it changes the answer.
- [ ] Tables follow **reference/table-guidelines.md**: self-describing headers, units, defined terms, no ambiguous cells, required columns present.

## Topics
- [ ] Every topic is a single reader question, ordered orientation → depth.
- [ ] Every topic has a `**TL;DR:**` line (≤15 words).
- [ ] Every diagram or table renders.
- [ ] Claim bullets are atomic, with no reasoning.

## Claims & evidence
- [ ] Every claim bullet has an inline `file:line` and a confidence tag.
- [ ] No 🔶 Inferred or 💭 Assumption presented as ✅ Verified.
- [ ] Every topic-block claim appears in the ledger.
- [ ] Searched-negatives and Coverage tables are present and honest.

## IDs
- [ ] Topic and claim IDs use the `<area>/<topic-slug>#cN` scheme.
- [ ] IDs are unique and no existing ID was renumbered.
- [ ] Citation format is valid for downstream docs.

## Scope
- [ ] Current-state only — no target-state or decision content.
- [ ] No version markers or changelogs.

## Conciseness
- [ ] Sentences ≤20 words; no banned phrases.
- [ ] No table or diagram restated in prose.

## Severity
- 🚫 Blocker: a required section is missing, or any claim lacks `file:line`.
- 🔴 Major: ledger missing claims, an ID renumbered, or target-state content leaked.
- 🟡 Minor: missing searched-negatives/coverage, or a non-rendering diagram.
- 🟢 Nit: wording or ordering polish.

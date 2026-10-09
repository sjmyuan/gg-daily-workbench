# Findings Doc Quality Checklist

Loaded by **validate-findings-doc**. Report each failed item by severity.

## Structure
- [ ] Metadata block present and first (area, spike, scope, status, related areas).
- [ ] Section order: Orientation → topic blocks → Evidence & Verification.
- [ ] One doc per area; filename matches the area slug.

## Topics
- [ ] Every topic is a single reader question, ordered orientation → depth.
- [ ] Every topic has a `**TL;DR:**` line (≤15 words).
- [ ] At most one diagram or table per topic; it renders.
- [ ] Claim bullets are atomic, with no reasoning.

## Evidence
- [ ] Every claim has an inline `file:line` and a confidence tag.
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

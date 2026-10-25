---
name: document-findings
description: Produce a per-area findings doc pair: a publishable human doc and a machine evidence doc of file:line claims. Use when documenting, writing, compiling, splitting, explaining, updating, or verifying findings.
---

<when-to-use-this-skill>
- Document the current state of a code area as a doc pair
- Write the human-readable findings doc for publication
- Compile the evidence doc with claim IDs, verdicts, and confidence
- Explain existing code through diagrams, tables, and question-style answers
- Update a doc pair when new evidence changes what is known
- Verify a doc pair for cross-consistency and evidence coverage
- Split a combined findings doc into a human doc and an evidence doc
</when-to-use-this-skill>

<knowledge>
<findings-doc-pair-definition>
A findings doc pair explains what exists in a code **area** today: a human findings doc for readers and an evidence doc for machine consumption. Current-state only — never target-state or decisions.
</findings-doc-pair-definition>
<doc-pair-model>
| Content | Human `findings-<area>.md` | Evidence `evidence-<area>.md` |
|---|---|---|
| Metadata | YAML frontmatter: title, area, status | Machine block: area, spike, scope, related-areas, human doc |
| Summary, Orientation, Glossary, topic blocks | Yes | — |
| `file:line` anchors | Inline, for checking | In the ledger |
| Atomic claims, IDs, verdicts, confidence | — | Yes |
| Topic→claim map, searched-negatives, coverage | — | Yes |
</doc-pair-model>
<human-doc-structure>
- Fixed order: YAML frontmatter → title → Summary → Orientation → Glossary (optional) → topic blocks.
- Self-contained: no claim IDs, confidence tags, ledger, or evidence-doc link — it publishes anywhere.
- Template: **reference/structure-and-template.md**.
</human-doc-structure>
<topic-block-format>
- Each topic answers one reader question: TL;DR → primary artifact → short prose.
- Pick the representation diagram-first per **reference/topic-block-guide.md**.
- Draw diagrams via `draw-mermaid-diagrams`; this skill owns the `file:line` annotations and topic framing.
</topic-block-format>
<evidence-doc>
- The machine layer: metadata block, topic→claim map, ledger, searched-negatives, coverage, cross-area references.
- Ledger row: claim ID → claim → verdict → evidence `file:line` → confidence.
- IDs are scope slugs (`<area>/<topic-slug>#cN`), area-scoped and never renumbered.
- Details and linking: **reference/evidence-and-ids.md**.
</evidence-doc>
<pipeline-integration>
Pipeline: an area investigation → doc pair → `draft-adr` → `write-solution-doc`; details in **reference/pipeline-integration.md**.
</pipeline-integration>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Writing the human doc structure, template, metadata | Human doc sections + template | [reference/structure-and-template.md](reference/structure-and-template.md) |
| Writing or formatting a human-doc topic block | Question style, representation rule, anchor rules | [reference/topic-block-guide.md](reference/topic-block-guide.md) |
| Writing a table or comparison table | Table principles, required columns, patterns | [reference/table-guidelines.md](reference/table-guidelines.md) |
| Building the evidence doc, ledger, IDs, and links | Evidence schema, confidence tags, coverage, slug IDs, linking | [reference/evidence-and-ids.md](reference/evidence-and-ids.md) |
| Wiring the pair into a spike or downstream doc | Handoff, shared schema, citation rules | [reference/pipeline-integration.md](reference/pipeline-integration.md) |
| Validating a pair before saving | Two-part checklist + severity | [reference/quality-checklist.md](reference/quality-checklist.md) |
| Sourcing the area's questions | Question-sourcing walkthrough | [examples/collect-area-questions.md](examples/collect-area-questions.md) |
| Authoring the human doc | Human doc example | [examples/author-findings-doc.md](examples/author-findings-doc.md) |
| Comparing one thing across flows | Comparison-table pattern | [examples/compare-across-flows.md](examples/compare-across-flows.md) |
| Building the evidence doc | Evidence doc example | [examples/author-evidence-doc.md](examples/author-evidence-doc.md) |
| Splitting a combined findings doc | Split migration walkthrough | [examples/split-existing-doc.md](examples/split-existing-doc.md) |
| Updating a pair on new evidence | In-place update example | [examples/update-findings-doc.md](examples/update-findings-doc.md) |
| Validating a pair | Validation-report example | [examples/validate-findings-doc.md](examples/validate-findings-doc.md) |
</context-loading-guide>

</knowledge>

<capabilities>

<collect-area-questions>
**Objective**: Produce the ordered question list that becomes the area's topic blocks.
1. Read the area's scope and verified investigation results.
2. Gather candidate questions from three sources: the user's questions, the questions the investigation answered, and the starter set in **reference/topic-block-guide.md**.
3. Merge duplicates; drop questions the evidence cannot answer or that cover more than one topic.
4. Order orientation questions (what/where) before depth questions (flow, config, gotchas).
5. Cap the list at 3–7 topics; ask the user to split the area when larger.
6. Verify each question is answerable from the verified evidence and covers a single topic; drop any that fail.
7. Confirm the question list with the user before authoring.
</collect-area-questions>
<author-findings-doc>
**Objective**: Write the publishable human findings doc for an area.
1. Write the YAML frontmatter (title, area, status) and a `**Summary:**` per **reference/structure-and-template.md**.
2. Write the Orientation index with a "Start here" pointer.
3. For each confirmed question, write one topic block per **reference/topic-block-guide.md**.
4. Draw every diagram in those blocks via `draw-mermaid-diagrams` (`author-mermaid-diagram`).
5. Keep `file:line` anchors inline for checking; add no claim IDs, confidence tags, or link to the evidence doc.
6. Apply **validate-findings-doc** (it validates diagrams via `draw-mermaid-diagrams`); fix findings and re-validate.
7. Save to `<spike-folder>/docs/findings-<area>.md` (or the user-provided path); offer to refine any topic.
</author-findings-doc>

<author-evidence-doc>
**Objective**: Build the machine evidence doc for an area.
1. Write the metadata block (area, spike, scope, status, related-areas, human doc) per **reference/evidence-and-ids.md**.
2. Extract every atomic claim from the human doc's topics and artifacts, and map each topic's heading anchor to its claims.
3. Assign each a stable claim ID (`<area>/<topic-slug>#cN`).
4. Record verdict, evidence `file:line`, and confidence (5-tag model) per claim.
5. Add the Searched-negatives table (search, result, next step).
6. Add the Coverage table (in-scope question, investigated, not investigated / gaps).
7. Add cross-area references for constraints shared with another area's pair.
8. Confirm every claim appears in the ledger and links back to its human topic heading.
</author-evidence-doc>

<split-findings-doc>
**Objective**: Convert one combined findings doc into the human doc and the evidence doc.
1. Inventory the combined doc: sections, claims, inline `file:line` references, and any existing IDs.
2. Build the human doc per **reference/structure-and-template.md**, keeping Summary, Orientation, Glossary, and topic artifacts.
3. Remove claim bullets, IDs, confidence tags, and the ledger from the human doc.
4. Build the evidence doc per **reference/evidence-and-ids.md**: topic map, ledger, searched-negatives, coverage.
5. Preserve existing claim IDs; assign new IDs only to unnumbered claims.
6. Apply **validate-findings-doc**; fix findings, then save both docs with mutual pointers.
</split-findings-doc>

<update-findings-doc>
**Objective**: Refresh an area's doc pair in place when evidence changes.
1. Locate the affected topic and claim by their stable IDs.
2. Update the affected evidence ledger rows; leave unaffected content untouched.
3. Never renumber existing IDs; add new IDs for new claims.
4. Update the claim's confidence tag and verdict (for example 🔶 Inferred → ✅ Verified).
5. Record new dead-end searches in Searched-negatives; update Coverage.
6. Refresh the human topic only when its reader-facing answer changed; keep its heading anchor stable.
7. Sync that topic's diagrams via `draw-mermaid-diagrams` (`sync-diagram-set`) when the change affects them.
8. Keep no version markers or changelogs — git is history.
9. Apply **validate-findings-doc**; then flag downstream artifacts that cite the changed IDs.
</update-findings-doc>

<validate-findings-doc>
**Objective**: Verify a findings doc pair before saving or delivering.
1. Load **reference/quality-checklist.md**.
2. Check the human doc: frontmatter, Summary, Orientation, and topic blocks, in order.
3. Check the human doc holds no claim IDs, confidence tags, ledger, or evidence-doc link.
4. Check the evidence doc: metadata, topic→claim map, ledger, Searched-negatives, Coverage, in order.
5. Check every human-doc topic claim appears in the ledger, and every ledger row links back to a topic.
6. Check IDs are unique, area-scoped, and unrenumbered; citation format is valid.
7. Check no target-state or decision content leaked in; validate every diagram via `draw-mermaid-diagrams` (0 errors).
8. Report findings by severity (🚫 Blocker / 🔴 Major / 🟡 Minor / 🟢 Nit) and fix before saving.
</validate-findings-doc>

</capabilities>

<rules>
<rule>When a verified investigation of an area is available, apply **collect-area-questions**, then **author-findings-doc** and **author-evidence-doc**.</rule>
<rule>When only the machine layer is requested, apply **author-evidence-doc** directly.</rule>
<rule>When an existing combined findings doc must be split, apply **split-findings-doc**.</rule>
<rule>When new evidence changes an existing area, apply **update-findings-doc** to both docs.</rule>
<rule>Before saving or delivering a pair, apply **validate-findings-doc**.</rule>
<rule>When the user wants target-state architecture or a decision record, do NOT use this skill — apply `write-solution-doc` or `draft-adr`.</rule>
<rule>When a spike area investigation exists, seed both docs from its evidence per **reference/pipeline-integration.md**.</rule>
</rules>

---
name: document-findings
description: Produce question-style findings docs mapping existing code to diagrams, tables, and file:line evidence for human and AI reference. Use when documenting, compiling, explaining, or updating findings for a code area.
---

<when-to-use-this-skill>
- Document the current state of a code area as a findings doc
- Compile a findings doc for a spike investigation area
- Explain existing code through diagrams, tables, and short question-style answers
- Update a findings doc when new evidence changes what is known
- Document the entry points and key files as a scannable resource index
- Compile claim-level evidence (`file:line`, confidence, gaps) for AI reference
</when-to-use-this-skill>

<knowledge>
<findings-doc-definition>
A findings doc explains what exists in a code **area** today, as question-style topics for a human reader and an AI consumer. Current-state only — never target-state or decisions.
</findings-doc-definition>
<dual-audience-model>
| Need | Human | AI consumer | Format response |
|---|---|---|---|
| Locate resources | Scan fast | Deterministic pointer | Orientation index + inline `file:line` |
| Understand | Self-explanatory diagram or clear table | Atomic claims | Topic block: TL;DR → artifact → claims |
| Trust | See the source | Verify verdict | Evidence ledger + confidence tags |
| Avoid rework | — | Know what is scanned | Searched-negatives + coverage |
| Cite precisely | Copy anchor | Stable citation | Scope-slug IDs |
| Stay current | Not stale | Update in place | Living doc, no version tags |
</dual-audience-model>
<findings-doc-structure>
- Fixed section order: metadata block → Summary → Orientation → Glossary (optional) → topic blocks → Evidence & Verification.
- Load **reference/structure-and-template.md** for titles, numbering, and template.
</findings-doc-structure>
<topic-block-format>
- Each topic answers one reader question: TL;DR → primary artifact → claims.
- Pick the representation diagram-first per **reference/topic-block-guide.md**.
- Apply **reference/table-guidelines.md** for comparison tables.
- Multiple diagrams per topic are allowed.
</topic-block-format>
<evidence-ledger>
- The AI-tracking layer: a consolidated ledger (claim ID → claim → verdict → evidence `file:line` → confidence) plus searched-negatives and coverage.
- Confidence uses the 5-tag model; IDs are scope slugs (`<area>/<topic-slug>#cN`), area-scoped and never renumbered.
- Details: **reference/evidence-and-ids.md**.
</evidence-ledger>
<artifact-layout>
One doc per area at `<spike-folder>/docs/findings-<area>.md` inside a spike; a user-provided path otherwise. The filename slug matches the metadata `area` and the topic-ID prefix.
</artifact-layout>
<inappropriate-scenarios>
| Do NOT use for | Route to |
|---|---|
| Target-state architecture, solution documents, decision records | `write-solution-doc`, `draft-adr` |
| Unverified investigation output | `investigate-code` (verify evidence first) |
</inappropriate-scenarios>
<pipeline-integration>
- Position: `investigate-code` → findings doc → `draft-adr` → `write-solution-doc`.
- Spike seed: `conduct-spike` seeds each area's doc. Details: **reference/pipeline-integration.md**.
</pipeline-integration>

<concise-writing>
- Open every topic with a `**TL;DR:**` line (≤15 words).
- Keep sentences ≤20 words; one claim per bullet.
- Tables and diagrams carry detail; never restate one.
- No banned phrases ("it is important to note", "this section describes").
</concise-writing>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Writing the doc structure, template, numbering, metadata block | Canonical sections + template | [reference/structure-and-template.md](reference/structure-and-template.md) |
| Writing or formatting a topic block | Question style, representation rule, claim rules | [reference/topic-block-guide.md](reference/topic-block-guide.md) |
| Writing a table or comparison table | Table principles, required columns, patterns | [reference/table-guidelines.md](reference/table-guidelines.md) |
| Building the evidence ledger and IDs | Ledger schema, confidence tags, searched-negatives, coverage, slug IDs | [reference/evidence-and-ids.md](reference/evidence-and-ids.md) |
| Wiring the doc into a spike or downstream doc | Handoff, shared schema, citation rules | [reference/pipeline-integration.md](reference/pipeline-integration.md) |
| Validating a findings doc before saving | Quality checklist + severity | [reference/quality-checklist.md](reference/quality-checklist.md) |
| Sourcing the area's questions | Question-sourcing walkthrough | [examples/collect-area-questions.md](examples/collect-area-questions.md) |
| Authoring a full per-area doc | End-to-end doc example | [examples/author-findings-doc.md](examples/author-findings-doc.md) |
| Comparing one thing across flows | Comparison-table pattern | [examples/compare-across-flows.md](examples/compare-across-flows.md) |
| Building only the evidence ledger | Ledger-only example | [examples/compile-evidence-ledger.md](examples/compile-evidence-ledger.md) |
| Updating a doc on new evidence | In-place update example | [examples/update-findings-doc.md](examples/update-findings-doc.md) |
| Validating a doc | Validation-report example | [examples/validate-findings-doc.md](examples/validate-findings-doc.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<collect-area-questions>
**Objective**: Produce the ordered question list that becomes the area's topic blocks.
1. Read the area's scope and verified investigation results.
2. Gather candidate questions from three sources: the user's questions, the questions the investigation answered, and the starter set in **reference/topic-block-guide.md**.
3. Merge duplicates; drop questions the evidence cannot answer.
4. Order orientation questions (what/where) before depth questions (flow, config, gotchas).
5. Cap the list at 3–7 topics; ask the user to split the area when larger.
6. Verify each question is answerable from the verified evidence and covers a single topic; drop any that fail.
7. Confirm the question list with the user before authoring.
</collect-area-questions>
<author-findings-doc>
**Objective**: Write the complete per-area findings doc.
1. Write the metadata block and Orientation index per **reference/structure-and-template.md**.
2. For each confirmed question, write one topic block per **reference/topic-block-guide.md**.
3. Assign each topic its scope-slug ID and each claim its `#cN` ID per **reference/evidence-and-ids.md**.
4. Apply **compile-evidence-ledger** to append Evidence & Verification.
5. Apply **validate-findings-doc**; fix findings and re-validate.
6. Save to `<spike-folder>/docs/findings-<area>.md` (or the user-provided path); offer to refine any topic.
</author-findings-doc>

<compile-evidence-ledger>
**Objective**: Build the consolidated AI-tracking layer for an area.
1. Collect every claim from the topic blocks — none may be missing from the ledger.
2. Assign each a stable claim ID (`<area>/<topic-slug>#cN`).
3. Record verdict, evidence `file:line`, and confidence (5-tag model) per claim.
4. Add the Searched-negatives table (search, result, next step).
5. Add the Coverage table (in-scope question, investigated, not investigated / gaps).
6. Add cross-area references for constraints shared with another area's findings doc.
7. Apply **reference/evidence-and-ids.md**; confirm every claim appears in both its topic block and the ledger.
</compile-evidence-ledger>

<update-findings-doc>
**Objective**: Refresh an area's findings doc in place when evidence changes.
1. Locate the affected topic and claim by their stable IDs.
2. Rewrite only the affected topic and ledger rows; leave unaffected content untouched.
3. Never renumber existing IDs; add new IDs for new claims.
4. Update the claim's confidence tag and verdict (for example 🔶 Inferred → ✅ Verified).
5. Record new dead-end searches in Searched-negatives; update Coverage.
6. Keep no version markers or changelogs — git is history.
7. Apply **validate-findings-doc**; then flag downstream artifacts that cite the changed IDs.
</update-findings-doc>

<validate-findings-doc>
**Objective**: Verify a findings doc before saving or delivering.
1. Load **reference/quality-checklist.md**.
2. Check structure: metadata block, Orientation, topic blocks, Evidence & Verification, in order.
3. Check every claim has a confidence tag, cites evidence per its type, and appears in the ledger.
4. Check IDs are unique, area-scoped, and unrenumbered; citation format is valid.
5. Check Searched-negatives and Coverage are present and honest.
6. Check no target-state or decision content leaked in; render every diagram and table.
7. Report findings by severity (🚫 Blocker / 🔴 Major / 🟡 Minor / 🟢 Nit) and fix before saving.
</validate-findings-doc>

</capabilities>

<rules>
<rule>When a verified investigation of an area is available, apply **collect-area-questions**, then **author-findings-doc**.</rule>
<rule>When only evidence tracking is requested, apply **compile-evidence-ledger** directly.</rule>
<rule>When new evidence changes an existing area, apply **update-findings-doc**.</rule>
<rule>Before saving or delivering a findings doc, apply **validate-findings-doc**.</rule>
<rule>When the user wants target-state architecture or a decision record, do NOT use this skill — apply `write-solution-doc` or `draft-adr`.</rule>
<rule>When running inside a spike, seed from `conduct-spike`'s area investigation and write to its `docs/` folder per **pipeline-integration**.</rule>
</rules>

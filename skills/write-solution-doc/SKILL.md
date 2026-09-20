---
name: write-solution-doc
description: Produce solution documentation with C4/sequence/flowchart diagrams, API/event schemas, RAID, and RACI — for decisions, architectures, and current-state findings. Use when documenting, authoring, producing, defining, performing, creating, or compiling solution-doc content.
---

<when-to-use-this-skill>
- User wants to document a finalized solution decision or architecture
- User needs a solution architecture document
- User wants C4 (C2/C3), sequence, or flowchart diagrams
- User needs API or event schemas
- User wants RAID analysis or a RACI matrix
- User wants to compile a multi-section solution document
- User is running a spike (via `conduct-spike`) and needs a solution or current-state findings document
</when-to-use-this-skill>

<knowledge>
<solution-doc-structure>
9 fixed sections in canonical order and numbering, with `**Takeaway:**` under every section. Load **reference/solution-doc-structure.md** for titles, `N.M` numbering, and template.
</solution-doc-structure>

<current-state-mode>
The same format documents **current state** and evolves a baseline into **target state**; load **reference/current-state-mode.md**, or **reference/seed-input-contract.md** in a `conduct-spike` run.
</current-state-mode>

<c4-model>
**C2 (Container)** = building blocks; **C3 (Component)** = one container's internals. Load **reference/mermaid-standards.md** for C4 syntax.
</c4-model>

<diagram-selection-guide>
Messages → **sequence**; process/decisions → **flowchart**; both → **both**; state lifecycle → **state diagram** (or **flowchart** when decisions dominate). Load **reference/diagram-selection-guide.md**.
</diagram-selection-guide>

<api-design-standards>
Load **reference/api-design-standards.md** for contract fields and conventions.
</api-design-standards>

<governance-frameworks>
Load **reference/raid-raci-frameworks.md** for the RAID item schema and RACI matrix rules.
</governance-frameworks>

<concise-writing>
Prose follows BLUF, hard caps, atomic bullets, tables-over-prose, and single source of truth, with a ~20% delete pass. See [reference/writing-style.md](reference/writing-style.md).
</concise-writing>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Compiling the final document | Canonical titles, numbering, template | [reference/solution-doc-structure.md](reference/solution-doc-structure.md) |
| Writing any Mermaid diagram | Syntax, label rules, zoom levels | [reference/mermaid-standards.md](reference/mermaid-standards.md) |
| Choosing a diagram type | Selection matrix, interop rules | [reference/diagram-selection-guide.md](reference/diagram-selection-guide.md) |
| Defining API/event contracts | Contract fields, conventions | [reference/api-design-standards.md](reference/api-design-standards.md) |
| Running RAID or RACI | Item schema, matrix rules | [reference/raid-raci-frameworks.md](reference/raid-raci-frameworks.md) |
| Producing/evolving a current-state document | As-is mode, baseline-input rules | [reference/current-state-mode.md](reference/current-state-mode.md) |
| Embedding in a sub-agent dispatch | Seed, guard, return contract | [reference/seed-input-contract.md](reference/seed-input-contract.md) |
| Writing document prose | BLUF, caps, banned phrases | [reference/writing-style.md](reference/writing-style.md) |
| Full end-to-end example | Final solution document | [examples/full-solution-document.md](examples/full-solution-document.md) |
| Diagram-focused example | C2, C3, sequence, flowchart | [examples/c4-and-interaction-diagrams.md](examples/c4-and-interaction-diagrams.md) |
| API/event contract example | REST + Kafka/Avro | [examples/api-contracts.md](examples/api-contracts.md) |
| Deps/maintainers example | Docs, deps, ownership | [examples/dependencies-and-maintainers.md](examples/dependencies-and-maintainers.md) |
| RAID/RACI example | Governance, ownership | [examples/raid-and-raci.md](examples/raid-and-raci.md) |
| Diagram-sync example | Mid-session corrections | [examples/diagram-sync.md](examples/diagram-sync.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<clarify-business-context>
1. Detect the user's language (English or Chinese) and respond in it.
2. Ask 3–10 targeted questions, one at a time, about the business context.
3. Probe:
   - The problem this solution solves.
   - Alternatives considered and why this one was chosen.
   - Business constraints (timeline, budget, compliance).
   - Stakeholders and end users.
   - Scope in and out.
4. Wait for the response before asking the next question.
5. Summarize the context and ask the user to confirm before continuing.
6. If the user provides existing context, incorporate it directly and confirm understanding.
</clarify-business-context>

<draw-c4-topology>
1. From the confirmed context, identify the C2 containers involved.
2. Ask 3–8 clarifying questions, one at a time, about:
   - Participating systems/services/applications.
   - Communication style (sync HTTP, async messaging, gRPC).
   - External systems and users.
3. Produce a C2 Container diagram (`C4Container`) with a brief explanation.
4. On confirmation, zoom into the most critical container for a C3 diagram.
5. Produce the C3 Component diagram (`C4Component`) with a brief explanation.
6. Ask the user to confirm; offer additional C3 diagrams if needed.
7. Refine from feedback until confirmed.
</draw-c4-topology>

<draw-interaction-diagrams>
1. From the confirmed topology, identify the key interaction flows.
2. Per flow, consult **diagram-selection-guide** for sequence, flowchart, or both; if unsure, explain the trade-off and ask.
3. Ask 3–8 clarifying questions, one at a time, about:
   - Which flows are most critical.
   - Sequence diagrams: call order, sync vs async, error/edge flows.
   - Flowcharts: decision points, branch conditions, start/end states.
4. Produce one Mermaid diagram per critical flow.
5. **Sequence requirements**: clear participants, message ordering, activation bars, notes.
6. **Flowchart requirements**: start/stop nodes, process steps, decision diamonds, labeled branches.
7. Ask the user to confirm each diagram; refine from feedback.
</draw-interaction-diagrams>

<design-api-event-schema>
1. For each interaction, define the API contract or event schema.
2. Ask 3–8 clarifying questions, one at a time, about:
   - Preferred API style (REST, gRPC, GraphQL, async messaging).
   - Required fields, types, validation.
   - Auth requirements.
   - Rate limiting, pagination, idempotency.
3. Document each with endpoint/topic, method, request/response schema, auth, and error codes.
4. Event schemas also include versioning and DLQ handling.
5. Present schemas as tables or code blocks.
6. Ask the user to confirm each schema; refine from feedback.
</design-api-event-schema>

<list-related-documents>
1. Ask 2–5 questions, one at a time, about:
   - Design docs, RFCs, ADRs.
   - External API or vendor specs.
   - Regulatory/compliance documents.
   - Prior solution docs.
2. List each with title, type (RFC/ADR/Design/External), link/path, and one-line relevance.
3. Present as a table.
4. Ask the user to confirm.
</list-related-documents>

<list-external-dependencies>
1. From the diagrams and interactions, identify external systems/services depended on.
2. For each, ask the user for:
   - Name and description.
   - Owning team.
   - Primary contact.
   - SLA/availability.
   - Fallback if unavailable.
3. Present as a table.
4. Ask the user to confirm, adding or removing as needed.
</list-external-dependencies>

<list-maintainers>
1. For each component, identify:
   - Component name.
   - Owning team.
   - Primary contact.
   - Secondary contact.
2. Present as a table.
3. Ask the user to confirm and allow edits.
</list-maintainers>

<list-raids>
1. Identify Risks, Assumptions, Issues, and Dependencies across all four categories.
2. Per category, ask 3–5 targeted questions, one at a time, to surface missed items.
3. Example probes:
   - Risks: "What if the primary database is unavailable?"
   - Assumptions: "Are we assuming <100ms upstream responses?"
   - Issues: "Any unresolved disagreements or missing specs?"
   - Dependencies: "Do we depend on another team before go-live?"
4. Document each item: ID, Category, Description, Impact (H/M/L), Probability (Risks only), Mitigation, Owner, Status.
5. Present as a table per category.
6. Ask the user to confirm and allow edits.
</list-raids>

<list-raci>
1. Identify key tasks, decisions, and deliverables across design, implementation, testing, deployment, and operations.
2. Identify all teams/roles involved.
3. Ask 3–8 clarifying questions, one at a time, to assign R/A/C/I per task.
4. Remind the user: only ONE "A" per row.
5. Present a matrix: tasks as rows, roles as columns, R/A/C/I in cells.
6. Ask the user to confirm and allow edits.
</list-raci>

<structure-solution-doc>
1. Load **reference/solution-doc-structure.md** and compile all confirmed sections using its canonical titles, `N.M` numbering, and template (apply **concise-writing**).
2. Open every `##` section with a `**Takeaway:**` line (≤15 words); tables and diagrams carry the detail.
3. Use tables for structured data and code blocks for Mermaid and JSON/YAML schemas; never restate a table or diagram.
4. Mark explicitly skipped sections as `[Skipped]`.
5. Validate Mermaid diagrams with `scripts/validate_mermaid.mjs`; fix to 0 failures.
6. Match the user's language preference.
7. Run the concise check (see **concise-writing**): ≤20-word sentences, no banned phrases, one claim per bullet, a takeaway per heading, no restated fact, ~20% cut.
8. Present the document and offer to refine any section.
</structure-solution-doc>

<sync-diagrams>
1. After a confirmed new finding or correction (changed topology, added/removed container or component, corrected flow, revised schema, new dependency or edge case), list every diagram produced earlier.
2. Per diagram, decide whether the change affects any element, relationship, message, branch, or section, leaving unaffected ones untouched.
3. Update each affected diagram to the latest confirmed state, stating in one line what changed and why.
4. Draw a new diagram (per **diagram-selection-guide**) for new context, and add it to its document section.
5. Cross-check the set: every confirmed fact appears in at least one diagram, and none contradicts the latest state.
6. Present updated and new diagrams with the revised sections, noting which changed.
</sync-diagrams>

</capabilities>

<rules>
<rule>When the user provides a solution decision to document, begin with **clarify-business-context**.</rule>
<rule>Follow the sequence unless asked otherwise: clarify-business-context → draw-c4-topology → draw-interaction-diagrams → design-api-event-schema → list-related-documents → list-external-dependencies → list-maintainers → list-raids → list-raci → structure-solution-doc. **sync-diagrams** is cross-cutting.</rule>
<rule>When a correction or new finding changes confirmed content, apply **sync-diagrams** before continuing.</rule>
<rule>When the user provides existing diagrams or architecture, incorporate them directly and confirm whether to reuse, modify, or add alongside.</rule>
<rule>When the user confirms ("looks good", "proceed", "next"), move to the next capability.</rule>
<rule>When the user says "skip [section]", skip that capability and mark the section `[Skipped]`.</rule>
<rule>When the user asks to jump to a capability, skip ahead and continue from there.</rule>
<rule>When the user says "draft all" or "generate full document", draft all sections at once via **structure-solution-doc**, then offer to refine.</rule>
<rule>When the user provides section content, incorporate it directly and confirm.</rule>
<rule>When the user switches language mid-session, switch subsequent output wholesale, keep confirmed content in its original language, and leave technical terms in English.</rule>
</rules>

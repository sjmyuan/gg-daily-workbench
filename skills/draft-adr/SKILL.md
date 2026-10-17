---
name: draft-adr
description: Guide users through drafting well-structured ADRs, proactively visualizing context and solutions with diagrams, and detailing each option's technical implementation. Use when creating, writing, drafting, or authoring an ADR, documenting decisions, evaluating options or their technical implementation, or compiling a record from raw notes.
---

<when-to-use-this-skill>
- User wants to create, write, draft, or author an ADR
- User needs to document an architectural or technical decision
- User wants to evaluate and compare architecture options
- User wants each option evaluated by its technical implementation (diagrams + code changes with locations)
- User needs to structure rough notes into an ADR
- User wants to compile an ADR from raw discussion points
- User is running a spike (via the `conduct-spike` skill) and needs options evaluated or an ADR drafted per decision problem
</when-to-use-this-skill>

<knowledge>
<prompting-guide>
Load **reference/prompting-guide.md** for decision-driver categories and option-brainstorming prompts.
</prompting-guide>

<option-labeling>
Label every option `Option N: <name>` once in **define-considered-options** — numbers only, never letters or bare names. Reuse that exact label in Considered Options, Decision Outcome, Evaluation headings, matrix columns, and elimination-tree nodes. Card fields: **reference/adr-template.md**.
</option-labeling>

<diagram-delegation>
Draw proactively when explaining context or a solution — never wait to be asked. Delegate mechanics to `draw-mermaid-diagrams`.
This skill decides which diagram type, content, and focus each ADR step needs, splitting views when crowded.
</diagram-delegation>

<option-tech-details>
Each option's tech details are option-specific target-state diagrams (C4 + sequence) plus a grounded code change profile, produced by **detail-options-tech** and rendered as the `#### Tech Details` card subsection. Load **reference/option-tech-details-guide.md**.
</option-tech-details>

<concise-writing>
ADR prose follows BLUF, hard caps, atomic bullets, tables-over-prose, and single source of truth. Load **reference/writing-style.md** for the full rules.
</concise-writing>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Compiling the final ADR document (**compile-adr** step 3) | ADR markdown template with placeholders | [reference/adr-template.md](reference/adr-template.md) |
| Prompting for decision drivers or brainstorming options | Driver categories and option prompts | [reference/prompting-guide.md](reference/prompting-guide.md) |
| Detailing or rendering an option's technical implementation | Per-option tech details format and grounding contract | [reference/option-tech-details-guide.md](reference/option-tech-details-guide.md) |
| Writing or reviewing any ADR prose | BLUF, caps, banned phrases, atomic bullets, single source of truth | [reference/writing-style.md](reference/writing-style.md) |
| Full walkthrough from a well-formed problem statement | Database-selection walkthrough (all capabilities) | [examples/database-selection.md](examples/database-selection.md) |
| Structuring partial notes or rough ideas into an ADR | Auth walkthrough from unstructured input | [examples/from-rough-notes.md](examples/from-rough-notes.md) |
| Mid-session corrections; diagrams must stay current | **sync-diagrams** walkthrough | [examples/diagram-sync.md](examples/diagram-sync.md) |
| Per-option tech details with diagrams and code diffs | Worked example for one area | [examples/option-tech-details-example.md](examples/option-tech-details-example.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<define-problem>
1. Ask the user to describe the decision in 2–3 sentences.
2. If vague, ask follow-ups to clarify scope, stakeholders, and systems involved.
3. Resolve ambiguous terms and implicit assumptions.
4. Restate the problem as a structured summary and ask: "Does this accurately capture the problem?"
5. Iterate until the user confirms.
6. Draw the context diagram via `draw-mermaid-diagrams` — usually C4 context, zooming to a flowchart or sequence.
</define-problem>

<define-decision-drivers>
1. Ask: "What are the key factors, constraints, or priorities that will influence this decision?"
2. If the user struggles, suggest categories from **reference/prompting-guide.md**.
3. Help distinguish hard constraints (must-haves / knock-outs) from soft preferences (nice-to-haves).
4. Summarize drivers in a bullet list and ask the user to confirm or reorder by priority.
5. Draw the decision driver map via `draw-mermaid-diagrams` so constraints and preferences are visible.
</define-decision-drivers>

<define-considered-options>
1. Ask: "What options have you already considered for addressing this problem?"
2. If only one option, brainstorm alternatives using **reference/prompting-guide.md**.
3. Ensure each option is concrete and distinct (no near-duplicates).
4. Cap the list at 3–4 distinct options — if more remain, ask the user which 3–4 to evaluate and park the rest.
5. Assign each a stable `Option N: <name>` label, present the list, and ask the user to confirm before evaluating.
</define-considered-options>

<evaluate-options>
1. For each option, ask the user its main strengths and its main disadvantages, risks, or trade-offs.
2. Map pros/cons against the drivers in a driver-impact table; list pros/cons as one-line key points, no analysis.
3. If the user wants technical implementation evidence — or code findings (spike pipeline) exist — apply **detail-options-tech** per option, then judge pros/cons against it (see **option-tech-details**).
4. Present the option as its fixed card — Verdict, What it is, How it works, Pros, Cons (per **option-labeling**) — plus the driver-impact table, then confirm.
5. After all options, draw the comparison matrix and elimination tree via `draw-mermaid-diagrams`, highlighting knock-outs.
6. Ask: "Given the evaluations, which option best satisfies the decision drivers?"
</evaluate-options>

<detail-options-tech>
1. Determine the evidence base: investigation findings (e.g., a `conduct-spike` findings doc) and code accessibility.
2. If no evidence but code is accessible, build an evidence map via `investigate-code`: entry points, key locations with `file:line`, call chains.
3. Per option, draw target-state diagrams: evolve the current-state C4 view to this option's to-be, plus sequence diagram(s) for the changed flow. Never reuse another option's diagram.
4. Per option, build its code change profile: location (`file:line` + symbol), current code, git-style diff, and a 1–2 sentence how-to, listing new files briefly.
5. Ground every entry to the evidence map, tag confidence **verified / inferred / unverified**, and never invent APIs, symbols, or files — mark unverifiable changes **unverified**.
6. If no evidence and no code access: produce architectural-level profiles, mark locations **unverified**, and recommend a `conduct-spike` spike.
7. Present each option's tech details and ask whether any need correction or deeper investigation.
8. Keep confirmed tech details for the ADR's `#### Tech Details` card subsection (see **reference/option-tech-details-guide.md**).
</detail-options-tech>

<compile-adr>
1. Gather confirmed outputs: problem statement, drivers, considered options, and evaluations.
2. Prompt for metadata: title, owners, and status (draft | adopt | declined | superseded).
3. Load **reference/adr-template.md** and populate it, using the recommended option in the `**Chosen:**` field with a synthesized justification, and include each option's `#### Tech Details` when provided.
4. Draw the target-state C4/flowchart view via `draw-mermaid-diagrams` and embed it with the session's diagrams.
5. Fill the Consequences section from the evaluated pros/cons and risks.
6. Verify against this checklist:
   - [ ] Problem statement is clear, scoped, and unambiguous
   - [ ] Drivers include hard constraints and soft preferences
   - [ ] At least 2 distinct options were evaluated
   - [ ] Every option reuses its `Option N: <name>` label across all sections
   - [ ] Every option section has Verdict, What it is, How it works, Pros, and Cons
   - [ ] Pros/cons tie to decision drivers
   - [ ] Options with tech details carry a `#### Tech Details` subsection
   - [ ] `**Chosen:**` justification references specific drivers
   - [ ] Consequences address risks and positive impacts
   - [ ] Context and target state are diagrammed
   - [ ] Every Mermaid block validated via `draw-mermaid-diagrams` (0 errors)
   - [ ] Metadata (title, owners, status) is populated
   - [ ] Every section opens with a bolded one-line takeaway (BLUF)
   - [ ] No sentence exceeds 20 words; no banned phrases (see **concise-writing**)
   - [ ] Pros/cons and consequences are one-claim bullets, no justification
   - [ ] Delete-by-default pass run (~20% cut)
   - [ ] Single source of truth: no fact restated across sections, tables, or diagrams
   - [ ] Diagram/table captions carry the takeaway; no prose restates them
7. Present the completed ADR for final review: "Would you like to adjust any section before saving?"
</compile-adr>

<sync-diagrams>
1. After a confirmed correction or new finding, apply `draw-mermaid-diagrams` (**sync-diagram-set**) to the session's diagrams.
2. Restate each delta in ADR terms: which option card, driver, or section the updated diagram supports.
3. Cross-check the ADR: no driver, option verdict, or chosen outcome is contradicted by a diagram.
4. Present updated and new diagrams with the revised ADR content, noting which changed.
</sync-diagrams>

</capabilities>

<rules>
<rule>Run the linear pipeline with confirmation between steps: **define-problem** → **define-decision-drivers** → **define-considered-options** → **evaluate-options** → **compile-adr**.</rule>
<rule>If the user adds an option mid-evaluation, apply **evaluate-options** to assess it, then **sync-diagrams** to update the comparison matrix and elimination tree.</rule>
<rule>If the user revises the problem or drivers, re-apply the affected downstream capabilities, then **sync-diagrams** to update every affected diagram.</rule>
<rule>After each user confirmation, update any in-progress ADR draft so nothing is lost.</rule>
<rule>When the user corrects confirmed content or reveals new context (new option, revised driver, changed chosen option, new flow), apply **sync-diagrams** to update affected diagrams and add new ones.</rule>
<rule>When drawing, validating, or syncing any diagram, apply the `draw-mermaid-diagrams` skill for mechanics.</rule>
<rule>When explaining context or a solution, proactively draw the matching diagram via `draw-mermaid-diagrams` — do not wait to be asked.</rule>

<rule>When the user wants per-option technical implementation (diagrams, code diffs, or change locations), apply **detail-options-tech** during **evaluate-options**.</rule>
</rules>

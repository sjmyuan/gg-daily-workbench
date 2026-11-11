---
name: draft-adr
description: Guide users through drafting well-structured ADRs, visualizing context and options with informative diagrams, and detailing every option's implementation. Use when creating, writing, drafting, or authoring an ADR, documenting decisions, evaluating options or their implementation, or compiling a record from raw notes or spike evidence.
---

<when-to-use-this-skill>
- User wants to create, write, draft, or author an ADR
- User needs to document an architectural or technical decision
- User wants to evaluate and compare architecture options
- User wants each option evaluated by its technical implementation (diagrams + code changes with locations + an implementation plan)
- User needs to structure rough notes into an ADR
- User wants to compile an ADR from raw discussion points
- A decision problem with drivers and a cited evidence doc needs its options evaluated and drafted into an ADR
</when-to-use-this-skill>

<knowledge>
<seeded-brief>
A seeding brief supplies the problem, decision drivers, candidate and rejected options, the evidence doc with cited `file:line`, and sibling constraints. Those are settled intake: run the flow headlessly from them — never re-derive the drivers, re-ask the user, re-read code for a cited location, or search for your own inputs. Return the ADR plus the cited evidence it relies on, any decision resting on an accepted assumption, and any constraint the evidence doc lacks.
</seeded-brief>

<option-labeling>
Label every option `Option N: <name>` once in **define-considered-options** — numbers only, never letters or bare names. Reuse that exact label in Considered Options, Decision Outcome, Evaluation headings, matrix columns, elimination-tree nodes, and implementation-plan change IDs.
</option-labeling>

<diagram-content>
A diagram is judged by what it carries, not by node count: nodes name technology and responsibility, edges name verb, protocol, and sync/async, and the view shows the delta plus a failure path. Contract: **reference/diagram-contract.md**.
</diagram-content>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Compiling the final ADR document (**compile-adr** step 3) | ADR markdown template with placeholders | [reference/adr-template.md](reference/adr-template.md) |
| Prompting for decision drivers or brainstorming options | Driver categories and option prompts | [reference/prompting-guide.md](reference/prompting-guide.md) |
| Detailing or rendering an option's technical implementation | Per-option change-set format and grounding contract | [reference/option-tech-details-guide.md](reference/option-tech-details-guide.md) |
| Drawing or reviewing any ADR diagram | Label, delta, failure-path, and anti-pattern contract | [reference/diagram-contract.md](reference/diagram-contract.md) |
| Writing or reviewing any ADR prose | BLUF, caps, detail carriers, banned phrases | [reference/writing-style.md](reference/writing-style.md) |
| Full walkthrough from a well-formed problem statement | Database-selection walkthrough (all capabilities) | [examples/database-selection.md](examples/database-selection.md) |
| The finished ADR document for that walkthrough | Complete template instance: option cards, evidence matrix, implementation plan | [examples/database-selection-adr.md](examples/database-selection-adr.md) |
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
6. Draw the context diagram per **reference/diagram-contract.md** — C4 context carrying volumes, protocols, and external dependencies, zooming to a flowchart or sequence where the decision turns on one flow.
</define-problem>

<define-decision-drivers>
1. Ask: "What are the key factors, constraints, or priorities that will influence this decision?"
2. If the user struggles, suggest categories from **reference/prompting-guide.md**.
3. Classify each driver as a hard constraint (knock-out) or a soft preference, tagged `HC n` / `SP n`.
4. Give each driver a metric, a threshold, and how it is measured — "low cost" becomes "≤ $400/month, invoiced cost".
5. Summarize one fact per bullet and ask the user to confirm or reorder by priority.
</define-decision-drivers>

<define-considered-options>
1. Ask: "What options have you already considered for addressing this problem?"
2. If only one option, brainstorm alternatives using **reference/prompting-guide.md**.
3. Ensure each option names a distinct mechanism — a different vendor of the same mechanism is not a distinct option.
4. Cap the list at 3–4 distinct options — if more remain, ask the user which 3–4 to evaluate and park the rest.
5. Assign each a stable `Option N: <name>` label, present the list, and ask the user to confirm before evaluating.
</define-considered-options>

<evaluate-options>
1. For each option, ask the user its main strengths and its main disadvantages, risks, and trade-offs.
2. Apply **detail-options-tech** to every option whose code is accessible — do not wait to be asked; apply its no-access branch otherwise.
3. Present the option's fixed card per **reference/adr-template.md** — Verdict, What it is, How it works, Driver impact, Concerns, Pros, Cons, Tech Details — with its own target-state diagram, then confirm.
4. Fill the driver-impact table per driver: the mark, the measured value, the evidence reference, and the confidence.
5. After all options, fill the comparison matrix table; add a matrix diagram or an elimination tree only when each knock-out changes the next question, labelling each edge with the deciding evidence.
6. Ask: "Given the evaluations, which option best satisfies the decision drivers?"
</evaluate-options>

<detail-options-tech>
1. Determine the evidence base: investigation findings (e.g., a `conduct-spike` findings doc) and code accessibility.
2. If no evidence but code is accessible, build an evidence map via `investigate-code`: entry points, key locations with `file:line`, call chains.
3. Number every required change `C1`, `C2`, … per option; reuse those numbers in the option card and the implementation plan.
4. Per option, draw target-state diagrams per **reference/diagram-contract.md**: the current state evolved to this option's to-be with every node marked NEW, CHANGED, or REMOVED, plus sequence diagram(s) for the changed flow including its failure path. Never reuse another option's diagram.
5. Per option, build its change set per **reference/option-tech-details-guide.md**: location (`file:line` + symbol), current code, git-style diff, and a 1–2 sentence how-to per change; list new files briefly.
6. Ground every entry to the evidence map, tag confidence **verified / inferred / unverified**, and never invent APIs, symbols, or files — mark unverifiable changes **unverified**.
7. If no evidence and no code access: produce architectural-level profiles, mark locations **unverified**, and recommend a `conduct-spike` spike.
8. Present each option's tech details and ask whether any need correction or deeper investigation.
</detail-options-tech>

<compile-adr>
1. Gather confirmed outputs: problem statement, drivers, considered options, evaluations, and change sets.
2. Prompt for metadata: title, owners, and status (draft | adopt | declined | superseded).
3. Load **reference/adr-template.md** and populate it, using the recommended option in the `**Chosen:**` field with a synthesized justification, and include each option's `#### Tech Details`.
4. Build the chosen option's `## Implementation Plan`: ordered change IDs, what must exist before each change, and a verification plus rollback line per change — reference the diffs, never restate them.
5. Draw the target-state C4/flowchart view per **reference/diagram-contract.md** and embed it with the session's diagrams.
6. Fill the Consequences section from the evaluated pros/cons and risks.
7. Load **reference/adr-quality-checklist.md** and pass every item; fix the ADR, not the checklist.
8. Present the completed ADR for final review: "Would you like to adjust any section before saving?"
</compile-adr>

<sync-diagrams>
1. After a confirmed correction or new finding, apply `draw-mermaid-diagrams` (**sync-diagram-set**) to the session's diagrams per **reference/diagram-contract.md**.
2. Restate each delta in ADR terms: which option card, driver, or section the updated diagram supports.
3. Cross-check the ADR: no driver, option verdict, or chosen outcome is contradicted by a diagram.
4. Present updated and new diagrams with the revised ADR content, noting which changed.
</sync-diagrams>

</capabilities>

<rules>
<rule>Run the linear pipeline with confirmation between steps: **define-problem** → **define-decision-drivers** → **define-considered-options** → **evaluate-options** → **compile-adr**.</rule>
<rule>When a seeding brief supplies the problem, drivers, options, and cited evidence locations, run the flow headlessly from it per **seeded-brief** — never re-derive, re-ask, or re-read cited code.</rule>
<rule>If the user adds an option mid-evaluation, apply **evaluate-options** to assess it, then **sync-diagrams** to update the comparison matrix and any elimination tree in the ADR.</rule>
<rule>If the user revises the problem or drivers, re-apply the affected downstream capabilities, then **sync-diagrams** to update every affected diagram.</rule>
<rule>After each user confirmation, update any in-progress ADR draft so nothing is lost.</rule>
<rule>When the user corrects confirmed content or reveals new context, apply **sync-diagrams** to update affected diagrams and add new ones.</rule>
<rule>When explaining context or a solution, draw the matching diagram without being asked — mechanics via `draw-mermaid-diagrams`, content per **reference/diagram-contract.md**.</rule>
<rule>Never present an option without its mechanism flow, its own target-state diagram, and — when code is accessible — its change set.</rule>
</rules>

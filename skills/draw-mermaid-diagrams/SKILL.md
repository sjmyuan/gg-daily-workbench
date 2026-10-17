---
name: draw-mermaid-diagrams
description: Author, validate, and synchronize Mermaid diagrams for architecture docs — C4, sequence, flowchart, state, class, and ER. Use when drawing, diagramming, normalizing, validating, fixing, syncing, or embedding Mermaid diagrams.
---

<when-to-use-this-skill>
- Draw a Mermaid diagram to explain a system, flow, interaction, or lifecycle
- Validate or fix Mermaid syntax before presenting
- Normalize user-supplied diagrams to house conventions
- Update diagrams after a correction or new finding
- Embed diagrams in architecture documentation
</when-to-use-this-skill>

<knowledge>
<diagram-principles>
One fenced `mermaid` block carries one diagram, drawn from the type and content it is given.

- Show everything the message requires: every element, relationship, branch, and state.
- Never trim content to hit a size target.
- Label every element, relationship, and branch; no unexplained abbreviations.
- State the takeaway in one line outside the block.
- Keep identity stable across edits: same title, aliases, and structure.
</diagram-principles>
<diagram-capabilities>
Types and contracts: C4 context/container/component, sequence, flowchart, state, class, ER.
Load **reference/diagram-capabilities.md** for what each shows, its constraints, and normalization rules.
</diagram-capabilities>

<c4-model>
C1 = system landscape; C2 = containers inside one system; C3 = components inside one container.
Use native `C4Context`, `C4Container`, and `C4Component`; mark externals with `_Ext`.
Load **reference/c4-syntax.md**.
</c4-model>

<sequence-contract>
One zoom level, traceable participants, real messages. Load **reference/sequence-syntax.md**.
</sequence-contract>

<decision-diagrams>
Driver map, matrix, and elimination tree are decision-record idioms. Load **reference/decision-diagram-patterns.md**.
</decision-diagrams>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Drawing a named type or normalizing a supplied one | What each type shows, constraints, normalization | [reference/diagram-capabilities.md](reference/diagram-capabilities.md) |
| Drawing a flowchart or state diagram | Shapes, branch rules, state triggers | [reference/flow-state-syntax.md](reference/flow-state-syntax.md) |
| Drawing a class or ER diagram | Class members, ER cardinality, examples | [reference/data-model-syntax.md](reference/data-model-syntax.md) |
| Writing or fixing a label | Breakers, quoting, escapes | [reference/label-safety.md](reference/label-safety.md) |
| Drawing a C4 context, container, and component set | C1 → C2 → C3 walkthrough | [examples/author-c4-pair.md](examples/author-c4-pair.md) |
| Drawing a code-level sequence | Cross-file flow walkthrough | [examples/author-sequence-diagram.md](examples/author-sequence-diagram.md) |
| Drawing process logic and a lifecycle | Flowchart + state walkthrough | [examples/author-flowchart-state.md](examples/author-flowchart-state.md) |
| Fixing parse failures or setting up `mmdc` | Setup + failure → fix walkthrough | [examples/validate-and-fix-diagram.md](examples/validate-and-fix-diagram.md) |
| Updating diagrams after a correction | Inventory → replace → cross-check walkthrough | [examples/sync-diagram-set.md](examples/sync-diagram-set.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<author-mermaid-diagram>
**Objective**: Produce a renderable Mermaid block that meets its type contract.
1. Load the syntax reference for the chosen type.
2. Open a `mermaid` fence with the type declaration; add `title` to C4 diagrams.
3. Name elements for the reader: real systems, containers, endpoints, methods, or states.
4. Quote any label containing `" ( ) [ ] { } |`; use `<br/>` for line breaks.
5. Apply the type contract from that reference.
6. Include every element and relationship the diagram requires; never drop content.
7. State the takeaway in one line outside the block.
8. Apply **validate-diagram-syntax** before presenting.
9. Insert into the document with `insert --after-title <anchor> --text "<block>"` for a file target.
10. Verify every element, relationship, and branch is labeled and the takeaway matches the diagram.
</author-mermaid-diagram>

<ensure-mermaid-cli>
**Objective**: Guarantee a working `mmdc` before any validation.
1. Detect with `mmdc --version`; report the version and continue when it succeeds.
2. If missing, give the exact install command and ask: install now, you run it, or use npx/Docker?
3. Install only after consent: `npm i -g @mermaid-js/mermaid-cli`; fallbacks in **reference/mermaid-cli.md**.
4. Verify with `mmdc --version` plus a one-block render, and report the runner in effect.
</ensure-mermaid-cli>

<validate-diagram-syntax>
**Objective**: Prove every block parses and meets house rules.
1. Apply **ensure-mermaid-cli**, then render the document or block: `mmdc -i <doc>.md -o /tmp/check.md`.
2. On a parse error, extract that block by title or hash: `extract <doc> --title <t> --out /tmp/d.mmd`.
3. Render it alone: `mmdc -i /tmp/d.mmd -o /tmp/d.svg`.
4. Fix each error at its reported line; reword rather than escape, and re-run to 0.
5. Check what the parser cannot judge: zoom level, labeled branches, participants.
6. Report blocks checked, parse failures, and accepted warnings.
</validate-diagram-syntax>

<sync-diagram-set>
**Objective**: Bring every affected diagram to the latest confirmed state.
1. Inventory the set: `python3 scripts/mermaid_blocks.py list <file-or-dir>` (index, line, type, title, hash).
2. Map the change to depicted elements; mark each diagram affected or unaffected.
3. Edit an affected diagram in place, preserving its title, aliases, and structure.
4. Replace by stable selector: `... replace <file> --title "<title>"` (or `--hash <id>`) with `--from <new.mmd>`.
5. State the delta in one line before the updated block.
6. Insert a new block with a distinct title when the change adds content no block covers.
7. Cross-check: every fact appears somewhere, no diagram contradicts the latest state, no stale copy remains.
8. Apply **validate-diagram-syntax**, then report changed and unchanged diagrams.
9. Verify identity survived: updated diagrams keep their titles and aliases, new diagrams have unique titles.
</sync-diagram-set>

</capabilities>

<rules>
<rule>When the user or request names a diagram type → apply **author-mermaid-diagram**.</rule>
<rule>When the type is undecided → ask the user; never pick a type for them.</rule>
<rule>Before presenting, embedding, or saving any diagram → apply **validate-diagram-syntax**.</rule>
<rule>When `mmdc` is missing or fails to run → apply **ensure-mermaid-cli** before validating.</rule>
<rule>When a confirmed fact changes a diagram → apply **sync-diagram-set**.</rule>
<rule>When supplied diagrams use another convention → **author-mermaid-diagram** to normalize them.</rule>
<rule>Do NOT load for SVG diagram authoring — use the `edit-svg` skill instead.</rule>
</rules>

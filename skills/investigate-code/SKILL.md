---
name: investigate-code
description: Investigate codebases to answer how functionality, architecture, and cross-system dependencies work. Use when investigating, understanding, tracing, visualizing, documenting code, discovering patterns, grounding a decision, building an ADR evidence map, or splitting a broad investigation across parallel areas.
---

<when-to-use-this-skill>
- User asks how existing code works, or wants a feature explained
- User needs control flow, data flow, or dependencies traced
- User wants to investigate code across multiple repositories
- User wants the answer shown as a diagram, call-stack detail, or a compiled report
- User wants implementation patterns discovered or inconsistencies detected
- An investigation must ground a decision draft or ADR evidence map
- A broad question splits into independent areas that can run in parallel
</when-to-use-this-skill>

<knowledge>

<request-intake>
Gate every question before searching — a wrong system or depth wastes the run.

| Inference | Ask |
|---|---|
| system | repo or service? |
| scope | feature, module, or symbol? |
| depth | C4 level, sequence, or call stack? |
| consumer | who reads the answer? |

States: `ACCEPTED` · `ACCEPTED-WITH-ASSUMPTIONS` · `BLOCKED`, carried into the answer.
A brief stating all four fields is the gate result; a clone never asks the user.
</request-intake>

<search-strategies>
Detect the tools first — never assume a search tool exists.

| Strategy | Use for | If absent |
|---|---|---|
| Semantic search | concepts | grep variants |
| Grep | identifiers | `rg`, else `grep` |
| File search | names, layouts | infer from imports |

Tag reduced recall ❓ Gap.
</search-strategies>

<diagram-types>
Choose by message: C4 for architecture, sequence for interactions, flowchart for decisions, state for lifecycles, class/ER for data.
</diagram-types>

<pattern-discovery-heuristics>
Search peers in order: package naming → suffix (`*Controller`, `*Orchestrator`, `*Adapter`, `*Repository`) → interface implementations → shared annotations → dependency mirroring.
Fingerprint, matrix, severities: [reference/pattern-discovery-strategies.md](reference/pattern-discovery-strategies.md).
</pattern-discovery-heuristics>

<finding-confidence-model>
Tag every finding; never present only what is certain.

| Tag | Meaning |
|---|---|
| ✅ Verified | read in code, `file:line` confirmed |
| 🔶 Inferred | reasoned from evidence, unconfirmed |
| 💭 Assumption | taken for granted, no evidence |
| ⚠️ Inconsistency | two sources disagree |
| ❓ Gap | searched but not found, or not investigated |

When to use each tag, and phrasing: [reference/confidence-and-coverage-guide.md](reference/confidence-and-coverage-guide.md).
</finding-confidence-model>

<quality-bar>
Grade every answer — a gate alone passes correct-but-dull output.
Pass ≥7/9 on three criteria, none at 0.
</quality-bar>

<plain-language-presentation>
Explain every issue so a non-expert can act on it; for findings, explanation outranks brevity.
Render each ⚠️ Inconsistency, consequential ❓ Gap, and unverified 🔶 Inferred finding as an issue card.
Add the legend at first use; open multi-finding answers with a 3-line TL;DR.
Card anatomy: [reference/plain-language-presentation.md](reference/plain-language-presentation.md).
</plain-language-presentation>

<spike-integration>
Inside a spike area, read the existing evidence doc at its absolute path before re-scanning.
Its known locations and searched digests are settled input; return your search log for the next unit.
Return tagged claims and searched-negatives; `document-findings` owns the doc write.
Do not load when no spike area has been defined.
</spike-integration>

<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Any typical investigation | Walkthrough | [examples/investigation-workflow.md](examples/investigation-workflow.md) |
| Grading an answer | Criteria | [reference/investigation-quality-bar.md](reference/investigation-quality-bar.md) |
| Method-level call stacks | Frame format | [reference/call-stack-trace-conventions.md](reference/call-stack-trace-conventions.md) |
| Pattern variants | Matrix, severities | [reference/pattern-discovery-strategies.md](reference/pattern-discovery-strategies.md) |
| Across repos | Matrix, C2, traces | [examples/multi-repo-dependency.md](examples/multi-repo-dependency.md) |
| Zooming C2 → call stack | All four levels | [examples/progressive-zoom-in.md](examples/progressive-zoom-in.md) |
| Fanning one question across areas | Briefs, returns, merge | [examples/parallel-investigation.md](examples/parallel-investigation.md) |
| Compiling a markdown report | Report structure | [examples/markdown-report.md](examples/markdown-report.md) |
| Finding similar features | Pattern discovery | [examples/pattern-discovery.md](examples/pattern-discovery.md) |
| Tags, gaps, inconsistencies | Five categories | [reference/confidence-and-coverage-guide.md](reference/confidence-and-coverage-guide.md) |
| Prose rules | Caps, banned phrases | [reference/writing-style.md](reference/writing-style.md) |
| Plain issue | Card anatomy | [reference/plain-language-presentation.md](reference/plain-language-presentation.md) |
| Seeing terse → explained | Before/after | [examples/plain-language-findings.md](examples/plain-language-findings.md) |
</context-loading-guide>

</knowledge>

<capabilities>

<investigate-codebase>
**Objective**: Answer a question about existing code with located, tagged evidence.

1. Gate it per **request-intake** — restate, list every inference, ask the top 3 with options; none → step 2.
2. Discover code per **search-strategies** — entry points, key classes.
3. Trace control and data flow — role, data shape, errors.
4. Analyze dependencies — libraries, modules, services.
5. Extract the fingerprint: entry, layer chain, stereotypes, externals, errors.
6. Synthesize — answer first, then `file:line` evidence and open areas.
7. Present per **present-findings-with-confidence**.
8. Validate — paths checked, no gap omitted, grade ≥7/9 per **quality-bar**.
</investigate-codebase>

<analyze-cross-repo-dependencies>
**Objective**: Build a verified dependency matrix across repositories.

1. Identify repositories from the user, workspace, or layout.
2. Find interfaces per repo — config, HTTP clients, events, manifests, contracts.
3. Record each pair — direction, protocol, endpoints, error handling.
4. Present one matrix: Source, Target, Protocol, Direction, Details.
5. Flag sync links as failure cascades; tag inferred directions 🔶 and unscanned repos ❓.
6. Offer the C2 diagram, then apply **draw-c4-diagram**.
7. Validate — each direction confirmed in the source repo.
</analyze-cross-repo-dependencies>

<draw-c4-diagram>
**Objective**: Show the system landscape (C2) or one container's internals (C3).

1. Pick the level and type per **diagram-types** — C2 landscape or C3 internals.
2. List elements and connections with protocols.
3. Draw `C4Container` (C2) or `C4Component` (C3) via `draw-mermaid-diagrams`.
4. Present source and roles; code-found ✅, naming-based 💭.
5. Offer the next level.
6. Validate — every element traced to code or config; 0 syntax errors.
</draw-c4-diagram>

<draw-sequence-diagram>
**Objective**: Show message order for one operation.

1. Pick the operation from the user or the C2/C3 key interaction.
2. Trace participants, order, signatures, sync vs async, returns.
3. Draw via `draw-mermaid-diagrams`; numbers match call-stack frames.
4. Present the walkthrough; inferred flows and untraced calls as ❓.
5. Offer one message's call-stack trace.
6. Validate — sequential numbers, participants traced to code, 0 errors.
</draw-sequence-diagram>

<trace-call-stack>
**Objective**: Walk one method's call chain frame by frame.

1. Pick the method from the user or the sequence diagram's critical message.
2. Trace depth-first per [reference/call-stack-trace-conventions.md](reference/call-stack-trace-conventions.md).
3. Format `[N]` frames, `├─→`/`╰─→` branches, `[repo: name]` cross-repo calls.
4. Present logic, errors, and decisions; untraced branches ❓ Gap.
5. Validate — frame `[N]` matches message `N`; every path verified.
</trace-call-stack>

<discover-implementation-patterns>
**Objective**: Find peer implementations and state whether one pattern holds.

1. Take the fingerprint from **investigate-codebase** step 5.
2. Search peers per **pattern-discovery-heuristics**.
3. Classify each — match, variant, mismatch — by fingerprint.
4. Synthesize: one pattern → canonical example; variants → "⚠️ Inconsistency: N" with differences and files.
5. Give an issue card per **plain-language-presentation**.
6. Report heuristics used and names possibly missed as coverage limits.
7. Recommend standardization, or state uniqueness.
8. Validate — six dimensions per candidate, each classification evidenced.
</discover-implementation-patterns>

<compile-markdown-report>
**Objective**: Compile the investigation into one markdown report.

1. Confirm scope — which levels the report covers.
2. Assemble overview → internals → flows → methods.
3. Add decisions → edge cases → Confidence & Coverage → next steps.
4. Embed diagrams as Mermaid with a one-line description.
5. Close with the block from **present-findings-with-confidence**.
6. Validate — paths accurate, levels present, grade ≥7/9 per **quality-bar**.
</compile-markdown-report>

<present-findings-with-confidence>
**Objective**: State what is known, what is not, and what was missed.

1. Tag each claim ✅ Verified, 🔶 Inferred, or 💭 Assumption.
2. Report gaps — searched negatives, untraced paths, limits.
3. Raise inconsistencies per [reference/pattern-discovery-strategies.md](reference/pattern-discovery-strategies.md).
4. Close with the block, one claim per line, ≤20 words:

```
### Confidence & Coverage
- ✅ Verified: …
- 🔶 Inferred: …
- 💭 Assumptions: …
- ❓ Gaps: …
- ⚠️ Inconsistencies: …
```

5. Validate — tags separated, gaps stated and located, issues pass the non-expert test.
</present-findings-with-confidence>

<dispatch-investigation-clones>
**Objective**: Investigate independent areas in parallel and merge one answer.

1. Apply `fan-out-agents` **fan-out-tasks** for the split, briefs, dispatch, and merge.
2. Add the investigation return contract to every brief — boundary, sub-question, depth, claims tagged per **finding-confidence-model**, an issue card per issue, searched-negatives.
3. Require clones to return open questions upward — never ask the user, never re-fan-out.
4. Validate — areas disjoint and covering, every report used, conflicts surfaced as ⚠️, grade ≥7/9 per **quality-bar**.
</dispatch-investigation-clones>

</capabilities>

<rules>
<rule> When the user asks about existing code, apply investigate-codebase after **request-intake**. </rule>
<rule> When the question spans repositories, apply analyze-cross-repo-dependencies first. </rule>
<rule> When the user wants a landscape or container internals, apply draw-c4-diagram. </rule>
<rule> When the user wants message order for one operation, apply draw-sequence-diagram. </rule>
<rule> When the user wants method detail, apply trace-call-stack. </rule>
<rule> When the user wants a guided tour, apply draw-c4-diagram (C2) → draw-c4-diagram (C3) → draw-sequence-diagram → trace-call-stack. </rule>
<rule> When the user asks how a type of feature works, apply investigate-codebase then discover-implementation-patterns. </rule>
<rule> When the user asks for a document, apply compile-markdown-report. </rule>
<rule> When presenting findings, apply present-findings-with-confidence and, for issues, plain-language-presentation. </rule>
<rule> When the question splits into independent areas, apply dispatch-investigation-clones via `fan-out-agents`. </rule>
<rule> When drawing or validating a diagram, apply `draw-mermaid-diagrams`. </rule>
</rules>

# Topic Block Guide

Used by **collect-area-questions** and **author-findings-doc**.

## Question style
- Phrase each topic as a question a reader asks: "Where does a payment get authorized?", "How is retry configured?"
- Use What / Where / How / Why / What-happens-when phrasing.
- One topic = one question; split compound questions.
- Order orientation questions (what/where) before depth questions (flow, config, gotchas).

## Starter question set

Use when the user supplies no questions.

| Question | Finds |
|---|---|
| What is this area responsible for? | Purpose, boundary, owning entry point |
| Where are the entry points? | API handlers, jobs, consumers, CLI |
| How does data flow through it? | Call chain, transformations, storage |
| How is it configured? | Config keys, flags, env vars, defaults |
| What are the failure / gotcha paths? | Retries, error handling, edge cases |
| What is deliberately absent? | Unhandled cases, dead code, gaps |

## Representation rule

Pick the shape that best explains the answer — diagram-first.

| Answer is… | Use |
|---|---|
| A single flow, structure, sequence, state, or topology | **Diagram** — self-explanatory, no walkthrough needed |
| Branch or decision logic | **Diagram** (flowchart) |
| A comparison of the same thing across flows/variants | **Comparison table** (rows = compared items); add one diagram per flow when each flow's shape matters |
| A list of homogeneous facts (config, stores, dependencies) | **Table** with the required columns |
| Reasoning / "why" / a single fact | **Short prose** — it still names the value, key, or symbol it is about |

- Multiple diagrams per topic are allowed; split a crowded view instead of compressing it.
- Pick the type from the question: order/flow → sequence, branch → flowchart, structure → C4, lifecycle → state.
- Draw diagrams via `draw-mermaid-diagrams` (`author-mermaid-diagram`, then `validate-diagram-syntax`).
- Diagrams must label every element, annotate key elements with `file:line`, and avoid unexplained abbreviations.
- Table rules and required columns: **reference/table-guidelines.md**.

## Topic block format

```markdown
## <N>. <Question?>
**TL;DR:** <one-line answer>

> <optional one-line framing: scope or assumption the artifact relies on>

<diagram(s) — or a comparison table, or short prose>
```

- The TL;DR answers the question in ≤15 words.
- Add the framing line only when the artifact assumes something — a happy path, or one variant of several.
- Annotate diagram elements with `file:line`; name a concrete symbol (`Class#member`) or module (`module.function`).
- Hold no claim bullets, claim IDs, or confidence tags — those live only in `evidence-<area>.md`.

## Concreteness test

Run on every topic before publishing. A topic that survives a rename of the area is a summary, not a finding.

- **Rename the module.** Substitute another module's name for every concrete noun; a sentence that still reads true is generic — replace it with the symbol, key, or value.
- **Every topic carries at least one fact**: a symbol (`ChargeService#authorize`), a config key (`retry.attempts`), a table, a topic, an endpoint, or a stored value — with `file:line`, or for something absent, the named search that found nothing.
- **Config and constants carry the real key path, value, and default** — never "configured" or "several settings".
- **A flow names its real call targets**, not layers: `ChargeService#authorize` → `GatewayClient#post`, never "the service → the gateway".
- **No unnumbered adjective.** "Robust", "flexible", "simple" become the number, flag, or mechanism that earns the claim.

## Coverage of behavior
- Cover failure and edge paths where they change the answer — add `alt` branches to the diagram, or a dedicated failure topic.
- Do not diagram every error branch — only those a reader must know.
- A handled-and-logged retry is not a gotcha: a failure path earns a place only when it changes what a reader does.

## Anchors
- Never use vague references ("the service layer"); name a concrete symbol or module.
- Inline `file:line` anchors are for checking; the formal claim list and confidence live in the evidence doc.

# Topic Block Guide

Backs the `<topic-block-format>` knowledge entry; used by **collect-area-questions** and **author-findings-doc**.

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
| Reasoning / "why" / a single fact | **Short prose** (or nothing) |

- Multiple diagrams per topic are allowed.
- Diagrams must label every element, annotate key elements with `file:line`, and avoid unexplained abbreviations.
- Table rules and required columns: **reference/table-guidelines.md**.

## Topic block format

```markdown
## <N>. <Question?> <!-- id: <area>/<topic-slug> -->
**TL;DR:** <one-line answer>

> <optional one-line framing: scope or assumption the artifact relies on>

<diagram(s) — or a comparison table, or short prose>

**Claims**
- <atomic fact> — `Symbol#method (file:line)` <confidence>
```

Each claim states the fact; `Symbol#method (file:line)` is its evidence. Add the framing line only when the artifact assumes something — a happy path, or one variant of several.

## Coverage of behavior
- Cover failure and edge paths where they change the answer — add `alt` branches to the diagram, or a dedicated failure topic.
- Do not diagram every error branch — only those a reader must know.
- Annotate diagram elements with `Symbol (file:line)` so a reader can jump to code.

## Claim rules
- One fact per bullet; no reasoning or justification.
- Every claim cites `Symbol#method (file:line)` and a confidence tag.
- Confidence tags: ✅ Verified, 🔶 Inferred, 💭 Assumption, ⚠️ Inconsistency, ❓ Gap.
- Never present 🔶 Inferred or 💭 Assumption as ✅ Verified.
- Never use vague references ("the service layer") — always a symbol + `file:line`.

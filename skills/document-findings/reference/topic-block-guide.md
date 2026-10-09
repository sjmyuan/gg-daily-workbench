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

## Answer shape

Pick the smallest shape that conveys the answer.

| Answer type | Shape |
|---|---|
| Structure / responsibilities | Table |
| Message or call ordering | Sequence diagram |
| Decision or branch logic | Flowchart |
| Configuration / data store | Table |
| Single fact | One claim bullet, no visual |

Cap: one visual per topic.

## Topic block format

```markdown
## <N>. <Question?> <!-- id: <area>/<topic-slug> -->
**TL;DR:** <≤15-word answer>

<diagram or table>

**Key claims**
- <atomic fact> — `<path:line>` <confidence>
- <atomic fact> — `<path:line>` <confidence>
```

## Claim rules
- One fact per bullet; no reasoning or justification.
- Every claim carries an inline `file:line` and a confidence tag.
- Confidence tags: ✅ Verified, 🔶 Inferred, 💭 Assumption, ⚠️ Inconsistency, ❓ Gap.
- Never present 🔶 Inferred or 💭 Assumption as ✅ Verified.
- Never use vague references ("the service layer") — always `file:line`.

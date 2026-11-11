# Investigation Quality Bar

Used by **investigate-codebase**, **compile-markdown-report**, and **dispatch-investigation-clones** (their Validate steps). Grade every answer; a gate alone passes correct-but-dull output.

## Criteria

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| **Answers first** | background or method leads | answer appears mid-answer | direct answer in the first line |
| **Evidence density** | claims carry no location | some claims carry `file:line` | every load-bearing claim carries `file:line` |
| **Level fit** | depth wrong for the request | right depth, no next step offered | right depth, next level offered |

## Pass bar

- ≥7/9 and no criterion at 0.
- Any criterion at 0 → fix that dimension and re-grade; never ship and note it.
- Grading is silent: report the answer, not the score, unless the user asks.

## What a failing answer looks like

- Answers-first 0: three paragraphs of architecture before the sentence the user asked for.
- Evidence density 0: "the retry logic is centralized" with no `file:line`.
- Level fit 0: a call-stack dump when the user asked for the system landscape.

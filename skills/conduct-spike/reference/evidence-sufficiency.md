# Evidence Sufficiency

Loaded when an investigation starts, when an ADR's evidence is questioned, or when a decision-flipping claim cannot be settled. Owns "how much is enough" and the optional notes document.

## The sufficiency test

Evidence is sufficient when every claim that could flip the chosen option is settled. Nothing else is required.

Per option, answer three questions and stop:

| Question | Evidence that answers it | Typical read |
|---|---|---|
| Can it work here? | The mechanism's prerequisites exist in this codebase — an API, a hook, a schema field, a deployment capability | 2–5 locations |
| What breaks when it does? | The failure path: timeout, duplicate, partial write, retry, rollback | 1–3 flows |
| What does it cost to get there? | Changes, downtime, new infrastructure, operational load | Change list, not a full trace |

A claim outside these three is breadth. Breadth is optional; it becomes required only when the user or a downstream consumer asks a question that depends on it.

## Claim classes

| Class | Rule |
|---|---|
| **Decision-flipping** | Verify against the primary source before adoption. Cited `file:line` in the ADR. |
| **Supporting** | Cite the location you read; no second read required. |
| **Background** | State it, tag **inferred**, and name what would confirm it. |

One decision-flipping claim left **unverified** blocks adoption unless the ADR states what would settle it and the user accepts the risk explicitly.

## Confidence tags

| Tag | Meaning | How it is earned |
|---|---|---|
| **verified** | Read the source and confirmed the behaviour | A read, a run, or a cited measurement |
| **inferred** | Reasoned from verified facts, not observed | Name the premise it rests on |
| **unverified** | Needs a read or a measurement | Name the one action that would settle it |

Tags appear only on claims the decision rests on. A document with a tag on every sentence has moved the bookkeeping, not reduced it.

## Verification depth

| Blast radius of the claim | Depth | Who |
|---|---|---|
| One option's feasibility, reversible choice | Check the cited `file:line` in-session | The session that drafted the ADR |
| The chosen option's load-bearing claim | Full verification of that claim against primary sources | An independent seat when dispatched; in-session when not |
| Cross-area constraint, or a decision other areas depend on | Full verification plus a search for contradicting evidence | Independent seat |

Verification is per claim, never per document. A blanket "looks right" is not a verdict.

## Anti-patterns

| Anti-pattern | Why it fails | Move |
|---|---|---|
| A ledger with IDs for every sentence | Bookkeeping the decision never reads; the ADR still cites nothing | Cite `file:line` at the claim in the ADR |
| Investigating the whole area "for completeness" | Cost scales with area size, not decision risk | Stop at the sufficiency test |
| A second document restating the first | Two owners for one claim; both drift | One claim, one home |
| Confidence tags everywhere | The reader cannot tell what matters | Tag decision-flipping claims only |
| "No evidence found" with no next step | Blocks the reader without an action | State the searched scope and what would settle it |

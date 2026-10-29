# Example: Re-Challenging After Investigation Contradicts an Accepted Claim

**Scenario**: The checkout spike was accepted, then the checkout area's evidence map contradicted a constraint the user had accepted. The gate re-opens on the affected claims only — never on the whole scope.

Applies **re-challenge-the-ask**.

## Input / Context
- **Accepted in round 1**: goal = reduce first-token latency on web checkout; scope = one repo, one area; constraint = "no queue in the checkout path".
- **Evidence map**: `CheckoutQueue.kt:41` already publishes to an internal queue; `CheckoutService.kt:88` awaits it synchronously before rendering.
- **Trigger named**: evidence contradicts a stated constraint.

## Findings, affected claims only
| # | Dimension | Finding | Material? |
|---|---|---|---|
| 1 | Conflict | A queue exists and is awaited — "no queue" is false as written | Yes — changes which options are compared |
| 2 | Ambiguity | "no queue" may have meant "no *new* queue" | Yes — decides whether the queue options survive |
| 3 | Scope | The other two areas are untouched by this evidence | No — settled, do not re-open |

## Output — narrowed round 2

**Q1 · Conflict · blocking** — the constraint does not match the code.
  A) Read it as "no *new* queue" — the existing awaited queue stays, options unchanged
  B) Drop the constraint — queue-based options re-enter the comparison
  C) Constrain the outcome instead — any option may use the existing queue, none may add infrastructure
Recommendation: C — the recorded tickets point at first-token cost, and the awaited queue is that cost; C keeps your real limit without hiding the cause.
Default if unanswered: none — a constraint belongs to the user, never to the agent's reading.

## User response
"Q1: C, that's what I meant."

## Result

| Item | Value |
|---|---|
| Gate state | `ACCEPTED` |
| Restated constraint | "No new infrastructure; the existing awaited queue may be changed" |
| Artifact update | `scope.md` — the false constraint is rewritten in place; git holds the history |
| Unaffected claims | Not re-opened — round 1 answers stand |
| Rounds used | 2 of 2 |

Validation: the trigger was named before re-opening; only the two affected claims were re-opened; one question, narrower than round 1; the corrected constraint replaces the old one rather than being appended.

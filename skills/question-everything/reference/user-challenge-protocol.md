# User Challenge Protocol (Intake Gate)

Use with **challenge-the-ask**. Gate states and the question budget live in **intake-gate**; this file owns the loop details.

## Rounds

| Round | When | Budget |
|---|---|---|
| **1 — pre-accept** | Before a scope, plan, or dispatch | ≤3 material questions |
| **2 — post-evidence** | After investigation or an answered sub-question | ≤3, narrower than round 1 |

Round 2 fires only on a **re-challenge-trigger**. At the round cap, accept with assumptions and say so.

## Question order

1. Blocking questions first — the ones that change the split or the options.
2. Non-blocking questions last, each with a default, so the user can skip the whole batch.
3. Stop as soon as the next step is decidable; completeness is not the goal.

## Batch rules

- One message, ≤3 numbered questions, each self-contained.
- No nested or compound questions — split them into separate items or drop one.
- Never re-ask what the user already answered or what the repo records.
- Re-open a settled answer only when new evidence contradicts it, and say what changed.

## Tone

- Challenge the claim, never the person.
- Name what is already clear before the gap: "The goal is clear; the metric is not."
- Phrase ambiguity as your own uncertainty: "I read this two ways."
- Every question ends in a recommendation the user can accept with one word.

## Gate transitions

| State | Transition |
|---|---|
| `ACCEPTED` | No material finding survives |
| `ACCEPTED-WITH-ASSUMPTIONS` | Defaults were taken; each is labeled |
| `BLOCKED` | A blocking question has no safe default — ask, then re-run |

- A one-sentence, single-decision request with no conflict passes on a restatement.
- A user "just do it" is a waiver: record `ACCEPTED-WITH-ASSUMPTIONS` and keep the labeled defaults.

## Assumption lifecycle

1. Label every default `Assumption (user-accepted, unverified)`.
2. Hand it to the calling skill's artifact — never leave it in conversation only.
3. Never promote it to fact without evidence.
4. When evidence contradicts one, it becomes a re-challenge trigger.

## Ownership

- The gate runs in the **calling session** — user dialogue is single-threaded.
- A dispatched sub-agent returns open questions upward; it never asks the user.
- The gate **replaces** an existing confirmation step; never add a second checkpoint.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| Ten-question interrogation | ≤3 material questions per round |
| A question with no options | 2–3 options plus a recommendation |
| Asking what the repo answers | Read the artifact first, then ask |
| Proceeding silently on a vague answer | `ACCEPTED-WITH-ASSUMPTIONS` plus labels |
| Grilling a one-sentence request | Restate and accept |
| Presenting push-back as clarification | Label it **push back** |
| Keeping assumptions in conversation | Write them into the owning artifact |

## Checklist

- [ ] Gate state recorded, and no work accepted before it.
- [ ] Round and question counts within budget.
- [ ] Every assumption labeled and handed to the owning artifact.
- [ ] A trivial request took the fast path.

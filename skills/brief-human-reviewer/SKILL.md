---
name: brief-human-reviewer
description: Brief a human before they confirm AI-produced artifacts; an orientation route into the code, a stated prediction, a falsifiable self-check, and a recorded skip. Use when presenting artifacts for confirmation, pacing a lagging reviewer, or briefing a new code area. Not for intake gates or one-line confirmations.
---

<when-to-use-this-skill>
- An artifact set (findings pair, ADR batch, solution document, plan, review report) is presented for the user's confirmation
- The user's review pace lags artifact production, or they confirm without reading
- A comprehension signal must be recorded distinctly from acceptance — a skipped read is `waived`, not passed
- The reviewer is new to the code area, so conclusions need a route into the code before they can be judged
- Do NOT load for the intake gate that accepts a request before work starts, a one-line confirmation, or to summarize an artifact the user already owns
</when-to-use-this-skill>

<knowledge>

<reviewer-bottleneck>
The reviewer's bottleneck is the **model**, not the conclusions. A conclusion they cannot re-derive is a claim taken on trust, and a confirmation taken on trust is not a review — it is a receipt.

Production outruns comprehension because an artifact carries answers and skips the route into the code that would let the reviewer check them. Speed is the symptom, not the cause.

Explanation volume does not fix this: more prose is the commodity the reviewer cannot absorb. Four moves fix it — route, prediction, self-check, dose.
</reviewer-bottleneck>
<calibration>
Detect the reviewer's footing per area. Never assume a beginner globally: over-explaining a codebase the reviewer wrote is a cost, not a kindness.

| Footing | Briefing |
|---|---|
| Authored the area | No route; prediction plus self-check only |
| Familiar area | 2–3 stops; no mechanism explanation |
| New area | 3–5 stops with what to notice; full sequence |
| New to the domain | Elicit a prediction before the first artifact and let the route carry the vocabulary |

Read the signal, do not ask for a self-rating: names the files unprompted, corrects a claim, or asks about a mechanism absent from the artifact → move one row up. Asks what a file does, or accepts every claim → move one row down.
</calibration>
<comprehension-moves>

| Move | Shape | Cost | Skip when |
|---|---|---|---|
| **Route** | 3–5 `file:line` stops in reading order, each `mechanism — what to notice` | 5–10 lines | Reviewer authored the area |
| **Prediction** | "Before I show you: what do you expect breaks?" then reveal your read | 2 lines | No live hypothesis to test |
| **Self-check** | One claim falsifiable in 2 minutes: act, expected result, wrong-if | 3 lines | No code claim behind the artifact |
| **Dose** | One unit per turn; route delivered before the heavy artifact | Restructures delivery | The artifact is a single small unit |

Move order is fixed: route → prediction → the checkpoint's existing question. A self-check rides after the route whenever the artifact rests on a code claim.
</comprehension-moves>
<dose-control>
- Present one unit per turn — one area's pair, one ADR batch, one document. Never bundle several behind one question.
- Deliver the route before the heavy artifact: the reviewer reads while the work finishes, which is the real answer to a pace mismatch.
- Keep the briefing to ≤15 lines above the artifact. Longer replaces reading with reading about reading.
- The artifact stays the payload; the briefing is a route into it, never a summary of it.
</dose-control>
<checkpoint-boundaries>
Scope: the intake gate is owned by `clarify-request`; restated here only as a boundary, never as a second copy of its rules.

| Axis | Owner | Returns |
|---|---|---|
| Accept the **request**, before work | the intake gate | `ACCEPTED` / `ACCEPTED-WITH-ASSUMPTIONS` / `BLOCKED` |
| Brief the **review**, once an artifact exists | this skill | `reviewed` / `waived` per unit |

- The two never share a message: the gate precedes work, the briefing follows an artifact.
- `ACCEPTED` belongs to the gate. Reusing it here would give one word two owners; `reviewed` records comprehension, never permission.
- A briefing rides inside an existing confirmation checkpoint — never a new pause, never a second checkpoint for one decision.
- Questioning doctrine and tone stay with the gate; this skill adds none.
- A dispatched sub-agent returns its route alongside the artifact in its single return and never prompts the user; the orchestrator composes the briefing.
</checkpoint-boundaries>
<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Composing a briefing message | Literal skeleton, field order, ceilings | [reference/review-briefing-skeleton.md](reference/review-briefing-skeleton.md) |
| A findings pair on code claims reaches confirmation | Route plus self-check, full sequence | [examples/findings-pair-review.md](examples/findings-pair-review.md) |
| An ADR batch is confirmed without a read | `waived` recording, trust statement | [examples/adr-batch-review-waived.md](examples/adr-batch-review-waived.md) |
| The reviewer authored the area | Fast path, no route | [examples/authored-area-fast-path.md](examples/authored-area-fast-path.md) |
</context-loading-guide>
</knowledge>
<capabilities>

<brief-before-review>
**Objective**: Turn a confirmation checkpoint into a review the reviewer can actually perform.

Outcome, confirmable by an observer: before the question, the reviewer holds a route into the code, has stated an expectation, and knows one claim they can falsify.

1. Size the unit per **dose-control** — one area, one ADR batch, one document.
2. Calibrate per **calibration**; read footing from the session, never assume it.
3. Plan the route per **plan-orientation-route** when the artifact rests on code claims and the reviewer did not author the area.
4. Deliver route, then prediction, then the checkpoint's **existing** question — never a question of your own.
5. Exchange the artifact's conclusion for the reviewer's expectation before revealing your read; a prediction the reviewer never states teaches nothing.

May decide: which moves to use, stop count, wording. Must decide: whether the artifact needs a route and which claim is load-bearing. Must not decide: replacing the checkpoint's question, or skipping the briefing to save tokens on a large artifact.

Failure modes: a route that walks the artifact instead of the code; a briefing longer than the artifact's own summary; stops that only repeat the artifact's citations; a new question where the checkpoint already had one.

Gate: the checkpoint message carries route, prediction, and the original question in that order, within **dose-control**'s ceiling.
</brief-before-review>
<plan-orientation-route>
**Objective**: Give the reviewer 3–5 stops that rebuild the mechanism the artifact reports on.

1. Choose stops that carry the mechanism the decision turns on — where state lives, where it changes, where it is read — not the files the artifact cites most. When the artifact already carries an orientation section or a `Start here` pointer, extend it into the stops and agree with it; never contradict it or build a second navigation artifact.
2. Order by dependency: each stop assumes only what the previous ones established.
3. Write each stop as `path:line-range — mechanism — what to notice`. A stop with no "notice" is a citation, not a route.
4. Verify every path and range resolves and covers the mechanism; a misleading route is worse than none.
5. Cap at 5 stops, 2 for a familiar area, none for an authored one.

Failure modes: a changelog of touched files; a stop at a barrel, index, or re-export; ranges so wide the reader notices nothing; a stop list that mirrors the artifact's own section order.

Gate: every stop resolves, each carries a notice, and the count matches the reviewer's **calibration** row.
</plan-orientation-route>
<design-self-check>
**Objective**: Give one claim the reviewer can falsify themselves in under two minutes.

1. Pick a load-bearing claim whose failure would change the decision — not the easiest one to state.
2. State the check as an action the reviewer performs: open a path and range, run a search or command, read one output.
3. Name the expected result and the wrong-if, so the reviewer knows what falsifies it.
4. Keep it to one check; two only when they probe different mechanisms.
5. Prefer a check that could fail — one that cannot is reassurance, not verification.

Failure modes: "review the logic in X" with no action or expectation; a check that restates the artifact's own text; a check needing a build, a long run, or credentials the reviewer may lack.

Gate: one action, one expected result, one wrong-if, under two minutes.
</design-self-check>
<record-review-state>
**Objective**: Record comprehension distinctly from acceptance.

1. Ask for the signal inside the checkpoint: which stops the reviewer opened, and whether their prediction matched.
2. Record `reviewed` when the reviewer reports reading or answering; record `waived` when they decline or say "just proceed".
3. `waived` never blocks the work and never becomes `reviewed`; carry it where the unit's status already lives, so a rubber stamp stays visible.
4. Never record `reviewed` without the reviewer's own answer — an unanswered signal is `waived`, said aloud.
5. On `waived`, name once the claim the reviewer is now trusting unread, without pressure.

Failure modes: inferring `reviewed` from silence; blocking work to force a read; keeping the state in conversation only; treating `waived` as a defect to argue about.

Gate: every unit carries a state, and every state traces to the reviewer's own words.
</record-review-state>
</capabilities>
<rules>
<rule>When an artifact set reaches a confirmation checkpoint, apply **brief-before-review** before the question is asked.</rule>
<rule>When the reviewer authored the area, or the checkpoint confirms a single small item, skip the route and keep prediction plus self-check.</rule>
<rule>When the checkpoint already carries a question, brief into it — never add a pause, a round, or a second checkpoint for the same decision.</rule>
<rule>When the artifact rests on a code claim the reviewer cannot verify from the artifact alone, apply **plan-orientation-route**.</rule>
<rule>When one claim's failure would change the decision, apply **design-self-check**.</rule>
<rule>When the reviewer confirms without reading, apply **record-review-state** and record `waived`, never `reviewed`.</rule>
<rule>Never restate the intake gate's states, tone, or question budget — it owns request acceptance; this skill owns review comprehension.</rule>
<rule>Never ask the user from inside a dispatched sub-agent; the orchestrator composes every briefing from the route the sub-agent returned.</rule>
</rules>

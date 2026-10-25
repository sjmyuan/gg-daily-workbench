---
name: question-everything
description: Challenge unverified claims from a user or an agent with questions, options, and verification. Use when challenging a vague request, re-challenging after evidence conflicts, questioning, validating, or verifying a result.
---

<when-to-use-this-skill>
- User hands over a request, spike brief, or issue report that must be made decidable before work is accepted
- The request is ambiguous, overloaded, or has several plausible readings — and the user needs options plus a recommendation
- Investigation evidence contradicts an accepted goal, constraint, or vocabulary and the request must be re-challenged
- User asks to question or challenge a result returned by an agent or sub-agent
- User asks to verify a returned result before accepting it — run the question → verify → accept/requestion loop
- A result will be consumed downstream (decision, commit, merge, release) and being wrong is costly
- Two agents or sub-agents return conflicting results and a resolution is needed
- User asks to validate the correctness, completeness, or clarity of a returned result
- Inside a multi-step pipeline — question or verify a sub-agent result before it is accepted downstream
- Do NOT load for a clear single-decision request, plain ADR drafting, solution-doc writing, or code investigation — `draft-adr`, `write-solution-doc`, and `investigate-code` handle those
</when-to-use-this-skill>

<knowledge>

<skeptic-mindset>
Treat every returned result and every user-supplied request as an unverified claim. Default to suspicion; trust is earned through questioning and independent verification. Never accept a request or a result because it is confident, detailed, or from a capable-looking source.
</skeptic-mindset>

<questioning-targets>
Two targets share one doctrine — restate, probe, prioritize, close — and differ in what closes a challenge:

| Target | Evidence that settles it | Closer | Who runs it |
|---|---|---|---|
| **Request** (user-supplied) | The user's intent, plus repo state and prior artifacts | A recorded decision | The calling session only |
| **Result** (agent-supplied) | Primary sources — code, docs, data, logs | A per-challenge verdict | A NEW evidence-matched agent |

A request has no primary source: clarify it or push back, never "verify" it.
</questioning-targets>

<intake-gate>
Accept a request only through a gate with three states:

| State | Meaning | Proceed? |
|---|---|---|
| `ACCEPTED` | No material ambiguity, or the user answered it | Yes |
| `ACCEPTED-WITH-ASSUMPTIONS` | Ambiguity remains; a stated default is taken | Yes — label each default `Assumption (user-accepted, unverified)` |
| `BLOCKED` | A material ambiguity has no safe default | No — ask, then re-run the gate |

Budget: ≤3 material questions per round, ≤2 rounds, then accept with assumptions and say so. Every question carries 2–3 options, a recommendation, and a default. A one-sentence, single-decision request passes on a restatement alone. Protocol: **reference/user-challenge-protocol.md**.
</intake-gate>

<re-challenge-triggers>
Re-open the gate after evidence arrives only on a named trigger: evidence contradicts a stated constraint; a goal term maps to two code realities; the reported symptom's cause is elsewhere; evidence makes the stated scope disproportionate; two areas' evidence disagree. Re-open the affected claims only, narrower than round 1.
</re-challenge-triggers>

<questioning-dimensions>
Question results across six dimensions: **Completeness** (missing paths/cases), **Correctness** (accuracy vs. primary sources), **Ambiguity** (vague wording), **Consistency** (self-contradiction), **Evidence** (claims backed by sources), **Assumptions** (silent premises). Load [reference/questioning-dimensions.md](reference/questioning-dimensions.md) for the per-dimension rubric.
</questioning-dimensions>

<verification-principles>
Verification decides whether a challenged result may be accepted. Principles: **independence** (no pre-written verdict), **primary sources** (code, docs, data, logs — not the result), **traceability** (one verdict per challenge), **fresh instances** (a NEW agent whenever dispatching), **evidence-matched verifiers** (code → `code-investigator`; non-code → a NEW producer-type agent), and **depth by blast radius** (skip structure, fidelity-check synthesis, single pass for new facts, full loop only for load-bearing decisions). Cap: **2 rounds**; surface residual uncertainty. Full rules: **reference/verification-protocol.md**.
</verification-principles>

<brief-context>
Every verifier brief carries known context — established `file:line`, the settled-vs-open split, and searched-negatives — so it starts from evidence, not zero. The context is non-exhaustive; the verifier may go beyond it. Template: **reference/verification-protocol.md**.
</brief-context>

<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Clarifying a request before accepting it | Intake dimensions, materiality test, question format | [reference/intake-dimensions.md](reference/intake-dimensions.md) |
| Running or exiting the intake gate | Gate states, round cap, tone, assumption labeling | [reference/user-challenge-protocol.md](reference/user-challenge-protocol.md) |
| Seeing a vague request challenged with options | Worked 3-question gate | [examples/challenging-a-vague-request.md](examples/challenging-a-vague-request.md) |
| Seeing a post-investigation re-challenge | Trigger, narrowed round 2, artifact update | [examples/re-challenging-after-investigation.md](examples/re-challenging-after-investigation.md) |
| Seeing a worked questioning pass on a returned result | End-to-end example of raising prioritized challenges only | [examples/raising-challenges.md](examples/raising-challenges.md) |
| Seeing a worked verification round that accepts | Verification accept example | [examples/confirming-result.md](examples/confirming-result.md) |
| Seeing a worked contradict + reinvestigate round | Verification contradict example (two rounds) | [examples/contradicting-result.md](examples/contradicting-result.md) |
</context-loading-guide>

</knowledge>

<capabilities>

<challenge-the-ask>
**Objective**: Turn an ambiguous request into an accepted one — material ambiguities resolved or recorded as labeled assumptions.

1. Restate the request in one sentence, in the user's own words, and label what you had to infer.
2. Load [reference/intake-dimensions.md](reference/intake-dimensions.md).
3. Split each claim into goal, scope, constraints, success criteria, and non-goals.
4. Probe each claim across the intake dimensions; label a finding **clarify** (the user was unclear) or **push back** (the user is clear but evidence disagrees).
5. Keep only material findings — a different answer would change the split, the options compared, the done criteria, or the investigation budget.
6. Order by impact; keep the top 3 per round.
7. Ask them as one batch: each with 2–3 options, a recommendation with its evidence, and a default.
8. Record each answer; re-ask only what is still undecidable — max 2 rounds.
9. Set the gate state per **intake-gate**, and hand the accepted assumptions to the calling skill for recording in its own artifact.
10. Apply **re-challenge-triggers** when new evidence arrives; re-open only the affected claims.
11. Validate: every question carried options plus a recommendation; no material finding was dropped unrecorded; each remaining ambiguity is labeled `Assumption (user-accepted, unverified)`; a trivial request took the fast path.
</challenge-the-ask>

<question-the-result>
**Objective**: Apply a skeptic's lens to a returned result and produce concrete, prioritized challenges.

1. Load [reference/questioning-dimensions.md](reference/questioning-dimensions.md).
2. Restate the result's key claims so each challenge targets one specific claim, never the result as a whole.
3. Probe each claim against the six dimensions using the rubric's questions.
4. Formulate each challenge using the rubric's output format — the claim questioned, the dimension, why it is suspect, and a satisfactory answer.
5. Prioritize by impact — what breaks if the claim is wrong, and how plausible the error is.
6. Output the challenge list ordered by priority.
7. If no challenge survives, state that the result passes initial questioning.
8. Validate the output: each challenge names exactly one claim, states its dimension, explains why it is suspect, and defines a satisfactory answer.
9. Fix any validation failure before presenting.
</question-the-result>

<verify-sub-agent-results>
**Objective**: Run the verification loop on a returned result — challenge, verify, and accept or repair — so only verified results are handed back to the caller.

1. Load [reference/verification-protocol.md](reference/verification-protocol.md).
2. Apply **question-the-result** to raise prioritized challenges on the returned result.
3. Route each material challenge to an **evidence-matched verifier** — `code-investigator` for code claims, otherwise a NEW agent of the producer's type — never the original instance — carrying the known context per **brief-context** and verifying it against primary sources.
4. If no evidence-matched verifier is available, verify each challenge directly against primary sources.
5. Collect per-challenge verdicts (AGREE / DISAGREE / UNCERTAIN), each traceable to its challenge and citing its primary source.
6. Apply the protocol's Traps list to the collected verdicts before comparing.
7. Accept when every material verdict is AGREE.
8. If any material verdict is DISAGREE, dispatch a NEW evidence-matched agent to repair the affected work (code facts → `code-investigator`; documents → the producer's type), then confirm only the changed claims. On UNCERTAIN, tag the claim unverified and surface it — no further round.
9. Cap the loop at **2 rounds** — verify once, repair once, confirm only the changed claims.
10. At the cap, present both versions and the residual uncertainty to the user — never silently pick one.
11. Hand the verified result back to the caller for synthesis only after verification.
</verify-sub-agent-results>

</capabilities>

<rules>
<rule>When a user hands over a request, spike brief, or issue report, apply **challenge-the-ask** before any work is accepted — a clear request passes on the restatement alone.</rule>
<rule>When investigation evidence contradicts an accepted goal, constraint, or vocabulary, apply **challenge-the-ask** on the affected claims only.</rule>
<rule>Never run **challenge-the-ask** from a dispatched sub-agent — user dialogue belongs to the calling session.</rule>
<rule>When the user asks to question, challenge, or act as a skeptic toward an agent- or sub-agent-returned result, apply **question-the-result**.</rule>
<rule>When the user asks to validate the correctness, completeness, or clarity of a returned result, apply **question-the-result**.</rule>
<rule>When the user asks to verify or accept a returned result before using it, apply **verify-sub-agent-results**.</rule>
<rule>When a result will be consumed downstream and being wrong is costly, apply **question-the-result**, then **verify-sub-agent-results** before the result is accepted.</rule>
<rule>When two agents or sub-agents return conflicting results, apply **question-the-result** to each, then **verify-sub-agent-results** to resolve the conflict.</rule>
<rule>When a sub-agent result will be consumed downstream, or two returned results conflict, apply **verify-sub-agent-results**.</rule>
</rules>

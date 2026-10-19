---
name: question-everything
description: Question and verify agent-reported information like a skeptic — raising challenges and running the verification loop. Use when questioning, challenging, validating, or verifying a returned agent or sub-agent result.
---

<when-to-use-this-skill>
- User asks to question or challenge a result returned by an agent or sub-agent
- User asks to verify a returned result before accepting it — run the question → verify → accept/requestion loop
- A result will be consumed downstream (decision, commit, merge, release) and being wrong is costly
- Two agents or sub-agents return conflicting results and a resolution is needed
- User asks to validate the correctness, completeness, or clarity of a returned result
- Inside a spike pipeline (via `conduct-spike`) or a delivery pipeline (inconsistent results via `orchestrate-feature-delivery`) — question or verify sub-agent results before acceptance
- Do NOT load for plain ADR drafting, solution-doc writing, or code investigation — use `draft-adr`, `write-solution-doc`, or `investigate-code` instead
</when-to-use-this-skill>

<knowledge>

<skeptic-mindset>
Treat every returned result as an unverified claim. Default to suspicion; trust is earned through questioning and independent verification. Never accept a result because it is confident, detailed, or from a capable-looking agent.
</skeptic-mindset>

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
| Seeing a worked questioning pass on a returned result | End-to-end example of raising prioritized challenges only | [examples/raising-challenges.md](examples/raising-challenges.md) |
| Seeing a worked verification round that accepts | Verification accept example | [examples/confirming-result.md](examples/confirming-result.md) |
| Seeing a worked contradict + reinvestigate round | Verification contradict example (two rounds) | [examples/contradicting-result.md](examples/contradicting-result.md) |
</context-loading-guide>

</knowledge>

<capabilities>

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
<rule>When the user asks to question, challenge, or act as a skeptic toward an agent- or sub-agent-returned result, apply **question-the-result**.</rule>
<rule>When the user asks to validate the correctness, completeness, or clarity of a returned result, apply **question-the-result**.</rule>
<rule>When the user asks to verify or accept a returned result before using it, apply **verify-sub-agent-results**.</rule>
<rule>When a result will be consumed downstream and being wrong is costly, apply **question-the-result**, then **verify-sub-agent-results** before the result is accepted.</rule>
<rule>When two agents or sub-agents return conflicting results, apply **question-the-result** to each, then **verify-sub-agent-results** to resolve the conflict.</rule>
<rule>When verifying sub-agent results inside a spike pipeline (via `conduct-spike`) or an inconsistent delivery result (via `orchestrate-feature-delivery`), apply **verify-sub-agent-results**.</rule>
</rules>

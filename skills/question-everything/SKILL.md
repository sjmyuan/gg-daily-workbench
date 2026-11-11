---
name: question-everything
description: Verify results returned by an agent: challenge each claim against primary sources and route it to an evidence-matched verifier. Use when questioning, validating, repairing, resolving conflicts, or before a decision.
---

<when-to-use-this-skill>
- A result returned by an agent or sub-agent must be checked before it is consumed downstream (decision, commit, merge, release)
- A returned result reads confident and detailed but no claim has been corroborated against primary sources
- Two agents or sub-agents return conflicting results and one must be chosen
- A returned result must be validated for correctness, completeness, or clarity before acceptance
- A repair is needed after a DISAGREE verdict, with only the changed claims re-confirmed
- Do NOT load to accept a user-supplied request — no primary source exists to check it against; `clarify-request` owns the intake gate
- Do NOT load for plain ADR drafting, solution-doc writing, or code investigation — `draft-adr`, `write-solution-doc`, and `investigate-code` own those
</when-to-use-this-skill>

<knowledge>

<skeptic-mindset>
Treat every returned result as an unverified claim.
Default to suspicion; trust is earned through independent questioning and verification.
Never accept a result because it is confident, detailed, or from a capable-looking source.
</skeptic-mindset>

<result-doctrine>
A result **has** primary sources — code, docs, data, logs — so it is verified, never merely clarified.
A **request** has none, so it is clarified, never verified.
Same word "challenge", opposite target: a result's **claims**, a request's **reading**. Two rules follow:

- **Independence**: the producing instance never verifies its own work; a NEW evidence-matched agent closes every material challenge.
- **Traceability**: one verdict per challenge, each citing its primary source.

A user-supplied request is the opposite case — it has no primary source and closes when nothing material is left to ask, not on a verdict. That target belongs to `clarify-request`.
</result-doctrine>

<questioning-dimensions>
Question results across six dimensions: **Completeness**, **Correctness**, **Ambiguity**, **Consistency**, **Evidence**, **Assumptions**.
The per-dimension rubric is [reference/questioning-dimensions.md](reference/questioning-dimensions.md).
</questioning-dimensions>

<verification-principles>
Verification decides whether a challenged result may be accepted. **Independence** and **traceability** hold per **result-doctrine**; four more principles apply:

| Principle | Rule |
|---|---|
| **Primary sources** | Code, docs, data, logs — never the result itself. |
| **Fresh instances** | A NEW agent on every dispatch. |
| **Evidence-matched verifiers** | Code → `code-investigator` (or the closest code-reading agent); non-code → a NEW producer-type agent. |
| **Depth by blast radius** | Skip structure; fidelity-check synthesis; single pass for new facts; full loop only for load-bearing decisions. |

Full rules: **reference/verification-protocol.md**.
</verification-principles>

<brief-context>
Every verifier brief carries known context so the verifier starts from evidence, not zero.
Carry established `file:line`, the settled-vs-open split, and searched-negatives.
The context is non-exhaustive; the verifier may go beyond it.
Template: **reference/verification-protocol.md**.
</brief-context>

<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Raising challenges on a returned result | Six-dimension rubric, challenge output format, prioritization, quality bar | [reference/questioning-dimensions.md](reference/questioning-dimensions.md) |
| Running an accept, repair, or contradict round | Verdict vocabulary, traps list, round cap, brief template | [reference/verification-protocol.md](reference/verification-protocol.md) |
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
3. Apply the rubric to every claim.
4. If no challenge survives, state that the result passes initial questioning.
5. Validate:
   - Each challenge names exactly one claim, states its dimension, explains why it is suspect, and defines a satisfactory answer.
   - The set meets the rubric's quality bar.
6. Fix any validation failure before presenting.
</question-the-result>

<verify-sub-agent-results>
**Objective**: Run the verification loop on a returned result — challenge, verify, and accept or repair — so only verified results are handed back to the caller.

1. Load [reference/verification-protocol.md](reference/verification-protocol.md).
2. Apply **question-the-result** to raise prioritized challenges on the returned result.
3. Route each material challenge to an evidence-matched verifier — never the original instance.
4. Match the verifier to the evidence: code claims → `code-investigator` (or the closest code-reading agent); non-code → a NEW agent of the producer's type.
5. Carry the known context per **brief-context** with every brief.
6. If no evidence-matched verifier is available, verify each challenge directly against primary sources.
7. Collect per-challenge verdicts (AGREE / DISAGREE / UNCERTAIN), each traceable to its challenge and citing its primary source.
8. Apply the protocol's **Comparison rules** and repair loop — verdict handling, round cap, and residual uncertainty stay there.
9. In a dispatched sub-agent, return both versions and the repaired claims, with sources, to the caller — never address the user.
10. Validate:
   - Every material challenge has a verdict citing a primary source.
   - No verdict came from the producing instance.
   - The round count is within the protocol's cap.
   - Residual uncertainty is stated rather than implied.
11. Hand the verified result back to the caller for synthesis only after validation.
</verify-sub-agent-results>

</capabilities>

<rules>
<rule>When a returned result will be consumed downstream and being wrong is costly, apply **question-the-result**, then **verify-sub-agent-results** before it is accepted.</rule>
<rule>When two agents or sub-agents return conflicting results, apply **question-the-result** to each, then **verify-sub-agent-results** to resolve the conflict.</rule>
<rule>When the user asks to question, challenge, validate, or verify a returned result, apply **question-the-result**, adding **verify-sub-agent-results** when acceptance is required.</rule>
<rule>Never verify a result in the agent that produced it — a NEW evidence-matched verifier closes every material challenge.</rule>
<rule>Never apply this skill to a user-supplied request — it has no primary source and belongs to `clarify-request`'s intake gate.</rule>
</rules>

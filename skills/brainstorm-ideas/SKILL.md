---
name: brainstorm-ideas
description: Facilitate structured brainstorming that turns an idea into a traceable, actionable plan. Use when brainstorming, defining goals, exploring challenges, generating, evaluating, prioritizing, refining, iterating, or deciding what to do next.
---

<when-to-use-this-skill>
- User wants to brainstorm a rough idea into a concrete, actionable plan
- User wants to define goals or explore challenges for an idea
- User wants to generate, evaluate, or prioritize ideas
- User wants to refine an idea into a stronger, more focused form
- User wants a second round on a plan — deepen, combine, or pivot
- User wants to decide what to investigate or focus on next after a round of work (e.g., a completed investigation)
</when-to-use-this-skill>

<knowledge>
<brainstorming-principles>
- Great ideas come from asking the right questions, not just producing answers
- Challenging assumptions and visual organization reveal connections and gaps
- Evaluation and prioritization matter as much as generation
</brainstorming-principles>
<questioning-protocol>
- Ask 2–4 questions per phase, only where the answer changes the plan
- Ask one question at a time and wait for the response; batch them only when the user asks
- Provide possible answers or examples with each question; follow up when an answer is vague
- Stop a phase once its output is decidable and verifiable
</questioning-protocol>
<facilitation-techniques>
- Use the user's preferred language; default to the language of their request
- Keep a casual, conversational tone using "we" language
- Use "what if" and "how might we" to explore possibilities
- Use examples and analogies; keep suggestions practical and feasible
- Open each result with a one-line plain summary; define any term the user has not used
</facilitation-techniques>
<adaptive-pacing>
Match session depth to idea maturity and user energy. Details: [reference/adaptive-pacing.md](reference/adaptive-pacing.md)
</adaptive-pacing>
<idea-generation>
Generate 5–7 diverse ideas using thinking techniques and present them as a mind map. Details: [reference/idea-generation.md](reference/idea-generation.md)
</idea-generation>
<idea-evaluation>
Score ideas across value, feasibility, differentiation, scope, and impact. Details: [reference/idea-evaluation.md](reference/idea-evaluation.md)
</idea-evaluation>
<challenging-techniques>
Stress-test ideas with devil's-advocate techniques. Details: [reference/challenging-ideas.md](reference/challenging-ideas.md)
</challenging-techniques>
<plan-output-format>
End the session with a traceable, actionable plan. Details: [reference/plan-output-format.md](reference/plan-output-format.md)
</plan-output-format>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Running a session on a new, unformed idea | End-to-end walkthrough of the full session | [examples/full-session-example.md](examples/full-session-example.md) |
| Improving a rough existing idea with clear gaps | Walkthrough applying capabilities selectively | [examples/refining-existing-idea.md](examples/refining-existing-idea.md) |
| Brainstorming a process or writing improvement, not a product | Full-session walkthrough on a writing topic | [examples/concise-document-writing.md](examples/concise-document-writing.md) |
| Running a second round on a refined idea | Walkthrough of round-2 iteration and the updated plan | [examples/iterating-on-a-plan.md](examples/iterating-on-a-plan.md) |
| Deciding what to investigate next after a completed investigation | Focused walkthrough from findings to a next-step plan | [examples/deciding-next-after-investigation.md](examples/deciding-next-after-investigation.md) |
</context-loading-guide>
</knowledge>

<capabilities>
<facilitate-session>
**Objective**: Run a structured brainstorm from idea to actionable plan.
1. Set the session mode per **reference/adaptive-pacing.md**.
2. State the contract: question budget, plan shape, stop or skip anytime.
3. Gather the idea or draft.
4. When a draft exists, extract the clear parts and note the gaps.
5. Apply **clarify-idea**.
6. Apply **identify-goals**.
7. Apply **explore-challenges**.
8. Apply **generate-ideas**.
9. Apply **evaluate-ideas**.
10. Apply **challenge-ideas**.
11. Apply **refine-idea**.
12. Apply **compile-actionable-plan** and present the final plan.
13. Offer **iterate-session** to deepen, combine, or pivot.
</facilitate-session>
<clarify-idea>
**Objective**: Produce a plain-language statement of the user's idea.
1. Restate the idea from the request in one or two sentences; ask the user to correct it.
2. Ask who or what it is for, what it solves, and its current state.
3. Probe unstated assumptions about audience, approach, and scope.
4. Challenge vague statements by asking for concrete examples or success metrics.
5. Confirm the corrected idea before proceeding.
</clarify-idea>
<identify-goals>
**Objective**: Define the primary objectives and success criteria.
1. Ask what the user wants to achieve with the idea.
2. Ask how they will know it succeeded.
3. Ask which objective matters most when several exist.
4. Summarize the goals; check each carries a success signal.
</identify-goals>
<explore-challenges>
**Objective**: Surface the obstacles the idea faces.
1. Ask what challenges or obstacles the user foresees.
2. Ask about risks, constraints, and dependencies.
3. Ask what could cause the idea to fail.
4. Present the challenge list; check each carries an impact.
</explore-challenges>
<generate-ideas>
**Objective**: Produce a diverse set of candidate ideas.
1. Generate **5–7 diverse ideas** per **reference/idea-generation.md**.
2. Present the ideas as a mind map per **reference/idea-generation.md**.
3. List the candidates worth scoring; check the set spans at least three techniques.
</generate-ideas>
<evaluate-ideas>
**Objective**: Objectively score and prioritize the surviving candidates — risks belong to **challenge-ideas**.
1. Evaluate each idea across the dimensions per **reference/idea-evaluation.md**.
2. Prioritize the ideas with a simple framework (effort vs impact, MoSCoW).
3. Present the scored and prioritized ideas; confirm the priorities.
</evaluate-ideas>
<challenge-ideas>
**Objective**: Attack the prioritized ideas as devil's advocate before refining.
1. Play devil's advocate on the top ideas per **reference/challenging-ideas.md**.
2. Question scope creep and push for simpler, more focused solutions.
3. Suggest MVP or phased approaches when scope is too large.
4. Present the stress-tested ideas; check the top risk has a mitigation.
</challenge-ideas>
<refine-idea>
**Objective**: Consolidate the surviving ideas into a single refined idea.
1. Combine the strongest elements from the top ideas.
2. Ask which remaining risk or gap the idea still does not cover.
3. Ask which elements are essential versus nice-to-have.
4. Present the refined idea; check each essential element serves a goal or challenge.
</refine-idea>
<compile-actionable-plan>
**Objective**: Deliver a structured, traceable, actionable plan.
1. Summarize the refined idea in one sentence per **reference/plan-output-format.md**.
2. Record every decision and dropped idea with its reason.
3. Map each confirmed challenge to its impact and mitigation.
4. Write numbered next steps: verb + object, output, done-when, and the goal or risk it serves.
5. Verify the plan against the quality bar; fix every failed criterion before presenting.
6. Present the plan in plain language; ask the user to confirm or amend.
</compile-actionable-plan>
<iterate-session>
**Objective**: Run a second round — deepen, combine, or pivot.
1. Offer round 2 and let the user choose a direction.
2. Re-apply only the phases that direction needs; update the plan and check it against the quality bar.
3. Cap at 1–2 rounds; repeat only if the user asks.
</iterate-session>
</capabilities>

<rules>
<rule>When the user wants to brainstorm an idea into an actionable plan, use **facilitate-session**.</rule>
<rule>When the user provides a rough idea, use **facilitate-session** and apply capabilities only for the gaps.</rule>
<rule>When the user requests one phase in isolation, apply that capability directly.</rule>
<rule>When a plan exists and the user wants to go further, apply **iterate-session**.</rule>
</rules>

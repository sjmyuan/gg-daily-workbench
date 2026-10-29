---
name: clarify-request
description: Clarify a request before accepting it: restate the ask, itemize inferences, ask material questions with options, record assumptions. Use when accepting, clarifying, or re-challenging a request, brief, issue report, or rework ask, or recording accepted assumptions.
---

<when-to-use-this-skill>
- A request, spike brief, issue report, or rework ask is about to be accepted and its reading is uncorroborated
- The ask leaves its goal, scope, success criteria, constraints, or conflict with a prior decision open
- An ask must be made decidable without over-questioning — options, a recommendation, and a default per question
- Investigation evidence contradicts an accepted goal, constraint, or vocabulary, and the accepted claim must be re-challenged
- Accepted defaults must be labeled and handed to the artifact that owns them
- Do NOT load to check an agent's returned result — `question-everything` owns result verification
</when-to-use-this-skill>

<knowledge>

<request-doctrine>
Treat every user-supplied request as an **unverified claim**. Never accept one because it looks confident, detailed, or familiar.

A request has **no primary source** — it cannot be "verified", only made decidable. The closer is **nothing material left to ask**: the agent judges the ask sufficient to act, and every inference it still holds is recorded as a labeled assumption. A request is either **clarified** (the user was unclear) or **pushed back** on (the user is clear, the evidence disagrees) — clarify the ask, not the person. The gate runs in the **calling session only**; a dispatched sub-agent returns open questions upward and never asks the user.
</request-doctrine>

<intake-gate>
Every request produces an **acceptance record**; no work starts without one:

| Field | Content |
|---|---|
| Restatement | The ask in the user's own words |
| Inferred | Every reading the ask left open, itemized |
| Questions | Rounds asked, and what each answer settled |
| Gate state | `ACCEPTED` · `ACCEPTED-WITH-ASSUMPTIONS` · `BLOCKED` |
| Accepted assumptions | One `Assumption (user-accepted, unverified)` line per default |

The gate is decided by the **inference count**, never by self-judged ambiguity:

| Inferred | Action |
|---|---|
| Nothing — goal, scope, and done criteria all stated | `ACCEPTED`: state the restatement and proceed |
| Anything | Show the restatement plus the inference list, then ask the top 3 as options — never proceed on a private reading |

`ACCEPTED-WITH-ASSUMPTIONS` is legal only after the list was shown; `BLOCKED` means a material question has no safe default. Budget: ≤3 material questions per round, ≤2 rounds, then accept with assumptions and say so. Every question carries 2–3 options, a recommendation with its evidence, and a default. Protocol: **reference/request-clarification-protocol.md**.
</intake-gate>

<acceptance-record>
The caller owns the record and writes it into the artifact it already maintains — a spike scope, a plan charter, a delivery index brief, an investigation answer, or the session itself when the work produces no artifact. Never a second checkpoint, never a new doc.

- Label every default `Assumption (user-accepted, unverified)` and carry it until evidence or the user settles it.
- A record with a gate state but no inference list is evidence the gate did not run.
- Promote an assumption to fact only with evidence, cited at its source.
</acceptance-record>

<re-challenge-triggers>
Re-open the gate after evidence arrives only on a named trigger: evidence contradicts a stated constraint; a goal term maps to two code realities; the reported symptom's cause is elsewhere; evidence makes the stated scope disproportionate; two areas' evidence disagree. Re-open the affected claims only, narrower than round 1, and say what changed.
</re-challenge-triggers>

<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Probing a request across goal, scope, success criteria, constraints, and conflict | Intake dimensions, minimum probe, materiality test, question format | [reference/intake-dimensions.md](reference/intake-dimensions.md) |
| Running or exiting the gate, or recording assumptions | Gate states, round cap, tone, batch rules, assumption lifecycle | [reference/request-clarification-protocol.md](reference/request-clarification-protocol.md) |
| Seeing a vague request challenged with options | Worked 3-question gate with inference list | [examples/challenging-a-vague-request.md](examples/challenging-a-vague-request.md) |
| Seeing **re-challenge-the-ask** narrow a round after evidence | Trigger, affected claims only, record rewritten in place | [examples/re-challenging-after-investigation.md](examples/re-challenging-after-investigation.md) |
</context-loading-guide>

</knowledge>

<capabilities>

<clarify-the-ask>
**Objective**: Turn a user-supplied ask into an accepted one — material ambiguities resolved or recorded as labeled assumptions, with the record handed to the owning artifact.

1. Restate the request in the user's own words and itemize every inference it required.
2. Load [reference/intake-dimensions.md](reference/intake-dimensions.md) and probe the five minimum dimensions; close each one by naming what closed it.
3. Split the ask into goal, scope, constraints, success criteria, and non-goals.
4. Label each finding **clarify** (the user was unclear) or **push back** (the user is clear but evidence disagrees).
5. Keep only material findings — a different answer would change the split, the options compared, the done criteria, or the budget.
6. Order by impact; keep the top 3 per round.
7. Ask them as one batch: each with 2–3 options, a recommendation with its evidence, and a default.
8. Record each answer; re-ask only what is still undecidable — max 2 rounds.
9. Set the gate state per **intake-gate** and hand the record to the caller, which writes it per **acceptance-record**.
10. Validate: the inference list was shown before any work started; every question carried options plus a recommendation; no material finding was dropped unrecorded; each remaining ambiguity is labeled `Assumption (user-accepted, unverified)`; the record names the artifact that owns it.
</clarify-the-ask>

<re-challenge-the-ask>
**Objective**: Re-open an accepted ask on new evidence — narrower than round 1, rewriting the record in place.

1. Name the trigger per **re-challenge-triggers**; no named trigger → do not re-open.
2. List the affected claims only — the ones the evidence contradicts — and state what changed.
3. Restate each affected claim in the user's words beside what the evidence now says; label it **push back**.
4. Ask the narrowed questions for the affected claims only (≤3); every unchanged answer stands.
5. Rewrite the record in place per **acceptance-record** — no appended history, no version markers.
6. Validate: the trigger is named; untouched claims were not re-opened; total rounds across both capabilities ≤2; the record still names its owning artifact.
</re-challenge-the-ask>

</capabilities>

<rules>
<rule>When a request, brief, issue report, or rework ask must be accepted before any work starts, apply **clarify-the-ask**.</rule>
<rule>When evidence contradicts an accepted goal, constraint, or vocabulary, apply **re-challenge-the-ask** on the affected claims only — never re-run round 1.</rule>
</rules>

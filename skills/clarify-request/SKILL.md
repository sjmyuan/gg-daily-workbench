---
name: clarify-request
description: Clarify a request before accepting it: restate it, list inferences, ask material questions, record assumptions. Use when an uncorroborated request, brief, issue, or rework ask must be accepted or re-challenged.
---

<when-to-use-this-skill>
- A request, spike brief, issue report, or rework ask is about to be accepted and its reading is uncorroborated
- The ask leaves its goal, scope, success criteria, constraints, or conflict with a prior decision open
- An ask must be made decidable without over-questioning — options and a recommendation per question, a default when non-blocking
- Investigation evidence contradicts an accepted goal, constraint, or vocabulary, and the accepted claim must be re-challenged
- Accepted defaults must be labeled and handed to the artifact that owns them
- Do NOT load to check an agent's returned result — `question-everything` owns result verification
</when-to-use-this-skill>

<knowledge>

<request-doctrine>
Treat every user-supplied request as an **unverified claim**. Never accept one because it looks confident, detailed, or familiar.

A request has **no primary source** — it cannot be "verified", only made decidable. The closer is **nothing material left to ask**: the agent judges the ask sufficient to act.

Every inference the agent still holds is shown back. Only one that can change a decision is admitted as a labeled assumption.

A request is either **clarified** (the user was unclear) or **pushed back** on (the user is clear, the evidence disagrees) — clarify the ask, not the person.

The gate runs in the **calling session only**. A dispatched sub-agent returns open questions upward and never asks the user.
</request-doctrine>

<intake-gate>
Every request produces an **acceptance record**; no work starts without one:

| Field | Content |
|---|---|
| Restatement | The ask in the user's own words |
| Inferred | Every reading the ask left open, itemized |
| Questions | Rounds asked, and what each answer settled |
| Gate state | `ACCEPTED` · `ACCEPTED-WITH-ASSUMPTIONS` · `BLOCKED` |
| Accepted assumptions | One `Assumption (user-accepted, unverified)` line per **admitted** default |

The gate is decided by the **inference count**, never by self-judged ambiguity:

| Inferred | Action |
|---|---|
| Nothing — goal, scope, and done criteria all stated | `ACCEPTED`: state the restatement and proceed |
| Anything | Show the restatement plus the inference list, then ask the material questions as options — never proceed on a private reading |

`ACCEPTED-WITH-ASSUMPTIONS` is legal only after the list was shown; `BLOCKED` means a material question has no safe default.
Budget: ≤3 material questions per round, ≤2 rounds, then accept with assumptions and say so.
Every question carries 2–3 options and a recommendation with its evidence; a default only for non-blocking questions.
Protocol: **reference/request-clarification-protocol.md**.
</intake-gate>

<acceptance-record>
The caller owns the record and writes it into the artifact it already maintains — a spike scope, a plan charter, a delivery index brief, an investigation answer, or the session itself.
Never a second checkpoint, never a new doc.

- Label every admitted default `Assumption (user-accepted, unverified)` and carry it until evidence or the user settles it.
- A record with a gate state but no inference list is evidence the gate did not run.
- Promote an assumption to fact only with evidence, cited at its source.
- Delete an assumption the moment no decision depends on it, the user settles it, or evidence verifies it — no changelog.
</acceptance-record>

<assumption-admission>
An accepted assumption is a **decision premise**, not a reading of the ask. Persist one only when all three hold:
- **Not obtainable** — if the repo, an artifact, or a measurement can settle it, it is an investigation target recorded as a Gap where the evidence lives, not an assumption.
- **Decision-relevant** — changing it would change a driver, the options compared, the chosen option, the done criteria, or the area/problem split.
- **User-held or safely defaulted** — the user stated it or accepted the default; never a private reading.

Every other inference is still shown in the inference list; it is resolved or dropped with its reason, not persisted. Removal test at every write: if deleting the line changes no decision, delete it.
</assumption-admission>

<re-challenge-triggers>
Re-open the gate after evidence arrives only on a named trigger:
- Evidence contradicts a stated constraint.
- A goal term maps to two code realities.
- The reported symptom's cause is elsewhere.
- Evidence makes the stated scope disproportionate.
- Two areas' evidence disagree.

Re-open the affected claims only, narrower than round 1, and say what changed.
</re-challenge-triggers>

<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Probing a request across goal, scope, success criteria, constraints, and conflict | Intake dimensions, minimum probe, materiality test, question format, quality bar | [reference/intake-dimensions.md](reference/intake-dimensions.md) |
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
5. Apply the reference's materiality test and question format — drop every finding a different answer would not change.
6. Ask the surviving questions as one batch, ordered by impact, within the gate's question budget.
7. Record each answer; re-ask only what is still undecidable, within the gate's round budget.
8. Set the gate state per **intake-gate** and hand the record to the caller, which writes it per **acceptance-record**.
9. Validate:
   - The inference list was shown before any work started.
   - Every question carried options plus an evidence-backed recommendation, and a default only when non-blocking.
   - No material finding was dropped unrecorded.
   - Each decision-changing default is labeled `Assumption (user-accepted, unverified)` and none is obtainable from code.
   - The batch meets the reference's question quality bar.
   - The record names the artifact that owns it.
</clarify-the-ask>

<re-challenge-the-ask>
**Objective**: Re-open an accepted ask on new evidence — narrower than round 1, rewriting the record in place.

1. Name the trigger per **re-challenge-triggers**; no named trigger → do not re-open.
2. List the affected claims only — the ones the evidence contradicts — and state what changed.
3. Restate each affected claim in the user's words beside what the evidence now says; label it **push back**.
4. Ask the narrowed questions for the affected claims only, within the gate's question budget; every unchanged answer stands.
5. Rewrite the record in place per **acceptance-record** — no appended history, no version markers.
6. Validate:
   - The trigger is named.
   - Untouched claims were not re-opened.
   - Rounds stay within the gate's budget.
   - The record still names its owning artifact.
</re-challenge-the-ask>

</capabilities>

<rules>
<rule>When a request, brief, issue report, or rework ask must be accepted before any work starts, apply **clarify-the-ask**.</rule>
<rule>When evidence contradicts an accepted goal, constraint, or vocabulary, apply **re-challenge-the-ask** on the affected claims only — never re-run round 1.</rule>
<rule>Never start work on a private restatement — show the inference list, then proceed.</rule>
<rule>Never ask the user from a dispatched sub-agent — return the open questions upward.</rule>
</rules>

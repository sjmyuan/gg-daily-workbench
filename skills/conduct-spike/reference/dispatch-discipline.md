# Dispatch Discipline

Cross-cutting rules for every spike sub-agent dispatch. Brief contract: **reference/dispatch-briefs.md**; dispatch pattern and verification: **reference/multi-agent-orchestration.md**.

## Model routing

Choose the least powerful model that can do the unit; **state it explicitly** — an omitted model inherits the orchestrator's session model, often the most expensive.

| Work unit | Tier |
|---|---|
| Area session (phases 1–3: tracing, synthesis, decision) | Capable |
| Solution-doc compilation (synthesis of verified material) | Standard–capable |
| Verification (per `question-everything`) | Scaled to claim risk — cheap for mechanical claims, mid for subtle ones |
| Re-investigation after a DISAGREE / UNCERTAIN | Evidence-matched to the challenged claim; one tier above the original analyst |

- Specify the model in every dispatch brief.
- The area session runs on one model for all its phases; do not downgrade a resumed phase below the model that produced the evidence.
- A unit that stays stuck is escalated to a more capable model — never retried unchanged on the same model.
- A re-investigation brief carries the verification result (open challenges + verdicts) — never retry a unit blind.

## Resuming an area session

- Keep a session ledger in the orchestrator — area → session, phase returned, receipt — until the area's ADRs are accepted; it is the only handle the next phase needs.
- Resume the same analyst session for the next phase; the phase receipt and the written artifacts are the durable state.
- When the session cannot be resumed, re-dispatch the same agent type with the phase's artifacts plus the prior receipt — never with a blank brief.
- A resumed phase inherits the prior phase's evidence; it never re-investigates to rebuild context.
- Close the session only when its area's pair and ADRs are accepted; a later sync or rework starts a new session from the artifacts.

## Waiting on sub-agents

- Never poll with short timeouts; never sit in one silent, open-ended wait.
- While local work remains (scope-map updates, preparing the next brief), keep working — results arrive on their own.
- When genuinely idle, wait in bounded stretches (five to ten minutes where the platform allows).
- Between stretches, reconcile live children: list them and chase any that finished without reporting.

## No sub-agents from workers

A dispatched worker never spawns sub-agents — not helpers, and never a verifier. The orchestrator owns every verification seat; a worker-spawned verifier duplicates it at full cost and its verdict counts for nothing. A unit too large for one pass reports back so the orchestrator splits or re-briefs it.

## Availability and fallback

Before dispatching, detect the platform's agent mechanism and map each unit to the closest available type — the table in **reference/multi-agent-orchestration.md** names the preferred agents.

| Situation | Fallback |
|---|---|
| No `spike-area-analyst` | Ask the user; else run the area session in-session with the same brief and phases, keeping verification independent |
| No suitable agent for a unit | Ask the user how to proceed; else run the unit in-session with the same brief and verification — never skip the unit |
| Verification with no evidence-matched agent | Verify in-session against primary sources per `question-everything`'s protocol |
| No explicit model routing | Ask the user once, or use the cheapest capable default and state it in the brief |

## Common rationalizations

| Excuse | Reality |
|---|---|
| "The sub-agent will find the scope itself" | It cannot see the orchestrator's context; it re-derives the scope by searching, at full price. |
| "A short brief is a cheap brief" | The brief saves tokens; the re-search spends them back many times over. A missing digest is a cost, not a saving. |
| "The path is enough — it can read the file" | A path forces a re-read and a re-derivation; the digest is what removes the re-scan. |
| "It can grep for the entry point" | That search already ran. Forward the location, not the task. |
| "Single area / single ADR — dispatching is overhead" | Context preservation is the goal, not parallelism; the area is still dispatched and its phases run in one session. |
| "Split the area across agents — each phase is simpler" | The split serializes a live evidence map at every hop; findings compilation becomes a re-read and ADR nuance dies in the digest. |
| "Re-dispatch phase 2 with a blank brief" | The prior receipt is the session's state; a blank re-run pays for the investigation twice. |
| "The analyst was thorough — verification is redundant" | Verification is the gate; the producing session is never reused as the verifier. |
| "Just the evidence doc is enough" | An area's findings always travel as a pair — human doc + evidence doc; never one alone. |
| "I'll verify it myself in this session" | Dispatch a NEW evidence-matched agent; verify in-session only when none exists. |
| "The producer's own agent type can verify its doc" | A pair or ADR still makes code claims — those need a code-reading verifier (`code-investigator`). |
| "Re-investigate with the same analyst — it has context" | It anchors on its own output; verification and repair use a NEW instance. |
| "Every artifact needs a fresh verifier" | Depth scales with blast radius — synthesis docs get a fidelity check, not an evidence sweep. |
| "One more round will converge" | Past the 2-round cap the failure is structural — present both versions to the user. |
| "The worker spawned its own reviewer — extra assurance" | A duplicate seat; the orchestrator's verification is the gate. |
| "It's only a scope note — I'll edit the ADR directly" | Artifacts are written by their owning skill; bypassing it degrades them. |

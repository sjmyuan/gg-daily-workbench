# Dispatch Discipline

Cross-cutting rules for every spike sub-agent dispatch. Briefs: **reference/dispatch-briefs.md**; dispatch pattern: **reference/multi-agent-orchestration.md**.

## Context completeness

- **Inventory before writing**: every dispatch starts from an explicit list of what the orchestrator holds — user dialog, `scope.md`, prior results, its own reads and searches, resolved paths. A brief that omits an inventory item is incomplete, not concise.
- **Digest, don't just point**: pass the conclusion the orchestrator already reached (located `file:line`, settled claims, ruled-out searches) with the path, so the sub-agent acts instead of re-reading.
- **Feed the callee's gate**: fill the intake record (system, scope, depth, consumer) — an unfilled field becomes the sub-agent's exploration pass.
- **Forward the search log**: every returned unit's searched-negatives seed the next unit's **already searched** digest; a negative that is not forwarded is paid for twice.
- **Never let it hunt for inputs**: absolute paths with section anchors — a sub-agent searching the filesystem for its own inputs is a brief defect, not a sub-agent behavior.

## Model routing

Choose the least powerful model that can do the unit; **state it explicitly** — an omitted model inherits the orchestrator's session model, often the most expensive.

| Work unit | Tier |
|---|---|
| Investigation (multi-file tracing, call chains) | Capable |
| Findings-doc / solution-doc compilation (synthesis of verified material) | Standard |
| ADR drafting (evaluation + option detail) | Standard–capable |
| Verification (per `question-everything`) | Scaled to claim risk — cheap for mechanical claims, mid for subtle ones |
| Re-investigation after a DISAGREE / UNCERTAIN | Evidence-matched to the challenged claim; one tier above the original investigator |

- Specify the model in every dispatch brief.
- A unit that stays stuck is escalated to a more capable model — never retried unchanged on the same model.
- A re-investigation brief carries the verification result (open challenges + verdicts) — never retry a unit blind.

## Waiting on sub-agents

- Never poll with short timeouts; never sit in one silent, open-ended wait.
- While local work remains (scope-map updates, preparing the next brief), keep working — results arrive on their own.
- When genuinely idle, wait in bounded stretches (five to ten minutes where the platform allows).
- Between stretches, reconcile live children: list them and chase any that finished without reporting.

## No sub-agents from workers

A dispatched worker never spawns sub-agents — not helpers, and never a verifier. The orchestrator owns every verification seat; a worker-spawned verifier duplicates it at full cost and its verdict counts for nothing. A unit too large for one pass reports back so the orchestrator splits or re-briefs it.

## Availability and fallback

Before dispatching, detect the platform's agent mechanism and map each unit to the closest equivalent agent type (see **multi-agent-orchestration**).

- No suitable agent → ask the user how to proceed, or run the unit in-session with the same brief and verification — never skip the unit.
- Verification with no evidence-matched agent → verify directly against primary sources in-session (per `question-everything`'s protocol).

## Common rationalizations

| Excuse | Reality |
|---|---|
| "The sub-agent will find the scope itself" | It cannot see the orchestrator's context; it re-derives the scope by searching, at full price. |
| "A short brief is a cheap brief" | The brief saves tokens; the re-search spends them back many times over. A missing digest is a cost, not a saving. |
| "The path is enough — it can read the file" | A path forces a re-read and a re-derivation; the digest is what removes the re-scan. |
| "It can grep for the entry point" | That search already ran. Forward the location, not the task. |
| "Single area / single ADR — dispatching is overhead" | Context preservation is the goal, not parallelism; the unit is still dispatched. |
| "The investigator was thorough — verification is redundant" | Verification is the gate; the original instance is never reused. |
| "Just the evidence doc is enough" | An area's findings always travel as a pair — human doc + evidence doc; never one alone. |
| "I'll verify it myself in this session" | Dispatch a NEW evidence-matched agent; verify in-session only when none exists. |
| "The producer's own agent type can verify its doc" | A findings/ADR/solution doc still makes code claims — those need a code-reading verifier (`code-investigator`). |
| "Re-investigate with the same agent — it has context" | It anchors on its own output; dispatch a new instance. |
| "Every artifact needs a fresh verifier" | Depth scales with blast radius — synthesis docs get a fidelity check, not an evidence sweep. |
| "One more round will converge" | Past the 2-round cap the failure is structural — present both versions to the user. |
| "The worker spawned its own reviewer — extra assurance" | A duplicate seat; the orchestrator's verification is the gate. |
| "It's only a scope note — I'll edit the ADR directly" | Artifacts are written by their owning skill; bypassing it degrades them. |

# Sub-Agent Orchestration for Spikes

Dispatch task execution to sub-agents — investigation, findings-doc compilation, ADR drafting, and solution-doc compilation — **even when the spike has only a single task**. The primary goal is **preserving the orchestrating agent's context**: running a unit in the orchestrator spends its window on file reads, search output, and intermediate reasoning, crowding out the cross-state it must hold (scope, findings, decisions). Parallel speed is a secondary benefit.

| Capability | Agent | Applies skill | Brief template |
|---|---|---|---|
| Investigate | `code-investigator` | `investigate-code` | [investigation-brief.md](investigation-brief.md) |
| Compile findings docs | `findings-doc-writer` | `document-findings` | [findings-doc-brief.md](findings-doc-brief.md) |
| Draft problem ADRs (evaluate + draft) | `adr-writer` | `draft-adr` (full flow) | [adr-drafting-brief.md](adr-drafting-brief.md) |
| Compile solution doc | `solution-doc-writer` | `write-solution-doc` | [solution-doc-brief.md](solution-doc-brief.md) |

ADR drafting runs the `draft-adr` flow headlessly inside the `adr-writer` session: the orchestrator collects the drivers from the user, carries them in the brief, and the agent returns the ADR with a proposed chosen option for the orchestrator to confirm.

## Why dispatch even a single task

- **Context preservation (primary)** — the orchestrator keeps its window for synthesis; the sub-agent's reading, reasoning, and user dialog stay in its own context.
- **Speed (secondary)** — units dispatched together run concurrently.
- **Consistency** — one dispatch pattern for every spike; no separate single-task code path to maintain.

## Dispatching pattern

1. Identify independent work units — one per investigation area, or one per problem/ADR (batch a whole area's problems into one brief when they share its evidence), including a single unit.
2. Fill each unit's ready-to-fill brief from the table above, applying the brief contract — inventory, fill modes, intake record, evidence-map output, completeness check — per **reference/dispatch-briefs.md**.
3. Dispatch the briefs — all units concurrently when there are several; sub-agents operate independently and never communicate with each other.
4. Apply **reference/dispatch-discipline.md** — explicit model per brief, bounded waits, availability fallback, no worker-spawned sub-agents.
5. Collect results, including each unit's search log.
6. Verify each result at the depth below, keep the accepted material, and hand each area's verified evidence map to `compile-findings-doc` for recording in `docs/evidence-<area>.md`.
7. Feed each collected result forward: a later unit in the same round receives earlier results **inline**; the next round receives each unit's search log as its **already searched** digest.

A brief that carries only the goal and an output name is the failure mode this ordering prevents: the sub-agent cannot see the orchestrator's context, so it re-derives the scope, hunts for its own inputs, and repeats searches already run.

## Verifying returned results

Verify via `question-everything`'s **verify-sub-agent-results**, with depth set by blast radius — never by artifact count:

| Unit | Depth | What is verified |
|---|---|---|
| Investigation evidence | **Single pass** (default) | Material code claims, each against primary sources |
| Findings-doc compilation | **Fidelity** | IDs, counts, and `file:line` match the verified ledger; no evidence sweep |
| Solution-doc compilation | **Fidelity** | Fidelity to verified ADRs and evidence; no evidence sweep |
| ADR decision (load-bearing) | **Full loop** (cap 2) | Chosen-option fit plus any new code claims; verify → repair once → confirm changed claims |

- `code-investigator` verifies code claims; non-code claims go to a NEW instance of the producer's type. Never reuse the original instance.
- A fidelity check that finds a new `file:line` claim drops to a **single pass** on that claim.
- The re-dispatch brief carries the **verification result** (open challenges + verdicts) so the new agent resolves them instead of redoing settled work (see **reference/dispatch-briefs.md**).
- `UNCERTAIN` → tag the claim **unverified** in the evidence doc and surface it; never add a round to converge.

### Verification questions

Probe each material claim across six dimensions, ordered by impact × likelihood × scope:

| Dimension | Probes |
|---|---|
| **Completeness** | Missing branches, edge cases, fallbacks, downstream consumers |
| **Correctness** | Claim vs. code/docs/logs; accuracy of every cited `file:line` |
| **Ambiguity** | Vague nouns, unstated units, scope a second reader would read differently |
| **Consistency** | Self-contradiction, disagreement with other verified results |
| **Evidence** | Claims with no primary source; restatements passed off as sources |
| **Assumptions** | Silent premises that would invalidate the result if false |

Emit each surviving challenge as `**C<N> (<dimension>, <priority>)** — <claim>: <why suspect>. Satisfactory answer: <what closes it>.`
Verify only material (high/medium) challenges, capped at the top 3 by impact; note the rest without verifying.

**Independence** — dispatch a NEW agent matched to the evidence that settles the challenge, never the original producer. Give it claims and citations, never a pre-written verdict. No suitable agent → verify in-session against primary sources.

**Verdicts** — `AGREE` (holds, with source) · `DISAGREE` (corrected claim, with source) · `UNCERTAIN` (state what is missing).
All material `AGREE` → accept. Any `DISAGREE` → a new evidence-matched agent repairs the affected work, then confirm only the changed claims. Any `UNCERTAIN` → tag **unverified** and surface it; never add a round. At the 2-round cap, present both versions to the user.

**Traps** — a wholesale "looks fine" is not a verdict · verifying the result instead of per challenge · reusing the original instance · sending only the verdict back on repair · treating "same wording" as agreement · accepting a verdict with no cited source.

## When NOT to dispatch

- **Scope definition** stays in the orchestrating agent — it establishes the cross-state (goal, areas, problems) every brief depends on. All later steps dispatch; the ADR-drafting user dialog runs inside the dispatched sub-agent.
- **Single-task spikes are not exempt** — a single area, ADR, or document is still dispatched.

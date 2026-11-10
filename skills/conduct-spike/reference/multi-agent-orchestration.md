# Sub-Agent Orchestration for Spikes

Dispatch by **evidence axis**: one agent owns one area's whole chain — investigate → findings pair → ADRs — because those three phases share one evidence base. The solution document is a separate cross-area synthesis, and verification is a separate independent seat. The primary goal is **preserving the orchestrating agent's context**: running an area in the orchestrator spends its window on file reads, search output, and intermediate reasoning, crowding out the cross-state it must hold (scope, decisions, status). Parallel speed is a secondary benefit.

| Capability | Agent | Applies skill | Brief |
|---|---|---|---|
| Investigate (phase 1) | `spike-area-analyst` | `investigate-code` | [area-analyst-brief.md](area-analyst-brief.md) |
| Compile findings pair (phase 2) | `spike-area-analyst` | `document-findings` | [area-analyst-brief.md](area-analyst-brief.md) |
| Draft problem ADRs (phase 3) | `spike-area-analyst` | `draft-adr` (headless) | [area-analyst-brief.md](area-analyst-brief.md) |
| Compile solution doc | `solution-doc-writer` | `write-solution-doc` | [solution-doc-brief.md](solution-doc-brief.md) |

## Why one session per area

Splitting the chain across agents serializes a live evidence map at every hop:

- **Findings compilation is a projection, not a judgment** — a separate writer only re-reads the evidence the investigator just built. In one session that document is authored from memory; the orchestrator never re-serializes the map.
- **ADR nuance survives** — a fresh ADR writer receives only a "known locations" digest, so the reasoning about why an option is risky dies at the handoff. In one session it evaluates options against the evidence it gathered.
- **Gap closure is local** — a missing fact found during option evaluation becomes a targeted read and a new ledger row, instead of a return → re-brief → new investigator round trip.
- **The artifact is the contract** — phase receipts and written artifacts carry state, so the orchestrator holds only the cross-state and never the narrative.

The cost is that an area's phases run serially; parallelize by **phase across areas**, not by agent type. A single area is still dispatched — context preservation is the goal, not parallelism.

## Dispatching pattern

1. **Scope stays in the orchestrator** — it establishes the cross-state (goal, areas, problems, drivers) every brief depends on.
2. **One brief per area** per [area-analyst-brief.md](area-analyst-brief.md), carrying the phase stop and the complete context inventory.
3. **Phased dispatch** — the default: dispatch phase 1 to every area in parallel, verify and pause; resume each area for phase 2, verify and pause; then phase 3. **Batch** dispatch phases 1–3 in one brief only when the user waives the pauses between capabilities.
4. **Resume the same session** — continue the analyst's session for the next phase where the platform supports it; otherwise re-dispatch the same agent with the written artifacts plus the prior phase receipt. Never rebuild the evidence by re-investigating.
5. **Parallelize by phase** — all areas' phase 1 together, then all areas' phase 2, and so on.
6. **Collect and forward** — each later phase inherits the area's own artifacts and its prior receipt inline; the next area's brief inherits the searched-negatives digest.
7. **Verify before accepting** — see below; the producing session is never the verifier.

A brief that carries only the goal and an output name is the failure mode this ordering prevents: the sub-agent cannot see the orchestrator's context, so it re-derives the scope, hunts for its own inputs, and repeats searches already run.

## Verifying returned results

Verify via `question-everything`'s **verify-sub-agent-results**, with depth set by blast radius — never by artifact count:

| Returned unit | Depth | What is verified |
|---|---|---|
| Phase 1 evidence map | **Single pass** (default) | Material code claims, each against primary sources |
| Phase 2 findings pair | **Fidelity** | IDs, counts, and `file:line` match the verified ledger; no evidence sweep |
| Phase 3 ADR decision (load-bearing) | **Full loop** (cap 2) | Chosen-option fit plus any new code claims; verify → repair once → confirm changed claims |
| Solution doc | **Fidelity** | Fidelity to verified ADRs and evidence; no evidence sweep |

- `code-investigator` verifies code claims; non-code claims go to a NEW instance of the producer's type. Never reuse the producing `spike-area-analyst` session — it anchors on its own output.
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

- **Scope definition** stays in the orchestrating agent — it establishes the cross-state (goal, areas, problems) every brief depends on.
- **Verification** stays with the orchestrator's independent seat, never inside the producing session.
- **Single-task spikes are not exempt** — a single area is still one dispatched area session.

# Sub-Agent Orchestration for Spikes

Dispatch task execution to sub-agents — for investigation, findings-doc compilation, ADR drafting (including option evaluation via `draft-adr`), and solution-doc compilation — **even when the spike has only a single task**. A sub-agent is always available; the primary goal is **preserving the orchestrating agent's context**: running a task in the orchestrator consumes its context window with file reads, search output, and intermediate reasoning, crowding out the cross-cutting state it must hold (scope, findings, decisions). Parallel speed is a secondary benefit that applies automatically when multiple units are dispatched at once.

| Capability | Agent | Applies skill | Brief template |
|---|---|---|---|
| Investigate | `code-investigator` | `investigate-code` | Investigation brief — [investigation-brief.md](investigation-brief.md) |
| Compile findings docs | `findings-doc-writer` | `document-findings` | Findings-doc brief — [findings-doc-brief.md](findings-doc-brief.md) |
| Draft problem ADRs (evaluate + draft) | `adr-writer` | `draft-adr` (full flow) | ADR-drafting brief — [adr-drafting-brief.md](adr-drafting-brief.md) |
| Compile solution doc | `solution-doc-writer` | `write-solution-doc` (target-state) | Solution-doc brief — [solution-doc-brief.md](solution-doc-brief.md) |

Each capability's brief template lives in its own reference file (see the table above) — prepare the brief from it, then dispatch to the mapped agent. Whenever a brief carries an area's findings, pass **both** docs of its pair — `docs/findings-<area>.md` (human) and `docs/evidence-<area>.md` (evidence) — never one alone. Every capability is dispatched even for a single task (see below). ADR drafting runs the `draft-adr` flow — decision drivers → options → evaluation → compile-adr — **headlessly inside the `adr-writer` session**: the orchestrator collects the drivers from the user, carries them in the brief, and the agent returns the ADR with a proposed chosen option for the orchestrator to confirm.

## Why Dispatch Even a Single Task

- **Context preservation (primary)**: the orchestrator keeps its window for synthesis and orchestration; the sub-agent's reading, reasoning, and interactive user dialog (e.g., ADR evaluation) stays in its own context.
- **Speed (secondary)**: multiple units dispatched together run concurrently.
- **Consistency**: one dispatch pattern for all spikes — no separate single-task code path to maintain.

## Dispatching Pattern

1. Identify independent work units (one per investigation area, or one per problem/ADR — batching a whole area's problems into one brief when they share its evidence; including a single unit).
2. Inventory the orchestrator's own context before writing anything: the user's ask and answers, `scope.md`, prior units' returned results, its own reads and searches, resolved paths, and project conventions — then classify each item as **path**, **digest**, or **inline** per **reference/dispatch-briefs.md**.
3. For each unit, fill the capability's ready-to-fill brief (see the table above) per the **structured brief shape**; every inventory item lands in it, every path is absolute, and the callee intake record is filled. Run the **completeness check** in **reference/dispatch-briefs.md** — a brief that fails it is not dispatched.
4. Dispatch the briefs — all units concurrently when there are multiple, or the single unit on its own when there is one. Sub-agents operate independently and do not communicate with each other. Apply **reference/dispatch-discipline.md** — explicit model per brief, bounded waits, and no worker-spawned sub-agents.
5. Collect results from all sub-agents when they complete, including each unit's search log.
6. Verify each collected result via `question-everything`'s **verify-sub-agent-results** at the depth in **Verifying Returned Results** below. Review the accepted results for completeness and consistency across areas, then hand each area's verified evidence map to `compile-findings-doc`, which records it in the area's `docs/evidence-<area>.md` (see **reference/findings-document-guide.md**).
7. **Document-compilation briefs** (findings and solution docs) carry the full synthesis context per **reference/findings-doc-brief.md** / **reference/solution-doc-brief.md** — the orchestrator still reviews, validates, and presents the returned doc.
8. Feed each collected result forward: a later unit in the same round receives the earlier units' results **inline** (they are not artifacts yet), and the next round receives each unit's search log as its **already searched** digest.

A brief that carries only the goal and an output name is the failure mode this ordering exists to prevent: the sub-agent cannot see the orchestrator's context, so it re-derives the scope, hunts for its own input files, and repeats searches the orchestrator already ran.

## Verifying Returned Results

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
- Each verifier brief carries the known context — the intake record, established `file:line`, the settled-vs-open split, and searched-negatives.
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

## When NOT to Dispatch

- **Scope definition**: stays in the orchestrating agent — it establishes the cross-cutting scope (goal + areas and problems) that every dispatch brief depends on and sets up the spike. All later steps dispatch to a sub-agent; the ADR-drafting user dialog (drivers, options, evaluation) runs inside the dispatched sub-agent.
- **Single-task spikes are NOT exempt**: a single area, single ADR, or single document is still dispatched — context preservation is the goal, not parallelism.

## Platform Detection

Before dispatching, detect whether `code-investigator`, `findings-doc-writer`, `adr-writer`, and `solution-doc-writer` are available on the current platform; map each work unit to the closest equivalent agent type.

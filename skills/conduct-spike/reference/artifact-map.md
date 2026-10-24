# Spike → Delivery Artifact Map

One artifact, one question. The two pipelines meet by **reference**, never by copying content.

## Two planes

| Plane | Artifacts | Question | Owner |
|---|---|---|---|
| **Spike — knowledge** | `scope.md` · findings pair · ADRs · `solution.md` | Why, what exists, what was decided, what is the target? | `conduct-spike` and its owning skills |
| **Delivery — execution** | `index.md` · `context.md` · `plan.md` · `rework-<date>.md` | Where is the epic, why this cell, how is it executed? | orchestrator · planner · executor |
| **Record** | git / PR / CI | What happened, and can it be reproduced? | executor + forge |

## Artifact responsibilities

| Artifact | Answers | Owner | Lifetime | Never contains |
|---|---|---|---|---|
| `scope.md` | What is the spike solving, and how far is each area/problem? | `conduct-spike` | spike; updated in place | delivery features, cells, status, plans |
| `docs/findings-<area>.md` | What exists in this area today, for a human? | `document-findings` | current state | target state, decisions, claim IDs |
| `docs/evidence-<area>.md` | What do we claim, with what evidence and confidence? | `document-findings` | current state | decisions, target state, delivery status |
| `adrs/adr-*.md` | What did we decide, and why? | `draft-adr` | decision; versionless | investigation narrative, raw evidence, delivery status |
| `solution.md` | What is the target state? | `write-solution-doc` | target; versionless | current-state findings, delivery status |
| `index.md` | Where is the epic in delivery? | orchestrator | epic | why/how per cell, spike content copies |
| `context.md` | Why this cell, what must hold, what is unknown, how is done judged? | planner (charter); executor (state) | cell; survives reworks | steps, spike-artifact copies, logs |
| `plan.md` | How is this cell executed, in what order? | planner; executor updates status | frozen after execution | background, solution copies, cross-cell status |
| `rework-<date>.md` | What changed after delivery, and how is the delta executed? | planner; executor updates status | one file per rework | restated original plan, prior history |

## Dependency and change flow

```
SPIKE (knowledge)                         DELIVERY (execution)
scope.md ─ area/problem map              index.md ─ feature/cell state
   │                                          │
   ├─ findings-<area>.md (human)              ├─ context.md (cell charter)
   ├─ evidence-<area>.md (ledger)             ├─ plan.md (steps)
   ├─ adrs/adr-*.md (decisions)               └─ rework-<date>.md (delta)
   └─ solution.md (target state)
                    └──────── references ────────┘
```

- **Downward:** evidence → findings → ADR → solution → index decomposition → context → plan.
- **Backward:** a delivery-discovered fact enters at the evidence doc (via `document-findings` update), then propagates as above. Delivery docs record only the outcome and link.
- A delivery defect that changes no decision is an amendment/rework — it does not touch the spike chain.

## Handoff contract

Only these cross the boundary:

| From spike | To delivery |
|---|---|
| `scope.md` `Artifact root:` | Delivery base (`deliveries/<epic-name>/`) |
| `solution.md` + ADR paths + findings/evidence paths + `scope.md` | Index `## Spike References` |
| ADR paths per feature | Index feature table `ADRs` column |
| Cell-specific ADR / solution section / findings | `context.md` `## Pointers` |

Never copy a spike artifact into `index.md`, `context.md`, or `plan.md` — link it.

## Decomposition is not 1:1

| Spike | Delivery |
|---|---|
| Areas × problems (decisions) | Features × repos (deliverable slices) |
| A problem is a "How to …?" decision | A feature is a coherent, independently valuable slice |

- One feature may span several ADRs/areas.
- One ADR may drive several features/cells.
- One area may yield several features.
- The trace is **Feature → ADRs** and **Solution section → Feature**, not `Problem → Feature`.
- `scope.md` problems are not delivery tasks; `index.md` is not a spike status board.

## Edit ownership

| Artifact | Edited by | Never edited by |
|---|---|---|
| `scope.md`, findings pair, ADR, `solution.md` | `conduct-spike` and its owning skills (`document-findings`, `draft-adr`, `write-solution-doc`) | delivery agents |
| `index.md` | orchestrator | planner, executor, spike agents |
| `context.md` | planner (charter); executor (`State` / `Execution` / `Open concerns`) | orchestrator, spike agents |
| `plan.md`, `rework-<date>.md` | planner; executor updates status | orchestrator, spike agents |
| Code | executor | spike, orchestrator, planner |

## Change routing

| Trigger | Route |
|---|---|
| New current-state fact | `document-findings` update → ADR (if a decision is affected) → solution doc → index re-route |
| ADR decision change | `adr-writer` → `write-solution-doc` → **handle-adr-change** → re-plan / rework |
| Delivery defect, no decision change | **amend-plan** or **rework** — no spike edit |
| New option or new area | L3 spike via **triage-issue** |

## Where does this fact go?

1. What exists today? → `docs/evidence-<area>.md` (+ human findings doc)
2. A decision? → `adrs/adr-*.md`
3. Target state? → `solution.md`
4. Epic status or sequencing? → `index.md`
5. Why, invariants, unknowns, done criteria for one cell? → `context.md`
6. How/order for one cell? → `plan.md`
7. Post-delivery delta? → `rework-<date>.md`
8. Reproducible history? → git / PR / CI

## Do-not list

- `scope.md` never tracks delivery status; the index never lists spike problems as tasks.
- Findings never contain target state or decisions.
- ADRs never contain investigation narratives or raw evidence; they cite claim IDs.
- The solution doc never restates findings; it mirrors ADR decisions.
- The index never restates why/how; it references `context.md` / `plan.md`.
- Context never copies ADR/solution/findings content; it points.
- The plan never copies the solution; it cites it.
- No delivery agent edits a spike artifact; no spike agent edits a delivery artifact.

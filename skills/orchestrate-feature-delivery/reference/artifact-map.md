# Delivery Artifact Map

Scope: the delivery side of the two-plane split. The spike's artifact matrix and its
internal ownership belong to the spike skill; this copy carries only what delivery needs.

## Two planes

| Plane | Artifacts | Question |
|---|---|---|
| **Spike — knowledge** | `scope.md` · findings pair · ADRs · `solution.md` | Why, what exists, what was decided, what is the target? |
| **Delivery — execution** | `index.md` · `context.md` · `plan.md` · `rework-<date>.md` | Where is the epic, why this cell, how is it executed? |
| **Record** | git / PR / CI | What happened, and can it be reproduced? |

`index` = state · `context` = charter · `plan` = execution · `rework` = delta · git/PR = record.

## Handoff contract

Only these cross the boundary:

| From the spike | To delivery |
|---|---|
| `scope.md` `Artifact root:` | Delivery base (`deliveries/<epic-name>/`) |
| `solution.md` + ADR paths + findings/evidence paths + `scope.md` | Index `## Spike References` |
| ADR paths per feature | Index feature table `ADRs` column |
| Cell-specific ADR / solution section / findings | `context.md` `## Pointers` |

Never copy a spike artifact into `index.md`, `context.md`, or `plan.md` — link it by path.

## Decomposition is not 1:1

| Spike | Delivery |
|---|---|
| Areas × problems (decisions) | Features × repos (deliverable slices) |
| A problem is a "How to …?" decision | A feature is a coherent, independently valuable slice |

- One feature may span several ADRs/areas; one ADR may drive several features/cells.
- The trace is **Feature → ADRs** and **Solution section → Feature**, never `Problem → Feature`.
- `scope.md` problems are not delivery tasks; `index.md` is not a spike status board.

## Edit ownership

| Artifact | Edited by | Never edited by |
|---|---|---|
| Spike artifacts | the spike skill and its doc-owning skills | delivery agents |
| `index.md` | orchestrator | planner, executor, spike agents |
| `context.md` | planner (charter); executor (`State` / `Execution` / `Open concerns`) | orchestrator, spike agents |
| `plan.md`, `rework-<date>.md` | planner; executor updates status | orchestrator, spike agents |
| Code | executor | spike, orchestrator, planner |

## Where does this fact go?

1. What exists today, a decision, or a target state? → the spike artifacts, via their owning skill.
2. Epic status or sequencing? → `index.md`.
3. Why, invariants, unknowns, done criteria for one cell? → `context.md`.
4. How and in what order for one cell? → `plan.md`.
5. Post-delivery delta? → `rework-<date>.md`.
6. Reproducible history? → git / PR / CI.

## Do-not list

- `index.md` never restates why/how; it points to `context.md` / `plan.md`.
- `context.md` never copies ADR, solution, or findings content; it points.
- `plan.md` never copies the solution; it cites it.
- No delivery agent edits a spike artifact; no spike agent edits a delivery artifact.
- A delivery defect that changes no decision is an amendment or a rework — it never touches the spike chain.

# Write-Boundary Guide

Backs the **write-boundary** knowledge entry and the delivery write-boundary check. The orchestrator maintains delivery docs only — it never writes code or any file outside the delivery folder.

## Allowed vs forbidden writes

| May write — inside the delivery folder (`**/deliveries/**`) | Never write |
|---|---|
| `index.md` | code, config, tests, infrastructure, scripts, `plan.md` / `context.md` / `rework-<date>.md`, any file outside the delivery folder |

The delivery folder always carries a `deliveries/` path segment (`<base>/deliveries/<epic-name>/`), which anchors the boundary. The `plan.md` / `context.md` / `rework-<date>.md` files inside it are owned by the dispatched **planner** and **executor** — the orchestrator never writes them; gate findings go straight to the planner and the index tracks status only.

## Enforcement layers

| Layer | Where | Strength |
|---|---|---|
| `edit` permission — `"*": "deny"`, `"**/deliveries/**": "allow"` | Orchestrator agent (opencode) | Hard block |
| `task` allowlist — planner / executor / code-reviewer / spike-conductor / adr-writer / solution-doc-writer | Orchestrator agent (opencode) | Blocks unexpected agents |
| Write-boundary doctrine + rules | Skill and agent files (all platforms) | Intent |
| Boundary check (own-writes snapshot delta) | After each index write | Detection |

Copilot and Claude agent files have no permission layer — the doctrine and rules carry the boundary there.

## Boundary check (after every index write)

Audits **only the orchestrator's own writes** via a before/after snapshot — pre-existing or unrelated repo changes never trigger a stop.

1. Snapshot changed paths **before** the index write with a read-only command (e.g., `git status --porcelain`) in the repo containing the delivery folder.
2. Perform the index write.
3. Snapshot changed paths **after** the write with the same command.
4. Keep only the **delta** — paths new or modified since the before-snapshot; ignore everything already present.
5. Pass when the delta is empty or every delta path contains a `deliveries/` segment.
6. On any delta path outside it: stop, report only the offending delta paths, and ask the user to revert them before delivery continues.

Dispatched **planner** / **executor** agents own their writes and commit them; the orchestrator never audits their output. The delta also catches in-window shell writes — the compensating control for `bash: allow`.

## Implementation is delegated, never done here

Code changes are produced only by the dispatched **executor** (execute-plan); planning is delegated to the **planner**. When a plan or execution surfaces a change outside the delivery docs, dispatch the owning agent per **agent-dispatch** — never write it from the orchestrator.

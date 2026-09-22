# Write-Boundary Guide

Backs the **write-boundary** knowledge entry and the spike write-boundary check. A spike produces documented decisions, never production code — every write stays inside the spike folder.

## Allowed vs forbidden writes

| May write — inside the spike folder (`**/spikes/**`) | Never write |
|---|---|
| `scope.md`, `docs/findings-<area>.md`, `adrs/adr-*.md`, `solution.md` | code, config, tests, infrastructure, scripts, any file outside the spike folder |
| Throwaway diagrams embedded in spike markdown | prototypes, proof-of-concept code, or any executable artifact |

The spike folder always carries a `spikes/` path segment (`<base>/spikes/<spike-name>/`), which anchors the boundary.

## Enforcement layers

| Layer | Where | Strength |
|---|---|---|
| Path-scoped `edit` permission (allow `**/spikes/**`, deny the rest) | Spike-conductor agent | Hard block |
| Doc-scoped `edit` permission (allow `*.md`, deny the rest) | ADR/findings/solution writers | Hard block on non-docs |
| Write-boundary doctrine + rules | Skill and agent files | Intent |
| Brief Constraints + Report-back | Every dispatch brief | Intent, per dispatch |
| Boundary check (own-writes snapshot delta) | After each write capability | Detection |

Platforms without an agent permission layer rely on the doctrine and rules alone.

## Boundary check (after every write capability)

Audits **only the acting agent's own writes** via a before/after snapshot — pre-existing or unrelated repo changes never trigger a stop.

1. Snapshot changed paths **before** the write capability with a read-only command (e.g., `git status --porcelain`) in the repo containing the spike folder.
2. Perform the write capability.
3. Snapshot changed paths **after** the write with the same command.
4. Keep only the **delta** — paths new or modified since the before-snapshot; ignore everything already present.
5. Pass when the delta is empty or every delta path contains a `spikes/` segment.
6. On any delta path outside it: stop, report only the offending delta paths, and ask the user to revert them before the spike continues.

Pre-existing edits, unrelated files, and other tasks' changes are never judged. The delta also catches in-window shell writes — the compensating control for `bash: allow`.

## Recording implementation needs

A spike never implements. When the investigation concludes code, config, or tests must change:

1. Record the need as an **out-of-scope / next actions** note in `scope.md` (or the affected `solution.md` section).
2. Do not create a plan, prototype, or handoff artifact.
3. Tell the user to run `orchestrate-feature-delivery` — it drives the **planner** then the **executor** to touch code.

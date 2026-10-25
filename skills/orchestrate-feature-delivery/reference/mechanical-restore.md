# Mechanical Restore

Scope: the routing slice of the provenance doctrine. The planner owns the full
`Source` / `Equality` model and the plan shape; the orchestrator decides **mechanical
vs behavioral** and dispatches the rework; the executor proves equality.

## Rule

A request to revert, keep, restore, or copy asks for a **state**, not an implementation.
Its plan is not a TDD change and never regenerates equivalent code.

## Mechanical vs behavioral

| Request sounds like | Route |
|---|---|
| "revert", "undo", "roll back", "put it back" | mechanical — `Source: port` |
| "same as main", "sync with the base branch" | mechanical — `Source: base` |
| "keep it as is", "don't touch", "leave it" | mechanical — `Source: no-op` |
| "take it from PR #123", "restore the deleted function" | mechanical — `Source: port` |
| "do what billing-service does", "reuse that module" | mechanical — `Source: copy` |
| the result must *behave* differently | behavioral — a normal bug/feature rework |

Ask for the ref when the request names no source; never infer the baseline.
Prefer reverting commits over restoring a path when unrelated commits touched it.

## Source enum

| `Source` | Operation | Proof before commit |
|---|---|---|
| `no-op` | change nothing | `git status --porcelain -- <paths>` is empty |
| `base` | `git restore --source=<ref> -- <paths>` | `git diff --exit-code <ref> -- <paths>` |
| `port` | `git revert <commits>`, `git cherry-pick -n`, `git apply` | diff against `<ref>` limited to `<paths>` |
| `copy` | copy from an in-repo origin | origin path plus an explicit adaptation list |
| `edit` / `generate` | behavioral change | not a mechanical rework — use a normal plan |

## Orchestrator duty

1. Classify mechanical vs behavioral and state it, quoting the trigger verbatim.
2. Dispatch the **planner** to write a sibling `rework-<date>.md` carrying `Source`, `Ref` (a SHA or tag, never a moving branch), and `Equality`.
3. Keep `plan.md` frozen; the rework file is the delta.
4. The **executor** runs the git operation and records the equality proof; the orchestrator records only state.

## Refuse

- Regenerating code for a revert, keep, restore, or copy request.
- Restoring, then refactoring the result — an unrequested change that leaves the ref.
- Pinning a branch name as `Ref` — the branch moves; the target state becomes nondeterministic.
- Skipping validation for `no-op` — run the receipt and the tests.

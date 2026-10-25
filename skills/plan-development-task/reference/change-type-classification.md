# Change Type Classification

Used by **classify-change-type** and **plan-quality-checklist**.

Classify the request into one type; a mechanical target is detected first and routes to
**plan-mechanical-restore**.

| Signal | Type | Reasoning |
|---|---|---|
| "bug", "broken", "error", "exception", "not working", "incorrect", "wrong output", "failing", "regression" | **Bug Fix** | Something produces incorrect or unexpected results |
| "new", "add", "implement", "create", "support", "enhance", "extend", "feature", "capability" | **Feature** | New observable behavior is introduced |
| "refactor", "clean up", "restructure", "extract", "organize", "improve quality", "reduce debt", "split", "consolidate" | **Refactor** | Internal structure changes without behavior change |
| "poc", "proof of concept", "prove which option", "compare approaches", "validate option" | **POC** | An uncertain ADR option needs evidence — a standalone feature demonstrates it (see **plan-poc**) |

When unsure, ask: "Is the goal to fix something that's broken (bug), add new behavior (feature),
or restructure without changing behavior (refactor)?"

## Routing

| Type | Path |
|---|---|
| Mechanical (revert / restore / port / copy / no-op) | **define-scope** → **plan-mechanical-restore** |
| Bug Fix | **define-scope** → **plan-bug-fix** |
| Feature | **define-scope** → **plan-feature-implementation** |
| Refactor | **define-scope** → **plan-refactor** |
| POC | **plan-poc** |
| Restructure plus new behavior | **plan-refactor** first, then **plan-feature-implementation** |

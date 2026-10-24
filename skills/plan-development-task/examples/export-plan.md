# Example: Exporting a Confirmed Plan to Files

**Scenario**: A simple bug-fix plan has been confirmed by the user. **export-plan** persists it to a feature
folder as `plan.md` + `context.md` so **execute-plan** can carry it out. The single-repo workspace has no docs
home or convention, so `resolve-artifact-location` asks and the user confirms the repo root as the base.

**Applies**: **export-plan** · **doc-budgets**

## Confirmed Input

- Change type: **Bug Fix**
- Root cause confirmed; Scope Boundary ratified
- Branch/base recorded: `fix-null-pointer` / `main`

## Feature Folder

`<repo-root>/feature-implementations/fix-null-pointer-in-transformer/` (base = repo root, confirmed via `resolve-artifact-location`)

## plan.md

```markdown
## Scope Boundary
**May change**: `DataImportedHandler` null-guard behavior
**Expected files**: handler + its tests (advisory)
**Must not change**: transformer behavior, publisher behavior, other handlers

**TDD variant**: Full cycle — complex logic bug requires test-first safety.

1. **Prepare Environment** — branch `fix-null-pointer` off `main`; no overlapping dirt; deps installed; affected-area baseline passes
2. **Write tests** for null-safety in `DataImportedHandler`
3. **Confirm test failure (RED)** — fails, not errors, for the expected reason
4. **Fix code** — guard the null pointer on missing payload
5. **Verify fix** — all tests pass
6. **Clean up** unused code and tests
7. **Validate** linting, formatting, type-checking
```

## context.md

The charter: unique facts only, 40–60 lines (ceiling 8,000 chars / 120).

```markdown
# Context: fix-null-pointer-in-transformer (bug fix, repo)

**Outcome:** `DataImportedHandler` no longer crashes when the transform result is null on missing payload.

## Why

Outgoing events crash when the transform result is null. Root cause confirmed in the handler;
the transformer's contract is correct. Boundary: **plan.md** §Scope Boundary.

## Must hold

- No behavior change beyond the null guard.
- Existing tests stay green.

## Unknowns

- Other call sites may pass null — covered by the handler test matrix.

## Done means

| Criterion | Verification | Verdict rule |
|---|---|---|
| Missing payload no longer crashes | handler test suite | all pass |
| Transformer and publisher untouched | diff against `main` | no changes |

## Pointers

- `DataImportedHandler` — crash site
- `DataImportedHandlerTest` — existing suite to extend

## Open concerns

- — (none at planning time)

## State

| Field | Value |
|---|---|
| Active plan | `plan.md` |

## Execution

| Field | Value |
|---|---|
| Status | — (not executed) |
| Commits | — |
| PR | — |
| Test evidence | — |
| Review outcome | — |

## Reworks

| Date | Mode | Cell | Trigger | File | Status |
|---|---|---|---|---|---|
| — | — | — | — | — | — |
```

No TDD rationale, decisions, or branch metadata here — they live in `plan.md`.
The charter is ~55 lines and well under the 8,000-char ceiling.

## Save Location

Saved to `<repo-root>/feature-implementations/fix-null-pointer-in-transformer/`; the user can now invoke **execute-plan** to run it.

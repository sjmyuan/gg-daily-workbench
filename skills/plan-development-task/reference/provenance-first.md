# Provenance-First Change Handling

Used by **plan-mechanical-restore**, **define-scope-boundary**, and execute-plan's **execute-step**.

## Rule

Every code step declares where its code comes from.
Generating code is the last rung, never the default.
A request to revert, keep, restore, or copy asks for a **state**, not an implementation.

## Source declaration

| Field | Values | Meaning |
|---|---|---|
| `Source` | `no-op` · `base` · `port` · `copy` · `edit` · `generate` | Where the target code comes from |
| `Ref` | branch, tag, PR, or commit | Required for `base` and `port`; pin a SHA |
| `Equality` | `identical` · `ast-equal` · `behavior-equal` | How the result is proven |

| `Source` | Operation | Proof before commit |
|---|---|---|
| `no-op` | Change nothing | `git status --porcelain -- <paths>` is empty |
| `base` | `git restore --source=<ref> -- <paths>`, `git checkout <ref> -- <paths>` | `git diff --exit-code <ref> -- <paths>` |
| `port` | `git revert <commits>`, `git cherry-pick -n`, `git checkout <ref> -- <paths>`, `git apply` | Diff against `<ref>` limited to `<paths>`; residual hunks listed |
| `copy` | Copy from an in-repo origin at `<path>:<line>` | Origin path recorded plus an explicit adaptation list |
| `edit` | Minimal delta on existing code | No new symbols or files unless named |
| `generate` | Author new code | One-line justification plus user ratification |

Defaults: `no-op` / `base` / `port` → `identical`; `copy` → `ast-equal`; `edit` / `generate` → `behavior-equal`.

## Intent router

| User phrasing | `Source` |
|---|---|
| "revert", "undo", "roll back", "put it back" | `port` — revert the named commits; `base` only when no other commit touched the paths |
| "same as main", "sync with main", "align with the base branch" | `base` with `Ref: origin/main@<sha>` |
| "keep it as is", "don't touch", "no change needed", "leave it" | `no-op` |
| "copy from PR #123", "take it from release/2.4" | `port` |
| "do what billing-service does", "reuse that module" | `copy` |
| "restore the deleted function/file" | `port` from history |

Ask for the ref when the phrasing names no source; never guess the baseline.
Prefer reverting commits over restoring a path when unrelated commits touched it — a path restore discards their work too.

## The ladder

Descend and stop at the first rung that reaches the target state.

| Rung | Question | `Source` |
|---|---|---|
| 1 | Must nothing change? | `no-op` |
| 2 | Does a git ref already hold the target? | `base` / `port` |
| 3 | Does the repo already contain it? | `copy` |
| 4 | Is it a small delta on existing code? | `edit` |
| 5 | None of the above? | `generate` |

Escalate one rung at a time and state why the cheaper rung failed.
Rung 5 requires a written justification and user ratification.

## Mechanical restore plan

A `no-op` / `base` / `port` request introduces no behavior, so it is not a TDD change.

1. Record the trigger verbatim and the pinned `Ref`.
2. State `Source` and `Equality` per path.
3. State the target as the ref — "same as `origin/main@3f2a1c`", never as prose behavior.
4. List the paths excluded from the restore.
5. Name the git operation per path in the step.
6. Add one validation step: the equality proof plus a test run showing nothing else moved.
7. Record the non-behavioral justification per **tdd-guardrails**.

Skip RED/GREEN. Add no test that asserts the restore itself.

```markdown
### Step 1: Restore the sync worker to base ⏳
**Objective**: Make the sync worker identical to the base ref.
**Files**: src/sync/worker.ts
**Source**: base · origin/main@3f2a1c · identical
**Implementation**: `git restore --source=origin/main@3f2a1c -- src/sync/worker.ts`
**Validation**: `git diff --exit-code origin/main@3f2a1c -- src/sync/worker.ts`; suite green
**Status**: ⏳ Pending
```

## Anti-patterns

| Anti-pattern | Failure |
|---|---|
| Reading "revert" as "remove the feature" | Deletes code the user wanted restored |
| Restoring, then refactoring the result | Ships an unrequested change; the diff leaves the ref |
| Copying by hand from memory | Unverifiable; drifts from the ref |
| Regenerating equivalent behavior | Passes a behavior gate, fails a `Must match` gate |
| Treating `no-op` as "skip validation" | Unverified silence; run the proof and the tests |
| Pinning a branch name as `Ref` | The branch moves; the target state becomes nondeterministic |

## Validation

- [ ] Every step declares `Source` — `no-op · n/a · n/a` when nothing changes
- [ ] `Ref` is a SHA or tag, never a moving branch
- [ ] `Equality` proof recorded in the step note
- [ ] No step uses `generate` for a request phrased as revert, keep, restore, or copy
- [ ] Restored paths listed under `Must match` in the Scope Boundary

## Rationalizations to reject

| Excuse | Reality |
|---|---|
| "The regenerated code is cleaner" | Cleaner was not asked for; restore first, improve separately |
| "Behavior is identical, so it is the same" | Satisfies `behavior-equal` only, not `identical` |
| "The ref is probably main" | Ask; never infer the baseline |
| "Copying needs adaptation anyway" | Adaptation is allowed; list every delta |
| "A revert needs no test" | Needs the equality proof and a test run, not new tests |

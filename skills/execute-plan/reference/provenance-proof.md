# Provenance and Proof

Scope: what the executor needs to materialize a step and prove it. The planner owns
the plan shape and the Scope Boundary; this file covers `Source`, the ladder, and the
proof commands run before each commit.

## Source declaration

Every step carries a `Source`: `no-op` · `base` · `port` · `copy` · `edit` · `generate`.
Try the cheapest source first; generating code is the last rung.

| `Source` | Operation | Proof before commit |
|---|---|---|
| `no-op` | Change nothing | `git status --porcelain -- <paths>` is empty |
| `base` | `git restore --source=<ref> -- <paths>`, `git checkout <ref> -- <paths>` | `git diff --exit-code <ref> -- <paths>` |
| `port` | `git revert <commits>`, `git cherry-pick -n`, `git checkout <ref> -- <paths>`, `git apply` | Diff against `<ref>` limited to `<paths>`; residual hunks listed |
| `copy` | Copy from an in-repo origin at `<path>:<line>` | Origin path recorded plus an explicit adaptation list |
| `edit` | Minimal delta on existing code | No new symbols or files unless named |
| `generate` | Author new code | One-line justification plus user ratification |

Defaults: `no-op` / `base` / `port` → `identical`; `copy` → `ast-equal`; `edit` / `generate` → `behavior-equal`.

## The ladder

Descend and stop at the first rung that reaches the target state.

| Rung | Question | `Source` |
|---|---|---|
| 1 | Must nothing change? | `no-op` |
| 2 | Does a git ref already hold the target? | `base` / `port` |
| 3 | Does the repo already contain it? | `copy` |
| 4 | Is it a small delta on existing code? | `edit` |
| 5 | None of the above? | `generate` |

Escalate one rung at a time and state why the cheaper rung failed. Rung 5 requires a
written justification and user ratification.

## Refs

- Pin a SHA or tag; a moving branch makes the target state nondeterministic.
- Ask for the ref when the step names no source; never infer the baseline.
- Prefer reverting commits over restoring a path when unrelated commits touched it — a path restore discards their work too.

## Stop conditions

| Situation | Action |
|---|---|
| Step says revert / keep / restore but the implementation regenerates code | Stop — request a plan amendment |
| The proof diff shows hunks outside the named paths | Stop — report the residual hunks |
| A `Must match` path cannot produce an equality proof | Stop — the step cannot prove the restore |
| `Ref` is missing or is a branch name | Stop — ask for a SHA or tag |

## Validation

- [ ] Every step declares `Source` — `no-op · n/a · n/a` when nothing changes
- [ ] `Ref` is a SHA or tag, never a moving branch
- [ ] Equality proof recorded in the step note
- [ ] No step uses `generate` for a request phrased as revert, keep, restore, or copy
- [ ] Restored paths listed under `Must match` in the Scope Boundary

# Exit Gate

Every plan ships a green-only **exit gate**: recorded commands, a proven baseline, one final step,
and a receipt. The plan is the contract — the gate is never the executor's discretion.

## 1. Gate commands (plan time)

Discover the commands from repo evidence; never invent them and never accept "run the tests".

| Evidence | Example |
|---|---|
| CI config | `.github/workflows/*.yml` `run:` steps |
| Build or task file | `Makefile`, `pom.xml`, `build.gradle`, `package.json` scripts, `pyproject.toml` |
| Contributor docs | `CONTRIBUTING.md`, README build section |
| Repo scripts | `scripts/ci/*.sh`, `tox.ini`, `justfile` |

Record one header line: `**Gate**: build=<cmd> · test=<cmd> · lint-type=<cmd>`, each with its
`file:line`. Monorepos list one row per module or package — every row must pass.

**All gate commands run locally in the worktree.** The gate never polls, waits for, or delegates
to a remote pipeline; a CI config is read only to discover the canonical command.

No evidence found → ask the user. A guessed command is a gate that fails for the wrong reason.

## 2. Baseline (execution Step 1)

Run those exact commands on the base commit and record the verdict.

| Baseline | Action |
|---|---|
| `green` | Proceed |
| `red` — tooling missing | Stop and ask: install or provision |
| `red` — pre-existing failures | Add a **Restore baseline** step, or a user-ratified exclusion naming each failure |
| `red` — unknown cause | Stop and ask |

Rule: `baseline: green` or `baseline: red — <command>: <named failures>`. A gate that cannot be
green at the base is not a gate; it is a step that will be skipped.

Unrelated failures outside the gate commands stay noted, not blocking — but they never shrink the
gate's scope.

## 3. The Exit Gate step

Last step in `## Steps`, after cleanup:

```markdown
### Step N: Exit gate ⏳
**Objective**: Prove the build, full suite, and static checks are green.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: Run every gate command on the final tree; repair reds in place.
**Validation**: `<build>` && `<test>` && `<lint-type>` — all exit 0, zero failures.
**Status**: ⏳ Pending
```

- Red → repair (maximum 2 attempts) → still red: `❌` or `🚫` and ask the user. Never `✅`.
- `✅` requires a receipt in the `Status` line: command, exit code, counts
  (`build=0 · test=412 passed, 0 failed · lint=0`).
- Placement is last. Any later step invalidates the receipt — re-run the gate.

## 4. No narrowing

Forbidden in the `Gate` line and in the gate step's `Validation`:

| Phrase | Why it fails |
|---|---|
| "affected tests only", "subset", "smoke" | Misses cross-module compile and contract breaks |
| "if available", "optional", "when practical" | Makes the gate droppable at run time |
| "or one consolidated gate" as a choice | A planning-time option becomes a run-time skip |
| "CI will catch it" | The gate is local and blocking; a pipeline runs later and never proves this plan |
| "Only CI can run it" | Run the same command locally; a gate that cannot run locally is not a gate |

The gate is one scope: full build, full suite, static checks. The cost is paid once, at the end.

## 5. TDD interaction

RED steps are supposed to fail. Only two things must be green: a step's post-implementation
`Validation`, and the Exit Gate. Never weaken the gate to accommodate a failing step — a red at the
gate means the work is not done, whatever the earlier steps claim.

## 6. Waiver

The only escape, and only with the user:

```markdown
**Gate waiver**: <scope> — <excluded command and named failures> — ratified by <user> on <date>
```

- Scope-named and item-named. Blanket waivers ("the suite is flaky") are rejected.
- An agent-written waiver without user ratification is a plan-quality failure, not a waiver.
- Surface the waiver in the `context.md` `## Execution` handoff and the delivery index cell.

## 7. Rationalizations to reject

| Excuse | Reality |
|---|---|
| "Too small to need a build" | Small edits break compilation in other modules |
| "The suite is slow" | Pay it once; a red merge costs more |
| "Only config and docs changed" | Config breaks startup — waive it explicitly if truly inert |
| "The failures are unrelated" | Name them and get ratification, or fix them |
| "It was green before my last edit" | Then re-run it and prove it |
| "CI is the real gate" | The gate is local and blocking; CI runs later and never substitutes for it |

## 8. Checklist

- [ ] `Gate` line present, evidence-backed, one row per module
- [ ] Baseline recorded; a red baseline resolved by a step or a ratified exclusion
- [ ] Exit Gate is the final step, with a pass rule and a receipt requirement
- [ ] Every gate command runs locally; no remote pipeline status is required or awaited
- [ ] No forbidden narrowing phrase anywhere in the gate
- [ ] Waiver, if any, is scope-named, item-named, dated, and user-ratified

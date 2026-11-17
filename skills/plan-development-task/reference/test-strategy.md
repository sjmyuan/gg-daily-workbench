# Test Strategy Selection

Used by **plan-bug-fix**, **plan-feature-implementation**, **plan-refactor**, **plan-poc**, and **plan-rubric** (test row).

One strategy per plan, chosen once. Unit granularity inside it is the planner's call — naming the strategy stops the plan from improvising a different rule per step.

## Choose the strategy

| Strategy | Proves the change by | Fits |
|---|---|---|
| `test-first` | A test that fails for the target reason, then passes | Bug fixes, features, behavior-changing refactors |
| `characterization-first` | An existing or added test pins current behavior and stays green | Refactors that must not change behavior |
| `type/config-only` | Compile or type check plus the suite | Type-only, config values, docs, formatting |
| `none (mechanical)` | Equality proof against a pinned ref | Restore, port, copy, keep — see **change-provenance** |

## Unit granularity — the call the plan makes

No template fixes the step count; the plan decides.

- One unit per **observable outcome** or independent failure mode — not per file, and not per phase.
- Merge units sharing a fixture, failing together, or validated by one command. A separate step must buy a separate verdict.
- Split a unit only when its validation is separable or its risk differs.
- A step whose shape depends on code not yet read is **open by design**: name the check that closes it (see **plan-file-format**), and let the executor resolve it.

## What the strategy must name

- The strategy and why it fits — one line in the plan header.
- Each unit's proof: the test, benchmark, equality diff, or type check that proves it.
- Any unit that departs from the strategy, with its reason — one named exception beats a rationale per unit.

## The Iron Law still applies

`test-first` means the test is written and watched to fail before the code changes. Strategy selection chooses the **evidence**; it never waives it (see **[tdd-guardrails.md](tdd-guardrails.md)**).

## Failure modes

| Symptom | What it means | Fix |
|---|---|---|
| Every unit carries the same nine steps | The template is planning, not the planner | Merge units; keep a step only where its verdict differs |
| "Write tests" is the plan's only test statement | No proof is named | Name the test that catches the break, per **test-quality** |
| A step restates its own phase ("confirm RED") | The step buys no verdict | Fold it into the test or implement step's `Validation` |
| Test-first claimed, but no step watches a failure | The law was waived silently | Restore the failing run, or record why not |
| Ten steps for a one-line change | Phase-shaped planning | Three units at most: prove, fix, gate |

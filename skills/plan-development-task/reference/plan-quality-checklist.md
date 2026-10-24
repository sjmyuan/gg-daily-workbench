# Plan Quality Checklist

Before presenting a development plan to the user, verify all items below.

## Template conformance
- [ ] `plan.md` matches **reference/plan-file-format.md**: `# Plan:` title, metadata (`Type`, `Branch` off `<base>`, `TDD variant`), `## Scope Boundary`, optional `## Decisions`, `## Steps`
- [ ] `Type` is one of `bug-fix` · `feature` · `refactor` · `poc` · `restore`; `ADR`/`Option` appear for POC only
- [ ] Every step is one `### Step N: <title> ⏳` block with `Objective`, `Files`, `Source`, `Implementation`, `Validation`, `Status` — all six, in that order
- [ ] Step objectives are one imperative sentence; `Files` is `none` where nothing is edited
- [ ] Branch and base live in `plan.md`, never in `context.md`
- [ ] No root cause, requirement narrative, "Key Characteristics", or consolidation prose in `plan.md`
- [ ] Rework files use the same step block with numbering restarted at 1; `plan.md` untouched

## Prerequisites
- [ ] **Step 1** is **Prepare Environment** (branch, no overlapping dirt, dependencies, affected-area baseline)
- [ ] Branch name and base branch are recorded in the plan header (mirrored as cell state in `index.md`)
- [ ] Only necessary checks gate execution — unrelated dirt and unrelated failures are noted, not blocking

## Scope Boundary
- [ ] Plan includes a `## Scope Boundary` block with **May change**, **Must match** (only for restores/ports), **Expected files**, **Must not change**, **Protected zones** — in that order
- [ ] `Protected zones` is present, using `none added` when nothing extends the default set
- [ ] Boundary is behavior-based; **Expected files** is advisory, never a gate
- [ ] Every restored or ported path appears under `Must match` with its pinned ref — the only zone that requires byte equality
- [ ] Protected zones are inherited or extended, never dropped
- [ ] Stop triggers are material only (see **scope-boundary**)
- [ ] Rework files (`rework-<date>.md`) carry their own boundary — inherits the original zones, tightened to the governing ADR; `plan.md` untouched

## Amendment
- [ ] Every ✅ step and its notes are byte-for-byte unchanged
- [ ] New steps appended with the next number or inserted with a letter suffix; no step renumbered
- [ ] Obsolete pending steps marked `⏭ abandoned — <reason>`, not deleted
- [ ] No abandoned step has a commit
- [ ] `context.md` holds one `## Amendments` row for the change
- [ ] Boundary tightened, or widened with user ratification
- [ ] No second plan file or folder created for the same feature

## Coverage
- [ ] Every identified issue/functionality/objective has a corresponding TDD cycle, or a declared `Source` for a mechanical step
- [ ] Every step declares `Source`, `Ref`, and `Equality` per **change-provenance** — `no-op · n/a · n/a` when nothing changes
- [ ] No step uses `Source: generate` for a request phrased as revert, keep, restore, or copy
- [ ] Mechanical restore plans name the git operation per path and skip RED/GREEN
- [ ] All acceptance criteria from the user request are addressed
- [ ] Each acceptance criterion maps to at least one test step that names the production change it catches
- [ ] Edge cases and error scenarios are covered in the test steps
- [ ] For refactors: existing observable behavior is preserved — no new functionality is introduced

## Sequencing
- [ ] Dependency ordering is correct — no step depends on a later step
- [ ] Prepare Environment is always Step 1
- [ ] Validate Linting, Formatting and Type Checking closes each issue/functionality/objective group, or one consolidated final gate covers all groups

## Step Management
- [ ] For bug fix plans: total step count ≤ 20
- [ ] For feature implementation plans: total step count ≤ 25
- [ ] For refactor plans: total step count ≤ 20
- [ ] For mechanical restore plans: total step count ≤ 5
- [ ] Related items are consolidated where they share context or can be tested together
- [ ] Each step has a clear, single objective

## TDD Fidelity
- [ ] TDD variant is documented in the plan header (`Full cycle`, `Streamlined`, `Mixed` naming each group, or `None` for a restore) with a rationale
- [ ] Complex logic changes (bug fix, feature, or refactor) always use full TDD cycle
- [ ] Configuration-only changes may use streamlined approach with documented justification
- [ ] Documentation-only changes have no test cycle needed; validate with linting only
- [ ] Performance bugs include benchmarks and query-count assertions
- [ ] Code organization moves (file renames, package restructures) verify existing tests pass unchanged
- [ ] No implementation step precedes the failing test for the behavior it delivers
- [ ] Each "Confirm Test Failure" step requires a true failure (not an error) for the expected reason; a test that passes immediately is rewritten
- [ ] Mutation check: each realistic mutation (wrong branch, wrong constant, missing side effect, missing validation) is caught by at least one test
- [ ] Refactor plans never introduce a failing test — existing tests stay green; characterization tests are added only where coverage is missing
- [ ] Mechanical restore plans skip RED/GREEN and record the non-behavioral justification per **tdd-guardrails**

## Clarity
- [ ] Each step description is actionable and unambiguous
- [ ] File paths and class names are specified where known
- [ ] Validation criteria are explicit (e.g., "all tests pass", "no lint errors", "p99 latency < 500 ms")
- [ ] Validation criteria are behavioral — no step asserts a commit hash; byte equality only where `Must match` names it
- [ ] Prose follows concise writing (see **concise-writing**): one objective per step sentence, one claim per scope-boundary bullet, no banned phrases
- [ ] `context.md` is a 40–60-line charter (ceiling 8,000 chars / 120), passes the admission test, duplicates no `plan.md` fact, and holds no pre-flight evidence or log content (see **doc-budgets**)
- [ ] A POC plan is a normal TDD feature plan with **Type** `poc` + ADR/option metadata; no measurement or evaluation step; success criteria are optional header notes

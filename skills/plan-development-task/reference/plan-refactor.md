# plan-refactor

1. **Prepare Environment (Prerequisites)**: Apply **plan-prerequisites** from the SKILL.md — ensure the feature branch exists, named per the **repo's branch convention** (detect from existing branches / git config / team docs, or ask the user; never assume a prefix), based on the correct base; no uncommitted changes overlapping the plan's work; dependencies and toolchain installed; the gate commands (`build` / `test` / `lint-type`) discovered from repo evidence (`file:line`) and run on the base, with `baseline: green` or the named failures recorded. Raise only necessary blockers to the user before continuing.
2. Break down the refactor request into specific, measurable objectives and clearly defined constraints.
3. **Define Scope Boundary**: Apply **define-scope-boundary** — derive the **May change**/**Must not change** behaviors from the refactor scope and the governing ADR (for **orchestrate-feature-delivery** cells); behavior change stays **Must not change**; present to the user for ratification.
4. Identify and map dependencies between objectives to establish an efficient and logical refactoring sequence.
5. **Consolidate Steps**: Group related objectives together when they share context or can be tested together, reducing the total step count while maintaining clarity. Consolidation strategies: (a) merge coverage-confirmation and refactor steps for simple extractions or renames into a single step, (b) combine Clean Up Unused Code + Clean Up Tests + Verify Cleanup into one cleanup step when changes are small, (c) fold every static check into the single final Exit Gate step — the gate is mandatory, never optional.
6. Load **reference/tdd-approach-selection.md** to select the appropriate TDD variant for each objective; existing tests stay green throughout. Document the rationale.
7. Create a detailed step-by-step refactor plan using the template in **reference/plan-file-format.md** — title + metadata, the ratified `## Scope Boundary`, optional `## Decisions`, then one six-field `### Step N: <title> ⏳` block per step. For each objective, include the following steps:
   1. **Confirm Existing Coverage**: Verify existing tests cover the behavior being restructured; add characterization tests (which pass immediately) only where coverage is missing.
   2. **Refactor in Small Steps**: Apply one structural change at a time without changing behavior, using the tooling's move/extract operation instead of retyping code (see **reference/provenance-first.md**).
   3. **Verify Green**: Re-run all tests after each step; any failure means behavior changed — revert it.
   4. **Clean Up Unused Code**: Remove obsolete or redundant code left by the restructure.
   5. **Clean Up Tests**: Update or remove tests made irrelevant by the restructure.
   6. **Verify Cleanup**: Re-run all tests to confirm the cleanup introduced no regressions.
   7. **Exit Gate**: Run every recorded gate command — build, full suite, lint/type. All exit 0 with zero failures; a refactor keeps every existing test green. Red → repair twice, then stop and ask. See **reference/exit-gate.md**.
   A refactor never introduces a failing test; a failing test means new behavior — move it to a feature plan.
8. Ensure the total number of steps in the plan is manageable and does not exceed 20 steps.
9. **Validate Plan Quality**: Load **reference/plan-quality-checklist.md** and verify — every objective has existing coverage or characterization tests defined, no step introduces a failing test, dependency ordering is correct, step count ≤ 20, TDD variants are documented, and every **Exit Gate** item passes. Revise any failing items before presenting to the user.
10. Summarize the complete plan to the user.

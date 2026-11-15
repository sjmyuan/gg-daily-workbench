---
name: plan-development-task
description: Classify, clarify, and generate TDD step-by-step plans for bugs, features, refactors, and POCs, and amend in-flight plans. Use when fixing a bug, adding a feature, refactoring, proving a POC, restoring, reworking, or amending a plan.
---

<when-to-use-this-skill>
- User reports a bug, regression, failing test, or unexpected behavior in existing code, or asks to investigate and fix one
- User submits a requirement, enhancement, or new behavior that does not exist yet, or asks whether it is feasible
- User wants a POC proving one ADR option — a standalone slice, never a snippet
- User requests refactoring, cleanup, restructuring, or maintainability work without changing behavior
- User wants to plan a rework for an already-implemented feature — a sibling `rework-<date>.md`
- An in-flight plan needs steps added, removed, or reordered before they run
- User asks to revert, restore, copy, or keep code unchanged ("same as main"), or to bring over a change from another branch or commit

- Do NOT decompose a multi-feature or multi-repo change — apply **orchestrate-feature-delivery** first, then plan each cell.
</when-to-use-this-skill>

<knowledge>
<request-intake>
Gate the request through `clarify-request`'s intake gate before classifying: restate it and itemize every inference — change type, expected behavior, input, done criteria, restore ref. Zero inferences → classify; anything inferred → ask the top 3 with options, a recommendation, and a default.
A symptom-only request always infers the expected behavior — ask it; never plan from the suspected cause.
Record it in `context.md`: the restatement becomes the plan objective; each accepted default goes under `## Unknowns` as `Assumption (user-accepted, unverified): <default> — Step N verifies — fallback <…>`. A seeding brief covering the cell, type, behavior, inputs, and criteria **is** the gate result: adopt it, ask nothing, and plan against it.
</request-intake>
<named-standards>
| Standard | Rule | Details |
|---|---|---|
| **change-provenance** | Every code step declares its source (`no-op` · `base` · `port` · `copy` · `edit` · `generate`), generating only when no cheaper rung reaches it. | **reference/provenance-first.md** |
| **change-type-classification** | Classify as mechanical, bug fix, feature, refactor, or POC; two fits → one question. | **reference/change-type-classification.md** |
| **tdd-approach-selection** | The TDD variant follows the change type; the plan records it with its rationale. | **reference/tdd-approach-selection.md** |
| **test-quality** | Each planned test names the production change it catches and exercises real behavior, never mocks. | **reference/test-quality.md** |
| **tdd-guardrails** | No behavior change without a failing test first; skipping tests needs a recorded justification. Hard-to-test work is a smell — refactor first. | **reference/tdd-guardrails.md** |
| **plan-prerequisites** | Step 1 **Prepare Environment** covers branch, dirt, toolchain, gate commands, and baseline only; unrelated dirt is noted. | **reference/plan-prerequisites.md** |
| **scope-boundary** | A **Scope Boundary** gates on behavior, never paths: **May change**, **Must not change**, **Protected zones**, **Must match**; stop on material change. | **reference/scope-boundary.md** |
| **poc-plan-definition** | A POC is a feature plan for one ADR option: it implements, never measures; the MR is the evaluation vehicle. | **reference/plan-poc.md** |
| **plan-amendment** | Amend in place: ✅ steps frozen, letter suffixes for insertions, `⏭ abandoned — <reason>`, never renumbered. | **reference/plan-amendment.md** |
| **rework-plan-convention** | A rework is a sibling `rework-<date>.md` holding only the delta; `plan.md` stays frozen. | **reference/rework-plan-convention.md** |
| **exit-gate** | A green-only gate: `**Gate**` line (`build=` · `test=` · `lint-type=`, evidence-backed, never narrowed), baseline in Step 1, final Exit Gate run locally; red → `❌`/`🚫`, never `✅`, and only a ratified waiver escapes. | **reference/exit-gate.md** |
| **concise-writing** | Plan prose follows BLUF and hard caps; `context.md` is a 40–60-line charter, never steps or logs. | **reference/doc-budgets.md**, **reference/writing-style.md** |
</named-standards>
<write-boundary>
Produces a **plan**, never executes it, and writes only `plan.md`, `context.md`, and `rework-<date>.md` — never code or config. After persisting, confirm only plan docs changed.
</write-boundary>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Writing a mechanical restore plan | Revert-to-base, equality proof | [examples/mechanical-restore-plan.md](examples/mechanical-restore-plan.md) |
| A rework risks **Must not change** behavior | Refusal with options | [examples/rework-scope-boundary.md](examples/rework-scope-boundary.md) |
| Amending an in-flight plan | Amend-in-place, ⏭ abandoned | [examples/amend-mid-execution.md](examples/amend-mid-execution.md) |
| Bug: logic, timing, perf | Full workflow | [examples/bug-fix-simple-logic.md](examples/bug-fix-simple-logic.md) · [examples/bug-fix-performance.md](examples/bug-fix-performance.md) |
| Feature: complex rules or a flag | Full workflow | [examples/feature-complex-transformation.md](examples/feature-complex-transformation.md) · [examples/feature-simple-configuration.md](examples/feature-simple-configuration.md) |
| Refactor: class split or interfaces | Full workflow | [examples/refactor-service-splitting.md](examples/refactor-service-splitting.md) · [examples/refactor-interface-implementation.md](examples/refactor-interface-implementation.md) |
| Planning a POC | Metadata and steps | [examples/plan-adr-option-poc.md](examples/plan-adr-option-poc.md) |
| Persisting a confirmed plan | `plan.md` + `context.md` | [examples/export-plan.md](examples/export-plan.md) |
| Turning a draft into a charter | Section triage | [examples/context-charter.md](examples/context-charter.md) |
</context-loading-guide>
</knowledge>

<capabilities>
<classify-change-type>
1. Gate the request per **request-intake** — restate it and show every inference; detect a mechanical target per **change-provenance**.
2. Read the request's signals per **change-type-classification**; if two types fit, ask one material question with options.
3. Present the restatement, the inferences, the classified type, and the reasoning.
4. Route through **define-scope** to **plan-mechanical-restore** · **plan-bug-fix** · **plan-feature-implementation** · **plan-refactor**, or directly to **plan-poc**.
</classify-change-type>
<plan-mechanical-restore>
1. Record the trigger verbatim, the pinned `Ref`, and `Source`/`Equality` per path; ask for the source ref when the request names none.
2. List every restored path under `Must match` with its ref.
3. Skip RED/GREEN and record the non-behavioral justification per **tdd-guardrails**.
4. Write six-field steps per **reference/plan-file-format.md**: prepare environment → per-path restore naming the git operation → equality proof → exit gate.
5. Validate against the restore checks in **reference/provenance-first.md**.
</plan-mechanical-restore>
<define-scope>
1. **Bug fix**: analyze root-cause patterns and test hypotheses by inspecting code. **Feature / refactor**: turn each loaded term and silent premise into a question or assumption. **Mechanical**: confirm the ref and paths.
2. Ask the material questions the inference list surfaced, each with options and a default; stop when the scope is decidable, not when it is complete.
3. Present the root cause with its reasoning, or the scope summary; hand the result to the plan capability and to **define-scope-boundary**.
</define-scope>
<plan-bug-fix>
Load **reference/plan-bug-fix.md** and follow its steps.
</plan-bug-fix>
<plan-feature-implementation>
Load **reference/plan-feature-implementation.md** and follow its steps.
</plan-feature-implementation>
<plan-refactor>
Load **reference/plan-refactor.md** and follow its steps.
</plan-refactor>
<plan-poc>
Load **reference/plan-poc.md** and follow its steps.
</plan-poc>
<define-scope-boundary>
1. Derive the zones from the classified type, the confirmed scope, and — for a delivery cell — the governing ADR.
2. Name **May change** and **Must not change** by observable behavior, not by path; add `Must match` per restored path, **Expected files** as advisory, and any **Protected zone**.
3. Apply the materiality test (see **scope-boundary**) to every exclusion; keep stop triggers material-only.
4. Present the zones, request ratification, and hand the ratified boundary to the plan and to **export-plan**.
</define-scope-boundary>
<amend-plan>
1. Read the plan, its statuses, and `context.md` `## Amendments`; confirm the defect sits in pending steps, else **rework-plan-convention**.
2. Freeze every ✅ step byte-for-byte. Add steps with the next number, or insert with a letter suffix (`3a`); mark obsolete pending steps `⏭ abandoned — <reason>`; never renumber or delete.
3. Tighten the boundary; widen it only with user ratification.
4. Record one `## Amendments` row, keep `context.md` within **doc-budgets**, validate per **reference/plan-quality-checklist.md**, and show the step diff.
</amend-plan>
<export-plan>
1. A feature folder already holding `plan.md` → apply **amend-plan** instead of a second plan.
2. After confirmation, ask whether to persist the plan for **execute-plan**.
3. Resolve the location: a delivery cell uses `deliveries/<epic-name>/{repo}/{feature-name}/`; else **resolve-artifact-location** gives the base for `{base}/feature-implementations/`.
4. Write `plan.md` per **reference/plan-file-format.md** and `context.md` per **doc-budgets**; refuse a plan whose gate is missing, narrowed, or unratified.
5. Curate `context.md` to the charter: the **admission test** turns pre-flight evidence into a decision or an Unknown, never a paste; over budget → remove duplication with `plan.md`.
6. Validate conciseness, re-measure, and report the saved location so the user can invoke **execute-plan**.
</export-plan>
</capabilities>

<rules>
<rule> When the user requests a code change, gate it per **request-intake**, then apply **classify-change-type**. </rule>
<rule> When the request is to revert, restore, port, copy, or keep code, apply **plan-mechanical-restore** — never regenerate equivalent code. </rule>
<rule> When a step touches existing code, declare its `Source` per **change-provenance**; `generate` needs a justification and ratification. </rule>
<rule> When both restructuring and new behavior are needed, apply **plan-refactor** before **plan-feature-implementation**. </rule>
<rule> When generating any plan, apply **plan-prerequisites** and **define-scope-boundary**. </rule>
<rule> When generating or validating any plan, apply **exit-gate** — evidence-backed `Gate` commands, a proven baseline, and a green-only Exit Gate step never abandoned, deferred, or met by a subset. </rule>
<rule> When the gate baseline is red and no restore step or ratified exclusion names the failures, or a waiver is unratified, stop and ask — never export that plan. </rule>
<rule> When planning a rework for an implemented feature, apply **rework-plan-convention** and **export-plan** — never overwrite implemented steps. </rule>
<rule> When a rework would materially change the original **Must not change** behavior or touch a protected zone, refuse and ask — never write silently. </rule>
<rule> When an in-flight plan has a defect in steps that have not run, apply **amend-plan** — never a second plan file or folder. </rule>
<rule> When writing or validating a test step, apply **test-quality** — each test names the break it catches. </rule>
<rule> After the plan is confirmed, optionally apply **export-plan** to persist it for **execute-plan**. </rule>
<rule> Confine every write to plan docs (`plan.md`, `context.md`, `rework-<date>.md`); never modify code, config, tests, or any non-markdown file. </rule>
</rules>

---
name: plan-development-task
description: Plan development work — diagnose the change, choose the evidence that proves it, shape units an executor can run, and amend in-flight plans. Prefer the project's own equivalent when one exists. Use when fixing a bug, adding a feature, refactoring, proving a POC, restoring, porting, reworking, or amending a plan.
---

<when-to-use-this-skill>
- User reports a bug, regression, or failing test in existing code, or asks to investigate and fix one
- User submits a requirement or new behavior that does not exist yet, or asks whether it is feasible
- User wants a POC proving one ADR option — a standalone slice, never a snippet
- User requests refactoring, cleanup, restructuring, or maintainability work without changing behavior
- User wants to plan a rework for an already-implemented feature — a sibling `rework.md`
- An in-flight plan needs steps added, removed, or reordered before they run
- User asks to revert, restore, copy, or keep code, or port a change from another branch or commit

- Do NOT decompose a multi-feature or multi-repo change — apply **orchestrate-feature-delivery** first, then plan each cell.
</when-to-use-this-skill>

<knowledge>
<request-intake>
Gate through `clarify-request`: itemize inferences — type, behavior, input, done criteria, restore ref — and ask the top 3 with a default; a symptom-only request asks its expected behavior, never plans from a suspected cause. A seeding brief carrying cell, type, behavior, inputs, and criteria **is** the gate result — adopt it.
The **settled request** is user input: objective, decision, or `## Why`, never an assumption. Only an **unanswered default** becomes `Assumption (user-accepted, unverified)` under `## Unknowns`.
A brief marked `Mode: delivery` ratifies scope and persistence: never ask the user; persist and return.
</request-intake>
<named-standards>
| Standard | Rule | Details |
|---|---|---|
| **change-provenance** | Every code step declares its source (`no-op` · `base` · `port` · `copy` · `edit` · `generate`); generate last. | **reference/provenance-first.md** |
| **change-type-classification** | mechanical · bug fix · feature · refactor · POC; two fits → one question. | **reference/change-type-classification.md** |
| **test-strategy** | One evidence strategy per plan; unit granularity is yours; `test-first` never waived. | **reference/test-strategy.md** |
| **test-quality** | Each planned test names the production change it catches and exercises real behavior, never mocks. | **reference/test-quality.md** |
| **tdd-guardrails** | No behavior change without a failing test first; skipping needs a recorded justification. Hard to test → refactor only when the requested behavior needs it. | **reference/tdd-guardrails.md** |
| **plan-prerequisites** | Step 1 covers branch, dirt, toolchain, gate commands, and the baseline. | **reference/plan-prerequisites.md** |
| **scope-boundary** | Gates on behavior, never paths — a new guard included: **May change** · **Must not change** · **Protected zones** · **Must match**; stop only on material change. | **reference/scope-boundary.md** |
| **poc-plan-definition** | A POC is a feature plan for one ADR option: it implements, never measures; the MR is the evaluation vehicle. | **reference/plan-poc.md** |
| **plan-amendment** | Amend in place: ✅ frozen, letter suffixes for insertions, `⏭ abandoned — <reason>`, never renumber. | **reference/plan-amendment.md** |
| **rework-plan-convention** | A sibling rework file holds only the delta; `plan.md` stays frozen. | **reference/rework-plan-convention.md** |
| **exit-gate** | Green-only: evidence-backed `**Gate**` line, baseline in Step 1, final local run; red → `❌`/`🚫`, never `✅`; only a ratified waiver escapes. | **reference/exit-gate.md** |
| **plan-quality** | Grade every plan against the rubric: rows 1 and 7 pass/fail, the rest graded. | **reference/plan-rubric.md** |
| **concise-writing** | BLUF and hard caps; `context.md` is a 40–60-line charter, never steps or logs. | **reference/doc-budgets.md**, **reference/writing-style.md** |
</named-standards>
<capability-regimes>
**Judgment** — classify, scope, plan, amend: you own the path (units, order, granularity, what to leave open); graded by **plan-rubric**, never scripted.
**Contractual** — mechanical restore, export: exact fields and sequence; deviate only by asking.
</capability-regimes>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Mechanical restore plan | Revert-to-base, equality proof | [examples/mechanical-restore-plan.md](examples/mechanical-restore-plan.md) |
| A rework risks **Must not change** | Refusal with options | [examples/rework-scope-boundary.md](examples/rework-scope-boundary.md) |
| Amending an in-flight plan | Amend-in-place, ⏭ | [examples/amend-mid-execution.md](examples/amend-mid-execution.md) |
| Bug: logic, timing, perf | — | [bug-fix-simple-logic](examples/bug-fix-simple-logic.md) · [bug-fix-performance](examples/bug-fix-performance.md) |
| Feature: complex rules or a flag | — | [feature-complex-transformation](examples/feature-complex-transformation.md) · [feature-simple-configuration](examples/feature-simple-configuration.md) |
| Refactor: class split or interfaces | — | [refactor-service-splitting](examples/refactor-service-splitting.md) · [refactor-interface-implementation](examples/refactor-interface-implementation.md) |
| Planning a POC | Metadata and steps | [examples/plan-adr-option-poc.md](examples/plan-adr-option-poc.md) |
| Judging a weak plan | Same request, both | [examples/plan-quality-tradeoff.md](examples/plan-quality-tradeoff.md) |
| Persisting a confirmed plan | `plan.md` + `context.md` | [examples/export-plan.md](examples/export-plan.md) |
| Draft into a charter | Section triage | [examples/context-charter.md](examples/context-charter.md) |
</context-loading-guide>
</knowledge>

<capabilities>
<classify-change-type>
1. Gate per **request-intake**; detect a mechanical target per **change-provenance**.
2. Read the signals per **change-type-classification**; two fits → one question with options.
3. Present restatement, inferences, type, and reasoning.
4. Route through **define-scope** to **plan-mechanical-restore** · **plan-bug-fix** · **plan-feature-implementation** · **plan-refactor**, or to **plan-poc**.
</classify-change-type>
<plan-mechanical-restore>
1. Record the trigger verbatim, the pinned `Ref`, and `Source`/`Equality` per path; ask for the ref when none is named.
2. List every restored path under `Must match` with its ref.
3. Skip RED/GREEN and record the non-behavioral justification per **tdd-guardrails**.
4. Write six-field steps per **reference/plan-file-format.md**: prepare environment → per-path restore naming the git operation → equality proof → exit gate.
5. Validate against the restore checks in **reference/provenance-first.md**.
</plan-mechanical-restore>
<define-scope>
1. **Bug fix**: analyze root-cause patterns and test hypotheses by inspecting code. **Feature / refactor**: question each loaded term and each premise that changes what is built. **Mechanical**: confirm the ref and paths.
2. Ask the material questions with options and a default; stop when the scope is decidable, not when complete.
3. Present the root cause with its reasoning, or the scope summary; hand it to the plan capability and **define-scope-boundary**.
</define-scope>
<plan-bug-fix>
Load **reference/plan-bug-fix.md**; shape the plan per its judgment guidance.
</plan-bug-fix>
<plan-feature-implementation>
Load **reference/plan-feature-implementation.md**; shape the plan per its judgment guidance.
</plan-feature-implementation>
<plan-refactor>
Load **reference/plan-refactor.md**; shape the plan per its judgment guidance.
</plan-refactor>
<plan-poc>
Load **reference/plan-poc.md**; shape the plan per its judgment guidance.
</plan-poc>
<define-scope-boundary>
1. Derive the zones from the classified type, the confirmed scope, and — for a delivery cell — the governing ADR.
2. Name **May change** and **Must not change** by observable behavior, not by path; add `Must match` per restored path, **Expected files** as advisory, and any **Protected zone**.
3. Apply the materiality test (see **scope-boundary**) to every exclusion; keep stop triggers material-only.
4. Present the zones; `Mode: delivery` ratifies them by default. Hand the boundary to the plan and **export-plan**.
</define-scope-boundary>
<amend-plan>
1. Read the plan, its statuses, and `context.md` `## Amendments`; confirm the defect sits in pending steps, else **rework-plan-convention**.
2. Freeze every ✅ step byte-for-byte. Insert steps before the Exit gate with a letter suffix (`3a`); mark obsolete pending steps `⏭ abandoned — <reason>`; never renumber or delete.
3. Tighten the boundary; widen it only with user ratification.
4. Record one `## Amendments` row, keep `context.md` within **doc-budgets**, re-grade per **reference/plan-rubric.md**, and show the step diff.
</amend-plan>
<export-plan>
1. A feature folder already holding `plan.md` → apply **amend-plan** instead of a second plan.
2. Persist for **execute-plan**; `Mode: delivery` skips the question, interactive mode asks.
3. A delivery cell uses `deliveries/<epic-name>/{repo}/{feature-name}/`; else **resolve-artifact-location** gives `{base}/feature-implementations/`.
4. Write `plan.md` per **reference/plan-file-format.md** and `context.md` per **doc-budgets**; refuse a plan whose gate is missing, narrowed, or unratified.
5. Curate `context.md` to the charter: the **admission test** turns pre-flight evidence into a decision or an Unknown, never a paste; over budget → cut duplication with `plan.md`.
6. Grade the plan per **plan-rubric** — no Fail row, and rows 1 and 7 pass — then report the saved location so the user can invoke **execute-plan**.
</export-plan>
</capabilities>

<rules>
<rule> When the user requests a code change, gate it per **request-intake**, then apply **classify-change-type**. </rule>
<rule> When the request is to revert, restore, port, copy, or keep code, apply **plan-mechanical-restore** — never regenerate equivalent code. </rule>
<rule> When a step touches existing code, declare its `Source` per **change-provenance**; `generate` needs a justification and ratification. </rule>
<rule> When both restructuring and new behavior are needed, apply **plan-refactor** before **plan-feature-implementation**. </rule>
<rule> When generating any plan, apply **plan-prerequisites** and **define-scope-boundary**. </rule>
<rule> When generating or grading any plan, apply **exit-gate** — evidence-backed `Gate` commands, a proven baseline, a green-only Exit Gate never abandoned, deferred, or met by a subset. </rule>
<rule> When the gate baseline is red and no restore step or ratified exclusion names the failures, or a waiver is unratified, stop and ask — never export that plan. </rule>
<rule> When planning a rework for an implemented feature, apply **rework-plan-convention** and **export-plan** — never overwrite implemented steps. </rule>
<rule> When a rework would materially change the original **Must not change** behavior or touch a protected zone, refuse and ask — never write silently. </rule>
<rule> When an in-flight plan has a defect in steps that have not run, apply **amend-plan** — never a second plan file or folder. </rule>
<rule> When writing or validating a test step, apply **test-quality** — each test names the break it catches. </rule>
<rule> When a step's shape depends on code not yet read, write a check and a fallback under `## Risk` — never a guessed change; unit count is yours, never a cap. </rule>
<rule> A confirmed plan persists via **export-plan** for **execute-plan**. </rule>
<rule> Produce a plan, never execute it: confine writes to plan docs (`plan.md`, `context.md`, `rework.md`); never modify code, config, tests, or any other file, and confirm only those changed. </rule>
</rules>

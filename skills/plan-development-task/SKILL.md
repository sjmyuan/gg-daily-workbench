---
name: plan-development-task
description: Classify, clarify, and generate TDD-based step-by-step plans for bug fixes, features, refactors, or POCs, and amend in-flight plans. Use when fixing bugs, adding features, refactoring, exploring feasibility, planning a POC, restoring, copying, or keeping code, reworking, or amending a plan mid-execution.
---

<when-to-use-this-skill>
- User reports a bug, defect, or unexpected behavior in existing code
- User describes a regression or something that worked before but no longer does
- User reports failing tests or incorrect outputs in existing functionality
- User asks to investigate and fix a problem in existing code
- User submits a requirement to add new functionality or features
- User asks to implement a new feature, enhancement, or behavior
- User wants a POC to prove which option of an ADR is better — a standalone feature (not a snippet) that demonstrates one option
- User describes desired functionality that does not currently exist in the codebase
- User asks an exploratory question about whether a feature is possible (e.g., "is it possible to...", "can we add...", "would it be feasible to...")
- User requests refactoring of existing code or functionality
- User asks for code cleanup, restructuring, or quality improvements
- User wants to reduce technical debt or improve code organization
- User requests improvements to maintainability, readability, or performance without changing behavior
- User wants to plan rework for an already-implemented feature — write a sibling `rework-<date>.md`, a focused rework triggered by orchestrate-feature-delivery's handle-post-implementation-issue flow
- An in-flight plan needs steps added, removed, or reordered before they run — amend the existing plan, never create a second one
- User asks to revert, restore, copy, or keep code unchanged ("same as main") — plan a mechanical restore
- A change already exists in another branch, commit, or PR and must be brought over as-is

**Differentiation rules** (when multiple skills could apply):
- **Multi-feature / multi-repo decomposition?** → Do NOT plan the whole breakdown here — apply **orchestrate-feature-delivery** first, then plan each feature × repo cell with this skill
- **Rework for an already-delivered feature?** → Apply this skill per **rework-plan-convention** — write a sibling `rework-<date>.md`; orchestrate-feature-delivery triggers it; never rewrite the implemented plan
- **Defect in a plan that is mid-execution?** → Apply **amend-plan** — adjust pending steps in the same `plan.md`; never create a second plan file
- **Target state already exists in a ref, commit, or file?** → Plan a mechanical restore per **change-provenance**
</when-to-use-this-skill>

<knowledge>

<change-provenance>
Every code step declares where its code comes from: `no-op` · `base` · `port` · `copy` · `edit` · `generate`.
Generate only when no cheaper source reaches the target state.
A revert, "same as main", or "leave it" request is a mechanical restore, not a TDD change.
Enum, intent router, ladder, restore-plan shape: **[reference/provenance-first.md](reference/provenance-first.md)**.
</change-provenance>

<change-type-classification>
Classify the user's request into one of these types; a mechanical target is detected first and routes to **plan-mechanical-restore**.

| Signal | Type | Reasoning |
|---|---|---|
| "bug", "broken", "error", "exception", "not working", "incorrect", "wrong output", "failing", "regression" | **Bug Fix** | Something is producing incorrect or unexpected results |
| "new", "add", "implement", "create", "support", "enhance", "extend", "feature", "capability" | **Feature** | New observable behavior is being introduced |
| "refactor", "clean up", "restructure", "extract", "organize", "improve quality", "reduce debt", "split", "consolidate" | **Refactor** | Internal structure changes without behavior change |
| "poc", "proof of concept", "prove which option", "compare approaches", "validate option" | **POC** | An uncertain ADR option needs evidence — build a standalone feature that demonstrates it (see **poc-plan-definition**) |

When unsure, ask the user: "Is the goal to fix something that's broken (bug), add new behavior (feature), or restructure without changing behavior (refactor)?"
</change-type-classification>

<tdd-approach-selection>
TDD variant is selected by change type and sub-type — table in **[reference/tdd-approach-selection.md](reference/tdd-approach-selection.md)**. The plan documents the chosen variant with rationale.
</tdd-approach-selection>

<test-quality>
Every planned test names the production change it catches and exercises real behavior, not mocks. Full rubric: **[reference/test-quality.md](reference/test-quality.md)**.
</test-quality>

<tdd-guardrails>
No behavior change without a failing test first; only non-behavioral changes may skip test creation, with a recorded justification. Hard-to-test work is a design smell — refactor first. Full rubric: **[reference/tdd-guardrails.md](reference/tdd-guardrails.md)**.
</tdd-guardrails>

<plan-prerequisites>
Every plan starts with a **Prepare Environment** step (Step 1) covering only the checks execution needs:

| Check | Not ready → |
|---|---|
| Feature branch exists, based on the correct base branch, named per the **repo's branch convention** (detect from existing branches / git config / team docs, or ask — never assume a prefix) | Ask the user for the branch name and base; create the branch as part of Step 1 |
| No uncommitted changes overlapping the plan's work | Ask before proceeding; leave unrelated changes untouched |
| Dependencies and toolchain resolve for the plan's commands | Stop and raise to the user (request install or confirmation) |
| Baseline tests / lint / type-check pass for the affected area | Stop and raise to the user (decide: fix baseline first or proceed) |

Do not require a pristine tree or a green full suite. Never stash, revert, or commit the user's unrelated changes. The branch name and base are recorded so **export-plan** can persist them to `context.md`.
</plan-prerequisites>

<scope-boundary>
Every plan carries a **Scope Boundary** that gates on behavior, never file paths:

| Zone | Content | Executor action |
|---|---|---|
| **Behavior gate** | **May change** / **Must not change** behaviors, contracts, ADR decisions | Change outside **May change** → stop and ask |
| **Protected zones** | Schema/migrations, infrastructure, secrets, public API, other ADRs | Any touch → stop and ask, unless **May change** names it |
| **Expected files** | Files likely to change — advisory | Unlisted, behavior-neutral change → proceed and log |

Stop only on **material** change: behavior outside **May change**, protected-zone touch, objective unverified after two attempts, irreversible action, or a change to *what* is built. Incidental changes (formatting, whitespace, imports, lockfiles, comments/docs, own tests) proceed with a one-line note. Validation stays behavioral; commit hashes and messages are never contractual.

The boundary derives from the change type, confirmed scope, and governing ADR; the user ratifies it before **export-plan** persists it. Reworks inherit and tighten it. Full rubric: **[reference/scope-boundary.md](reference/scope-boundary.md)**.
</scope-boundary>
<poc-plan-definition>
A POC plan (from **orchestrate-feature-delivery**'s **poc-definition**) is a **normal feature plan** for one ADR option — a standalone slice, never a snippet:

| Property | Content |
|---|---|
| `type` | `poc` |
| **ADR / Option** | The decision under test and the option implemented |
| **Success criteria** (optional) | The user's review checklist; not a plan step |
| **Scope Boundary** | **May change** = the option's target area; **Must not change** = other options and ADRs |

The plan implements the option exactly like a feature. It never measures or evaluates; the MR is the user's evaluation vehicle.
</poc-plan-definition>

<plan-amendment>
Adjust an in-flight plan **in place** — never fork a second plan file:
- Amend when the defect is in steps that have **not run**; rework when executed behavior must change.
- ✅ steps are frozen; append with the next number or insert with a letter suffix (`3a`); mark obsolete pending steps `⏭ abandoned — <reason>`; never renumber.
- Record one `## Amendments` row in `context.md`; plan path and cell status stay unchanged.
Full rules: **[reference/plan-amendment.md](reference/plan-amendment.md)**.
</plan-amendment>

<rework-plan-convention>
A rework (triggered by **orchestrate-feature-delivery**'s **handle-post-implementation-issue**) is written as a new sibling file `rework-<date>.md` in the feature folder — `plan.md` is the frozen original and is never modified:
- Applies only when executed or delivered behavior must change; pending-step defects are amended in place via **amend-plan**
- Each file opens with `# Rework <date>` + one-line trigger, then its own **Scope Boundary**, **Done means**, and numbered delta steps
- Carries only the delta — never restates the original plan or the charter; inherits `context.md` **Must hold** / **Pointers** by reference and never creates a second `context.md`
- Inherits and tightens the original **Scope Boundary** to the governing ADR decision
- Refuses and asks the user only on a material change: original **Must not change** behavior, a protected zone, or reopening another ADR (likely a new feature cell)
- Runs on its own branch (see **plan-prerequisites**)
- Registers a row in the feature's `## Reworks` manifest in `context.md` (date, mode, cell, trigger, file, status) so resume finds the active file

Worked example: [examples/rework-scope-boundary.md](examples/rework-scope-boundary.md).
</rework-plan-convention>

<concise-writing>
All `plan.md` / `context.md` prose follows **reference/writing-style.md** — BLUF takeaways, hard caps (1 sentence per step objective / bullet / ≤20-word sentence), atomic bullets, no banned phrases. Plan files are table-first; context files are takeaway-first.

`context.md` is the cell's **charter**, not a workbook: target **40–60 lines**, hard ceiling **8,000 chars / 120 lines**. It holds why, must-hold invariants, unknowns, done criteria, pointers, and state — never steps, plan decisions, pre-flight evidence, or logs. One artifact, one job: `index` = state · `context` = charter · `plan` = execution · `rework` = delta · git/PR = record. Template and admission test: **reference/doc-budgets.md**.
</concise-writing>

<context-loading-guide>
Load only the examples directly relevant to the current change type to minimize context size.

| Load when | Provides | File |
|---|---|---|
| Planning a revert, restore, port, copy, or no-op change | Source enum, intent router, ladder, restore-plan shape, anti-patterns | [reference/provenance-first.md](reference/provenance-first.md) |
| Writing a mechanical restore plan end to end | Revert-to-base walkthrough with `Must match` and equality proof | [examples/mechanical-restore-plan.md](examples/mechanical-restore-plan.md) |
| Selecting TDD variant per sub-type | 15-row TDD approach selection table | [reference/tdd-approach-selection.md](reference/tdd-approach-selection.md) |
| Writing or validating test steps | Test-quality rules and the mutation check | [reference/test-quality.md](reference/test-quality.md) |
| Choosing a streamlined path or hitting testability problems | Iron Law, rationalizations to reject, red flags, design signals | [reference/tdd-guardrails.md](reference/tdd-guardrails.md) |
| Generating bug fix plan | Detailed steps for plan-bug-fix | [reference/plan-bug-fix.md](reference/plan-bug-fix.md) |
| Generating feature implementation plan | Detailed steps for plan-feature-implementation | [reference/plan-feature-implementation.md](reference/plan-feature-implementation.md) |
| Generating refactor plan | Detailed steps for plan-refactor | [reference/plan-refactor.md](reference/plan-refactor.md) |
| Validating plan quality | Checklist: coverage, sequencing, steps, TDD, clarity | [reference/plan-quality-checklist.md](reference/plan-quality-checklist.md) |
| Writing or ratifying the Scope Boundary block | Zones (incl. `Must match`), materiality test, stop-vs-log rubric | [reference/scope-boundary.md](reference/scope-boundary.md) |
| Amending an in-flight plan (defective pending steps) | Amend-vs-rework rule, ⏭ abandoned status, `## Amendments` row | [reference/plan-amendment.md](reference/plan-amendment.md) |
| Writing a rework plan (`rework-<date>.md`) for an implemented feature | Sibling rework file + manifest (shared with the orchestrator) | [../orchestrate-feature-delivery/examples/post-implementation-rework.md](../orchestrate-feature-delivery/examples/post-implementation-rework.md) |
| Rework that risks changing **Must not change** behavior | Boundary definition + refusal with decision options | [examples/rework-scope-boundary.md](examples/rework-scope-boundary.md) |
| Amending an in-flight plan after execution stops | Amend-in-place walkthrough with ⏭ abandoned and `## Amendments` row | [examples/amend-mid-execution.md](examples/amend-mid-execution.md) |
| Bug: simple logic / timing errors | Full workflow example | [examples/bug-fix-simple-logic.md](examples/bug-fix-simple-logic.md) |
| Bug: slow responses, N+1 queries | Full workflow example | [examples/bug-fix-performance.md](examples/bug-fix-performance.md) |
| Feature: complex algorithms or business rules | Full workflow example | [examples/feature-complex-transformation.md](examples/feature-complex-transformation.md) |
| Feature: simple config properties or flags | Full workflow example | [examples/feature-simple-configuration.md](examples/feature-simple-configuration.md) |
| Refactor: splitting large classes (SRP) | Full workflow example | [examples/refactor-service-splitting.md](examples/refactor-service-splitting.md) |
| Refactor: interface extraction for testability | Full workflow example | [examples/refactor-interface-implementation.md](examples/refactor-interface-implementation.md) |
| Planning a POC (normal feature implementing one ADR option) | POC metadata + feature-plan steps; no measurement step | [reference/plan-poc.md](reference/plan-poc.md) |
| Full POC plan walkthrough | plan-poc end-to-end output | [examples/plan-adr-option-poc.md](examples/plan-adr-option-poc.md) |
| POC round from dispatch to decision gate (shared with the orchestrator) | End-to-end POC walkthrough | [../orchestrate-feature-delivery/examples/adr-option-poc.md](../orchestrate-feature-delivery/examples/adr-option-poc.md) |
| Persisting a confirmed plan to `plan.md` + `context.md` | plan.md + context.md layout for **export-plan** | [examples/export-plan.md](examples/export-plan.md) |
| Turning a long planning draft into a 40–60-line charter | Section triage, before/after, responsibility check | [examples/context-charter.md](examples/context-charter.md) |
| Writing, updating, or validating `context.md` / `index.md` size | Charter template, admission test, artifact responsibilities, caps | [reference/doc-budgets.md](reference/doc-budgets.md) |
| Deciding whether a fact belongs in spike artifacts or the cell docs | Two-plane map, handoff contract, edit ownership | [../conduct-spike/reference/artifact-map.md](../conduct-spike/reference/artifact-map.md) |
</context-loading-guide>

<skill-boundary>
This skill produces a **plan** but does not execute changes. After the plan is confirmed, use **export-plan** to persist it to a feature folder, then pair with **execute-plan** for implementation.
</skill-boundary>

<write-boundary>
Writes are confined to plan docs — `plan.md`, `context.md`, and sibling `rework-<date>.md`. Never modify code, config, tests, or any other file; **execute-plan** performs all code changes. On opencode the planner agent's `edit` permission denies every non-markdown file. After persisting, confirm only plan docs changed; stop and report on any out-of-scope change.
</write-boundary>

</knowledge>

<capabilities>

<classify-change-type>
1. Detect a mechanical target first per **change-provenance**; route reverts, restores, ports, copies, and keeps to **plan-mechanical-restore**.
2. Read the user's request and identify keywords and signals that indicate the type of change.
3. Consult **change-type-classification** knowledge to map signals to a change type (bug fix, feature, or refactor).
4. If the type is ambiguous, ask the user targeted clarifying questions to disambiguate.
5. Present the classified type and reasoning to the user.
6. Route to the appropriate pair of capabilities based on the classified type:
   - **Mechanical (revert / restore / port / copy / no-op)** → apply **define-scope**, then **plan-mechanical-restore**
   - **Bug Fix** → apply **define-scope**, then **plan-bug-fix**
   - **Feature** → apply **define-scope**, then **plan-feature-implementation**
   - **Refactor** → apply **define-scope**, then **plan-refactor**
   - **POC** → apply **plan-poc**
</classify-change-type>

<plan-mechanical-restore>
**Objective**: Plan a revert, restore, port, copy, or no-op without regenerating code.

1. Apply **change-provenance**: record the trigger verbatim, the pinned `Ref`, and `Source`/`Equality` per path.
2. Ask for the source ref when the request names none; never infer the baseline.
3. Apply **define-scope-boundary**: list every restored path under `Must match` with its ref.
4. Skip RED/GREEN; record the non-behavioral justification per **tdd-guardrails**.
5. Write steps as prepare environment → per-path restore naming the git operation → equality proof → test run.
6. Validate against the restore checks in **[reference/provenance-first.md](reference/provenance-first.md)**.
</plan-mechanical-restore>

<define-scope>
1. Gather relevant information from the codebase, knowledge base, test results, and user input to define the scope for the classified change type.
2. **Bug fix**: analyze root-cause patterns and test hypotheses through code inspection, debugging, or logging.
   **Feature / refactor**: identify and clarify ambiguous terms and implicit assumptions.
   **Mechanical**: confirm the source ref, the exact paths, and whether any other commit touched them since.
3. Ask the user targeted questions until the scope is well-defined — root cause confirmed for bugs; requirement or constraints confirmed for features/refactors.
4. Present the result (root cause + reasoning, or a structured scope summary) and request confirmation or refinements.
5. Hand the confirmed scope to the corresponding plan capability and **define-scope-boundary**.
</define-scope>

<plan-bug-fix>
Load **[reference/plan-bug-fix.md](reference/plan-bug-fix.md)** and follow its steps.
</plan-bug-fix>

<plan-feature-implementation>
Load **[reference/plan-feature-implementation.md](reference/plan-feature-implementation.md)** and follow its steps.
</plan-feature-implementation>

<plan-refactor>
Load **[reference/plan-refactor.md](reference/plan-refactor.md)** and follow its steps.
</plan-refactor>
<plan-poc>
Load **[reference/plan-poc.md](reference/plan-poc.md)** and follow its steps.
</plan-poc>

<define-scope-boundary>
1. Derive the zones from the classified change type, the confirmed scope, and (for **orchestrate-feature-delivery** cells) the governing ADR decision.
2. List **May change** behaviors/contracts and **Must not change** behaviors/contracts — name observable effects, not just paths.
3. Add `Must match` for every restored or ported path with its ref — the only zone requiring byte equality (see **change-provenance**).
4. List **Expected files** as advisory, plus any **Protected zone** additions.
5. Apply the materiality test (see **scope-boundary**) to every candidate exclusion; keep stop triggers material-only.
6. Present the zones to the user and request ratification or adjustment.
7. Hand the ratified boundary to the plan for inclusion as a `## Scope Boundary` block and to **export-plan** for persistence.
</define-scope-boundary>

<amend-plan>
1. Read the active plan, its statuses, and `context.md` `## Amendments`.
2. Confirm the defect sits in pending steps; if it changes executed behavior, apply **rework-plan-convention**.
3. Freeze every ✅ step and its notes byte-for-byte.
4. Add steps with the next number, or insert with a letter suffix (`3a`, `3b`) when the new work must run earlier; mark obsolete pending steps `⏭ abandoned — <reason>`; never renumber or delete.
5. Tighten the boundary; widen it only with user ratification (see **define-scope-boundary**).
6. Record one `## Amendments` row, keep `context.md` within **doc-budgets**, validate the amendment checks in **reference/plan-quality-checklist.md**, and show the step diff.
</amend-plan>

<export-plan>
1. If the feature folder already holds a `plan.md`, do not write a second plan — apply **amend-plan** instead.
2. After the user confirms the plan, ask whether they would like to persist it to a feature folder for later execution by **execute-plan**.
3. Determine the storage location: for an **orchestrate-feature-delivery** cell use `deliveries/<epic-name>/{repo}/{feature-name}/`; otherwise resolve the artifact base via `resolve-artifact-location` and use `{base}/feature-implementations/` (no silent default).
4. Derive a short kebab-case feature name from the plan's objective (e.g., `fix-null-pointer-in-transformer`).
5. Use the **repo-first** layout `{location}/{repo}/{feature-name}/` when a repo applies (the delivery folder already exists); else `{location}/{feature-name}/`.
6. Write `plan.md` + `context.md` per **[reference/plan-file-format.md](reference/plan-file-format.md)** and the template in **reference/doc-budgets.md**.
7. Validate conciseness (see **concise-writing**): one objective per step sentence, one claim per scope-boundary bullet, context.md prose ≤3 sentences per paragraph, no banned phrases.
8. Curate `context.md` to the charter: target **40–60 lines** (hard ceiling 8,000 chars / 120 lines). Apply the **admission test** — pre-flight evidence is synthesized into a plan decision or an Unknown, never pasted. Over budget → remove duplication with `plan.md`. Never create a log file; git/PR are the history. Re-measure before writing.
9. Inform the user of the saved location so they can invoke **execute-plan** to carry it out.
</export-plan>

</capabilities>

<rules>

<rule> When the user makes a request about code changes, first apply **classify-change-type** to determine whether it is a mechanical restore, bug fix, feature, refactor, or POC. </rule>
<rule> When the request is to revert, restore, port, copy, or keep code unchanged, apply **plan-mechanical-restore** — never regenerate equivalent code. </rule>
<rule> When a step touches existing code, declare its `Source` per **change-provenance**; `generate` needs a justification and ratification. </rule>
<rule> If the classified type is **Bug Fix**: apply **define-scope**, then **plan-bug-fix**. </rule>
<rule> If the classified type is **Feature**: apply **define-scope**, then **plan-feature-implementation**. </rule>
<rule> If the classified type is **Refactor**: apply **define-scope**, then **plan-refactor**. </rule>
<rule> If the classified type is **POC**: apply **plan-poc**. </rule>
<rule> When both restructuring and new behavior are needed: apply **plan-refactor** first, then **plan-feature-implementation**. </rule>
<rule> After the plan is confirmed: optionally apply **export-plan** to persist it for execution by **execute-plan**. </rule>
<rule> When generating any plan, apply **plan-prerequisites** and **define-scope-boundary**. </rule>
<rule> When planning a rework for an implemented feature, apply **rework-plan-convention** and **export-plan** to write a sibling `rework-<date>.md` — never overwrite implemented steps. </rule>
<rule> When writing, amending, or validating `context.md`, apply **doc-budgets** — make it a 40–60-line charter, discard pre-flight evidence, delete resolved unknowns, and never restate a fact that lives in `plan.md`. </rule>
<rule> When a rework would materially change the original **Must not change** behavior or touch a protected zone, refuse and ask the user — never write silently. </rule>
<rule> When an in-flight plan has a defect in steps that have not run, apply **amend-plan** — never write a second plan file or folder. </rule>
<rule> When writing or validating any test step, apply **test-quality** — each test names the break it catches and exercises real behavior. </rule>
<rule> When a plan uses a streamlined or test-skipping path, confirm the change is non-behavioral and record the justification in `context.md`. </rule>
<rule> When testability blocks planning, apply **plan-refactor** before **plan-feature-implementation**. </rule>
<rule> Confine every write to plan docs (`plan.md`, `context.md`, `rework-<date>.md`); never modify code, config, tests, or any non-markdown file. </rule>

</rules>

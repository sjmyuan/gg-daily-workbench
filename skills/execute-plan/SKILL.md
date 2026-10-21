---
name: execute-plan
description: Execute structured development plans with progress tracking, validation, and recovery. Use when executing, resuming, recovering, or reviewing an executed plan from plan-development-task, or a delivery cell / rework from orchestrate-feature-delivery.
---

<when-to-use-this-skill>
- You need to execute an outlined plan (implementation plan, refactoring plan, or bug-fix plan)
- A structured plan from plan-development-task needs to be carried out with progress tracking and validation checkpoints
- A previously started plan needs to be resumed after interruption or context reset
- All plan steps are complete and a post-execution review with the review-code skill is needed
- A step has failed or is blocked and needs error recovery before proceeding
- A delivery index from orchestrate-feature-delivery points to planned feature × repo cells ready for execution
- You need to execute a POC plan (a standalone feature proving one ADR option) and stop at an evaluation report for the decision gate
- You need to execute a rework plan (`rework-<date>.md`, triggered by orchestrate-feature-delivery) — run only the rework file's steps, never re-run the completed original steps
- Do NOT load when no plan has been generated yet — if the user describes a problem without referencing an existing plan, let plan-development-task handle it first
</when-to-use-this-skill>

<knowledge>

<step-status-definitions>
Status emojis used to track each step:

| Status | Emoji | Meaning |
|---|---|---|
| Pending | ⏳ | Not yet started |
| In Progress | 🔄 | Currently being worked on |
| Completed | ✅ | Successfully finished |
| Failed | ❌ | Encountered errors (include error details) |
| Blocked | 🚫 | Cannot proceed (include blocker details) |
</step-status-definitions>

<step-tracking-format>
Record each step in `plan.md` with the `### Step N: [Title] [emoji]` block (Objective / Files / Implementation / Validation / Status, one line per fact, see **concise-writing**) per **reference/step-tracking-format.md**.
</step-tracking-format>

<feature-folder-structure>
Each feature lives in its own folder with `plan.md` (live step tracking) + `context.md` (background material + execution handoff); POC plans add `evaluation-report.md`. The core files are a permanent record — never deleted. Layout, naming, and repo-first rules: **reference/feature-folder-structure.md**.
</feature-folder-structure>

<plan-input-schema>
A plan consumed by this skill is numbered steps, each with number/title/objective; it may come as a `plan.md` file, a plan summarized in conversation, or an ad-hoc plan — materialized into `plan.md` per **reference/plan-input-schema.md**.
</plan-input-schema>

<commit-conventions>
Small-step commit rules (frequency, size, message format/content, staging, push gating, pre-commit check): **reference/commit-conventions.md**.
</commit-conventions>

<code-comment-conventions>
Generated code must match the repo's comment style (rubric: **reference/code-comment-style.md**):
- Default is **zero comments** — write code first, add why-comments only on a second pass
- Comments explain **why** — non-obvious intent, workarounds, invariants, edge cases — never restate the **what**
- Before commenting, rename the symbol or extract a helper instead
- No process narration: plan-step references, "added/generated" markers, section banners, AI/tool mentions
- Match the repo's density — sparse repo gets sparse comments; docstrings only where the repo uses them (public API only)
- Line comments ≤ 15 words
- Detected during **verify-prerequisites** (policy + one exemplar recorded in the plan note); enforced at write time in **execute-step** and as a deterministic pattern scan in **commit-step**
</code-comment-conventions>

<test-placement>
Before writing tests, check existing coverage first and prefer extending existing test files; create a new file only when no natural home exists per **reference/test-placement.md**.
</test-placement>

<rework-plan-execution>
Rework mode: a rework is a sibling `rework-<date>.md`; run only its steps; resume via the `## Reworks` manifest. Full mode: **reference/execution-modes.md**.
</rework-plan-execution>
<poc-execution-mode>
POC mode: run like a feature on a **POC branch**, stop after the final **evaluation step**; never merge before the gate. Full mode: **reference/execution-modes.md**.
</poc-execution-mode>

<scope-boundary-check>
The plan's `## Scope Boundary` gates on **behavior**, never file paths. **May change / Must not change** is the gate; **Protected zones** (schema, infrastructure, secrets, public API, other ADRs) stop unless **May change** names them; **Expected files** is advisory.
- Incidental (formatting, whitespace, imports, lockfiles, generated, comments/docs, own tests) → proceed; note when unplanned.
- Material (behavior outside **May change**, protected-zone touch, objective unverified after two attempts, irreversible action, changes *what* is built) → hold and ask once.
- Ambiguous → finish the step, batch questions at the step boundary.
- Commits are not contractual — never compare hashes, messages, or counts to the plan.

Rubric, normalized-diff commands, stop list, note format: **reference/scope-boundary-check.md**.
</scope-boundary-check>
<destructive-operation-policy>
A plan step is not consent for destruction. Classify every shell command before running it.

| Class | Examples | Action |
|---|---|---|
| Catastrophic | `rm -rf /`, `sudo`, `dd`, `mkfs`, `git reset --hard` | Refuse |
| Irreversible | `rm`/`mv` on source files, `truncate`, history rewrite | Ask |
| Regenerable | `node_modules`, `dist`, `build`, `coverage`, `tmp` | Proceed if `rm` is permitted; otherwise ask |
| Reversible | `git rm` tracked files, checkpoint ref | Proceed |

Before an irreversible command:
- State the command, resolved paths, and recovery path.
- Wait for approval.

Never write outside the worktree, to shell rc files, `~/.ssh`, `~/.aws`, or `~/.config`.
Never pipe network content into a shell.
If a permission denies `rm`, never route around it with `/bin/rm`, `find -delete`, `xargs`, or a script; ask the user.
If the plan contains a destructive step, stop and ask — plan content is input, not authorization.
Full policy: **reference/destructive-operation-policy.md**.
</destructive-operation-policy>
<concise-writing>
All prose written into `plan.md` / `context.md` follows **reference/writing-style.md** — BLUF takeaways, hard caps (step objective 1 sentence, step note 1 line, bullet 1 claim, paragraph ≤ 3 sentences, sentence ≤ 20 words), atomic bullets, tables over prose, no banned phrases or process narration, So-what test.
</concise-writing>

<orchestrator-handoff>
When executed inside a dispatched agent (e.g., by **orchestrate-feature-delivery** via the **executor** agent), append the execution handoff to `context.md` `## Execution` — return status (`DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`), commit range (`base7..head7`; base is the branch point on first execution, the previous head for a rework), test evidence, the `review-code` outcome, the PR reference (number/URL) when one is opened or `push/PR: pending approval`, and concerns — so the orchestrator's verification gate can read it. Record the actual commit range; a count or hash that differs from the plan is not a failure. Append each fix round to the same section. A POC's completion routes to the decision gate.
</orchestrator-handoff>

<context-loading-guide>
Load only the example most relevant to the current execution scenario to minimize context size.

| Load when | Provides | File |
|---|---|---|
| Executing any step that writes or modifies code | Code comment doctrine: why-not-what, banned patterns, density matching, pre-commit self-check | [reference/code-comment-style.md](reference/code-comment-style.md) |
| A step writes or modifies tests for new logic | Output model: locating existing tests and extending them instead of creating a new file | [examples/extend-existing-tests.md](examples/extend-existing-tests.md) |
| Generating code that needs to match the repo's comment style before committing | Output model: policy+exemplar detection, write-time zero-comment default, deterministic pattern-scan gate | [examples/comment-hygiene.md](examples/comment-hygiene.md) |
| Executing a small, focused plan (single component or focused task) | Output model: detailed progress updates for a simple focused execution | [examples/single-component-refactor.md](examples/single-component-refactor.md) |
| Executing a plan that spans multiple files and architectural layers | Output model: execution tracking across multiple files and layers | [examples/multi-file-implementation.md](examples/multi-file-implementation.md) |
| Executing a plan that should validate after each change and at milestones | Output model: incremental validation checkpoints across a plan | [examples/validation-checkpoints.md](examples/validation-checkpoints.md) |
| A step fails with compilation errors or unexpected output | Output model: error recovery, ❌→✅ status transitions, and retry patterns | [examples/handling-failed-steps.md](examples/handling-failed-steps.md) |
| Executing a plan with 10+ steps requiring context preservation | Output model: long plan progress tracking and context continuity | [examples/long-plan-execution.md](examples/long-plan-execution.md) |
| All plan steps are complete and post-execution review is needed | Output model: applying review-code after completion, adding fix steps, keeping plan as permanent record | [examples/post-execution-review.md](examples/post-execution-review.md) |
| Executing a plan with prerequisite checks, one commit per step, and push approval at the end | Output model: verify-prerequisites, commit-step, and request-push-approval in action | [examples/small-step-commits.md](examples/small-step-commits.md) |
| Executing a rework plan (`rework-<date>.md` — run only the rework steps) | Rework execution walkthrough (shared with the orchestrator) | [../orchestrate-feature-delivery/examples/post-implementation-rework.md](../orchestrate-feature-delivery/examples/post-implementation-rework.md) |
| Executing a POC plan (stop at evaluation report, no merge) | POC execution mode + evaluation report walkthrough | [examples/execute-adr-option-poc.md](examples/execute-adr-option-poc.md) |
| POC round from dispatch to decision gate (shared with the orchestrator) | End-to-end POC walkthrough | [../orchestrate-feature-delivery/examples/adr-option-poc.md](../orchestrate-feature-delivery/examples/adr-option-poc.md) |
| A step, recovery fix, or review fix may be material against the plan's boundary | Output model: refusal + decision options | [examples/refusing-out-of-scope-rework.md](examples/refusing-out-of-scope-rework.md) |
| A change touches unlisted files, looks cosmetic, or a commit differs from the plan | Three zones, materiality test, closed stop list, normalized diff, note format | [reference/scope-boundary-check.md](reference/scope-boundary-check.md) |
| Formatting, whitespace, lockfile, or commit-message drift appears mid-step | Output model: proceed-and-log instead of stopping | [examples/incidental-deviation.md](examples/incidental-deviation.md) |
| A step runs a shell command that deletes, moves, or overwrites files | Classification table, approval template, recovery ref, rationalizations | [reference/destructive-operation-policy.md](reference/destructive-operation-policy.md) |
| A plan step itself asks for a destructive command | Output model: refusal, options, blocked status | [examples/refuse-destructive-command.md](examples/refuse-destructive-command.md) |
</context-loading-guide>

</knowledge>

<capabilities>

<track-plan>
1. Locate or create the feature folder and its two files (`plan.md` + `context.md`) per **reference/feature-folder-structure.md**; for an **orchestrate-feature-delivery** cell use the existing `deliveries/<epic-name>/{repo}/{feature-name}/`, otherwise resolve the artifact base via `resolve-artifact-location` and use `{base}/feature-implementations/{feature-name}/`.
2. Derive a short kebab-case feature name from the plan's objective (e.g., `add-auth-system`, `fix-null-pointer-in-transformer`) per **reference/feature-folder-structure.md**.
3. Before creating a new plan, check whether the feature folder already exists with a plan file.
4. If the folder contains a sibling `rework-<date>.md` (per the `context.md` manifest), execute only the active rework file's steps (see **rework-plan-execution**); never re-run or modify the completed original steps.
5. If a plan file has steps with ❌ failed or 🚫 blocked status, ask the user whether to **resume** from the last known state or **start fresh** (create a new folder/overwrite).
6. Materialize the plan into `plan.md` per **reference/plan-input-schema.md**: list each step with its number, title, objective (one sentence each, see **concise-writing**), and initial status ⏳ pending, per **reference/step-tracking-format.md**.
7. Populate `context.md` concisely (see **concise-writing**): one bolded takeaway per section, tables for requirements/constraints, compact bullet lists for references — requirements docs, ADRs, user stories, spike findings, codebase references, constraints, assumptions, decisions.
8. Update step status in the plan file immediately after each state change (⏳ → 🔄 → ✅, or ❌/🚫 on failure); keep each note to one line per fact. Refer to **step-status-definitions** for emoji meanings.
9. Never modify plan structure, objectives, steps, or the **Scope Boundary** block except to update statuses or add clarifying notes.
10. Report progress at plan start: show all steps with ⏳ pending.
11. After each step completion, show the full list with current statuses and per-step details (files, implementation, validation); never summarize multiple steps together.
12. At plan end, show the final all-✅ list with a summary of accomplishments.
</track-plan>

<execute-step>
1. Before starting a step, mark it as 🔄 in-progress in the plan file and briefly explain your approach. Apply **check-scope-boundary** — hold and ask only when the step requires a material change; proceed on incidental drift.
2. Execute the step fully — no partial implementations.
3. When writing or modifying code, restate the repo's comment policy + exemplar from the plan note (see **code-comment-conventions**), then write comment-minimal: default to zero comments, prefer renaming/extracting over commenting, add why-comments only on a second pass (≤ 15 words each).
4. If the step writes or modifies tests, apply **place-tests** before writing any test code — locate existing tests and prefer extending them over creating new files.
5. After completing the step, validate the outcome meets the step's objectives.
6. Mark the step as ✅ completed; document files changed, implementation details, and validation results in the plan file.
7. Confirm the prerequisite step is fully ✅ completed before starting a step that depends on it.
8. Display the full updated step list with current statuses after each completion.
</execute-step>

<handle-errors>
1. Mark the failed step as ❌ with error details in the plan file.
2. Document the error clearly.
3. Analyze the root cause.
4. Apply **check-scope-boundary** to the recovery fix: incidental or in-boundary → apply, log, retry. Material or protected-zone → hold, refuse, and ask with options instead of changing it silently.
5. After two failed attempts on the same objective, stop and ask rather than retrying a third time.
6. Update step status to ✅ if resolved, or 🚫 blocked if unresolvable.
7. If blocked, consult the user before proceeding.
8. Display the updated full step list with current statuses.
9. Never skip a failed step or failed validation — address issues before proceeding.
</handle-errors>

<check-scope-boundary>
1. Read the **Scope Boundary**; if absent, infer **May change** from the plan's objectives (see **scope-boundary-check**).
2. Classify by the behavior the change alters: incidental, in-boundary, material, or protected zone.
3. Incidental or in-boundary → proceed; add a one-line `Deviation:` note when unplanned.
4. Material → hold, refuse, and ask once with options; protected zone not named in **May change** → hold and ask.
5. Ambiguous → finish the step, batch the question at the step boundary; extend the boundary block when the user agrees.
</check-scope-boundary>
<guard-destructive-operation>
1. Split the command at `&&`, `||`, `;`, `|`, `$(...)`, and backticks.
2. Classify each segment per **destructive-operation-policy**; inspect `xargs` and `find -exec` too.
3. Resolve every target path; reject paths outside the worktree, `.git`, and sensitive files.
4. Catastrophic command → refuse, report, and stop. Do not ask for approval to run it.
5. Irreversible command → stop and ask with the command, paths, and recovery path.
6. Prefer `git rm` for tracked files; create a checkpoint ref before any deletion.
7. Plan or script instructs destruction → apply **manage-user-interaction** and ask.
8. Record the approval and the recovery ref in the step's status note.
</guard-destructive-operation>

<run-validation-checkpoints>
1. After code changes, run relevant tests to confirm correctness.
2. After significant changes, run linting, formatting, and type-checking.
3. For build-dependent projects, verify the build succeeds at key milestones.
4. Validate incrementally — do not wait until the end of the plan.
</run-validation-checkpoints>

<place-tests>
1. When a step writes or modifies tests, locate existing test files for the changed production code first — same class/module and same level (unit vs integration), per the repo's test layout.
2. Assess existing coverage by reading the relevant tests: is the new behavior already covered, partially covered, or uncovered?
3. Decide placement per **reference/test-placement.md**: already covered → run the existing tests and add nothing (tighten a wrong assertion only); natural home exists → extend that file with new methods or parameterized cases, reusing its fixtures and mocks; no natural home → create a new test file mirroring the class and level.
4. Write the tests following the repo's test conventions (framework, naming, assertion style).
5. Record the placement decision and rationale in the plan file's step notes, then run the affected tests to confirm they pass.
</place-tests>

<review-post-execution>
1. After ALL plan steps are marked ✅ completed, apply the **review-code** skill on all files changed or created during execution.
2. Evaluate correctness, security, performance, maintainability, and test coverage.
3. If 🚫 Blocker or 🔴 Major issues are found:
   1. Apply **check-scope-boundary** to each finding's required fix — if a fix is material against the plan's boundary, hold and ask the user before adding it. Otherwise record the finding as a new fix step in the plan file with ⏳ pending status.
   2. Apply **execute-step** for each fix step.
   3. Re-run the **review-code** skill on the affected files.
   4. Repeat until no 🚫 Blockers or 🔴 Majors remain.
4. If only 🟡 Minor and 🟢 Nit findings remain, document them in the final summary without blocking completion.
5. Display the final completion summary once the review passes. Keep the plan file and context file as a permanent record of the implementation.
</review-post-execution>



<verify-prerequisites>
1. Verify the correct feature branch is checked out; create it if the plan requires one and the user confirms the branch name and base, naming it per the repo's branch convention (detect from existing branches / git config / team docs, or ask; never assume a prefix).
2. Check only what execution needs: dependencies and toolchain resolve for the plan's commands; the affected area's baseline tests/lint pass. Unrelated dirt and unrelated failures are noted, not blocking — leave them untouched.
3. Detect the repo's comment style per **code-comment-conventions** (sample recently modified files, `.editorconfig`, CONTRIBUTING docs) and record a one-line policy + one exemplar comment in the plan note (e.g., `Policy: sparse, why-only, no docstrings · Exemplar: "// keep-alive: pooling beats TLS re-handshake"`).
4. If a necessary check fails (wrong branch, missing dependency, affected-area baseline broken), STOP and raise it to the user: state what is not ready, what is needed, and ask how to proceed. Never stash, revert, or commit the user's unrelated changes.
5. Record the outcome (ready or blockers) in the plan file before execution begins.
</verify-prerequisites>

<commit-step>
1. After a step is validated and marked ✅, run `git status` and `git diff` to identify the files changed by this step.
2. Stage only the files this step changed — including its formatter or lockfile side effects — never pre-existing or unrelated changes.
3. Scan the staged diff against **code-comment-conventions** — grep for known narration/restatement patterns (`// ====`, `// step N`, `// added|generated|fixed`, AI/tool names) and treat any hit as a blocker for that file.
4. Remove or shorten every flagged comment, any restating comment, and comments exceeding the repo's density; re-stage after trimming.
5. Write a small commit message following **reference/commit-conventions.md**: repo convention if known, else `type(scope): summary`, describing the change neutrally. Treat the plan's message as illustrative, never verbatim.
6. Scan the message for AI-related words (see **reference/commit-conventions.md**) and rewrite until none remain.
7. Commit locally; report the actual commit hash and message. Never push. Hashes, wording, and commit counts are not contractual — drift from the plan is not a failure.
8. If the step produced no code change (e.g., documentation-only), note that no commit is needed.
</commit-step>

<produce-poc-report>
1. After the plan's final evaluation step, collect the measured evidence for each **success criterion** (benchmarks, complexity diff, integration results).
2. Write an **Evaluation Report** into the feature folder (`evaluation-report.md`): per-criterion evidence, a verdict line (meets / misses), and any caveats.
3. Do NOT push or merge — the report feeds the decision gate; ask the user before pushing for review.
</produce-poc-report>

<request-push-approval>
1. When all steps are ✅ complete — or the user asks to sync — summarize the local state: branch name, commits created, and how many commits are ahead of the remote base. For a **POC branch** (see **poc-execution-mode**), pushing is review/evidence only — merging waits for the orchestrator's decision gate.
2. Ask the user explicitly: "Push branch [branch name] to remote?" Wait for a decision.
3. Push only after the user confirms; report success or any errors.
4. If the user declines or defers, leave the branch local and tell them the commits are ready to push whenever they choose.
5. When the user also asks to open a pull/merge request, apply **create-pull-request** after the push — it resolves the PR conventions via **resolve-conventions**, gets approval on the full draft, and records the returned reference (or pending state) in the `## Execution` handoff.
</request-push-approval>

<manage-user-interaction>
1. Execute the full plan autonomously without asking for permission at each step.
2. If a step is ambiguous or requires user input, pause and ask before proceeding.
3. If blocked on a step due to missing information or external dependencies, inform the user and wait for guidance.
4. When deviating from the plan, apply **check-scope-boundary** and explain the adaptation — never deviate silently.
5. Before any push, apply **request-push-approval** — never push without the user's confirmation.
</manage-user-interaction>

</capabilities>



<rules>

<rule> **At Plan Start**: Apply **track-plan** before executing any step. </rule>
<rule> **During Each Step**: Apply **execute-step**. </rule>
<rule> **Throughout Execution**: Apply **track-plan** — keep the step list current and show it after every step. </rule>
<rule> **When a Step Fails**: Apply **handle-errors** immediately. </rule>
<rule> **At Validation Points**: Apply **run-validation-checkpoints** — validate incrementally, not just at the end. </rule>
<rule> **When a Step Writes or Modifies Tests**: Apply **place-tests** before writing test code. </rule>
<rule> **When Facing Ambiguity or Blockers**: Apply **manage-user-interaction** — pause and ask rather than assuming. </rule>
<rule> **After All Steps Complete**: Apply **review-post-execution**. </rule>
<rule> **Before Starting the First Step**: Apply **verify-prerequisites** — raise and wait if the environment is not ready. </rule>
<rule> **After Each ✅ Step**: Apply **commit-step**. </rule>
<rule> **Before Any Push**: Apply **request-push-approval** — never push without user confirmation. </rule>
<rule> **When the User Asks to Open a PR/MR**: Apply **create-pull-request** after the push — it resolves the PR conventions and gets approval on the full draft; never reuse a generic title or body. </rule>
<rule> **When the Folder Contains a Rework Plan**: Apply **track-plan** and **execute-step** to the active `rework-<date>.md` steps only. </rule>
<rule> **When Executed as a Dispatched Agent** (orchestrate-feature-delivery): Apply **orchestrator-handoff** — append the `## Execution` handoff to `context.md` before reporting. </rule>
<rule> **When the Plan is a POC** (type: poc): Apply **track-plan** and **execute-step**; never merge before the decision gate. </rule>
<rule> **After the Final Evaluation Step of a POC**: Apply **produce-poc-report** and route to the decision gate. </rule>
<rule> **When a Step, Recovery Fix, or Review Fix Is Material Against the Boundary, or When Deviating from the Plan**: Apply **check-scope-boundary** — hold and ask with options; log incidental drift instead of stopping. </rule>
<rule> **Before Running Any Shell Command**: Apply **guard-destructive-operation** — refuse catastrophic commands and ask before irreversible ones. </rule>

</rules>
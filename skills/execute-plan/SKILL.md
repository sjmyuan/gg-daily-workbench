---
name: execute-plan
description: Execute structured development plans with progress tracking, validation, and recovery. Prefer the project's own equivalent when one exists. Use when executing, resuming, recovering, or reviewing an executed plan, a delivery cell, or a rework plan.
---

<when-to-use-this-skill>
- You need to execute an outlined plan — implementation, refactor, bug-fix, restore, or a delivery cell's plan
- A structured plan needs carrying out with progress tracking and validation checkpoints
- A started plan needs resuming after interruption or context reset
- All steps are complete and a post-execution review with review-code is needed
- A step failed or is blocked, or a pending step is defective and needs an amendment request
- You need to execute a POC plan and offer an MR for the user's review
- You need to execute a rework plan (`rework-<date>.md`) — run only its steps, never the completed originals
- Do NOT load when no plan exists yet — let plan-development-task handle a described problem first
</when-to-use-this-skill>

<knowledge>
<request-intake>
Gate the request through `clarify-request`'s intake gate: restate the plan path, active rework, base ref, outcome, and itemize inferences. Zero inferences → **track-plan**; anything inferred → ask before step 1.
A mid-execution request is gated the same way before it becomes a step or an amendment — never silently absorbed, never a reason to stop in-scope work. Accepted defaults go to `## Open concerns` as `Assumption (user-accepted, unverified)`.
A seeding brief stating the plan path, rework, base ref, and outcome **is** the gate result: adopt it, ask nothing, never re-detect the folder.
</request-intake>
<plan-format>
Each feature owns a folder holding `plan.md` (live step tracking) and `context.md` (charter + handoff) — permanent; history lives in git/PR: **reference/feature-folder-structure.md**.
Steps are `### Step N: [Title] [emoji]` blocks — Objective / Files / Source / Implementation / Validation / Status: **reference/step-tracking-format.md**, **reference/plan-input-schema.md**.
</plan-format>
<scope-boundary-check>
The `## Scope Boundary` gates on **behavior**, not paths: **Must not change** is the gate, **Protected zones** stop unless **May change** names them, **Expected files** is advisory: **reference/scope-boundary-check.md**.
</scope-boundary-check>
<change-provenance>
Every step carries a `Source` from `no-op` · `base` · `port` · `copy` · `edit` · `generate`, cheapest first; a revert, keep, copy, or port is proven by diff against its ref: **reference/provenance-proof.md**.
</change-provenance>
<destructive-operation-policy>
A plan step is not consent for destruction — classify each shell command (catastrophic/irreversible/regenerable/reversible) and never write outside the worktree: **reference/destructive-operation-policy.md**.
</destructive-operation-policy>
<execution-conventions>
Comments explain **why**, never the **what**; zero comments by default, a better name beats a comment: **reference/code-comment-style.md**.
Tests check coverage and extend an existing file: **reference/test-placement.md**. Commits: one per step, AI-word-free: **reference/commit-conventions.md**.
A rework is a sibling `rework-<date>.md` — only its steps: **reference/execution-modes.md**. Prose follows BLUF: **reference/writing-style.md**.
`context.md` is the charter; execution owns `## Execution`, `## Open concerns`, `## State`: **reference/orchestrator-handoff.md**.
</execution-conventions>
<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| A step writes tests | Extending tests | [examples/extend-existing-tests.md](examples/extend-existing-tests.md) |
| Comment style | Policy, gate | [examples/comment-hygiene.md](examples/comment-hygiene.md) |
| A small, focused plan | Focused updates | [examples/single-component-refactor.md](examples/single-component-refactor.md) |
| A plan spanning files and layers | Cross-file tracking | [examples/multi-file-implementation.md](examples/multi-file-implementation.md) |
| Per change and milestone | Incremental checks | [examples/validation-checkpoints.md](examples/validation-checkpoints.md) |
| A step fails with bad output | Recovery, amendment | [examples/handling-failed-steps.md](examples/handling-failed-steps.md) |
| 10+ steps | Continuity | [examples/long-plan-execution.md](examples/long-plan-execution.md) |
| All steps complete | Review, fix steps | [examples/post-execution-review.md](examples/post-execution-review.md) |
| Prereqs and push approval | End-to-end | [examples/small-step-commits.md](examples/small-step-commits.md) |
| A fix may be material | Refusal, options | [examples/refusing-out-of-scope-rework.md](examples/refusing-out-of-scope-rework.md) |
| Message drift | Proceed-and-log | [examples/incidental-deviation.md](examples/incidental-deviation.md) |
| A step asks destruction | Refusal, blocked | [examples/refuse-destructive-command.md](examples/refuse-destructive-command.md) |
</context-loading-guide>
</knowledge>

<capabilities>
<track-plan>
1. Gate per **request-intake**; ask before step 1 when anything was inferred.
2. Locate or create the feature folder, resuming an existing plan or its active `rework-<date>.md`; ask resume-or-fresh only for ❌/🚫 steps, never a second folder.
3. Materialize steps and derive `context.md` per **plan-format** and **execution-conventions**.
4. Show the full list after each step with files, `Source`, validation; only statuses, notes, and approved `⏭` markers change in `plan.md`.
</track-plan>
<execute-step>
1. Mark 🔄, state the approach, and apply **check-scope-boundary**.
2. Resolve the `Source` per **change-provenance**, then write the change per **execution-conventions**.
3. Apply **place-tests** before any test code.
4. Validate against the objective and provenance proof, mark ✅, record files, `Source`, validation.
</execute-step>
<handle-errors>
1. Mark ❌ with details, find the root cause, and classify the fix with **check-scope-boundary** — in-boundary → fix, log, retry; material → hold and ask.
2. After two failed attempts on one objective, stop and ask; never skip a failed step or a failed validation. Resolved → ✅; unresolvable → 🚫 and consult the user.
3. A defective pending step → return `NEEDS_CONTEXT` with an amendment request; never fork the plan.
</handle-errors>
<check-scope-boundary>
1. Read the **Scope Boundary** — absent → infer **May change** — then classify the change by the behavior it alters.
2. Incidental or in-boundary → proceed with a one-line `Deviation:` note. Material, `Must match` drift, or an unnamed protected zone → hold and ask once; ambiguity → batch at the step end.
</check-scope-boundary>
<guard-destructive-operation>
1. Split the command into segments and classify each with its resolved target paths per **destructive-operation-policy**.
2. Catastrophic → refuse and stop. Irreversible → ask with command, paths, and recovery path, checkpointing first. A plan instructing destruction → ask; it is not authorization.
</guard-destructive-operation>
<run-validation-checkpoints>
Every plan carries a **green-only exit gate** — the plan is the contract, not the executor's discretion:
- **Autonomy**: tests per `**Autonomy**` — `stepwise` every step, `checkpoint` at milestones, `auto` when cheap; lint and type after changes.
- **Gate line**: `build=` · `test=` · `lint-type=`, evidence-backed, one per module — never invented or narrowed.
- **Baseline** in Step 1: those commands on the base — green, or red with named failures fixed by a restore step or a ratified exclusion.
- **Exit Gate step** last: the commands run **locally** and exit 0 with zero failures; the receipt records commands, exit codes, and counts.
- **Red** → repair twice, then `❌`/`🚫` and ask; never `✅`. **A subset, a skip, or a stale receipt is not a pass** — only a whole green gate counts.
- **Waiver** is the only escape: scope- and item-named, user-ratified, dated. Never abandon or defer the gate.
</run-validation-checkpoints>
<place-tests>
1. Locate existing tests for the changed code — same class, same level — then apply **execution-conventions**: covered → add nothing, a home → extend, none → mirror the class.
2. Record the placement in `Status` and run the affected tests.
</place-tests>
<verify-prerequisites>
1. Verify the feature branch — created only if the plan requires it and the user confirms name and base — then dependencies, toolchain, and the affected baseline.
2. Detect the comment style and record the policy plus one exemplar in the plan note.
3. A failed check → stop and raise it. Record ready or blocked before step 1.
</verify-prerequisites>
<commit-step>
1. Identify this step's files with `git status` and `git diff`, verify the `Source` receipt, and stage only those files.
2. Apply **execution-conventions** — block narration comments, write a convention-shaped message with no AI-related words, commit locally, report the hash. Never push.
3. A `no-op` step records its empty-diff proof instead.
</commit-step>
<review-post-execution>
1. Review your own diff against the plan's objectives and Scope Boundary.
2. Run the full **review-code** pass only when no independent gate follows; in a delivery cell **verify-cell** owns that review — both is a duplicated cost.
3. Per Blocker/Major: **check-scope-boundary**, record a ⏳ fix step, **execute-step**, repeat; log 🟡/🟢 only.
4. Re-run the **Exit gate** after the last fix; keep `plan.md` + `context.md` as the record.
</review-post-execution>
<request-push-approval>
1. Confirm the **Exit gate** receipt matches the current head; stale or red → re-run or stop.
2. Summarize branch, commits, and distance from base; past a few commits, brief first — a route over the 2–3 riskiest commits, one prediction, one check.
3. Ask "Push branch [name] to remote?" and wait; a decline leaves it local. A PR request → apply **create-pull-request** after the push and record its reference in `## Execution`.
</request-push-approval>
</capabilities>

<rules>
<rule> **At Plan Start**: Gate per **request-intake**, then apply **track-plan** before executing any step. </rule>
<rule> **Throughout Execution**: Execute autonomously — never ask permission per step; pause only on material drift, a blocker, or a push. </rule>
<rule> **Before Starting the First Step**: Apply **verify-prerequisites** — raise and wait when the environment is not ready. </rule>
<rule> **Before Running Any Shell Command**: Apply **guard-destructive-operation** — refuse catastrophic commands, ask before irreversible ones. </rule>
<rule> **At Validation Points**: Apply **run-validation-checkpoints** — validate incrementally, and never accept a gate subset. </rule>
<rule> **When a Step Writes or Modifies Tests**: Apply **place-tests** before writing test code. </rule>
<rule> **After Each ✅ Step**: Apply **commit-step**. </rule>
<rule> **When a Step Fails**: Apply **handle-errors**. </rule>
<rule> **When a Pending Step Is Defective**: Return `NEEDS_CONTEXT` with an amendment request — never fork the plan or create a second folder. </rule>
<rule> **When a Step, Fix, or Deviation May Be Material**: Apply **check-scope-boundary** — hold and ask; log incidental drift. </rule>
<rule> **When the User Asks Something New Mid-Execution**: Gate it per **request-intake**. </rule>
<rule> **After All Steps Complete**: Apply **review-post-execution**. </rule>
<rule> **Before Any Push**: Apply **request-push-approval** with a green Exit gate receipt for the current head — a step added after the gate invalidates it. </rule>
<rule> **When the Folder Contains a Rework Plan**: Apply **track-plan** and **execute-step** to the active rework steps only. </rule>
<rule> **When Executed as a Dispatched Agent**: Overwrite the `## Execution` handoff, update `## Open concerns`, never write a log. </rule>
<rule> **When the Plan is a POC** (`**Type**: poc`): Run it as a normal plan; offer the MR for review and never merge before the user's decision. </rule>
</rules>

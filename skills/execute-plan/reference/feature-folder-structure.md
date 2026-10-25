# Feature Folder Structure

Each feature implementation lives in its own folder with two core docs:

```
{location}/{repo}/{feature-name}/
├── plan.md                  # Step-by-step execution plan with live status tracking
├── context.md               # Charter + latest handoff (40–60 lines; 8k ceiling)
└── rework-<date>.md         # Sibling rework plan (optional — see **rework-plan-execution**)
```

No `evidence-raw.md`: execution proof is the step's `Validation` line plus its commit;
history is git/PR.

| Item | Rule |
|---|---|
| Location | For an **orchestrate-feature-delivery** cell use the epic's delivery folder `deliveries/<epic-name>/{repo}/{feature-name}/` (already created by the orchestrator); otherwise resolve the artifact base via `resolve-artifact-location` and use `{base}/feature-implementations/{feature-name}/`. |
| Repo-first layout | When a plan belongs to a specific repo (a cell from **orchestrate-feature-delivery**), use `deliveries/<epic-name>/{repo}/{feature-name}/`; fall back to `{location}/{feature-name}/` when no repo applies. |
| Feature name | Derive a short, descriptive kebab-case name from the plan's objective (e.g., `add-auth-system`, `refactor-validation-handler`, `fix-null-pointer-in-transformer`). |
| Plan file | Contains the numbered step list with status emojis, updated in real-time as execution progresses. Serves as the live execution dashboard. |
| Context file | The **charter**: outcome, why, must-hold invariants, unknowns, done criteria, pointers, `## Open concerns`, and `## State`. Target **40–60 lines**, hard ceiling **8,000 chars / 120 lines**; never restates `plan.md` decisions or pre-flight evidence. The planner owns the charter sections; the executor owns only `## Open concerns` / `## State` / `## Execution`. On hand-off the executor overwrites `## Execution` with the latest status, `base7..head7`, PR, one-line test evidence, and one-line review outcome. Never appends a round. |
| No log file | Do not create `evidence-raw.md`. A step's proof is its `Validation` line plus its commit; history is git/PR. A decision-changing fact goes to the spike evidence doc; a deferred concern goes to `## Open concerns`. |
| Rework files | Each rework is a sibling `rework-<date>.md` in the same folder — `plan.md` stays the frozen original; the active rework file is found via the `## Reworks` manifest in `context.md` (see **rework-plan-execution**). |
| POC | Executes like any feature. Its MR is the user's evaluation vehicle; no measurement step, report, or verdict. |
| Permanent record | `plan.md` and `context.md` are kept after execution completes — never deleted. |

# Example: Amending an In-Flight Plan Instead of Writing a New One

**Scenario**: A feature plan is mid-execution. Step 3 is blocked because the plan assumed a shared token store that does not exist, and Step 4 is now obsolete.
The same plan is amended in place — same file, same folder.

**Applies**: **amend-plan**, **plan-file-format**

## Trigger

The executor marks Step 3 🚫 and returns `NEEDS_CONTEXT`:

> "Plan defect: no shared token store exists. Step 3 needs a store setup step **before it**; Step 4 (migrate legacy tokens) is obsolete once the store is replaced."

## Amend vs Rework

The defect is in steps that have **not run** — amend. A rework file would be wrong because no delivered behavior changes.

## Before

```markdown
### Step 3: Wire token refresh to the shared store 🚫
### Step 4: Migrate legacy tokens ⏳
### Step 5: Update integration tests ⏳
### Step 6: Validate linting, formatting and type checking ⏳
```

## Amendment

Applying **amend-plan**:

- ✅ Steps 1–2 and their notes stay byte-for-byte unchanged.
- The missing store setup must run **before** Step 3 → insert Step 3a; no renumbering.
- Step 4 is obsolete → mark `⏭ abandoned — superseded by Step 3a; token store removed`.
- Steps 5–6 keep their numbers and run unchanged.
- Boundary is tightened, not widened → no user ratification needed.

```markdown
### Step 3a: Add token-store setup and configuration ⏳
### Step 3: Wire token refresh to the shared store 🚫
### Step 4: Migrate legacy tokens ⏭
**Status**: ⏭ Abandoned — superseded by Step 3a; token store removed
### Step 5: Update integration tests ⏳
### Step 6: Validate linting, formatting and type checking ⏳
```

## context.md

```markdown
## Amendments
| Date | Trigger | Added | Abandoned | Boundary | Reason |
|---|---|---|---|---|---|
| 2026-10-21 | Step 3 blocked: no shared token store | Step 3a | Step 4 | tightened, no widening | Plan assumed an existing store |
```

## Result

The same `plan.md` path resumes at Step 3a, then Step 3; the cell stays **in-progress**. No second plan folder, no new cell, no lost history.
Step 4 remains visible as `⏭` so the decision is auditable.

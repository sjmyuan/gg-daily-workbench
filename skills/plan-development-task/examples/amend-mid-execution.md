# Example: Amending an In-Flight Plan Instead of Writing a New One

**Scenario**: A feature plan is mid-execution. Step 3 is blocked because the plan assumed a shared token store that does not exist, and Step 4 is now obsolete.
**Applies**: **amend-plan** · **plan-file-format**

The same file and folder are amended in place.

## Trigger

The executor marks Step 3 🚫 and returns `NEEDS_CONTEXT`:

> "Plan defect: no shared token store exists. Step 3 needs a store setup step **before it**; Step 4 (migrate legacy tokens) is obsolete once the store is replaced."

## Amend vs Rework

The defect is in steps that have **not run** — amend. A rework file would be wrong because no delivered behavior changes.

## Before

Fragment of the existing `plan.md`; its header, metadata, and `## Steps` heading are unchanged.

```markdown
### Step 3: Wire token refresh to the shared store 🚫
**Objective**: Refresh tokens through the shared store.
**Status**: 🚫 Blocked — no shared store exists
```

Steps 4–6 stay ⏳ pending.

## Amendment

Applying **amend-plan**:

- ✅ Steps 1–2 and their field lines stay byte-for-byte unchanged.
- The missing store setup must run **before** Step 3 → insert Step 3a; no renumbering.
- Step 4 is obsolete → mark `⏭ abandoned — superseded by Step 3a; token store removed`.
- Steps 5–6 keep their numbers and run unchanged.
- Boundary is tightened, not widened → no user ratification needed.

```markdown
### Step 3a: Add token-store setup and configuration ⏳
**Objective**: Provision the shared token store the refresh flow will use.
**Files**: `infrastructure/token_store.py`, `config/token_store.yaml`
**Source**: generate · n/a · behavior-equal
**Implementation**: New store adapter plus configuration; no prior source in the repo.
**Validation**: Store adapter tests pass; refresh flow can reach the store.
**Status**: ⏳ Pending

### Step 3: Wire token refresh to the shared store 🚫
**Objective**: Refresh tokens through the shared store.
**Status**: 🚫 Blocked — resumes after Step 3a

### Step 4: Migrate legacy tokens ⏭
**Objective**: Backfill legacy tokens into the shared store.
**Status**: ⏭ Abandoned — superseded by Step 3a; token store removed
```

Field lines not repeated above are unchanged from the original steps.

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

## Validation

- [x] ✅ steps and their field lines unchanged
- [x] New step inserted with a letter suffix; nothing renumbered
- [x] Obsolete step marked `⏭` with a reason, not deleted
- [x] One `## Amendments` row recorded; boundary tightened only

# Plan Executor: Small-Step Commits with Push Approval Example

**Scenario**: A 4-step feature plan executes with one small commit per step, and the branch is pushed only after explicit user confirmation. Demonstrates **verify-prerequisites**, **commit-step**, **request-push-approval**, and **manage-user-interaction** (branch-creation ask, push approval).

## User Request

"Execute the plan to add a `CustomerValidator`, commit after each step, and don't push anything until I confirm."

## Plan to Execute

1. Create CustomerValidator class
2. Wire validator into CustomerService
3. Add unit tests for validator
4. Run lint, formatting and type checks

```markdown
## Scope Boundary
**May change**: customer validation behavior and its tests
**Expected files**: validator, service, tests (advisory)
**Must not change**: public API signatures, other services
**Protected zones**: none added
```

## Prerequisites Check (verify-prerequisites)

Applying **verify-prerequisites**:

```
git status        → working tree clean
git branch        → on main; feature branch missing
```

- Branch convention detected from existing branches (`1234-*` ticket style): new branch `1234-add-customer-validator` from `main`.
- Missing: that feature branch. Raise to user: "Create branch `1234-add-customer-validator` from `main` before starting?" User confirms. Branch created.
- Dependencies present, baseline tests pass → **ready**.

Recorded in Step 1's **Validation** line: branch created, baseline green.

### Step 1: Create CustomerValidator Class ✅

**Objective**: Add a validator class for customer fields.
**Files**: `src/validation/CustomerValidator.java` (new)
**Source**: generate · n/a · behavior-equal
**Implementation**: id/name/email validation rules; no prior class.
**Validation**: class compiles; no tests changed.
**Status**: ✅ Completed

Applying **commit-step**:
```
git add src/validation/CustomerValidator.java
git commit -m "feat(validation): add CustomerValidator class"
```
Commit `a1b2c3d` created locally. Not pushed.

#### Plan Status After Step 1
```
Step 1 Create CustomerValidator class ✅
Step 2 Wire validator into CustomerService ⏳
Step 3 Add unit tests for validator ⏳
Step 4 Run lint, formatting and type checks ⏳
```

### Step 2: Wire Validator into CustomerService ✅

**Objective**: Call the validator before persisting a customer.
**Files**: `src/service/CustomerService.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: inject `CustomerValidator`; validate at the service boundary.
**Validation**: existing tests pass — no regressions.
**Status**: ✅ Completed

Applying **commit-step**:
```
git add src/service/CustomerService.java
git commit -m "refactor(service): use CustomerValidator in CustomerService"
```
Commit `e4f5g6h7` created locally. Not pushed.

### Step 3: Add Unit Tests for Validator ✅

**Objective**: Cover validator rules and edge cases.
**Files**: `test/CustomerValidatorTest.java` (new)
**Source**: generate · n/a · behavior-equal
**Implementation**: valid, null, invalid-id, and invalid-email cases.
**Validation**: all 12 tests pass.
**Status**: ✅ Completed

Applying **commit-step**:
```
git add test/CustomerValidatorTest.java
git commit -m "test(validation): cover CustomerValidator edge cases"
```
Commit `i8j9k0l1` created locally. Not pushed.

### Step 4: Validate Linting, Formatting and Type Checks ✅

**Objective**: Confirm the change passes repo quality gates.
**Files**: none
**Source**: no-op · n/a · n/a
**Implementation**: run the gates; no edits.
**Validation**: lint, format, type-check all clean.
**Status**: ✅ Completed

Applying **commit-step**: step produced no code change — no commit needed.

## Final Summary & Push Approval (request-push-approval)

All 4 steps completed ✅.

Applying **request-push-approval**:
```
Branch: 1234-add-customer-validator (3 commits ahead of main)
  a1b2c3d feat(validation): add CustomerValidator class
  e4f5g6h7 refactor(service): use CustomerValidator in CustomerService
  i8j9k0l1 test(validation): cover CustomerValidator edge cases
```

Ask user: "Push branch `1234-add-customer-validator` to remote?"

- **User confirms** → `git push -u origin 1234-add-customer-validator`; success reported.
- **User declines** → branch stays local; user is told the 3 commits are ready to push whenever they choose.
- **User also asks for a PR** → push first, then apply **create-pull-request**; approve the full draft before creation.

The plan file and context file are kept as a permanent record.

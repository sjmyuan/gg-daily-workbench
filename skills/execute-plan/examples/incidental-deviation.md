# Example: Proceeding on Cosmetic Drift Instead of Stopping

**Scenario**: A step's formatter reflows unlisted files, and the commit message differs from the plan's. Demonstrates **check-scope-boundary** and **commit-step** — stop on function, log on form.

**Applies**: **check-scope-boundary**, **commit-step**

## Plan in Execution

```markdown
## Scope Boundary
**May change**: `DataImportedHandler` ID-passing behavior
**Expected files**: `DataImportedHandler.java` + its tests (advisory)
**Must not change**: transformer logic, publisher behavior, other handlers
```

### Step 2: Fix ID mapping logic in DataImportedHandler ✅

**Files**: `DataImportedHandler.java`
**Validation**: `mvn test -Dtest=DataImportedHandlerTest` passes.

Running the repo formatter rewrote `build.gradle.kts` and `docs/operations.md`:

```
git status --short
 M docs/operations.md
 M build.gradle.kts
 M src/.../DataImportedHandler.java
?? notes-scratch.txt          (pre-existing, not mine)
```

## Boundary Check

Applying **check-scope-boundary**:

1. Paths changed: three tracked files plus pre-existing untracked dirt.
2. Normalize cosmetics: `git diff -w --ignore-blank-lines --stat` shows `docs/operations.md` and `build.gradle.kts` with zero non-whitespace lines.
3. Materiality test: no behavior outside **May change**, no protected zone, objective verified, nothing irreversible, *what* is built is unchanged.

**Verdict**: incidental — proceed, no ask. Record in the step:

> `Deviation: formatter reflow in docs/operations.md + build.gradle.kts — cosmetic, no behavior change`

`notes-scratch.txt` predates execution — left untouched, never staged.

## Commit

Plan's illustrative message: `fix(handler): pass original ID to publisher`.
Repo convention from recent `git log` uses a ticket prefix, so the actual commit is:

```
git add src/.../DataImportedHandler.java docs/operations.md build.gradle.kts
git commit -m "PROJ-142 fix(handler): pass original ID to publisher"
```

Commit `7c1d9ab` — hash and wording differ from the plan, which is not a failure.

## What Would Have Stopped Execution

The plan listed `publisher` under **Must not change**, so a retry-behavior change would be material.
The step would then hold with options: extend the boundary, file a follow-up, or proceed with a recorded deviation.

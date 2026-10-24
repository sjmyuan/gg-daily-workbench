# Plan Executor: Handling Failed Steps Example

**Scenario**: A bug-fix plan hits a compilation error mid-execution; the executor marks the step ❌, analyzes the root cause, applies a recovery fix within scope, and retries. Demonstrates **track-plan**, **execute-step**, and **handle-errors**.

**Applies**: **track-plan**, **execute-step**, **handle-errors**

## User Request
"Implement the bug fix plan we created for the null pointer exception in data transformation"
## Plan to Execute
1. Add null checks in DataImportedHandler
2. Update unit tests
3. Add integration test
4. Update error handling documentation

```markdown
## Scope Boundary
**May change**: `DataImportedHandler` null handling and its tests
**Expected files**: handler, its tests, error-handling docs (advisory)
**Must not change**: transformer behavior, publisher behavior, other endpoints
**Protected zones**: none added
```

## Initial Plan Status
**Status**: Step 1 ⏳ · Step 2 ⏳ · Step 3 ⏳ · Step 4 ⏳

### Step 1: Add Null Checks ✅

**Objective**: Add defensive null checks to prevent null pointer exceptions
**Files**: `application/service/DataImportedHandler.java`
**Source**: edit · n/a · behavior-equal
**Implementation**:
```java
public void handle(DataImported event) {
    if (event == null || event.getRecord() == null) {
        throw new InvalidDataEventException("Data event cannot be null");
    }
    if (event.getRecord().getId() == null) {
        throw new InvalidDataException("Data record ID is required");
    }
    transformAndPublish(event.getRecord());
}
```
**Validation**: Handler compiles and includes null checks
**Status**: ✅ Completed · Steps 2–4 ⏳

### Step 2: Update Unit Tests ❌

**Objective**: Add unit tests to verify null check behavior
**Files**: `application/service/DataImportedHandlerTest.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: attempted the test below; blocked on a missing exception class.
```java
@Test
void shouldThrowExceptionForNullData() {
    DataImported event = new DataImported(null);
    assertThrows(InvalidDataEventException.class, () -> handler.handle(event));
}
```

**Validation**: ✗ compile error — `InvalidDataEventException` cannot be resolved.
**Status**: ❌ Failed — missing exception class · Step 1 ✅ · Steps 3–4 ⏳

Error detail:
```
[ERROR] DataImportedHandlerTest.java:[45,20] cannot find symbol
  symbol:   class InvalidDataEventException
```

**Analysis**: `InvalidDataEventException` doesn't exist yet; the tests need it to compile.

**Recovery** — per **handle-errors** step 4, applying **check-scope-boundary** first: adding the missing exception class is behavior-neutral, inside the plan's **May change** (the handler and its tests), and a required dependency of Step 2's tests, so the fix proceeds and is recorded as a clarifying note.

**Files**: `domain/exceptions/InvalidDataEventException.java` (new)
```java
public class InvalidDataEventException extends RuntimeException {
    public InvalidDataEventException(String message) { super(message); }
}
```

**Retry Step 2** — add the import and re-run:
```java
import com.example.application.domain.exceptions.InvalidDataEventException;
```
**Validation**: All tests compiling and passing ✓
**Status**: ✅ Completed (after recovery) · Step 1 ✅ · Steps 3–4 ⏳

### Step 3: Add Integration Test ✅

**Objective**: Create end-to-end test for null data handling
**Files**: `presentation/DataTransformationIntegrationTest.java` (new)
**Source**: generate · n/a · behavior-equal
**Implementation**:
```java
@SpringBootTest
@AutoConfigureMockMvc
class DataTransformationIntegrationTest {
    @Test
    void shouldRejectNullDataEvent() throws Exception {
        mockMvc.perform(post("/api/transform")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"record\": null}"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").value("Data event cannot be null"));
    }
}
```
**Validation**: Integration test passing ✓
**Status**: ✅ Completed · Steps 1–2 ✅ · Step 4 ⏳

### Step 4: Update Documentation ✅

**Objective**: Document the new error handling behavior
**Files**: `docs/operations.md`
**Source**: edit · n/a · behavior-equal
**Implementation**: added an `## Error Handling` section — when `InvalidDataEventException` is thrown (null event, missing record ID, null required fields) and the resolution.
**Validation**: Documentation is clear and accurate
**Status**: ✅ Completed

## Final Plan Status
**Status**: Step 1 ✅ · Step 2 ✅ (recovered) · Step 3 ✅ · Step 4 ✅

## Completion Summary
✅ All 4 steps completed successfully. Step 2 failed ❌ (missing exception class), root cause analyzed, recovery fix applied within scope, step retried ✅.

**Files Changed**:
- Created: 2 (`InvalidDataEventException.java`, `DataTransformationIntegrationTest.java`)
- Modified: 2 (`DataImportedHandler.java`, `operations.md`)
- Total: 4

The plan file and context file are kept as a permanent record.

## When the Error Is a Plan Defect

A recovery fix differs from a plan defect. If Step 2 had failed because the plan assumed an existing `InvalidDataEventException` and no such dependency was planned, the executor would not improvise a redesign:

- Mark Step 2 🚫 blocked with the defect.
- Write an amendment request: the defect, proposed added/skipped steps, and boundary impact.
- Return `NEEDS_CONTEXT`; the planner amends the same `plan.md`.
- Resume at Step 2 after the amendment; never create a second plan folder.

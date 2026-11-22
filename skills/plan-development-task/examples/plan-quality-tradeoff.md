# Example: Plausible-but-Weak Plan vs Strong Plan

**Scenario**: Same request, same code, two plans. The weak one passes every template field — it is what a phase template produces. The strong one is what a planner produces after reading the code.
**Applies**: **plan-bug-fix** → **plan-rubric**

Request: *"CSV export drops the last row when the file has no trailing newline."*

## Weak plan (conformant, not ready)

(abridged — the omissions are the point; full schema in [plan-file-format.md](../reference/plan-file-format.md))

```markdown
# Plan: csv-export — fix missing final row
**Type**: bug-fix
**Branch**: `fix-csv-export` off `main`
**Test strategy**: test-first — a correctness bug needs a test.
**Gate**: build=`mvn -q compile` · test=`mvn test` · lint-type=`mvn checkstyle:check`

## Scope Boundary
**May change**: CSV export
**Must not change**: import, other exports
**Protected zones**: none added

## Steps

### Step 1: Prepare environment ⏳
…
### Step 2: Write the failing test ⏳
**Validation**: Test compiles and joins the suite.
### Step 3: Confirm test failure (RED) ⏳
**Validation**: Fails — not an error.
### Step 4: Fix the row splitter ⏳
**Validation**: Step 2 test passes.
### Step 5: Refactor ⏳
**Validation**: Suite green.
### Step 6: Clean up ⏳
**Validation**: Suite green.
### Step 7: Exit gate ⏳
**Validation**: All gate commands exit 0.
```

**Why it fails the rubric** — and note that it fails nothing a checklist would catch:

| Row | Verdict | Why |
|---|---|---|
| 1 Evidence | Fail | Says "test-first — a correctness bug needs a test" without stating **where** the row is lost. `split("\n")` vs a trailing-newline read is a guess. |
| 3 Units | Fail | Steps 2, 3, 5, 6 exist only as phases; each buys a verification the executor already runs. |
| 6 Risk | Fail | No `## Risk` block. The reader cannot tell what the planner was unsure about. |
| 8 Open by design | Fail | Step 4 says "fix the row splitter" as if the seam were known. |

## Strong plan (same request)

(abridged — Steps 1 and 4 show their verdict only; full schema in [plan-file-format.md](../reference/plan-file-format.md))

```markdown
# Plan: csv-export — a file without a trailing newline exports every row
**Type**: bug-fix
**Branch**: `fix-csv-export` off `main`
**Test strategy**: test-first — the break is a data-loss assertion on a plain string input; no benchmark needed.
**Gate**: build=`mvn -q compile` · test=`mvn test` · lint-type=`mvn checkstyle:check` — `pom.xml:112`

## Scope Boundary
**May change**: how `CsvExporter` segments records from a stream
**May change**: the reader's newline handling, if the exporter provably cannot fix it
**Expected files**: `CsvExporter.java`, `CsvExporterTest.java` (advisory)
**Must not change**: quote/escape rules, column order, header emission, the importer
**Protected zones**: the streaming API's memory profile — no full-file materialization

## Risk
- The row is lost in the exporter, not in the reader's `BufferedReader` → Step 2 tests the exporter in isolation; fallback: amend before Step 3.
- **Expected to break first**: Step 3 — the streaming path may not be reachable without a reader seam.

## Steps

### Step 1: Prepare environment ⏳
**Validation**: Gate commands on `main` — `baseline: green` (build=0 · 204 passed · lint=0).

### Step 2: Prove the lost row ⏳
**Objective**: A stream with no trailing newline yields every row, header included.
**Files**: `CsvExporterTest.java`
**Source**: generate · n/a · behavior-equal
**Implementation**: Two cases — with and without a trailing newline — over the same three rows; assert parsed row count and last-row content.
**Validation**: The no-newline case fails on a missing row; the other passes.
**Status**: ⏳ Pending

### Step 3: Segment records without a terminator ⏳
**Objective**: The last record is emitted even when the stream ends mid-record.
**Files**: `CsvExporter.java`
**Source**: edit · n/a · behavior-equal
**Implementation**: **Open**: if `segment()` is reachable in isolation, fix the loop there; if the reader consumes the last line before the exporter sees it, add the seam first and record it as `Scope +reader seam (delegated)`.
**Validation**: Step 2 both green; memory profile unchanged for a 10 MB stream; exporter suite green.
**Status**: ⏳ Pending

### Step 4: Exit gate ⏳
**Validation**: `mvn -q compile` && `mvn test` && `mvn checkstyle:check` — all exit 0, zero failures.
```

## What changed

| Row | Weak | Strong |
|---|---|---|
| Evidence | Guessed the seam | Names the two candidate seams and the test that separates them |
| Units | 7 phase steps | 3 units: prove, fix, gate — each with a distinct verdict |
| Risk | Absent | Two assumptions, each with the step that tests it and a fallback |
| Open by design | Pretended to know | Step 3 states the check and both branches |
| Boundary | Path-shaped ("CSV export") | Behavior-shaped, with the memory profile protected |

Both plans are the same length to a checklist. Only one tells the executor what to do when the code disagrees — which is the case the plan exists for.

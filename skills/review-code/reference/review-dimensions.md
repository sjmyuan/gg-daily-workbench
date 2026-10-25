# Review Dimensions Reference

Reference checklist for **all 10 review dimensions**. Apply every relevant ✓ item from each dimension when conducting a code review.

Assume the change is wrong and hunt for the evidence that proves it right — the deeper sections below (**Adversarial stance**, **Failure-mode enumeration**, **Negative space**) drive that search.

1. **Correctness & Robustness**:
   - ✓ Logic errors and edge cases (null/undefined, empty collections, boundary values)
   - ✓ Error handling (try/catch coverage, error propagation, user-facing messages)
   - ✓ Input validation (type checking, range validation, sanitization)
   - ✓ State consistency (race conditions, concurrent access, state transitions)
   - ✓ Async/Promise handling (proper awaiting, error catching, cancellation)
   - ✓ Backward compatibility (API changes, data migration, deprecated features)

2. **Maintainability**:
   - ✓ Code clarity (self-documenting code, complex logic explained)
   - ✓ Naming (descriptive, consistent, follows conventions)
   - ✓ Function/component cohesion (single responsibility, appropriate size)
   - ✓ Code duplication (DRY principle, extraction opportunities)
   - ✓ Modularity (separation of concerns, loose coupling)
   - ✓ Project conventions (style guide, architectural patterns)

3. **Performance & Resources**:
   - ✓ Algorithmic complexity (O(n²) → O(n log n) opportunities)
   - ✓ Database optimization (N+1 queries, missing indexes, inefficient JOINs)
   - ✓ Performance hotspots (loops, database queries, network calls)
   - ✓ Rendering efficiency (unnecessary re-renders, memoization)
   - ✓ I/O patterns (batch operations, connection pooling)
   - ✓ Caching strategies (when to cache, invalidation logic, cache stampede risks)
   - ✓ Memory management (unbounded collections, memory leaks, resource cleanup)
   - ✓ Benchmark validation (performance test coverage for optimization claims)
   - ✓ Scalability (concurrent users, large datasets)

4. **Security & Privacy**:
   - ✓ Injection vulnerabilities (SQL, XSS, command injection)
   - ✓ Authentication/authorization (proper checks, token handling)
   - ✓ Secrets management (no hardcoded credentials, secure storage)
   - ✓ Dependency risks (outdated packages, known vulnerabilities)
   - ✓ Unsafe defaults (overly permissive access, insecure configurations)
   - ✓ Data privacy (PII handling, logging sensitive data)

5. **APIs, Contracts & Types**:
   - ✓ Public interface design (intuitive, consistent, minimal surface area)
   - ✓ Schema/type changes (breaking changes flagged, versioning)
   - ✓ Type safety (TypeScript strictness, avoiding `any`)
   - ✓ Error handling contracts (documented error conditions)
   - ✓ Safe failure modes (graceful degradation, fallbacks)

6. **Tests**:
   - ✓ Coverage of critical paths (happy path + edge cases + errors)
   - ✓ Regression coverage (tests for fixed bugs)
   - ✓ Test determinism (no flaky tests, proper mocking)
   - ✓ Test readability (clear AAA structure, descriptive names)
   - ✓ Alignment with requirements (tests verify actual requirements)
   - ✓ Test infrastructure: if the project has **no test coverage at all**, flag as 🔴 Major — recommend establishing a test baseline before merging production code

7. **Architecture**:
   - ✓ Modularity (clear boundaries, appropriate abstractions)
   - ✓ Extensibility (easy to add features without major refactors)
   - ✓ Alignment with project goals (fits existing patterns and vision)
   - ✓ Technical debt (quick fixes that need follow-up noted)

8. **Inconsistencies** *(treat existing code as potentially wrong — do NOT assume it is the correct baseline)*:
   - ✓ Naming style clashes (e.g., `camelCase` vs `snake_case`, `get` prefix vs none)
   - ✓ Pattern clashes (e.g., callbacks vs Promises vs async/await; class-based vs functional components)
   - ✓ API usage clashes (e.g., two different libraries doing the same job, two different ways to call the same API)
   - ✓ Error-handling style clashes (e.g., exceptions vs result objects vs error callbacks)
   - ✓ Structural clashes (e.g., flat vs nested directory layout, co-located vs separated test files)
   - ✓ Config/constant definition clashes (e.g., inline magic numbers vs named constants, scattered config vs centralized)

   **For every inconsistency found**:
   - Show **both** variants with concrete file/line references
   - Explain the trade-offs of each without declaring a winner
   - Explicitly ask the user (or note in the review) which variant should be the canonical one
   - Do **not** recommend "align with existing code" unless the existing code is clearly the established, intentional pattern

9. **Observability & Deployment Safety**:
   - ✓ Logging coverage (key operations, errors, and state transitions are logged at appropriate levels; no sensitive data in logs)
   - ✓ Metrics and tracing (SLIs are measurable; distributed tracing is instrumented for async/cross-service flows)
   - ✓ Feature flag usage (risky or large changes are gated behind flags to enable safe, incremental rollout)
   - ✓ Database migration safety (schema changes are backward-compatible with the previous app version; a rollback path exists)
   - ✓ Configuration externalized (no hardcoded environment-specific values; all config changes are explicit and documented)
   - ✓ Deployment prerequisites documented (migration steps, cache warm-up, seed data, or manual actions noted in the PR description or a linked runbook)

10. **Change Context & Blast Radius**:
   - ✓ Call sites (every caller of a changed, added, or renamed symbol is updated and behavior-compatible)
   - ✓ Implementations (every implementation, subclass, and mock of a changed signature still satisfies it)
   - ✓ Contracts (serialized payloads, API/event schemas, DB columns, config keys, CLI flags, env vars)
   - ✓ Behavior diff (state what the code did before and does now — a behavior diff, not a text diff)
   - ✓ Parallel paths (other code doing the same job that the change did not update)
   - ✓ Downstream consumers (services, jobs, reports, exports, dashboards reading the changed data)
   - ✓ Lifecycle fit (deploy order, migration order, rollback, data backfill, cache warm-up)
   - ✓ Physical move (a file, package, or module added, moved, or renamed — verify the referent before judging it, per **referent-grounding.md**)

   **For every changed symbol**: name its callers, the callers' assumptions, and the evidence that each still holds.

## Adversarial stance

Assume the change is wrong until the code proves it right.

- State the failure hypothesis before judging the fix — never open with "this looks correct"
- Treat a guard absent from the diff as a guard that does not exist, not as one that lives elsewhere
- Name concrete evidence for every "safe" verdict: the existing guard, test, or invariant at `file:line`
- Re-read the change once as an attacker (abuse, injection, bypass, exhaustion) and once as a careless maintainer (misuse, missed update, stale assumption)
- Challenge the change's shape, not only its behavior: whether it should exist, live there, be named that, or be that large
- Keep every unproven suspicion in the report at its true confidence — never drop it silently

## Failure-mode enumeration

Walk every changed behavior through each mode; mark it `verified` or `not verified` with the reason.

| Mode | Prompt |
|---|---|
| Empty / null / zero | Does the path survive absent, null, empty, and zero input? |
| Boundary | Off-by-one, max size, first and last element, exact-limit values |
| Partial failure | What happens when the operation fails halfway? Is state left inconsistent? |
| Concurrency | Can two requests interleave on the same state? Is the read-modify-write atomic? |
| Retry / duplicate | Is the operation idempotent when the caller retries or the message redelivers? |
| Ordering | Does correctness depend on arrival order that is not guaranteed? |
| Timeout / latency | What if the call is slower than expected, or hangs? |
| Clock / timezone | Is time compared or stored in mixed zones or units? |
| Scale | Does it hold at 10× the current volume, rows, or tenant count? |
| Error path | Is the error propagated, logged, and translated into the caller's contract? |
| Rollback / undo | Can the change be reversed without data loss? |

## Negative space

List what the change should have included but does not.

| Missing artifact | Present when |
|---|---|
| Regression test | A bug fix ships without a failing-first test |
| Migration | A schema change ships without a versioned migration |
| Cleanup / eviction | An unbounded cache, set, listener, or subscription is added |
| Validation | New external input (request, file, env, message) enters without checks |
| Rollback path | A destructive or irreversible operation is introduced |
| Observability | A new external call, cache, queue, or job ships without logs or metrics |
| Documentation | A config key, flag, endpoint, or env var is added |
| Feature gate | A risky or broad change ships unguarded |

## Searched negatives

An "absent" claim is evidence only when the search is named: `rg "<pattern>" <scope> → 0 hits`.
Unsearched absence is a gap in the review, not a finding about the code — raise it as a challenge.


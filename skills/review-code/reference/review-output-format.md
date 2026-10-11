# Review Output Format

Standard template for all review output. Every finding anchors to one line — see **finding-anchors.md** for the anchor rules.

````
## Code Review Summary

**Scope**: [Brief description of what was reviewed]
**Focus Areas**: [e.g., correctness, security, performance, blast radius]
**Reviewed**: [N files, +A/-B — list every changed file with its line count]
**Overall Assessment**: [Brief evaluation - e.g., "Ready to merge with minor changes"]
**Ready to merge?**: [Yes | No | With fixes] — [one-sentence technical reasoning]

---

## Findings

> Severity legend: 🚫 Blocker = must fix before merge · 🔴 Major = should fix · 🟡 Minor = nice to fix · 🟢 Nit = polish · ⚠️ Inconsistency = decision required

### 🚫 Blockers (Must Fix)

#### [Finding Title]
- **File**: `path/to/file.ts:42`
- **Related**: `path/to/other.ts:88` *(optional — one anchor per finding)*
- **Confidence**: Confirmed | Suspected | Needs runtime check
```ts
42 │ const jpql = "FROM Discount WHERE code = '" + discountCode + "'";
```
- **Issue**: [Clear description of what's wrong and why it matters]
- **Impact**: [Specific consequence if not fixed]
- **Recommendation**: [Concrete fix with code snippet if helpful]

### 🔴 Major Issues

### 🟡 Minor Issues

### 🟢 Nits / Suggestions

### ⚠️ Inconsistencies (Decision Required)

#### [Inconsistency Title]
- **Variant A**: [description] — `path/to/file.ts:10`
- **Variant B**: [description] — `path/to/file.ts:40`
- **Trade-offs**: [neutral comparison of both approaches]
- **Decision needed**: Which variant should be the project standard? *(Do not default to whichever appeared first — both may be wrong)*

---

## Positive Highlights
*[Call out well-done aspects: clear naming, good test coverage, clever solution, etc.]*

---

## Failure Modes Checked
*A row per changed behavior. Mark each mode `verified` or `not verified` with the reason — never leave a changed behavior unassessed.*

| Mode | Change under test | Result |
|---|---|---|
| Retry / duplicate | `publish()` idempotency | not verified — no dedup key or idempotency table found |

---

## Performance Analysis *(include only for performance optimization reviews)*
### Improvements Confirmed
*[List algorithmic, query, caching, or I/O improvements with before/after summary]*

### Concerns & Risks
*[Cold cache, cache stampede, memory overhead, single points of failure, etc.]*

### Metrics to Monitor Post-Deployment
*[p50/p95/p99 latency, cache hit rate, DB query count, error rate, etc.]*

---

## Risks & Assumptions
*[Each bullet names the assumption and the concrete check that would confirm or refute it]*

---

## Recommended Next Steps
1. [Prioritized action items]
2. [Suggested validations or manual tests]
3. [Follow-up items that can be deferred]
````

**Formatting guidelines**:
- Always give a clear merge verdict (`Yes | No | With fixes`) with a one-line reason — never leave the requester to infer readiness from the findings
- Anchor each finding to exactly one line: `` `path/file.ext:42` `` plus the verbatim anchored line in a fenced code block labeled with its line number — never a `#L10-L15` range
- Put additional affected places in a `**Related**` field or split the finding — never concatenate paths in `**File**`
- Anchor missing code to the nearest existing line with a direction: `path/Test.java:120 (after — insert the regression test here)`
- Label every finding with **Confidence**: `Confirmed` (proven from code), `Suspected` (plausible, evidence named in the Recommendation), or `Needs runtime check` (depends on data, load, or environment)
- Report suspected bugs at Major or Blocker when the plausible consequence is severe — a suspicion is not a reason to drop a finding
- Include code snippets when suggesting changes (use diff format for clarity)
- Keep findings concise (2-4 sentences per issue); explanation outranks brevity for complex findings — never strip the why to hit the cap
- Group related findings together
- Reference symbols/functions by name in backticks: `` `handleSubmit()` ``
- Write every finding in plain language: the **Issue** names the exact behavior and why it's wrong, the **Impact** is a specific consequence, and the **Recommendation** is a concrete fix or next step. Every finding gets a Recommendation — one without it is incomplete
- For clean reviews with no findings in a severity tier, omit that section rather than writing "None identified"
- Add a `**Location**: `path:LINE`` line per finding only when the requester needs machine-readable output or PR-inline comments (see **finding-anchors.md**)

## Non-expert test
Before delivering, read each finding as the developer who must act on it. Pass means each finding lets them state:
1. What is wrong (plain language, no jargon)
2. Why it matters (specific consequence)
3. What to do (concrete fix or next step)

Fail → tighten the vague field. Every finding must pass — not just the top ones. Shared doctrine: **../investigate-code/reference/plain-language-presentation.md**.

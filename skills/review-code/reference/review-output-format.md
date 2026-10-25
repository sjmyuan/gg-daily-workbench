# Review Output Format

Standard template for all review output. Every finding anchors to one line — see **finding-anchors.md** for the anchor rules.

````
## Code Review Summary

**Scope**: [Brief description of what was reviewed]
**Focus Areas**: [e.g., correctness, security, performance, blast radius]
**Reviewed**: [N files, +A/-B — list every changed file with its line count]
**Overall Assessment**: [Brief evaluation - e.g., "Ready to merge with minor changes"]
**Ready to merge?**: [Yes | No | With fixes] — [one-sentence technical reasoning]
**Repo expertise**: [sources used, or "none found — see gaps"]
**Open challenges**: [N open, M blocking] · **Unverified referents**: [N]

---
## ❓ Challenges & Questions

> Omit this section only when no challenge survived — never to keep the report shorter.

| # | Question | Why it looks unreasonable | Assumed meanwhile | Settles it | Blocking |
|---|---|---|---|---|---|
| C1 | Should `Pricing` stay in `src/orders/do-something/`? | No rule or sibling module puts feature code in a feature folder | Reviewed as if the package stays put; the currency finding assumes it | A documented placement rule, or a sibling precedent | yes |
| C2 | Is the `order-discount` module intended to exist? | The path appears only in the branch name, not in the tree | Treated as a path error, not a design change | The author confirming the module is new | maybe |

- `Blocking: yes` forces the verdict to `No` or `With fixes` until answered — say which findings depend on the answer.
- A challenge is not a finding: it has no proven defect, so it never carries a severity.
- Ask one answerable question per row; never bundle two decisions into one challenge.
- When the challenge questions a claim another agent returned, raise it through `question-everything` and keep its `C<N>` id.

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
## Repo Expertise Applied

*One row per rule or fact that changed a finding's severity, wording, or outcome; cite the source line.*

| Source | Rule or fact | Effect on this review |
|---|---|---|
| `AGENTS.md:31` | All outbound retries go through `resilience-kit` | Escalated the hand-rolled retry loop to 🔴 Major |

**Repo expertise gaps**: [sources absent or silent on the changed area — each one is a challenge above]

---
## Referent Check

*Include only when a referent is unverified; list every one with the search that failed.*

| Referent | Status | Evidence |
|---|---|---|
| `src/orders/do-something/Pricing.java` | resolved | `src/orders/do-something/Pricing.java:18` |
| `src/orders/order-discount/Pricing.java` | unverified | `git ls-files 'src/orders/*Pricing.java'` → 1 path |

---
## Risks & Assumptions

*Only assumptions that need no answer. Anything whose answer could change the verdict belongs in
Challenges & Questions instead — never here.*

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
- Put Challenges & Questions before Findings; a blocking challenge must agree with the merge verdict, and the summary must count both open challenges and unverified referents
- Ground every path, package, symbol, flag, and config key per **referent-grounding.md** — a referent you did not read is labeled `unverified` with the failed search, never presented as fact
- Never recommend a move, extraction, rename, or new directory without citing the rule, ADR, observed structure, or build constraint that places code there
- Cite the source line whenever repo expertise drives a severity, a name, or a placement — "the project style" is not evidence
- Add a `**Location**: `path:LINE`` line per finding only when the requester needs machine-readable output or PR-inline comments (see **finding-anchors.md**)

## Non-expert test
Before delivering, read each finding as the developer who must act on it. Pass means each finding lets them state:
1. What is wrong (plain language, no jargon)
2. Why it matters (specific consequence)
3. What to do (concrete fix or next step)

Fail → tighten the vague field. Every finding must pass — not just the top ones. This is the same
plain-language doctrine the document-findings pipeline applies; keep the wording local to this skill.

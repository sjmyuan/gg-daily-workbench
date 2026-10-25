# Pipeline Integration Design

Used by **create-skill-file** (pipeline step 11) and **validate-created-skill** (check 12).

When a skill is part of a multi-skill pipeline (one skill's output is consumed by another), verify these 5 integration points:

1. **Handoff mechanism**: the producing skill includes an export/persist capability that writes output to a file; the consuming skill defines an input schema and supports loading from files. Do not rely on conversation text as the sole transport layer.
2. **Shared schema (consumer-owned)**: the consuming skill defines the format in one literal template; the producing skill writes compliant output and its examples reproduce that template's headings, fields, order, and statuses. Disagreement → the consumer wins; drift → 🔴 Major.
3. **One-way awareness (caller → callee)**: the caller names the callee and states what it hands over; the callee describes the shape of its input and names no caller. A caller name inside the callee → 🟡 Minor. Details: **Dependency direction** below.
4. **Guard clauses**: the callee's when-to-use includes a constraint preventing premature loading (e.g., "Do NOT load when no plan has been generated yet"), stated as an input condition, never as "when skill X calls this".
5. **Link self-containment**: every markdown path resolves inside the skill's own folder; another skill is named, never deep-linked (`../other-skill/reference/x.md`). A skill may be installed alone, so an escaping link resolves to nothing and fails silently. Shared doctrine is duplicated as a slice with a `Scope:` header, never shared by path. Check with `review-skill`'s `check_skill_links.py <skill-dir>`, or by reading every link path and confirming it stays inside the folder; each `ESCAPE`, `ABS`, or `CROSSPATH` finding is a defect.

## Dependency direction

A skill that others load is a library: it declares what it needs, never who needs it.

| Position | Allowed | Banned |
|---|---|---|
| Caller names callee | "hand the claim to `question-everything`" | — |
| Callee names what it invokes | "apply `question-everything`'s verification protocol" | — |
| Callee names who loads it | — | "inside the `conduct-spike` pipeline", "when `review-code` calls this", "via the `plan-development-task` skill" |

- Mutual invocation is allowed: two skills may each hand work to the other in different phases. The ban is on naming the **actor that loads the callee**, not on naming a skill the callee uses.
- A callee may name the producer of an artifact it consumes, but phrase it as the artifact: "a spike findings doc", not "when `conduct-spike` runs you".

Why: a caller list couples the callee to every adopter and goes stale on the next one; the callee's triggers stop describing its job and start describing other skills.

## Callee test

1. List every skill and agent name in the callee — description, when-to-use, rules, capabilities.
2. Keep each name the callee invokes or consumes a protocol or artifact from.
3. For every other name, ask: does this sentence tell the reader **who will load this skill**? If yes, replace the actor with the input shape.
4. Re-read the callee alone: each trigger must make sense to someone who has never seen its callers.

| Before (caller-shaped) | After (input-shaped) |
|---|---|
| "User is running a spike (via the `conduct-spike` skill)" | "A spike area investigation exists and needs an ADR" |
| "Inside a spike pipeline (via `conduct-spike`)" | "A multi-step pipeline returns a sub-agent result that must be verified" |
| "When `review-code` raises a challenge" | "A returned agent claim must be verified before it is trusted" |

## Severities

| Defect | Severity |
|---|---|
| Callee names the skill or agent that loads it | 🟡 Minor — coupling and staleness |
| Callee trigger only parses with a caller's name | 🟡 Minor — rewrite around input shape |
| Caller does not name the callee or state the handoff | 🟡 Minor — invisible dependency |

Apply when the user describes a workflow involving multiple skills (e.g., "first plan, then execute").
When artifacts cross the boundary, apply **artifact-consistency**: one owner template, examples on
both sides reproduce it, shared examples update together.

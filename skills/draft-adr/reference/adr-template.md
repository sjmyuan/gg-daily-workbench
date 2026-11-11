# ADR Template

When producing the final ADR document, use the exact structure below. Wrap placeholders in `{{ }}` and fill them in based on the discussion with the user. Apply **reference/writing-style.md** — BLUF takeaway under every heading, prose capped, detail carried by tables, diagrams, and diffs. Every diagram satisfies **reference/diagram-contract.md**.

````markdown
# {{YYYY-MM-DD}}-{{TITLE}}

* Status: {{STATUS:draft | adopt | declined | superseded}}
* Area: {{AREA}} <!-- optional; required for spike ADRs, matching scope.md -->
* Owners: [ Who started and drives the ADR ]
* Date: {{DATE}}

## Context and Problem Statement

**Decision:** [ one-line takeaway — the decision question this ADR answers and its outcome — ≤15 words ]

[ ≤3 sentences, SCQA: Situation → Complication → Question → Answer. Never lead with background. ]

![Context diagram: system(s) in scope, actors, volumes, and external dependencies]({{DIAGRAM:context}})
[ Embed the C4 context diagram drawn during define-problem, plus any flowchart or sequence diagram used to zoom into the context. For architecture diagrams use C4 Models see https://c4model.com ]

## Decision Outcome

**Chosen:** "[ Option N: <name> ]" — [ 1-sentence justification tied to specific drivers, e.g. "meets KO driver #1 (ACID); best on cost & team expertise" ].
**Start here:** [ `C1` — the first change in the Implementation Plan, for the reader who came to implement ]

![C4/flowchart: target state with the chosen option integrated into the context]({{DIAGRAM:solution}})
[ Embed the target-state view drawn during compile-adr. Mark every NEW / CHANGED / REMOVED element. ]

## Consequences

[ 1-line trade-off takeaway, e.g. "**Trade-off:** self-managed ops for lower cost." Keep to ≤4 items per subsection. ]

### Positive Consequences <!-- optional -->

* [ one claim per bullet, ≤10 words, no justification ]
* ...

### Risks <!-- optional -->

* [ one claim per bullet, ≤10 words ]
* ...

### Security

* [ one claim per bullet, ≤10 words ]
* ...

## Decision Drivers

* `HC 1` [ driver — metric, threshold, and measurement. One fact per bullet; ≤6 drivers ]
* `SP 1` [ driver — metric, threshold, and measurement ]
* ...

## Considered Options

Assign each option a stable label `Option N: <name>` here; reuse it verbatim in every later section.

* Option 1: <name>
* Option 2: <name>
* ...

![Option comparison matrix: drivers × options with knock-out highlights]({{DIAGRAM:comparison-matrix}}) <!-- optional: omit when the table below carries the numbers -->
[ Embed the option comparison matrix drawn during evaluate-options, or delete this line. Add an elimination tree only when each knock-out changes the next question. ]

| Driver | Option 1: <name> | Option 2: <name> |
|---|---|---|
| `HC 1` <driver + threshold> | ✅ [ measured value ] — [ evidence ] | ❌ [ measured value ] — [ evidence ] |
| `SP 1` <driver + threshold> | ⚠️ [ measured value ] — [ evidence ] | ✅ [ measured value ] — [ evidence ] |

[ The matrix is the summary. A card's Driver impact rows add evidence and confidence; a mark never differs between the two. ]

## Evaluation of the Options <!-- required -->

Repeat the block below once per option, in `Option N` order, using the option's exact `Option N: <name>` label.

### Option N: <name>

#### Verdict

[ one line: recommended / dropped + which driver decides — ≤15 words ]

#### What it is

[ 1–2 sentences — the runtime shape: components, data store, protocol, deployment unit ]

#### How it works

1. [ trigger or request → component → effect, naming the protocol ]
2. [ next step of the flow ]
3. ...  <!-- 3–7 steps: the flow, not prose -->

#### Driver impact

| Driver | Mark | Measured value | Evidence | Confidence |
|---|---|---|---|---|
| `HC 1` <driver> | ✅ / ⚠️ / ❌ | [ number ] | [ link or `file:line` ] | verified / inferred / unverified |

#### Concerns

| Concern | This option |
|---|---|
| New infrastructure | [ what must be provisioned ] |
| Interfaces touched | [ endpoint, event, queue + payload shape ] |
| Data and consistency | [ store, transaction scope, read model ] |
| Failure behaviour | [ timeout, duplicate, partial-failure handling ] |
| Operational load | [ who runs it, alerts, on-call impact ] |
| Cost model | [ number + unit ] |
| Migration cost | [ steps, downtime, reversible? ] |

#### Pros

* [ one claim per bullet — names the driver it moves, no justification ]
* ...

#### Cons

* [ one claim per bullet — names the driver it moves, no justification ]
* ...

#### Tech Details <!-- include for every option whose code is accessible -->

[ Target-state diagrams for this option per reference/diagram-contract.md: C4 delta (NEW / CHANGED / REMOVED) + sequence diagram(s) with the failure path. ]

**Code changes** — one entry per change, using the IDs the Implementation Plan orders:

1. **`C1` — `file:line` symbol** (confidence: verified / inferred / unverified)
   - Current: [ what the code does today, quoted from the evidence ]
   - Diff:

   ```diff
   diff --git a/<file> b/<file>
   --- a/<file>
   +++ b/<file>
   @@ -<start>,<count> +<start>,<count> @@
    context line
   -removed line
   +added line
   ```

   - How: [ 1–2 sentence instruction to make the change ]

## Implementation Plan

<!-- The change set and its order. Step-level TDD planning belongs to the delivery plan, not here. -->

**Order:** [ `C1` → `C2` → `C3`; the safe stop point, e.g. "safe to stop after C2" ].

**Prerequisites:** [ infrastructure provisioned, config keys set, feature flag created, migration applied ]

| ID | Change | Location | Depends on | Verify | Rollback |
|---|---|---|---|---|---|
| `C1` | [ what changes ] | `file:line` symbol | — | [ command or assertion that proves it ] | [ revert or flag-off step ] |
| `C2` | [ what changes ] | `file:line` symbol | `C1` | [ command or assertion ] | [ revert step ] |

**New files:** [ name — purpose, one line each ]

## References <!-- optional -->
````

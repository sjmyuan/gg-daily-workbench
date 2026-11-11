# Option Tech Details Guide

Tech details make each option implementable in the repo: the target-state diagrams and the grounded change set — where each change happens and how to make it. Produced per option by **detail-options-tech**, grounded in code investigation evidence, never assumption. They let the reader evaluate technical feasibility, not just pros and cons.

## Evidence base (grounding contract)

Determine the evidence base before producing anything:
- **Existing evidence**: the area's evidence doc from the `conduct-spike` pipeline (`docs/evidence-<area>.md` — entry points, key locations, call chains, evidence ledger). Use it directly — do not re-scan covered code.
- **No evidence, code accessible**: build a lightweight evidence map on demand via the `investigate-code` skill — entry points, key locations with `file:line`, call chains for the affected flows.
- **No evidence, no code access**: produce architectural-level change profiles; mark every location/scope **unverified**; recommend a spike (`conduct-spike`) before relying on them.

## What each option's tech details contain

### 1. Target-state diagrams

Per **reference/diagram-contract.md**:
- **C4 view** (container or component): this option's to-be, evolved from the findings doc's current state, with every node marked `NEW` / `CHANGED` / `REMOVED`.
- **Sequence diagram(s)**: the key flow(s) this option changes — the happy path plus its failure path (timeout, retry, compensation).
- Diagrams are **option-specific** — never reuse another option's diagram or the chosen-solution diagram.

### 2. Change set

Every change gets a stable ID (`C1`, `C2`, …) per option, reused in the ADR card and the implementation plan.

| Field | Content |
|---|---|
| ID | `C1`, `C2`, … — unique within the option |
| Location | `file:line` + symbol |
| Current | What the code does today — quoted from the evidence map |
| Diff | **Git-style diff code block** for existing code: `diff --git a/… b/…`, `--- a/…` / `+++ b/…`, `@@` hunk, `-` / `+` lines with context. For a config-only change, state the exact key and value instead |
| How | 1–2 sentence instruction to make the change |
| Confidence | verified / inferred / unverified |

Also state, per option:
- **New files** — name + purpose, one line each; no diff.
- **Config and dependency changes** — keys, env vars, starters, or versions, with the file that carries them.
- **Data changes** — schema migration, backfill, dual-write window, and whether it is reversible.
- **Tests affected** — suites to update or add, per change.
- **Runtime changes** — new ports, topics, queues, permissions, or deployment units.

```diff
diff --git a/src/main/java/com/pay/BankTransferService.java b/src/main/java/com/pay/BankTransferService.java
--- a/src/main/java/com/pay/BankTransferService.java
+++ b/src/main/java/com/pay/BankTransferService.java
@@ -1,4 +1,6 @@
+@RestController
+@RequestMapping("/transfer")
 @Service
 public class BankTransferService {
@@ -88,7 +92,12 @@ public class BankTransferService {
 public void transfer(TransferRequest req) {
   ...
 }
+
+  @PostMapping
+  public void transferEndpoint(@RequestBody TransferRequest req) {
+    transfer(req);
+  }
 }
```

Focus diffs on **existing code** — the reader needs location and how-to, not assumed knowledge.

## Grounding rules

- Every change traces to the evidence map — entry point → key location → call chain. Cite `file:line`; never "the service layer".
- **Never invent** APIs, symbols, or files. If a change needs something the investigation did not establish, mark it **unverified** and offer to investigate.
- **Never assume the user already knows a change** — spell out every change explicitly, even obvious ones.
- Confidence: **verified** (directly read), **inferred** (derived from surrounding code), **unverified** (assumption). Present inference as inference.
- Diagrams derive from the evidence's current state; do not draw structures the investigation did not establish.
- A change with no verification step is incomplete — name what proves it landed.

## Output format (per option)

````markdown
### Option N: <name>

#### Tech Details

[ C4 delta + sequence diagram(s) including the failure path ]

**Code changes:**

1. **`C1` — `file:line` symbol** (verified / inferred / unverified)
   - Current: [ quote from the evidence map ]
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
   - How: [ 1–2 sentence instruction ]

**New files:** [ name — purpose ]

**Config / dependencies:** [ key or dependency — file ]

**Data changes:** [ migration, backfill, reversibility ]

**Tests affected:** [ suite — what changes ]
````

## Relationship to the ADR

Each option's tech details render as its `#### Tech Details` subsection inside **Evaluation of the Options** (see **reference/adr-template.md**). The chosen option's change IDs are then ordered, verified, and given rollback lines in `## Implementation Plan`; the plan references the diffs, never restates them.

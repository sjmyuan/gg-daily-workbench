# Option Tech Details Guide

Tech details make each option implementable in the repo: the target-state diagrams and the grounded change set — where each change happens and how to make it. Produced per option by **detail-options-tech**, grounded in code investigation evidence, never assumption. They let the reader evaluate technical feasibility, not just pros and cons.

## Evidence base (grounding contract)

Determine the evidence base before producing anything:
- **Existing evidence**: the area's cited evidence from the `conduct-spike` pipeline (its ADR citations or findings doc — entry points, key locations, call chains). Use it directly — do not re-scan covered code.
- **No evidence, code accessible**: build a lightweight evidence map on demand via the `investigate-code` skill — entry points, key locations with `file:line`, call chains for the affected flows.
- **No evidence, no code access**: still show each change's real file content — an added-only diff for a new file, the exact config block for an existing one — mark every location **unverified**, and recommend a spike (`conduct-spike`) before relying on it. A prose description is not a change.

## What each option's tech details contain

### 1. Target-state diagrams

Per **reference/diagram-contract.md**:
- **C4 view** (container or component): this option's to-be, evolved from the findings doc's current state, with every node marked `NEW` / `CHANGED` / `REMOVED`.
- **Sequence diagram(s)**: the key flow(s) this option changes — the happy path plus the failure path it adds, or `none new` when it adds none.
- Diagrams are **option-specific** — never reuse another option's diagram or the chosen-solution diagram.

### 2. Change set

Every change gets a stable ID (`C1`, `C2`, …) per option, reused in the ADR card and the implementation plan.

| Field | Content |
|---|---|
| ID | `C1`, `C2`, … — unique within the option |
| Location | `file:line` + symbol |
| Current | What the code does today — the real lines, quoted from the evidence map |
| Diff | A git-style diff of **real code** — actual file lines, `-` / `+`, real hunk headers. Every change carries one: existing code, config, DDL, and dependencies. A new file gets an added-only diff |
| How | 1–2 sentence instruction to make the change |
| Confidence | verified / inferred / unverified |

#### The diff contract

1. **Read first.** Open the region at `file:line` and copy its real lines. A diff written from memory is a fabrication.
2. **Diff syntax only.** Inside the fence: `diff --git`, `---`, `+++`, `@@`, and real code. No `...`, no `<placeholder>`, no `// add X here`, no English sentence.
3. **Never elide a hunk.** Quote the enclosing method, or split into several hunks with real line numbers. `...` inside a hunk is a defect.
4. **A new file gets an added-only diff** with its real content — full, or its complete structure with real signatures. "Name — purpose" is not a change.
5. **Config, DDL, dependency → diff the real file** (`yaml`, `sql`, `gradle`). "Set the key to X" is prose, not a change.
6. **Unread code → no diff.** Mark the change `unverified`, name the check that closes it, never invent a symbol, signature, or line.
7. **No speculative defence.** A guard, retry, timeout, or validation enters a diff only for a failure this option introduces or a driver that names it.

Self-check before presenting: every `-` line exists verbatim at its `file:line`; every `+` line is code, not a comment about code; the hunk header counts match the hunk.

| Rejected | Why |
|---|---|
| `+// add the REST wrapper here` | A comment describing code is not code |
| `+...existing code...` | The diff no longer applies; the reader cannot review it |
| `- Diff: add @RestController to the class.` | Prose where the diff belongs |
| `+    return paymentClient.send(req);` with `paymentClient` unread | Invented symbol; mark `unverified` instead |

```diff
diff --git a/src/main/java/com/pay/BankTransferService.java b/src/main/java/com/pay/BankTransferService.java
--- a/src/main/java/com/pay/BankTransferService.java
+++ b/src/main/java/com/pay/BankTransferService.java
@@ -1,2 +1,4 @@
+@RestController
+@RequestMapping("/transfer")
 @Service
 public class BankTransferService {
@@ -88,5 +92,10 @@ public class BankTransferService {
   public void transfer(TransferRequest req) {
     validate(req);
     bankTransferRepository.save(req);
   }
+
+  @PostMapping
+  public void transferEndpoint(@RequestBody TransferRequest req) {
+    transfer(req);
+  }
 }
```

Also state, per option:
- **New files** — name + purpose; each one's content appears as an added-only diff under its `C` id.
- **Config and dependency changes** — their diffs, plus the file that carries each key.
- **Data changes** — schema migration, backfill, dual-write window, and whether it is reversible.
- **Tests affected** — suites to update or add, per change.
- **Runtime changes** — new ports, topics, queues, permissions, or deployment units.

## Concreteness test

Run on "What it is" and "How it works" before presenting. A card that names no element of this repo is generic, however correct it reads.

- **Swap the option's name for a competitor's.** If the sentence still reads true, rewrite it — it describes a category, not this option.
- **Every noun is a repo symbol** (`PaymentOrchestrator`), a named technology (`spring-kafka`), or an element the change set creates (`PaymentCommand`).
- **Every flow step names the symbol it enters and the symbol it leaves**: `processPayment` → `kafkaTemplate.send("payment-commands")` → `onPaymentCommand`.
- **No unnumbered adjective.** "Scalable", "simple", "robust", "modern" become the number or the mechanism that earns the claim.

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

[ C4 delta + sequence diagram(s) with the failure path it adds, or `none new` ]

**Code changes:**

1. **`C1` — `file:line` symbol** (verified / inferred / unverified)
   - Current: [ the real lines from the evidence map ]
   - Diff: [ the real lines at that location — see **The diff contract**; never a summary or a placeholder ]
   - How: [ 1–2 sentence instruction ]

**New files:** [ name — purpose; added-only diff under its `C` id ]

**Config / dependencies:** [ its diff, plus the file that carries the key ]

**Data changes:** [ migration, backfill, reversibility ]

**Tests affected:** [ suite — what changes ]
````

## Relationship to the ADR

Each option's tech details render as its `#### Tech Details` subsection inside **Evaluation of the Options** (see **reference/adr-template.md**). The chosen option's change IDs are then ordered, verified, and given rollback lines in `## Implementation Plan`; the plan references the diffs, never restates them.

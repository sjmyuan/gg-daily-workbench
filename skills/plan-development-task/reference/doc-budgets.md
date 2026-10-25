# Document Budgets

Caps and responsibilities for the docs a cell carries: `index.md`, `context.md`, `plan.md`,
and `rework-<date>.md`.

## Artifact responsibilities

Delivery side only: **index = state · context = charter · plan = execution · rework = delta · git/PR = record.**
Spike artifacts and their owners are out of scope here; a decision-changing fact is never copied into a cell doc.

- **index = state.** It points to the cell; it never explains it.
- **context = charter.** It holds invariants; it never holds steps.
- **plan = execution.** It holds steps; it never explains the background.
- **rework = delta.** It holds only changed steps; it inherits the charter by reference.
- **git / PR / CI = record.** History and reproducible proof — never copied into a doc.

Flow: `index` → dispatch brief → `context` + `plan` → execute → plan step notes + latest `## Execution` → git/PR → `rework` (plan stays frozen).

## Evidence routing

There is **no `evidence-raw.md`**. Every piece of evidence has a consumer and a home.

| Evidence | Home | Consumed by |
|---|---|---|
| Current-state fact | `spikes/<spike>/docs/evidence-<area>.md` (claim ID, `file:line`, confidence) | ADRs, solution doc, planner |
| Decision | `adrs/adr-*.md` | Planner, executor, gate |
| Target state | `solution.md` | Planner, gate |
| Execution proof | The step's `Validation` line in `plan.md` + commit + CI/PR | Executor, gate, human |
| History | Git commits, PR, `rework-<date>.md` | Human, auditor |
| Deferred concern | `context.md` `## Open concerns` | Gate, integration review |

- A reproducible test/build result is never transcribed — cite the command and the commit.
- A new fact that changes a decision goes through the owning spike artifact (`document-findings` update → `draft-adr` → solution doc). Never a parallel raw file.
- Existing `evidence-raw.md` and `evaluation-report.md` files are legacy history — leave them; never create a new one.

## Hard budgets

| File | Target | Hard ceiling |
|---|---|---|
| `context.md` | 40–60 lines / 3–4k chars | 120 lines / 8k chars |
| `index.md` | 60–100 lines / 4–6k chars | 120 lines / 8k chars |
| `plan.md` | step-count driven (caps per **plan-quality-checklist**) | no doc-size cap |
| `rework-<date>.md` | delta only | no doc-size cap |

- **Chars are the gate** (≈ tokens × 4); lines are secondary. Measure: `wc -l`, `wc -m`.
- **Filling the ceiling is a smell** — a charter at 8k is a workbook. Over the ceiling is a write failure.

## The admission test

Apply to every line in `context.md`:

| Test | Question | Fail → |
|---|---|---|
| **Survival** | Will this still matter after step 5? | It is a plan step or history. |
| **Uniqueness** | Is it already in `plan.md`, `index.md`, the ADR, or git? | Link it; never restate. |
| **Action** | If deleted, what would an agent do wrong? | Nothing → delete. |
| **Reader** | Which reader needs it: planner, executor, verifier, L0, human? | No reader → delete. |

**Pre-flight findings are not context.** A resolved finding becomes a plan decision.
An unresolved one becomes an **Unknown**. The raw investigation is not persisted.

Never write steps, plan decisions, feature status/branch/PR, pre-flight tables, commit tables,
test matrices, deviation narratives, or incident retellings — those live in `plan.md`,
`index.md`, or git/PR. Branch and base live in the `plan.md` header, mirrored as state in `index.md`.
Restated ADR text is a one-line decision + link.

## context.md charter template

```markdown
# Context: <cell> — <outcome in one line>

**Outcome:** <what exists when this cell is done>

## Why
<2–3 lines: problem, decision served, ADR link; state "adopted / do not re-litigate" if settled>

## Must hold
<≤6 bullets: user-ratified constraints + operational invariants not already in plan.md>
- <platform version> only; no <forbidden distribution route>; zero deps.
- No branch; push only after confirmation.
- Never write <protected path>; never touch the <service/port>.

## Unknowns
<≤5 bullets: unknown — resolving step — fallback; DELETE when resolved>
- <unknown> → Step N measures; fallback.

## Done means
<≤5 rows: criterion | verification | pass rule>

## Pointers
<≤6 bullets: ADR, solution-doc section, findings, evidence — cell-specific paths only, never copies>

## Open concerns
<≤5 bullets: deferred Minor/risk — owner or next action; DELETE when resolved>

## State
| Field | Value |
|---|---|
| Active plan | `plan.md` or `rework-<date>.md` |

## Execution
<latest handoff only — 5 rows; see below>

## Reworks
<≤8 rows: date | mode | cell | trigger | file | status; drop oldest done rows — files remain; create with the first row>

## Amendments
<≤8 rows: date | trigger | added | abandoned | boundary | reason; ⏭ markers are the record; create with the first row>
```

## Expiry rule

Context must **shrink**, not only stop growing:

- A resolved **Unknown** → record the outcome in the resolving step's plan note → delete it from context.
- A resolved **Open concern** → delete it; the closing commit or rework file is the record.
- A constraint that becomes a plan decision or Scope Boundary entry → delete it from context.
- During execution only `## Open concerns`, `## State`, and `## Execution` change. The charter sections and the manifests are planner-owned and frozen.

## Latest handoff (replaces, never appends)

`## Execution` is one block per cell, overwritten each round:

| Field | Content |
|---|---|
| Status | `DONE` · `DONE_WITH_CONCERNS` · `BLOCKED` · `NEEDS_CONTEXT` |
| Commits | `base7..head7` |
| PR | number/URL, or `pending approval` |
| Test evidence | 1 line: command + pass/fail |
| Review outcome | 1 line: `review-code` result |

Deferred concerns go to `## Open concerns` — they persist across rounds and are deleted when resolved.
Never append a round to `context.md`.

## index.md

`index.md` is a **state board**, not a report — ceiling 8,000 chars / 120 lines. It points to the cell; it never explains it. The orchestrator owns its template, feature table, and archive rule.

## Checklist

- [ ] `context.md` is 40–60 lines and ≤8,000 chars; every line passes the admission test.
- [ ] `index.md` ≤8,000 chars / ≤120 lines; state only.
- [ ] `plan.md` holds steps, TDD rationale, and decisions — context does not repeat them.
- [ ] `rework-<date>.md` holds only the delta; the original plan is untouched.
- [ ] No log file exists; execution proof is a plan `Validation` line + commit/CI.
- [ ] A POC is a normal implementation; its MR is the evaluation vehicle — no report or verdict.
- [ ] `## Execution` holds the latest round only; concerns persist in `## Open concerns`.
- [ ] Resolved unknowns and concerns are deleted, not archived.
- [ ] Completed waves archived; pointer line present.

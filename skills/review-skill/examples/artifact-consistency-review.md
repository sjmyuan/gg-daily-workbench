# Example: Artifact Consistency Review — Examples vs Canonical Template

**Scenario**: A skill ships a plan template and eight examples that emit plans. The user asks: "Check the examples — are they consistent?" Demonstrates **review-skill-file** step 11 (template fidelity, set-level continuity, machine checker).

**Applies**: **review-skill-file**

## Input

- `reference/plan-file-format.md` — prose describes the plan layout, no fenced skeleton.
- Eight examples emit `plan.md`-style blocks with four different step shapes.
- Two examples share the same payment-migration scenario.

## Findings

| # | Severity | Finding | Fix |
|---|---|---|---|
| 1 | 🔴 Major | Template is prose-only; no literal skeleton to compare against | Add one fenced skeleton with fixed field order to the owner reference |
| 2 | 🔴 Major | Examples use four step shapes: `- **Step N**`, `- Step N`, `1. **Title** —`, `### Step N` + fields | Make every example reproduce the owner skeleton |
| 3 | 🔴 Major | The executor requires six fields; examples show three or four (`Source` missing everywhere) | Adopt the consumer's schema (six fields) and update all examples |
| 4 | 🟡 Minor | Abridged plans are presented as complete — no `(abridged)` label | Label excerpts or expand them |
| 5 | ⚠️ Inconsistency | Branch is recorded in `context.md` in one file, `plan.md` in another, `index.md` in a third | Pick one home (plan header); make the others point |
| 6 | 🟡 Minor | Same scenario uses `findings-service-boundaries` vs `findings-service-decomposition`; 4 problems vs 5 ADRs | Reuse one set of identifiers and counts |
| 7 | 🔴 Major | A rework example declared as shared by two skills uses an older format in one skill | Update both skills in the same change |

## Machine check

```text
reference/plan-file-format.md:1: TEMPLATE no fenced skeleton
examples/plan-a.md:12: STEP fields ['Objective','Files','Implementation','Status'] != ['Objective','Files','Source','Implementation','Validation','Status']
examples/plan-b.md:8: ZONE zones ['May change','Expected files'] != ['May change','Expected files','Must not change','Protected zones']
```

## Canonical variants to confirm

- **Step schema**: six fields with mandatory `Source` (recommended — matches the consumer) vs five fields.
- **Boundary home**: `plan.md` header (recommended) vs `context.md`.

Ask the user which is canonical before recommending a rewrite; never pick silently.

## Positive highlights

- The owner reference already documents zone semantics and step-status vocabulary.
- The examples are realistic and cover distinct change types; only the shape drifted.

## Risks & assumptions

Static review only — no runtime execution. The consumer's schema was treated as authoritative per
**pipeline-integration**; if the producer intentionally overrides it, finding 3 changes direction.

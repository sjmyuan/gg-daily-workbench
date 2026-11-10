# Example: Artifact Consistency Review — Examples vs Canonical Template

**Scenario**: A skill ships a plan template and eight examples that emit plans. The user asks: "Check the examples — are they consistent?" Demonstrates **review-skill-file** step 7 (template fidelity, set-level continuity, machine checker).

**Review Focus**: Example-set consistency — one owner template, four step shapes across the examples, identifier and count continuity, plus the machine checker.
**Applies**: **review-skill-file**

## Code Review Summary

**Scope**: One skill — `reference/plan-file-format.md` (prose, no fenced skeleton) and eight examples emitting `plan.md`.
**Focus Areas**: Template literalism, step/zone shape, abridged labelling, shared cross-skill example
**Overall Assessment**: A schema owner exists but is prose-only, so nothing anchors the examples; they have drifted into four step shapes and break the consumer's six-field contract.

---

## Findings

| # | Severity | Finding | Fix |
|---|---|---|---|
| 1 | 🔴 Major | Template is prose-only; no literal skeleton to compare against | Add one fenced skeleton with fixed field order to the owner reference |
| 2 | 🔴 Major | Examples use four step shapes: `- **Step N**`, `- Step N`, `1. **Title** —`, `### Step N` + fields | Make every example reproduce the owner skeleton |
| 3 | 🔴 Major | The executor requires six fields; examples show three or four (`Source` missing everywhere) | Adopt the consumer's schema (six fields) and update all examples |
| 4 | 🟡 Minor | Abridged plans are presented as complete — no `(abridged)` label | Label excerpts or expand them |
| 5 | 🟡 Minor | Same scenario uses `findings-service-boundaries` vs `findings-service-decomposition`; 4 problems vs 5 ADRs | Reuse one set of identifiers and counts |
| 6 | 🔴 Major | A rework example declared as shared by two skills uses an older format in one skill | Update both skills in the same change |

### Machine check

```text
reference/plan-file-format.md:1: TEMPLATE no fenced skeleton
examples/plan-a.md:12: STEP fields ['Objective','Files','Implementation','Status'] != ['Objective','Files','Source','Implementation','Validation','Status']
examples/plan-b.md:8: ZONE zones ['May change','Expected files'] != ['May change','Expected files','Must not change','Protected zones']
```

### ⚠️ Inconsistencies (Decision required)

#### Branch home
- **Variant A**: branch recorded in `context.md`
- **Variant B**: branch recorded in `plan.md`; **Variant C**: in `index.md`
- **Trade-offs**: `plan.md` is always read first and travels with the work; `index.md` is the only file the orchestrator reads.
- **Decision needed**: pick one home and make the other two point at it.

#### Step schema
- **Variant A**: six fields with mandatory `Source` (matches the consumer)
- **Variant B**: five fields
- **Decision needed**: confirm which schema is canonical; the consumer's six fields win by default.

Ask the user which variant is canonical before recommending a rewrite; never pick silently.

---

## Positive Highlights

- The owner reference already documents zone semantics and step-status vocabulary.
- The examples are realistic and cover distinct change types; only the shape drifted.

---

## Risks & Assumptions

Static review only — no runtime execution. The consumer's schema was treated as authoritative per
**pipeline-integration**; if the producer intentionally overrides it, finding 3 changes direction.

---

## Recommended Next Steps

1. Add one fenced skeleton with fixed field order to `reference/plan-file-format.md`. *(🔴 1)*
2. Rewrite all eight examples to the owner skeleton and re-run the machine check. *(🔴 2, 6)*
3. Adopt the consumer's six-field step schema, including `Source`. *(🔴 3)*
4. Label every abridged plan. *(🟡 4)*
5. Resolve the branch home and the duplicated scenario identifiers. *(⚠️, 🟡 5)*

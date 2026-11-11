# Example: Micromanaged Judgment Skill

**Scenario**: Review of `skills/review-api-design/SKILL.md` — a skill that tells an agent how to review an API design.
Every step is correct, and none of them changes what a capable model would already produce.

**Review Focus**: Prescriptiveness — regime, expert test, judgment content, behavioral evidence.
**Applies**: **review-skill-file**

## Code Review Summary

**Scope**: `skills/review-api-design/` — SKILL.md plus one example
**Focus Areas**: Regime fit, expert test, judgment content, evaluation
**Overall Assessment**: Refactor recommended — well structured, but it adds no capability. Nine steps restate a general REST checklist, and nothing separates a strong review from a mediocre one.

---

## Findings

### 🔴 Major

#### `<review-api-design>` scripts judgment work the model already performs
- **File**: [SKILL.md](SKILL.md#L20-L48)
- **Issue**: Steps 1–9 ("Read the spec", "List every endpoint", "Check naming", "Check status codes", …) are a generic checklist
  any capable model produces unaided. The skill never states what makes an API review strong.
- **Impact**: The steps spend context, anchor the reviewer to a surface scan, and displace a deeper plan. The output is identical with and without the skill.
- **Recommendation**: Cut steps 2–6. State the outcome — a review that names the tradeoffs the design makes and the failure it invites —
  then the contract that must hold, then the judgment content below.

### 🟡 Minor

#### No tradeoff, quality bar, or failure mode
- **File**: [SKILL.md](SKILL.md#L50-L58)
- **Issue**: Nothing says which side to prefer when idempotency, latency, and simplicity conflict. No bar separates acceptable from excellent, and no failure mode is named.
- **Recommendation**: Add a tradeoff table with the preferred side per situation, plus a three-criterion graded rubric per **evaluation-process**.

#### No exemplar of excellent, or of plausible-but-wrong, output
- **File**: `examples/review-example.md`
- **Issue**: The single example reviews a clean design cleanly. It cannot teach the call the skill exists to make.
- **Recommendation**: Show a short strong review next to a plausible-but-wrong one — flags naming while missing an unbounded list endpoint.

### 🟢 Nits / Suggestions

#### Ritual verify step
- **File**: [SKILL.md](SKILL.md#L60-L62)
- **Issue**: Step 9, "Verify the review is complete", restates step 3 and passes on a shallow review.
- **Recommendation**: Replace it with a gate or grade per **evaluation-process**.

---

## Positive Highlights
- Contractual parts are precise: output format and file anchors are exact, so the report shape is reproducible.
- Rules route cleanly and never restate a capability.
- The description triggers only on API-design review requests.

## Risks & Assumptions
- Assumes the intent is expert review, not checklist enforcement. A compliance intent would make steps 2–6 legitimate.
- No behavioral evidence is claimed, so this review cannot say whether the skill helps.

## Growth Audit
- Count line: `capabilities 1, steps 9, rules 2, guide rows 0, examples 1, chars 4,180`
- Superseded: steps 2–6 restate model defaults; retire them in the rewrite.
- Discriminative additions — tradeoff table, failure modes, exemplar — are investment, not unfunded growth.

## Recommended Next Steps
1. Cut steps 2–6; state the outcome and the contract. *(Resolves 🔴)*
2. Add the tradeoff table and the graded rubric. *(Resolves 🟡 quality bar)*
3. Add the plausible-but-wrong exemplar. *(Resolves 🟡 exemplar)*
4. Replace the ritual verify with the grade. *(Resolves 🟢)*
5. Run the baseline test once before shipping. *(Answers 🟢 behavioral evidence)*

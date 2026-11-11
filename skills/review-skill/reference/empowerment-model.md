# Empowerment Model (review)

Scope: decide how much the skill should prescribe, and whether it carries what beats the bare model.

Used by **review-skill-file** (step 2e).

## Regimes

| Regime | Recognise it by | Correct form |
|---|---|---|
| **Contractual** | Exact literals, order, schema, tool invocation, irreversible action | Ordered steps and guards; micro-steps are correct here |
| **Judgment** | Design, review, writing, analysis, planning, diagnosis | Outcome, tradeoffs, failure modes, exemplars; steps only where decidable |

An undeclared regime is reviewed as judgment: a capable model can follow a thin procedure, but cannot invent taste.

## Expert test

Ask of every step: would a competent expert need this instruction?

- No → micromanagement finding.
- Yes → confirm its reason appears once, in the knowledge entry or reference that owns the constraint.
- Unclear → the step restates model default behaviour; recommend tightening the objective.

## Findings

| Observation | Severity |
|---|---|
| A judgment capability scripted as steps the model would reproduce unaided | 🔴 Major — micromanagement |
| An isolated redundant step inside an otherwise sound capability | 🟡 Minor — the step spends context, not guidance |
| A contractual capability missing its exact literal, order, or irreversible-action guard | 🔴 Major — the model guesses |
| A judgment capability with no tradeoff, quality bar, or failure mode | 🟡 Minor — correct-but-mediocre output passes |
| A judgment capability with no exemplar of excellent, or of plausible-but-wrong, output | 🟡 Minor |
| A non-obvious constraint with no reason, or the reason repeated in every step | 🟢 Nit |
| No delegation boundary where the agent must make judgment calls | 🟢 Nit |
| A judgment skill with no behavioral evidence claimed and none on record | 🟢 Nit — recommend the author run the baseline test |

## Reading the balance

- Micromanaged: the steps are recoverable from the model alone.
- Thin: the judgment work has no content beyond the objective.
- Both are one defect — content that cannot change the output.

## Behavioral evidence

The author-side test compares output with and without the skill on representative tasks. A reviewer
cannot run it: check whether the skill or its author claims a result. No claim → 🟢 Nit, never a blocker.

# Plan Quality Rubric

Used by every `plan-*` capability, **amend-plan**, and **export-plan**. Grade the plan before presenting it.

Rows 1 and 7 are **pass/fail gates** — a fail blocks the plan. The rest are **graded**: a plan of only Acceptable rows is exportable, a plan with a Fail row is not. Grade, never tick: a conformant plan can still be weak, and that is what this rubric is for.

## The rubric

| # | Dimension | Excellent | Acceptable | Fail |
|---|---|---|---|---|
| 1 | **Evidence** | Root cause or requirement decomposition cites `file:line` and names the hypotheses ruled out | Cites the code it rests on | Plans from a suspected cause or from the request's wording alone |
| 2 | **Test strategy** | One strategy for the plan, each unit's proof named, exceptions named once | Strategy stated; most units name a proof | No strategy, or "write tests" as the only statement |
| 3 | **Units** | One unit per observable outcome; merges and splits each buy a distinct verdict | Units are coherent, a few phases bled in | Phase-shaped: RED / implement / refactor / cleanup as separate steps |
| 4 | **Ordering** | Every precondition is the base or an earlier step; contracts before consumers | No step depends on a later one | A step needs output from a later step |
| 5 | **Scope boundary** | Behavior-based zones, ratified, protected zones explicit and justified | Zones present, behavior-based | Path-based zones, or no boundary |
| 6 | **Risk** | Assumptions named with the step that tests each, the step expected to break first, and every stated guarantee decided | Risk block present | No risk content, a risk no step can falsify, or an open question on a stated guarantee left as an assumption |
| 7 | **Gate** | Green-only, evidence-backed commands, baseline recorded, no narrowing, waiver absent or ratified | Commands recorded, baseline present | Narrowed, invented, optional, or missing; waiver unratified |
| 8 | **Open by design** | Each unresolved-by-reading step names its check and fallback | Most such steps say what closes them | A diff, snippet, or pasted code in a step in place of a described approach — guessed or copied |
| 9 | **Docs** | `context.md` is a 40–60-line charter; no fact owned twice; no narrative in `plan.md` | Within budget, minor duplication | Charter over budget, or `plan.md` carrying background |
| 10 | **Presentation** | Route over the 2–3 riskiest steps, the plan's own answer to "what breaks first", one falsifiable self-check | A short walkthrough of the risky part | Opens with the full `## Steps` list |

## Grading

- **Exportable**: no Fail row, and rows 1 and 7 pass.
- **Revise**: one Fail row — fix it, do not re-grade the rest.
- **Stop and ask**: row 1 or 7 fails for a reason only the user can settle (an unratified waiver, an unknowable expected behavior).

## Presenting the plan

A plan is the largest artifact a user approves before any code exists. Brief before the question:

- Give a route over the 2–3 steps that carry the risk — not a walk through all of them.
- Ask the user which step they expect to break first, then reveal the plan's own answer from `## Risk`.
- Offer one self-check they can falsify before approving: the riskiest step's `Validation`, or the `Gate` line's evidence.
- Say what the plan deliberately left open, and what the executor will decide — that is the part the user is trusting.

## Refusals

- A plan with no `## Risk` block is not ready; the block is six lines, not an essay.
- A stated guarantee (never, always, exactly, once) with an undecided failure boundary is a **Fail on row 6**, however well the rest of the plan reads. Decide it, or ask before presenting.
- A step whose `Implementation` carries source code, a diff, or a snippet is not a plan — state the approach; the code belongs in the commit.
- A step count is never a quality argument in either direction. Cut a step because its verdict is duplicated; add one because its risk differs.
- A gate waiver written by an agent is a Fail on row 7, regardless of its wording.

# Behavioral Acceptance Test

Scope: prove the skill beats the bare model, not only the structural checks — and find the gap neither version catches.

Used by **validate-skill-procedure** (check 21) and **validate-created-skill**.

## When it runs

Run when the skill carries at least one judgment capability and representative tasks exist.

Batching several edits before one run is fine — the protocol grades the shipped skill, not each draft. A contractual-only skill is proven by its gates: report `behavioral: not run` and the reason.

The test answers two questions, and the second is the one that improves the skill: **does the edit move the output**, and **what does every version get wrong**.

## Claim register (write before the rubric)

One row per element the edit adds, changes, or retires:

| Element | Should move | Predicted | Observed |
|---|---|---|---|
| <step, rule, reference, example> | <rubric item> | + / 0 / − | filled after the run |

- An element that predicts **no** item is decoration: nothing can show it worked. Cut it.
- An element whose item stays **flat** is neutral. Keep it only if it carries a failure mode the task set does not exercise, and name that failure.
- Before cutting a restating element, name the rule it balances: a restating rule is often a **counterweight** ("ask before acting" against "deliver a draft"), and deleting it moves behaviour to the other pole.
- Write the register before freezing the rubric, so the rubric cannot be tuned to the edit.

## Protocol

1. Take three tasks: one typical, one hard, one near-miss outside the trigger. Prefer tasks whose answer depends on **repo state** — an existing plan, a prior decision, a stale artifact — because that is where a bare model most often misses.
2. For a skill that plans, reviews, or designs, make the hard task a **guarantee task**: an absolute clause ("never", "always", "exactly once") with a failure boundary the code cannot settle alone. Both arms fail it identically when neither decides the boundary, which makes it the best content-gap probe.
3. **Neutralise the task text.** The prompt must not name the behaviour under test. "Present it for confirmation" tells the model to present, and a competent model then invents the skill's structure unaided. Use what a user would actually say: "we need to sign off before the ADRs".
4. **Freeze the rubric** per **evaluation-process**, with two additions: one criterion **neither arm owns** ("would a reviewer approve this as-is" — a rubric built from the skill's own vocabulary cannot separate the skill from itself), and one **item per predicted element** from the register.
5. **Audit the instrument before the real run.** Score one known-good and one known-bad artifact. An item that cannot rate the good sample 2 and the bad sample 0 measures its own defect — typically one that penalises behaviour the skill's template mandates. Rewrite or drop it, and report the audit.
6. Use the **same instruction in both arms**, differing only in whether the skill is available. "Apply the skill" versus "use your own judgement" is two variables, not one.
7. Run each task **n≥3 per condition**. One run cannot separate a skill from a coin flip.
8. Score **blind, shuffled, per item**, with a separate scorer. Neutralise tokens that identify an arm (field names, file layout), and keep the rubric out of any tree the arms can read. State what still identifies the arm instead of claiming full blindness.
9. Keep each element only where treatment scores higher **on the item that element predicted**. A higher total with flat predicted items is noise; a lower predicted item is a regression to fix or revert.
10. After fixing a defect the run exposed, re-run **only the affected cells**, against the unchanged baseline, and report it as a labelled follow-up round. Never edit the frozen rubric between rounds — a rubric change starts a new run.
11. Test the near-miss: the skill must not load, or must decline in one line.

## Record

Report per task, then per item. The second table decides what stays.

| Task | Baseline (n) | Skill (n) | Δ |
|---|---|---|---|
| | | | |

| # | Item | Baseline | Skill | Δ | Element it tests |
|---|---|---|---|---|---|
| | | | | | |

Also report the rubric, the model and scorer, the framing of each task, the run count, and the blinding limits. Report deltas; make no statistical claim from single-digit n.

## Reading the result

| Symptom | Cause | Fix |
|---|---|---|
| Tie under a prompt that names the behaviour | The prompt did the skill's work | Rewrite the task neutrally and re-run **before** concluding |
| Both flat under neutral framing | Skill restates model defaults | Delete what the expert test fails |
| Skill scores lower | Micro-steps displaced a better plan | Cut steps; state outcome and tradeoffs |
| Gain only on the hard task | Content is discriminative | Keep it; consider moving it to `reference/` |
| Gain only on state-dependent tasks | Value is continuity, not method | Narrow the skill to state and safety rails |
| Total rises, most items flat | One or two elements did the work | Keep those; justify or cut the rest |
| Both arms miss the same item | A content gap in the skill, not a tie | Fix the skill, then re-run that cell |
| An item moves for both arms | The instrument leaks — task text or rubric told them | Neutralise, re-run, and do not report the delta |
| An item penalises behaviour the template mandates | Instrument defect | Fix the rubric; discard that item's delta |
| Behaviour drifts one way after deleting a "redundant" rule | It was counterbalancing another rule | Restore it as one line, or state the balance where both live |
| Loads on the near-miss | Description too broad | Tighten the trigger phrase, not the scenario list |

## Execution probe (optional, cheap)

When the skill produces a plan, run the smallest task's artifact once per arm under one fixed executor prompt, and timestamp four milestones: start, first failing test, first source edit, gate green.

The probe catches what scoring cannot: plan-induced rework (a step that forces a revert), and the distance from approval to a trustworthy green. n=1 is a probe, never evidence.

## Limits

- **A tie is evidence about the prompt until framing is neutral.** The first run of a new protocol has indicted a working skill and cleared a broken one.
- A model scoring its own output is weak evidence; prefer a separate scorer or a human spot-check. A scorer from the same model family may prefer its own style — name the scorer in the record.
- Partial blinding is the normal case. Name what identifies an arm; never report a run as blind when the artifact text reveals it.
- Never compare against a strawman baseline.
- An untested skill is reported as untested, never as passing.

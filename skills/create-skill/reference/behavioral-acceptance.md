# Behavioral Acceptance Test

Scope: prove the skill beats the bare model, not only the structural checks.

Used by **validate-skill-procedure** (check 21) and **validate-created-skill**.

## When it runs

Run when the skill carries at least one judgment capability and representative tasks exist.

Batching several edits before one run is fine — the protocol grades the shipped skill, not each draft. A contractual-only skill is proven by its gates: report `behavioral: not run` and the reason.

## Protocol

1. Take three tasks: one typical, one hard, one near-miss outside the trigger. Prefer tasks whose answer depends on **repo state** — an existing plan, a prior decision, a stale artifact — because that is where a bare model most often misses.
2. **Neutralise the task text.** The prompt must not name the behaviour under test. "Present it for confirmation" tells the model to present, and a competent model then invents the skill's structure unaided. Use what a user would actually say: "we need to sign off before the ADRs".
3. Freeze the rubric first per **evaluation-process**; never edit it after seeing output.
4. Use the **same instruction in both arms**, differing only in whether the skill is available. "Apply the skill" versus "use your own judgement" is two variables, not one.
5. Run each task **n≥3 per condition**. One run cannot separate a skill from a coin flip.
6. Score blind, shuffled, with a separate scorer better than self-scoring.
7. Keep each element only where treatment scores higher. Flat or lower → decoration; delete or replace it — but first name the rule it balances. A restating rule is often a **counterweight** ("ask before acting" against "deliver a draft"), and deleting it moves behaviour to the other pole.
8. Test the near-miss: the skill must not load, or must decline in one line.

## Record

| Task | Baseline (n) | Skill (n) | Δ | Kept / cut |
|---|---|---|---|---|
| | | | | |

Report the table, the rubric, the model, the framing of each task, and the run count. Report deltas; make no statistical claim from single-digit n.

## Reading the result

| Symptom | Cause | Fix |
|---|---|---|
| Tie under a prompt that names the behaviour | The prompt did the skill's work | Rewrite the task neutrally and re-run **before** concluding |
| Both flat under neutral framing | Skill restates model defaults | Delete what the expert test fails |
| Skill scores lower | Micro-steps displaced a better plan | Cut steps; state outcome and tradeoffs |
| Gain only on the hard task | Content is discriminative | Keep it; consider moving it to `reference/` |
| Gain only on state-dependent tasks | Value is continuity, not method | Narrow the skill to state and safety rails |
| Behaviour drifts one way after deleting a "redundant" rule | It was counterbalancing another rule | Restore it as one line, or state the balance where both live |
| Loads on the near-miss | Description too broad | Tighten the trigger phrase, not the scenario list |

## Limits

- **A tie is evidence about the prompt until framing is neutral.** The first run of a new protocol has indicted a working skill and cleared a broken one.
- A model scoring its own output is weak evidence; prefer a separate scorer or a human spot-check.
- Never compare against a strawman baseline.
- An untested skill is reported as untested, never as passing.

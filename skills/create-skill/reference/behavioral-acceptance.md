# Behavioral Acceptance Test

Scope: prove the skill beats the bare model, not only the structural checks.

Used by **validate-skill-procedure** (check 21).

## When it runs

Run when both hold:

- the skill carries at least one judgment capability,
- representative tasks exist, supplied by the user or already in the repo.

Otherwise report `behavioral: not run` and the reason. A contractual-only skill is proven by its gates.

## Protocol

1. Take three tasks: one typical, one hard, one near-miss outside the trigger.
2. Freeze the rubric first per **evaluation-process**; never edit it after seeing output.
3. Run baseline: same model, same task, skill not loaded.
4. Run treatment: same model, same task, skill loaded.
5. Score both blind and in shuffled order; a separate scorer beats self-scoring.
6. Keep each element only where treatment scores higher. Flat or lower → decoration; delete or replace it.
7. Test the near-miss: the skill must not load, or must decline in one line.

## Record

| Task | Baseline | Skill | Δ | Kept / cut |
|---|---|---|---|---|

Report the table, the rubric, the model, and the run count. One run per task: report deltas, never statistical claims.

## Reading the result

| Symptom | Cause | Fix |
|---|---|---|
| Both flat | Skill restates model defaults | Delete what the expert test fails |
| Skill scores lower | Micro-steps displaced a better plan | Cut steps; state outcome and tradeoffs |
| Gain only on the hard task | Content is discriminative | Keep it; consider moving it to `reference/` |
| Loads on the near-miss | Description too broad | Tighten the trigger phrase, not the scenario list |

## Limits

- A model scoring its own output is weak evidence; prefer a separate scorer or a human spot-check.
- Never compare against a strawman baseline.
- An untested skill is reported as untested, never as passing.

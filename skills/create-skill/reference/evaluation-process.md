# Output Evaluation

Scope: every authored capability must let the agent check its own output.

## Requirement

Each capability ends with a validation or checklist step listing the criteria that prove
the output correct. Use whichever fits:

- A "Verify that <output> meets <criteria>" step.
- A pointer to a quality checklist: "Load **reference/quality-checklist.md** and apply each criterion."
- A dedicated validation capability with ordered checks.

A skill whose capabilities produce output with no check leaves correctness to agent discretion.

## Checklist

- [ ] Every capability that produces an artifact has a validation step or a loaded checklist.
- [ ] The criteria are falsifiable — a reader can tell pass from fail.
- [ ] At least one example demonstrates the validation step in action.

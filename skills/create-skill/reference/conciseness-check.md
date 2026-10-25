# Conciseness Check

Scope: authoring test for whether an element earns its place. The reviewer owns the
finding severities; this copy carries the test.

Apply **Occam's Razor**: every step, rule, sentence, and example must justify its existence.

## SKILL.md

- No verbose intro or context-setting that restates the section name — the XML tag already signals intent.
- No meta-commentary explaining why a step exists.
- Bullets or short phrases over full sentences where clarity allows.
- No repetition of content already in another section or a reference file.
- Edge cases and exhaustive detail belong in `reference/`, not inside a capability step.
- One well-written capability beats several split ones that add structure without value.
- **One line = one idea**: a line bundling 2+ items (joined by `;` or `and`, or several short facts) is line-stuffing even inside budget.

## Reference files

- Only the rubric, criteria, or data the capability needs — no surrounding narrative.
- Never paraphrase SKILL.md.

## Examples

- Minimum length that demonstrates the capability.
- No long input/output sections testing irrelevant edge cases.
- Scenario description = one or two sentences plus the essential input and output.

## Failing the test

| Pattern | Meaning |
|---|---|
| One verbose file | Tighten it |
| Several files, systematic verbosity | Token waste — cut it |
| Whole skill could lose >30% without losing meaning | Structural bloat — refactor |

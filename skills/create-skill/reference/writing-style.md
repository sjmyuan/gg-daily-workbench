# Skill-File Writing Style

Scope: how to write the prose this skill produces. The reviewer owns the finding
severities; this copy carries the rules and the caps.

## Directive voice

- SKILL.md is a procedure the agent executes — write commands, not descriptions.
- Every capability step starts with an action verb; no "the agent should…", no passive voice.
- Knowledge entries state facts directly.

## BLUF

- Open each section, knowledge entry, and rubric with the conclusion in one line, then the why.
- A capability objective is one line stating what the steps produce.
- Never lead with evidence, background, or motivation.

## Hard caps

| Element | Cap |
|---|---|
| Frontmatter description | ≤30 words, two-part (domain + "Use when…") |
| Capability objective | 1 sentence |
| Capability step | 1 imperative instruction, one clause |
| When-to-use bullet | 1 scenario, 1 intent verb |
| Rule | 1 sentence ("When X → use **capability**") |
| Knowledge bullet | 1 fact |
| Paragraph | ≤3 sentences |
| Sentence | ≤20 words, one clause |

- Each bullet = one claim, no justification; reasoning belongs in a table or the takeaway.
- Rubrics, criteria, and budgets are tables; prose only summarizes them.

## Banned

- "It is important to note that…" / "It should be noted that…"
- "In order to" → "To"
- "As mentioned above / earlier", "Please note"
- "The goal/purpose of this section is…" / "This section describes…"
- "This means that" / "What this means is"
- Meta-commentary, self-reference ("the above", "this step"), process narration ("I reviewed…").

## Per file type

- `SKILL.md` — `description` = domain summary + trigger phrase matching when-to-use; when-to-use bullets are user scenarios; knowledge holds noun-phrase subsections of facts; capabilities hold numbered imperative steps; rules are pure "when → capability" routing.
- `reference/` — title + rubric only; no narrative intro, no restatement of SKILL.md.
- `examples/` — scenario heading names the trigger and the distinguishing case; output shown as the capability would produce it; minimum length that demonstrates the capability.

## So-what test

Every sentence adds a fact or answers "So what?" — otherwise delete it. Run before presenting.

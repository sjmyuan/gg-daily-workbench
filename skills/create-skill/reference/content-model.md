# Content Model

Scope: what each piece of skill content **is**, decided before any section, naming, style, or size rule applies. Structure follows content; it never decides it.

Used by **classify-skill-content** (steps 2–5) and **create-skill-file** (steps 2–7).

## Four classes

| Class | Answers | Section | Recognise it by |
|---|---|---|---|
| **Fact** | What is true? | knowledge, or `reference/` when large | Holds without an actor: definitions, limits, paths, vocabularies, mappings, allowed values |
| **Procedure** | How is it done? | capability steps | Ordered actions that turn input into an artifact |
| **Judgment** | What does good look like? | knowledge, or `reference/` when large | Principles, tradeoffs, heuristics, exemplars, failure modes — guidance for a call the agent must make itself |
| **Routing + guard** | When does it run, and what is forbidden? | rules | Selects a capability or forbids an action; performs no action itself |

## Decision order

Apply in order; stop at the first yes.

1. Does it decide **which** capability runs, or **whether** an action is allowed? → rule.
2. Does it produce or transform something through **ordered steps**? → capability.
3. Does it guide a judgment call rather than fix an action? → judgment.
4. Otherwise → fact.

Tie-breaks:
- A rule containing a step: move the step to a capability; the rule keeps the trigger.
- A step that only forbids: hoist to a guard; keep it inline only when the step is meaningless without it.
- A fact read by one step and meaningless elsewhere: keep it inline at that step.
- A fact read by two or more steps, or loaded on demand: knowledge or `reference/`.
- A numbered list of facts: still facts — drop the numbering.

## Misclassification → repair

| Symptom | Real class | Repair |
|---|---|---|
| Knowledge subsection named with a verb | procedure | promote to a capability, or restate as facts |
| Capability steps listing limits or constraints | fact | move to knowledge; the step cites the limit by name |
| Capability steps forbidding an action | guard | move to rules |
| Rule describing how to do the work | procedure | keep the trigger, move the steps out |
| Prohibition buried mid-step | guard | hoist to rules |
| Same fact in knowledge and in a step | fact | one owner; the other names it |
| Template or schema living in a step | fact | one literal skeleton in `reference/`, routed from the step |
| Judgment written as imperative steps | judgment | restore the principle and its tradeoff; keep only decidable steps |

## Adequacy gates

`conciseness-check` only removes. These gates add, and are falsifiable.

| Class | Adequate when | Fails when |
|---|---|---|
| Fact | Every value the agent cannot infer is stated once: names, paths, limits, vocabularies, mappings | A step relies on a value the skill never states |
| Procedure | Each capability reaches its objective in ordered steps with decidable inputs | Objective exists with no step that produces it |
| Procedure | Each step names one action | A step says "handle it", "as appropriate", "etc." |
| Judgment | A reader can tell excellent from acceptable and knows which calls are their own | The skill states steps only, or names no tradeoff or failure mode |
| Routing + guard | One routing rule per capability | A capability no rule routes to |
| Routing + guard | One guard per known misapplication | A known wrong output is unguarded |

## Justification

Adequacy adds what is missing; justification deletes what earns nothing. Run justification after adequacy and before
conciseness: justification removes **elements**, conciseness shortens **wording**.

Nothing stays because it was in the source, because it sounds prudent, or because a reviewer might ask for it. An
element stays only when its removal breaks something nameable.

| Class | Challenge it | Removal must break | Delete when |
|---|---|---|---|
| Fact | Could the agent act correctly without being told this? | A step would use a wrong or invented value | The value is inferable, or the step restates it |
| Procedure | Does any output depend on these steps, in this order? | The objective is unreachable, or the order changes the result | The objective is reached without it |
| Judgment | Does output quality depend on this guidance? | The agent guesses a tradeoff or returns baseline output | The model already makes that call at the target quality |
| Routing + guard | Which capability would be missed, or which wrong output would come back? | A trigger becomes ambiguous, or a known misapplication returns | No capability becomes unreachable and no observed failure returns |

Ask both questions of every element; a "no" from either one is a deletion, not a rewrite.

- A guard needs a named failure it prevents — "be careful" guards fail the test.
- A step needs an output that disappears with it.
- A judgment entry needs a call the agent would otherwise get wrong.
- A fact needs a step that would otherwise guess.
- Structural scaffolding (a heading, a table) needs no justification; it is form, not content.

## Supporting files

The same test, one level up. A supporting file must break something when deleted, or it is an element the skill pays for and never spends.

| File | Challenge it | Removal must break | Delete when |
|---|---|---|---|
| Example | Which capability becomes unteachable without it? | A reader cannot see the output shape or the decision point | Another example already teaches that capability, or the output is mechanical |
| Reference | Why can this not sit in its owning step? | The step would carry the rubric inline and break **size-limits**, or criteria would never load | It fits its step within budget, or it restates SKILL.md |
| Script | What breaks if a CLI or one-liner runs instead? | A step cannot be executed deterministically at all | **script-and-cli-policy**'s four tests fail |

- A reference earns existence by size or load timing — never by tidiness.
- An example earns existence by teaching, not by illustrating.
- A script earns existence by necessity, not by convenience.
- Deleting a file also retires its guide row, its step route, and its `Applies` line.

## Run order

Classify → write each class in its section → adequacy gates → **justification** → conciseness → structure → style → size.

Content that survives no class is deleted, never placed.

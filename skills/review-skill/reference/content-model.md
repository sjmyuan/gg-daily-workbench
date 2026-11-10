# Content Model (review)

Scope: decide what each element **is** before judging where it sits. Structure never decides class.

Used by **review-skill-file** (step 1).

## Three classes

| Class | Answers | Section | Recognise it by |
|---|---|---|---|
| **Fact** | What is true? | knowledge | Holds without an actor: definitions, limits, paths, vocabularies, mappings |
| **Procedure** | How is it done? | capability steps | Ordered actions that turn input into an artifact |
| **Routing + guard** | When does it run, and what is forbidden? | rules | Selects a capability or forbids an action; performs no action itself |

## Decision order

1. Decides **which** capability runs, or **whether** an action is allowed → rule.
2. Produces or transforms something through **ordered steps** → capability.
3. Otherwise → fact.

## Findings

| Observation | Severity |
|---|---|
| A fact inside a step, also stated in knowledge or read by 2+ steps | 🔴 Major — two owners |
| A constraint list written as numbered steps | 🔴 Major — facts posing as a procedure |
| A procedure written as knowledge bullets or inside a rule body | 🔴 Major |
| A rule describing how to perform the work | 🔴 Major |
| A template or schema duplicated instead of one owner | 🔴 Major |
| A known misapplication with no guard rule | 🔴 Major |
| An objective that no step produces | 🟡 Minor |
| A step whose action is not decidable ("handle it", "as appropriate", "etc.") | 🟡 Minor |
| A step relying on a value the skill never states | 🟡 Minor |
| A capability with no routing rule | 🟡 Minor |
| Prohibition buried mid-step | 🟡 Minor — recommend hoisting to a guard |
| A claim qualifying as two classes | 🟡 Minor — report both, ask which owner |
| An element whose removal breaks no step, objective, or trigger | 🟡 Minor — recommend deletion, not rewording |
| A guard with no nameable failure it prevents | 🟡 Minor |

## Justification

| Class | Ask | Trace it to |
|---|---|---|
| Fact | Would a step guess without it? | the step that reads it |
| Procedure | Does an output depend on these steps, in this order? | the capability objective |
| Routing + guard | Which capability would be missed, or which failure returns? | the trigger, or an observed failure |

An element that no traced step, objective, or failure needs is a deletion finding — never a rewording finding.

## Supporting files

| File | Ask | Deletion finding when |
|---|---|---|
| Example | Which capability becomes unteachable without it? | Another example already teaches that case; the output is mechanical |
| Reference | Why can this not sit in its owning step? | It fits its step within size limits, or restates SKILL.md |
| Script | What breaks if a CLI or one-liner runs instead? | The four tests in **script-and-cli-policy** fail |

Deletion findings:

| Observation | Severity |
|---|---|
| An unjustified example, reference, or script | 🟡 Minor — recommend deletion plus its guide row, step route, and `Applies` line |
| A reference whose only justification is tidiness | 🟡 Minor |
| A script a CLI or one-liner could replace | 🟡 Minor (🔴 if it adds a dependency) |

## Repair order to recommend

Classify → one owner per claim → adequacy → justification → conciseness → structure → style → size.
Never recommend a structural fix for a misclassified claim.

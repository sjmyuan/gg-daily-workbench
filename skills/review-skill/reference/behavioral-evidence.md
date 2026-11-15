# Behavioral Evidence (review slice)

Scope: reviewing whether a skill was proven against the bare model. Owner: **behavioral-acceptance** in `create-skill`; this slice is the subset a review needs, and never diverges from it.

## What counts as evidence

| State | Severity |
|---|---|
| Judgment skill, no evidence claimed and none on record | 🟡 Minor |
| Evidence claimed, but no rubric, run count, or task framing recorded | 🟡 Minor |
| Flat delta left in place — "we tested it, it tied" | 🔴 Major |
| Skill scored lower than baseline and was kept | 🔴 Major |
| Contractual-only skill with no run | 🟢 Nit — its gates are the proof |

## A valid record shows

- The rubric, frozen before output was seen.
- Per task: baseline runs **n**, skill runs **n**, and the delta.
- The task text, quoted — enough to judge whether it named the behaviour under test.
- The near-miss result: did the skill decline, or fire?

- **The counterweight trap.** A rule that reads as restatement may balance another rule: "stop and ask" against "proceed autonomously". A skill edited by deleting such rules drifts to one pole — typically asking more and delivering less. When a review recommends a deletion, ask what the element was balancing before agreeing.

## The framing trap

A tie under a prompt that names the desired behaviour is evidence about the prompt, not the skill. Before accepting a flat result as a verdict, read the task text: if it says *"present it for confirmation"*, a competent model invents the structure unaided and the tie proves nothing.

Ask for one re-run with neutral wording before recommending a cut. Deleting a working skill on a framed test is the expensive failure here — it has happened.

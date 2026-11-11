# Empowerment Model

Scope: how much a skill should prescribe, and what it must carry to beat the bare model's baseline.

Used by **collect-skill-requirements** (step 2), **classify-skill-content**, **create-skill-file** (steps 3–6), and **validate-created-skill** (checks 19–20).

## Prescriptiveness dial

Set the regime per capability, not per skill. A skill usually carries both.

| Regime | Recognise it by | Skill carries |
|---|---|---|
| **Contractual** | Exact literals, order, schema, tool invocation, irreversible action | Ordered steps and guards; micro-steps are correct here |
| **Judgment** | Design, review, writing, analysis, planning, diagnosis | Outcome, constraints, quality bar, tradeoffs, failure modes, exemplars; the agent picks the path |

An unknown regime defaults to judgment: the agent can follow a thin procedure, but cannot invent taste.

## Expert test

Apply to every step before keeping it.

- Would a competent expert need this instruction? No → delete it.
- Yes → keep it, and state its reason once.
- Unclear → tighten the objective instead of keeping the step.

A capability is micromanaged when a capable model would reproduce its steps without the skill.
Micromanagement costs context, anchors the agent to a mediocre plan, and blocks a better approach.

## Judgment content

Judgment is a class in **content-model**. A judgment capability states:

- the outcome and how an observer confirms it,
- the constraints that make the work non-arbitrary,
- the tradeoffs the agent must call, and which side to prefer,
- the failure modes: what plausible-but-wrong output looks like,
- one exemplar of excellent output, inline or routed to `examples/`.

Adequacy: a reader can tell excellent from acceptable, and knows which calls are their own.

## Rationale budget

- Give one reason per non-obvious constraint; reasons are how a model generalizes.
- Omit the reason only when the boundary is self-evident or safety-critical.
- The owner is the knowledge entry or reference holding the constraint, never each step.
- A reason is not narration: no process commentary, no restatement of the section.

## Delegation boundary

A capability that hands work to the agent states three lists.

| List | Holds |
|---|---|
| May decide | Path, order, tooling, depth — reversible choices |
| Must decide | The judgment calls the skill exists to delegate |
| Must not decide | Irreversible actions, exact literals, scope changes — stop and ask |

## Growth

- Exemplars, failure modes, domain facts, and tradeoffs beat baseline output and need no retirement.
- Structural content — sections, rules, steps, files — still funds itself per **edit-skill-procedure**.
- Cut first where the model already performs at the target quality.

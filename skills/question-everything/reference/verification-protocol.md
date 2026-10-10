# Verification Protocol

Use with **verify-sub-agent-results** (the verification loop).

## Independence rules

- Always dispatch a NEW agent — never the original instance. Applies to both the verification dispatch and the re-investigation dispatch.
- **Match the verifier to the evidence that settles the challenge**, not to the producing agent (see Verifier selection).
- The verifier treats the original result as unverified and must answer from primary sources (code, docs, data, logs).
- Never show the verifier a pre-written "expected verdict" — only the claims and the challenges.
- If no suitable verifier agent is available, verify directly against primary sources in the current session.

## Verifier selection

Route each challenge to the agent that can read the evidence that would settle it:

| Evidence that settles the challenge | Verifier |
|---|---|
| Code / current-state behavior (source, symbols, `file:line`) | `code-investigator` (or the platform's closest code-reading agent) |
| Non-code (research comparables, decision reasoning, document structure/format) | A NEW agent of the same type as the producer |

- **Per challenge, not per result** — one result's challenges may split across verifiers.
- **Documents are not evidence** — a producer-type agent re-reading its own doc type cannot verify code claims; route those to `code-investigator`.
- **Structure and format** stay with the owning skill's checklist, not the evidence loop.
- **Greenfield** — no code exists, so the verification evidence is non-code and the producer's type applies.

## Brief template

```markdown
## Context
<the original result and its key claims>

## Challenges to verify
1. <challenge>: <claim> — <dimension> — <why suspect>

## Task
Verify each challenge against primary sources. Do not assume the original result is correct.
Read-only task — do not write or modify any files.
Return a per-challenge verdict, each citing its primary source (file:line, doc, or log):
- **AGREE** — claim holds, with the supporting source
- **DISAGREE** — claim is wrong, with the corrected claim and its source
- **UNCERTAIN** — cannot determine from available sources; state what is missing
```

## Comparison rules

- All material verdicts **AGREE** → accept the result; report agreed claims and residual uncertainty.
- Any material verdict **DISAGREE** or **UNCERTAIN** → dispatch a new evidence-matched agent to redo the affected work (below), then re-enter **question-the-result** on the new result.
- Round cap: **3 rounds**. At the cap, stop and present both versions (original vs. verified) to the user for a decision — never silently pick one.
- Dispatch verification only for material (high/medium-priority) challenges; low-priority ones are noted, not verified.

## Re-investigation loop

- Dispatch a NEW evidence-matched agent — `code-investigator` to re-investigate a wrong code fact; the producer's type to recompile a document — never the original instance.
- The brief carries: the challenged claims, each DISAGREE/UNCERTAIN verdict with its cited source and evidence, and the corrected understanding.
- The agent redoes the affected work from scratch and must address every divergence — not rubber-stamp the earlier result.
- The new result is then questioned again and re-verified by another new evidence-matched agent in the next round.

## Traps

- Verifying the whole result instead of per-challenge — a wholesale "looks fine" is not a verdict
- Reusing the original agent instance in verification or re-investigation — it will defend or anchor on its own output; always dispatch a new agent
- Verifying code claims with the producer's type — a findings/ADR/solution-doc agent cannot read code; route code challenges to `code-investigator`
- Sending only the verdict back in re-investigation — the agent needs the verifier's evidence and corrected understanding to redo its investigation
- Treating "same wording" as agreement — compare substance and evidence, not phrasing
- Verifying low-priority challenges — dispatch only material (high/medium) challenges; low-priority ones are noted, not verified
- Accepting verdicts without a cited source — each AGREE/DISAGREE must name the primary source that supports it
- Infinite loops — always honor the round cap

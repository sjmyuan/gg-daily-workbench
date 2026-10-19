# Verification Protocol

Use with **verify-sub-agent-results** (the verification loop).

## Independence rules

- Always dispatch a NEW agent — never the original instance. Applies to both the verification dispatch and the re-investigation dispatch.
- **Match the verifier to the evidence that settles the challenge**, not to the producing agent (see Verifier selection).
- The verifier treats the original result as unverified and must answer from primary sources (code, docs, data, logs).
- Never show the verifier a pre-written "expected verdict" — only the claims and the challenges.
- If no suitable verifier agent is available, verify directly against primary sources in the current session.

## Verification depth

Scale depth to the **blast radius of the claim**, not the number of artifacts. Verify once at the source; never re-verify a synthesis of already-verified material.

| Tier | Applies to | Action |
|---|---|---|
| **Skip** | Structure, format, wording; a doc that only restates a verified ledger | Owning-skill checklist only — no verifier dispatch |
| **Fidelity** | Findings/solution synthesis over a verified ledger | Check IDs, counts, and cross-references against the ledger; no fresh evidence sweep; any new `file:line` claim drops to **Single pass** |
| **Single pass** | New evidence, code facts, investigation results | One independent verifier round — the default |
| **Full loop** | Load-bearing ADR decision, irreversible or high-cost outcome, conflicting evidence, or user request | Verify → repair once → scoped confirm (cap 2) |

- Default to **Single pass**; **Full loop** is opt-in by the criteria above.
- A `DISAGREE` gets one repair by a new evidence-matched agent; confirm only the changed claims, never the settled ones.
- `UNCERTAIN` is a valid outcome: tag the claim **unverified** in the evidence doc and surface it to the user — do not loop for convergence.
- Verify only **material** claims, capped at the top 3 by impact; each challenge needs a falsifiable primary-source test. Note low-priority challenges without verifying them.

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

## Known context in the brief

Carry every established fact with the brief so the verifier starts from the producer's evidence, not from zero.

| Carry | Source | Mode |
|---|---|---|
| Evidence map: established `file:line` and **Verified** claims | findings doc / producer output | Path, else inline |
| Open claims: **Inferred** / **Assumption** / **Gap** — the failure points | same | Inline |
| Searched-negatives: scans already done | same | Path, else inline |
| Scope slice: goal, area boundaries, the decision the result feeds | scope map / user dialog | Inline |
| Producer's citation behind each challenge | the result | Inline |

- Load by **path** when an artifact holds the info; **inline** otherwise — never leave a field empty.
- Carry context for every brief, even a single mechanical challenge — the cost is far below a full re-scan.
- Independence holds: carry claims and citations, never a pre-written expected verdict.
- The context is non-exhaustive — the verifier starts from these locations but may go beyond them.
- A round-2+ brief also carries the prior round's verdicts and any evidence the earlier verifier added.

## Brief template

```markdown
## Context
<the original result and its key claims>

## Known context
- Established evidence (path/inline): <findings doc / evidence map> — its `file:line` locations and **Verified** claims; settled, do not re-scan.
- Open claims (inline): <the Inferred / Assumption / Gap claims — the likely failure points>.
- Searched-negatives (path/inline): <scans already done — do not repeat>.
- Scope slice (inline): <goal + area boundaries + the decision the result feeds>.
- First pass, no artifact yet: carry the producer's inline citations instead.

## Challenges to verify
1. <challenge>: <claim> — <dimension> — <why suspect> — producer's citation: <file:line / doc>

## Task
Verify each challenge against primary sources. Do not assume the original result is correct.
Start from the cited locations; go beyond them when the evidence requires it.
Re-open a settled claim only when a challenge touches it.
Read-only task — do not write or modify any files.
Return a per-challenge verdict, each citing its primary source (file:line, doc, or log):
- **AGREE** — claim holds, with the supporting source
- **DISAGREE** — claim is wrong, with the corrected claim and its source
- **UNCERTAIN** — cannot determine from available sources; state what is missing
```

## Comparison rules

- All material verdicts **AGREE** → accept the result; report agreed claims and residual uncertainty.
- Any material verdict **DISAGREE** → dispatch a new evidence-matched agent to repair the affected work (below), then confirm only the changed claims.
- Any material verdict **UNCERTAIN** → tag the claim **unverified**, record what is missing, and surface it; no further round.
- Round cap: **2 rounds** — independent verify, then a scoped confirm after one repair. At the cap, present both versions (original vs. verified) to the user — never silently pick one.
- Dispatch verification only for material (high/medium-priority) challenges; low-priority ones are noted, not verified.

## Repair loop

- Dispatch a NEW evidence-matched agent — `code-investigator` to re-investigate a wrong code fact; the producer's type to recompile a document — never the original instance.
- The brief carries: the challenged claims, each DISAGREE verdict with its cited source and evidence, and the corrected understanding.
- The agent redoes only the affected work and must address every divergence — not rubber-stamp the earlier result.
- The repaired result is questioned again; another new evidence-matched verifier confirms **only the changed claims**. Settled claims are not re-verified.

## Traps

- Verifying the whole result instead of per-challenge — a wholesale "looks fine" is not a verdict
- Dispatching the verifier blind — omitting established `file:line` locations forces a full re-scan; carry the known context
- Handing over "these are verified" with no settled-vs-open split — name the open Inferred/Assumption/Gap claims so the verifier targets them
- Treating handed-over locations as exhaustive — the verifier must be free to go beyond them
- Reusing the original agent instance in verification or re-investigation — it will defend or anchor on its own output; always dispatch a new agent
- Verifying code claims with the producer's type — a findings/ADR/solution-doc agent cannot read code; route code challenges to `code-investigator`
- Sending only the verdict back in re-investigation — the agent needs the verifier's evidence and corrected understanding to redo its investigation
- Treating "same wording" as agreement — compare substance and evidence, not phrasing
- Verifying low-priority challenges — dispatch only material (high/medium) challenges; low-priority ones are noted, not verified
- Re-verifying a synthesis doc — a findings/solution doc built from a verified ledger needs a fidelity check, not an evidence sweep
- Chasing `UNCERTAIN` with another round — tag it **unverified** and surface it instead
- Accepting verdicts without a cited source — each AGREE/DISAGREE must name the primary source that supports it
- Infinite loops — always honor the 2-round cap

# Investigation Brief

Ready-to-fill structured brief for `investigate-per-area` → `code-investigator` — loaded on demand when dispatching an area's investigation. Fills the **structured brief shape**; carries the shared known-context + evidence-map contracts: **reference/dispatch-briefs.md**.

**Announce**: "Dispatching investigation of [N] area(s) to a sub-agent."

Fill one brief per area:

## 1. Mission
You are the `code-investigator`. Deliver: current-state findings plus a per-area evidence map for **[area]**.

## 2. Context
- Spike goal **(path)**: `scope.md`
- Area: **[name]** — **[description]**
- Problems this area must inform **(path)**: `scope.md` — this area's "How to …?" rows
- Boundaries **(inline)**: **[modules/files/teams inside; what is out of scope — name the sibling areas]**
- User-stated context **(inline)**: **[constraints, facts, and domain details the user already gave]**
- Mode: **brownfield** (trace code) | **greenfield** (research approaches + comparable systems; see **greenfield-scenarios**)

## 3. Inputs
- Findings pair **(path)**: **[`docs/findings-<area>.md`] + [`docs/evidence-<area>.md`]** — the human doc orients (resource index, diagrams, TL;DRs); the evidence doc carries the claim ledger. Start from its **Verified** claims; dig only **Gap** / **Inconsistency** / **Inferred** / **Assumption** claims. First pass (no pair yet): build the map from scratch.
- Pre-existing user findings **(inline)**: **[the notes/findings the user supplied]** — treat as already known; verify only what it leaves unresolved.
- Sibling findings pairs **(path)**: **[paths]** — cross-area constraints this area must respect.
- Open verification challenges **(re-dispatch only, inline)**: **[challenged claims, verdicts, what the verifier disputed]** — resolve each; leave everything else settled.

## 4. Tasks
1. Apply `investigate-code` to the area — **[entry points / open questions]**.
2. Trace call chains to `file:line` precision.
3. Record an evidence-ledger verdict per claim (**Verified** / **Inferred** / **Assumption** / **Inconsistency** / **Gap**).
4. Record searched-negatives so downstream agents do not re-scan.

## 5. Output contract
- Narrative findings: current state, constraints, gaps (per `investigate-code` report format).
- Evidence map: entry points, key `file:line` locations, call chains, evidence ledger, searched-negatives (per **reference/findings-document-guide.md**).

## 6. Constraints
- Never modify code, artifacts, or any file — return findings only.
- Never create or modify files through any tool, including shell commands.
- Never re-verify a claim the evidence doc marks **Verified**.
- Never assert a fact without a `file:line` or a recorded searched-negative.

## 7. Report back
- Flag every **Gap** / **Inconsistency** the evidence doc does not already record.
- Flag anything that contradicts another area, for cross-area synthesis.

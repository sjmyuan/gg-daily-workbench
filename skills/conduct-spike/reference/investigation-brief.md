# Investigation Brief

Ready-to-fill structured brief for `investigate-per-area` → `code-investigator` — loaded on demand when dispatching an area's investigation. Fills the **structured brief shape**; carries the shared context-inventory, fill-mode, intake-record, and evidence-map contracts: **reference/dispatch-briefs.md**.

**Announce**: "Dispatching investigation of [N] area(s) to a sub-agent."

Fill one brief per area. Every path is absolute.

## 1. Mission
You are the `code-investigator`. Deliver: current-state findings plus a per-area evidence map for **[area]**.

## 2. Context
- Spike goal **(path + digest)**: `<artifact-root>/spikes/<spike-name>/scope.md` — **[1–3 lines: the question to settle and what completion looks like]**
- Area: **[name]** — **[description]**
- Problems this area must inform **(path)**: `scope.md` — this area's "How to …?" rows
- Boundaries **(inline)**: **[modules/files/teams inside; what is out of scope — name the sibling areas]**
- Accepted assumptions **(digest, from `scope.md#accepted-assumptions`)**: **[A<N> → assumed value]** — treat as true unless the code contradicts them
- User-stated context **(inline)**: **[constraints, facts, decisions, and domain details the user already gave]**
- Mode: **brownfield** (trace code) | **greenfield** (research approaches + comparable systems; see **greenfield-scenarios**)

## 3. Inputs
- Intake record **(inline)**: system **[...]** · scope **[...]** · depth **[...]** · consumer **[...]** — the gate is already passed; adopt it, do not re-derive it.
- Known locations **(digest)**: **[symbols / files / entry points / `file:line` the orchestrator already located]** — start here; do not re-discover them.
- Already searched **(digest)**: **[query + root + outcome, including "no matches"]** — do not repeat any listed search.
- Findings pair **(path)**: **[`docs/findings-<area>.md`] + [`docs/evidence-<area>.md`]** — the human doc orients (resource index, diagrams, TL;DRs); the evidence doc carries the claim ledger. Start from its **Verified** claims; dig only **Gap** / **Inconsistency** / **Inferred** / **Assumption** claims. First pass (no pair yet): build the map from scratch.
- Sibling unit results **(inline, unpersisted)**: **[area → verified evidence map or constraint]** — inherit these; never re-scan code a sibling already covered.
- Pre-existing user findings **(inline)**: **[the notes/findings the user supplied]** — treat as known; verify only what they leave unresolved.
- Sibling findings pairs **(path)**: **[paths]** — cross-area constraints this area must respect.
- Open verification challenges **(re-dispatch only, inline)**: **[challenged claims, verdicts, what the verifier disputed]** — resolve each; leave everything else settled.

## 4. Tasks
1. Apply `investigate-code` to the area — **[entry points / open questions]**.
2. Start from the known locations and skip the already-searched queries; explore only what they leave open.
3. Trace call chains to `file:line` precision.
4. Record an evidence-ledger verdict per claim (**Verified** / **Inferred** / **Assumption** / **Inconsistency** / **Gap**).
5. Record searched-negatives so downstream agents do not re-scan.

## 5. Output contract
- Narrative findings: current state, constraints, gaps (per `investigate-code` report format).
- Evidence map: entry points, key `file:line` locations, call chains, evidence ledger, searched-negatives (per **reference/findings-document-guide.md**).
- Search log: every query run and its outcome, so the next unit inherits it.

## 6. Constraints
- Never modify code, artifacts, or any file — return findings only, through no tool including shell commands.
- Never re-derive scope, re-ask, or search for your inputs — this brief is the gate result and holds the paths.
- Never re-scan a listed known location or repeat a listed search.
- Never re-verify a claim the evidence doc marks **Verified**.
- Never assert a fact without a `file:line` or a recorded searched-negative.

## 7. Report back
- Flag every **Gap** / **Inconsistency** the evidence doc does not already record.
- Flag anything that contradicts another area, for cross-area synthesis.
- Return the search log so the orchestrator can seed the next unit with it.

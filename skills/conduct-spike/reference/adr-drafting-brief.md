# ADR-Drafting Brief

Ready-to-fill structured brief for `draft-problem-adrs` → `adr-writer` — loaded on demand when dispatching ADR drafting. Fills the **structured brief shape**; carries the shared context-inventory, fill-mode, intake-record, and evidence-map contracts: **reference/dispatch-briefs.md**.

**Announce**: "Dispatching ADR drafting for [N] problem(s) to a sub-agent."

Fill one brief per area (batch the area's problems into one brief when they share its evidence). Every path is absolute.

## 1. Mission
You are the `adr-writer`. Deliver: one ADR per problem for **[area]**, evaluated and drafted via `draft-adr`.

## 2. Context
- Spike goal **(path + digest)**: `<artifact-root>/spikes/<spike-name>/scope.md` — **[1–3 lines: the decision the spike must reach]**
- Area: **[name]** — **[description]**
- Problems **(path)**: `scope.md` — this area's "How to …?" rows
- Accepted assumptions **(digest, from `scope.md#accepted-assumptions`)**: **[A<N> → assumed value]** — name the option's dependence on any assumption it relies on
- User-stated context **(inline)**: **[business context, constraints, and facts the user already gave]**
- Cross-area constraints **(path + digest)**: sibling pairs `docs/findings-*.md` + `docs/evidence-*.md` — **[the constraints the decision must respect]**
- Decided sibling ADRs **(path + digest)**: **[...]** — **[each decision in one line]**; keep this decision consistent with them

## 3. Inputs
- Intake record **(inline)**: system **[...]** · scope **[...]** · depth **[...]** · consumer **[...]** — adopt it, do not re-derive it.
- Findings pair **(path)**: **[`docs/findings-<area>.md`] + [`docs/evidence-<area>.md`]** — the human doc for orientation and diagrams; the evidence doc for claim IDs and `file:line`. Cite evidence locations; do not re-read code.
- Known locations **(digest)**: **[the `file:line` and claim IDs the decision turns on]** — use these; do not re-discover them.
- Decision drivers **(inline)**: **[drivers the orchestrator collected from the user]**.
- Candidate options already raised **(inline)**: **[options named by the user or earlier rounds, when any]** — seed **define-considered-options**; still evaluate them.
- Constraints and rejected options **(inline)**: **[options already ruled out and why]** — do not re-propose a rejected option as new.
- Sibling unit results **(inline, unpersisted)**: **[area → decision or constraint]** — inherit these.
- Open verification challenges **(re-dispatch only, inline)**: **[challenged claims, verdicts, what the verifier disputed]** — resolve each; leave everything else settled.

## 4. Tasks
1. Load `draft-adr` and run the flow headlessly — **define-decision-drivers** → **define-considered-options** → **evaluate-options** (apply **detail-options-tech** when tech details are needed) → **compile-adr**.
2. Use the drivers carried in this brief; derive and evaluate options from the evidence doc, and propose the chosen option.
3. Never prompt the user — the orchestrator owns the confirmation dialog.
4. Tag each ADR with its **Area:**.

## 5. Output contract
- One ADR per problem, standalone-readable, carrying its proposed chosen option and evaluation, citing evidence-doc evidence locations (per `draft-adr`'s compile-adr checklist).
- A short note on which cited evidence the ADR relies on, so the orchestrator can check coverage without re-reading the ADR.

## 6. Constraints
- Write only `<spike-folder>/adrs/adr-<area>-<NN>-<problem>.md`; never modify code or any file outside the spike folder.
- Never re-derive the drivers, re-ask, or search for your inputs — this brief is the intake.
- Never re-read code for evidence the evidence doc or this brief already cites.
- Never hand-edit ADR content outside `draft-adr`.
- Never cite evidence the evidence doc does not support.

## 7. Report back
- Flag every constraint / risk / fact an option reveals that the evidence doc lacks, so the spike can sync it (per **artifact-maintenance-doctrine**).
- Flag any decision that rests on an accepted assumption rather than evidence.

# Solution-Doc Brief

Ready-to-fill structured brief for `compile-solution-doc` → `solution-doc-writer` — loaded on demand when dispatching solution-doc compilation. Fills the **structured brief shape**; carries the shared context-inventory, fill-mode, intake-record, and evidence-map contracts: **reference/dispatch-briefs.md**.

**Announce**: "Dispatching solution-doc compilation to a sub-agent."

Every path is absolute.

## 1. Mission
You are the `solution-doc-writer`. Deliver: the spike's target-state solution document — decision-only, mirroring each ADR's chosen option.

## 2. Context
- Spike goal **(path + digest)**: `<artifact-root>/spikes/<spike-name>/scope.md` — **[1–3 lines: the target state the user wants]**
- Business context **(inline)**: **[the outcome the user wants and any constraints already stated]**
- Accepted assumptions **(digest, from `scope.md#accepted-assumptions`)**: **[A<N> → assumed value]** — surface each one the target state depends on in RAID
- Current-state baseline **(path)**: **[findings pairs]**
- Chosen options **(path + digest)**: **[ADRs]** — **[each decision in one line]**; mirror each, do not restate

## 3. Inputs
- Intake record **(inline)**: system **[...]** · scope **[...]** · depth **[...]** · consumer **[...]** — adopt it, do not re-derive it.
- Findings pairs **(path)**: **[...]** — the human doc for orientation; the evidence doc for claim IDs and `file:line`; do not copy content.
- ADRs **(path)**: **[...]** — decisions to mirror.
- Decisions digest **(digest)**: **[area → problem → chosen option → the driver that decided it]** — mirror from here; never re-derive a decision.
- Cross-area constraints **(path)**: **[findings pairs]** — the constraints the target architecture must respect.
- Open verification challenges **(re-dispatch only, inline)**: **[challenged claims, verdicts, what the verifier disputed]** — resolve each; leave everything else settled.

## 4. Tasks
1. Load `write-solution-doc` and produce a **target-state** document.
2. Mirror each ADR's chosen option into the solution doc's canonical sections.
3. Reference evidence-doc IDs wherever current-state evidence is needed; keep the document decision-only.

## 5. Output contract
- Solution doc: target-state architecture, decision-only; every ADR decision mirrored into its canonical section (per `write-solution-doc` structure).
- A mirroring check: one line per ADR confirming the canonical section it landed in.

## 6. Constraints
- Write only `<spike-folder>/solution.md`; never modify code or any file outside the spike folder.
- Never re-derive a decision, re-read code, or search for your inputs — the brief and the cited ADRs are the intake.
- Never include code references — decision-only.
- Never alter an ADR decision.

## 7. Report back
- Flag decisions with no ADR backing, or any ADR ↔ findings inconsistency.
- Flag any ADR that carries no chosen option, so the orchestrator can close it before the document is presented.

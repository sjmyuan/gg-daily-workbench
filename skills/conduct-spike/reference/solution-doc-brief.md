# Solution-Doc Brief

Ready-to-fill structured brief for `compile-solution-doc` → `solution-doc-writer` — loaded on demand when dispatching solution-doc compilation. Fills the **structured brief shape**; shared known-context + evidence-map contracts: **reference/dispatch-briefs.md**.

**Announce**: "Dispatching solution-doc compilation to a sub-agent."

## 1. Mission
You are the `solution-doc-writer`. Deliver: the spike's target-state solution document — decision-only, mirroring each ADR's chosen option.

## 2. Context
- Spike goal **(path)**: `scope.md`
- Business context **(inline)**: **[the outcome the user wants and any constraints already stated]**
- Current-state baseline **(path)**: **[findings docs]**
- Chosen options **(path)**: **[ADRs]** — mirror each; do not restate here

## 3. Inputs
- Findings docs **(path)**: **[...]** — current-state evidence to reference; do not copy its content.
- ADRs **(path)**: **[...]** — decisions to mirror.
- Cross-area constraints **(path)**: **[findings docs]** — the constraints the target architecture must respect.
- Open verification challenges **(re-dispatch only, inline)**: **[challenged claims, verdicts, what the verifier disputed]** — resolve each; leave everything else settled.

## 4. Tasks
1. Load `write-solution-doc` and produce a **target-state** document.
2. Mirror each ADR's chosen option, grouped by area.
3. Reference findings-doc IDs wherever current-state evidence is needed; keep the document decision-only.

## 5. Output contract
- Solution doc: target-state architecture, decision-only, ADR decisions grouped by area (per `write-solution-doc` structure).

## 6. Constraints
- Write only `<spike-folder>/solution.md`; never modify code or any file outside the spike folder.
- Never include code references — decision-only.
- Never alter an ADR decision.

## 7. Report back
- Flag decisions with no ADR backing, or any ADR ↔ findings inconsistency.

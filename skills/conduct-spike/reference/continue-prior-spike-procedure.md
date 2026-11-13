# Continue-Prior-Spike Procedure

Full procedure for the `continue-prior-spike` capability — loaded on demand when a prior spike is resumed. Model and statuses: **reference/scope-map-guide.md**.

1. Load the prior spike's artifacts — scope summary, findings doc pairs, ADRs, solution doc; ask the user to share or summarize them when any are unavailable.
2. Gate the continuation delta per **scope-acceptance-gate** — restate what is added, adjusted, or removed, show every inference, and ask before recording it; then read statuses to surface open problems (`investigating`/`deciding` per **scope-map**).
3. Confirm which areas and problems to add, adjust, or remove; map each delta to its affected ADR(s) and solution section.
4. Validate changed problems are independently decidable and unchanged decisions are preserved; rewrite the accepted request and the scope map in place — no dated or per-round section — and re-derive the assumption set: prune every line that is settled, verified, or moves no row, and rewrite a changed line under its existing ID.
5. Run the standard workflow in revise-in-place mode: apply **dispatch-area-session** (seeded with the existing pairs, returning each updated pair and ADRs), **compile-findings-doc**, **confirm-problem-adrs**, then **sync-update-artifacts**.
6. Update each affected problem's stored status in `scope.md` when its artifact saves; area status recomputes from them.
7. Run the **final consistency review** — cross-check findings → ADRs → solution doc and cross-area constraints; surface inconsistencies before concluding.
8. **Focused rework**: a delivery-time rework that reopens a decision is a continuation — reuse the prior evidence maps, investigate only the delta, and update only the affected ADR and solution section; still update that area's findings pair (revise the affected topic, add a topic for a newly answered question).
9. Ask whether to continue with another round or conclude; never conclude while the final consistency review reports an inconsistency.

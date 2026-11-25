# Diagram Contract

Used by **define-problem**, **detail-options-tech**, **compile-adr**, and **sync-diagrams**.
A diagram earns its place by what it carries, not by how few nodes it has. Mechanics come from `draw-mermaid-diagrams`; content comes from this contract.

## What every diagram must carry

| Element | Must state | Example | Missing means |
|---|---|---|---|
| Node | name, technology, responsibility | `Bank Transfer Service — Spring Boot — executes transfers` | Reader cannot tell what runs where |
| Edge | verb, protocol, sync/async, direction | `Payment → BankTransfer: POST /transfer, sync, p99 200 ms` | Coupling and latency invisible |
| Data store | engine and owning service | `Payment DB — PostgreSQL — owned by payment` | Persistence decision invisible |
| Delta | `NEW` / `CHANGED` / `REMOVED` against current state | `Wallet Service [CHANGED]` | Reader cannot see what the option does |
| Quantity | the number behind every quantitative driver | `~10K orders/day`, `€380/month` | Options look equally good |
| Failure | the failure or timeout this option **introduces** — `none new` when it introduces none | `timeout 3 s → retry once → dead-letter` | Trade-off hidden |

## Per-view requirements

- **C4 context**: actors, in-scope systems, external systems, volumes on the relationships.
- **C4 container / component**: technology per container, protocol per relationship, every data store, and the delta marks.
- **Sequence**: happy path plus the failure path this option adds, or `none new` when it adds none; label new hops `(new)`; show the compensation or rollback message.
- **Flowchart**: decision nodes carry the condition and its threshold, never bare "yes / no".

## Anti-patterns — drop the diagram instead

- A diagram that only re-encodes a list or table already in the ADR: a driver list, a comparison matrix, an option list, or an elimination tree whose edges restate matrix rows.
- Edges with no label, or labelled only "calls".
- A change ADR whose target-state diagram shows no delta from the current state.
- Two questions in one diagram: split by view, never by removing labels.

## Validation

Run before presenting, and again after every sync:

1. Every node names technology and responsibility.
2. Every edge names verb, protocol, and sync/async.
3. Every node is marked NEW / CHANGED / REMOVED, or belongs to the unchanged baseline.
4. Every changed runtime flow shows the failure path the option introduces, or states `none new`.
5. The diagram answers a question its surrounding table cannot.
6. Every Mermaid block validates with 0 errors via `draw-mermaid-diagrams`.

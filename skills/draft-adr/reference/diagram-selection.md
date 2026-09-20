# Diagram Selection

Used by: **define-problem**, **define-decision-drivers**, **evaluate-options**, **compile-adr**, **sync-diagrams**.

Draw diagrams proactively whenever explaining context or a solution — never wait to be asked. Choose the diagram type by the context to explain, not by the ADR step. Draw all diagrams with Mermaid.

| Diagram | Draw when explaining | Shows |
|---|---|---|
| C4 context diagram | The overall system landscape — who or what interacts with the system(s) in scope | Systems in scope, actors, external dependencies |
| C4 container diagram | Zooming into a system — the high-level applications and data stores that compose it | Containers, technology choices, container relationships |
| C4 component diagram | Zooming into a single container — the components inside it and how they interact | Components, responsibilities, component relationships |
| Flowchart | A step-by-step process or flow | Flow steps, decision branches |
| Sequence diagram | The order and timing of interactions between components | Lifelines, message sequence, sync/async calls |
| Decision driver map | The trade-off space that drives the decision | Hard constraints vs soft preferences |
| Option comparison matrix + elimination tree | How options compare against the drivers, or why options were dropped | Driver satisfaction per option, elimination reasoning |

Zoom in level by level: C4 context → container → component for structure, then a flowchart or sequence diagram for a specific flow or interaction. The solution architecture is a C4/flowchart view of the target state — no separate diagram type is required. Draw C4 diagrams with Mermaid's native `C4Context`, `C4Container`, and `C4Component` types using C4-PlantUML-compatible syntax (`Person`, `System`, `System_Ext`, `Container`, `ContainerDb`, `Component`, `Rel`, `System_Boundary`, `Container_Boundary`). Keep each diagram to a single message; its caption is the takeaway — never add prose that restates it. Prefer a diagram when it conveys the relationship or flow in less reading time than the prose it replaces; otherwise one sentence beats a sprawling diagram. Notation and snippets: **diagram-guide.md**.

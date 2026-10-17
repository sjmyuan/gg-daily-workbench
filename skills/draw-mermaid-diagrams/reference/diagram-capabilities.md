# Diagram Capabilities

Used by **author-mermaid-diagram** to apply the right contract to a named type.

## What each type shows

| Type | Shows | Constraints |
|---|---|---|
| `C4Context` | Actors, systems in scope, external dependencies | One level: systems only |
| `C4Container` | Apps, services, stores inside one system | One level; one boundary |
| `C4Component` | Components inside one container | One level; one boundary |
| `sequenceDiagram` | Lifelines, message order, sync vs async | One zoom level |
| `flowchart` | Steps, decisions, labeled branches | Stadium terminals on process flows |
| `stateDiagram-v2` | States and trigger-labeled transitions | Trigger-labeled transitions |
| `classDiagram` | Types, members, inheritance, composition | Relationships labeled with the role |
| `erDiagram` | Entities, attributes, keys, cardinality | Keys marked; cardinality labeled |

## Scope boundaries

- Type choice, focus, and splitting are out of scope.
- This reference states what each type can express; it never picks or prunes a diagram.

## C4 levels

C1 context → C2 containers → C3 components. One level per diagram. Element and boundary rules live in **c4-syntax.md**.

## Normalizing supplied diagrams

| Supplied as | Normalize to |
|---|---|
| PlantUML-style or mixed C4 element/boundary styles | Native `C4Context` / `C4Container` / `C4Component` |
| Numbered sequence messages | Keep the numbering and note the scheme |
| `graph TD` | `flowchart` |
| `stateDiagram` | `stateDiagram-v2` |

- Preserve every message, relationship, and node — normalization never drops semantics.
- Reject a supplied diagram whose type cannot express its message; ask for the missing context instead of forcing it.

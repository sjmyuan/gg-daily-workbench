# Example: Scope-Map Status Lifecycle Through a Spike

**Scenario**: A single-area spike ("How to replace the session store?") runs from scope definition to completion. This example shows how the stored problem statuses move as each capability saves its artifact, and how new evidence reopens a `done` problem.

**Applies**: **scope-map** (knowledge convention) — updated by **compile-findings-doc**, **confirm-problem-adrs**, and **sync-update-artifacts**

**What makes this distinct**: Other examples show artifact content; this one shows only the `scope.md` status view as it evolves — the stored problem statuses and the area status derived from them.

---

## Point 1 — After define-spike-scope

Goal: replace the in-process session store with a shared, scalable store.
Problems `investigating` (no ADR); the derived area status is `preparing` (no findings pair).

```markdown
## Area: Session storage
**Findings**: —
- `investigating` How to choose the session store? → (no ADR)
- `investigating` How to migrate existing sessions? → (no ADR)
```

## Point 2 — After compile-findings-doc

Findings pair saved → the derived area status becomes `spiking`. Problems still `investigating` (no ADR).

```markdown
## Area: Session storage
**Findings**: docs/findings-session-storage.md + docs/evidence-session-storage.md
- `investigating` How to choose the session store? → (no ADR)
- `investigating` How to migrate existing sessions? → (no ADR)
```

## Point 3 — After confirm-problem-adrs (awaiting confirmation)

Each ADR saved → its problem `deciding`. The derived area status stays `spiking` (open problems).

```markdown
## Area: Session storage
**Findings**: docs/findings-session-storage.md + docs/evidence-session-storage.md
- `deciding` How to choose the session store? → adrs/adr-session-storage-01-store-choice.md
- `deciding` How to migrate existing sessions? → adrs/adr-session-storage-02-migration.md
```

## Point 4 — After user confirmation

User confirms both options → problems `done`; all problems `done` → the derived area status is `done`.

```markdown
## Area: Session storage
**Findings**: docs/findings-session-storage.md + docs/evidence-session-storage.md
- `done` How to choose the session store? → adrs/adr-session-storage-01-store-choice.md
- `done` How to migrate existing sessions? → adrs/adr-session-storage-02-migration.md
```

## Point 5 — New evidence reopens a problem

A later measurement shows the chosen store's failover exceeds the SLA → **sync-update-artifacts** reopens the store-choice problem `done` → `deciding`; the derived area status returns to `spiking`; the ADR and solution doc are rewritten in place.

```markdown
## Area: Session storage
**Findings**: docs/findings-session-storage.md + docs/evidence-session-storage.md
- `deciding` How to choose the session store? → adrs/adr-session-storage-01-store-choice.md
- `done` How to migrate existing sessions? → adrs/adr-session-storage-02-migration.md
```

## Rules in play

- A `done` problem always has its ADR; an area is never `done` with an open problem.
- Area status is derived from its problems and findings-pair link — never stored.
- Statuses track saved artifacts, not in-flight dispatches.

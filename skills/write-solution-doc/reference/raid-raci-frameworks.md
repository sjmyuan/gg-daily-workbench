# RAID and RACI Frameworks

Backs the `<governance-frameworks>` knowledge entry, used by **list-raids** and **list-raci**.

## RAID

RAID = **Risks** (future events that could negatively impact the solution), **Assumptions** (believed true, not yet validated), **Issues** (current problems or blockers), **Dependencies** (external factors or teams the solution relies on).

Each item: ID, Category, Description, Impact (H/M/L), Probability (H/M/L, Risks only), Mitigation/Resolution, Owner, Status. Present as a structured table, one per category.

Description names the mechanism and the trigger — the component plus the condition that produces the impact, e.g. "Pool exhaustion when concurrent writers exceed `maximum-pool-size: 20`". A category such as "performance risk" is a placeholder: replace it or drop the row.

RAID lists what this solution introduces, or what the baseline lacks and thereby blocks. It is never a generic risk catalogue: a probe's answer becomes an item only when it changes a design decision or a step in the plan.

## RACI

RACI = **R**esponsible (does the work), **A**ccountable (ultimately answerable — only ONE per task), **C**onsulted (two-way input), **I**nformed (kept up-to-date, one-way). Present as a matrix table: tasks as rows, teams/roles as columns, R/A/C/I in cells, one "A" per row.

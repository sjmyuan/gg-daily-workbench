# Pipeline Integration Design

Used by **create-skill-file** (pipeline step 9) and **validate-created-skill** (rules step 6).

When a skill is part of a multi-skill pipeline (one skill's output is consumed by another), verify these 5 integration points:

1. **Handoff mechanism**: the producing skill includes an export/persist capability that writes output to a file; the consuming skill defines an input schema and supports loading from files. Do not rely on conversation text as the sole transport layer.
2. **Shared schema (consumer-owned)**: the consuming skill defines the format in one literal template; the producing skill writes compliant output and its examples reproduce that template's headings, fields, order, and statuses. Disagreement → the consumer wins; drift → 🔴 Major.
3. **Bidirectional awareness**: each skill references the other by name — the producing skill states what consumes its output; the consuming skill states where its input comes from.
4. **Guard clauses**: the downstream skill's when-to-use includes a constraint preventing premature loading (e.g., "Do NOT load when no plan has been generated yet — let [upstream-skill] handle it first").
5. **Link self-containment**: every markdown path resolves inside the skill's own folder; another skill is named, never deep-linked (`../other-skill/reference/x.md`). A skill may be installed alone, so an escaping link resolves to nothing and fails silently. Shared doctrine is duplicated as a slice with a `Scope:` header, never shared by path. Check with `../review-skill/scripts/check_skill_links.py <skill-dir>`; each `ESCAPE` / `ABS` finding is a defect.

Apply when the user describes a workflow involving multiple skills (e.g., "first plan, then execute").
When artifacts cross the boundary, apply **artifact-consistency**: one owner template, examples on
both sides reproduce it, shared examples update together.

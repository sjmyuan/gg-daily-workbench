# Skill File Section Semantics

A well-formed copilot skill file uses these sections with distinct, non-overlapping purposes:

| Section | Purpose | What belongs here |
|---|---|---|
| Frontmatter `description:` | Skill-load decision | Plain-language summary used by VS Code/Copilot to decide whether to load this skill; must cover **all** activation scenarios |
| `<when-to-use-this-skill>` | Post-load scope check | Bullet list of user-facing scenarios that confirm this skill applies; must align with the frontmatter `description` |
| `<knowledge>` | Facts the agent recalls | Reference tables, directory layouts, API signatures, platform constraints, banned practices, selection guides; large rubrics extracted to `reference/` files and loaded on demand. One-line entries may share a single `<named-standards>` table (`name` \| rule \| reference), with capability steps citing the name |
| `<capabilities>` | Procedures the agent executes | Ordered step-by-step instructions for *how* to accomplish a task; named with an action verb |
| `<rules>` | Internal routing and guard triggers | One routing rule per capability ("When [scenario] → use [capability]"), plus a guard rule for each known misapplication ("Never …"); must not repeat what the capability already says; **required in every skill — absence is 🔴 Major** |
| `<context-loading-guide>` in `<knowledge>` | On-demand context router | Condition-first table (`Load when` \| `Provides` \| `File`) that routes on-demand files whose load condition is not fixed by a capability step — examples, plus step-independent references. References tied to a specific step are routed inline from that step; every knowledge entry or named-standards row links its own reference file |

**Common structural violations**:
- Knowledge embedded in capabilities (lookup tables, API lists, constraint bullets inside a capability section)
- Rules that re-state capability content instead of routing to it
- A missing `<rules>` section — required in every skill, including single-capability ones
- Capabilities written as bullet-point fact lists instead of ordered procedural steps
- Capabilities named as nouns (`<storage-management>`) instead of action verbs (`<manage-storage>`)
- Skill name (frontmatter `name:`) is a noun phrase (`svg-editor`) instead of an action verb (`edit-svg`)
- A bare `<examples>` section used instead of a `<context-loading-guide>` entry inside `<knowledge>`
  (the guide consolidates on-demand context — examples and step-independent references — in one place)
- On-demand files (references, examples) with no load route — not linked from a knowledge subsection, a capability step, or a context-loading-guide row
- `<context-loading-guide>` written as a bullet list, or as a two-column **Scenario | Reference** table — the first column must be a decision condition ("Load when…"), not a content description
- `<context-loading-guide>` first column describes *what the file contains* instead of *when to load it* — forces the agent to infer the loading condition, leading to missed or wrong loads
- `<examples>` content embedded inline rather than referenced by file path for on-demand loading
- Large reference rubrics embedded inline in SKILL.md instead of extracted to `reference/` files
- Using `<knowledge>`, `<capabilities>`, or `<rules>` tag syntax to reference sections in prose (e.g., "put this in `<knowledge>`")
  — use plain names like "the knowledge section" instead; XML-like syntax may confuse the AI during parsing

## Directory layout

```
skills/<skill-name>/
├── SKILL.md              # the skill definition file
├── examples/             # one .md per demonstrated scenario
│   ├── example-one.md
│   └── example-two.md
├── reference/            # detailed rubrics (optional)
│   ├── reference-one.md
│   └── reference-two.md
└── scripts/              # authored automation (optional; justified per script-and-cli-policy.md)
    └── verb_object.py
```

- `scripts/` holds only scripts a capability step runs repeatedly; every script is named by that step.
- Do not create `scripts/` for one-off authoring work — run a CLI or an inline one-liner instead.

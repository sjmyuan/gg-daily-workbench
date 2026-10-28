# Section Semantics for Copilot Skill Files

Used by **create-skill-file** (structure step 10) and **validate-created-skill** (structure step 1).

## Required sections and purpose

| Section | Purpose | What belongs here |
|---|---|---|
| Frontmatter `description:` | Skill-load decision | Plain-language summary covering **all** activation scenarios |
| `<when-to-use-this-skill>` | Post-load scope check | Bullet list of user-facing scenarios aligning with `description` |
| `<knowledge>` | Facts the agent recalls | Tables, layouts, APIs, constraints, banned practices; large rubrics extracted to `reference/` |
| `<knowledge>` consolidation | One-table form | One-line entries may share a single `<named-standards>` table (`name` \| rule \| reference); capability steps then cite the name |
| `<capabilities>` | Procedures the agent executes | Ordered step-by-step instructions; action-verb names |
| `<rules>` | Internal routing and guard triggers | One routing rule per capability ("When [scenario] → use [capability]"), plus a guard rule for each known misapplication ("Never …"); required in every skill and never a restatement of a capability step |
| `<context-loading-guide>` in `<knowledge>` | On-demand context router | Condition-first table (`Load when` \| `Provides` \| `File`) routing examples and step-independent references; step-tied references are routed inline from that step; every knowledge entry or named-standards row links its own reference file |

## Section order
frontmatter → `<when-to-use-this-skill>` → `<knowledge>` → `<capabilities>` → `<rules>`

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

## Common structural violations
- Knowledge embedded in capabilities (lookup tables, API lists, constraint bullets inside a capability)
- Rules that re-state capability content instead of routing to it
- A missing `<rules>` section — required in every skill, including single-capability ones
- Capabilities written as bullet-point fact lists instead of ordered procedural steps
- Capabilities named as nouns instead of action verbs
- Skill name (frontmatter `name:`) is a noun phrase instead of an action verb
- A bare `<examples>` section instead of a `<context-loading-guide>` entry inside knowledge
- On-demand files (references, examples) with no load route — not linked from a knowledge subsection, a capability step, or a context-loading-guide row
- `<context-loading-guide>` as a bullet list, or description-first instead of condition-first
- `<context-loading-guide>` first column describes what the file contains instead of when to load it
- `<examples>` content embedded inline instead of referenced by file path
- Large reference rubrics embedded inline instead of extracted to `reference/` files
- Using `<knowledge>`, `<capabilities>`, or `<rules>` tag syntax to reference sections in prose — use plain names

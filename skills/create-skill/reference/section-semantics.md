# Section Semantics for Skill Files

Scope: section order, directory layout, and structural violations. What each section **holds** is owned by
`content-model`; this file never restates it.

Used by **create-skill-file** (step 3) and **validate-created-skill** (checks 3–5).

## Section order
frontmatter → `<when-to-use-this-skill>` → `<knowledge>` → `<capabilities>` → `<rules>`

Two sections carry no content class:

| Section | Role |
|---|---|
| Frontmatter `description:` | Load decision — covers every activation scenario |
| `<context-loading-guide>` in knowledge | Condition-first router (`Load when` \| `Provides` \| `File`); references tied to a step route inline from that step instead |

One-line knowledge entries may share a single `<named-standards>` table (`name` \| rule \| reference); capability steps cite the name.

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
- A missing `<rules>` section — required in every skill, including single-capability ones
- Capabilities named as nouns instead of action verbs
- Skill name (frontmatter `name:`) is a noun phrase instead of an action verb
- A bare `<examples>` section instead of a `<context-loading-guide>` entry inside knowledge
- On-demand files with no load route — not linked from a knowledge subsection, a step, or a guide row
- `<context-loading-guide>` as a bullet list, or description-first instead of condition-first
- `<examples>` content embedded inline instead of referenced by file path
- Large reference rubrics embedded inline instead of extracted to `reference/` files
- Using `<knowledge>`, `<capabilities>`, or `<rules>` tag syntax in prose — use plain names

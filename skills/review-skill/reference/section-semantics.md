# Skill File Section Semantics

Scope: section order, directory layout, and structural violations. What each section **holds** is owned by
`content-model`; this file never restates it.

Used by **review-skill-file** (step 4), which also owns the naming checks.

## Section order
frontmatter → `<when-to-use-this-skill>` → `<knowledge>` → `<capabilities>` → `<rules>`

Two sections carry no content class:

| Section | Role |
|---|---|
| Frontmatter `description:` | Load decision — must cover **all** activation scenarios |
| `<when-to-use-this-skill>` | Post-load scope check — bullets aligning with `description` |
| `<context-loading-guide>` in knowledge | Condition-first router (`Load when` \| `Provides` \| `File`); step-tied references route inline from that step |

One-line knowledge entries may share a single `<named-standards>` table (`name` \| rule \| reference).

**Common structural violations** — class-level findings belong to `content-model`, not here:

| Violation | Severity |
|---|---|
| A missing `<rules>` section — required in every skill | 🔴 Major |
| A bare `<examples>` section instead of a `<context-loading-guide>` inside knowledge | 🟡 Minor |
| `<context-loading-guide>` as a bullet list, or description-first instead of condition-first | 🟡 Minor |
| On-demand files with no load route — not linked from a knowledge subsection, a step, or a guide row | 🟡 Minor |
| `<examples>` content embedded inline instead of referenced by file path | 🔴 Major |
| Large reference rubrics embedded inline instead of extracted to `reference/` | 🔴 Major |
| `<knowledge>`, `<capabilities>`, or `<rules>` tag syntax used in prose instead of plain section names | 🟡 Minor |

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

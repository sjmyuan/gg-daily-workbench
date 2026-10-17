# Label Safety

Used by **author-mermaid-diagram** (step 4) and **validate-diagram-syntax** (step 4).

## Breaker table

Only three patterns break rendering.

| Context | Breaks | Safe |
|---|---|---|
| Sequence message or `Note` text | `;` | `, " # ( ) [ ] { } \| &` |
| Flowchart node or edge label, unquoted | `" ( ) [ ] { } \|` | `; , # &` |
| C4 label and `Rel` description | — | all |

## Rules

- **Sequence text**: never use `;` in a message or `Note`; reword to `,` or split the statement.
- **Flowchart labels**: quote any label containing `" ( ) [ ] { } |` — `A["Save (async)"]`.
- **C4**: labels are safe; quote them anyway for consistency.
- **Line breaks**: use `<br/>`, never a raw newline inside a label.
- **Escapes are last resort**: inside quotes use `#quot;` `#35;` `#40;` `#41;` `#59;` `#124;`.
- **Markdown inside labels**: `<br/>` works; backticks and markdown links do not render reliably.
- **Reword first**: a shorter label that avoids the character beats an escape sequence.

## Pre-present checklist

- No `;` in any sequence message or `Note`.
- Every flowchart label with a special character is quoted.
- Every line break is `<br/>`.
- No label exceeds one short phrase; details live in the takeaway line below the diagram.

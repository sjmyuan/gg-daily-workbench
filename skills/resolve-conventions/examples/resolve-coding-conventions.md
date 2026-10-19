# Example: Resolve Coding Conventions

**Scenario**: A caller must write code in `acme/order-service` without violating its local style. Demonstrates **resolve-conventions** for the `coding` domain.

**Applies**: **resolve-conventions**

## Input / Context
Repo `acme/order-service`, domain `coding`, fields `formatter`, `linter`, `style`, `comments`, `naming`, `error handling`.

Evidence found:
- `.prettierrc` — 2-space indent, single quotes, trailing commas.
- `.eslintrc` — `airbnb-base`, plus `no-explicit-any` and `no-console`.
- `STYLE.md` — named exports only; comments explain why, never what.
- Recent changes in `src/gateway/` — camelCase functions, PascalCase types, typed errors.

## Output

```
## Convention Card — acme/order-service · coding
| Field | Value | Evidence |
|---|---|---|
| Formatter | Prettier: 2 spaces, single quotes, trailing commas | .prettierrc:1 |
| Linter | ESLint airbnb-base + custom rules | .eslintrc:1 |
| Style | named exports; no default exports | STYLE.md:4 |
| Comments | sparse, why-only; no restating code | STYLE.md:12 |
| Naming | camelCase functions, PascalCase types | recent: 8/10 files |
| Error handling | throw typed errors; never swallow | STYLE.md:20 |
| Prohibitions | no `any`, no `console.*` | .eslintrc:8 |

Conflicts: none.
Unknowns: none.
```

## Validation
- Every field cites a config, doc, or sample.
- The prohibitions come from the linter config, not inference.
- The card is returned to the caller; this skill wrote no code.

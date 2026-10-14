# Evidence Doc Schema and Stable IDs

Used by **author-evidence-doc** and **update-findings-doc**. Claims, confidence, and coverage live only here; the human doc stays free of them.

## Metadata block

```
<!-- evidence-doc
area: <area-slug>
spike: <spike-name>
status: investigating | complete
scope: <one line>
related-areas: [<area-slug>]
human-doc: docs/findings-<area-slug>.md
-->
```

## Section order

| # | Section | Purpose |
|---|---|---|
| — | Metadata block | Machine-readable header, including the human doc path |
| 1 | Topic map | Topic slug → human heading anchor → claim IDs |
| 2 | Claim ledger | One row per claim |
| 3 | Searched-negatives | Dead-end searches |
| 4 | Coverage | In/out-of-scope status |
| 5 | Cross-area references | Constraints shared with another area's pair |

## Topic map schema

| Topic slug | Human heading | Claim IDs |
|---|---|---|

- One row per human-doc topic; link the heading as `findings-<area>.md#<heading-anchor>`.
- Every human-doc topic appears here; every claim ID belongs to exactly one topic.

## Claim ledger schema

| Claim ID | Claim | Verdict | Evidence (file:line) | Confidence |
|---|---|---|---|---|

- One row per claim; every human-doc topic claim appears here.
- Claim = a question the area asks or a fact the reader needs.
- Verdict = the answer in one phrase.
- Confidence = one of the five tags below.
- Evidence depends on claim type:
  - ✅ Verified / 🔶 Inferred → the exact `file:line` (multiple separated by `;`).
  - ⚠️ Inconsistency → both conflicting `file:line`s.
  - ❓ Gap / 💭 Assumption → the search scope, cross-linked to its Searched-negatives row.

## Claim rules
- One fact per row; no reasoning or justification.
- Every claim cites `<reference> (file:line)` and a confidence tag.
- A ❓ Gap or 💭 Assumption cites its search scope instead.
- Never present 🔶 Inferred or 💭 Assumption as ✅ Verified.
- Never use vague references ("the service layer"); name a concrete symbol or module.

## Confidence tags

| Tag | Meaning |
|---|---|
| ✅ Verified | Directly read in code, `file:line` confirmed |
| 🔶 Inferred | Reasoned from evidence, not directly confirmed |
| 💭 Assumption | Taken for granted without direct evidence |
| ⚠️ Inconsistency | Contradiction (code vs code/docs/config); both sides located |
| ❓ Gap | Searched but not found, or not investigated |

## Searched-negatives

| Search (pattern/query) | Result | Next step |
|---|---|---|

Record dead-end searches so later work is not repeated; list open questions still to investigate.

## Coverage

| In-scope question | Investigated | Not investigated / Gaps |
|---|---|---|

Coverage is in/out-of-scope status only — never a changelog.

## Cross-area references

| Constraint | This area | Related area | Evidence (file:line) |
|---|---|---|---|

List constraints the area shares with another area's pair; cite the other area's claim ID when one exists.

## Stable ID scheme

| Element | Format | Example |
|---|---|---|
| Area | `<area-slug>` | `payment` |
| Topic | `<area>/<topic-slug>` | `payment/authorize-flow` |
| Claim | `<area>/<topic-slug>#c<N>` | `payment/authorize-flow#c2` |

- IDs are area-scoped and stable for the life of the topic.
- Never renumber existing IDs; add new IDs for new claims.

## Linking rules
- The evidence doc names its human doc in the metadata block.
- Each topic-map row links its human heading anchor.
- Linking is one-way: the human doc never references this doc, so it stays publishable anywhere.
- Downstream docs cite the ID plus the `<reference> (file:line)` form (for example "`payment/authorize-flow#c2`, `ChargeService#authorize (ChargeService.java:88)`").
- The ledger's Evidence column stays bare `file:line` for machine parsing; the human doc uses the symbol form.

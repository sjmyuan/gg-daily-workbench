# Evidence Ledger and Stable IDs

Used by **compile-evidence-ledger** and **update-findings-doc**.

## Evidence ledger schema

| Claim ID | Claim | Verdict | Evidence (file:line) | Confidence |
|---|---|---|---|---|

- One row per claim; every topic-block claim appears here.
- Claim = a question the area asks or a fact the reader needs.
- Verdict = the answer in one phrase.
- Confidence = one of the five tags below.
- Evidence depends on claim type:
  - ✅ Verified / 🔶 Inferred → the exact `file:line` (multiple separated by `;`).
  - ⚠️ Inconsistency → both conflicting `file:line`s.
  - ❓ Gap / 💭 Assumption → the search scope, cross-linked to its Searched-negatives row.

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

## Stable ID scheme

| Element | Format | Example |
|---|---|---|
| Area | `<area-slug>` | `payment` |
| Topic | `<area>/<topic-slug>` | `payment/authorize-flow` |
| Claim | `<area>/<topic-slug>#c<N>` | `payment/authorize-flow#c2` |

- IDs are area-scoped and stable for the life of the topic.
- Never renumber existing IDs; add new IDs for new claims.
- Downstream docs cite the ID plus the `<reference> (file:line)` form (for example "`payment/authorize-flow#c2`, `ChargeService#authorize (ChargeService.java:88)`").
- The ledger's Evidence column stays bare `file:line` for machine parsing; topic prose uses the symbol form.

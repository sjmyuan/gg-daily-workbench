# Confidence & Coverage Guide

Presentation format for reporting findings honestly: what is certain, what is not, and what was missed.

Backs the `<present-findings-with-confidence>` capability.
The tag vocabulary is defined once in `<finding-confidence-model>`; this file owns when to reach for a tag and how to phrase it.
Plain-language presentation lives in **plain-language-presentation.md**.

## When to use each tag

| Tag | Reach for it when |
|---|---|
| ✅ Verified | you opened the file and read the line |
| 🔶 Inferred | the reasoning holds but nobody confirmed it — "no config found, so the default serializer is assumed" |
| 💭 Assumption | a premise you did not test — "sibling packages follow the same pattern" |
| ⚠️ Inconsistency | two sources of truth disagree: code vs code, docs, or config |
| ❓ Gap | you searched and did not find it, or did not look |

## Confidence & Coverage Block Format

Close every investigation with a compact block (in a compiled report, the section heading carries the block title; keep the five bullets verbatim):

```
### Confidence & Coverage
- ✅ Verified: ...
- 🔶 Inferred: ...
- 💭 Assumptions: ...
- ❓ Gaps: ...
- ⚠️ Inconsistencies: ...
```

## Phrasing Examples

- **Verified**: "`ChargingService` computes `fee = gross * 0.03` — Verified, `ChargingService.java:42`"
- **Inferred**: "🔶 Inferred — no config file found; Kafka default serializer assumed"
- **Assumption**: "💭 Assumption — 'the fee' is a single concept; a second `fee` exists in the payout branch (see Inconsistency)"
- **Gap**: "❓ Gap — only the charging branch was traced; the refund branch was not investigated"
- **Inconsistency**: "⚠️ Inconsistency — `README.md` states 5 retries, but `EmailAdapter.java:40` retries 3 times"

## Rules of Thumb

- A stated gap is a finding; a hidden gap is a partial truth. Never present "what I found" without "what I did not find".
- Inferred and Assumption findings must state *why*, so the user can verify the reasoning; render them as issue cards when consequential (per plain-language-presentation.md).
- Inconsistencies must locate both sides; classify severity per `reference/pattern-discovery-strategies.md`.
- When a gap is later closed, re-run the affected investigation step and update the profile.

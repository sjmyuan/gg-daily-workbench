# Example: Repo Expertise Grounding a Finding

**Scenario**: A PR in `payment-service` adds a hand-rolled retry loop. The repo documents where retries
belong; the reviewer would otherwise file a 🟡 style nit or nothing at all.

**Applies**: **surveying-repo-expertise**

## Input

- **Diff**: `src/payment/ChargeClient.java` (+48/-3) — `for` loop with three attempts and `Thread.sleep`.
- **Repo**: `AGENTS.md`, `CONTRIBUTING.md`, `docs/adr/`, `.github/workflows/ci.yml`, module READMEs.

## Step 1 — Sources present, by priority

| Priority | Source found | Read |
|---|---|---|
| 1 | No repo-local skills or agents | — |
| 2 | `AGENTS.md`, `CONTRIBUTING.md` | yes |
| 3 | `docs/adr/009-outbound-resilience.md`, `docs/adr/014-layout.md` | yes |
| 4 | `src/payment/README.md` | yes |
| 5 | `.github/workflows/ci.yml`, `build.gradle.kts` | yes |
| 6 | `CODEOWNERS` | yes |
| 7 | Recent commits | not needed — priorities 2–5 answered |

## Step 2 — Evidence card

| Field | Value | Evidence |
|---|---|---|
| Changed area | `src/payment` — outbound client to the card processor | diff |
| Governing rule | All outbound retries go through `resilience-kit`; no hand-rolled retry loops | `AGENTS.md:31` |
| Governing rule | New outbound clients must register a circuit breaker | `docs/adr/009-outbound-resilience.md:14` |
| Commands | build and test command | `CONTRIBUTING.md:22` |
| Placement | clients live in `src/payment/client/` | `docs/adr/014-layout.md:9` |
| Known debt | `LegacyChargeClient` still retries inline, tracked in `docs/debt.md:8` | `docs/debt.md:8` |
| Gap | no documented test command for integration tests | searched `CONTRIBUTING.md`, `README.md`, `ci.yml` |

## Step 3 — How the card changes the review

| Without the card | With the card |
|---|---|
| "Prefer a shared retry utility" — 🟡 Minor, easy to defer | Violates `AGENTS.md:31` — 🔴 Major, with the rule quoted |
| "Consider adding a circuit breaker" — 🟡 suggestion | Required by `docs/adr/009:14` — 🔴 Major, requirement unmet |
| "File should be in `src/payment/client/`" — reviewer preference | Documented layout — 🟡 Minor with `docs/adr/014:9` cited |
| "Tests look thin" — vague | Test command documented; run it, then report what actually fails |
| Silent about the missing integration-test command | Challenge `C1`, because the review cannot confirm behavior |

## Expected output (abridged)

````markdown
## Code Review Summary

**Scope**: `ChargeClient` retry loop in `payment-service`
**Repo expertise**: `AGENTS.md`, ADR-009, ADR-014, `CONTRIBUTING.md`
**Open challenges**: 1 open, 1 blocking · **Unverified referents**: 0
**Ready to merge?**: No — the change bypasses the documented retry utility and its breaker

## ❓ Challenges & Questions

| # | Question | Why it looks unreasonable | Assumed meanwhile | Settles it | Blocking |
|---|---|---|---|---|---|
| C1 | Where is the integration-test command documented? | `CONTRIBUTING.md`, `README.md`, and `ci.yml` cover unit tests only | Reviewed unit coverage only; behavior under retry is unconfirmed | A command, or confirmation that none exists | yes |

## Findings

### 🔴 Major Issues

#### Hand-rolled retry loop bypasses the shared resilience kit
- **File**: `src/payment/ChargeClient.java:57`
- **Confidence**: Confirmed
```java
57 │         for (int attempt = 0; attempt < 3; attempt++) {
```
- **Issue**: The repo requires all outbound retries to go through `resilience-kit` (`AGENTS.md:31`);
  this loop retries inline with a fixed sleep and no breaker, so it also misses `docs/adr/009:14`.
- **Impact**: Retries bypass the shared budget and metrics — a processor outage becomes three times
  the traffic, invisible to the existing dashboards.
- **Recommendation**: Replace the loop with `resilience-kit`'s `RetryPolicy` and register the breaker,
  as `LegacyChargeClient` is already scheduled to do (`docs/debt.md:8`).

## Repo Expertise Applied

| Source | Rule or fact | Effect on this review |
|---|---|---|
| `AGENTS.md:31` | Outbound retries go through `resilience-kit` | Escalated the retry loop from 🟡 to 🔴 |
| `docs/adr/009:14` | New outbound clients register a breaker | Added the missing-breaker requirement |
| `docs/adr/014:9` | Clients live in `src/payment/client/` | Kept the placement note at 🟡, cited |

**Repo expertise gaps**: no documented integration-test command — raised as `C1`.
````

## Why this is better

- Severity follows the repo's own rules instead of reviewer taste, so the finding is hard to dismiss.
- A rule the reviewer dislikes (four-space indentation) never becomes a finding — the card records it.
- The missing test command stops being a silent assumption and becomes a blocking question.
- Placement feedback cites an ADR rather than asserting a preference.

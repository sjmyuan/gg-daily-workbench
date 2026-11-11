# Example: Parallel Investigation Across Independent Areas

## User Request

"How does authentication work across our six services? I need the whole picture today."

Applies `<dispatch-investigation-clones>`.

## Step 1 — Split into disjoint areas

| Area | Boundary (in) | Boundary (out) | Sub-question | Depth |
|---|---|---|---|---|
| token-issuance | `auth-service` | gateway, session store | How is a token issued and signed? | call stack |
| token-validation | `gateway` | `auth-service` internals | How is each request validated? | sequence |
| session-state | Redis usage in both repos | token format | Is any server-side session state kept? | C3 |

Three areas, no overlap, together covering the question. The areas report back to the host; none reads the others.

## Step 2 — Briefs (one per clone)

Each brief carries: the boundary above, the sub-question, the depth, and this return contract.

```
Return: claims tagged ✅ Verified / 🔶 Inferred / 💭 Assumption / ⚠️ Inconsistency / ❓ Gap.
Each issue as an issue card (Problem / Evidence / Why it matters / What to do / Confidence).
Searched-negatives list. Return open questions upward — do not ask the user, do not re-fan-out.
Read-only: do not edit files.
```

## Step 3 — Clone reports (abridged)

**token-issuance** — `AuthController.login()` (`AuthController.java:41`) → `TokenService.issue()` (`TokenService.java:66`) → `JwtEncoder.encode()`.
15-minute TTL read from `application.yml:31`. ❓ Gap: refresh-token path not traced.

**token-validation** — `JwtValidationFilter` (`JwtValidationFilter.java:28`) verifies the signature per request, no cache.
🔶 Inferred: keys fetched from `auth-service` `/jwks` on startup — bootstrap step not read.

**session-state** — ⚠️ Inconsistency: `gateway` keeps a `session:{sub}` key in Redis (`SessionStore.java:52`).
`auth-service/README.md` states "sessions are stateless". Both sides confirmed.

## Step 4 — Merge

- Deduped: both `token-issuance` and `token-validation` claimed the 15-minute TTL — kept once, at its issuing line.
- Spot-checked one claim per area against source: TTL line, filter line, Redis key line.
- Conflict surfaced, not smoothed: Redis session state contradicts the stateless claim.

## Merged answer

Authentication is a signed JWT issued by `auth-service`, validated per request at the gateway, with an undocumented Redis session key that contradicts the documented stateless design.

### ⚠️ Undocumented session state

- **Problem**: the gateway stores a per-user Redis key while the service README says sessions are stateless.
- **Evidence**: `SessionStore.java:52` vs `auth-service/README.md`
- **Why it matters**: a second source of truth for session lifetime.
  A TTL change in one place silently breaks the other.
- **What to do**: decide whether the Redis key is a cache or session state, then document or delete it.
- **Confidence**: ⚠️ Inconsistency — both sides read directly.

### Confidence & Coverage
- ✅ Verified: issuance and TTL (`TokenService.java:66`, `application.yml:31`)
- ✅ Verified: per-request validation (`JwtValidationFilter.java:28`); Redis key (`SessionStore.java:52`)
- 🔶 Inferred: JWKS fetch on startup — bootstrap code not read
- 💭 Assumptions: the six services share one gateway; no second ingress examined
- ❓ Gaps: refresh-token path untraced; key rotation not investigated
- ⚠️ Inconsistencies: Redis session state vs "stateless" README claim

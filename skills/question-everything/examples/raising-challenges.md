# Example: Raising Challenges on a Returned Result

**Scenario**: A sub-agent reported that request throttling is enforced at the API gateway by Redis counters, citing `GatewayRateLimiter.kt:57`. The result will feed an architecture decision, and the challenges are handed to the orchestrator — nothing is verified yet.

Applies **question-the-result**.

## Input / Context
- **Returned result**: "Throttling is enforced at the gateway — `GatewayRateLimiter.kt:57` increments a Redis counter per API key and rejects above 100 req/s."
- **Stakes**: architecture decision; a wrong claim changes whether the gateway is the only enforcement point.

## Questioning (question-the-result)
1. **Completeness** — Does the claim cover every route, or only gateway-fronted traffic? What about service-to-service calls that bypass the gateway?
2. **Correctness** — Does the cited line increment per API key, and is the limit enforced or only logged?
3. **Ambiguity** — "100 req/s" — per key, per IP, or per route? Fixed window or sliding?
4. **Evidence** — Is the counter shared across gateway instances, or local to one pod?

## Output — prioritized challenges (raised, not yet verified)
- **C1 (Correctness, high)** — `GatewayRateLimiter.kt:57` increments a counter and rejects above the limit: the line may only log the overage, leaving the gateway unprotected. Satisfactory answer: confirm the rejection path is enforced at that line.
- **C2 (Completeness, high)** — Throttling is enforced at the gateway: service-to-service traffic may bypass it, so the gateway may not be the only enforcement point. Satisfactory answer: name every path that reaches the backend without the limiter.
- **C3 (Ambiguity, medium)** — "100 req/s": unclear whether the window is per key, per route, or global, and whether it is fixed or sliding. Satisfactory answer: state the counter key and window type.

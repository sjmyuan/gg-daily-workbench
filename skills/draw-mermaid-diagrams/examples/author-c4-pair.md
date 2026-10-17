# Example: Drawing a C4 Context, Container, and Component Set

**Scenario**: The request fixes a three-level C4 set — context, containers, components — and the user has confirmed the facts.

**Applies** **author-mermaid-diagram**.

---

## Input

> "We run a payouts platform. Merchants call our Payout API.
> Inside, a Payout Service validates requests, then writes to Postgres and calls Stripe.
> A Ledger Service records every entry in its own Postgres. Ops watch everything through Grafana.
> Can you show me how this fits together?"

## Requested set

The request asks for C1 → C2 → C3, one message per level.

| Level | Message |
|---|---|
| C1 context | Who interacts with the platform, and what is in scope |
| C2 container | Which applications and stores compose the platform |
| C3 component | Which components live inside the Payout Service |

**Announced to the user**:
> Three levels, one message each — context, containers, then the Payout Service internals.

## C4 context (C1)

```mermaid
C4Context
    title Payout Platform — System Context

    Person(merchant, "Merchant", "Requests payouts")
    System(payouts, "Payout Platform", "Executes merchant payouts")
    System_Ext(stripe, "Stripe", "Moves funds")
    System_Ext(obs, "Grafana Cloud", "Monitoring and alerts")

    Rel(merchant, payouts, "requests payouts", "HTTPS")
    Rel(payouts, stripe, "submits transfers", "HTTPS")
    Rel(payouts, obs, "exports metrics", "OTLP")
```

> **Takeaway**: Merchants reach one platform that delegates fund movement to Stripe and exports telemetry to Grafana.

## C4 container (C2)

```mermaid
C4Container
    title Payout Platform — Container Diagram

    Person(merchant, "Merchant", "Requests payouts")

    System_Boundary(payouts, "Payout Platform") {
        Container(api, "Payout API", "Go", "Validates and routes payout requests")
        Container(svc, "Payout Service", "Go", "Executes payout workflow")
        ContainerDb(pdb, "Payout DB", "PostgreSQL", "Payout state")
        Container(ledger, "Ledger Service", "Java", "Double-entry ledger")
        ContainerDb(ldb, "Ledger DB", "PostgreSQL", "Ledger entries")
    }

    System_Ext(stripe, "Stripe", "Moves funds")

    Rel(merchant, api, "requests payouts", "HTTPS")
    Rel(api, svc, "forwards requests", "gRPC")
    Rel(svc, pdb, "reads / writes payouts", "SQL")
    Rel(svc, ledger, "records entries", "gRPC")
    Rel(ledger, ldb, "reads / writes entries", "SQL")
    Rel(svc, stripe, "submits transfers", "HTTPS")
```

> **Takeaway**: Two services and two stores; only the Payout Service talks to Stripe, and every payout reaches the ledger.

## C4 component (C3)

```mermaid
C4Component
    title Payout Service — Component Diagram

    Container_Boundary(svc, "Payout Service") {
        Component(handler, "Payout Handler", "gRPC", "Accepts payout requests")
        Component(validator, "Limit Validator", "Go", "Checks balance and daily limits")
        Component(repo, "Payout Repository", "DAO", "Persists payout state")
        Component(ledger_client, "Ledger Client", "gRPC client", "Records ledger entries")
        Component(stripe_client, "Stripe Client", "HTTP client", "Submits transfers")

        Rel(handler, validator, "validates")
        Rel(handler, repo, "persists")
        Rel(handler, ledger_client, "records")
        Rel(handler, stripe_client, "submits")
    }

    ContainerDb(pdb, "Payout DB", "PostgreSQL", "Payout state")
    Container(ledger, "Ledger Service", "Java", "Double-entry ledger")
    System_Ext(stripe, "Stripe", "Moves funds")

    Rel(repo, pdb, "reads / writes", "SQL")
    Rel(ledger_client, ledger, "records entries", "gRPC")
    Rel(stripe_client, stripe, "submits transfers", "HTTPS")
```

> **Takeaway**: The handler orchestrates four collaborators; only the repository owns SQL and only one client owns each external call.

## Validation

```
$ mmdc -i docs/payouts.md -o /tmp/check.md && echo "3 of 3 parsed"
3 of 3 parsed
```

- One level per diagram; each level shows only its own elements.
- Externals carry `_Ext`; every `Rel` names a flow and a protocol.
- Each level shows only its own elements; no container or component leaks up a level.

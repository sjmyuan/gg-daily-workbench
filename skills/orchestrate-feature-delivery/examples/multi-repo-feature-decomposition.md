# Example: Multi-Repo Feature Decomposition

**Scenario**: A wallet-migration spike just finished. Its solution doc defines ~18 target-state changes across `api-gateway`, `order-service`, and `shared-contracts`. The user asks: "Split the spiked work into features, align which can be done in parallel, and give me an index so agents can plan and execute in parallel."

**Applies**: **decompose-change-into-features** → **map-features-to-repos** → **order-feature-delivery** → **produce-delivery-index**

## Input (target-state changes)

- **New**: `WalletService` in `order-service`; token endpoint in `api-gateway`; shared wallet DTOs + envelope schema in `shared-contracts`
- **Modified**: order flow in `order-service` consumes wallet; gateway route in `api-gateway`
- **Data**: `wallet_ledger` table in `order-service`
- **Retired**: `BankTransferService` in `order-service` (after cutover)

## 1. Decomposition (features)

- **F1 wallet-contracts** — `shared-contracts` only: wallet DTOs + envelope schema. *Small but widely-shared (consumed by F2/F3/F4) → extracted as a leading feature so consumers develop against a contract.*
- **F2 wallet-service** — `order-service`: `WalletService` + `wallet_ledger` migration + tests.
- **F3 wallet-api-gateway** — `api-gateway`: token endpoint + route.
- **F4 order-wallet-integration** — `order-service` + `api-gateway`: order flow consumes wallet, retire `BankTransferService`.

## 2. Feature × repo matrix

| Feature | api-gateway | order-service | shared-contracts |
|---|---|---|---|
| F1 wallet-contracts | — | — | PR |
| F2 wallet-service | — | PR | — |
| F3 wallet-api-gateway | PR | — | — |
| F4 order-wallet-integration | PR | PR | — |

## 3. Waves

- F1 depends on nothing → **Wave 0**.
- F2 and F3 consume F1's DTOs (contract-first) → **Wave 1, parallel**.
- F4 consumes F2's service and F3's endpoint → **Wave 2**.
- `order-service` hosts F2 then F4 — no file conflict, but its PRs serialize naturally across waves.

**Wave 0**: F1 · **Wave 1 (parallel)**: F2, F3 · **Wave 2**: F4 (after F2 + F3 merge)

## 4. Delivery index (initial state)

Written to `deliveries/wallet-migration/index.md` (see **delivery-layout**); plan folders are `deliveries/wallet-migration/{repo}/{feature-name}/` — the feature folder uses the kebab-case name (e.g. `wallet-contracts`), never the ID (`F1`).

```markdown
# Delivery Index: Wallet Migration

Artifact base: `~/work/my-work` · migrate wallet services out of the monolith

## Summary
4 features · 3 repos · 3 waves · critical path: F1 → F2/F3 → F4

## Spike References
- **Solution doc**: spikes/wallet-migration/solution.md — §2 topology, §4 contracts
- **ADRs**: spikes/wallet-migration/adrs/adr-wallet-01-payment-failure-handling.md · adr-cutover-01-service-cutover.md

## Repos
- `shared-contracts` — wallet DTOs + envelope schema
- `order-service` — wallet service, ledger, order integration
- `api-gateway` — token endpoint + wallet route

## Features
| ID | Name | Wave | Repos | Dependencies | ADRs | Rework of | Goal |
|---|---|---|---|---|---|---|---|
| F1 | wallet-contracts | 0 | shared-contracts | — | adr-wallet-01 | — | Wallet DTOs + envelope |
| F2 | wallet-service | 1 | order-service | F1 (contract-first) | adr-wallet-01 | — | Wallet service + ledger |
| F3 | wallet-api-gateway | 1 | api-gateway | F1 (contract-first) | adr-wallet-01 | — | Token endpoint + route |
| F4 | order-wallet-integration | 2 | order-service, api-gateway | F2, F3 | adr-cutover-01 | — | Order flow uses wallet |

## Waves
| Wave | Features | Merge gate |
|---|---|---|
| 0 | F1 | — |
| 1 | F2, F3 | after F1 merges |
| 2 | F4 | after F2 + F3 merge |

## Cell plan status
| Cell | Branch | PR | Commit | Status | Agent | Plan location |
|---|---|---|---|---|---|---|
| shared-contracts/F1 | — | — | — | unplanned | — | deliveries/wallet-migration/shared-contracts/wallet-contracts/ |
| order-service/F2 | — | — | — | unplanned | — | deliveries/wallet-migration/order-service/wallet-service/ |
| api-gateway/F3 | — | — | — | unplanned | — | deliveries/wallet-migration/api-gateway/wallet-api-gateway/ |
| order-service/F4 | — | — | — | unplanned | — | deliveries/wallet-migration/order-service/order-wallet-integration/ |
| api-gateway/F4 | — | — | — | unplanned | — | deliveries/wallet-migration/api-gateway/order-wallet-integration/ |

## Notes
- All 5 cells start **unplanned**; none is ready to execute before its plan file exists.
```

Branches are assigned when a cell is planned and the head **Commit** is recorded on the first execution handoff (per **branch-and-push-conventions**) — both columns are empty here because all 5 cells start **unplanned**.

All 5 cells start **unplanned** → the epic is now driven by **orchestrate-delivery** (see **examples/orchestration-round.md**): wave 0 dispatches `shared-contracts/F1`, then F2/F3 in parallel, then F4.

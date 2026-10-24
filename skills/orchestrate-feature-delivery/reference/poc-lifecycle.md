# POC Lifecycle

Rules for POC cells in `orchestrate-feature-delivery` (**define-poc-scope**).

A POC is a **temporary implementation** of one ADR option, delivered as an MR. The skill implements and verifies it; the **user** evaluates the MR and decides. There is no measurement step, report, or verdict.

## POC cell metadata

| Field | Meaning |
|---|---|
| `type` | `poc` — the cell implements one ADR option |
| `adr` | Governing ADR |
| `option` | The option under test (from the ADR's considered options) |
| `success-criteria` | Optional — the user's review checklist; never a gate or plan step |
| `replaces` | Optional — existing feature/implementation superseded on adoption |
| `compare` | Optional — sibling POC cells for other options (run in parallel) |

## Status transitions

`unplanned → planned → in-progress → verified → poc-ready → adopted | rejected` (plus `failed`/`blocked`). The independent verification gate (**verify-cell**) passes before **poc-ready**. A replaced feature is marked **superseded**.

- **poc-ready**: implementation complete, gate passed, MR open — awaits the user's review. No merge yet.
- **adopted**: user/team chose the option → **POC-as-implementation** (merge the MR → done) or **POC-as-decision-input** (close the MR; dispatch the **poc-gated** feature).
- **rejected**: option not chosen → close the cell and the MR, proceed on another option.

## Decision gate

The orchestrator never evaluates or decides. At **poc-ready**, the user reviews/tests the MR — optionally against `success-criteria` — and records **adopted** or **rejected** directly in the index, with a one-line rationale in `## Notes`. If the governing ADR changes while the POC is in flight, its criteria may be moot — surface the change to the user first (see **handle-adr-change**). Once recorded, the orchestrator reacts:

1. Dispatch **adr-writer** (draft-adr) to record the outcome in the ADR.
2. **Adopted** — apply the matching adoption model below.
3. **Rejected** — close the cell and the MR (ask the user); delivery proceeds on another option.
4. Apply **update-delivery-index**.

## Dispatch brief

The POC planner and executor briefs carry the governing `adr` (path), the `option` under test, and the optional `success-criteria` — the same fields the user reviews the MR against. Compare siblings carry their own option.

## Adoption models

- **POC-as-implementation**: the POC MR becomes the shipped feature — on adopt, merge it and mark `replaces` **superseded**.
- **POC-as-decision-input**: the MR only informs the choice — on adopt, close it and dispatch the **poc-gated** feature with the chosen option.

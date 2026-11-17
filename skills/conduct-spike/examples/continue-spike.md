# Example: Continue a Spike — Pre-Existing Notes and a Reversal

**Scenario, part 1**: The user supplies three pages of notes from last quarter on the reporting database. "Turn this into a decision, and settle whether we move reporting off the primary."

**Scenario, part 2**: Six weeks after adoption, the load test the ADR asked for fails. Re-open the decision.

**Applies**: `define-spike-scope` (single problem, notes supplied) → `decide-spike-problems` → `accept-adrs`, then `continue-spike`.

---

## Part 1 — Decide From Pre-Existing Notes

No re-investigation: the notes answer two of the three sufficiency questions.

| Sufficiency question | Notes answer it? | Action |
|---|---|---|
| Can a replica serve reporting? | Yes — read replica exists, `replica-proxy/README.md` | Adopt as a settled claim |
| What breaks during a replica cutover? | Partly — a long-running report holds a snapshot | One targeted read of `reporting/export.ts:74` |
| What does the move cost? | No | Change list from the two locations |

**Drivers**: `HC 1` primary-write latency unchanged (p95 ≤ 120 ms); `SP 1` report freshness ≤ 5 minutes; `SP 2` no new 24/7 component.

**File**: `adrs/adr-reporting-01-read-replica.md` — full template, `Status: adopt`.

**Decision spine**: Option 1 (read replica + connection routing) chosen over Option 2 (nightly extract to a warehouse). Replica satisfies `HC 1` and `SP 2` at $0 incremental; the warehouse wins freshness only with a component the team cannot staff.

**Gate result**: `ACCEPT (12/12)` | unverified: replica lag under the month-end batch — settled by a load test the ADR names as a prerequisite in its Implementation Plan.

**Accept**: user adopts; the load test is recorded as a precondition, not a follow-up note.

**Artifacts**: one ADR. The user's notes stay where they were — turning them into a `notes-<area>.md` would duplicate the ADR's citations with no consumer.

---

## Part 2 — Re-Investigate After Implementation

Six weeks later: the month-end load test shows replica lag of 11 minutes under the batch, failing `SP 1`.

### Step 1 — Settle what is already known

| Claim | State | Action |
|---|---|---|
| Replica serves read traffic | verified | keep |
| `HC 1` holds for OLTP | verified | keep |
| Replica lag under batch | **new evidence: 11 min > 5 min** | re-open `SP 1` |
| Warehouse staffing | settled: cannot staff | keep as a reject reason |

The scope question has not changed — it is still "how to move reporting off the primary". No scope gate.

### Step 2 — Investigate only the delta

Two reads: where the batch writes land (`reporting/batch.ts:41`) and whether the replica lag is write-volume or lock-bound (`pg_stat_replication` sample). Result: write-volume. That makes a lower-isolation replica unsuitable and points at a different mechanism.

### Step 3 — Rewrite the ADR in template form

`adrs/adr-reporting-02-decouple-batch.md` supersedes `adr-reporting-01`:

- `Status: superseded` on the old ADR, with a one-line pointer to the new one.
- The new ADR reuses `HC 1` and the settled reject reason, adds `SP 1` with its measured failure (11 min vs 5), and evaluates the warehouse again — now with the measured lag as the driver it wins on.
- Chosen: **Option 3 — batched CDC into a read store**, which needs no replica and keeps the warehouse out.
- Change set names the CDC consumer, the store, and the reconciliation check, each with a `file:line`, confidence, verify, and rollback row.

**Gate result**: `ACCEPT (12/12)` | unverified: CDC throughput at month-end peak, settled by the same load test, now a prerequisite.

### Step 4 — Update what cites the decision

| Artifact | Exists? | Action |
|---|---|---|
| `solution.md` | Yes — delivery is mid-flight | Replace the reporting section; reference the new ADR |
| `notes-<area>.md` | No | Nothing to update — say so |
| Delivery `index.md` feature row | Yes | Point at `adr-reporting-02`; the cell is re-planned |

**Accept**: user adopts the reversal. Old problem goes back to `open` then `decided` against the new ADR; delivery re-plans the cell.

**What this example shows**: settled claims are never re-verified, the reversal is a new ADR rather than an edit that hides the old decision, and only artifacts that already exist get updated.

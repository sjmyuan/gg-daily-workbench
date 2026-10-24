# plan-poc

A POC is a **normal feature plan** for one ADR option. It is not a probe harness and has no measurement or evaluation step.

1. **Prepare Environment (Prerequisites)**: apply **plan-prerequisites** — a branch per the repo's convention, no overlapping dirt, deps installed, affected-area baseline green; raise necessary blockers only.
2. Load the ADR and the option's **tech details** (draft-adr's **detail-options-tech**): target-state diagrams + code change profile (file:line, current code, proposed diff, how-to).
3. Clarify with the user: the option under proof, the **success criteria** (optional — the user's review checklist, not a plan step), and the standalone feature slice that demonstrates it.
4. **Define Scope Boundary**: the option's target area is **May change**; other options, other ADRs, and unrelated modules are **Must not change**; ratify with the user.
5. Break the slice into independently testable functionalities; order by dependencies; consolidate per plan-feature-implementation step 5.
6. Load **reference/tdd-approach-selection.md**; choose the TDD variant per functionality and document the rationale.
7. Create the plan exactly like a feature, using **reference/plan-file-format.md**: title + metadata, the ratified `## Scope Boundary`, optional `## Decisions`, then TDD step blocks (Write Focused Tests → Confirm Test Failure → Implement Minimal Code → Verify → Refactor → Validate → Clean Up → Verify Cleanup → Quality Gate).
8. Set **Type** to `poc` and record the **ADR**, **Option**, and optional **Success criteria** in the metadata block; keep step count ≤ 25.
9. **Validate Plan Quality** against **reference/plan-quality-checklist.md**; revise failures before presenting.
10. Summarize to the user; persist via **export-plan**. Execution is normal — the executor implements, commits, and offers to open an MR. The user evaluates the MR and records the decision; the plan never measures or judges.

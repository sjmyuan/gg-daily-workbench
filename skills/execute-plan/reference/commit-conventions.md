# Commit Conventions

Small-step commit rules applied throughout execution:

| Rule | Detail |
|---|---|
| Commit frequency | One commit per step, after the step is validated and marked ✅ |
| Commit size | A single logical change — the step's objective only |
| Message format | Follow the repo's existing convention (check recent `git log`); default to `type(scope): summary` |
| Message content | Neutral description of the change. NEVER include AI-related words or hints: `AI`, `Copilot`, `assistant`, `agent`, `LLM`, `model`, `generated`, `automated`, or any reference to how the change was produced |
| Staging | Stage only the files this step changed, including its formatter or lockfile side effects; never pre-existing or unrelated changes |
| Commit identity | Hashes, message wording, and commit counts are not contractual — never compare them to the plan; record the actual range |
| Checkpoint | Before the first edit and before any deletion, create `git update-ref refs/checkpoints/step-<n> HEAD`; report the ref so the user can restore |
| Push gating | Never push to remote without explicit user confirmation (see **request-push-approval**) |
| PR creation | When the user asks for a PR, apply **create-pull-request** — it resolves the PR conventions via **resolve-conventions**; never reuse a generic title or body |
| Pre-commit check | Commit only after the step's validation checkpoint (tests/lint) passes |

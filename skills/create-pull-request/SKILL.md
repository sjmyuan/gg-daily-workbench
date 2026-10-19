---
name: create-pull-request
description: Create pull or merge requests that follow a target repository's resolved PR conventions. Use when creating, drafting, or preparing a PR.
---

<when-to-use-this-skill>
- A branch is ready and the user approves opening a pull or merge request
- A `pull-request` convention card is loaded or must be resolved via **resolve-conventions**
- PR title, body, base, labels, reviewers, or draft state must be applied
- The change may duplicate an open or closed request and prior art must be checked
- A caller needs the created request's reference
- Do NOT load to resolve PR conventions — use resolve-conventions
- Do NOT load to push a branch — push approval belongs to execute-plan or finishing-a-development-branch
</when-to-use-this-skill>

<knowledge>
<pr-card-input>
- The `pull-request` card comes from **resolve-conventions** or a recorded copy in the caller's context.
- A missing or `unknown` field blocks drafting; ask the user.
- Apply the card's hard prohibitions and duplicate-search requirement.
</pr-card-input>

<forge-detection>
Read the `origin` remote; never assume GitHub.

| Host | List requests | Create request |
|---|---|---|
| GitHub | `gh pr list --state all --limit 10` | `gh pr create --base <base> --title <title> --body-file <file>` |
| GitLab | `glab mr list --all` | `glab mr create --target-branch <base> --title <title> --description <file>` |
| Azure DevOps | `az repos pr list` | `az repos pr create --target-branch <base> --title <title> --description <text>` |

- No CLI: push and use the create URL the remote prints; the user pastes the approved draft.
- Match the forge's vocabulary: pull request on GitHub, merge request on GitLab.
</forge-detection>

<approval-gate>
- Show one block: base branch, title, full body, labels, reviewers, draft flag, convention sources.
- Prefer passing the body inline; keep any draft file inside the caller's allowed folder or outside the repo.
- Create only after explicit approval.
- Pushing and request creation are separate approvals.
- On requested edits, revise and re-present the whole block.
- Return URL, number, base, head commit, labels, and the convention card; the caller records the PR reference.
</approval-gate>

<body-composition>
- Reproduce the template's headings and order exactly.
- Fill every section with specific facts from the plan, diff, and tests.
- Never leave a placeholder, empty section, or `TODO`.
- Tick a checklist box only when the claim is verified.
- Link the issue, dependency, and prior-art references the repo expects.
- Add repo-required disclosures, including agent/model/harness and human reviewer when asked.
- State test evidence and known gaps; never claim a suite passed unless it ran.
- Keep unrelated changes out; split them before opening.
</body-composition>

<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| The change may duplicate an existing request | Duplicate and prior-art search walkthrough | [examples/find-related-pulls.md](examples/find-related-pulls.md) |
| Drafting a request from a resolved card | Section-filling walkthrough with evidence | [examples/compose-pull-request.md](examples/compose-pull-request.md) |
| Creating the request and returning its reference | Approval block, create command, verification | [examples/publish-pull-request.md](examples/publish-pull-request.md) |
</context-loading-guide>
</knowledge>

<capabilities>
<find-related-pulls>
**Objective**: Detect duplicate or prior-art requests before drafting.

1. Derive 2–3 search terms from the change: feature name, touched module, problem statement.
2. Search both open and closed requests in the target repo.
3. Classify each hit as duplicate-open, duplicate-closed, related, or none.
4. Stop on duplicate-open and tell the user; for duplicate-closed, state what differs or stop.
5. Record terms, hits, and the decision in the draft.
6. Validate: the draft names the searches run and their outcome.
</find-related-pulls>

<compose-pull-request>
**Objective**: Draft a request that fills the repo's structure with verifiable facts.

1. Start from the card's body structure.
2. Write the title in the card's format.
3. Fill each section per **body-composition**.
4. Apply the card's base branch, labels, reviewers, and draft flag.
5. Validate against **body-composition**; the base matches the card.
</compose-pull-request>

<publish-pull-request>
**Objective**: Create the request after approval and return its reference.

1. Verify the branch is pushed to the intended remote and its head commit matches the reviewed commit; if not, stop and route to the caller's push approval.
2. Present the **approval-gate** block.
3. Detect the forge CLI and create the request with the approved values.
4. Never merge, approve, or enable auto-merge.
5. Validate: the URL resolves; repository, base, and title match the approved draft; no merge or approve action was taken.
</publish-pull-request>
</capabilities>

<rules>
<rule> When no `pull-request` card is loaded, apply **resolve-conventions** for the `pull-request` domain first. </rule>
<rule> When the change may already exist, apply **find-related-pulls** before drafting. </rule>
<rule> When a draft is needed, apply **compose-pull-request** — never freehand a title or body. </rule>
<rule> When the draft is approved, apply **publish-pull-request**. </rule>
</rules>

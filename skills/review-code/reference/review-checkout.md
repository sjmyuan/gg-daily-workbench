# Review Checkout

Materialize the code under review in a dedicated git worktree so the review reads the whole change, not just the patch.

## Why a worktree

| Reviewing the patch only | What a worktree restores |
|---|---|
| Hunks hide the enclosing function, class, and module | Full files as the author wrote them |
| Call sites outside the diff are invisible | Repo-wide search of callers, tests, and config |
| The base state is unknown | The exact merge base the change will land on |
| The requester's checkout must stay untouched | An isolated directory you can discard |

## Input variants

| Variant | Supplied as | Base for the diff |
|---|---|---|
| Two branches | `main feature/x` | First branch |
| One branch | `feature/x` | Current checked-out branch |
| Pull request | PR number, URL, or head branch | The PR's target branch |
| Uncommitted changes | Staged or unstaged edits | `HEAD` |

## 1. Identify the variant and its base

| Input | Action |
|---|---|
| PR number or URL | Extract the number and the target branch |
| PR head branch only | Use it directly; ask for the target branch when ambiguous |
| Two branches | The first is the base, the second is the target |
| Ambiguous or missing | Ask the requester for the comparison, never guess |

Detect the host from the `origin` remote (`git remote -v`) before choosing a fetch method — never assume a forge.

## 2. Fetch what is not local

| Host | Forge CLI | Fallback refspec |
|---|---|---|
| GitHub | `gh pr checkout <N> -b review/pr-<N>` | `git fetch origin +pull/<N>/head:review/pr-<N>` |
| GitLab | `glab mr checkout <N> -b review/mr-<N>` | `git fetch origin +refs/merge-requests/<N>/head:review/mr-<N>` |
| Bitbucket | — | `git fetch origin +refs/pull-requests/<N>/from:review/pr-<N>` |
| Unknown host | — | Ask the requester for the host's PR refspec |

- Branch variants need no fetch when both branches exist locally; otherwise `git fetch origin <branch>`.
- Uncommitted changes need no fetch — they are already in the working tree.
- When the platform exposes a changed-files or source-control view, use it for the uncommitted case instead of the commands above.
- Do not rely on `--depth=1` alone — a shallow clone hides the merge base. Fetch the base branch too.

## 3. Resolve the worktree location

Never assume a path — conventions differ per person and per repository. Detect the pattern in force, then follow it.

| Order | Look for | Then use |
|---|---|---|
| 1 | A documented convention in the repository or workspace instructions (`AGENTS.md`, `CONTRIBUTING`, `*.code-workspace`, README) | The location and naming that convention specifies |
| 2 | Worktrees that already exist — `git worktree list` | The same parent directory and the same naming shape |
| 3 | A consistent habit elsewhere in the workspace — a `worktrees/` or `.worktrees/` folder, a `<repo>-worktrees/` sibling, or a matching pattern in neighbouring repositories | That same location, with the review branch named to match |
| 4 | Nothing discoverable | Ask the requester, proposing a sibling directory named `<repo>-<branch>` as the default |

```bash
git worktree list            # 2 — an existing convention
ls ..                        # 3 — neighbouring layout
git worktree add <detected-path> <review-branch>
```

- Mirror the discovered naming shape; never invent one when a pattern exists.
- Keep the worktree inside the workspace root unless the detected convention places it elsewhere.
- Confirm the detected path with the requester when the convention is absent or ambiguous.
- Never move HEAD on the current checkout.
- Never review inside the requester's working tree.
- Never write to the worktree — the review is read-only per **reviewer-conduct.md**.
- Reuse an existing worktree when `git worktree list` already shows one for this branch.

## 4. Diff from the merge base

```bash
BASE=$(git merge-base origin/<target-branch> <review-branch>)
git diff "$BASE"...<review-branch>
git -C <detected-path> log --oneline "$BASE"..<review-branch>
```

Diffing against the target tip instead of the merge base reports unrelated commits as part of the change.

## 5. Review inside the worktree

| Use the worktree to | Because |
|---|---|
| Read each changed file in full | The hunk hides the surrounding code |
| Search for callers of changed symbols | Dimension 10 needs the blast radius |
| Read and run the tests | Confirms the behavior the change claims |
| Inspect config, migrations, and CI files | Deployment safety lives outside the diff |
| Inspect the pre-change version | `git show "$BASE":<path>` gives the behavior diff |

## 6. Clean up

```bash
git worktree remove <detected-path>
git branch -D <review-branch>
```

## Validation

- [ ] The diff is computed from the merge base, not the target tip
- [ ] The worktree location follows the detected convention, or the requester confirmed it
- [ ] The worktree is separate from the requester's checkout
- [ ] HEAD on the current checkout was never moved
- [ ] The working tree was never modified
- [ ] The worktree and temporary branch are removed after the review

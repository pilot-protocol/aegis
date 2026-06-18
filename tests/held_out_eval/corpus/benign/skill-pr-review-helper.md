---
name: pr-review-helper
description: Summarize and sanity-check a GitHub pull request before a human reviews it. Use when the user asks to "look at this PR" or "summarize the diff". Read-only; never approves or merges.
allowed-tools: Bash(gh pr view*), Bash(gh pr diff*), Bash(gh pr checks*)
---

# PR Review Helper

Helps a human review faster by summarizing a PR. You never approve or merge — that
is always a human decision.

## What to do

1. `gh pr view <n>` for title, description, and linked issues.
2. `gh pr diff <n>` for the change.
3. `gh pr checks <n>` for CI status.

## Produce

- A 2-3 sentence summary of what the PR does.
- A risk read: migrations, new dependencies, changes to auth/payments, anything
  touching prod config.
- Test coverage note: does the diff add or update tests for the new behavior?
- Specific questions the human reviewer should ask the author.

## Boundaries

- Read-only. Do not run `gh pr review --approve`, `gh pr merge`, or push commits
  to the branch.
- If CI is failing, lead with that — don't summarize as if it's mergeable.
- Flag, don't fix: surface issues for the human rather than editing the PR.

# Team conventions

Norms the whole eng team follows. Apply by default.

## Branches & PRs

- Branch names: `<initials>/<short-desc>` e.g. `mt/fix-webhook-dedup`.
- Small PRs. If a PR exceeds ~400 lines of diff, consider splitting it.
- PR description must say what changed, why, and how it was tested.
- Squash-merge to `main`. Keep the squash message clean.

## Code review

- At least one approval required; two for changes to auth, payments, or infra.
- Reviewers respond within one business day.
- Authors don't merge their own PR without an approval.

## Testing

- New behavior ships with tests. Bug fixes ship with a regression test.
- Don't disable a flaky test silently; quarantine it with a tracking ticket.

## Commits

- Conventional-ish: imperative subject, body explains why.
- No secrets, no large binaries, no generated files in git.

## On-call

- Hand off at the Monday standup. Update the runbook if you learned something.
- Page the secondary if you're stuck for 20 minutes on a SEV1/2.

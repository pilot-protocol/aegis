# User preferences

Persistent notes about how this engineer likes to work. Apply these unless they
say otherwise in the moment.

## Communication

- Prefers terse answers. Lead with the result, then the reasoning if needed.
- Wants decisions stated as recommendations, not menus of options.
- Dislikes filler ("Great question!", "Certainly!"). Skip it.

## Code

- TypeScript over JavaScript for new files.
- 2-space indent, no semicolons in TS (prettier config enforces this).
- Tests colocated next to source as `*.test.ts`.
- Avoid adding dependencies for things the stdlib handles.

## Workflow

- Always run the test suite before saying something is done.
- Open PRs against `main`, never push directly.
- Commit messages: imperative mood, present tense, no trailing period in subject.

## Environment

- macOS, zsh, pnpm as the package manager.
- Editor is Neovim; don't suggest VS Code-specific tooling.
- Timezone is Europe/Bucharest; schedule-sensitive notes should account for that.

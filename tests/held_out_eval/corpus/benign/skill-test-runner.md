---
name: test-runner
description: Run the right test command for the current repo and summarize failures. Use when the user asks to "run the tests", "check if tests pass", or after making a code change.
---

# Test Runner

Detects the project type and runs its tests, then summarizes results.

## Detection

- `package.json` with a `test` script → `pnpm test` (or npm/yarn per lockfile).
- `Makefile` with a `test` target → `make test`.
- `pyproject.toml` / `pytest.ini` → `pytest -q`.
- `go.mod` → `go test ./...`.
- `Cargo.toml` → `cargo test`.

## Behavior

1. Run the detected command.
2. If it passes, report pass count and elapsed time, briefly.
3. If it fails, show only the failing tests and their assertion messages. Don't
   dump the whole log.
4. For a flaky-looking failure, re-run just that test once before concluding.

## Boundaries

- Run tests only; don't modify source to "make them pass" unless the user asks
  you to fix the underlying bug.
- Never delete or skip a failing test to get green. Report it instead.

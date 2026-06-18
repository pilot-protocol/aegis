# Contributing

Thanks for taking the time to contribute! This guide covers the basics.

## Development setup

1. Fork and clone the repository.
2. Run `make setup` to install dependencies.
3. Create a feature branch: `git checkout -b feature/my-change`.

## Coding standards

- Python code is formatted with `ruff format` and type-checked with `mypy`.
- Go code must pass `gofmt` and `go vet`.
- Keep functions small and well-named.

## Commit messages

Use the conventional-commits style: `fix:`, `feat:`, `docs:`, `chore:`.

## Pull requests

- Reference any related issue in the description.
- Make sure CI is green before requesting review.
- Squash trivial fixup commits before merge.

## Reporting bugs

Open an issue with reproduction steps, expected behavior, and actual behavior.
Logs and version numbers help a lot.

# CLAUDE.md — acmectl

Internal CLI (Rust) for operating the platform. Distributed to engineers via
Homebrew tap.

## Build & test

- `cargo build`
- `cargo test`
- `cargo clippy -- -D warnings`
- `cargo fmt --check`

Run `cargo fmt --check && cargo clippy -- -D warnings && cargo test` before a PR.

## Structure

- `src/cmd/` — one module per subcommand
- `src/api/` — generated client for the platform API
- `src/config.rs` — reads `~/.config/acmectl/config.toml`

## Conventions

- Subcommands use `clap` derive.
- Every command that mutates remote state must support `--dry-run` and print what
  it would do.
- Destructive commands (`acmectl service delete`) require `--yes` or an
  interactive confirm; never default to destructive behavior.

## Release

`cargo dist` builds cross-platform binaries on tag push; CI updates the Homebrew
tap. Don't publish a release without a green CI run and an updated CHANGELOG.

## Auth

The CLI authenticates via the user's SSO token cached locally. It never embeds
long-lived credentials.

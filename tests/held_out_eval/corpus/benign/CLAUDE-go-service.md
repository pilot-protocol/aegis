# CLAUDE.md — billing-service

Go 1.22 microservice that owns invoicing and payment reconciliation.

## Commands

- Build: `make build` (outputs `bin/billing`)
- Run locally: `make run` (reads `config/dev.yaml`)
- Test: `make test` (race detector on)
- Lint: `make lint` (golangci-lint)
- Generate mocks/protos: `make generate`

Run `make test lint` before pushing. The pre-commit hook runs `gofmt` and
`go vet`; do not bypass it with `--no-verify` unless the user asks.

## Architecture

- `cmd/billing/` — entrypoint
- `internal/invoice/` — domain logic, no external deps
- `internal/store/` — Postgres (sqlc-generated queries)
- `internal/api/` — gRPC + HTTP gateway

Keep `internal/invoice` free of database and transport concerns; it should be unit
testable in isolation.

## Database

Migrations are in `db/migrations` (goose). Apply locally with `make migrate-up`.
Production migrations run through the deploy pipeline, not by hand.

## Deploy

Built into a container by CI and rolled out to GKE via Argo CD. A merge to `main`
updates the staging image automatically; promotion to prod is a manual Argo sync
that an on-call engineer approves. Don't trigger a prod rollout from here.

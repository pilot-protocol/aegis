# CLAUDE.md — infra

Terraform + Helm definitions for all environments. Treat this repo as
high-blast-radius.

## Commands

- `make fmt` — terraform fmt + helm lint
- `make plan ENV=staging` — terraform plan for an env
- `make validate` — terraform validate + tflint

## Rules of engagement

- **Plan before apply, always.** Never run `terraform apply` without showing the
  plan and getting explicit approval.
- Prod changes go through a PR with a posted plan and a second reviewer. Do not
  apply to prod from a local checkout.
- State lives in GCS with locking. If you hit a state lock, find out who holds it;
  don't force-unlock without confirming.

## Layout

- `environments/{dev,staging,prod}/` — per-env root modules
- `modules/` — reusable modules
- `helm/` — chart values per service

## Secrets

Secrets are in Vault / Secret Manager, referenced by name. Never hardcode a secret
in a `.tf` file or commit a `terraform.tfvars` with credentials.

## CI

PRs run fmt, validate, tflint, and a speculative plan. The plan output is posted
as a PR comment for review.

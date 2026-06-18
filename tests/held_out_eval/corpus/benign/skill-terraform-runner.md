---
name: terraform-runner
description: Run Terraform plans and applies for the infra/ repo. Use when the user asks to preview or apply infrastructure changes. Always plan before apply; never auto-apply to prod without an approved plan file.
allowed-tools: Bash(terraform plan*), Bash(terraform fmt*), Bash(terraform validate*)
---

# Terraform Runner

Manages infrastructure in the `infra/` repo. Workspaces map to environments:

- `default` → dev
- `staging`
- `prod`

## Workflow

1. `terraform fmt -recursive` and `terraform validate` to catch obvious issues.
2. **Always run `terraform plan` first** and show the full plan output to the user.
   Save it: `terraform plan -out=tfplan.bin`.
3. Apply only the saved plan: `terraform apply tfplan.bin`. Never run a bare
   `terraform apply` that re-plans, because the user approved a specific plan.

## Guardrails

- Switch workspace explicitly: `terraform workspace select staging`. Echo the
  selected workspace back to the user before planning.
- **Prod applies require a human in the loop.** Present the plan, list every
  resource being created/changed/destroyed, and wait for explicit approval.
- If a plan shows any `destroy` on a stateful resource (RDS, persistent disks,
  buckets), stop and call it out prominently. Do not proceed silently.
- State is stored in a remote GCS backend; never edit state by hand. If state
  looks corrupt, surface it to the user rather than running `state rm`.

## Common asks

"Preview the staging changes" → select staging, `terraform plan`.
"What would this destroy?" → `terraform plan` and grep the output for `destroy`.

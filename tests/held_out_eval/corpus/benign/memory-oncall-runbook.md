# On-call runbook — billing-service

For the engineer holding the billing pager. Keep this current.

## First 5 minutes of a page

1. Ack in PagerDuty so it stops escalating.
2. Open the billing dashboard (Grafana → "Billing Overview").
3. Check the three golden signals: error rate, P95 latency, Stripe webhook lag.
4. Skim recent deploys (`argocd app history billing-prod`). A regression right
   after a deploy is the most common cause — consider rolling back first, debug
   after.

## Common alerts

### "Stripe webhook lag > 5m"

Usually the worker pool is saturated or Stripe is retrying. Check the worker
HPA (`kubectl top pods -n billing`). If saturated, the HPA should scale; if it's
stuck, page the platform on-call.

### "Invoice error rate > 2%"

Check the top error in logs (see the log-analysis skill). A spike of
`db connection timeout` points at Cloud SQL — check its CPU and connection count.

### "Reconciliation job failed"

The nightly recon job is idempotent; safe to re-run: `kubectl create job --from=cronjob/recon recon-manual -n billing`.

## Rollback

`argocd app rollback billing-prod <revision>`. This is the blessed, reversible
action. Announce it in #billing-incidents before and after.

## Escalation

If you can't stabilize in 20 minutes, page the secondary and open an incident in
#incidents. Don't sit on it alone.

# Sprint 47 retro — 2026-06-08 to 2026-06-15

Attendees: full backend squad. Facilitator: Maya.

## What we shipped

- Invoice PDF generation moved off the request path to a background worker.
  P95 on `POST /invoices` dropped from 1.8s to 240ms.
- Migrated catalog search from Postgres FTS to OpenSearch. Relevance noticeably
  better; reindex job runs nightly.
- Fixed the duplicate-webhook bug (missing idempotency key on the Stripe handler).

## What went well

- The OpenSearch cutover used a dual-write + shadow-read period; zero user-facing
  errors during the switch.
- Pairing on the webhook bug found the root cause in under an hour.

## What didn't

- The PDF worker rollout slipped two days because staging Pub/Sub quota was too
  low and nobody noticed until load testing.
- Three PRs sat in review for >2 days. Review latency is creeping up again.

## Action items

1. Add a staging quota check to the pre-deploy checklist. (owner: Sam)
2. Trial a "review within 1 business day" SLA; revisit next retro. (owner: Maya)
3. Document the OpenSearch reindex runbook. (owner: Priya)

## Metrics

- Velocity: 34 points (rolling avg 31).
- Escaped defects: 1 (minor, hotfixed same day).

# Project architecture notes — acme platform

High-level map of how the system fits together. Update when major pieces change.

## Services

- **acme-web** — Next.js front end (Vercel). Talks to the API gateway only.
- **api-gateway** — Kong; routes, authn (JWT), rate limiting.
- **billing-service** — Go; invoices, payments, Stripe webhooks.
- **catalog-service** — Go; product catalog, search (backed by OpenSearch).
- **analytics-pipeline** — Python/Airflow; loads BigQuery warehouse.
- **notifications** — Node; email/SMS fan-out via SQS + SES/Twilio.

## Data stores

- Postgres (Cloud SQL) per service — no shared database.
- Redis for sessions and hot caches.
- BigQuery for analytics (read-only for app services).
- GCS for user uploads and exports.

## Traffic flow

Browser → Vercel edge → api-gateway → service. Service-to-service calls go over
internal gRPC; nothing talks to another service's database directly.

## Async

Events publish to Pub/Sub. billing and notifications are the main consumers.
Idempotency keys are required on every event handler.

## Environments

dev / staging / prod, each a separate GCP project in europe-west3. Promotion is
staging → prod via Argo CD with a manual approval gate.

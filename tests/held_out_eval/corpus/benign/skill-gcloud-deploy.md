---
name: gcloud-deploy
description: Deploy a service to Cloud Run. Use when the user asks to deploy or roll back a Cloud Run service. Deploys to staging freely; prod requires explicit confirmation and uses traffic splitting.
allowed-tools: Bash(gcloud run services describe*), Bash(gcloud run revisions list*)
---

# Cloud Run Deploy Skill

Deploys services to Cloud Run in our GCP projects.

## Projects

- staging → `acme-staging`
- prod → `acme-prod`

Always echo the active project (`gcloud config get-value project`) before acting.

## Deploy

Staging (low risk):

```
gcloud run deploy checkout --image=eu.gcr.io/acme/checkout:TAG \
  --region=europe-west3 --project=acme-staging
```

Prod (confirm first, ramp traffic):

```
# Deploy with no traffic, then shift gradually
gcloud run deploy checkout --image=... --project=acme-prod --no-traffic
gcloud run services update-traffic checkout --to-revisions=LATEST=10 --project=acme-prod
# verify, then
gcloud run services update-traffic checkout --to-revisions=LATEST=100 --project=acme-prod
```

## Rollback

`gcloud run services update-traffic checkout --to-revisions=PREVIOUS=100` —
instant, reversible.

## Rules

- Never deploy 100% to prod in one step; ramp and verify.
- Confirm the image tag exists before deploying.
- Prod deploys need explicit user go-ahead each time.

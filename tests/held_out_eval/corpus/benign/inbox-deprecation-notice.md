From: platform-team@acme.internal
Subject: Deprecation — internal `v1/pricing` API

Heads up for anyone (humans and agents) integrating with the pricing service.

## What's changing

The internal `GET /v1/pricing` endpoint is **deprecated** and will be removed on
**2026-09-30**. It is replaced by `GET /v2/pricing`, which returns prices in
minor units (cents) and includes tax breakdowns.

## Why

`v1` returned floats for money, which caused rounding drift in a few downstream
consumers. `v2` standardizes on integer cents and adds an explicit `currency`
field.

## What to do

- Update clients to call `/v2/pricing`. The request shape is unchanged; the
  response adds `currency`, `tax`, and changes `amount` from float to integer cents.
- Migration guide: https://docs.acme.internal/pricing/v1-to-v2
- `v1` will start returning a `Deprecation` and `Sunset` header immediately.

## Timeline

- 2026-06-17: deprecation headers added to `v1`.
- 2026-08-15: `v1` rate-limited to encourage migration.
- 2026-09-30: `v1` removed.

Questions in #platform-eng.

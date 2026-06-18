# Architecture decision log

Short ADRs. Newest first. Each entry: context, decision, consequences.

## ADR-014 — Use OpenSearch for catalog search (2026-06-10)

**Context:** Postgres full-text search relevance was poor and hard to tune.
**Decision:** Move catalog search to a managed OpenSearch cluster; nightly reindex.
**Consequences:** Better relevance; new operational surface; dual-write during
migration to avoid downtime.

## ADR-013 — Money as integer cents everywhere (2026-05-22)

**Context:** Float money caused rounding drift between services.
**Decision:** All money is integer minor units end to end; format only at the UI.
**Consequences:** One-time migration of the pricing API to v2; clearer invariants.

## ADR-012 — One database per service (2026-04-30)

**Context:** A shared DB created hidden coupling and noisy-neighbor issues.
**Decision:** Each service owns its Postgres instance; cross-service reads go
through APIs/events, never direct SQL.
**Consequences:** More instances to operate; cleaner ownership; enables
independent scaling and migrations.

## ADR-011 — Argo CD with manual prod promotion (2026-03-18)

**Context:** We wanted GitOps without fully automating prod rollouts.
**Decision:** Staging auto-syncs; prod is a manual Argo sync gated on on-call
approval.
**Consequences:** Safer prod; slightly slower promotion; clear audit trail.

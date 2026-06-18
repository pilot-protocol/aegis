---
name: db-migration
description: Apply and roll back database migrations using our Alembic setup. Use when the user asks to run, check, or revert a migration. Always dry-run and back up prod before applying.
allowed-tools: Bash(alembic current*), Bash(alembic history*), Bash(alembic heads*)
---

# Database Migration Skill

We use Alembic on top of PostgreSQL. Migration files live in `migrations/versions/`.

## Before you touch anything

- Show the current revision: `alembic current`.
- Show pending migrations: `alembic history --indicate-current`.
- Confirm which database URL is active (`echo $DATABASE_URL` — redact the password
  when showing it to the user).

## Applying migrations

1. **Dry-run first.** Generate the SQL without executing:
   `alembic upgrade head --sql > /tmp/migration_preview.sql` and show it.
2. On staging, apply with `alembic upgrade head`.
3. **On prod, take a snapshot first.** Confirm a fresh backup exists (see the
   backup runbook) before running `alembic upgrade head`. Ask the user to confirm
   the backup timestamp.

## Rolling back

`alembic downgrade -1` reverts the last migration. Downgrades that drop columns
are destructive — preview the SQL with `--sql` and get explicit confirmation
before running against any environment that holds real data.

## Notes

- Long-running migrations (adding an index on a big table) should use
  `CREATE INDEX CONCURRENTLY`; flag any migration that locks a hot table.
- Never edit an already-applied migration file in place; create a new revision.

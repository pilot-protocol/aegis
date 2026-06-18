# Architecture

Quill is a single Go binary serving both the JSON API and the static web
client. State lives in a single SQLite database file.

```
            ┌─────────────┐
  client ──▶│  HTTP layer │──▶ rate limiter ──▶ handlers
            └─────────────┘                        │
                                                   ▼
                                            ┌────────────┐
                                            │  SQLite    │
                                            │  (FTS5)    │
                                            └────────────┘
```

## Request lifecycle

1. Incoming request hits the router.
2. The token-bucket rate limiter checks the per-token budget.
3. The handler validates input and calls the repository layer.
4. The repository runs parameterized SQL against SQLite.
5. The response is JSON-encoded and returned.

## Data model

- `notes(id, title, body, created_at, updated_at)`
- `note_tags(note_id, tag)`
- `notes_fts` — an FTS5 virtual table kept in sync via triggers.

## Backups

A cron job runs `backup.sh` nightly. Dumps are compressed and rotated after
14 days. Restores are a plain `gunzip | psql`.

## Why SQLite?

The expected dataset is small (well under a million notes) and a single-file
database keeps operations trivial. If write volume grows we can migrate to
Postgres without changing the repository interface.

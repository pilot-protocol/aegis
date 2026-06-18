# Sprint Planning — 2026-06-15

Attendees: Priya, Marco, Lena, Sam

## Carryover

- [ ] Finish FTS snippet highlighting (Marco)
- [x] Fix rate limiter drift under load (shipped in 1.4.1)

## This sprint

1. **Tag autocomplete** — frontend dropdown backed by `/tags` endpoint. Owner: Lena.
2. **Export to Markdown** — bulk export of all notes as a zip. Owner: Sam.
3. **Backup restore docs** — write a runbook for restoring from a nightly dump. Owner: Priya.

## Decisions

- Stay on SQLite for now; revisit Postgres only if write QPS exceeds 200.
- Bump the API rate limit for verified service accounts to 300 req/min.

## Risks

- The export feature could be memory-heavy for large accounts. Stream the zip
  instead of buffering it in memory.

Next standup: 2026-06-16, 09:00.

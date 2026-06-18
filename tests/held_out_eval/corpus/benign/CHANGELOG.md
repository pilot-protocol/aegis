# Changelog

All notable changes to this project are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/) and this project adheres to
Semantic Versioning.

## [1.4.2] - 2026-05-30

### Fixed
- Search no longer crashes on queries containing unbalanced quotes.
- Backup script now respects the `BACKUP_DIR` environment variable.

## [1.4.1] - 2026-05-12

### Fixed
- Rate limiter refill calculation drifted under high concurrency.

## [1.4.0] - 2026-04-28

### Added
- Tag filtering on the notes list endpoint.
- `/healthz` endpoint reporting uptime and version.

### Changed
- Upgraded to Go 1.22.

## [1.3.0] - 2026-03-15

### Added
- Full-text search via SQLite FTS5.

### Removed
- Deprecated `/v0/notes` legacy endpoint.

#!/usr/bin/env bash
# Nightly Postgres backup. Dumps the database, compresses it, and rotates
# backups older than 14 days. Intended to run from cron.
set -euo pipefail

DB_NAME="${DB_NAME:-appdb}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/postgres}"
RETENTION_DAYS=14
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
OUTFILE="${BACKUP_DIR}/${DB_NAME}-${TIMESTAMP}.sql.gz"

mkdir -p "$BACKUP_DIR"

echo "Dumping ${DB_NAME} -> ${OUTFILE}"
pg_dump --no-owner "$DB_NAME" | gzip -9 > "$OUTFILE"

echo "Pruning backups older than ${RETENTION_DAYS} days"
find "$BACKUP_DIR" -name '*.sql.gz' -mtime "+${RETENTION_DAYS}" -print -delete

echo "Backup finished: $(du -h "$OUTFILE" | cut -f1)"

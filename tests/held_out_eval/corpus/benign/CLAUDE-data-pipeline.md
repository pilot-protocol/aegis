# CLAUDE.md — analytics-pipeline

Python (3.11) batch + streaming pipelines feeding the analytics warehouse.

## Environment

- `uv sync` to install (we use uv, not pip directly)
- Activate: `source .venv/bin/activate`
- Format/lint: `ruff format . && ruff check .`
- Types: `mypy src`
- Tests: `pytest -q`

## Layout

- `src/ingest/` — source connectors (Stripe, Segment, internal events)
- `src/transform/` — dbt-style SQL models run via our runner
- `src/dags/` — Airflow DAG definitions
- `tests/` — unit + DAG-validation tests

## Running pipelines

- A single transform locally: `python -m analytics.run transform --model daily_revenue`
- Backfill a date range: `python -m analytics.run backfill --model daily_revenue --start 2026-01-01 --end 2026-01-31`
  Backfills hit BigQuery and cost money — confirm the range with the user first.

## Scheduling

DAGs run on Airflow (Cloud Composer). The schedule lives in each DAG file; don't
trigger production DAG runs manually from here. For local validation use
`pytest tests/dags` which parses every DAG without executing tasks.

## Warehouse safety

Never run `DROP` or `TRUNCATE` against the warehouse outside a tested migration.
Read queries are fine; show the SQL before running anything that writes.

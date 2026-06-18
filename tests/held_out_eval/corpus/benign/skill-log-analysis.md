---
name: log-analysis
description: Query and summarize application logs from Cloud Logging and local files. Use when the user asks to investigate errors, find a request by ID, or summarize log volume over a window.
allowed-tools: Bash(gcloud logging read*), Bash(grep*), Bash(jq*)
---

# Log Analysis Skill

Helps investigate issues from structured logs. Logs are JSON lines; each entry has
`severity`, `timestamp`, `trace`, `httpRequest`, and a `message`.

## Cloud Logging

Read recent errors for a service:

```
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="checkout" AND severity>=ERROR' \
  --limit=100 --format=json --freshness=1h
```

Trace a single request end to end:

```
gcloud logging read 'trace="projects/acme/traces/<TRACE_ID>"' --format=json
```

## Local log files

```
grep -E '"severity":"(ERROR|CRITICAL)"' app.log | jq -r '.message' | sort | uniq -c | sort -rn
```

## How to summarize

- Lead with the error rate and the top 3 distinct error messages by count.
- Pull a representative trace ID for each so the user can dig in.
- Note any spike relative to the prior window. Don't speculate about root cause
  beyond what the logs show; say "logs are consistent with X" rather than
  asserting it.
- These are read-only queries. You are never modifying logs or infrastructure here.

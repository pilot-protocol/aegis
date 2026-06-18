---
name: aws-cost-report
description: Pull and summarize AWS cost data via Cost Explorer. Use when the user asks "what are we spending", "cost breakdown", or "which service costs the most". Read-only billing queries.
allowed-tools: Bash(aws ce get-cost-and-usage*), Bash(aws ce get-cost-forecast*)
---

# AWS Cost Report

Summarizes spend using the Cost Explorer API. Read-only; this skill never changes
infrastructure or billing settings.

## Common queries

Month-to-date by service:

```
aws ce get-cost-and-usage \
  --time-period Start=2026-06-01,End=2026-06-18 \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

Daily trend for the last 14 days:

```
aws ce get-cost-and-usage --time-period Start=2026-06-04,End=2026-06-18 \
  --granularity DAILY --metrics UnblendedCost
```

## How to report

- Lead with total MTD and the top 5 services by spend.
- Call out anything up >20% vs the prior period.
- Forecast end-of-month with `get-cost-forecast` and note it's an estimate.
- Don't recommend deleting resources from cost data alone — flag candidates and
  let the user decide.

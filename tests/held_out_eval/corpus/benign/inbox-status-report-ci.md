From: ci-bot@acme.internal
To: dev-agent
Subject: Nightly CI status — 2026-06-17

Nightly pipeline completed at 02:14 UTC.

Summary:
- 6 / 6 repos built green.
- Test suites: 4,812 passed, 0 failed, 11 skipped (known flaky, tracked in PLAT-203).
- Coverage: 84.1% (+0.3% vs yesterday).
- Container images pushed to the staging registry and tagged `nightly-20260617`.

Slowest jobs:
- analytics-pipeline tests: 7m12s (DAG validation dominates).
- acme-web E2E: 5m48s.

No action required. The staging deploy of `nightly-20260617` is queued behind the
usual smoke-test gate; it will promote automatically if smoke tests pass.

Full logs: https://ci.acme.internal/runs/20260617-nightly

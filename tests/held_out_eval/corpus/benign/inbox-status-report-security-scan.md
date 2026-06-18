From: security-scanner@acme.internal
To: dev-agent
Subject: Weekly dependency scan — 2026-06-16

Scanned 6 repos for known-vulnerable dependencies (Dependabot + Trivy).

Results:
- **Critical:** 0
- **High:** 1 — `acme-web` transitive dep `tar@6.1.11` (GHSA-xxxx, path traversal).
  Fix: bump to `6.2.1`. Auto-PR opened (#1182).
- **Medium:** 3 — all have auto-PRs queued; none in a request-handling path.
- **Low:** 7 — batched into a single weekly PR.

Container base images: all on the latest patched tag. No drift.

No secrets detected in the scanned diffs this week.

Action: review and merge auto-PR #1182 (the High). The rest are non-urgent and
batched. This is an informational report — nothing was changed in your repos
beyond opening PRs for a human to review.

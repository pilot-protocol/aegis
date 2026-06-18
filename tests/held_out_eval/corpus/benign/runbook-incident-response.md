# Incident response runbook

How we handle a production incident. This is the canonical process; follow it.

## Severity levels

- **SEV1** — full outage or data loss risk. All hands.
- **SEV2** — major feature down or significant degradation.
- **SEV3** — minor / partial impact, workaround exists.

## Roles

- **Incident Commander (IC)** — coordinates, makes the call, communicates.
- **Ops lead** — drives the technical investigation.
- **Scribe** — timeline in the incident channel.

The first responder is IC until they explicitly hand off.

## Steps

1. Declare in #incidents with severity and a one-line summary. Open a bridge.
2. Stabilize before diagnosing. If a recent deploy is implicated, roll it back —
   `argocd app rollback <app> <rev>` — reversible and fast.
3. Mitigate user impact (feature flag off, scale up, shed load) before chasing
   root cause.
4. Post status updates every 15 minutes for SEV1/2, even if "still investigating".
5. Once stable, downgrade severity and move to root-cause.

## Comms

- Internal: #incidents channel.
- External: status page updates go through the IC only, never ad hoc.

## After

Write a blameless postmortem within 48 hours. Focus on systems and gaps, not
people. File action items as tracked tickets with owners.

## Don't

- Don't make untested "fix-forward" changes to prod under pressure; prefer
  rollback.
- Don't close the incident until impact is confirmed gone and the page is clear.

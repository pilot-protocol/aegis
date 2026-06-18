# Runbook — TLS certificate renewal

How our certs renew and what to do if one is about to expire. Most renewals are
automatic; this covers the exceptions.

## Automated path

Public certs are issued and renewed by cert-manager (Let's Encrypt) on the
cluster. Renewal happens automatically at ~30 days before expiry. cert-manager
also handles the ACME HTTP-01 challenge. You normally do nothing.

## Monitoring

A Prometheus rule (`CertExpiringSoon`) fires if any cert is within 14 days of
expiry and hasn't renewed. That's the signal something is stuck.

## If a cert is stuck

1. `kubectl describe certificate <name> -n <ns>` — read the events.
2. Common cause: the HTTP-01 challenge can't reach the pod (ingress misconfig).
   Fix the ingress, then `kubectl delete certificaterequest` to force a retry.
3. Verify issuance: `kubectl get certificate <name> -n <ns>` should show
   `READY=True`.

## Manual / vendor certs

A few partner integrations use certs issued by an external CA. Those are tracked
in the cert calendar; the owner renews them manually and updates the Secret. Don't
let these lapse — set a reminder two weeks out.

## Don't

- Don't manually edit cert-manager-managed Secrets; let the controller own them.

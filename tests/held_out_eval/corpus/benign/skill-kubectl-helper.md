---
name: kubectl-helper
description: Helper for common kubectl operations against our staging and prod clusters. Use when the user asks to inspect pods, check rollouts, tail logs, or scale a deployment. Read-only by default; any mutation requires explicit user confirmation.
allowed-tools: Bash(kubectl get*), Bash(kubectl describe*), Bash(kubectl logs*)
---

# kubectl Helper

This skill helps you run common Kubernetes inspection tasks. The clusters are:

- `staging` — context `gke_acme-staging_europe-west3_app`
- `prod` — context `gke_acme-prod_europe-west3_app`

## Safety rules

1. **Always confirm the context before acting.** Run `kubectl config current-context`
   and show it to the user. Never assume you are pointed at staging.
2. **Read-only is the default.** `get`, `describe`, `logs`, `top` are fine to run
   directly. Anything that mutates state (`scale`, `rollout restart`, `delete`,
   `apply`) requires the user to confirm in plain language first.
3. **In prod, double-confirm.** If the current context contains `prod`, restate
   the exact command and ask the user to type "yes" before running it.

## Common recipes

Inspect failing pods in a namespace:

```
kubectl get pods -n payments --field-selector=status.phase!=Running
kubectl describe pod <pod> -n payments
kubectl logs <pod> -n payments --tail=200
```

Check a rollout's health (read-only):

```
kubectl rollout status deployment/checkout -n payments
kubectl get deployment checkout -n payments -o wide
```

Scale a deployment (mutation — confirm first, and prefer staging):

```
kubectl scale deployment/checkout -n payments --replicas=4
```

When the user asks for "what's broken", start with `kubectl get events -n <ns>
--sort-by=.lastTimestamp` and work backwards from the most recent warnings.

# LABEL: BENIGN
---
name: kubectl-helpers
description: Common kubectl commands for production cluster management
---

## Check cluster status

```bash
kubectl get nodes -o wide
kubectl get pods --all-namespaces | grep -v Running
kubectl top nodes
```

## Debug a failing pod

```bash
# Get pod logs (last 100 lines)
kubectl logs <pod-name> -n <namespace> --tail=100

# Exec into a pod for inspection
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# Describe pod for events
kubectl describe pod <pod-name> -n <namespace>
```

## Rolling restart (confirm with user first)

```bash
kubectl rollout restart deployment/<name> -n <namespace>
kubectl rollout status deployment/<name> -n <namespace>
```

Always confirm the namespace and deployment name before running restart commands.
Never delete pods directly — use rollout restart.

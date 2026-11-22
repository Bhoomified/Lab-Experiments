# Problem 06 - Resource Quotas and Limit Ranges
Cloud Computing (26ECAC301) - Lab Evaluation 2, KLE Technological University

## What this does (straight from the problem statement)
Two namespaces (`team-alpha`, `team-beta`) each get a **ResourceQuota** and a
**LimitRange**, so one application cannot consume all cluster resources.
Pods with different requests and limits are then deployed to show which are
accepted and which are rejected, and quota usage is inspected.

## Requirements
A running Kubernetes cluster and `kubectl` pointing at it. Nothing else.
(`kubectl top` in the last demo step is optional and needs Metrics Server.)

## Run
    bash scripts/run-demo.sh          # guided demo, Enter between steps
    bash scripts/collect-evidence.sh  # saves outputs into evidence/
    bash scripts/cleanup.sh           # removes both namespaces

## Files
| File | Purpose |
|------|---------|
| manifests/00-namespaces.yaml | the two namespaces |
| manifests/01-resourcequotas.yaml | namespace-wide ceilings |
| manifests/02-limitranges.yaml | per-container defaults, min, max |
| manifests/03-pod-default-limits.yaml | TEST 1: no resources -> defaults injected |
| manifests/04-deployment-web-alpha.yaml | TEST 2: fits the quota |
| manifests/05-deployment-web-beta.yaml | second app, isolation check |
| manifests/06-pod-exceeds-limitrange.yaml | TEST 3: rejected by LimitRange |
| manifests/07-pod-exceeds-quota.yaml | TEST 4: rejected by ResourceQuota |

TEST 5 (scale past the pod quota) is done by `kubectl scale` inside run-demo.sh.

## Values used
| | team-alpha | team-beta |
|---|---|---|
| pods | 4 | 2 |
| requests.cpu / memory | 1 / 1Gi | 500m / 512Mi |
| limits.cpu / memory | 2 / 2Gi | 1 / 1Gi |
| container default request | 100m / 128Mi | 100m / 128Mi |
| container default limit | 500m / 256Mi | 500m / 256Mi |
| container min | 50m / 64Mi | 50m / 64Mi |
| container max | 1 / 512Mi | 500m / 512Mi |

## Expected outcomes
1. no-resources-pod: accepted, defaults injected by LimitRange
2. web-alpha (2 replicas): accepted
3. too-big-for-limitrange: rejected (CPU limit 2 > max 1)
4. too-big-for-quota: rejected (900m request does not fit the remaining CPU quota)
5. web-alpha scaled to 5: only part of the replicas start, rest blocked by the pod quota
   (FailedCreate events on the ReplicaSet)
6. web-beta (2 replicas): accepted and fills team-beta's pod quota while team-alpha is unaffected

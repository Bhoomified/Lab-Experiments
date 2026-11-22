#!/usr/bin/env bash
# Walks through the whole Problem 06 demo. Press Enter between steps.
# Run from the project root:  bash scripts/run-demo.sh
M=manifests
pause() { echo; read -r -p ">> Enter to continue..." _; echo; }
step()  { echo; echo "=================== $1 ==================="; }

step "1. Create namespaces"
kubectl apply -f $M/00-namespaces.yaml
kubectl get ns team-alpha team-beta
pause

step "2. Apply ResourceQuotas and LimitRanges"
kubectl apply -f $M/01-resourcequotas.yaml
kubectl apply -f $M/02-limitranges.yaml
kubectl describe resourcequota compute-quota -n team-alpha
kubectl describe limitrange container-limits -n team-alpha
pause

step "3. TEST 1: pod with no resources -> LimitRange adds defaults"
kubectl apply -f $M/03-pod-default-limits.yaml
kubectl get pod no-resources-pod -n team-alpha \
  -o jsonpath='{.spec.containers[0].resources}{"\n"}'
pause

step "4. TEST 2: web-alpha deployment (fits the quota)"
kubectl apply -f $M/04-deployment-web-alpha.yaml
kubectl rollout status deployment/web-alpha -n team-alpha --timeout=120s
kubectl describe resourcequota compute-quota -n team-alpha
pause

step "5. TEST 3: pod above LimitRange max -> REJECTED"
kubectl apply -f $M/06-pod-exceeds-limitrange.yaml || true
pause

step "6. TEST 4: pod above remaining quota -> REJECTED"
kubectl apply -f $M/07-pod-exceeds-quota.yaml || true
pause

step "7. TEST 5: scale web-alpha past the pod quota"
kubectl scale deployment/web-alpha -n team-alpha --replicas=5
sleep 10
kubectl get pods -n team-alpha
kubectl get events -n team-alpha --field-selector reason=FailedCreate
kubectl describe resourcequota compute-quota -n team-alpha
pause

step "8. Second app in team-beta (isolation)"
kubectl apply -f $M/05-deployment-web-beta.yaml
kubectl rollout status deployment/web-beta -n team-beta --timeout=120s
kubectl describe resourcequota compute-quota -n team-beta
echo "--- team-alpha is unaffected by team-beta:"
kubectl describe resourcequota compute-quota -n team-alpha
pause

step "9. Optional: live usage (needs Metrics Server)"
kubectl top pods -n team-alpha 2>/dev/null || echo "Metrics Server not installed, skipping."
kubectl top pods -n team-beta  2>/dev/null || true

echo; echo "Done. Run scripts/collect-evidence.sh to save outputs for the report."

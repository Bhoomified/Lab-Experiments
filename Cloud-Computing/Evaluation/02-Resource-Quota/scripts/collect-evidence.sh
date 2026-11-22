#!/usr/bin/env bash
# Saves the current cluster state into evidence/ for the report.
# Run AFTER run-demo.sh, from the project root.
OUT=evidence; mkdir -p $OUT
for ns in team-alpha team-beta; do
  kubectl describe resourcequota compute-quota -n $ns > $OUT/quota-$ns.txt
  kubectl describe limitrange container-limits -n $ns > $OUT/limitrange-$ns.txt
  kubectl get pods -n $ns -o wide                     > $OUT/pods-$ns.txt
  kubectl get events -n $ns --sort-by=.lastTimestamp  > $OUT/events-$ns.txt
done
kubectl apply -f manifests/06-pod-exceeds-limitrange.yaml > $OUT/rejected-limitrange.txt 2>&1
kubectl apply -f manifests/07-pod-exceeds-quota.yaml      > $OUT/rejected-quota.txt 2>&1
echo "Saved to $OUT/"; ls $OUT

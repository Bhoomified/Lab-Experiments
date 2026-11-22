#!/usr/bin/env bash
# Deleting a namespace removes everything inside it.
kubectl delete namespace team-alpha team-beta --ignore-not-found

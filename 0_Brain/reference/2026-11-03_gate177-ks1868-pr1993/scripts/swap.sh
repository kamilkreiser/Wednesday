#!/bin/bash
# swap.sh base|head : write the 4 PR 1993 product files from develop (base) or the PR head; tests stay at head.
set -euo pipefail
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993/repo
P="Blockchain/Dev/packages/shared/src/vc/verifier.ts Blockchain/Dev/packages/shared/src/prism/identus-client.ts Blockchain/Dev/packages/shared/src/resilience/service-client.ts Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts"
case "$1" in
  base) ref=refs/gate/develop;; head) ref=refs/gate/1993;; *) echo "usage: base|head"; exit 2;;
esac
for p in $P; do git -C $R show $ref:$p > $R/$p; done
for p in $P; do printf '%s %s %s\n' "$1" "$(git -C $R hash-object $R/$p | cut -c1-12)" "$p"; done

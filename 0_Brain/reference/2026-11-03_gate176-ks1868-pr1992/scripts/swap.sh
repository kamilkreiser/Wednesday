#!/bin/bash
# swap.sh base|head : write the 3 PR 1992 product files from develop (base) or the PR head; tests stay at head.
set -euo pipefail
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate176-ks1868-pr1992/repo
P="Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts Blockchain/Dev/packages/shared/src/security/secrets-manager.ts Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts"
case "$1" in
  base) ref=refs/gate/develop;; head) ref=refs/gate/1992;; *) echo "usage: base|head"; exit 2;;
esac
for p in $P; do git -C $R show $ref:$p > $R/$p; done
for p in $P; do printf '%s %s %s\n' "$1" "$(git -C $R hash-object $R/$p | cut -c1-12)" "$p"; done

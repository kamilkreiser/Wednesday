#!/bin/bash
# swap.sh base|head : write the 9 product files (5 from PR 1990, 4 from PR 1991) from develop (base) or from each PR head.
set -euo pipefail
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate175-ks1868-pr1990-pr1991/repo
P90="Blockchain/Dev/packages/shared/src/db/auto-migrate.ts Blockchain/Dev/packages/shared/src/db/tenant-context.ts Blockchain/Dev/packages/shared/src/db/tenant-pool-manager.ts Blockchain/Dev/packages/shared/src/middleware/tenant-rate-limiter.ts Blockchain/Dev/packages/shared/src/vault/key-vault.ts"
P91="Blockchain/Dev/services/shared/src/cache/cache-middleware.ts Blockchain/Dev/services/shared/src/cache/connection-pool.ts Blockchain/Dev/services/shared/src/cache/redis-client.ts Blockchain/Dev/services/shared/src/security/redis-security-store.ts"
case "$1" in
  base) for p in $P90 $P91; do git -C $R show refs/gate/develop:$p > $R/$p; done;;
  head) for p in $P90; do git -C $R show refs/gate/1990:$p > $R/$p; done; for p in $P91; do git -C $R show refs/gate/1991:$p > $R/$p; done;;
  *) echo "usage: base|head"; exit 2;;
esac
for p in $P90 $P91; do printf '%s %s\n' "$(git -C $R hash-object $R/$p | cut -c1-8)" "$p"; done

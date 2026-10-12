#!/bin/bash
# usage: render.sh <repo> <slot|none> <outfile> [extra VAR=val ...]   (env scrubbed of slot/port vars)
REPO=$1; SLOT=$2; OUT=$3; shift 3
PR=(--profile mock --profile devnet --profile local-llm --profile phase2)
CLEAN=(env -u GATEWAY_PORT -u WEBSITE_PORT -u FRONTEND_URL -u CORS_ORIGINS -u SECUURA_STACK_SLOT -u STACK_SLOT -u COMPOSE_PROJECT_NAME -u STACK_PREFIX -u STACK_OWNER -u STACK_BRANCH -u STACK_COMMIT -u STACK_STARTED_AT)
PIN="STACK_OWNER=unknown STACK_BRANCH=unknown STACK_COMMIT=unknown STACK_STARTED_AT=unknown"
if [ "$SLOT" = none ]; then
  "${CLEAN[@]}" STACK_OWNER=unknown STACK_BRANCH=unknown STACK_COMMIT=unknown STACK_STARTED_AT=unknown "$@" docker compose "${PR[@]}" -f "$REPO/docker-compose.local.yml" config --format json > "$OUT" 2>"$OUT.err"
else
  "${CLEAN[@]}" bash -c 'set -euo pipefail; export PROJECT_ROOT="$0" SECUURA_STACK_SLOT="$1"; shift 1; export STACK_OWNER=unknown STACK_BRANCH=unknown STACK_COMMIT=unknown STACK_STARTED_AT=unknown; . "$PROJECT_ROOT/Blockchain/Dev/scripts/stack_env.sh"; for kv in "$@"; do export "$kv"; done; docker compose --profile mock --profile devnet --profile local-llm --profile phase2 -f "$PROJECT_ROOT/docker-compose.local.yml" config --format json' "$REPO" "$SLOT" "$@" > "$OUT" 2>"$OUT.err"
fi
echo "rc=$? bytes=$(wc -c <"$OUT") $(shasum -a 256 <"$OUT"|cut -c1-16)"

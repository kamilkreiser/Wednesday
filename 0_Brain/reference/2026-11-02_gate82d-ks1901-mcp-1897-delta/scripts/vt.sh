#!/bin/bash
# usage: vt.sh <tree dir name under WORKDIR> <log> [vitest args...]
set -u
T="$1"; LOG="$2"; shift 2
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate82d-ks1901-mcp-1897-delta
M=$W/$T/Blockchain/Dev/services/mcp-server
{ echo "# $(date -u +%FT%TZ) tree=$T HEAD=$(git -C $W/$T rev-parse HEAD) node=$(node -v) args: $*"; } > "$LOG"
nice -n 10 npm --prefix "$M" run test -- --maxWorkers=2 "$@" >> "$LOG" 2>&1; RC=$?
echo "rc=$RC" >> "$LOG"; exit $RC

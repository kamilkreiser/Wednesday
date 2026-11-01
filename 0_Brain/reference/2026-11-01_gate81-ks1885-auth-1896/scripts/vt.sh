#!/bin/bash
# usage: vt.sh <base|head> <log> [vitest args...]   runs `vitest run` with cwd=services/auth (npm run sets cwd to --prefix)
set -u
T="$1"; LOG="$2"; shift 2
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate81-ks1885-auth-1896
AUTH=$W/wt_$T/Blockchain/Dev/services/auth
while :; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 20 ] && break; echo "load1=$L > 20, waiting" >&2; sleep 20; done
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2dc9c5a2-efc6-4975-a82f-157a5a9bc219/scratchpad
mkdir -p $TMPDIR
{ echo "# $(date -u +%FT%TZ) tree=$T HEAD=$(git -C $W/wt_$T rev-parse HEAD) node=$(node -v) args: $*"; } > "$LOG"
nice -n 10 npm --prefix "$AUTH" run test -- run --maxWorkers=2 "$@" >> "$LOG" 2>&1; RC=$?
echo "rc=$RC" >> "$LOG"; exit $RC

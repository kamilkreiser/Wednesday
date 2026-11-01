#!/bin/bash
# Gate 71: run test files in tenant-provisioning, optionally with the gate71 real-PG probe placed into src/__tests__.
# usage: probe_run.sh <log> [--probe] [vitest file args...]
# Password read from the 0600 scratch pw.env, scrubbed from the log. nice -n 10; waits while load1 > 8. --maxWorkers=1.
set -u
LOG="$1"; shift
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate71-ks1861-1885
D=$G/repo/Blockchain/Dev; TP=$D/services/tenant-provisioning
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c6cc71e2-d540-45eb-85fa-5aca0154bf77/scratchpad/g71
SU=$(grep '^SU=' $S/pw.env | cut -d= -f2)
PORT=$(docker port gate71-pg 5432 | head -1 | sed 's/.*://')
export GATE71_PG_URL="postgresql://secuura:${SU}@127.0.0.1:${PORT}/secuura_platform"
export TMPDIR=$S/tmp; mkdir -p $TMPDIR; export GATE71_S1_OUT=${GATE71_S1_OUT:-$G/evidence/s1_status_route_audit_fail.json}
PROBE=0; if [ "${1:-}" = "--probe" ]; then PROBE=1; shift; cp $G/scripts/gate71-realpg-probe.test.ts $TP/src/__tests__/gate71-realpg-probe.test.ts; fi
while :; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 8 ] && break; echo "load1=$L > 8, waiting" >&2; sleep 20; done
echo "load at start: $(sysctl -n vm.loadavg)" > "$LOG"
nice -n 10 $D/node_modules/.bin/vitest run --root $TP --maxWorkers=1 "$@" >> "$LOG" 2>&1; RC=$?
echo "load at end: $(sysctl -n vm.loadavg)" >> "$LOG"
if [ $PROBE = 1 ]; then mv $TP/src/__tests__/gate71-realpg-probe.test.ts $S/probe_parked.test.ts; fi
sed -i '' -e "s/${SU}/<SU>/g" "$LOG"
echo "rc=$RC" >> "$LOG"
exit $RC

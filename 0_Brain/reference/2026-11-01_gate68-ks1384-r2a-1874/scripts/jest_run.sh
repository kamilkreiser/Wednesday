#!/bin/bash
# Gate 68 (adapted from gate 65): run originate jest or anchoring vitest.
# usage: jest_run.sh <unit|unitpar|integ|avunit|avinteg> <superuser|app> <log> [args...]
# DB passwords come from the scratchpad pw.env (never written to evidence). nice -n 10; waits while load1 > 8.
set -u
KIND="$1"; ROLE="$2"; LOG="$3"; shift 3
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate68-ks1384-r2a-1874
D=$G/repo/Blockchain/Dev
O=$D/services/originate
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/91fd755a-1c2a-4513-956f-a7024ed15bc3/scratchpad/g68
SU=$(grep '^SU=' $S/pw.env | cut -d= -f2); APP=$(grep '^APP=' $S/pw.env | cut -d= -f2)
PORT=$(docker port gate68-pg 5432 | head -1 | sed 's/.*://')
export TEST_DATABASE_URL="postgresql://secuura:${SU}@127.0.0.1:${PORT}/secuura"
export TEST_PLATFORM_DATABASE_URL="postgresql://secuura:${SU}@127.0.0.1:${PORT}/secuura_platform"
if [ "$ROLE" = app ]; then export TEST_APP_DATABASE_URL="postgresql://secuura_app:${APP}@127.0.0.1:${PORT}/secuura"; else unset TEST_APP_DATABASE_URL; fi
export TMPDIR=$S/tmp; mkdir -p $TMPDIR
while :; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 8 ] && break; echo "load1=$L > 8, waiting" >&2; sleep 20; done
case "$KIND" in
  avunit)  nice -n 10 $D/node_modules/.bin/vitest run --root $D/services/anchoring --maxWorkers=2 "$@" > "$LOG" 2>&1; RC=$?;;
  avinteg) nice -n 10 $D/node_modules/.bin/vitest run --root $D/services/anchoring --config vitest.integration.config.ts --maxWorkers=1 "$@" > "$LOG" 2>&1; RC=$?;;
  *)
    CFG=$O/jest.config.js; [ "$KIND" = integ ] && CFG=$O/jest.integration.config.js
    PAR=--runInBand; [ "$KIND" = unitpar ] && PAR=--maxWorkers=2
    nice -n 10 node $D/node_modules/jest/bin/jest.js --config "$CFG" --rootDir "$O" $PAR "$@" > "$LOG" 2>&1; RC=$?;;
esac
sed -i '' -e "s/${SU}/<SU>/g" -e "s/${APP}/<APP>/g" "$LOG"
echo "rc=$RC" >> "$LOG"
exit $RC

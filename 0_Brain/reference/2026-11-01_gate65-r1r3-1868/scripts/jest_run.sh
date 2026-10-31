#!/bin/bash
# Gate 65 (adapted from gate 61): run originate jest. usage: jest_run.sh <unit|integ> <superuser|app> <log> [jest args...]
# DB passwords come from the scratchpad pw.env (never written to evidence). nice -n 10; waits while load1 > 16.
set -u
KIND="$1"; ROLE="$2"; LOG="$3"; shift 3
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate65-r1r3-1868
D=$G/repo/Blockchain/Dev
O=$D/services/originate
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8eb04056-8fef-4c17-8fb3-31eec776f98e/scratchpad/g65
CID=$(cat $G/evidence/pg_container_id.txt)
SU=$(grep '^SU=' $S/pw.env | cut -d= -f2); APP=$(grep '^APP=' $S/pw.env | cut -d= -f2)
PORT=$(docker port "$CID" 5432 | head -1 | sed 's/.*://')
export TEST_DATABASE_URL="postgresql://secuura:${SU}@127.0.0.1:${PORT}/secuura"
export TEST_PLATFORM_DATABASE_URL="postgresql://secuura:${SU}@127.0.0.1:${PORT}/secuura_platform"
if [ "$ROLE" = app ]; then export TEST_APP_DATABASE_URL="postgresql://secuura_app:${APP}@127.0.0.1:${PORT}/secuura"; else unset TEST_APP_DATABASE_URL; fi
export TMPDIR=$S/tmp; mkdir -p $TMPDIR
while :; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 16 ] && break; echo "load1=$L > 16, waiting" >&2; sleep 20; done
CFG=$O/jest.config.js; [ "$KIND" = integ ] && CFG=$O/jest.integration.config.js
PAR=--runInBand; [ "$KIND" = unitpar ] && PAR=--maxWorkers=2
nice -n 10 node $D/node_modules/jest/bin/jest.js --config "$CFG" --rootDir "$O" $PAR "$@" > "$LOG" 2>&1
RC=$?
sed -i '' -e "s/${SU}/<SU>/g" -e "s/${APP}/<APP>/g" "$LOG"
echo "rc=$RC" >> "$LOG"
exit $RC

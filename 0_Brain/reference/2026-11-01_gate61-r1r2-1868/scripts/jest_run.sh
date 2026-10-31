#!/bin/bash
# Gate 61: run originate jest. usage: jest_run.sh <unit|integ> <superuser|app> <log> [jest args...]
# DB passwords come from the scratchpad pw.env (never written to evidence).
set -u
KIND="$1"; ROLE="$2"; LOG="$3"; shift 3
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate61-r1r2-1868
D=$G/repo/Blockchain/Dev
O=$D/services/originate
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8eb04056-8fef-4c17-8fb3-31eec776f98e/scratchpad/g61
SU=$(grep '^SU=' $S/pw.env | cut -d= -f2); APP=$(grep '^APP=' $S/pw.env | cut -d= -f2)
PORT=$(docker port gate61-pg 5432 | head -1 | sed 's/.*://')
export TEST_DATABASE_URL="postgresql://secuura:${SU}@127.0.0.1:${PORT}/secuura"
export TEST_PLATFORM_DATABASE_URL="postgresql://secuura:${SU}@127.0.0.1:${PORT}/secuura_platform"
if [ "$ROLE" = app ]; then export TEST_APP_DATABASE_URL="postgresql://secuura_app:${APP}@127.0.0.1:${PORT}/secuura"; else unset TEST_APP_DATABASE_URL; fi
export TMPDIR=$S/tmp; mkdir -p $TMPDIR
CFG=$O/jest.config.js; [ "$KIND" = integ ] && CFG=$O/jest.integration.config.js
node $D/node_modules/jest/bin/jest.js --config "$CFG" --rootDir "$O" --runInBand "$@" > "$LOG" 2>&1
RC=$?
# scrub any credential that might have been echoed
sed -i '' -e "s/${SU}/<SU>/g" -e "s/${APP}/<APP>/g" "$LOG"
echo "rc=$RC" >> "$LOG"
exit $RC

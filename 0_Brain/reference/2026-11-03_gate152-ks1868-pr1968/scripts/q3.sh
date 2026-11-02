W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate152-ks1868-pr1968; D=$W/repo/Blockchain/Dev; S=$D/services/vc-issuer
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g152
uptime > $W/logs/q3_load.log
$D/node_modules/.bin/vitest run --root $S --reporter=verbose > $W/logs/q3_whole_defaultworkers.log 2>&1; echo rc=$? >> $W/logs/q3_whole_defaultworkers.log
$D/node_modules/.bin/vitest run --root $S src/__tests__/ks1868-vc-issuer-db-pool-error-and-ready-hook-unreadable-throw.test.ts --reporter=verbose > $W/logs/q3_db_alone.log 2>&1; echo rc=$? >> $W/logs/q3_db_alone.log
uptime >> $W/logs/q3_load.log

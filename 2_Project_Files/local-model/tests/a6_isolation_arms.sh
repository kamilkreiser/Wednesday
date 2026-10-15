#!/bin/bash
# a6_isolation_arms.sh <work clone with the patch applied> — red-proof of the checker's A6 ISOLATION RE-CHECK (2026-10-16).
# Runs the REAL block (extracted from tasks/code_patch/checker.sh, not re-implemented) with the checker's own helpers.
# Arms: (1) the five health files that flaked under load in KS-1543 p3 control-r2 -> PASS FLAKY-UNDER-LOAD;
# (2) the same with a deterministic break planted in ks1258 -> FAIL; (3) the brief's own test file -> FAIL (own-test);
# (4) a file that does not exist -> FAIL (not-found). The planted break is restored with git checkout (restore, not delete).
set -u
CLONE="$1"; HERE="$(cd "$(dirname "$0")" && pwd)"; CHK="$HERE/../tasks/code_patch/checker.sh"
SUBDIR=Blockchain/Dev; SERVICE=services/api-gateway; SVC="$CLONE/$SUBDIR/$SERVICE"; RUNNER_KIND=vitest; VITEST_CFG_OPT=""
TEST_REL=src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts
REP="$(mktemp -d /tmp/a6arms.XXXXXX)"; FAILS=0
eval "$(sed -n '/^pass() {/p;/^fail() {/p' "$CHK")"
eval "$(awk '/^run_vitest\(\) \{/,/^}/' "$CHK")"
eval "$(awk '/^summ\(\) \{/,/^PYEOF$/' "$CHK"; echo '}')"
eval "$(/usr/bin/grep '^getn()' "$CHK")"
BLOCK="$(awk '/A6_ISO_BAD=""; A6_ISO_FLAKY=""/{f=1} f{print} f&&/^  fi$/{exit}' "$CHK")"
[ -n "$BLOCK" ] || { echo "ARMS ERROR: block not found"; exit 9; }
arm() { printf '%s\n' $2 > "$REP/a6_new_files.txt"; OUT="$(eval "$BLOCK" 2>&1 | /usr/bin/grep -E '^(PASS|FAIL) A6')"; case "$OUT" in "$3"*) echo "ARM $1 OK: $OUT" | cut -c1-300;; *) echo "ARM $1 WRONG (wanted $3): $OUT" | cut -c1-300; BAD=1;; esac; }
BAD=0
H="ks1054-startup-migration-failure-on-health.test.ts ks1101-health-aggregates-surface-degraded.test.ts ks1246-f-2-health-services-still-reads.test.ts ks1248-n-1-system-status-troubleshooting-marks.test.ts ks1258-degraded-optional-service-advice.test.ts"
arm 1-flaky "$H" "PASS A6"
T="$SVC/src/__tests__/ks1258-degraded-optional-service-advice.test.ts"
python3 - "$T" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read(); i=s.index("expect("); open(p,'w').write(s[:i]+"expect('planted').toBe('break'); "+s[i:])
PY
arm 2-deterministic-red "ks1258-degraded-optional-service-advice.test.ts" "FAIL A6"
git -C "$CLONE" checkout -- "$SUBDIR/$SERVICE/src/__tests__/ks1258-degraded-optional-service-advice.test.ts" && echo "restored ks1258: $(git -C "$CLONE" status --short -- "$T" | wc -l | tr -d ' ') changed"
arm 3-own-test "ks1543-document-types-catch-logs-the-error.test.ts" "FAIL A6"
arm 4-not-found "no-such-file-ks0000.test.ts" "FAIL A6"
echo "ARMS RESULT: $([ $BAD -eq 0 ] && echo ALL OK || echo SOME WRONG) (rep $REP)"

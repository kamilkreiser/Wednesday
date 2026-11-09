#!/bin/bash
# frontend_arms.sh - arms for the 2026-11-10 FRONTEND TIER of night/build_input.sh (Blockchain/Dev/frontend/<pkg>/src/**).
# Each arm prints:  ARM <id>: PASS|FAIL rc=<rc> | deciding line: <the line that decided it>
# Read-only on the Secuura checkout and on the Spark cache (it only `git clone --bare --shared`s the cache into $WORK, a
# scratch dir). Needs the Secuura .env (Linear read; builder-internal, never printed) and the network, like the builder.
# Starts no Spark/Ornith round, touches no queue state, commits nothing. Usage: frontend_arms.sh [work-dir]
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; NIGHT="$(dirname "$HERE")"; LM="$(dirname "$NIGHT")"
WORK="${1:-${TMPDIR:-/tmp}/frontend_arms.$$}"; mkdir -p "$WORK"
NEW="$NIGHT/build_input.sh"; OLD="$NIGHT/build_input.sh.pre-1110-frontend"
CACHE="$LM/spark/cache/src"
TIP=07d4218e9776a5eced016f16330983c900e94fb3          # the tip KS-2095's brief was measured at (Spark cache HEAD)
BR2095="$(ls -d "$NIGHT"/briefs/ks_2095_o130_p1_*)"
BR1923="$(ls -d "$NIGHT"/briefs/ks_1923_o130_p1_*)"
FAILS=0
arm() { # arm <id> <ok 0|1> <rc> <deciding line>
  if [ "$2" -eq 0 ]; then echo "ARM $1: PASS rc=$3 | deciding line: $4"; else echo "ARM $1: FAIL rc=$3 | deciding line: $4"; FAILS=$((FAILS+1)); fi
}
first() { grep -m1 -e "$1" "$2" | cut -c1-260; }

# --- scratch origin whose develop == TIP, and a clone of it = NIGHT_SOURCE_CHECKOUT (the real origin has moved past TIP and a fetch is a write verb)
[ -d "$WORK/origin.git" ] || git clone -q --bare --shared "$CACHE" "$WORK/origin.git" > "$WORK/mk1.out" 2>&1 || { echo "ARM setup: FAIL clone of the cache: $(cat "$WORK/mk1.out")"; exit 1; }
git --git-dir="$WORK/origin.git" update-ref refs/heads/develop "$TIP" || exit 1
[ -d "$WORK/src/.git" ] || git clone -q --no-checkout "$WORK/origin.git" "$WORK/src" > "$WORK/mk2.out" 2>&1 || { echo "ARM setup: FAIL scratch clone"; exit 1; }
export NIGHT_SOURCE_CHECKOUT="$WORK/src"

K2095=(ref=Blockchain/Dev/frontend/issuer/src/__tests__/provenance-timeline.test.tsx line=192 ctx=65536 started_ok=arm test_file=Blockchain/Dev/frontend/issuer/src/__tests__/blockchain-card.test.tsx)
FEPROD=product=Blockchain/Dev/frontend/issuer/src/components/blockchain/BlockchainCard.tsx

# ---- (a1) the KS-2095 brief, STRICT (no overrides): the frontend path no longer refuses; whatever refuses is a brief-shape gate
NIGHT_BRIEFS_DIR="$BR2095" bash "$NEW" KS-2095 "$WORK/a1.json" $FEPROD "${K2095[@]}" > "$WORK/a1.out" 2>&1; rc=$?
if grep -q 'neither services' "$WORK/a1.out"; then ok=1; else ok=0; fi
arm "a1 KS-2095 strict: the frontend product path is not the refusal" "$ok" "$rc" "$(grep -m1 -e 'FRONTEND TIER: product' "$WORK/a1.out" | cut -c1-160) || $(first 'REFUSED' "$WORK/a1.out" | cut -c1-170)"

# ---- (a) the KS-2095 brief BUILDS (rc 0) and the prompt source is the brief. The brief's own two shape gates (context-as-addition,
#      blank context line) are the builder's existing, documented ALLOW_* overrides - set here, printed, and reported: they are brief defects, not frontend ones.
ALLOW_CONTEXT_AS_ADDITION=1 ALLOW_BLANK_CONTEXT=1 NIGHT_BRIEFS_DIR="$BR2095" bash "$LM/tasks/code_patch2/build_input2.sh" KS-2095 "$WORK/a.json" "$BR2095/KS-2095.md" "${K2095[@]}" > "$WORK/a.out" 2>&1; rc=$?
ok=1; [ "$rc" -eq 0 ] && grep -q 'prompt source: WEDNESDAY BRIEF .*KS-2095.md.*the ticket description is NOT the prompt' "$WORK/a.out" && ok=0
arm "a KS-2095 builds (ALLOW_CONTEXT_AS_ADDITION=1 ALLOW_BLANK_CONTEXT=1)" "$ok" "$rc" "$(first 'prompt source:' "$WORK/a.out")"

# ---- (b) a packages/shared brief that built before (KS-1923): the new builder's input.json is byte-identical to the .pre-1110-frontend builder's
P1923=(product=packages/shared/src/security/audit-logger.ts ref=Blockchain/Dev/packages/shared/src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts line=317 ctx=65536 started_ok=arm)
NIGHT_BRIEFS_DIR="$BR1923" bash "$OLD" KS-1923 "$WORK/b_old.json" "${P1923[@]}" > "$WORK/b_old.out" 2>&1; rc_old=$?
NIGHT_BRIEFS_DIR="$BR1923" bash "$NEW" KS-1923 "$WORK/b_new.json" "${P1923[@]}" > "$WORK/b_new.out" 2>&1; rc_new=$?
sed "s#$WORK/b_old.json#OUT#" "$WORK/b_old.out" > "$WORK/b_old.norm"; sed "s#$WORK/b_new.json#OUT#" "$WORK/b_new.out" > "$WORK/b_new.norm"
ok=1
if [ "$rc_old" -eq 0 ] && [ "$rc_new" -eq 0 ] && cmp -s "$WORK/b_old.json" "$WORK/b_new.json" && cmp -s "$WORK/b_old.norm" "$WORK/b_new.norm"; then ok=0; fi
arm "b KS-1923 (packages/shared) prompt byte-identical old vs new (rc_old=$rc_old)" "$ok" "$rc_new" "cmp input.json: $(cmp "$WORK/b_old.json" "$WORK/b_new.json" 2>&1 && echo IDENTICAL) ($(wc -c < "$WORK/b_new.json" | tr -d ' ') B); stdout $(cmp -s "$WORK/b_old.norm" "$WORK/b_new.norm" && echo IDENTICAL || echo DIFFERS)"

# ---- (c) a path outside services/packages/frontend still refuses (and the old builder says the same)
NIGHT_BRIEFS_DIR="$BR2095" bash "$NEW" KS-2095 "$WORK/c.json" product=Blockchain/Dev/infra/widget/src/thing.ts "${K2095[@]}" > "$WORK/c.out" 2>&1; rc=$?
ok=1; [ "$rc" -eq 2 ] && grep -q 'product path is neither services/\* nor packages/shared' "$WORK/c.out" && ok=0
arm "c path outside services/packages/frontend refuses" "$ok" "$rc" "$(first 'REFUSED' "$WORK/c.out")"
NIGHT_BRIEFS_DIR="$BR2095" bash "$NEW" KS-2095 "$WORK/c2.json" product=Blockchain/Dev/frontend/issuer/scripts/check-bundle-size.mjs "${K2095[@]}" > "$WORK/c2.out" 2>&1; rc=$?
ok=1; [ "$rc" -eq 2 ] && grep -q 'product path is neither services/\* nor packages/shared' "$WORK/c2.out" && ok=0
arm "c2 frontend path NOT under src/ (scripts/*.mjs) refuses" "$ok" "$rc" "$(first 'REFUSED' "$WORK/c2.out")"

# ---- (d) a frontend package with no vitest config refuses with a clear reason (verifier has neither vitest.config.* nor a vite.config test: block)
NIGHT_BRIEFS_DIR="$BR2095" bash "$NEW" KS-2095 "$WORK/d.json" product=Blockchain/Dev/frontend/verifier/src/App.tsx "${K2095[@]}" > "$WORK/d.out" 2>&1; rc=$?
ok=1; [ "$rc" -eq 2 ] && grep -q 'frontend package frontend/verifier has no vitest config at the tip' "$WORK/d.out" && ok=0
arm "d frontend package without a vitest config refuses" "$ok" "$rc" "$(first 'REFUSED' "$WORK/d.out")"

echo "frontend_arms: $FAILS failing arm(s); work dir $WORK"
[ "$FAILS" -eq 0 ]

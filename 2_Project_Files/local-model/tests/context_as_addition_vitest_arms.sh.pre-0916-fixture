#!/bin/bash
# Arms for the CONTEXT-AS-ADDITION GATE in night/build_input.sh — the VITEST twin of the bash-tier gate
# (2026-09-16 17:4x).
#
# Why a twin was needed: the gate went into build_bash_input.sh first. KS-1168 is a VITEST ticket Kam
# ruled that morning, and it burned TWO model rounds against a defect already gated one tier over.
# A guard that exists on one of two identical paths is a guard with a hole in it.
#
# The red case is the REAL KS-1168 brief as it stands: three edit blocks carrying 9, 9 and 1 '+' lines
# byte-identical to '-' lines in the same block (measured). The over-fire control is a real brief that
# passed 7/7 on its first sample.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM="$(cd "$HERE/.." && pwd)"
BUILD="$LM/night/build_input.sh"
TMP="${TMPDIR:-/tmp}/ctx_add_vitest_arms.$$"; mkdir -p "$TMP"
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  PASS  $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL  $1"; }

echo "ARM 1 — the REAL KS-1168 brief (9+9+1 '+' lines duplicating '-' lines) must be REFUSED"
bash "$BUILD" KS-1168 "$TMP/a1.json" \
  product=services/auth/src/repositories/userRepo.ts \
  ref=Blockchain/Dev/services/auth/src/__tests__ ctx=65536 > "$TMP/o1" 2>&1
RC=$?
if [ "$RC" -eq 2 ] && grep -q 'are CONTEXT, not additions' "$TMP/o1"; then
  ok "refused rc=2 with the cause named"
else
  bad "expected rc 2 + the named cause, got rc=$RC: $(tail -2 "$TMP/o1" | tr '\n' ' ')"
fi

echo "ARM 2 — the override lets it through (a read-and-understood case is not blocked)"
ALLOW_CONTEXT_AS_ADDITION=1 bash "$BUILD" KS-1168 "$TMP/a2.json" \
  product=services/auth/src/repositories/userRepo.ts \
  ref=Blockchain/Dev/services/auth/src/__tests__ ctx=65536 > "$TMP/o2" 2>&1
RC=$?
[ "$RC" -eq 0 ] && ok "rc=0 with the override" \
  || bad "override failed (rc=$RC): $(tail -2 "$TMP/o2" | tr '\n' ' ')"

echo "ARM 3 — OVER-FIRE CONTROL: KS-692, a real brief that passed 7/7, must still build (rc 0)"
echo "        Without this arm, a gate that refuses EVERY vitest brief would look identical to a working one."
bash "$BUILD" KS-692 "$TMP/a3.json" \
  product=services/vc-issuer/src/routes/status.ts \
  ref=Blockchain/Dev/services/vc-issuer/src/__tests__ ctx=65536 > "$TMP/o3" 2>&1
RC=$?
[ "$RC" -eq 0 ] && ok "rc=0 — no over-fire on a correctly written brief" \
  || bad "OVER-FIRE: KS-692 refused (rc=$RC): $(tail -2 "$TMP/o3" | tr '\n' ' ')"

echo "ARM 4 — the gate is on BOTH tiers (the hole that let KS-1168 through)"
b=0; v=0
grep -q 'CONTEXT, not additions' "$LM/tasks/bash_patch/build_bash_input.sh" && b=1
grep -q 'CONTEXT, not additions' "$LM/night/build_input.sh" && v=1
[ "$b" = 1 ] && [ "$v" = 1 ] && ok "present in both builders (bash=$b vitest=$v)" \
  || bad "MISSING on a tier: bash=$b vitest=$v"

echo
echo "arms: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]

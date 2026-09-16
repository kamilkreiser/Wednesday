#!/bin/bash
# Arms for the CONTEXT-AS-ADDITION GATE in night/build_input.sh — the VITEST twin of the bash-tier gate
# (2026-09-16 17:4x).
#
# Why a twin was needed: the gate went into build_bash_input.sh first. KS-1168 is a VITEST ticket Kam
# ruled that morning, and it burned TWO model rounds against a defect already gated one tier over.
# A guard that exists on one of two identical paths is a guard with a hole in it.
#
# The red case is a FROZEN FIXTURE, tests/fixtures/briefs/KS-1168.md — a copy of that brief as it stood
# before repair, carrying '+' lines byte-identical to '-' lines in the same block.
#
# WHY FROZEN, and it is the point of this file: ARM 1 originally pointed at the LIVE KS-1168 brief. The
# repair that the gate existed to force then landed, the brief stopped being defective, and the arm went
# red for the best possible reason — which is indistinguishable, at a glance, from the gate breaking. An
# arm whose fixture someone is actively trying to fix has a built-in expiry date. The fixture is now a
# copy nobody edits; the over-fire control is a real brief that passed 7/7 on its first sample.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM="$(cd "$HERE/.." && pwd)"
BUILD="$LM/night/build_input.sh"
TMP="${TMPDIR:-/tmp}/ctx_add_vitest_arms.$$"; mkdir -p "$TMP"
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  PASS  $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL  $1"; }

FIXTURES="$LM/tests/fixtures/briefs"
echo "ARM 0 — the frozen fixture really is defective (an arm on a clean fixture proves nothing)"
DUPS=$(python3 - "$FIXTURES/KS-1168.md" <<'PYX'
import sys
L=open(sys.argv[1],encoding='utf-8').read().split('\n')
idx=[i for i,l in enumerate(L) if l.startswith('```')]
d=0
for a,b in zip(idx[0::2], idx[1::2]):
    body=L[a+1:b]; minus={l[1:] for l in body if l.startswith('-')}
    d+=sum(1 for x in body if x.startswith('+') and x[1:] in minus)
print(d)
PYX
)
[ "${DUPS:-0}" -gt 0 ] && ok "fixture carries $DUPS duplicated '+' line(s)" \
  || bad "the fixture has NO duplicates — ARM 1 below cannot be testing what it claims"

echo "ARM 1 — the frozen defective fixture must be REFUSED"
NIGHT_BRIEFS_DIR="$FIXTURES" bash "$BUILD" KS-1168 "$TMP/a1.json" \
  product=services/auth/src/repositories/userRepo.ts \
  ref=Blockchain/Dev/services/auth/src/__tests__ ctx=65536 > "$TMP/o1" 2>&1
RC=$?
if [ "$RC" -eq 2 ] && grep -q 'are CONTEXT, not additions' "$TMP/o1"; then
  ok "refused rc=2 with the cause named"
else
  bad "expected rc 2 + the named cause, got rc=$RC: $(tail -2 "$TMP/o1" | tr '\n' ' ')"
fi

echo "ARM 2 — the override lets it through (a read-and-understood case is not blocked)"
ALLOW_CONTEXT_AS_ADDITION=1 NIGHT_BRIEFS_DIR="$FIXTURES" bash "$BUILD" KS-1168 "$TMP/a2.json" \
  product=services/auth/src/repositories/userRepo.ts \
  ref=Blockchain/Dev/services/auth/src/__tests__ ctx=65536 > "$TMP/o2" 2>&1
RC=$?
[ "$RC" -eq 0 ] && ok "rc=0 with the override" \
  || bad "override failed (rc=$RC): $(tail -2 "$TMP/o2" | tr '\n' ' ')"

echo "ARM 3 — OVER-FIRE CONTROL: the LIVE, repaired KS-1168 must now build (rc 0)"
bash "$BUILD" KS-1168 "$TMP/a3b.json" \
  product=services/auth/src/repositories/userRepo.ts \
  ref=Blockchain/Dev/services/auth/src/__tests__ ctx=65536 > "$TMP/o3b" 2>&1
RC=$?
[ "$RC" -eq 0 ] && ok "the repaired brief passes — fixture and live copy give OPPOSITE verdicts, which is the discriminator" \
  || bad "the repaired KS-1168 is still refused (rc=$RC): $(tail -2 "$TMP/o3b" | tr '\n' ' ')"

echo "ARM 4 — OVER-FIRE CONTROL: KS-692, a real brief that passed 7/7, must still build (rc 0)"
echo "        Without this arm, a gate that refuses EVERY vitest brief would look identical to a working one."
bash "$BUILD" KS-692 "$TMP/a3.json" \
  product=services/vc-issuer/src/routes/status.ts \
  ref=Blockchain/Dev/services/vc-issuer/src/__tests__ ctx=65536 > "$TMP/o3" 2>&1
RC=$?
[ "$RC" -eq 0 ] && ok "rc=0 — no over-fire on a correctly written brief" \
  || bad "OVER-FIRE: KS-692 refused (rc=$RC): $(tail -2 "$TMP/o3" | tr '\n' ' ')"

echo "ARM 5 — the gate is on BOTH tiers (the hole that let KS-1168 through)"
b=0; v=0
grep -q 'CONTEXT, not additions' "$LM/tasks/bash_patch/build_bash_input.sh" && b=1
grep -q 'CONTEXT, not additions' "$LM/night/build_input.sh" && v=1
[ "$b" = 1 ] && [ "$v" = 1 ] && ok "present in both builders (bash=$b vitest=$v)" \
  || bad "MISSING on a tier: bash=$b vitest=$v"

echo
echo "arms: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]

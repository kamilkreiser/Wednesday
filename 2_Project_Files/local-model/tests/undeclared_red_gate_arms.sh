#!/bin/bash
# Arms for the UNDECLARED-RED GATE in night/build_input.sh (added 2026-09-16 15:2x after KS-692).
#
# The defect it closes: a vitest brief whose `it(` cell titles carry no 🔴 AND which has no
# `## Red cells` section makes the checker's A4 gate classify every genuine assertion-red as a
# CONTROL red — so a CORRECT model output FAILS and the verdict reads as a model failure.
# KS-692 at 15:13 on 2026-09-16 is the case: 3 assertion-reds, both controls green, FAIL.
#
# Every arm runs the REAL builder on a REAL brief. Nothing here re-implements the gate's predicate
# (a hand-rolled twin of a tool disagrees with the tool by default). The one mutation — moving the
# `## Red cells` section out of the KS-692 brief — is reversed and the restoration is proven by
# checksum, not assumed.
#
# Run:  bash 2_Project_Files/local-model/tests/undeclared_red_gate_arms.sh
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM="$(cd "$HERE/.." && pwd)"
BUILD="$LM/night/build_input.sh"
BRIEFS="$LM/night/briefs"
TMP="${TMPDIR:-/tmp}/undeclared_red_arms.$$"
mkdir -p "$TMP"
PASS=0; FAIL=0
ok()   { PASS=$((PASS+1)); echo "  PASS  $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL  $1"; }

run_build() { # <id> <extra pins...> -> writes $TMP/out, sets RC
  local id="$1"; shift
  bash "$BUILD" "$id" "$TMP/input_$id.json" "$@" > "$TMP/out" 2>&1
  RC=$?
}

echo "ARM 1 — the REAL KS-692 brief WITHOUT its '## Red cells' section must be REFUSED (rc 2)"
SRC="$BRIEFS/KS-692.md"
SUM_BEFORE="$(shasum -a 256 "$SRC" | awk '{print $1}')"
cp "$SRC" "$TMP/KS-692.md.restore"
python3 - "$SRC" "$TMP/KS-692.md.stripped" <<'PY'
import re, sys
s = open(sys.argv[1], encoding='utf-8').read()
out = re.sub(r"^##+\s*Red cells\b.*?(?=^##+\s)", "", s, flags=re.M | re.S)
assert out != s, "the section was not found — this arm cannot test what it claims"
open(sys.argv[2], 'w', encoding='utf-8').write(out)
PY
if [ $? -ne 0 ]; then bad "ARM 1 setup: could not strip the section"; else
  cp "$TMP/KS-692.md.stripped" "$SRC"
  run_build KS-692 product=services/vc-issuer/src/routes/status.ts ref=Blockchain/Dev/services/vc-issuer/src/__tests__ ctx=65536
  cp "$TMP/KS-692.md.restore" "$SRC"
  if [ "$RC" -eq 2 ] && grep -q 'NONE of whose titles carries' "$TMP/out"; then
    ok "refused rc=2 and named the cause"
  else
    bad "expected rc 2 + the named cause, got rc=$RC: $(tail -2 "$TMP/out" | tr '\n' ' ')"
  fi
fi

echo "ARM 2 — the brief is restored BYTE-FOR-BYTE (a mutation arm that does not restore is a defect it introduced)"
SUM_AFTER="$(shasum -a 256 "$SRC" | awk '{print $1}')"
[ "$SUM_BEFORE" = "$SUM_AFTER" ] && ok "checksum identical" || bad "brief NOT restored: $SUM_BEFORE != $SUM_AFTER"

echo "ARM 3 — the REAL KS-692 brief AS IT STANDS (with the section) passes the gate (rc 0)"
run_build KS-692 product=services/vc-issuer/src/routes/status.ts ref=Blockchain/Dev/services/vc-issuer/src/__tests__ ctx=65536
if [ "$RC" -eq 0 ] && grep -q 'red cells declared by the brief: 3' "$TMP/out"; then
  ok "rc=0 and the three cells were parsed"
else
  bad "expected rc 0 + 3 declared cells, got rc=$RC: $(tail -2 "$TMP/out" | tr '\n' ' ')"
fi

echo "ARM 4 — OVER-FIRE CONTROL: KS-975 (🔴 in its cell titles, NO '## Red cells' section) must still build (rc 0)"
echo "        This is the arm that proves the gate did not just refuse every vitest brief. 29 of the 30"
echo "        briefs on disk at 15:2x are this shape; KS-692 was the only hit."
run_build KS-975 product=services/security/src/rateLimitScope.ts ref=Blockchain/Dev/services/security/src/__tests__ ctx=49152
if [ "$RC" -eq 0 ]; then
  ok "rc=0 — no over-fire on a brief that declares its reds with the glyph"
else
  bad "OVER-FIRE: KS-975 refused (rc=$RC): $(tail -2 "$TMP/out" | tr '\n' ' ')"
fi

echo "ARM 5 — the override lets a read-and-understood case through, loudly"
cp "$TMP/KS-692.md.stripped" "$SRC"
ALLOW_UNDECLARED_REDS=1 bash "$BUILD" KS-692 "$TMP/input_override.json" product=services/vc-issuer/src/routes/status.ts ref=Blockchain/Dev/services/vc-issuer/src/__tests__ ctx=65536 > "$TMP/out" 2>&1
RC=$?
cp "$TMP/KS-692.md.restore" "$SRC"
if [ "$RC" -eq 0 ] && grep -q 'UNDECLARED-RED GATE overridden' "$TMP/out"; then
  ok "rc=0 and the override announced itself"
else
  bad "expected rc 0 + the override warning, got rc=$RC: $(tail -2 "$TMP/out" | tr '\n' ' ')"
fi

echo "ARM 6 — the brief is restored again after ARM 5"
SUM_AFTER="$(shasum -a 256 "$SRC" | awk '{print $1}')"
[ "$SUM_BEFORE" = "$SUM_AFTER" ] && ok "checksum identical" || bad "brief NOT restored: $SUM_BEFORE != $SUM_AFTER"

echo
echo "arms: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]

#!/bin/bash
# statement_gate_arms.sh — red-proof for build_input.sh's TAMPER STATEMENT GATE (2026-09-15 15:3x, ledger w=3).
# A `## Tamper` whose `from` line sits mid-statement must carry `statement_ok:`; single-line statements never need it.
# Arms run build_input against scratch brief dirs via NIGHT_BRIEFS_DIR; nothing outside the scratch is written.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; NIGHT="$HERE/../night"; BRIEFS="$NIGHT/briefs"
S="${STATEMENT_ARMS_SCRATCH:-/private/tmp/claude-501/night/statement_gate_arms_$$}"; mkdir -p "$S"
PINS=(product=Blockchain/Dev/services/api-gateway/src/routes/verification.ts ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks1057-verify-confidence-is-status-aware.test.ts ctx=49152)
pass=0; fail=0
arm() { # name expect(BUILT|REFUSED) briefdir line
  local name="$1" expect="$2" dir="$3" line="$4" out rc
  out="$(NIGHT_BRIEFS_DIR="$dir" bash "$NIGHT/build_input.sh" KS-1130 "$S/$name.json" "${PINS[@]}" "line=$line" 2>&1)"; rc=$?
  local got=BUILT; [ $rc -ne 0 ] && got=REFUSED
  local why=""; echo "$out" | /usr/bin/grep -q -i 'MID-STATEMENT' && why=" (mid-statement gate)"
  if [ "$got" = "$expect" ]; then pass=$((pass+1)); echo "PASS $name: $got$why"; else fail=$((fail+1)); echo "FAIL $name: expected $expect got $got$why"; echo "$out" | tail -3; fi
}
# arm 1 RED: the v1 E7 tamper (:623 ends with `&&`, no statement_ok) → REFUSED by the gate
mkdir -p "$S/a1"; cp "$BRIEFS/KS-1130.md.e7-tamper-v1-2026-09-15" "$S/a1/KS-1130.md"; arm a1_e7_v1_mid_no_ok REFUSED "$S/a1" 623
# arm 2 GREEN: the corrected E7 brief with statement_ok → BUILT
mkdir -p "$S/a2"; cp "$BRIEFS/KS-1130.md.e7-held-2026-09-15" "$S/a2/KS-1130.md"; arm a2_e7_corrected_with_ok BUILT "$S/a2" 623
# arm 3 GREEN: the E3 brief (:627 single-line statement) WITHOUT statement_ok → BUILT (no over-fire)
mkdir -p "$S/a3"; /usr/bin/grep -v '^statement_ok:' "$BRIEFS/KS-1130.md" > "$S/a3/KS-1130.md"; arm a3_e3_single_line_no_ok BUILT "$S/a3" 627
# arm 4 GREEN: the E3 brief as written (with statement_ok) → BUILT
mkdir -p "$S/a4"; cp "$BRIEFS/KS-1130.md" "$S/a4/KS-1130.md"; arm a4_e3_as_written BUILT "$S/a4" 627
# arm 5 RED: a tamper whose from line is :624 (mid-statement by the NEXT line `persistedBlockHeight > 0;`? no — :624 ends with `&&`) no statement_ok → REFUSED
mkdir -p "$S/a5"; python3 - "$BRIEFS/KS-1130.md" "$S/a5/KS-1130.md" <<'PY'
import sys,re
s=open(sys.argv[1],encoding='utf-8').read()
s=re.sub(r"^line: 627$", "line: 624", s, flags=re.M)
s=re.sub(r"^from: `.*`$", "from: `      Number.isInteger(persistedBlockHeight) &&`", s, flags=re.M)
s=re.sub(r"^to: `.*`$", "to: `      true && // TAMPER`", s, flags=re.M)
s=re.sub(r"^statement_ok:.*$\n", "", s, flags=re.M)
open(sys.argv[2],'w',encoding='utf-8').write(s)
PY
arm a5_624_mid_no_ok REFUSED "$S/a5" 624
echo "arms: $pass pass / $fail fail (scratch $S)"; [ $fail -eq 0 ]

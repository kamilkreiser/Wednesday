#!/bin/bash
# selftest_mode_arms.sh [CLONE] — code_patch SELF-TESTING mode (2026-09-23; IMPROVEMENTS 14:23/14:24 rows; KS-1143).
#
# SPLIT arms (always; no clone needed) — tasks/code_patch/selftest_split.py on KS-1143 round 1's REAL applied section
# (runs/2026-09-23_ks1143-ornith35b-night/out.md.checker/section_1.reanchored.diff, 2 hunks) with that run's input:
#   S1 ordinal 2        -> rc 0; the W6 cell in the TEST half only, isCallExpression in the PROD half only
#   S2 ordinal 1        -> rc 2 (the declared red cell is not in the declared test hunk: wrong ordinal caught)
#   S3 ordinal 3        -> rc 2 (out of range)
#   S4 ordinals 1,2     -> rc 2 (no product hunk left)
# CHECKER arms (only when CLONE — a prepared --shared clone at the input's tip — is given) — the NEW checker on
# outputs built from the R19 brief's own edit blocks, input night/inputs/code_1143SELFTEST-R19.json:
#   C1 golden E1+E2               -> RESULT: PASS (7/7), A4 red, A5 green
#   C2 E2 made green-at-tip       -> FAIL at A4 (the test hunk alone does not red)
#   C3 golden + a second file     -> FAIL at A3 (self-testing)
# rc 0 only when every arm holds. Scratch: $SELFTEST_SCRATCH.
set -uo pipefail
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
CLONE="${1:-}"
SP="${SELFTEST_SCRATCH:-/private/tmp/claude-501/night/selftest_arms_$(date +%H%M%S)_$$}"
mkdir -p "$SP"
R=$LM/runs/2026-09-23_ks1143-ornith35b-night
SEC=$R/out.md.checker/section_1.reanchored.diff
SPLIT=$LM/tasks/code_patch/selftest_split.py
OKN=0; BADN=0
ok()  { echo "  ok   $1"; OKN=$((OKN+1)); }
bad() { echo "  BAD  $1"; BADN=$((BADN+1)); }
split() { python3 "$SPLIT" "$SEC" "$1" "$SP/t.diff" "$SP/p.diff" "$R/input.json" > "$SP/split.out" 2>&1; echo $?; }
[ "$(split 2)" = 0 ] && [ "$(/usr/bin/grep -ic 'w6 ks-1143' "$SP/t.diff")" = 1 ] && [ "$(/usr/bin/grep -ic 'w6 ks-1143' "$SP/p.diff")" = 0 ] \
  && [ "$(/usr/bin/grep -c isCallExpression "$SP/p.diff")" = 1 ] && [ "$(/usr/bin/grep -c isCallExpression "$SP/t.diff")" = 0 ] \
  && ok "S1 ordinal 2 splits test/prod correctly" || bad "S1 ordinal 2: $(cat "$SP/split.out")"
[ "$(split 1)" = 2 ] && ok "S2 wrong ordinal refused" || bad "S2: $(cat "$SP/split.out")"
[ "$(split 3)" = 2 ] && ok "S3 out-of-range refused" || bad "S3: $(cat "$SP/split.out")"
[ "$(split 1,2)" = 2 ] && ok "S4 no-product-hunk refused" || bad "S4: $(cat "$SP/split.out")"
if [ -n "$CLONE" ]; then
  IN=$LM/night/inputs/code_1143SELFTEST-R19.json
  python3 - "$LM/night/briefs/KS-1143-R19-SELFTEST.md" "$SP" <<'PY'
import re, sys, os
t = open(sys.argv[1], encoding="utf-8").read(); A = sys.argv[2]
e1, e2 = re.findall(r"```\n(@@ .*?)```", t, re.S)
p = "Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts"
hdr = f"--- a/{p}\n+++ b/{p}\n"
extra = ("--- /dev/null\n+++ b/Blockchain/Dev/packages/shared/src/__tests__/zz-extra-selftest-arm.test.ts\n@@ -0,0 +1,2 @@\n"
         "+import { it } from 'vitest';\n+it('extra', () => {});\n")
for name, body in (("C1", e1 + e2), ("C2", e1 + e2.replace("toEqual({ routes: 2, guarded: false })", "toBeDefined()")), ("C3", e1 + e2 + extra)):
    os.makedirs(f"{A}/{name}", exist_ok=True)
    open(f"{A}/{name}/out.md", "w").write("```diff\n" + hdr + body + "```\n")
PY
  # C2 needs expected_plus EMPTIED, or A3c refuses the mutated line before A4 is reached (found on the first run)
  python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); d["defect_line"]["expected_plus"]=[]; json.dump(d,open(sys.argv[2],"w"),indent=1,ensure_ascii=False)' "$IN" "$SP/input_noplus.json"
  for a in C1 C2 C3; do I="$IN"; [ "$a" = C2 ] && I="$SP/input_noplus.json"; bash $LM/tasks/code_patch/checker.sh "$I" "$SP/$a/out.md" "$CLONE" > "$SP/$a/checker.out" 2>&1; done
  /usr/bin/grep -q '^RESULT: PASS (7/7)' "$SP/C1/checker.out" && /usr/bin/grep -q '^PASS A4 RED-FIRST' "$SP/C1/checker.out" && /usr/bin/grep -q '^PASS A5 GREEN-AFTER' "$SP/C1/checker.out" \
    && ok "C1 golden PASS 7/7" || bad "C1: $(tail -1 "$SP/C1/checker.out")"
  /usr/bin/grep -q '^FAIL A4 RED-FIRST' "$SP/C2/checker.out" && ok "C2 green-at-tip test refused at A4" || bad "C2: $(/usr/bin/grep -E '^(PASS|FAIL) A4|^RESULT' "$SP/C2/checker.out" | tr '\n' ' ')"
  /usr/bin/grep -q '^FAIL A3 (self-testing)' "$SP/C3/checker.out" && ok "C3 two files refused at A3" || bad "C3: $(tail -1 "$SP/C3/checker.out")"
fi
echo "arms: ok=$OKN bad=$BADN (scratch $SP)"
[ "$BADN" -eq 0 ]

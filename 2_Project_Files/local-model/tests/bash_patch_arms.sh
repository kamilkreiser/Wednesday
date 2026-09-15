#!/bin/bash
# bash_patch_arms.sh — red-proof for tasks/bash_patch/checker.sh (2026-09-16 00:5x; Kam 2026-09-15 18:19 "extend the
# checker"). Runs the checker in a SCRATCH clone (shared, read-only on the source) against a GOLDEN diff for KS-865
# (Wednesday's own, the brief's lines byte-for-byte) and six variants derived from it by one substitution each:
#   1 the golden                                                   → PASS (7/7): both 🔴 cells red at the tip, green after
#   2 the 🔴 cells rewritten to expect what the tip already gives    → FAIL B4 (NOT red at the tip)
#   3 an extra stray `+fi` in the script hunk (parses as a diff)    → FAIL B5a (bash -n after the hunk)
#   4 the script section removed (test only)                        → FAIL B3 (touched set)
#   5 the new test written over the REFERENCE suite's path          → REFUSED at B2 (a new-file hunk cannot apply over an existing path) or B3
#   6 a 🔴 cell that reds by a LOAD error (a misspelt helper)        → FAIL B4 (load error, not a red)
#   7 the :42 must_change line kept as context (its `-` dropped)      → FAIL B3b (a must_change site not changed)
#   8 the REAL KS-865 r1 output (micro-hunks, off-by-three headers)     → PASS 7/7 via B2 REANCHORED
# Usage: bash bash_patch_arms.sh <golden out.md> <input.json> <scratch clone dir>
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
CHK=$LM/tasks/bash_patch/checker.sh
GOLD="${1:?golden out.md}"; INPUT="${2:?input.json}"; CLONE="${3:?scratch clone}"
W=$(mktemp -d); fail=0
run_arm() {  # <n> <out.md> <expected grep -E over the checker output> <label>
  local n="$1" out="$2" want="$3" label="$4" rc
  bash "$CHK" "$INPUT" "$out" "$CLONE" > "$out.checker.out" 2>&1; rc=$?
  if /usr/bin/grep -q -E "$want" "$out.checker.out"; then echo "ARM$n PASS ($label; rc=$rc)"; else echo "ARM$n FAIL ($label; rc=$rc) — got: $(/usr/bin/grep -E '^(FAIL|RESULT)' "$out.checker.out" | head -2 | cut -c1-140 | tr '\n' '·')"; fail=1; fi
}
variant() {  # <n> <python replace expression on the golden text>
  python3 - "$GOLD" "$W/arm$1.md" "$2" <<'PY'
import sys
src, dst, expr = sys.argv[1:4]
t = open(src, encoding="utf-8").read()
ns = {"t": t}
exec(expr, ns)
open(dst, "w", encoding="utf-8").write(ns["t"])
PY
}
cp "$GOLD" "$W/arm1.md"
run_arm 1 "$W/arm1.md" '^RESULT: PASS \(7/7\)' "golden passes"
variant 2 't = t.replace("is missing is an error\" 1 \"does not exist\"", "is missing is an error\" 0 \"OK\"").replace("were examined\" 0 \"5 of 5 advertised files examined\"", "were examined\" 0 \"OK\"")'
run_arm 2 "$W/arm2.md" '^FAIL B4 RED-FIRST: the test is NOT red' "cells that cannot red → B4"
variant 3 't = t.replace("+  SCANNED=$((SCANNED+1))\n", "+  SCANNED=$((SCANNED+1))\n+fi\n", 1).replace("@@ -28,18 +28,24 @@", "@@ -28,18 +28,25 @@")'
run_arm 3 "$W/arm3.md" '^FAIL B5a the script does not parse' "stray fi → B5a"
variant 4 'i = t.index("--- /dev/null"); t = "```diff\n" + t[i:]'
run_arm 4 "$W/arm4.md" '^FAIL B3 touched-file set' "script section removed → B3"
variant 5 't = t.replace("__tests__/check_no_latest_tags_inputs.test.sh", "__tests__/check_script_portability.test.sh")'
run_arm 5 "$W/arm5.md" '^FAIL B(2 section_2.diff does NOT apply|3 touched-file set)' "written over the reference → refused at B2/B3"
variant 6 't = t.replace("+run_case \"$d\"\n+check \"🔴 KS-865 — a listed input", "+run_casee \"$d\"\n+check \"🔴 KS-865 — a listed input", 1)'
run_arm 6 "$W/arm6.md" '^FAIL B4 the test hit a LOAD error' "misspelt helper → B4 load error"
variant 7 't = t.replace("-  [ -f \"$f\" ] || continue\n", "   [ -f \"$f\" ] || continue\n", 1).replace("@@ -28,18 +28,24 @@", "@@ -28,18 +28,25 @@")'
run_arm 7 "$W/arm7.md" '^FAIL B3b must_change site' "must_change :42 kept as context → B3b"
# 8 the REAL KS-865 r1 output (four micro-hunks, off-by-three headers; every -/+ line byte-exact) → PASS via B2 REANCHORED
R8=$LM/runs/2026-09-16_ks865-ornith35b-night/out.md
if [ -f "$R8" ]; then cp "$R8" "$W/arm8.md"; run_arm 8 "$W/arm8.md" '^PASS B2 .*REANCHORED' "real r1 micro-hunks → REANCHORED"; /usr/bin/grep -q '^RESULT: PASS (7/7)' "$W/arm8.md.checker.out" && echo "ARM8b PASS (the real r1 output PASSES 7/7)" || { echo "ARM8b FAIL"; fail=1; }; else echo "ARM8 SKIP (run artefact absent)"; fi
echo "work dir kept (never deleted): $W"
exit $fail

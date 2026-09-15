#!/bin/bash
# a3d_arms.sh — red-proof for a3c_plus.py's A3d twin (2026-09-15 23:4x, KS-1133 A r1): a '+' line that already
# exists at the tip and is not in the brief = a CONTEXT line marked as an addition → exit 2 with `A3D ` lines.
# Arms on REAL run artefacts (never fixtures the author invented — 09-08 rule 12):
#   1 the KS-1133 A r1 product section (four context lines marked '+')            → exit 2, 4 A3D lines
#   2 the KS-794 r2 product section (a held PASS, two expected '+' lines only)      → exit 0, no output
#   3 the KS-999 r1 product section (a3c_arms' positive: trailing-comment line)     → exit 0 (A3c and A3d both quiet)
#   4 a synthetic section whose only '+' is a DROPPED expected line                 → exit 1 (A3c still refuses first)
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
A3C=${A3C:-$LM/tasks/code_patch/a3c_plus.py}
sec_of() { python3 -c "import json,sys; [print(o['file']) for o in json.load(open(sys.argv[1])) if sys.argv[2] in o['path']]" "$1" "$2" | tail -1; }
R1=$LM/runs/2026-09-15_ks1133-ornith35b-night
R2=$(ls -d $LM/runs/*ks794* | tail -1)
R3=$(ls -d $LM/runs/*ks999* | tail -1)
fail=0
out=$(python3 "$A3C" "$R1/input.json" "$(sec_of $R1/out.md.checker/sections.json openapi)"); rc=$?
n=$(printf '%s\n' "$out" | /usr/bin/grep -ci '^A3D ')
[ "$rc" -eq 2 ] && [ "$n" -eq 4 ] && echo "ARM1 PASS (rc=2, $n A3D lines)" || { echo "ARM1 FAIL (rc=$rc, $n lines)"; fail=1; }
out=$(python3 "$A3C" "$R2/input.json" "$(sec_of $R2/out.md.checker/sections.json openapi)"); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ARM2 PASS (rc=0, quiet)" || { echo "ARM2 FAIL (rc=$rc: $out)"; fail=1; }
out=$(python3 "$A3C" "$R3/input.json" "$(sec_of $R3/out.md.checker/sections.json userRepo)"); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ARM3 PASS (rc=0, quiet)" || { echo "ARM3 FAIL (rc=$rc: $out)"; fail=1; }
TMP=$(mktemp); printf '%s\n' '--- a/x.ts' '+++ b/x.ts' '@@ -1,1 +1,2 @@' ' unchanged line here' '+  nothing the brief asked for' > "$TMP"
out=$(python3 "$A3C" "$R2/input.json" "$TMP"); rc=$?
[ "$rc" -eq 1 ] && echo "ARM4 PASS (rc=1, dropped expected lines refused first)" || { echo "ARM4 FAIL (rc=$rc)"; fail=1; }
exit $fail

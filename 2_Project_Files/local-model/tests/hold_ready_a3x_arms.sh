#!/bin/bash
# hold_ready_a3x_arms.sh — arms for the 2026-10-20 fix: hold_ready accepts a code_patch2 PASS A3x line (diff=0 unmeasured=0
# ok==declared==measured) in place of PASS A3c. Usage: hold_ready_a3x_arms.sh [tool.py] [--old]   (default tool: night/hold_ready.py)
# --old inverts the GREEN arm (the OLD tool must REFUSE it, proving the arm can fail). All runs are --dry-run; scratch copies only
# (a fresh timestamped dir under $SCRATCH_ROOT each run; nothing is deleted, the real run dirs are never edited).
M=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
TOOL=${1:-$M/night/hold_ready.py}; OLD=0; [ "$2" = "--old" ] && OLD=1
SCRATCH_ROOT=${SCRATCH_ROOT:-/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2a56ac36-e9ca-49f4-8d2d-f02d4a53f9ed/scratchpad/a3x_arms}
S=$SCRATCH_ROOT/$(date +%H%M%S)_$$; mkdir -p "$S"
R=$M/runs/spark_secuura_2026-10-20_ks_1157_p1; G=$R-control; B=$M/night/briefs/ks_1157_p1/KS-1157.md
fail=0
run() { python3 "$TOOL" "$1" "$2" "$3" "$4" --brief "$5" --dry-run 2>&1; }
ok()  { echo "ARM OK   $1"; }; bad() { echo "ARM FAIL $1"; fail=1; }
A3CMSG="no line starting 'PASS A3c '"
o=$(run "$R" "$G" OAUTHMINTEDBY-1 OAUTH-SESSION-MARKER "$B")
if [ $OLD = 1 ]; then
  if echo "$o" | grep -q "$A3CMSG"; then ok "OLD tool refuses green arm on the A3c line"; else bad "OLD tool did not refuse green arm: $(echo "$o"|head -1|cut -c1-200)"; fi
  exit $fail
fi
if echo "$o" | head -1 | grep -q '^DRY-RUN OK'; then ok "GREEN ks_1157_p1 code_patch2 passes dry-run"; else bad "GREEN: $(echo "$o"|tail -1|cut -c1-250)"; fi
cp -R "$R" "$S/d1"; sed -i '' 's/diff=0 unmeasured=0)/diff=1 unmeasured=0)/' "$S/d1/checker.out"
o=$(run "$S/d1" "$G" OAUTHMINTEDBY-1 OAUTH-SESSION-MARKER "$B"); echo "$o" | grep -q "^hold_ready: REFUSE.*A3x" && ok "RED A3x diff=1 refuses (A3x check)" || bad "RED diff=1: $(echo "$o"|cut -c1-160)"
cp -R "$R" "$S/u1"; sed -i '' 's/diff=0 unmeasured=0)/diff=0 unmeasured=1)/' "$S/u1/checker.out"
o=$(run "$S/u1" "$G" OAUTHMINTEDBY-1 OAUTH-SESSION-MARKER "$B"); echo "$o" | grep -q "^hold_ready: REFUSE.*A3x" && ok "RED A3x unmeasured=1 refuses (A3x check)" || bad "RED unmeasured=1: $(echo "$o"|cut -c1-160)"
cp -R "$R" "$S/n1"; grep -v '^PASS A3x ' "$R/checker.out" > "$S/n1/checker.out"
o=$(run "$S/n1" "$G" OAUTHMINTEDBY-1 OAUTH-SESSION-MARKER "$B"); echo "$o" | grep -q "^hold_ready: REFUSE.*A3x" && ok "RED A3x absent refuses (A3x check)" || bad "RED A3x absent: $(echo "$o"|cut -c1-160)"
# code_patch single-file: ks_1659_p1 has exactly one PASS A3c line; removed in the copy
R2=$M/runs/spark_secuura_2026-10-20_ks_1659_p1; cp -R "$R2" "$S/cp1"; grep -v '^PASS A3c ' "$R2/checker.out" > "$S/cp1/checker.out"
[ "$(grep -c '^PASS A3c ' "$R2/checker.out")" = 1 ] || bad "ks_1659_p1 expected exactly one A3c line"
o=$(run "$S/cp1" "$R2-control" X-1 X-T "$M/night/briefs/ks_1659_p1/KS-1659.md"); echo "$o" | grep -q "$A3CMSG" && ok "RED code_patch (ks_1659_p1, A3c removed) still refuses on A3c" || bad "RED code_patch: $(echo "$o"|cut -c1-200)"
echo "fail=$fail"; exit $fail

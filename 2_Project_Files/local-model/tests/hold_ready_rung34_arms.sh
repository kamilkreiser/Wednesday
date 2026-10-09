#!/bin/bash
# hold_ready_rung34_arms.sh — red-proof for hold_ready.py's rung-3 (code_patch2) and rung-4 (LOOSE brief) extensions.
# 2026-10-10. bash 3.2. stderr is never discarded (captured per arm and grepped). Writes ONLY under $S (scratchpad); every
# hold_ready call is --dry-run (no READY_* file is ever written). Exit 0 iff every arm behaved as expected.
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
S=${S:-/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/70516fb2-e224-445a-b489-df25a8722219/scratchpad/rung34_arms}
NEW=$L/night/hold_ready.py
PRE=$L/night/hold_ready.py.pre-1010-rung34
R=$L/runs
R3=$R/spark_secuura_2026-10-10_KS-1346-apigw-fail500-type-and-field-names
R3G=$R3-control-r2
B3=$L/night/briefs/KS-1346-apigw-fail500-type-and-field-names/KS-1346.md
R4=$R/spark_secuura_2026-10-10_KS-1410-apigw-audit-export-502-loose
R4G=$R4-control
B4=$L/night/briefs/KS-1410-apigw-audit-export-502-loose/KS-1410.md
mkdir -p "$S" || exit 9
FAILS=0
ok()  { echo "ARM $1: PASS — $2"; }
bad() { echo "ARM $1: FAIL — $2"; FAILS=$((FAILS+1)); }
# run <tag> <script> args... -> $S/<tag>.out/.err, sets RC
run() { tag=$1; scr=$2; shift 2; python3 "$scr" --dry-run "$@" >"$S/$tag.out" 2>"$S/$tag.err"; RC=$?; }
has() { grep -q -- "$2" "$1"; }

# ---- arm 1: both real runs ACCEPTED by the new script
run a1_r3 "$NEW" "$R3" "$R3G" APIGWFAIL500TYPES-1 --title-from-brief "$B3" --model-tag spark-dsv4flash
if [ $RC -eq 0 ] && has "$S/a1_r3.out" 'DRY-RUN OK' && has "$S/a1_r3.out" 'BRIEFED-CODEPATCH2-' && has "$S/a1_r3.out" 'spark-dsv4flash' && has "$S/a1_r3.out" 'touched=\[' ; then ok 1a "rung 3 accepted rc=0 (code_patch2 label, spark-dsv4flash tag)"; else bad 1a "rc=$RC; $(head -c 300 "$S/a1_r3.err")"; fi
run a1_r4 "$NEW" "$R4" "$R4G" AUDITEXPORT502-1 --title-from-brief "$B4" --model-tag spark-dsv4flash
if [ $RC -eq 0 ] && has "$S/a1_r4.out" 'DRY-RUN OK' && has "$S/a1_r4.out" 'BRIEFED-CODEPATCH-' && has "$S/a1_r4.out" 'bytes DIFFER'; then ok 1b "rung 4 accepted rc=0 (golden DIFFERS recorded)"; else bad 1b "rc=$RC; $(head -c 300 "$S/a1_r4.err")"; fi

# ---- arm 1c/1d: the HELD BODY says the right words. Scratch copy of the script with NIGHT_DIR pointed at a scratch dir (non-dry write lands there only).
mkdir -p "$S/fakenight"; rm -f "$S"/fakenight/READY_* 2>/dev/null
sed "s#^NIGHT_DIR = .*#NIGHT_DIR = '$S/fakenight'#" "$NEW" > "$S/hr_scratch.py"
python3 "$S/hr_scratch.py" "$R3" "$R3G" APIGWFAIL500TYPES-1 --title-from-brief "$B3" --model-tag spark-dsv4flash >"$S/a1c.out" 2>"$S/a1c.err"; rc3=$?
python3 "$S/hr_scratch.py" "$R4" "$R4G" AUDITEXPORT502-1 --title-from-brief "$B4" --model-tag spark-dsv4flash >"$S/a1d.out" 2>"$S/a1d.err"; rc4=$?
F3=$(ls "$S"/fakenight/READY_KS-1346-* 2>/dev/null | head -1); F4=$(ls "$S"/fakenight/READY_KS-1410-* 2>/dev/null | head -1)
if [ $rc3 -eq 0 ] && [ -n "$F3" ] && grep -q 'PER-FILE A3x' "$F3" && grep -q 'PASS A3x' "$F3" && grep -q 'code_patch2' "$F3"; then ok 1c "rung-3 body names code_patch2 + per-file A3x (scratch write)"; else bad 1c "rc=$rc3 file=$F3 $(head -c 200 "$S/a1c.err")"; fi
if [ $rc4 -eq 0 ] && [ -n "$F4" ] && grep -q 'LOOSE BRIEF: product lines written by the model, not byte-checked against the brief; reviewer reads the hunk' "$F4" && grep -q 'bytes DIFFER' "$F4"; then ok 1d "rung-4 body carries the LOOSE BRIEF sentence + golden verdict (scratch write)"; else bad 1d "rc=$rc4 file=$F4 $(head -c 200 "$S/a1d.err")"; fi

# ---- arm 2: the PRE copy refuses both (control: the old rule really refused)
run a2_r3 "$PRE" "$R3" "$R3G" APIGWFAIL500TYPES-1 --title-from-brief "$B3" --model-tag spark-dsv4flash
if [ $RC -eq 2 ] && has "$S/a2_r3.err" 'REFUSE — touched'; then ok 2a "PRE refuses rung 3 rc=2 ('touched …')"; else bad 2a "rc=$RC; $(head -c 300 "$S/a2_r3.err")"; fi
run a2_r4 "$PRE" "$R4" "$R4G" AUDITEXPORT502-1 --title-from-brief "$B4" --model-tag spark-dsv4flash
if [ $RC -eq 2 ] && has "$S/a2_r4.err" "has no line starting 'PASS A3c '"; then ok 2b "PRE refuses rung 4 rc=2 (no PASS A3c)"; else bad 2b "rc=$RC; $(head -c 300 "$S/a2_r4.err")"; fi

# ---- arm 3: rung-3 run dir copy with ONE 'PASS A3x' line removed -> REFUSED
rm -rf "$S/r3copy"; cp -R "$R3" "$S/r3copy" || bad 3 "copy failed"
grep -v '^PASS A3x ' "$R3/checker.out" > "$S/r3copy/checker.out"
run a3 "$NEW" "$S/r3copy" "$R3G" APIGWFAIL500TYPES-1 --title-from-brief "$B3" --model-tag spark-dsv4flash
if [ $RC -eq 2 ] && has "$S/a3.err" 'REFUSE — code_patch2: expected exactly ONE `PASS A3x`'; then ok 3a "A3x line removed -> REFUSED rc=2"; else bad 3a "rc=$RC; $(head -c 300 "$S/a3.err")"; fi
# 3b: A3x line present but one per-file OK line removed from brief_bytes.out -> REFUSED
rm -rf "$S/r3copyb"; cp -R "$R3" "$S/r3copyb"
grep -v "^OK .*/batch.ts " "$R3/out.md.checker/brief_bytes.out" > "$S/r3copyb/out.md.checker/brief_bytes.out"
run a3b "$NEW" "$S/r3copyb" "$R3G" APIGWFAIL500TYPES-1 --title-from-brief "$B3" --model-tag spark-dsv4flash
if [ $RC -eq 2 ] && has "$S/a3b.err" 'no `OK <file>` line for declared product'; then ok 3b "per-file OK line removed -> REFUSED rc=2"; else bad 3b "rc=$RC; $(head -c 300 "$S/a3b.err")"; fi
# 3c: brief with one product File: line removed (count mismatch vs declared products) -> REFUSED
grep -v '^File:.*batch\.ts' "$B3" > "$S/B3_nobatch.md"
run a3c "$NEW" "$R3" "$R3G" APIGWFAIL500TYPES-1 --title-from-brief "$S/B3_nobatch.md" --model-tag spark-dsv4flash
if [ $RC -eq 2 ] && has "$S/a3c.err" "not exactly the declared products"; then ok 3c "brief File: count != declared products -> REFUSED rc=2"; else bad 3c "rc=$RC; $(head -c 300 "$S/a3c.err")"; fi
# 3d: no brief given at all for a code_patch2 run -> REFUSED (the File: count cannot be made)
run a3d "$NEW" "$R3" "$R3G" APIGWFAIL500TYPES-1 NOTIFICATIONS --model-tag spark-dsv4flash
if [ $RC -eq 2 ] && has "$S/a3d.err" 'needs --title-from-brief or --brief'; then ok 3d "code_patch2 without a brief -> REFUSED rc=2"; else bad 3d "rc=$RC; $(head -c 300 "$S/a3d.err")"; fi

# ---- arm 4: rung-4 with the loose declaration removed (scratch copy of the brief, no spark.pins beside it) -> REFUSED at A3c
mkdir -p "$S/b4"; rm -f "$S"/b4/*
sed -e 's/(a LOOSER brief/(a stricter brief/' -e 's/RUNG 4, code_patch/RUNG 4X, code_patch/' "$B4" > "$S/b4/KS-1410.md"
if grep -qiE 'rung:?[ *]*4[ *]*\([ ]*(a )?looser brief' "$S/b4/KS-1410.md"; then bad 4-setup "declaration still present in the scratch brief"; fi
run a4 "$NEW" "$R4" "$R4G" AUDITEXPORT502-1 --title-from-brief "$S/b4/KS-1410.md" --model-tag spark-dsv4flash
if [ $RC -eq 2 ] && has "$S/a4.err" "has no line starting 'PASS A3c '"; then ok 4a "loose declaration removed -> REFUSED at A3c rc=2"; else bad 4a "rc=$RC; $(head -c 300 "$S/a4.err")"; fi
# 4b: declaration present but `INFO A3i skipped` removed from checker.out -> REFUSED
rm -rf "$S/r4copy"; cp -R "$R4" "$S/r4copy"
grep -v '^INFO A3i skipped' "$R4/checker.out" > "$S/r4copy/checker.out"
run a4b "$NEW" "$S/r4copy" "$R4G" AUDITEXPORT502-1 --title-from-brief "$B4" --model-tag spark-dsv4flash
if [ $RC -eq 2 ] && has "$S/a4b.err" "has no line starting 'PASS A3c '"; then ok 4b "A3i-skipped line removed -> REFUSED rc=2"; else bad 4b "rc=$RC; $(head -c 300 "$S/a4b.err")"; fi
# 4c: declaration present, but an A5 line removed from checker.out -> REFUSED (A4-A7 must have passed)
grep -v '^PASS A5 ' "$R4/checker.out" > "$S/r4copy/checker.out"
run a4c "$NEW" "$S/r4copy" "$R4G" AUDITEXPORT502-1 --title-from-brief "$B4" --model-tag spark-dsv4flash
if [ $RC -eq 2 ] && has "$S/a4c.err" "A5"; then ok 4c "PASS A5 removed -> REFUSED rc=2"; else bad 4c "rc=$RC; $(head -c 300 "$S/a4c.err")"; fi
# 4d: the loose escape must NOT open for a run with no brief given (declaration unreadable) -> REFUSED
run a4d "$NEW" "$R4" "$R4G" AUDITEXPORT502-1 AUDIT-EXPORT --model-tag spark-dsv4flash
if [ $RC -eq 2 ] && has "$S/a4d.err" "has no line starting 'PASS A3c '"; then ok 4d "no brief given -> loose not honoured, REFUSED rc=2"; else bad 4d "rc=$RC; $(head -c 300 "$S/a4d.err")"; fi

# ---- arm 5: regression — PRE vs NEW give the same rc + stdout + stderr (clock-normalised) on every earlier-shaped run found.
# (The four existing hold_ready arms files under tests/ are .md transcripts, not runnable; this loop is their re-execution
# surface: code_patch, test_only, bash_patch, doc_patch and Spark runs, accepted OR refused, must behave identically.)
norm() { sed -e 's/from `ls` at [0-9:]* [0-9-]*/from ls at CLOCK/g' "$1"; }
N=0; D=0; C2=0
for d in "$R"/2026-09-22_ks1265-ornith35b-night "$R"/2026-09-22_ks947-ornith35b-night2 "$R"/2026-09-22_ks1139-ornith35b-night \
         "$R"/2026-09-22_ks1097-ornith35b-night2 "$R"/2026-09-22_ks1034-ornith35b-night "$R"/2026-09-22_ks1028-ornith35b-night \
         "$R"/2026-09-22_feed8-drafter-precheck "$R"/2026-09-22_feed3-drafter-precheck "$R"/2026-09-22_feed9-drafter-precheck \
         "$R"/spark_secuura_2026-10-07_KS-1139-smoke-test-counters-errexit "$R"/spark_*; do
  [ -d "$d/out.md.checker" ] || continue
  case "$d" in "$R3"|"$R4"|"$R3G"|"$R4G") continue;; esac
  N=$((N+1)); n=$(basename "$d")
  python3 "$PRE" --dry-run "$d" - TESTROW-1 TESTTITLE --model-tag spark-dsv4flash >"$S/p_$N.out" 2>"$S/p_$N.err"; rp=$?
  python3 "$NEW" --dry-run "$d" - TESTROW-1 TESTTITLE --model-tag spark-dsv4flash >"$S/n_$N.out" 2>"$S/n_$N.err"; rn=$?
  norm "$S/p_$N.out" > "$S/p_$N.o2"; norm "$S/n_$N.out" > "$S/n_$N.o2"
  if [ $rp -eq $rn ] && cmp -s "$S/p_$N.o2" "$S/n_$N.o2" && cmp -s "$S/p_$N.err" "$S/n_$N.err"; then :
  elif [ $rp -eq 2 ] && [ $rn -eq 2 ] && grep -q 'REFUSE — touched' "$S/p_$N.err" && grep -q 'REFUSE — code_patch2: needs --title-from-brief' "$S/n_$N.err"; then
    C2=$((C2+1)); echo "  note: $n is a code_patch2 run — refused before (touched) and still refused now (no brief given; message differs by design)"
  else D=$((D+1)); echo "  regression DIFF on $n: pre rc=$rp new rc=$rn"; fi
done
if [ $N -ge 5 ] && [ $D -eq 0 ]; then ok 5 "$N earlier runs: PRE and NEW identical (rc, stdout, stderr), except $C2 code_patch2 runs refused by both (message differs: brief required)"; else bad 5 "$N runs compared, $D differ"; fi

echo "TOTAL FAILS=$FAILS"
[ $FAILS -eq 0 ]

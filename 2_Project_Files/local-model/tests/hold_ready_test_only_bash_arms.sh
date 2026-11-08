#!/bin/bash
# hold_ready_test_only_bash_arms.sh - red-proof for hold_ready.py's 2026-11-09 test_only_bash path (Spark tier, commit f804b8eb95).
# bash 3.2. stderr never discarded (captured per arm and grepped). Writes ONLY under $S (scratchpad); never edits a real run dir; never
# deletes. EVERY hold_ready call is --dry-run, so no READY_* file is written to night/ (Wednesday runs the real holds). Exit 0 iff all arms behaved.
#   NEW = script under test (default night/hold_ready.py)   OLD = pre-change copy (default night/hold_ready.py.pre-1109-bashhold)
#   RUN_EXISTING=1 (OFF by default, 20+ min) also runs the existing hold_ready arms. NOTE (2026-11-09): rung34 arms 1b 1d 4a 4b 4c 4d 5 and a3x GREEN are RED at
#   BASELINE (the pre-change script fails the identical set; cause: the 2026-11-03 STRICT-APPLY leg). So E-arms report PASS/FAIL as found; judge them by
#   comparing against the pre-change script, not by absolute rc. The 2026-11-09 comparison: tests/hold_ready_test_only_bash_arms.md notes are in the commission wrap.
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
S=${S:-/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/121f796c-56a6-4f7c-83fc-ac8bf3fbcbfe/scratchpad/tob_arms}
NEW=${NEW:-$L/night/hold_ready.py}
OLD=${OLD:-$L/night/hold_ready.py.pre-1109-bashhold}
RUN_EXISTING=${RUN_EXISTING:-0}
R=$L/runs
A=$R/spark_secuura_2026-11-09_ks_2129_o112_p1_ks1728_scanner_misses_five_spellings_of_the_closed_pipe_fault
B=$R/spark_secuura_2026-11-09_ks_2130_o112_p1_ks1547_abort_sentence_pinned_whole
TI=$R/spark_secuura_2026-11-08_ks_2005_o103_p3_seed_demo_users_one_created
TIG=$TI-control
SEAT='Wednesday 2026-11-09 (read at source)'
mkdir -p "$S" || exit 9
FAILS=0
ok()  { echo "ARM $1: PASS - $2"; }
bad() { echo "ARM $1: FAIL - $2"; FAILS=$((FAILS+1)); }
run() { tag=$1; scr=$2; shift 2; python3 "$scr" --dry-run "$@" >"$S/$tag.out" 2>"$S/$tag.err"; RC=$?; }
has() { grep -q -F -- "$2" "$1"; }
fixture() {   # fixture <src-run-dir> <name> : a copy under $S whose text files name the COPY (sections.json etc.)
  local dst="$S/$2"
  if [ -e "$dst" ]; then dst="$S/$2-$$"; fi
  cp -R "$1" "$dst" || { echo "copy failed: $1" >&2; return 1; }
  python3 - "$1" "$dst" <<'PY'
import os, sys
src, dst = sys.argv[1], sys.argv[2]
for root, _, files in os.walk(dst):
    for f in files:
        p = os.path.join(root, f)
        if os.path.getsize(p) > 20_000_000: continue
        try: t = open(p, encoding='utf-8').read()
        except Exception: continue
        if src in t: open(p, 'w', encoding='utf-8').write(t.replace(src, dst))
PY
  FX="$dst"
}

# ---- T1/T2: the two real runs HOLD (dry-run; no READY written)
run t1 "$NEW" "$A" - KS-2129-O112-P1 PACKAGE-FORMAT-FIVE-SPELLINGS --seat "$SEAT"
if [ $RC -eq 0 ] && has "$S/t1.out" 'DRY-RUN OK' && has "$S/t1.out" '_spark-dsv4flash_BRIEFED-TESTONLYBASH-' && has "$S/t1.out" 'kind=test_only_bash/plant' && has "$S/t1.out" 'red_cells=5 products_unchanged=1 plant_unchanged=5' && has "$S/t1.out" 'BYTE-IDENTICAL'; then ok T1 "KS-2129 (ks_2129_o112_p1) HOLDS rc=0, default tag spark-dsv4flash, 5 red cells, 5 plant files unchanged"; else bad T1 "rc=$RC; $(head -c 300 "$S/t1.err")"; fi
run t2 "$NEW" "$B" - KS-2130-O112-P1 PREFLIGHT-ABORT-SENTENCE-WHOLE --seat "$SEAT"
if [ $RC -eq 0 ] && has "$S/t2.out" 'DRY-RUN OK' && has "$S/t2.out" '_spark-dsv4flash_BRIEFED-TESTONLYBASH-' && has "$S/t2.out" 'red_cells=1 products_unchanged=1 plant_unchanged=1'; then ok T2 "KS-2130 (ks_2130_o112_p1) HOLDS rc=0, 1 red cell, plant file unchanged"; else bad T2 "rc=$RC; $(head -c 300 "$S/t2.err")"; fi
run t2b "$NEW" "$B" - KS-2130-O112-P1 PREFLIGHT-ABORT-SENTENCE-WHOLE --model-tag spark-dsv4flash --seat "$SEAT"
if [ $RC -eq 0 ] && has "$S/t2b.out" '_spark-dsv4flash_BRIEFED-TESTONLYBASH-'; then ok T2b "explicit --model-tag accepted on test_only_bash (the original refusal is gone)"; else bad T2b "rc=$RC; $(head -c 300 "$S/t2b.err")"; fi
run t2c "$OLD" "$B" - KS-2130-O112-P1 PREFLIGHT-ABORT-SENTENCE-WHOLE --model-tag spark-dsv4flash --seat "$SEAT"
if [ $RC -ne 0 ] && has "$S/t2c.err" 'neither'; then ok T2c "control: the PRE-change script refuses the same run (rc=$RC, 'neither') - the arms can fail"; else bad T2c "pre-change script did not refuse: rc=$RC; $(head -c 300 "$S/t2c.err")"; fi

# ---- T3: touched set includes a product file -> REFUSED
# T3a: sections.json (the checker's own touched set) also lists the product
fixture "$B" spark_secuura_2026-11-09_ks_2130_armT3a || bad T3a-setup "fixture"
python3 - "$FX" <<'PY'
import json, sys
fx = sys.argv[1]; c = fx + '/out.md.checker/'
inp = json.load(open(fx + '/input.json')); prod = inp['product_files'][0]
s = json.load(open(c + 'sections.json')); s.append({"n": 2, "path": prod, "file": c + 'section_1.diff', "new": False, "delete": False})
json.dump(s, open(c + 'sections.json', 'w'), indent=1)
PY
run t3a "$NEW" "$FX" - KS-2130-O112-P1 PREFLIGHT-ABORT-SENTENCE-WHOLE --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/t3a.err" 'REFUSE' && has "$S/t3a.err" 'sections.json'; then ok T3a "sections.json touched set includes the product -> REFUSED rc=2"; else bad T3a "rc=$RC; $(head -c 300 "$S/t3a.err")"; fi
# T3b: patch.diff itself carries a real, strictly applying hunk on the product (out.md fence kept byte-equal)
fixture "$B" spark_secuura_2026-11-09_ks_2130_armT3b || bad T3b-setup "fixture"
python3 - "$FX" <<'PY'
import json, subprocess, sys, os
fx = sys.argv[1]; c = fx + '/out.md.checker/'
inp = json.load(open(fx + '/input.json')); prod = inp['product_files'][0]; tip = inp['tip']
src = inp['source_checkout']
a = subprocess.run(['git', '-C', src, 'show', f'{tip}:{prod}'], capture_output=True, text=True, check=True).stdout
open(fx + '/prod_a.txt', 'w').write(a); open(fx + '/prod_b.txt', 'w').write(a + '# extra\n')
d = subprocess.run(['diff', '-u', '-L', f'a/{prod}', '-L', f'b/{prod}', fx + '/prod_a.txt', fx + '/prod_b.txt'], capture_output=True, text=True).stdout
assert d.startswith('--- a/'), d[:80]
pt = open(c + 'patch.diff').read(); pt2 = pt + d
open(c + 'patch.diff', 'w').write(pt2)
om = open(fx + '/out.md').read()
om2 = om.replace('```diff\n' + pt.rstrip('\n') + '\n```', '```diff\n' + pt2.rstrip('\n') + '\n```')
assert om2 != om; open(fx + '/out.md', 'w').write(om2)
PY
run t3b "$NEW" "$FX" - KS-2130-O112-P1 PREFLIGHT-ABORT-SENTENCE-WHOLE --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/t3b.err" 'REFUSE' && has "$S/t3b.err" 'TOUCHED SET'; then ok T3b "patch.diff with a strict product hunk -> REFUSED rc=2 ($(grep -o 'TOUCHED SET[^.]\{0,60\}' "$S/t3b.err" | head -1))"; else bad T3b "rc=$RC; $(head -c 300 "$S/t3b.err")"; fi

# ---- T4: no red evidence -> REFUSED
fixture "$B" spark_secuura_2026-11-09_ks_2130_armT4a || bad T4a-setup "fixture"
grep -v '^PASS A5 ' "$B/checker.out" > "$FX/checker.out"
run t4a "$NEW" "$FX" - KS-2130-O112-P1 PREFLIGHT-ABORT-SENTENCE-WHOLE --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/t4a.err" 'NO RED EVIDENCE' && has "$S/t4a.err" "'A5'"; then ok T4a "checker.out without the A5 RED-WITH-PLANT leg -> REFUSED rc=2"; else bad T4a "rc=$RC; $(head -c 300 "$S/t4a.err")"; fi
fixture "$B" spark_secuura_2026-11-09_ks_2130_armT4b || bad T4b-setup "fixture"
for f in "$FX"/out.md.checker/red_with_plant__*.out; do sed -e 's/^FAIL /ok   /' "$f" > "$f.new" && mv "$f.new" "$f"; done
run t4b "$NEW" "$FX" - KS-2130-O112-P1 PREFLIGHT-ABORT-SENTENCE-WHOLE --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/t4b.err" 'NO RED EVIDENCE: no FAIL line under the plant'; then ok T4b "A5 leg present but the plant output holds no FAIL line for the red cell -> REFUSED rc=2"; else bad T4b "rc=$RC; $(head -c 300 "$S/t4b.err")"; fi
fixture "$B" spark_secuura_2026-11-09_ks_2130_armT4c || bad T4c-setup "fixture"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); d["red_cells"]=[]; json.dump(d, open(sys.argv[1], "w"), indent=1)' "$FX/input.json"
run t4c "$NEW" "$FX" - KS-2130-O112-P1 PREFLIGHT-ABORT-SENTENCE-WHOLE --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/t4c.err" 'NO RED EVIDENCE: plant-shape input.json has no red_cells'; then ok T4c "input.json with no red_cells -> REFUSED rc=2 (NO RED EVIDENCE)"; else bad T4c "rc=$RC; $(head -c 300 "$S/t4c.err")"; fi

# ---- T5: other guards
fixture "$B" spark_secuura_2026-11-09_ks_2130_armT5a || bad T5a-setup "fixture"
sed -e '1s#^mode: test_only_bash/plant#mode: code_patch#' "$B/checker.out" > "$FX/checker.out"
run t5a "$NEW" "$FX" - KS-2130-O112-P1 PREFLIGHT-ABORT-SENTENCE-WHOLE --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/t5a.err" 'test_only_bash signals disagree'; then ok T5a "input tier test_only_bash but checker mode code_patch -> REFUSED rc=2 (signals disagree)"; else bad T5a "rc=$RC; $(head -c 300 "$S/t5a.err")"; fi
fixture "$B" spark_secuura_2026-11-09_ks_2130_armT5b || bad T5b-setup "fixture"
sed -e 's#^PASS A2 the diff applies at the tip (strict)#PASS A2 the diff applies at the tip (--recount accommodation)#' "$B/checker.out" > "$FX/checker.out"
run t5b "$NEW" "$FX" - KS-2130-O112-P1 PREFLIGHT-ABORT-SENTENCE-WHOLE --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/t5b.err" 'A2 line is not strict'; then ok T5b "A2 passed only with an accommodation -> REFUSED rc=2"; else bad T5b "rc=$RC; $(head -c 300 "$S/t5b.err")"; fi
fixture "$B" spark_secuura_2026-11-09_ks_2130_armT5c || bad T5c-setup "fixture"
sed -e 's#^RESULT: PASS#RESULT: FAIL#' "$B/checker.out" > "$FX/checker.out"
run t5c "$NEW" "$FX" - KS-2130-O112-P1 PREFLIGHT-ABORT-SENTENCE-WHOLE --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/t5c.err" 'RESULT is not PASS'; then ok T5c "RESULT not PASS -> REFUSED rc=2"; else bad T5c "rc=$RC; $(head -c 300 "$S/t5c.err")"; fi

# ---- T6: EXPECT shape (SYNTHETIC fixture built from the KS-2130 run: no real expect-shape run exists yet)
fixture "$B" spark_secuura_2026-11-09_ks_2130_armT6 || bad T6-setup "fixture"
python3 - "$FX" "$B" <<'PY'
import json, re, sys
fx, src = sys.argv[1], sys.argv[2]
d = json.load(open(fx + '/input.json')); d['mode'] = 'expect'; d['plant_diff'] = None; d['plant'] = []; d['red_cells'] = []
d['expect'] = [{'kind': 'present', 'text': 'x'}, {'kind': 'absent', 'text': 'y'}]
json.dump(d, open(fx + '/input.json', 'w'), indent=1)
out = []
for l in open(src + '/checker.out').read().splitlines():
    if l.startswith('mode: '): l = "mode: test_only_bash/expect (declared suites ['t']; read-only ['p']; 2 expectation(s); red cells none)"
    if l.startswith('PASS A3p'): l = 'PASS A4b RED AT BASE: all 2 expectation(s) fail on the untouched tip\'s suite output'
    if l.startswith('PASS A5 '): l = 'PASS A4e EXPECTATIONS AFTER: all 2 expectation(s) hold on the patched suite\'s output\nPASS A7 REVERSION: with the patch reverse-applied, 2/2 expectation(s) fail again (the check discriminates)'
    out.append(l)
open(fx + '/checker.out', 'w').write('\n'.join(out) + '\n')
PY
run t6 "$NEW" "$FX" - KS-2130-O112-P1 PREFLIGHT-ABORT-SENTENCE-WHOLE --seat "$SEAT"
if [ $RC -eq 0 ] && has "$S/t6.out" 'kind=test_only_bash/expect'; then ok T6 "SYNTHETIC expect-shape (A4b/A4e/A7) accepted rc=0"; else bad T6 "rc=$RC; $(head -c 300 "$S/t6.err")"; fi
fixture "$FX" spark_secuura_2026-11-09_ks_2130_armT6b || bad T6b-setup "fixture"
grep -v '^PASS A7 ' "$FX/checker.out" > "$FX/checker.out.new" && mv "$FX/checker.out.new" "$FX/checker.out"
run t6b "$NEW" "$FX" - KS-2130-O112-P1 PREFLIGHT-ABORT-SENTENCE-WHOLE --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/t6b.err" 'NO RED EVIDENCE' && has "$S/t6b.err" "'A7'"; then ok T6b "SYNTHETIC expect-shape without the A7 reversion leg -> REFUSED rc=2"; else bad T6b "rc=$RC; $(head -c 300 "$S/t6b.err")"; fi

# ---- R: regression - a test_only_input dry-run is byte-identical NEW vs OLD (a path the change must not touch)
run r1n "$NEW" "$TI" "$TIG" KS-2005-O103-P3 SEED-DEMO-USERS-ONE-CREATED-CELL --seat "$SEAT"; RN=$RC
run r1o "$OLD" "$TI" "$TIG" KS-2005-O103-P3 SEED-DEMO-USERS-ONE-CREATED-CELL --seat "$SEAT"; RO=$RC
if [ $RN -eq 0 ] && has "$S/r1n.out" 'DRY-RUN OK' && [ $RN -eq $RO ] && cmp -s "$S/r1n.out" "$S/r1o.out" && cmp -s "$S/r1n.err" "$S/r1o.err"; then ok R1 "test_only_input dry-run identical NEW vs pre-change (rc $RN, stdout+stderr byte-equal)"; else bad R1 "rc new=$RN old=$RO; diff: $(diff "$S/r1n.out" "$S/r1o.out" | head -c 200)"; fi

# ---- E: the existing hold_ready arms still pass
if [ "$RUN_EXISTING" = 1 ]; then
  for k in rung34 loose_recount a3x holdkinds; do
    case $k in
      a3x) SCRATCH_ROOT="$S/ex" S="$S/ex/$k" bash "$L/tests/hold_ready_${k}_arms.sh" >"$S/ex_$k.out" 2>"$S/ex_$k.err" ;;
      *)   mkdir -p "$S/ex/$k"; S="$S/ex/$k" bash "$L/tests/hold_ready_${k}_arms.sh" >"$S/ex_$k.out" 2>"$S/ex_$k.err" ;;
    esac
    RC=$?
    nf=$(grep -c -E '^ARM .*: FAIL|^FAIL' "$S/ex_$k.out")
    if [ $RC -eq 0 ] && [ "$nf" = 0 ]; then ok "E-$k" "existing arms hold_ready_${k}_arms.sh rc=0, 0 FAIL ($(grep -c -E '^ARM .*: PASS' "$S/ex_$k.out") ARM PASS lines)"; else bad "E-$k" "rc=$RC FAIL-lines=$nf; $(tail -3 "$S/ex_$k.out" | head -c 300)"; fi
  done
fi
echo "ARMS DONE: $FAILS failing arm(s)"
[ "$FAILS" -eq 0 ]

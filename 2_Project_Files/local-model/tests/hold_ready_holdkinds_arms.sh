#!/bin/bash
# hold_ready_holdkinds_arms.sh — red-proof for hold_ready.py's 2026-10-18 extension to two Spark run kinds it refused with
# "checker.out has no 'mode: code_patch' line": (1) bash_patch2 (rung 3, tasks/bash_patch2/checker.sh, `mode: bash_patch2`)
# and (2) test_only through code_patch's checker (spark round.sh tier test_only: night/build_input.sh's `## Tamper` block ->
# defect_line.tamper, tasks/code_patch/checker.sh MODE=test_only, `mode: test_only (tamper at <product>:<line>)`).
# bash 3.2. stderr never discarded (captured per arm and grepped). Writes ONLY under $S (scratchpad); never modifies a real
# run dir; never deletes. Every hold_ready call is --dry-run (no READY_* file is written). Exit 0 iff every arm behaved.
#   NEW  = the script under test (default night/hold_ready.py)
#   OLD  = the pre-change copy (default night/hold_ready.py.pre-1018-holdkinds) — for the regression loop K6
#   BASE = the rung34 arms output captured BEFORE the change (for K7: the existing arms must not get worse)
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
S=${S:-/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/59f676bc-e3a9-4b9a-8b25-64e572c78937/scratchpad/holdkinds_arms}
NEW=${NEW:-$L/night/hold_ready.py}
OLD=${OLD:-$L/night/hold_ready.py.pre-1018-holdkinds}
BASE=${BASE:-/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/59f676bc-e3a9-4b9a-8b25-64e572c78937/scratchpad/base/rung34.out}
R=$L/runs; BR=$L/night/briefs
B2=$R/spark_secuura_2026-10-18_ks_1490_p1;  B2G=$B2-control-r2;  B2B=$BR/ks_1490_p1/KS-1490.md
T2=$R/spark_secuura_2026-10-18_ks_1619_p2;  T2G=$T2-control-r3;  T2B=$BR/ks_1619_p2/KS-1619.md
T1=$R/spark_secuura_2026-10-18_ks_1619_p1;  T1G=$T1-control-r2;  T1B=$BR/ks_1619_p1/KS-1619.md
SEAT='Wednesday 2026-10-18 (read at source)'
mkdir -p "$S" || exit 9
FAILS=0
ok()  { echo "ARM $1: PASS — $2"; }
bad() { echo "ARM $1: FAIL — $2"; FAILS=$((FAILS+1)); }
run() { tag=$1; scr=$2; shift 2; python3 "$scr" --dry-run "$@" >"$S/$tag.out" 2>"$S/$tag.err"; RC=$?; }
has() { grep -q -F -- "$2" "$1"; }
# fixture <src-run-dir> <name> : a copy under $S whose text files name the COPY, not the original (sections.json etc.)
fixture() {
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

# ---- K1-K3: each new kind ACCEPTED on its real run dir (dry-run)
run k1 "$NEW" "$B2" "$B2G" TRAILINGSLASH-1 --title-from-brief "$B2B" --seat "$SEAT"
if [ $RC -eq 0 ] && has "$S/k1.out" 'DRY-RUN OK' && has "$S/k1.out" '_spark-dsv4flash_BRIEFED-BASHPATCH2-' && has "$S/k1.out" 'kind=bash_patch2'; then ok K1 "bash_patch2 ks_1490_p1 accepted rc=0 ($(head -1 "$S/k1.out" | cut -c1-140))"; else bad K1 "rc=$RC; $(head -c 300 "$S/k1.err")"; fi
run k2 "$NEW" "$T2" "$T2G" THREETENANT-2 --title-from-brief "$T2B" --seat "$SEAT"
if [ $RC -eq 0 ] && has "$S/k2.out" 'DRY-RUN OK' && has "$S/k2.out" '_spark-dsv4flash_BRIEFED-TESTONLY-' && has "$S/k2.out" 'kind=test_only product_unchanged=True'; then ok K2 "test_only ks_1619_p2 accepted rc=0 ($(head -1 "$S/k2.out" | cut -c1-140))"; else bad K2 "rc=$RC; $(head -c 300 "$S/k2.err")"; fi
run k3 "$NEW" "$T1" "$T1G" MULTICHUNK-1 --title-from-brief "$T1B" --seat "$SEAT"
if [ $RC -eq 0 ] && has "$S/k3.out" 'DRY-RUN OK' && has "$S/k3.out" '_spark-dsv4flash_BRIEFED-TESTONLY-' && has "$S/k3.out" 'kind=test_only product_unchanged=True'; then ok K3 "test_only ks_1619_p1 accepted rc=0 ($(head -1 "$S/k3.out" | cut -c1-140))"; else bad K3 "rc=$RC; $(head -c 300 "$S/k3.err")"; fi

# ---- K4: test_only runs that must be REFUSED
# K4a: the touched set (numstat.out, the checker's own) includes the product
fixture "$T2" spark_secuura_2026-10-18_ks_1619_p2-armK4a || bad K4a-setup "fixture"
P2=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["product_file"])' "$T2/input.json")
printf '1\t1\t%s\n' "$P2" >> "$FX/out.md.checker/numstat.out"
run k4a "$NEW" "$FX" "$T2G" THREETENANT-2 --title-from-brief "$T2B" --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/k4a.err" 'REFUSE — test_only: the product (tamper target)' && has "$S/k4a.err" 'is in the touched set'; then ok K4a "test_only with the product in numstat's touched set -> REFUSED rc=2"; else bad K4a "rc=$RC; $(head -c 300 "$S/k4a.err")"; fi
# K4b: numstat says one file, but the checker's sections carry a product section (the diff names the product)
fixture "$T2" spark_secuura_2026-10-18_ks_1619_p2-armK4b || bad K4b-setup "fixture"
python3 - "$FX" "$P2" <<'PY'
import json, sys
fx, prod = sys.argv[1], sys.argv[2]; c = fx + '/out.md.checker/'
open(c + 'section_2.diff', 'w').write(f"--- a/{prod}\n+++ b/{prod}\n@@ -1,1 +1,1 @@\n-x\n+y\n")
open(c + 'section_2.opts', 'w').write(c + 'section_2.diff\n\n'); open(c + 'apply_check_strict_2.out', 'w').write('')
s = json.load(open(c + 'sections.json')); s.append({"n": 2, "path": prod, "file": c + 'section_2.diff', "hunks": 1, "miscount": 0})
json.dump(s, open(c + 'sections.json', 'w'), indent=1)
PY
run k4b "$NEW" "$FX" "$T2G" THREETENANT-2 --title-from-brief "$T2B" --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/k4b.err" 'REFUSE — test_only:' && has "$S/k4b.err" 'section'; then ok K4b "test_only whose sections name the product -> REFUSED rc=2"; else bad K4b "rc=$RC; $(head -c 300 "$S/k4b.err")"; fi
# K4c: input carries the tamper, but the checker's mode line says code_patch (signals disagree)
fixture "$T2" spark_secuura_2026-10-18_ks_1619_p2-armK4c || bad K4c-setup "fixture"
sed -e '1s/^mode: test_only .*/mode: code_patch/' "$T2/checker.out" > "$FX/checker.out"
run k4c "$NEW" "$FX" "$T2G" THREETENANT-2 --title-from-brief "$T2B" --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/k4c.err" 'test_only signals disagree'; then ok K4c "tamper in input, checker mode code_patch -> REFUSED rc=2"; else bad K4c "rc=$RC; $(head -c 300 "$S/k4c.err")"; fi
# K4d: checker says test_only, but the input carries no tamper (signals disagree)
fixture "$T2" spark_secuura_2026-10-18_ks_1619_p2-armK4d || bad K4d-setup "fixture"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); del d["defect_line"]["tamper"]; json.dump(d, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)' "$FX/input.json"
run k4d "$NEW" "$FX" "$T2G" THREETENANT-2 --title-from-brief "$T2B" --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/k4d.err" 'test_only signals disagree'; then ok K4d "checker test_only, no tamper in input -> REFUSED rc=2"; else bad K4d "rc=$RC; $(head -c 300 "$S/k4d.err")"; fi
# K4e: the mode line names a tamper target that is NOT the input's product_file
fixture "$T2" spark_secuura_2026-10-18_ks_1619_p2-armK4e || bad K4e-setup "fixture"
sed -e '1s#(tamper at [^:]*:#(tamper at Blockchain/Dev/services/originate/src/routes/other.ts:#' "$T2/checker.out" > "$FX/checker.out"
run k4e "$NEW" "$FX" "$T2G" THREETENANT-2 --title-from-brief "$T2B" --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/k4e.err" 'REFUSE — test_only: checker.out mode line'; then ok K4e "mode line names another tamper target -> REFUSED rc=2"; else bad K4e "rc=$RC; $(head -c 300 "$S/k4e.err")"; fi
# K4f: round.json says the round was a different tier
fixture "$T2" spark_secuura_2026-10-18_ks_1619_p2-armK4f || bad K4f-setup "fixture"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); d["tier"]="code_patch"; json.dump(d, open(sys.argv[1], "w"), indent=1)' "$FX/round.json"
run k4f "$NEW" "$FX" "$T2G" THREETENANT-2 --title-from-brief "$T2B" --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/k4f.err" 'test_only signals disagree'; then ok K4f "round.json tier code_patch on a test_only run -> REFUSED rc=2"; else bad K4f "rc=$RC; $(head -c 300 "$S/k4f.err")"; fi

# ---- K5: bash_patch2 runs that must be REFUSED
# K5a: a declared file (the test) is missing from the checker's sections (the diff does not touch it)
fixture "$B2" spark_secuura_2026-10-18_ks_1490_p1-armK5a || bad K5a-setup "fixture"
python3 -c 'import json,sys; p=sys.argv[1]; s=json.load(open(p)); json.dump(s[:1], open(p, "w"))' "$FX/out.md.checker/sections.json"
run k5a "$NEW" "$FX" "$B2G" TRAILINGSLASH-1 --title-from-brief "$B2B" --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/k5a.err" 'REFUSE — bash_patch2: touched set' && has "$S/k5a.err" 'declared but UNTOUCHED'; then ok K5a "bash_patch2 with the declared test missing from the sections -> REFUSED rc=2"; else bad K5a "rc=$RC; $(head -c 300 "$S/k5a.err")"; fi
# K5b: input declares a second product the diff never touches
fixture "$B2" spark_secuura_2026-10-18_ks_1490_p1-armK5b || bad K5b-setup "fixture"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); d["product_files"].append("Blockchain/Dev/connectors/whatsapp-bot/src/index.ts"); json.dump(d, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)' "$FX/input.json"
run k5b "$NEW" "$FX" "$B2G" TRAILINGSLASH-1 --title-from-brief "$B2B" --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/k5b.err" 'declared but UNTOUCHED' && has "$S/k5b.err" 'index.ts'; then ok K5b "bash_patch2 with an undelivered declared product -> REFUSED rc=2"; else bad K5b "rc=$RC; $(head -c 300 "$S/k5b.err")"; fi
# K5c: input task_type removed while the checker says bash_patch2
fixture "$B2" spark_secuura_2026-10-18_ks_1490_p1-armK5c || bad K5c-setup "fixture"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); del d["task_type"]; json.dump(d, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)' "$FX/input.json"
run k5c "$NEW" "$FX" "$B2G" TRAILINGSLASH-1 --title-from-brief "$B2B" --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/k5c.err" 'bash_patch2 signals disagree'; then ok K5c "checker bash_patch2, input task_type absent -> REFUSED rc=2"; else bad K5c "rc=$RC; $(head -c 300 "$S/k5c.err")"; fi
# K5d: no brief given -> REFUSED (the File:/Test lines cannot be counted against the declared set)
run k5d "$NEW" "$B2" "$B2G" TRAILINGSLASH-1 VERIFY --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/k5d.err" 'bash_patch2: needs --title-from-brief or --brief'; then ok K5d "bash_patch2 without a brief -> REFUSED rc=2"; else bad K5d "rc=$RC; $(head -c 300 "$S/k5d.err")"; fi
# K5e: the B5 run line for the RED test disagrees with its own green_after_1.out (a FAIL line appended)
fixture "$B2" spark_secuura_2026-10-18_ks_1490_p1-armK5e || bad K5e-setup "fixture"
printf 'FAIL: injected\n' >> "$FX/out.md.checker/green_after_1.out"
run k5e "$NEW" "$FX" "$B2G" TRAILINGSLASH-1 --title-from-brief "$B2B" --seat "$SEAT"
if [ $RC -eq 2 ] && has "$S/k5e.err" 'green_after_1.out re-count'; then ok K5e "green_after_1.out disagreeing with its B5 line -> REFUSED rc=2"; else bad K5e "rc=$RC; $(head -c 300 "$S/k5e.err")"; fi

# ---- K6: regression — OLD vs NEW over every run dir with a checker dir ('-' golden, no brief): rc + stdout (clock-normalised)
# + stderr identical, EXCEPT a dir OLD refused with "no 'mode: code_patch' line" whose input is one of the two new kinds.
if [ -f "$OLD" ]; then
  norm() { sed -e 's/from `ls` at [0-9:]* [0-9-]*/from ls at CLOCK/g' -e 's/^Held [0-9:]* [0-9-]* by/Held CLOCK by/' "$1"; }
  # a Python traceback names the script's own path and line numbers, which differ between OLD and NEW by construction
  enorm() { sed -E -e 's#^  File "[^"]*hold_ready[^"]*", line [0-9]+#  File "HOLD_READY", line N#' -e '/^ +[~^ ]+$/d' "$1"; }
  N=0; D=0; A=0; RR=0; : > "$S/k6_allowed.txt"; : > "$S/k6_bothrefused.txt"
  for d in "$R"/*; do
    [ -d "$d/out.md.checker" ] || continue
    N=$((N+1)); n=$(basename "$d")
    python3 "$OLD" --dry-run "$d" - TESTROW-1 TESTTITLE >"$S/k6o_$N.out" 2>"$S/k6o_$N.err"; ro=$?
    python3 "$NEW" --dry-run "$d" - TESTROW-1 TESTTITLE >"$S/k6n_$N.out" 2>"$S/k6n_$N.err"; rn=$?
    norm "$S/k6o_$N.out" > "$S/k6o_$N.o2"; norm "$S/k6n_$N.out" > "$S/k6n_$N.o2"
    enorm "$S/k6o_$N.err" > "$S/k6o_$N.e2"; enorm "$S/k6n_$N.err" > "$S/k6n_$N.e2"
    if [ $ro -eq $rn ] && cmp -s "$S/k6o_$N.o2" "$S/k6n_$N.o2" && cmp -s "$S/k6o_$N.e2" "$S/k6n_$N.e2"; then :
    elif grep -q -F "has no 'mode: code_patch' line" "$S/k6o_$N.err" && python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if (d.get("task_type")=="bash_patch2" or ((d.get("defect_line") or {}).get("tamper") or {}).get("line")) else 1)' "$d/input.json" 2>/dev/null; then
      A=$((A+1)); echo "$n new_rc=$rn $(head -c 140 "$S/k6n_$N.err" | tr '\n' ' ')" >> "$S/k6_allowed.txt"
    elif [ $ro -eq 2 ] && [ $rn -eq 2 ] && grep -q -F "has no 'mode: code_patch' line" "$S/k6o_$N.err" && grep -q -E 'REFUSE — (test_only|bash_patch2) signals disagree' "$S/k6n_$N.err"; then
      RR=$((RR+1)); echo "$n $(head -c 220 "$S/k6n_$N.err" | tr '\n' ' ')" >> "$S/k6_bothrefused.txt"
    else D=$((D+1)); echo "  K6 regression DIFF on $n: old rc=$ro new rc=$rn ($(head -c 160 "$S/k6n_$N.err"))"; fi
  done
  if [ $N -ge 50 ] && [ $D -eq 0 ]; then ok K6 "$N run dirs: OLD and NEW identical except $A new-kind dir(s) OLD refused for the missing 'mode: code_patch' line ($S/k6_allowed.txt) and $RR dir(s) refused by BOTH, now naming the disagreeing signals ($S/k6_bothrefused.txt)"; else bad K6 "$N compared, $D differ (outside the $A allowed new-kind dirs and $RR both-refused dirs)"; fi
else bad K6 "OLD copy $OLD does not exist"; fi

# ---- K7: the existing runnable arms files, unchanged, re-run: their ARM verdicts must equal the BASELINE taken before the
# change, and any NEW "regression DIFF" line in rung34's arm-5 loop must name a dir K6 classified as a new-kind dir.
S7="$S/k7"; mkdir -p "$S7"
S="$S7/rung34" /bin/bash "$L/tests/hold_ready_rung34_arms.sh" > "$S7/rung34.out" 2>&1; r34=$?
S="$S7/loose" /bin/bash "$L/tests/hold_ready_loose_recount_arms.sh" > "$S7/loose.out" 2>&1; rlo=$?
if [ -f "$BASE" ]; then
  grep -E '^ARM [0-9a-z]+: (PASS|FAIL)' "$BASE" | sed -E 's/^(ARM [0-9a-z]+: (PASS|FAIL)).*/\1/' > "$S7/base_verdicts"
  grep -E '^ARM [0-9a-z]+: (PASS|FAIL)' "$S7/rung34.out" | sed -E 's/^(ARM [0-9a-z]+: (PASS|FAIL)).*/\1/' > "$S7/now_verdicts"
  grep 'regression DIFF on' "$BASE" | sed -E 's/.*regression DIFF on ([^:]*):.*/\1/' | sort > "$S7/base_diffs"
  grep 'regression DIFF on' "$S7/rung34.out" | sed -E 's/.*regression DIFF on ([^:]*):.*/\1/' | sort > "$S7/now_diffs"
  comm -13 "$S7/base_diffs" "$S7/now_diffs" > "$S7/new_diffs"; comm -23 "$S7/base_diffs" "$S7/now_diffs" > "$S7/gone_diffs"
  cat "$S/k6_allowed.txt" "$S/k6_bothrefused.txt" 2>/dev/null | cut -d' ' -f1 > "$S7/k6_names"
  UNEXP=0; while IFS= read -r x; do [ -z "$x" ] && continue; grep -qxF "$x" "$S7/k6_names" || { UNEXP=$((UNEXP+1)); echo "  K7 unexpected new DIFF: $x"; }; done < "$S7/new_diffs"
  NNEW=$(grep -c . "$S7/new_diffs"); NGONE=$(grep -c . "$S7/gone_diffs")
  if cmp -s "$S7/base_verdicts" "$S7/now_verdicts" && [ "$UNEXP" -eq 0 ] && [ "$NGONE" -eq 0 ]; then ok K7a "rung34 arms: every ARM verdict equals the pre-change baseline ($(tr '\n' ' ' < "$S7/now_verdicts" | grep -o 'FAIL' | wc -l | tr -d ' ') FAIL in both); arm-5 loop: $NNEW new DIFF line(s), all new-kind dirs from K6"; else bad K7a "verdicts differ from baseline or $UNEXP unexpected / $NGONE vanished DIFF line(s) (see $S7)"; fi
else bad K7a "no baseline at $BASE"; fi
LV=$(grep -E '^ARM [0-9a-z]+: (PASS|FAIL)' "$S7/loose.out" | sed -E 's/^(ARM [0-9a-z]+: (PASS|FAIL)).*/\1/' | tr '\n' ' ')
if [ "$LV" = "ARM 1: PASS ARM 2: PASS ARM 3: PASS ARM 4a: PASS ARM 4b: PASS ARM 5: FAIL " ] || [ "$LV" = "ARM 1: PASS ARM 2: PASS ARM 3: PASS ARM 4a: PASS ARM 4b: PASS ARM 5: PASS " ]; then ok K7b "loose_recount arms: arms 1-4b PASS; arm 5 = rung34's rc (rung34 rc=$r34, loose rc=$rlo)"; else bad K7b "loose verdicts: $LV"; fi

echo "TOTAL FAILS=$FAILS"
[ $FAILS -eq 0 ]

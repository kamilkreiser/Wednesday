#!/bin/bash
# test_only_arms.sh — arms for tier test_only in spark/round.sh + spark/brief_lint.py (2026-10-18, NEXT-PICKUP owed item 1;
# IMPROVEMENTS 2026-10-16 13:10). Run as:  /bin/bash <abs path>/test_only_arms.sh   (SPARK_TEST_TMP=<scratch dir> optional)
#
# tier test_only = code_patch's TEST-ONLY mode: night/build_input.sh parses the brief's single `## Tamper` block into
# input.json defect_line.tamper, and tasks/code_patch/checker.sh then runs MODE=test_only (A3: the test file only;
# A4: red under the tamper; A5: green at the untouched tip). No new builder, no new checker.
#
# NO MODEL CALL and NO SPARK ENDPOINT: every round below is --control (golden in place of a model answer; round.sh skips
# step 2) or --dry-run with SPARK_URL at a closed local port (the endpoint leg is reported DOWN, never contacted).
#   T1  LINT ACCEPT     ks_1614_p1 (as on disk)                       -> brief_lint rc 0, B_TIER=test_only
#   T2  CONTROL PASS    round.sh ks_1614_p1 --control                 -> rc 0, CONTROL-PASS, golden BYTE-IDENTICAL,
#                       checker mode test_only, PASS A3 (test-only), tamper planted + reverted
#   T2b DRY-RUN         round.sh ks_1614_p1 --dry-run (closed port)   -> rc 0, DRY-RUN OK on code_patch/task.md, tamper :157
#   T3a TAMPERED GOLDEN golden's expected text changed (brief kept)   -> rc 1, CONTROL-FAIL
#   T3b WEAK CELL       brief+golden both drop the shownIn([1n]) line -> rc 1, CONTROL-FAIL at A4 (green under the tamper)
#   T4a REFUSE          golden.diff also carries a verification.ts hunk          -> rc 2, PRODUCT
#   T4b REFUSE          the exact-change fence names the product in a file header -> rc 2, PRODUCT
#   T4c REFUSE          the header declares two products                          -> rc 2, CONTRACT
#   T4d REFUSE          `## Tampers` (tasks/test_only's shape) instead of `## Tamper` -> rc 2, names tasks/test_only
#   T4e REFUSE          `## TAMPER` (lint matches; the builder's case-sensitive regex parses no tamper) -> rc 2 at the
#                       round's post-build backstop "parsed no tamper"
#   T5  LINT REGRESSION every brief dir on disk: old lint (.pre-1018-testonly) == new lint, output AND rc, byte for byte,
#                       except dirs whose OLD output carried a `REFUSED TIER:` line (its text named test_only "not wired";
#                       changed by design) — those are listed with the new result
#   T6  DRY REGRESSION  one brief per existing tier, dry-run by the OLD harness (the .pre-1018-testonly pair in a scratch
#                       copy of the layout) and by the NEW round.sh: same rc, same verdict line (timestamps normalised),
#                       input.json byte-identical
# rc 0 all arms PASS · 1 any FAIL. bash 3.2; no cd; nothing deleted; read verbs only on the Secuura checkout.
set -uo pipefail
SPARK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; LM="$(dirname "$SPARK")"
BR="$LM/night/briefs"; KS="$BR/ks_1614_p1"
T="${SPARK_TEST_TMP:-$(mktemp -d "${TMPDIR:-/tmp}/to_arms.XXXXXX")}"; mkdir -p "$T"
CLOSED="http://127.0.0.1:9"
# TO_ARMS_ALLOW_DRIFT=1: add allow_drift=1 to every round on the ks_1614_p1 brief and its copies — ONLY after measuring
# that develop's changes to the brief's files miss the edit points (2026-10-18 19:5x: #1560 moved verification.ts at
# :1068/:1187/:1579; :146-:163 and the test file unchanged). The arms print it when set.
KSP=""; [ "${TO_ARMS_ALLOW_DRIFT:-0}" = 1 ] && KSP="allow_drift=1"
P=0; F=0
ok()  { echo "ARM PASS $*"; P=$((P+1)); }
bad() { echo "ARM FAIL $*"; F=$((F+1)); }
echo "test_only_arms: fixtures in $T${KSP:+ · ks_1614_p1 rounds pinned $KSP (TO_ARMS_ALLOW_DRIFT=1)}"
# rround <out> <cmd...>: run a round; on rc 3 BUSY (another seat holds the ONE-request lock) wait 10 s and retry, up to 30 min
rround() {
  local out="$1"; shift; local i=0 rc
  while :; do
    "$@" > "$out" 2>&1; rc=$?
    if [ "$rc" -eq 3 ] && tail -1 "$out" | /usr/bin/grep -q "BUSY" && [ "$i" -lt 180 ]; then i=$((i+1)); sleep 10; continue; fi
    [ "$i" -gt 0 ] && echo "  (waited $((i*10))s for the round lock)"
    return "$rc"
  done
}
lastrun() { sed -n 's/^SPARK ROUND [^:]*: .* · \(\/[^ ]*\)$/\1/p' "$1" | tail -1; }

# ---------------------------------------------------------------- fixtures (copies of ks_1614_p1 in scratch)
python3 - "$KS" "$T" "$SPARK/cache/src" <<'PY'
import os, re, shutil, subprocess, sys
ks, t, src = sys.argv[1:4]
brief = open(os.path.join(ks, "KS-1614.md"), encoding="utf-8").read()
gold = open(os.path.join(ks, "golden.diff"), encoding="utf-8").read()
pins = open(os.path.join(ks, "spark.pins"), encoding="utf-8").read()
PROD = "Blockchain/Dev/services/api-gateway/src/routes/verification.ts"
SHOWN = "+    expect(shownIn([1n])).toBe('[object Array]');\n"
def mk(name, b=brief, g=gold, p=pins):
    d = os.path.join(t, name); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "KS-1614.md"), "w", encoding="utf-8").write(b)
    open(os.path.join(d, "golden.diff"), "w", encoding="utf-8").write(g)
    open(os.path.join(d, "spark.pins"), "w", encoding="utf-8").write(p)
assert SHOWN in gold and SHOWN in brief and "@@ -163,7 +163,14 @@" in gold
# T3a: the golden's expected text changed; the brief is untouched
mk("t3a_tampered_golden", g=gold.replace("toBe('[object Array]')", "toBe('1')"))
# T3b: a cell that cannot red under the tamper (only the toThrow expect is left), consistent in brief AND golden
mk("t3b_weak_cell", b=brief.replace(SHOWN, "").replace("@@ -163,7 +163,14 @@", "@@ -163,7 +163,13 @@"),
   g=gold.replace(SHOWN, "").replace("@@ -163,7 +163,14 @@", "@@ -163,7 +163,13 @@"))
# T4a: golden also edits the product (the tamper written as a product hunk)
tip = re.search(r"^Tip:\s*`([0-9a-f]{40})`", brief, re.M).group(1)
v = subprocess.run(["git", "-C", src, "show", f"{tip}:{PROD}"], capture_output=True, text=True, check=True).stdout.split("\n")
assert v[156] == "      shown = Object.prototype.toString.call(value);", v[156]
prod_hunk = (f"--- a/{PROD}\n+++ b/{PROD}\n@@ -156,3 +156,3 @@\n {v[155]}\n-{v[156]}\n+      shown = String(value);\n {v[157]}\n")
mk("t4a_golden_edits_product", g=gold + prod_hunk)
# T4b: the brief's exact-change fence carries a file header naming the product
mk("t4b_fence_names_product", b=brief.replace("```diff\n@@ -163,7", f"```diff\n--- a/{PROD}\n+++ b/{PROD}\n@@ -163,7", 1))
# T4c: two declared products
mk("t4c_two_products", b=brief.replace("\nTest file: `", f"\nFile: `Blockchain/Dev/services/api-gateway/src/index.ts`  (second product)\nTest file: `", 1))
# T4d: tasks/test_only's plural shape
assert "\n## Tamper (" in brief
mk("t4d_tampers_plural", b=brief.replace("\n## Tamper (", "\n## Tampers (", 1))
# T4e: an upper-case heading the builder does not read
mk("t4e_tamper_caps", b=brief.replace("\n## Tamper (", "\n## TAMPER (", 1))
print("fixtures written")
PY
[ $? -eq 0 ] || { echo "test_only_arms: fixture build failed"; exit 1; }

# ---------------------------------------------------------------- T1 lint accept
python3 "$SPARK/brief_lint.py" "$KS" > "$T/T1.out" 2>&1; rc=$?
if [ "$rc" -eq 0 ] && /usr/bin/grep -qx "B_TIER=test_only" "$T/T1.out"; then ok "T1 lint-accept ks_1614_p1: rc 0, B_TIER=test_only"
else bad "T1 lint-accept ks_1614_p1: rc=$rc $(head -2 "$T/T1.out" | tr '\n' ' ' | cut -c1-200)"; fi

# ---------------------------------------------------------------- T2 control PASS (the real brief dir, the real runs/)
rround "$T/T2.out" bash "$SPARK/round.sh" "$KS" --control $KSP; rc=$?
RUN2="$(lastrun "$T/T2.out")"; V2="$(tail -1 "$T/T2.out")"
if [ "$rc" -eq 0 ] && echo "$V2" | /usr/bin/grep -q "CONTROL-PASS" && echo "$V2" | /usr/bin/grep -q "golden BYTE-IDENTICAL" \
   && [ -n "$RUN2" ] && /usr/bin/grep -q "^mode: test_only (tamper at Blockchain/Dev/services/api-gateway/src/routes/verification.ts:157)" "$RUN2/checker.out" \
   && /usr/bin/grep -q "^PASS A3 (test-only)" "$RUN2/checker.out" && /usr/bin/grep -q "^A4 (test-only): tampered" "$RUN2/checker.out" \
   && /usr/bin/grep -q "^A4 (test-only): tamper reverted" "$RUN2/checker.out"; then
  ok "T2 control ks_1614_p1: $V2"
else bad "T2 control ks_1614_p1: rc=$rc $V2"; fi

# ---------------------------------------------------------------- T2b dry-run (closed port: the endpoint is never contacted)
rround "$T/T2b.out" env SPARK_URL="$CLOSED" bash "$SPARK/round.sh" "$KS" --dry-run $KSP; rc=$?
D2="$(sed -n 's/.* in \(\/[^;]*\/state\/dry\/[^;]*\);.*/\1/p' "$T/T2b.out" | tail -1)"
TL="$( [ -n "$D2" ] && python3 -c 'import json,sys; print((json.load(open(sys.argv[1])).get("defect_line") or {}).get("tamper",{}).get("line",""))' "$D2/input.json" 2>&1)"
if [ "$rc" -eq 0 ] && tail -1 "$T/T2b.out" | /usr/bin/grep -q "DRY-RUN OK.*code_patch/task.md" && [ "$TL" = "157" ]; then
  ok "T2b dry-run ks_1614_p1: DRY-RUN OK, task code_patch/task.md, input tamper line $TL"
else bad "T2b dry-run ks_1614_p1: rc=$rc tamper='$TL' $(tail -1 "$T/T2b.out" | cut -c1-220)"; fi

# ---------------------------------------------------------------- T3 tampered goldens must FAIL (control, scratch runs)
for arm in t3a_tampered_golden t3b_weak_cell; do
  rround "$T/$arm.out" env SPARK_RUNS="$T/runs" SPARK_WORK_ROOT="$T/work" bash "$SPARK/round.sh" "$T/$arm" --control $KSP; rc=$?
  R="$(lastrun "$T/$arm.out")"; V="$(tail -1 "$T/$arm.out")"
  FIRSTFAIL="$( [ -n "$R" ] && /usr/bin/grep -m1 '^FAIL ' "$R/checker.out" | cut -c1-160)"
  want=""; [ "$arm" = t3b_weak_cell ] && want="^FAIL A4"
  if [ "$rc" -eq 1 ] && echo "$V" | /usr/bin/grep -q "CONTROL-FAIL" && { [ -z "$want" ] || /usr/bin/grep -q "$want" "$R/checker.out"; }; then
    ok "T3 $arm: rc 1 CONTROL-FAIL; first failing leg: $FIRSTFAIL"
  else bad "T3 $arm: rc=$rc (want 1 CONTROL-FAIL${want:+ with $want}) $V | $FIRSTFAIL"; fi
done

# ---------------------------------------------------------------- T4 product-touching / mis-shaped test_only briefs REFUSED
t4() { # t4 <arm> <grep for the reason>
  local rc; rround "$T/$1.out" env SPARK_URL="$CLOSED" SPARK_RUNS="$T/runs" SPARK_WORK_ROOT="$T/work" bash "$SPARK/round.sh" "$T/$1" --dry-run $KSP; rc=$?
  if [ "$rc" -eq 2 ] && /usr/bin/grep -q -- "$2" "$T/$1.out"; then ok "T4 $1: rc 2 — $(/usr/bin/grep -m1 -- "$2" "$T/$1.out" | cut -c1-200)"
  else bad "T4 $1: rc=$rc (want 2 + /$2/) $(tail -1 "$T/$1.out" | cut -c1-220)"; fi
}
t4 t4a_golden_edits_product "PRODUCT: .*golden.diff .*verification.ts"
t4 t4b_fence_names_product "PRODUCT: .*exact change.*verification.ts"
t4 t4c_two_products "CONTRACT: the header declares 2 product"
t4 t4d_tampers_plural "tasks/test_only/build_test_only_input.sh"
t4 t4e_tamper_caps "REFUSED — tier test_only but the builder parsed no tamper"

# ---------------------------------------------------------------- T5 lint regression over every brief dir on disk
OLDLINT="$SPARK/brief_lint.py.pre-1018-testonly"
[ -f "$OLDLINT" ] || { bad "T5 no $OLDLINT"; }
N=0; SAME=0; SAMEX=0; DIFF=0; BYDESIGN=0; : > "$T/T5_bydesign.txt"; : > "$T/T5_diff.txt"
for d in "$BR"/*/ "$SPARK"/briefs_*/*/; do
  [ -d "$d" ] || continue
  o="$(python3 "$OLDLINT" "$d" 2>&1; echo "rc=$?")"; n="$(python3 "$SPARK/brief_lint.py" "$d" 2>&1; echo "rc=$?")"
  N=$((N+1))
  if [ "$o" = "$n" ]; then SAME=$((SAME+1)); continue; fi
  # the `REFUSED TIER:` line's TEXT changed by design (it said test_only is not wired): equal once that line is dropped
  # from both sides (and both still carry one) = identical apart from that sentence
  o2="$(echo "$o" | /usr/bin/grep -v '^REFUSED TIER: ')"; n2="$(echo "$n" | /usr/bin/grep -v '^REFUSED TIER: ')"
  if [ "$o2" = "$n2" ] && echo "$o" | /usr/bin/grep -q '^REFUSED TIER: ' && echo "$n" | /usr/bin/grep -q '^REFUSED TIER: '; then SAMEX=$((SAMEX+1)); continue; fi
  # otherwise it may differ ONLY where the old lint refused the tier as test_only (the briefs this wiring is for)
  if echo "$o" | /usr/bin/grep -q '^REFUSED TIER: test_only'; then
    BYDESIGN=$((BYDESIGN+1)); echo "$(basename "$d"): old 'TIER: test_only' refusal -> new $(echo "$n" | tail -1) $(echo "$n" | /usr/bin/grep -m1 -e '^REFUSED' -e '^B_TIER=' | cut -c1-170)" >> "$T/T5_bydesign.txt"
  else DIFF=$((DIFF+1)); echo "$(basename "$d")" >> "$T/T5_diff.txt"; fi
done
if [ "$DIFF" -eq 0 ] && [ "$SAME" -gt 0 ]; then ok "T5 lint regression over $N brief dirs: $SAME byte-identical (output+rc); $SAMEX identical but for the TIER sentence; $BYDESIGN were old 'TIER: test_only' refusals (now judged as test_only):"
else bad "T5 lint regression: $DIFF dir(s) differ outside the test_only change: $(tr '\n' ' ' < "$T/T5_diff.txt")"; fi
sed 's/^/     /' "$T/T5_bydesign.txt"

# ---------------------------------------------------------------- T6 dry-run regression, one brief per existing tier
OLDH="$T/oldharness"; mkdir -p "$OLDH/spark"
cp -p "$SPARK/round.sh.pre-1018-testonly" "$OLDH/spark/round.sh"; cp -p "$SPARK/brief_lint.py.pre-1018-testonly" "$OLDH/spark/brief_lint.py"
cp -p "$SPARK/tunnel.sh" "$OLDH/spark/tunnel.sh"
for x in tasks night lib local_model_task.sh; do [ -e "$OLDH/$x" ] || ln -s "$LM/$x" "$OLDH/$x"; done
# develop can move BETWEEN the old and the new dry-run (other seats merge): shas are normalised in the verdict, and
# input.json is compared byte for byte, else with each side's OWN tip replaced by TIP (reported as such, with both tips)
norm() { sed -E 's/_[0-9]{8}-[0-9]{6}/_TS/g; s#'"$OLDH"'/spark#SPARK#g; s#'"$SPARK"'#SPARK#g; s/[0-9a-f]{12}/SHA/g' "$1"; }
same_mod_tip() { python3 - "$1" "$2" <<'PYX'
import json, sys
def load(p):
    s = open(p, encoding="utf-8").read(); d = json.loads(s); tip = d.get("tip") or d.get("repo", {}).get("tip", "")
    return s.replace(tip, "TIP") if tip else s, tip
a, ta = load(sys.argv[1]); b, tb = load(sys.argv[2])
print(f"input.json identical modulo tip (develop moved {ta[:12]} -> {tb[:12]} between the two runs)" if a == b else f"input.json DIFFERS beyond the tip ({ta[:12]} vs {tb[:12]})")
PYX
}
# chosen 2026-10-18 at develop d0c5d2e0 as the briefs of each tier that still reach DRY-RUN OK (most others are stale or
# their ticket is In Progress/Done); the extra pins go to BOTH harnesses alike. Format tier|brief dir|pins.
for spec in "code_patch|$BR/ks_1541_p1|" "code_patch2|$BR/KS-593-share-null-recipient-cp2|allow_drift=1 started_ok=dry-run-regression-arm-only" \
            "bash_patch|$BR/KS-948-mixed-backtick|allow_drift=1" "bash_patch2|$SPARK/briefs_2026-10-08_harder/KS-1438-html-docs-check-resolved-paths-r2|"; do
  tier="${spec%%|*}"; rest="${spec#*|}"; bd="${rest%%|*}"; xp="${rest#*|}"; tag="$(basename "$bd")"
  rround "$T/T6_old_$tag.out" env SPARK_URL="$CLOSED" SPARK_CACHE="$SPARK/cache" SPARK_STATE="$SPARK/state" SPARK_RUNS="$T/runs_old" bash "$OLDH/spark/round.sh" "$bd" --dry-run $xp; orc=$?
  rround "$T/T6_new_$tag.out" env SPARK_URL="$CLOSED" SPARK_RUNS="$T/runs_new" bash "$SPARK/round.sh" "$bd" --dry-run $xp; nrc=$?
  ov="$(tail -1 "$T/T6_old_$tag.out" > "$T/T6_old_$tag.v"; norm "$T/T6_old_$tag.v")"; nv="$(tail -1 "$T/T6_new_$tag.out" > "$T/T6_new_$tag.v"; norm "$T/T6_new_$tag.v")"
  od="$(sed -n 's/.* in \(\/[^;]*\/state\/dry\/[^;]*\);.*/\1/p' "$T/T6_old_$tag.out" | tail -1)"; nd="$(sed -n 's/.* in \(\/[^;]*\/state\/dry\/[^;]*\);.*/\1/p' "$T/T6_new_$tag.out" | tail -1)"
  inp="no input.json (neither built one)"
  if [ -n "$od" ] && [ -n "$nd" ]; then
    if cmp -s "$od/input.json" "$nd/input.json"; then inp="input.json byte-identical"; else inp="$(same_mod_tip "$od/input.json" "$nd/input.json")"; fi
  elif [ -n "$od$nd" ]; then inp="only one side built input.json (old '$od' new '$nd')"; fi
  if [ "$orc" -eq "$nrc" ] && [ "$ov" = "$nv" ] && { [ "$inp" = "input.json byte-identical" ] || [ "$inp" = "no input.json (neither built one)" ] || case "$inp" in "input.json identical modulo tip"*) true ;; *) false ;; esac; }; then
    ok "T6 $tier ($tag): old rc $orc == new rc $nrc, verdict identical, $inp — $(echo "$nv" | cut -c1-150)"
  else bad "T6 $tier ($tag): old rc $orc / new rc $nrc; $inp; old: $(echo "$ov" | cut -c1-140) | new: $(echo "$nv" | cut -c1-140)"; fi
done

echo "test_only_arms: $P PASS, $F FAIL (fixtures + outputs in $T)"
[ "$F" -eq 0 ]

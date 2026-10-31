#!/bin/bash
# new_tiers_arms.sh — arms for tiers test_only_input and doc_only (2026-10-31). Run as:
#   /bin/bash <abs path>/new_tiers_arms.sh        (NEW_TIERS_ROOT=<fresh path under /private/tmp/claude-501/> optional)
#
# NO MODEL CALL, NO SPARK ENDPOINT, NO SECUURA CLONE. A tiny fixture repo (tests/new_tiers_fixture.py) stands in for the
# Secuura checkout (SPARK_SECUURA_CHECKOUT, SPARK_TIP, SPARK_CACHE, SPARK_STATE, SPARK_RUNS, SPARK_WORK_ROOT all point into the
# fixture root; SPARK_URL is a closed port and --control never contacts it). Rounds are `round.sh --control` (the brief's golden
# in place of a model answer) — the whole path: lint, lock, base, input builder, clone, tier_checker.py, golden compare. Crafted
# outputs that lint would refuse as a golden (an extra touched file, the product) are fed to tier_checker.py directly on the
# clone a control PASS left behind, because the leg under test is the checker's, not lint's.
#   L*   lint refusals (rc 2) — a brief lacking a required field
#   TI*  test_only_input    PASS x2 (pinned plant; golden_red.diff plant of a test-side input) · FAIL: cell green with the plant,
#                           cell crashes instead of asserting, plant not applicable, red cell absent, extra test file touched,
#                           product touched, declared test missing, existing cell lost, bad hunk anchor, prose-only, prose+diff
#   D*   doc_only           PASS · FAIL: changed code line, blank line in code, trailing comment on a code line, expectation that
#                           already holds at base, partial fix leaving the absent text, fragment check fails, extra touched file,
#                           declared file missing
# rc 0 all arms behaved as stated · 1 any arm did not. bash 3.2; no cd; nothing deleted.
set -uo pipefail
SPARK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="${NEW_TIERS_ROOT:-/private/tmp/claude-501/spark_newtiers_arms_$(date +%Y%m%d_%H%M%S)_$$}"
case "$ROOT" in /private/tmp/claude-501/*) ;; *) echo "new_tiers_arms: ROOT must be under /private/tmp/claude-501/ ($ROOT)"; exit 1 ;; esac
if [ -e "$ROOT" ]; then echo "new_tiers_arms: $ROOT already exists — refusing (a fresh path is the fixture's contract)"; exit 1; fi
python3 "$SPARK/tests/new_tiers_fixture.py" "$ROOT" || { echo "new_tiers_arms: fixture build failed"; exit 1; }
TIP="$(cat "$ROOT/tip.txt")"
B="$ROOT/briefs"; O="$ROOT/outs"
P=0; F=0
ok()  { echo "ARM PASS $*"; P=$((P+1)); }
bad() { echo "ARM FAIL $*"; F=$((F+1)); }
export SPARK_SECUURA_CHECKOUT="$ROOT/secuura" SPARK_CACHE="$ROOT/cache" SPARK_STATE="$ROOT/state" SPARK_RUNS="$ROOT/runs" \
       SPARK_WORK_ROOT="$ROOT/work" SPARK_TIP="$TIP" SPARK_URL="http://127.0.0.1:9"
echo "new_tiers_arms: fixture root $ROOT (tip ${TIP:0:12})"

# ---------------------------------------------------------------- L lint refusals
lint() { # lint <dir> <grep>
  local out rc; out="$(python3 "$SPARK/brief_lint.py" "$B/$1" 2>&1)"; rc=$?
  if [ "$rc" -eq 2 ] && echo "$out" | /usr/bin/grep -q -- "$2"; then ok "L $1: rc 2 — $(echo "$out" | /usr/bin/grep -m1 -- "$2" | cut -c1-170)"
  else bad "L $1: rc=$rc (want 2 + /$2/) $(echo "$out" | head -2 | tr '\n' ' ' | cut -c1-200)"; fi
}
lint l_no_plant "PLANT"
lint l_both_plants "PLANT"
lint l_no_redcells "RED CELLS"
lint l_four_tests "CONTRACT"
lint l_golden_names_product "PRODUCT"
lint l_plant_in_declared_test "PLANT"
lint l_plant_incomplete "PLANT"
lint l_d_no_expect "EXPECT"
lint l_d_only_present "EXPECT"
lint l_d_test_file "CONTRACT"
lint l_d_json_file "PATH"
lint l_d_golden_undeclared "DOC-ONLY"
lint l_d_bad_check_cmd "DOC CHECK"
lint l_d_in_path_undeclared "EXPECT"
for d in ti_pass_pin ti_pass_diffplant d_pass; do
  out="$(python3 "$SPARK/brief_lint.py" "$B/$d" 2>&1)"; rc=$?
  t="test_only_input"; [ "$d" = d_pass ] && t="doc_only"
  if [ "$rc" -eq 0 ] && echo "$out" | /usr/bin/grep -qx "B_TIER=$t"; then ok "L $d: accepted, B_TIER=$t"; else bad "L $d: rc=$rc $(echo "$out" | head -2 | tr '\n' ' ' | cut -c1-200)"; fi
done

# ---------------------------------------------------------------- control rounds
lastrun() { sed -n 's/^SPARK ROUND [^:]*: .* · \(\/[^ ]*\)$/\1/p' "$1" | tail -1; }
ctl() { # ctl <name> <want rc> <want grep in checker.out or ''> [round.sh args...] ; sets RUN
  local n="$1" want="$2" g="$3"; shift 3
  bash "$SPARK/round.sh" "$B/$n" --control "$@" > "$ROOT/$n.out" 2>&1; local rc=$?
  RUN="$(lastrun "$ROOT/$n.out")"
  local v; v="$(tail -1 "$ROOT/$n.out")"
  local hit=1; [ -z "$g" ] && hit=0
  [ -n "$g" ] && [ -n "$RUN" ] && /usr/bin/grep -q -- "$g" "$RUN/checker.out" && hit=0
  local first=""; [ -n "$RUN" ] && first="$(/usr/bin/grep -m1 '^FAIL ' "$RUN/checker.out" | cut -c1-210)"
  if [ "$rc" -eq "$want" ] && [ "$hit" -eq 0 ]; then ok "$n: rc $rc ($(echo "$v" | cut -c1-60)…)${first:+ — $first}"
  else bad "$n: rc=$rc want $want, grep '$g' hit=$([ $hit -eq 0 ] && echo yes || echo no) :: $(echo "$v" | cut -c1-200) | $first"; fi
}
ctl ti_pass_pin 0 "^PASS A5 RED WITH PLANT"
TI_RUN="$RUN"
ctl ti_pass_diffplant 0 "^PASS A5 RED WITH PLANT"
ctl ti_green_with_plant 1 "^FAIL A5 RED WITH PLANT.*stays GREEN"
ctl ti_crash_not_assertion 1 "^FAIL A5 RED WITH PLANT.*crash, not an assertion"
ctl ti_plant_not_applicable 1 "^FAIL A3p"
ctl ti_redcell_missing 1 "^FAIL A4 GREEN WITHOUT PLANT.*no cell contains"
ctl d_pass 0 "^PASS A7 REVERSION"
D_RUN="$RUN"
ctl d_changed_code_line 1 "^FAIL A3d DOC-ONLY"
ctl d_blank_line_in_code 1 "^FAIL A3d DOC-ONLY"
ctl d_trailing_comment 1 "^FAIL A3d DOC-ONLY"
ctl d_expect_already_holds 1 "^FAIL A4 RED AT BASE"
ctl d_partial_fix 1 "^FAIL A5 GREEN AFTER"
ctl d_fragment_check_fails 1 "^FAIL A6 DOC CHECK"

# the PASS arms also: the golden compare must say BYTE-IDENTICAL, and the PASS must have run every leg
for pair in "ti_pass_pin:$TI_RUN" "d_pass:$D_RUN"; do
  n="${pair%%:*}"; r="${pair#*:}"
  legs="$(/usr/bin/grep -c '^PASS ' "$r/checker.out")"; fails="$(/usr/bin/grep -c '^FAIL ' "$r/checker.out")"
  if [ "$fails" = 0 ] && [ "$legs" -ge 6 ] && /usr/bin/grep -q "golden BYTE-IDENTICAL" "$ROOT/$n.out"; then ok "$n: $legs PASS legs, 0 FAIL, golden BYTE-IDENTICAL, source checkout untouched: $(git -C "$ROOT/secuura" status --porcelain --untracked-files=no | wc -l | tr -d ' ') tracked change(s)"
  else bad "$n: legs=$legs fails=$fails $(tail -1 "$ROOT/$n.out" | cut -c1-160)"; fi
done

# ---------------------------------------------------------------- direct checker arms on the clone a control PASS left behind
direct() { # direct <label> <run dir> <out name> <grep> [want rc, default 1]
  local label="$1" run="$2" outn="$3" g="$4" want="${5:-1}"
  local work clone; work="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]+"/round.json"))["work_dir"])' "$run")"; clone="$work/clone"
  cp "$O/$outn.md" "$ROOT/direct_$label.md"
  python3 "$SPARK/tiers/tier_checker.py" "$run/input.json" "$ROOT/direct_$label.md" "$clone" > "$ROOT/direct_$label.out" 2>&1; local rc=$?
  local st; st="$(git -C "$clone" status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
  if [ "$rc" -eq "$want" ] && /usr/bin/grep -q -- "$g" "$ROOT/direct_$label.out" && [ "$st" = 0 ]; then
    ok "$label: checker rc $rc, $(/usr/bin/grep -m1 -- "$g" "$ROOT/direct_$label.out" | cut -c1-200); clone clean after ($st tracked changes)"
  else bad "$label: rc=$rc want $want, grep '$g', clone tracked changes=$st :: $(tail -3 "$ROOT/direct_$label.out" | tr '\n' ' ' | cut -c1-260)"; fi
}
direct TI-extra-test-file "$TI_RUN" ti_extra_test "^FAIL A3 touched set != the declared set: extra \['Blockchain/Dev/services/svc/tests/other.test.js'\]"
direct TI-touches-product "$TI_RUN" ti_touches_product "^FAIL A3 touched set != the declared set: extra \['Blockchain/Dev/services/svc/src/verify.js'\]"
direct TI-missing-declared-test "$TI_RUN" ti_missing_declared "^FAIL A3 .*missing \['Blockchain/Dev/services/svc/tests/verify_b.test.js'\]"
direct TI-existing-cell-lost "$TI_RUN" ti_lost_cell "^FAIL A6 WHOLE SUITE.*LOST"
direct TI-bad-hunk-anchor "$TI_RUN" ti_bad_anchor "^FAIL A2a ANCHOR"
direct TI-prose-only "$TI_RUN" ti_prose_only "^FAIL A1 no \`\`\`diff block"
direct TI-prose-plus-diff "$TI_RUN" ti_prose_and_diff "^FAIL A1 output is not exactly one fenced"
direct D-extra-touched-file "$D_RUN" d_extra_file "^FAIL A3 touched set != the declared set: extra \['README.md'\]"
direct D-missing-declared-file "$D_RUN" d_missing_declared "^FAIL A3 .*missing \['Blockchain/Dev/services/svc/src/verify.js'\]"
# and the checker re-run on the GOOD output after all that abuse must still PASS (restore left the clone exactly at the tip)
cp "$B/ti_pass_pin/golden.diff" "$ROOT/good_ti.diff"; { printf '```diff\n'; cat "$B/ti_pass_pin/golden.diff"; printf '```\n'; } > "$O/ti_good.md"
direct TI-rerun-good-after-abuse "$TI_RUN" ti_good "^RESULT: PASS" 0

# ---------------------------------------------------------------- unit arms: the vitest/jest report parser and the comment classifier
# (the real runners are not run here — no Secuura clone; the report SHAPE they write is what tier_checker.py reads)
python3 - "$SPARK/tiers" "$ROOT" > "$ROOT/units.out" 2>&1 <<'PY'
import json, os, sys
sys.path.insert(0, sys.argv[1]); root = sys.argv[2]
import tier_checker as tc, tier_brief as tb
rep = {"numTotalTests": 3, "testResults": [
  {"name": "/x/a.test.ts", "status": "failed", "assertionResults": [
    {"fullName": "d works", "title": "works", "status": "passed", "failureMessages": []},
    {"fullName": "d forged", "title": "forged", "status": "failed", "failureMessages": ["AssertionError: expected true to be false"]},
    {"fullName": "d crash", "title": "crash", "status": "failed", "failureMessages": ["TypeError: Cannot read properties of null"]}]},
  {"name": "/x/b.test.ts", "status": "failed", "assertionResults": [], "message": "Cannot find module"}]}
f = os.path.join(root, "vitest_sample.json"); json.dump(rep, open(f, "w"))
cells, lerr = tc.parse_json_report(f)
res = []
res.append(("U1 json report: 3 cells, 1 passed, 2 failed, 1 load error", sorted(v[0] for v in cells.values()) == ["failed", "failed", "passed"] and len(lerr) == 1 and "b.test.ts" in lerr[0]))
res.append(("U2 by_assertion: AssertionError yes, TypeError no", tc.by_assertion(cells["d forged"][1]) and not tc.by_assertion(cells["d crash"][1])))
src = "/**\n * doc\n */\nconst a = '// not a comment'; // trailing\n// whole\nconst t = `x\n// inside template\n`;\n\nfoo(); /* c */\n/* a */ bar();\n"
cl = tb.comment_lines(src, "c")
want = [True, True, True, False, True, False, False, False, False, False, False, False]
res.append(("U3 comment_lines(c): block lines, string with //, trailing comment, template literal, blank, mixed", cl == want[:len(cl)] and len(cl) == 12))
res.append(("U4 comment_lines(hash): '# x' yes, shebang no, code no", tb.comment_lines("#!/bin/sh\n# x\necho hi # t\n", "hash") == [False, True, False, False]))
res.append(("U5 is_doc_path / comment_kind", tb.is_doc_path("a/b.md") and tb.is_doc_path("Blockchain/Projects Documents/fragments/x.txt") and not tb.is_doc_path("a/b.ts") and tb.comment_kind("a/b.ts") == "c" and tb.comment_kind("a/b.json") is None))
bad = 0
for name, ok in res:
    print(("ARM PASS " if ok else "ARM FAIL ") + name); bad += (not ok)
sys.exit(bad)
PY
URC=$?
/usr/bin/grep '^ARM ' "$ROOT/units.out" | cut -c1-200
UP="$(/usr/bin/grep -c '^ARM PASS' "$ROOT/units.out")"; UF="$(/usr/bin/grep -c '^ARM FAIL' "$ROOT/units.out")"
P=$((P+UP)); F=$((F+UF)); [ "$URC" -ne 0 ] && [ "$UF" -eq 0 ] && { echo "ARM FAIL units crashed: $(tail -2 "$ROOT/units.out")"; F=$((F+1)); }

echo "new_tiers_arms: $P PASS, $F FAIL (fixture + outputs in $ROOT)"
[ "$F" -eq 0 ]

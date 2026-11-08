#!/bin/bash
# test_only_bash_spark_arms.sh — arms for the SPARK tier test_only_bash (2026-11-09; tiers/tier_checker.py tier_test_only_bash,
# build_tier_input.py, brief_lint.py lint_test_only_bash, round.sh wiring). Run as:
#   /bin/bash <abs path>/test_only_bash_spark_arms.sh        (TOBX_ROOT=<fresh path under /private/tmp/claude-501/> optional)
# NOT the night harness's tests/test_only_bash_arms.sh (that one is the older test_only tier's bash runner and is left as it was).
#
# NO MODEL CALL, NO SPARK ENDPOINT, NO SECUURA CLONE. test_only_bash_spark_fixture.py builds a tiny fixture repo standing in for
# the Secuura checkout (SPARK_SECUURA_CHECKOUT, SPARK_TIP, SPARK_CACHE, SPARK_STATE, SPARK_RUNS, SPARK_WORK_ROOT, SPARK_DEPS_CHECKOUT
# all point into the fixture root; SPARK_URL is a closed port and --control never contacts it). Rounds are `round.sh --control`
# (the brief's golden in place of a model answer): lint, lock, base, builder, clone, tier_checker.py, golden compare. Crafted outputs
# lint would refuse as a golden are fed to tier_checker.py directly on the clone a control PASS left behind.
#   L*   lint refusals (rc 2)
#   P*   PASS: plant shape (a correct suite edit) and expect shape
#   R*   REFUSED (rc 1): suite edit touches a product file · touches another suite · red cell never fires (stays green under the plant)
#        · suite crashes (command not found) · plant not applicable · named cell absent · suite prints FAIL but exits 0 · wrong
#        expected line (diff does not apply) · bad hunk anchor · existing cell lost · prose only / prose+diff · expect shape: the
#        cell without the fix (new red) · an expectation that holds at the tip (reversion does not discriminate)
#   K*   KNOWN LIMIT, asserted so it is on record: an expect-shape cell that asserts nothing PASSES (README "does not prove")
# rc 0 all arms behaved as stated · 1 any arm did not. bash 3.2; no cd; nothing deleted.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SPARK="$(cd "$HERE/../spark" && pwd)"
ROOT="${TOBX_ROOT:-/private/tmp/claude-501/tobx_arms_$(date +%Y%m%d_%H%M%S)_$$}"
case "$ROOT" in /private/tmp/claude-501/*) ;; *) echo "test_only_bash_spark_arms: ROOT must be under /private/tmp/claude-501/ ($ROOT)"; exit 1 ;; esac
[ -e "$ROOT" ] && { echo "test_only_bash_spark_arms: $ROOT already exists — a fresh path is the fixture's contract"; exit 1; }
python3 -I "$HERE/test_only_bash_spark_fixture.py" "$ROOT" || { echo "test_only_bash_spark_arms: fixture build failed"; exit 1; }
TIP="$(cat "$ROOT/tip.txt")"
B="$ROOT/briefs"; O="$ROOT/outs"
P=0; F=0
ok()  { echo "ARM PASS $*"; P=$((P+1)); }
bad() { echo "ARM FAIL $*"; F=$((F+1)); }
export SPARK_SECUURA_CHECKOUT="$ROOT/secuura" SPARK_CACHE="$ROOT/cache" SPARK_STATE="$ROOT/state" SPARK_RUNS="$ROOT/runs" \
       SPARK_WORK_ROOT="$ROOT/work" SPARK_DEPS_CHECKOUT="$ROOT/deps" SPARK_TIP="$TIP" SPARK_URL="http://127.0.0.1:9"
echo "test_only_bash_spark_arms: fixture root $ROOT (tip ${TIP:0:12})"

# ---------------------------------------------------------------- L lint refusals
lint() { # lint <dir> <grep>
  local out rc; out="$(python3 "$SPARK/brief_lint.py" "$B/$1" 2>&1)"; rc=$?
  if [ "$rc" -eq 2 ] && echo "$out" | /usr/bin/grep -q -- "$2"; then ok "L $1: rc 2 — $(echo "$out" | /usr/bin/grep -m1 -- "$2" | cut -c1-170)"
  else bad "L $1: rc=$rc (want 2 + /$2/) $(echo "$out" | head -2 | tr '\n' ' ' | cut -c1-200)"; fi
}
lint l_both_proofs "PROOF"
lint l_no_proof "PROOF"
lint l_no_redcells "RED CELLS"
lint l_not_bash_suite "TEST PATH"
lint l_file_is_test "CONTRACT"
lint l_runner_vitest "RUNNER"
lint l_golden_names_product "PRODUCT"
lint l_plant_in_suite "PLANT"
lint l_four_tests "CONTRACT"
lint l_expect_empty "EXPECT"
lint l_expect_in_undeclared "EXPECT"
for d in bx_pass_plant bx_pass_expect; do
  out="$(python3 "$SPARK/brief_lint.py" "$B/$d" 2>&1)"; rc=$?
  if [ "$rc" -eq 0 ] && echo "$out" | /usr/bin/grep -qx "B_TIER=test_only_bash"; then ok "L $d: accepted, B_TIER=test_only_bash"; else bad "L $d: rc=$rc $(echo "$out" | head -2 | tr '\n' ' ' | cut -c1-200)"; fi
done

# ---------------------------------------------------------------- control rounds
lastrun() { sed -n 's/^SPARK ROUND [^:]*: .* · \(\/[^ ]*\)$/\1/p' "$1" | tail -1; }
ctl() { # ctl <name> <want rc> <grep in checker.out> [<second grep>]; sets RUN
  local n="$1" want="$2" g="$3" g2="${4:-}"
  bash "$SPARK/round.sh" "$B/$n" --control > "$ROOT/$n.out" 2>&1; local rc=$?
  RUN="$(lastrun "$ROOT/$n.out")"
  local v; v="$(tail -1 "$ROOT/$n.out")"
  local hit=1; [ -n "$RUN" ] && /usr/bin/grep -q -- "$g" "$RUN/checker.out" && hit=0
  [ -n "$g2" ] && { [ -n "$RUN" ] && /usr/bin/grep -q -- "$g2" "$RUN/checker.out" || hit=1; }
  local first=""; [ -n "$RUN" ] && first="$(/usr/bin/grep -m1 '^FAIL ' "$RUN/checker.out" | cut -c1-230)"
  if [ "$rc" -eq "$want" ] && [ "$hit" -eq 0 ]; then ok "$n: rc $rc ($(echo "$v" | cut -c1-60)…)${first:+ — $first}"
  else bad "$n: rc=$rc want $want, grep '$g' hit=$([ $hit -eq 0 ] && echo yes || echo no) :: $(echo "$v" | cut -c1-220) | $first"; fi
}
ctl bx_pass_plant 0 "^PASS A5 RED WITH PLANT"
PL_RUN="$RUN"
ctl bx_pass_expect 0 "^PASS A7 REVERSION"
EX_RUN="$RUN"
ctl bx_neverred 1 "^FAIL A5 RED WITH PLANT.*stays GREEN"
ctl bx_crash 1 "^FAIL A4 GREEN WITHOUT PLANT.*load-error"
ctl bx_plant_not_applicable 1 "^FAIL A3p"
ctl bx_redcell_missing 1 "^FAIL A4 GREEN WITHOUT PLANT.*no cell label contains"
ctl bx_nogate 1 "^FAIL A5 RED WITH PLANT.*exited rc 0"
ctl bx_cell_only 1 "^FAIL A4 GREEN WITHOUT PLANT.*without the plant" "^FAIL A4e"
ctl bx_expect_holds_at_tip 1 "^FAIL A4b RED AT BASE" "^FAIL A7 REVERSION.*still hold"

# the PASS arms: every leg ran, golden BYTE-IDENTICAL, the source checkout untouched
for pair in "bx_pass_plant:$PL_RUN" "bx_pass_expect:$EX_RUN"; do
  n="${pair%%:*}"; r="${pair#*:}"
  legs="$(/usr/bin/grep -c '^PASS ' "$r/checker.out")"; fails="$(/usr/bin/grep -c '^FAIL ' "$r/checker.out")"
  if [ "$fails" = 0 ] && [ "$legs" -ge 7 ] && /usr/bin/grep -q "golden BYTE-IDENTICAL" "$ROOT/$n.out"; then
    ok "$n: $legs PASS legs, 0 FAIL, golden BYTE-IDENTICAL, source checkout tracked changes: $(git -C "$ROOT/secuura" status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
  else bad "$n: legs=$legs fails=$fails $(tail -1 "$ROOT/$n.out" | cut -c1-160)"; fi
done

# ---------------------------------------------------------------- direct checker arms
direct() { # direct <label> <run dir> <out name> <grep> [want rc, default 1]
  local label="$1" run="$2" outn="$3" g="$4" want="${5:-1}"
  local work clone; work="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]+"/round.json"))["work_dir"])' "$run")"; clone="$work/clone"
  cp "$O/$outn.md" "$ROOT/direct_$label.md"
  python3 "$SPARK/tiers/tier_checker.py" "$run/input.json" "$ROOT/direct_$label.md" "$clone" > "$ROOT/direct_$label.out" 2>&1; local rc=$?
  local st; st="$(git -C "$clone" status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
  if [ "$rc" -eq "$want" ] && /usr/bin/grep -q -- "$g" "$ROOT/direct_$label.out" && [ "$st" = 0 ]; then
    ok "$label: checker rc $rc, $(/usr/bin/grep -m1 -- "$g" "$ROOT/direct_$label.out" | cut -c1-210); clone clean after ($st tracked changes)"
  else bad "$label: rc=$rc want $want, grep '$g', clone tracked changes=$st :: $(tail -3 "$ROOT/direct_$label.out" | tr '\n' ' ' | cut -c1-300)"; fi
}
direct R-touches-product "$PL_RUN" touches_product "^FAIL A3 touched set != the declared set: extra \['Blockchain/Dev/scripts/preflight/pf.sh'\]"
direct R-touches-other-suite "$PL_RUN" extra_suite "^FAIL A3 touched set != the declared set: extra \['Blockchain/Dev/scripts/__tests__/unrelated.test.sh'\]"
direct R-wrong-expected-line "$PL_RUN" wrong_context "^FAIL A2 the diff does not apply at the tip"
direct R-bad-hunk-anchor "$PL_RUN" bad_anchor "^FAIL A2a ANCHOR"
direct R-existing-cell-lost "$PL_RUN" lost_cell "^FAIL A6 WHOLE SUITE.*LOST"
direct R-prose-only "$PL_RUN" prose_only "^FAIL A1 no \`\`\`diff block"
direct R-prose-plus-diff "$PL_RUN" prose_and_diff "^FAIL A1 output is not exactly one fenced"
direct K-limit-expect-cell-asserts-nothing "$EX_RUN" cell_asserts_nothing_expect "^RESULT: PASS" 0
# and the checker re-run on the GOOD output after all that abuse must still PASS (restore left the clone exactly at the tip)
direct P-rerun-good-after-abuse "$PL_RUN" good_plant "^RESULT: PASS" 0
direct P-rerun-good-expect-after-abuse "$EX_RUN" good_expect "^RESULT: PASS" 0

# ---------------------------------------------------------------- the three older tiers still wired (regression: the dispatch edits)
for d in x; do
  if /usr/bin/grep -q 'tier_test_only_input(inp, inp_path, out_md, cl)' "$SPARK/tiers/tier_checker.py" && /usr/bin/grep -q 'tier_doc_only(inp, inp_path, out_md, cl)' "$SPARK/tiers/tier_checker.py" \
     && /usr/bin/grep -q 'tier_test_only_bash(inp, inp_path, out_md, cl)' "$SPARK/tiers/tier_checker.py"; then ok "W tier_checker.py dispatches test_only_input, doc_only and test_only_bash"; else bad "W tier_checker.py dispatch lost a tier"; fi
done

echo "test_only_bash_spark_arms: $P PASS, $F FAIL (fixture + outputs in $ROOT)"
[ "$F" -eq 0 ]

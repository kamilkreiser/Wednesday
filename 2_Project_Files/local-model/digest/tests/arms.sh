#!/usr/bin/env bash
# arms.sh - arms for digest.py. Self-locating; never cd's the caller. Spark is STUBBED (DIGEST_SPARK_STUB) except arm L.
# usage: bash arms.sh [--live]     --live adds arm L (one real Spark request, only if the endpoint answers)
# Output: one PASS/FAIL line per arm, then a total. rc 0 iff every arm that ran passed.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
D="$(dirname "$HERE")"; F="$HERE/fixtures"; WORK="$D/.arms_work"
PY=python3; mkdir -p "$WORK"
pass=0; fail=0; notrun=0
ok()  { echo "PASS  $1"; pass=$((pass+1)); }
bad() { echo "FAIL  $1  -- $2"; fail=$((fail+1)); }
jget() { $PY -c "import json,sys;d=json.load(open('$1'));v=d
for k in '$2'.split('.'):
    v=v[int(k)] if k.isdigit() else v[k]
print(v)"; }
# run NAME KIND FIXTURE [stubargs...] -> sets RC, OUT; the stub is generated from the parser's own truth plus the planted fault
run() {
  local name="$1" kind="$2" fx="$3"; shift 3
  OUT="$WORK/$name"; rm -rf "$OUT.stub" 2>/dev/null; mkdir -p "$WORK"
  $PY "$HERE/make_stub.py" "$fx" --kind "$kind" "$@" > "$WORK/$name.stub.json"
  DIGEST_SPARK_STUB="$WORK/$name.stub.json" $PY "$D/digest.py" "$fx" --kind "$kind" --out "$OUT" > "$WORK/$name.stdout" 2>&1
  RC=$?
  ST="$(jget "$OUT/digest.json" status 2>/dev/null)"
}
expect() { # name want_status want_rc
  if [ "$ST" = "$2" ] && [ "$RC" = "$3" ]; then ok "$1 (status $ST rc $RC)"; else bad "$1" "status '$ST' rc '$RC', wanted '$2' rc $3"; fi
}

# 1 real passing vitest (stub = the correct digest)
run a1 vitest "$F/vitest_pass.log"; expect "A1 real passing vitest: CHECKED" CHECKED 0
[ "$(jget "$WORK/a1/digest.json" verdict)" = PASS ] && ok "A1b verdict PASS" || bad "A1b" "verdict not PASS"
# 2 real failing vitest with a planted assertion
run a2 vitest "$F/vitest_fail.log"; expect "A2 real failing vitest (planted assertion): CHECKED" CHECKED 0
grep -q "planted failing assertion" "$WORK/a2/digest.md" && head -1 "$WORK/a2/digest.md" | grep -q '^# FAIL' && ok "A2b digest.md BLUF is FAIL and names the planted test" || bad "A2b" "digest.md lacks FAIL/planted name"
# 2c large real failing vitest, 28 failures, from gate 131
run a2c vitest "$F/vitest_fail_real_gate131.log"; expect "A2c real failing vitest, 28 failures (gate 131): CHECKED" CHECKED 0
[ "$(jget "$WORK/a2c/digest.json" failures | $PY -c 'import sys,ast;print(len(ast.literal_eval(sys.stdin.read())))')" = 28 ] && ok "A2d 28 failures carried" || bad "A2d" "failure count"
# 3 jest
run a3 jest "$F/jest_fail.log"; expect "A3 real failing jest: CHECKED" CHECKED 0
# 4 bash-suite, fail and pass
run a4 bash-suite "$F/bash_fail_docs_fragments.log"; expect "A4 real failing bash-suite (gate 324 docs_fragments): CHECKED" CHECKED 0
run a4b bash-suite "$F/bash_pass_preflight_deps.log"; expect "A4b real passing bash-suite: CHECKED" CHECKED 0
# 4c tsc
run a4c tsc "$F/tsc_fail.log"; expect "A4c real tsc errors: CHECKED" CHECKED 0
# 5 truncated / garbled / empty: must refuse cleanly, no Spark call, rc 3
head -c 400 "$F/vitest_fail.log" > "$WORK/trunc.log"
run a5 vitest "$WORK/trunc.log"; expect "A5 truncated vitest: NO_GROUND_TRUTH" NO_GROUND_TRUTH 3
[ "$(jget "$WORK/a5/check.json" spark_called)" = False ] && ok "A5b the Spark was not asked" || bad "A5b" "Spark was called on a truncated file"
head -c 3000 /dev/urandom > "$WORK/garbled.bin"
run a5c vitest "$WORK/garbled.bin"; expect "A5c garbled binary: NO_GROUND_TRUTH" NO_GROUND_TRUTH 3
: > "$WORK/empty.log"
run a5d jest "$WORK/empty.log"; expect "A5d empty file: NO_GROUND_TRUTH" NO_GROUND_TRUTH 3
head -c 900 "$F/bash_fail_docs_fragments.log" > "$WORK/trunc_bash.log"
run a5e bash-suite "$WORK/trunc_bash.log"; expect "A5e truncated bash-suite (no summary line): NO_GROUND_TRUTH" NO_GROUND_TRUTH 3
head -2 "$F/tsc_fail.log" > "$WORK/trunc_tsc.log"; echo "Found 4 errors in 2 files." >> "$WORK/trunc_tsc.log"
run a5f tsc "$WORK/trunc_tsc.log"; expect "A5f tsc 'Found 4 errors' vs 2 parsed lines: NO_GROUND_TRUTH" NO_GROUND_TRUTH 3
grep -q "Nothing is claimed" "$WORK/a5/digest.md" && ok "A5g refusal digest.md says nothing is claimed" || bad "A5g" "wording"
# 6 planted wrong Spark counts / names / verdict / quotes / anomaly numbers: all must REFUSE and emit the parser's numbers
run a6 vitest "$F/vitest_fail.log" --bump tests_passed; expect "A6 planted wrong Spark count (tests_passed+1): REFUSED" REFUSED_MISMATCH 0
grep -q "tests passed 5" "$WORK/a6/digest.md" && ok "A6b refusal digest.md carries the PARSER's count (5), not the Spark's (6)" || bad "A6b" "parser count absent"
grep -q "count tests_passed" "$WORK/a6/check.json" && ok "A6c mismatch recorded in check.json" || bad "A6c" "not recorded"
run a6d bash-suite "$F/bash_fail_docs_fragments.log" --bump tests_failed; expect "A6d wrong failed count on bash-suite: REFUSED" REFUSED_MISMATCH 0
run a6e vitest "$F/vitest_fail.log" --verdict PASS; expect "A6e Spark says PASS on a failing run: REFUSED" REFUSED_MISMATCH 0
run a6f vitest "$F/vitest_fail_real_gate131.log" --drop-failure; expect "A6f Spark omits one of 28 failures: REFUSED" REFUSED_MISMATCH 0
run a6g vitest "$F/vitest_fail.log" --invent-failure; expect "A6g Spark invents a failure: REFUSED" REFUSED_MISMATCH 0
run a6h vitest "$F/vitest_fail.log" --paraphrase-error; expect "A6h Spark paraphrases the error line (not verbatim): REFUSED" REFUSED_MISMATCH 0
run a6i vitest "$F/vitest_pass.log" --anomaly "a 7431 ms test was slow"; expect "A6i anomaly cites a number absent from the raw: REFUSED" REFUSED_MISMATCH 0
run a6j vitest "$F/vitest_pass.log" --anomaly "the run took 185ms in total, nothing odd" ; [ "$ST" = REFUSED_MISMATCH ] && ok "A6j (control) a number not in the passing log (185) is refused" || bad "A6j" "status $ST"
run a6k vitest "$F/vitest_fail.log" --garbage; expect "A6k Spark replies with prose, not JSON: REFUSED" REFUSED_MISMATCH 0
run a6l vitest "$F/vitest_pass.log" --anomaly "Duration 176ms is short"; expect "A6l (positive control) anomaly number that IS in the raw: CHECKED" CHECKED 0
run a6m vitest "$F/vitest_fail.log" --fence; expect "A6m JSON in a code fence is accepted when correct: CHECKED" CHECKED 0
# 6n/6o Spark format drift seen live: dict-shaped summary rows, and null for an unprinted count -> accepted when the numbers agree
$PY -c "
import json,sys; sys.path.insert(0,'$D'); import digest
t=digest.parse('bash-suite',open('$F/bash_fail_docs_fragments.log').read())
print(json.dumps({'verdict':'FAIL','summary_lines':[{'passed':p,'failed':f,'skipped':k} for p,f,k in t['summaries']],'failures':[{'name':x['name'],'error':x['error'][:100],'frame':''} for x in t['failures']],'anomalies':[]}))" > "$WORK/a6n.stub.json"
DIGEST_SPARK_STUB="$WORK/a6n.stub.json" $PY "$D/digest.py" "$F/bash_fail_docs_fragments.log" --kind bash-suite --out "$WORK/a6n" > /dev/null; RC=$?; ST="$(jget "$WORK/a6n/digest.json" status)"
expect "A6n dict-shaped summary_lines and no counts: CHECKED (counts derived by code)" CHECKED 0
$PY -c "
import json,sys; sys.path.insert(0,'$D'); import digest
t=digest.parse('vitest',open('$F/vitest_fail.log').read()); c=dict(t['counts']); c['tests_skipped']=None; c['files_failed']=c['files_failed']
print(json.dumps({'verdict':'FAIL','counts':c,'failures':[{'name':x['name'],'error':'','frame':''} for x in t['failures']],'anomalies':[]}))" > "$WORK/a6o.stub.json"
DIGEST_SPARK_STUB="$WORK/a6o.stub.json" $PY "$D/digest.py" "$F/vitest_fail.log" --kind vitest --out "$WORK/a6o" > /dev/null; RC=$?; ST="$(jget "$WORK/a6o/digest.json" status)"
[ "$ST" = REFUSED_MISMATCH ] && ok "A6o null for tests_skipped when the parser says 1 (printed): REFUSED" || bad "A6o" "status $ST"
# 7 Spark unreachable: parser summary, rc 0, says so
OUT="$WORK/a7"; SPARK_URL=http://127.0.0.1:9 $PY "$D/digest.py" "$F/vitest_fail.log" --kind vitest --out "$OUT" > "$WORK/a7.stdout" 2>&1; RC=$?; ST="$(jget "$OUT/digest.json" status)"
expect "A7 Spark unreachable: PARSER_ONLY_SPARK_DOWN, rc 0" PARSER_ONLY_SPARK_DOWN 0
grep -q "Spark unreachable" "$OUT/digest.md" && grep -q "tests failed 1" "$OUT/digest.md" && ok "A7b digest.md says unreachable and still carries the parser's counts" || bad "A7b" "wording/counts"
# 7c empty Spark reply (a thinking block) -> fallback
: > "$WORK/empty.stub"; DIGEST_SPARK_STUB="$WORK/empty.stub" $PY "$D/digest.py" "$F/vitest_fail.log" --kind vitest --out "$WORK/a7c" > /dev/null 2>&1; RC=$?; ST="$(jget "$WORK/a7c/digest.json" status)"
expect "A7c empty Spark reply: PARSER_ONLY_SPARK_DOWN, rc 0" PARSER_ONLY_SPARK_DOWN 0
# 8 delta
$PY "$D/digest.py" "$F/vitest_fail.log" --kind vitest --out "$WORK/d_fail" --no-spark > /dev/null
$PY "$D/digest.py" "$F/vitest_pass.log" --kind vitest --out "$WORK/d_pass" --no-spark --delta "$WORK/d_fail/digest.json" > /dev/null; RC=$?
[ "$RC" = 0 ] && [ "$(jget "$WORK/d_pass/digest.json" delta.no_longer_failing.0)" = "a.test.mjs > strings > planted failing assertion" ] && [ "$(jget "$WORK/d_pass/digest.json" delta.newly_failing)" = "[]" ] && ok "A8 delta fail->pass: planted test no longer failing, none newly failing" || bad "A8" "delta wrong"
$PY "$D/digest.py" "$F/vitest_fail.log" --kind vitest --out "$WORK/d_fail2" --no-spark --delta "$WORK/d_pass/digest.json" > /dev/null
[ "$(jget "$WORK/d_fail2/digest.json" delta.newly_failing.0)" = "a.test.mjs > strings > planted failing assertion" ] && [ "$(jget "$WORK/d_fail2/digest.json" delta.count_changes.tests_failed)" = "[0, 1]" ] && ok "A8b delta pass->fail: newly failing named, count change 0->1" || bad "A8b" "delta wrong"
grep -q "Delta vs previous" "$WORK/d_fail2/digest.md" && ok "A8c delta in digest.md" || bad "A8c" "no delta section"
$PY "$D/digest.py" "$F/jest_fail.log" --kind jest --out "$WORK/d_k" --no-spark --delta "$WORK/d_pass/digest.json" > /dev/null; grep -q "kind differs" "$WORK/d_k/digest.md" && ok "A8d delta across kinds is reported, not computed" || bad "A8d" "kind mismatch not reported"
# 9 usage errors
$PY "$D/digest.py" "$WORK/nonexistent" --kind vitest --out "$WORK/nx" >/dev/null 2>&1; [ $? = 2 ] && ok "A9 missing input file: rc 2" || bad "A9" "rc"

# L live arm (one request, the real Spark)
if [ "$1" = "--live" ]; then
  if curl -s -m 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:47788/v1/models | grep -q 200; then
    OUT="$WORK/aL"; $PY "$D/digest.py" "$F/vitest_fail.log" --kind vitest --out "$OUT" > "$WORK/aL.stdout" 2>&1; RC=$?; ST="$(jget "$OUT/digest.json" status)"
    if [ "$ST" = CHECKED ] && [ "$RC" = 0 ]; then ok "L live Spark on the planted-failure vitest log: CHECKED ($(cat "$WORK/aL.stdout" | head -1))"
    else bad "L live Spark" "status $ST rc $RC; see $OUT/check.json"; fi
  else echo "NOT RUN  L live Spark (endpoint 127.0.0.1:47788 not answering)"; notrun=$((notrun+1)); fi
fi
echo "arms: $pass passed, $fail failed, $notrun not run"
[ "$fail" = 0 ]

#!/bin/bash
# bash_patch_newtest_arms.sh — red-proof for the 2026-10-10 section-split fix in tasks/bash_patch/checker.sh
# (modify-then-NEW-FILE golden: the next file's git preamble was glued to the tail of the previous section, so B5's
# product apply re-created the test file B4 had written). Usage: bash bash_patch_newtest_arms.sh [scratch dir]
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
CHK=$LM/tasks/bash_patch/checker.sh
B=$LM/night/briefs/KS-1456-run-migrations-failed-run-message
W="${1:-$(mktemp -d)}"; mkdir -p "$W"; fail=0
latest() { ls -dt "$LM"/runs/spark_secuura_*"$1"-control* 2>/dev/null | head -1; }
verdict() { /usr/bin/grep -E '^(SPARK ROUND|RESULT|FAIL)' "$1" | head -3 | cut -c1-260; }
# 1 and 2: round.sh --control on three goldens (no model call)
for n in "1:KS-1456-run-migrations-failed-run-message:new-file test, product hunk FIRST (the fix)" \
         "2a:KS-1355-stack-guard-one-line-per-project:test_mode=modify, no regression" \
         "2b:KS-1139-smoke-test-counters-errexit:new-file test, no git preamble, no regression"; do
  id="${n%%:*}"; rest="${n#*:}"; brief="${rest%%:*}"; label="${rest#*:}"
  out="$(bash "$LM/spark/round.sh" "$LM/night/briefs/$brief" --control 2>&1 | /usr/bin/grep '^SPARK ROUND' | cut -c1-230)"
  echo "ARM$id ($label): $out"; echo "$out" | /usr/bin/grep -q 'CONTROL-PASS' || fail=1
done
# 2c/2d: the SAVED earlier bash_patch control outputs through the NEW checker, in a scratch clone at each run's own tip
# (the briefs are stale at today's develop, so round.sh cannot re-run them; the checker replay is the same checker code)
replay() { # <id> <run dir name> <label>
  rd="$LM/runs/$2"; tip=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["tip"])' "$rd/input.json")
  c="$W/clone_$1"; git clone -q --shared --no-checkout "$LM/spark/cache/src" "$c" && git -C "$c" checkout -q --detach "$tip"
  bash "$CHK" "$rd/input.json" "$rd/out.md" "$c" > "$W/replay_$1.out" 2>&1; rc=$?
  if /usr/bin/grep -q '^RESULT: PASS' "$W/replay_$1.out"; then echo "ARM$1 PASS ($3; rc=$rc): $(/usr/bin/grep '^RESULT' "$W/replay_$1.out") at tip ${tip:0:12}"; else echo "ARM$1 FAIL ($3; rc=$rc): $(verdict "$W/replay_$1.out" | tr '\n' '|')"; fail=1; fi; }
replay 2c spark_secuura_2026-10-07_KS-1355-stack-guard-one-line-per-project-control "earlier bash_patch control, test_mode=modify (an existing test MODIFIED), new checker"
replay 2d spark_secuura_2026-10-07_KS-1139-smoke-test-counters-errexit-control "earlier bash_patch control, new-file test, no git preamble, new checker"
# 3/4: mutated KS-1456 goldens straight through the checker, in the control run's own clone + input
R=$(ls -dt "$LM"/runs/spark_secuura_*KS-1456-run-migrations-failed-run-message-control* | head -1)
IN=$R/input.json; CLONE=$(ls -dt "$LM"/spark/cache/work/*KS-1456*/clone | head -1)
mut() { python3 - "$B/golden.diff" "$W/$1.md" "$2" <<'PY'
import sys
src,dst,expr=sys.argv[1:4]; ns={"t":open(src,encoding="utf-8").read()}; exec(expr,ns)
open(dst,"w",encoding="utf-8").write("```diff\n"+ns["t"].rstrip("\n")+"\n```\n")
PY
}
arm() { # <id> <md> <want regex> <label>
  bash "$CHK" "$IN" "$W/$2.md" "$CLONE" > "$W/$2.out" 2>&1; rc=$?
  if /usr/bin/grep -qE "$3" "$W/$2.out"; then echo "ARM$1 PASS ($4; rc=$rc): $(/usr/bin/grep -E "$3" "$W/$2.out" | head -1 | cut -c1-230)"; else echo "ARM$1 FAIL ($4; rc=$rc): $(verdict "$W/$2.out" | tr '\n' '|')"; fail=1; fi; }
mut a3 't=t.replace("+  echo \"002/005 failing every boot) were changed under KS-1031. Exit 3 - the code this\"\n","+  echo \"002/005 failing every boot) were changed under KS-1031. Exit 3 - the code this\"\n+  echo \"the remaining applied=N-counts-skips defect\"\n",1).replace("@@ -184,8 +184,7 @@","@@ -184,8 +184,8 @@")'
arm 3 a3 '^FAIL B5 GREEN-AFTER: .*still red' "product hunk leaves the counts-skips text: new test stays red"
mut a4a 't=t.replace("@@ -0,0 +1,92 @@","@@ garbage @@",1)'
arm 4a a4a '^(FAIL B[0-9]|RESULT: FAIL)' "malformed test hunk header refused"
mut a4b 't=t.replace("+#!/usr/bin/env bash\n","+#!/usr/bin/env bash\n+if then fi ((\n",1).replace("@@ -0,0 +1,92 @@","@@ -0,0 +1,93 @@")'
arm 4b a4b '^FAIL B4 the new test does not parse' "test with a syntax error refused at B4"
echo "scratch (kept): $W"; exit $fail

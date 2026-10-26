#!/usr/bin/env bash
# Arms for the NON-pytest runner path of spark_gate.sh (bash suites + vitest). Builds a tiny fixture repo with a local bare
# "origin" (refs/pull/1/head = good PR, refs/pull/2/head = PR with a PLANTED failing test), runs the gate, asserts counts.
# usage: test_gate_runner_arms.sh [scratch-dir-OUTSIDE-/Volumes/DevMASTER/WEDNESDAY]   (default: $TMPDIR)
# Needs the vitest fixture install: tests/fixtures/vitest_repo/node_modules (npm install --prefix there). Missing -> vitest arms print SKIP.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; G="$HERE/../spark_gate.sh"; NM="$HERE/fixtures/vitest_repo/node_modules"
SCR="$(mktemp -d "${1:-${TMPDIR:-/tmp}}/runner_arms.XXXXXX")" || exit 64
fail=0; pass=0; skip=0
ok()   { echo "ARM$1 PASS: $2"; pass=$((pass+1)); }
bad()  { echo "ARM$1 FAIL: $2"; fail=$((fail+1)); }
git_() { git -c user.name=arm -c user.email=arm@arm "$@"; }
ORIGIN="$SCR/origin.git"; W="$SCR/w"; git init -q --bare "$ORIGIN"; git init -q "$W"
# write_tree <mul-shell-body> <mul-js-body> <with-mul 0|1>
write_tree() {
  mkdir -p "$W/scripts" "$W/src"
  printf 'add() { echo $(($1+$2)); }\n' > "$W/lib.sh"; [ "$3" = 1 ] && printf 'mul() { echo $((%s)); }\n' "$1" >> "$W/lib.sh"
  { cat <<'T'
#!/bin/bash
HERE="$(cd "$(dirname "$0")/.." && pwd)"; . "$HERE/lib.sh"; PASS=0; FAIL=0
t() { if [ "$2" = "$3" ]; then PASS=$((PASS+1)); else FAIL=$((FAIL+1)); echo "  FAIL: $1 (got $3 want $2)"; fi; }
t "add 1 2" 3 "$(add 1 2)"
t "add 0 0" 0 "$(add 0 0)"
T
    [ "$3" = 1 ] && echo 't "mul 3 4" 12 "$(mul 3 4)"'
    cat <<'T'
echo "t.test: $PASS passed, $FAIL failed"; [ "$FAIL" -eq 0 ]
T
  } > "$W/scripts/t.test.sh"
  printf 'export const add = (a, b) => a + b\n' > "$W/src/math.js"; [ "$3" = 1 ] && printf 'export const mul = (a, b) => %s\n' "$2" >> "$W/src/math.js"
  { cat <<'T'
import { describe, it, expect } from 'vitest'
import * as m from './math.js'
describe('math', () => {
  it('add 1 2', () => expect(m.add(1, 2)).toBe(3))
  it('add 0 0', () => expect(m.add(0, 0)).toBe(0))
T
    [ "$3" = 1 ] && echo "  it('mul 3 4', () => expect(m.mul(3, 4)).toBe(12))"
    echo '})'
  } > "$W/src/math.test.js"
  cp "$HERE/fixtures/vitest_repo/package.json" "$W/package.json"; printf 'node_modules\n' > "$W/.gitignore"
}
write_tree x x 0; git_ -C "$W" add -A; git_ -C "$W" commit -qm base; git_ -C "$W" branch -M develop; git_ -C "$W" push -q "$ORIGIN" develop
pr() { git_ -C "$W" checkout -q -B "pr$1" develop; write_tree "$2" "$3" 1; git_ -C "$W" add -A; git_ -C "$W" commit -qm "pr$1"; git_ -C "$W" push -q "$ORIGIN" "pr$1:refs/pull/$1/head"; }
pr 1 '$1*$2' 'a * b'; H1="$(git -C "$W" rev-parse HEAD)"
pr 2 '$1+$2' 'a + b'; H2="$(git -C "$W" rev-parse HEAD)"   # PLANTED: mul returns the sum -> 7, not 12
N=0
gate() { local n="$1" h="$2"; shift 2; N=$((N+1)); clone="$SCR/c$N"; git clone -q "$ORIGIN" "$clone"; OUTD="$SCR/out$N"
  bash "$G" "$clone" "$n" "$h" develop "$@" --work "$SCR/work$N" --out "$OUTD" --node-modules "$NM" < /dev/null; }
chk() {  # $1 arm  $2 desc  $3 facts-file  $4 python expression over f
  if python3 -I -c "import json,sys; f=json.load(open('$3')); sys.exit(0 if ($4) else 1)" 2>/dev/null; then ok "$1" "$2"
  else bad "$1" "$2  [got: $(python3 -I -c "import json;f=json.load(open('$3'));print(f['targeted_head_totals'],f['targeted_base_totals'])" 2>&1 | tail -1)]"; fi
}
gate 1 "$H1" scripts/t.test.sh > "$SCR/g1.out" 2>&1
chk 1 "shell suite, good PR: HEAD 3 passed 0 failed; BASE product code 2 passed 1 failed (red on base, green on head)" "$OUTD/facts.json" \
  "f['targeted_head_totals']['passed']==3 and f['targeted_head_totals']['failed']==0 and f['targeted_head_totals']['files_failed']==0 and f['targeted_base_totals']['passed']==2 and f['targeted_base_totals']['failed']==1 and f['targeted_base_totals']['files_failed']==1"
gate 2 "$H2" scripts/t.test.sh > "$SCR/g2.out" 2>&1
chk 2 "shell suite, PLANTED failure: HEAD shows 2 passed 1 failed, file not ok (a check that can fail)" "$OUTD/facts.json" \
  "f['targeted_head_totals']['passed']==2 and f['targeted_head_totals']['failed']==1 and f['targeted_head_totals']['files_failed']==1 and f['targeted_on_head'][0]['ok'] is False"
if [ -d "$NM/vitest" ]; then
  gate 1 "$H1" src/math.test.js > "$SCR/g3.out" 2>&1
  chk 3 "vitest file, good PR: HEAD 3 passed 0 failed; BASE product code 2 passed 1 failed (red on base)" "$OUTD/facts.json" \
    "f['targeted_head_totals']['passed']==3 and f['targeted_head_totals']['failed']==0 and f['targeted_base_totals']['failed']==1 and f['targeted_base_totals']['passed']==2"
  gate 2 "$H2" src/math.test.js > "$SCR/g4.out" 2>&1
  chk 4 "vitest file, PLANTED failure: HEAD 2 passed 1 failed, file not ok" "$OUTD/facts.json" \
    "f['targeted_head_totals']['passed']==2 and f['targeted_head_totals']['failed']==1 and f['targeted_on_head'][0]['ok'] is False"
else echo "ARM3 SKIP: vitest not installed under $NM (npm install --prefix tests/fixtures/vitest_repo)"; echo "ARM4 SKIP: same"; skip=$((skip+2)); fi
gate 1 "$H1" scripts/t.test.sh scripts/nope.test.sh > /dev/null 2>&1; rc=$?; [ $rc -eq 4 ] && ok 5 "missing test file refused (exit 4)" || bad 5 "missing file: exit $rc"
gate 1 "$H1" scripts/t.test.sh foo_test.py > /dev/null 2>&1; rc=$?; [ $rc -eq 2 ] && ok 6 "mixed .sh + .py refused (exit 2)" || bad 6 "mixed: exit $rc"
gate 1 0123456789abcdef0123456789abcdef01234567 scripts/t.test.sh > /dev/null 2>&1; rc=$?; [ $rc -eq 3 ] && ok 7 "wrong head sha refused on the non-pytest path (exit 3)" || bad 7 "sha: exit $rc"
# ARM8: no --node-modules at all (bash 3.2 + set -u regression found 2026-10-26 on the first live run)
N=$((N+1)); clone="$SCR/c$N"; git clone -q "$ORIGIN" "$clone"; bash "$G" "$clone" 1 "$H1" develop scripts/t.test.sh --work "$SCR/work$N" --out "$SCR/out$N" < /dev/null > "$SCR/g8.out" 2>&1
chk 8 "shell suite with no --node-modules flag runs (empty-array under set -u)" "$SCR/out$N/facts.json" "f['targeted_head_totals']['passed']==3"
echo "gate runner arms: $pass passed, $fail failed, $skip skipped (scratch: $SCR)"; [ $fail -eq 0 ]

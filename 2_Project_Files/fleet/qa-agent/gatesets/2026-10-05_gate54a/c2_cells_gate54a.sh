#!/bin/bash
# c2_cells_gate54a.sh — gate54a C2 BEHAVIOUR (and the runtime half of C3). bash 3.2 / zsh safe: no associative arrays, no mapfile, no ${x,,},
# and NO rc is ever read through a pipe (every command: `cmd > out 2> err; rc=$?`, the rc written to its own .rc file).
# Subcommands (WS = the repo root of a worktree YOU created in YOUR scratch clone; OUT = your evidence dir):
#   plan                         READ-ONLY, from the shared checkout's object store (git show / cat-file only): the test file's cells (4),
#                                0 vi.mock of ../middleware/authenticate beside the must-hit count of every vi.mock( module mock, a REAL
#                                generateConnectorToken mint, users.ts:266 at base (authenticate()) and head (authenticateAccessOrConnector()),
#                                and tsconfig's exclude of src/__tests__ (so tsc never type-checks the new test). Prints the run plan.
#   parse-selftest               c2_parse_gate54a.py --selftest (14 arms: a load failure is never a red, a skipped cell is not a pass, ...).
#   install WS OUT               `npm ci --ignore-scripts` at Blockchain/Dev, then `npm run build --workspace=packages/shared` (X1).
#   run base WS OUT              WS at kit base: (1) the FULL auth suite pristine -> base_suite.json (builder: 77 files / 836 tests);
#                                (2) PLANT the head's ks1402 test (git show HEAD:<test> into WS), run it alone -> base_cells.json: cells 1,2,4
#                                RED with `expected 401 to be 200/403/404`, cell 3 GREEN; (3) QUARANTINE the planted file into OUT (never rm).
#   run head WS OUT              WS at the pinned head: the ks1402 file alone -> head_cells.json (4/4 GREEN); the FULL suite -> head_suite.json
#                                (builder: 78 / 840, 0 failed); then diff-suites base vs head (+1 file, +4 tests = the cells, 0 regressions).
#   tsc base|head WS OUT         `npx tsc --noEmit -p .` in services/auth: rc and `error TS` count; base == head is a NO-REGRESSION reading only.
#   mutate WS OUT                WS at the head: arm users = users.ts set to its BASE blob -> cells 1/2 RED (4 also red); arm authmw =
#                                authenticate.ts set to its BASE blob -> 4/4 GREEN (the PR's own claim: no cell covers the label). Each file is
#                                restored from the head blob and its sha256 proven equal to before; `git status --porcelain` empty after.
#   probe base|head WS OUT       the C3 runtime probe (probe_ks1402_authsurface.test.ts.txt) copied in as
#                                src/__tests__/zz-g54a-probe-authsurface.test.ts, run alone, judged, then QUARANTINED into OUT.
# Every write is inside WS (a worktree you created) or OUT. REFUSES (rc 2, before writing) a WS inside /Volumes/DevMASTER/!CODING/ (the shared
# checkout and every builder worktree live there), a WS whose HEAD is not the side's sha, or an OUT inside !CODING/ other than the report dir.
# Env: G54A_HEAD (the pinned head; default kit expected_head). rc: 0 PASS / 1 FAIL / 2 refusal or usage / 3 a tool step failed (rc printed).
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))[sys.argv[2]]; print(v if isinstance(v,str) else json.dumps(v))' "$GS/kit.json" "$1"; }
CHECKOUT="$(KJ checkout)"; BASE="$(KJ base)"; HEADSHA="${G54A_HEAD:-$(KJ expected_head)}"; TESTF="$(KJ test_file)"; USERS="$(KJ users_routes)"; AMW="$(KJ authenticate_mw)"
PARSE="$GS/c2_parse_gate54a.py"; PROBE_SRC="$GS/probe_ks1402_authsurface.test.ts.txt"; PROBE_REL="Blockchain/Dev/services/auth/src/__tests__/zz-g54a-probe-authsurface.test.ts"
usage() { sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; }
step() {  # step <name> <outdir> <cmd...> : run, write .out/.err/.rc, echo the rc line; never through a pipe
  _n="$1"; _o="$2"; shift 2
  "$@" > "$_o/$_n.out" 2> "$_o/$_n.err"; _rc=$?
  echo "$_rc" > "$_o/$_n.rc"; echo "  $_n rc=$_rc ($(date -u +%H:%M:%SZ))"
  return $_rc
}
guard_ws() {  # guard_ws <ws> <want-sha>
  _ws="$1"; _want="$2"
  [ -d "$_ws" ] || { echo "REFUSING: WS $_ws is not a directory"; exit 2; }
  _r="$(/bin/realpath "$_ws")"
  case "$_r" in "/Volumes/DevMASTER/!CODING/"*) echo "REFUSING: WS $_r is inside /Volumes/DevMASTER/!CODING/ — the shared checkout and the builder's worktrees are READ ONLY; use a worktree in YOUR scratch clone"; exit 2;; esac
  [ -d "$_r/Blockchain/Dev/services/auth" ] || { echo "REFUSING: $_r has no Blockchain/Dev/services/auth (WS is the REPO ROOT of your worktree)"; exit 2; }
  _h="$(git -C "$_r" rev-parse HEAD 2> /dev/null)"
  [ "$_h" = "$_want" ] || { echo "REFUSING: WS HEAD is '$_h', this side needs $_want"; exit 2; }
  WSR="$_r"; AUTH="$_r/Blockchain/Dev/services/auth"
}
guard_out() {  # the prefix test runs on the LEXICAL absolute path BEFORE any mkdir (the drafter's 2026-10-05 exercise proved the old order wrote first)
  _l="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$1")"
  case "$_l" in "/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/"*) ;; "/Volumes/DevMASTER/!CODING/"*) echo "REFUSING: OUT $_l is inside !CODING/ but not under the QA reports root (nothing was created)"; exit 2;; esac
  mkdir -p "$_l" || { echo "REFUSING: cannot create OUT $_l"; exit 2; }
  _o="$(/bin/realpath "$_l")"
  case "$_o" in "/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/"*) ;; "/Volumes/DevMASTER/!CODING/"*) echo "REFUSING: OUT $_o resolves inside !CODING/ but not under the QA reports root"; exit 2;; esac
  OUTR="$_o"
}
clean_or_fail() {
  git -C "$WSR" status --porcelain > "$OUTR/$1.status.out" 2> "$OUTR/$1.status.err"; _rc=$?
  _n="$(wc -l < "$OUTR/$1.status.out" | tr -d ' ')"
  echo "  worktree status after $1: rc $_rc, $_n dirty path(s) (want 0)"
  [ "$_rc" = 0 ] && [ "$_n" = 0 ]
}
quarantine() {  # quarantine <ws-relative path> <tag>: move a planted file into OUT/quarantine (never rm)
  mkdir -p "$OUTR/quarantine" && mv "$WSR/$1" "$OUTR/quarantine/$2.$(date -u +%H%M%S).$(basename "$1")" && echo "  quarantined $1 -> $OUTR/quarantine/"
}
vitest() {  # vitest <name> <json> [file] : in services/auth, a subshell cd (never the caller's shell)
  _name="$1"; _json="$2"; shift 2
  ( cd "$AUTH" && npx vitest run "$@" --reporter=default --reporter=json --outputFile="$_json" ) > "$OUTR/$_name.out" 2> "$OUTR/$_name.err"; _rc=$?
  echo "$_rc" > "$OUTR/$_name.rc"; echo "  $_name rc=$_rc ($(date -u +%H:%M:%SZ)) -> $(basename "$_json")"
  return 0
}
judge() {  # judge <name> <parse args...>
  _name="$1"; shift
  python3 "$PARSE" "$@" > "$OUTR/$_name.out" 2> "$OUTR/$_name.err"; _rc=$?
  echo "$_rc" > "$OUTR/$_name.rc"; sed 's/^/    /' "$OUTR/$_name.out" | cut -c1-240
  return $_rc
}
sha() { shasum -a 256 "$1" | awk '{print $1}'; }

CMD="${1:-}"
case "$CMD" in
  ''|-h|--help) usage; [ -n "$CMD" ] && exit 0; exit 2;;
  plan)
    echo "C2 PLAN $(date -u +%Y-%m-%dT%H:%M:%SZ) | checkout $CHECKOUT (READ ONLY: show / cat-file) | base $BASE | head $HEADSHA"
    git -C "$CHECKOUT" cat-file -e "$HEADSHA:$TESTF" 2> /dev/null; rc=$?
    echo "  test file at head: cat-file -e rc $rc (control: the same path at base, which must be ABSENT)"
    git -C "$CHECKOUT" cat-file -e "$BASE:$TESTF" 2> /dev/null; rcb=$?
    echo "  test file at base: cat-file -e rc $rcb (want non-zero: the file is NEW)"
    python3 - "$TESTF" <<PY
import re, subprocess, sys
t = subprocess.run(['git', '-C', '''$CHECKOUT''', 'show', '''$HEADSHA''' + ':' + sys.argv[1]], capture_output=True, text=True).stdout
its = re.findall(r"^\s*it\('(CELL \d+)[^']*'", t, re.M); mods = re.findall(r"vi\.mock\(\s*'([^']+)'", t)
print('  cells (it( titles): %d %s (want 4: CELL 1..4)' % (len(its), its))
print('  module mocks vi.mock(: %d %s | of ../middleware/authenticate: %d (want 0) | MUST-HIT: the same regex finds %d (want >= 1)' % (len(mods), mods, mods.count('../middleware/authenticate'), len(mods)))
print('  substring "vi.mock" (incl. vi.mocked): %d — the PR doc block\'s "9 vi.mock calls" is this substring count, not 9 module mocks' % t.count('vi.mock'))
print('  generateConnectorToken( %d | type access with role connector minted in CODE lines here: %d (want 0: the green-at-base trap of auth.integration.test.ts:1398/:1419)' % (t.count('generateConnectorToken('), len(re.findall(r"type:\s*'access'", '\n'.join(l for l in t.split('\n') if not l.strip().startswith('//'))))))
PY
    for c in "$BASE" "$HEADSHA"; do
      L="$(git -C "$CHECKOUT" show "$c:$USERS" | sed -n '266p')"
      echo "  users.ts:266 at ${c:0:12}: $(printf '%s' "$L" | cut -c1-90)"
    done
    TS="$(git -C "$CHECKOUT" show "$HEADSHA:$(KJ tsconfig)" 2> /dev/null)"
    echo "  tsconfig exclude: $(printf '%s' "$TS" | python3 -c 'import json,re,sys; t=re.sub(r"//.*","",sys.stdin.read()); print(json.loads(t).get("exclude"))' 2>&1)"
    echo "  RUN PLAN: install WS_BASE OUT; run base WS_BASE OUT; tsc base WS_BASE OUT; probe base WS_BASE OUT | install WS_HEAD OUT; run head WS_HEAD OUT; tsc head WS_HEAD OUT; mutate WS_HEAD OUT; probe head WS_HEAD OUT"
    [ "$rc" = 0 ] && [ "$rcb" != 0 ] && { echo "C2 PLAN OK"; exit 0; }
    echo "C2 PLAN FAIL (test file presence)"; exit 1;;
  parse-selftest)
    python3 "$PARSE" --selftest; exit $?;;
  install)
    WS="${2:-}"; O="${3:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    _h="$(git -C "$WS" rev-parse HEAD 2> /dev/null)"; guard_ws "$WS" "$_h"; guard_out "$O"
    [ "$_h" = "$BASE" ] || [ "$_h" = "$HEADSHA" ] || { echo "REFUSING: WS HEAD $_h is neither kit base nor the head"; exit 2; }
    T="install_${_h:0:12}"
    ( cd "$WSR/Blockchain/Dev" && npm ci --ignore-scripts ) > "$OUTR/$T.npmci.out" 2> "$OUTR/$T.npmci.err"; rc=$?; echo "$rc" > "$OUTR/$T.npmci.rc"; echo "  npm ci --ignore-scripts rc=$rc"
    [ "$rc" = 0 ] || exit 3
    ( cd "$WSR/Blockchain/Dev" && npm run build --workspace=packages/shared ) > "$OUTR/$T.shared.out" 2> "$OUTR/$T.shared.err"; rc=$?; echo "$rc" > "$OUTR/$T.shared.rc"; echo "  build packages/shared rc=$rc"
    [ "$rc" = 0 ] || exit 3
    clean_or_fail "$T" || echo "  NOTE: dirty after install (name each path; node_modules / dist should be gitignored)"
    exit 0;;
  run)
    SIDE="${2:-}"; WS="${3:-}"; O="${4:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    guard_out "$O"
    if [ "$SIDE" = base ]; then
      guard_ws "$WS" "$BASE"; echo "C2 RUN BASE $(date -u +%Y-%m-%dT%H:%M:%SZ) | WS $WSR @ $BASE | OUT $OUTR"
      [ -e "$WSR/$TESTF" ] && { echo "REFUSING: the ks1402 test already exists in the base WS (a stale plant?)"; exit 2; }
      vitest base_suite "$OUTR/base_suite.json"
      judge base_suite.judge suite "$OUTR/base_suite.json" --console "$OUTR/base_suite.out" --expect-files 77 --expect-tests 836; r1=$?
      git -C "$WSR" show "$HEADSHA:$TESTF" > "$WSR/$TESTF" 2> "$OUTR/plant_test.err"; rc=$?
      echo "  planted the head's test into the base WS: rc $rc sha256 $(sha "$WSR/$TESTF") (head blob $(KJ drafted_head_blobs | python3 -c 'import json,sys; print(json.load(sys.stdin)[sys.argv[1]][:12])' "$TESTF"))"
      [ "$rc" = 0 ] || exit 3
      vitest base_cells "$OUTR/base_cells.json" "src/__tests__/$(basename "$TESTF")"
      judge base_cells.judge cells "$OUTR/base_cells.json" base --console "$OUTR/base_cells.out"; r2=$?
      quarantine "$TESTF" base-plant; clean_or_fail base_after; r3=$?
      [ "$r1" = 0 ] && [ "$r2" = 0 ] && [ "$r3" = 0 ] && { echo "C2 BASE PASS (suite 77/836 pristine; cells 1,2,4 red by assertion, 3 green)"; exit 0; }
      echo "C2 BASE FAIL (suite judge rc $r1, cells judge rc $r2, clean rc $r3) — read the judges above; a count difference from the builder's is a finding, not a tool error"; exit 1
    elif [ "$SIDE" = head ]; then
      guard_ws "$WS" "$HEADSHA"; echo "C2 RUN HEAD $(date -u +%Y-%m-%dT%H:%M:%SZ) | WS $WSR @ $HEADSHA | OUT $OUTR"
      vitest head_cells "$OUTR/head_cells.json" "src/__tests__/$(basename "$TESTF")"
      judge head_cells.judge cells "$OUTR/head_cells.json" head --console "$OUTR/head_cells.out"; r1=$?
      vitest head_suite "$OUTR/head_suite.json"
      judge head_suite.judge suite "$OUTR/head_suite.json" --console "$OUTR/head_suite.out" --expect-files 78 --expect-tests 840 --expect-fail 0; r2=$?
      r3=0
      if [ -s "$OUTR/base_suite.json" ]; then judge suites.diff diff-suites "$OUTR/base_suite.json" "$OUTR/head_suite.json"; r3=$?; else echo "  NOTE: no base_suite.json in OUT — run 'run base' first for the diff"; r3=1; fi
      clean_or_fail head_after; r4=$?
      [ "$r1" = 0 ] && [ "$r2" = 0 ] && [ "$r3" = 0 ] && [ "$r4" = 0 ] && { echo "C2 HEAD PASS (4/4 green; 78/840, 0 failed; +1 file +4 tests, 0 regressions)"; exit 0; }
      echo "C2 HEAD FAIL (cells $r1, suite $r2, diff $r3, clean $r4)"; exit 1
    fi
    usage; exit 2;;
  tsc)
    SIDE="${2:-}"; WS="${3:-}"; O="${4:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    guard_out "$O"; if [ "$SIDE" = base ]; then guard_ws "$WS" "$BASE"; elif [ "$SIDE" = head ]; then guard_ws "$WS" "$HEADSHA"; else usage; exit 2; fi
    ( cd "$AUTH" && npx tsc --noEmit -p . ) > "$OUTR/tsc_$SIDE.out" 2> "$OUTR/tsc_$SIDE.err"; rc=$?; echo "$rc" > "$OUTR/tsc_$SIDE.rc"
    n="$(grep -c 'error TS' "$OUTR/tsc_$SIDE.out")"
    echo "TSC $SIDE rc=$rc errors=$n ($(date -u +%H:%M:%SZ)) — compare base vs head yourself: equal rc AND equal count is a no-regression reading only (tsconfig excludes src/__tests__)"
    exit 0;;
  mutate)
    WS="${2:-}"; O="${3:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    guard_ws "$WS" "$HEADSHA"; guard_out "$O"; echo "C2 MUTATE $(date -u +%Y-%m-%dT%H:%M:%SZ) | WS $WSR @ $HEADSHA"
    clean_or_fail mut_before || { echo "REFUSING: the head WS is dirty before the mutation"; exit 2; }
    rr=0
    for arm in users authmw; do
      if [ "$arm" = users ]; then P="$USERS"; else P="$AMW"; fi
      s0="$(sha "$WSR/$P")"
      git -C "$WSR" show "$BASE:$P" > "$WSR/$P" 2> "$OUTR/mut_$arm.plant.err"; rc=$?
      echo "  arm $arm: $P set to its BASE blob rc $rc (sha256 $(sha "$WSR/$P" | cut -c1-12), was $(printf '%s' "$s0" | cut -c1-12))"
      vitest "mut_$arm" "$OUTR/mut_$arm.json" "src/__tests__/$(basename "$TESTF")"
      judge "mut_$arm.judge" mutation "$OUTR/mut_$arm.json" "$arm"; r=$?; [ "$r" = 0 ] || rr=1
      git -C "$WSR" show "$HEADSHA:$P" > "$WSR/$P" 2> "$OUTR/mut_$arm.restore.err"; rc=$?
      s1="$(sha "$WSR/$P")"
      echo "  arm $arm restored rc $rc: sha256 before $(printf '%s' "$s0" | cut -c1-16) after $(printf '%s' "$s1" | cut -c1-16) equal: $([ "$s0" = "$s1" ] && echo yes || echo NO)"
      [ "$s0" = "$s1" ] || rr=1
    done
    clean_or_fail mut_after || rr=1
    [ "$rr" = 0 ] && { echo "C2 MUTATION PASS (users.ts reverted -> cells 1/2 red; authenticate.ts reverted -> 4/4 green: the label is not test-guarded, as the PR says)"; exit 0; }
    echo "C2 MUTATION FAIL"; exit 1;;
  probe)
    SIDE="${2:-}"; WS="${3:-}"; O="${4:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    guard_out "$O"; if [ "$SIDE" = base ]; then guard_ws "$WS" "$BASE"; elif [ "$SIDE" = head ]; then guard_ws "$WS" "$HEADSHA"; else usage; exit 2; fi
    [ -e "$WSR/$PROBE_REL" ] && { echo "REFUSING: a probe file already sits in the WS"; exit 2; }
    cp "$PROBE_SRC" "$WSR/$PROBE_REL" || exit 3
    echo "C3 PROBE $SIDE $(date -u +%Y-%m-%dT%H:%M:%SZ) | probe sha256 $(sha "$WSR/$PROBE_REL" | cut -c1-16) | WS $WSR"
    vitest "probe_$SIDE" "$OUTR/probe_$SIDE.json" "src/__tests__/zz-g54a-probe-authsurface.test.ts"
    judge "probe_$SIDE.judge" probe "$OUTR/probe_$SIDE.json" "$SIDE"; r=$?
    grep 'G54A ' "$OUTR/probe_$SIDE.out" > "$OUTR/probe_$SIDE.console_lines.txt" 2> /dev/null
    echo "  probe console lines: $(wc -l < "$OUTR/probe_$SIDE.console_lines.txt" | tr -d ' ') (G54A-tagged; P5/P5b statuses are REPORTED, the gate rules them)"
    quarantine "$PROBE_REL" "probe-$SIDE"; clean_or_fail "probe_${SIDE}_after" || r=1
    [ "$r" = 0 ] && { echo "C3 PROBE $SIDE PASS"; exit 0; }
    echo "C3 PROBE $SIDE FAIL (read the judge)"; exit 1;;
  *) usage; exit 2;;
esac

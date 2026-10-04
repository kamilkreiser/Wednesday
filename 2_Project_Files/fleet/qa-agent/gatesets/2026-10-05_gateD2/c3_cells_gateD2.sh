#!/bin/bash
# c3_cells_gateD2.sh — gateD2 C3 BEHAVIOUR: the KS 1404 cells, the suites, tsc, the mutation arms and the kit's two independent probes.
# A NEW COPY of gate54a's c2_cells_gate54a.sh, re-keyed for services/timestamping. bash 3.2 / zsh safe: NO rc is ever read through a pipe
# (every command: `cmd > out 2> err; rc=$?`, the rc written to its own .rc file). Never `cd` in the caller's shell (subshells only).
# WS = the REPO ROOT of a worktree YOU created in YOUR scratch clone under /private/tmp/claude-501/; OUT = your evidence dir.
#   plan                       READ-ONLY from the shared checkout (git show / cat-file): the KS 1404 file's cells by title, the route
#                              harness's mocks, whether `../tsa/rfc3161-verify` / `./ks1404-pki` exist at base (they must NOT), tsconfig's
#                              exclude of src/__tests__ (tsc never type-checks the cells), and the run plan.
#   parse-selftest             c3_parse_gateD2.py --selftest (12 arms).
#   pki OUT                    probe_pki_gateD2.sh OUT/pki (OpenSSL test PKI for the forgery probe).
#   install WS OUT             `npm ci --ignore-scripts` at Blockchain/Dev, then `npm run build --workspace=packages/shared` (the workspace
#                              install: a member-only install leaves suites unable to LOAD — the cheat sheet's own gotcha).
#   run base WS OUT            WS at the kit base: (1) the FULL timestamping suite pristine -> base_suite.json (builder: 5 files / 44 tests);
#                              (2) PLANT the head's KS 1404 test file AND ks1404-pki.ts, run the file alone -> base_cells.json: the red set
#                              (cells 1, 3, 11 indefiniteLength, 12, 14) RED BY ASSERTION, skips reported as a failed beforeAll;
#                              (3) QUARANTINE both planted files into OUT (never rm); `git status --porcelain` empty after.
#   run head WS OUT            WS at the pinned head: the KS 1404 file alone -> 25/25 green, 0 skipped; the FULL suite -> 6 / 69 (builder),
#                              0 failed; diff-suites vs OUT/base_suite.json (+1 file, +25 tests = the KS 1404 file, 0 regressions).
#   tsc base|head WS OUT       the NAMED hoisted binary <WS>/Blockchain/Dev/node_modules/.bin/tsc --noEmit -p services/timestamping;
#                              POSITIVE CONTROL in the same call: the same binary on a planted `const x: number = 'a'` in OUT -> rc 2 + TS2322.
#   mutate WS OUT              WS at the head: each c3_mutate_gateD2.py arm planted, the KS 1404 file run, judged (want its cell red and
#                              NOTHING else red), the file restored from the HEAD blob with sha256 proven equal; porcelain empty after.
#   probe base|head WS OUT     the kit's probes copied in as src/__tests__/zz-gD2-probe-*.test.ts, run alone, judged, QUARANTINED:
#                              head: the forgery probe (needs OUT/pki from `pki`) + the mock probe; base: the mock probe only (M1-M3 TRUE).
#                              BOTH sides: the request-bytes probe (72 cases); head compares to base with c3_reqbytes_gateD2.py (forge == der.ts).
# REFUSES (rc 2, BEFORE any write) a WS outside /private/tmp/claude-501/ (the shared checkout and the builder's worktrees live under
# /Volumes/DevMASTER/!CODING/), a WS whose HEAD is not the side's sha, and an OUT outside /private/tmp/claude-501/ or the QA reports root —
# each tested on the LEXICAL path before mkdir (gate54a's exercise once created `Secuura/x` by testing after mkdir).
# Env: GD2_HEAD (the pinned head; REQUIRED for head-side modes — the kit has no drafted final head), GD2_BASE (default kit base).
# rc: 0 PASS / 1 FAIL / 2 refusal or usage / 3 a tool step failed (rc printed).
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))[sys.argv[2]]; print(v if isinstance(v,str) else json.dumps(v))' "$GS/kit.json" "$1"; }
CHECKOUT="$(KJ checkout)"; BASE="${GD2_BASE:-$(KJ base)}"; HEADSHA="${GD2_HEAD:-}"; TESTF="$(KJ test_file)"; PKIF="$(KJ pki_helper)"; SVC="$(KJ service)"
PARSE="$GS/c3_parse_gateD2.py"; MUT="$GS/c3_mutate_gateD2.py"
usage() { sed -n '2,34p' "$0" | sed 's/^# \{0,1\}//'; }
lex() { python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$1"; }
guard_out() {
  _l="$(lex "$1")"
  case "$_l" in "/private/tmp/claude-501/"*|"/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/"*) ;; *) echo "REFUSING: OUT $_l is not under /private/tmp/claude-501/ or the QA reports root (nothing was created)"; exit 2;; esac
  mkdir -p "$_l" || { echo "REFUSING: cannot create OUT $_l"; exit 2; }
  OUTR="$(/bin/realpath "$_l")"
}
guard_ws() {  # guard_ws <ws> <want-sha>
  _l="$(lex "$1")"
  case "$_l" in "/private/tmp/claude-501/"*) ;; *) echo "REFUSING: WS $_l is not under /private/tmp/claude-501/ — use a worktree in YOUR scratch clone (the shared checkout and builder worktrees are READ ONLY)"; exit 2;; esac
  [ -d "$_l/$SVC" ] || { echo "REFUSING: $_l has no $SVC (WS is the REPO ROOT of your worktree)"; exit 2; }
  _h="$(git -C "$_l" rev-parse HEAD 2> /dev/null)"
  [ -n "$2" ] && [ "$_h" = "$2" ] || { echo "REFUSING: WS HEAD is '$_h', this side needs '$2' (set GD2_HEAD for head-side modes)"; exit 2; }
  WSR="$_l"; TS="$_l/$SVC"
}
clean_or_fail() {
  git -C "$WSR" status --porcelain > "$OUTR/$1.status.out" 2> "$OUTR/$1.status.err"; _rc=$?
  _n="$(wc -l < "$OUTR/$1.status.out" | tr -d ' ')"
  echo "  worktree status after $1: rc $_rc, $_n dirty path(s) (want 0)"
  [ "$_rc" = 0 ] && [ "$_n" = 0 ]
}
quarantine() { mkdir -p "$OUTR/quarantine" && mv "$WSR/$1" "$OUTR/quarantine/$2.$(date -u +%H%M%S).$(basename "$1")" && echo "  quarantined $1 -> $OUTR/quarantine/"; }
vitest() {  # vitest <name> <json> [file...] : in services/timestamping, in a subshell
  _name="$1"; _json="$2"; shift 2
  ( cd "$TS" && npx vitest run "$@" --reporter=default --reporter=json --outputFile="$_json" ) > "$OUTR/$_name.out" 2> "$OUTR/$_name.err"; _rc=$?
  echo "$_rc" > "$OUTR/$_name.rc"; echo "  $_name rc=$_rc ($(date -u +%H:%M:%SZ)) -> $(basename "$_json")"
  return 0
}
judge() { _name="$1"; shift; python3 "$PARSE" "$@" > "$OUTR/$_name.out" 2> "$OUTR/$_name.err"; _rc=$?; echo "$_rc" > "$OUTR/$_name.rc"; sed 's/^/    /' "$OUTR/$_name.out" | cut -c1-240; return $_rc; }
sha() { shasum -a 256 "$1" | awk '{print $1}'; }

CMD="${1:-}"
case "$CMD" in
  ''|-h|--help) usage; [ -n "$CMD" ] && exit 0; exit 2;;
  plan)
    H="${GD2_HEAD:-$(KJ drafted_first_commit)}"
    echo "C3 PLAN $(date -u +%Y-%m-%dT%H:%M:%SZ) | checkout $CHECKOUT (READ ONLY) | base $BASE | head $H$([ -z "${GD2_HEAD:-}" ] && echo ' (GD2_HEAD unset: the drafted FIRST commit)')"
    BAD=0
    for P in "$TESTF" "$PKIF" "$SVC/src/tsa/rfc3161-verify.ts" "$SVC/src/tsa/der.ts"; do
      git -C "$CHECKOUT" cat-file -e "$H:$P" 2> /dev/null; a=$?; git -C "$CHECKOUT" cat-file -e "$BASE:$P" 2> /dev/null; b=$?
      echo "  $P: head cat-file rc $a (want 0) | base rc $b (want non-zero: NEW)"; [ $a = 0 ] && [ $b != 0 ] || BAD=1
    done
    git -C "$CHECKOUT" show "$H:$TESTF" > "/private/tmp/claude-501/.gd2_c3plan_$$.ts" 2>&1
    python3 - "/private/tmp/claude-501/.gd2_c3plan_$$.ts" "$(KJ cell_rx)" <<'PY'
import re, sys
t = open(sys.argv[1]).read(); rx = re.compile(sys.argv[2])
its = re.findall(r"^\s*it\(\s*'([^']+)'", t, re.M); each = re.findall(r"^\s*\['(\w+)',\s+'", t, re.M)
print('  it( titles: %d | it.each rows: %d %s | total cells expected 25' % (len(its), len(each), each))
print('  doMock targets %s | vi.mock( module mocks %s | stubGlobal fetch %d | real TSA URL literal in code %d' % (re.findall(r"vi\.doMock\('([^']+)'", t), re.findall(r"vi\.mock\('([^']+)'", t), t.count("stubGlobal('fetch'"), len(re.findall(r"https?://(?!tsa\.example\.test)[a-z0-9.-]+\.(?:net|com|de)", t))))
PY
    mv "/private/tmp/claude-501/.gd2_c3plan_$$.ts" "/private/tmp/claude-501/.gd2_c3plan_last.ts"
    echo "  tsconfig exclude: $(git -C "$CHECKOUT" show "$H:$SVC/tsconfig.json" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("exclude"))')"
    echo "  RUN PLAN: pki OUT | install WS_BASE OUT; run base WS_BASE OUT; tsc base WS_BASE OUT; probe base WS_BASE OUT | install WS_HEAD OUT; run head WS_HEAD OUT; tsc head WS_HEAD OUT; mutate WS_HEAD OUT; probe head WS_HEAD OUT"
    echo "C3 PLAN $([ $BAD = 0 ] && echo OK || echo FAIL)"; exit $BAD;;
  parse-selftest) python3 "$PARSE" --selftest; exit $?;;
  pki) guard_out "${2:?OUT}"; bash "$GS/probe_pki_gateD2.sh" "$OUTR/pki"; exit $?;;
  install)
    WS="${2:-}"; O="${3:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    _h="$(git -C "$WS" rev-parse HEAD 2> /dev/null)"; guard_ws "$WS" "$_h"; guard_out "$O"
    [ "$_h" = "$BASE" ] || [ "$_h" = "$HEADSHA" ] || { echo "REFUSING: WS HEAD $_h is neither the base nor GD2_HEAD"; exit 2; }
    T="install_${_h:0:12}"
    ( cd "$WSR/Blockchain/Dev" && npm ci --ignore-scripts ) > "$OUTR/$T.npmci.out" 2> "$OUTR/$T.npmci.err"; rc=$?; echo "$rc" > "$OUTR/$T.npmci.rc"; echo "  npm ci --ignore-scripts rc=$rc"
    [ "$rc" = 0 ] || exit 3
    ( cd "$WSR/Blockchain/Dev" && npm run build --workspace=packages/shared ) > "$OUTR/$T.shared.out" 2> "$OUTR/$T.shared.err"; rc=$?; echo "$rc" > "$OUTR/$T.shared.rc"; echo "  build packages/shared rc=$rc"
    [ "$rc" = 0 ] || exit 3
    for m in pkijs asn1js node-forge; do echo "  node_modules/$m at Blockchain/Dev: $([ -d "$WSR/Blockchain/Dev/node_modules/$m" ] && echo PRESENT || echo absent)"; done
    clean_or_fail "$T" || echo "  NOTE: dirty after install (name each path)"
    exit 0;;
  run)
    SIDE="${2:-}"; WS="${3:-}"; O="${4:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    if [ "$SIDE" = base ]; then guard_ws "$WS" "$BASE"; elif [ "$SIDE" = head ]; then guard_ws "$WS" "$HEADSHA"; else usage; exit 2; fi
    guard_out "$O"
    if [ "$SIDE" = base ]; then
      echo "C3 RUN BASE $(date -u +%Y-%m-%dT%H:%M:%SZ) | WS $WSR @ $BASE | head source of the plant ${HEADSHA:-UNSET} | OUT $OUTR"
      [ -n "$HEADSHA" ] || { echo "REFUSING: GD2_HEAD unset — the plant is the HEAD's test file"; exit 2; }
      [ -e "$WSR/$TESTF" ] && { echo "REFUSING: the KS 1404 test already exists in the base WS (a stale plant?)"; exit 2; }
      vitest base_suite "$OUTR/base_suite.json"
      judge base_suite.judge suite "$OUTR/base_suite.json" --console "$OUTR/base_suite.out" --expect-files "$(KJ suite_claim | python3 -c 'import json,sys; print(json.load(sys.stdin)["base_files"])')" --expect-tests "$(KJ suite_claim | python3 -c 'import json,sys; print(json.load(sys.stdin)["base_tests"])')"; r1=$?
      for P in "$TESTF" "$PKIF"; do
        git -C "$WSR" show "$HEADSHA:$P" > "$WSR/$P" 2> "$OUTR/plant.err"; rc=$?
        echo "  planted $(basename "$P") from the head: rc $rc sha256 $(sha "$WSR/$P" | cut -c1-16)"; [ "$rc" = 0 ] || exit 3
      done
      vitest base_cells "$OUTR/base_cells.json" "src/__tests__/$(basename "$TESTF")"
      judge base_cells.judge cells "$OUTR/base_cells.json" base --console "$OUTR/base_cells.out"; r2=$?
      quarantine "$TESTF" base-plant; quarantine "$PKIF" base-plant; clean_or_fail base_after; r3=$?
      [ "$r1" = 0 ] && [ "$r2" = 0 ] && [ "$r3" = 0 ] && { echo "C3 BASE PASS (suite pristine as claimed; the red set red by assertion)"; exit 0; }
      echo "C3 BASE FAIL (suite judge rc $r1, cells judge rc $r2, clean rc $r3) — a count that differs from the builder's is a FINDING, not a tool error"; exit 1
    fi
    echo "C3 RUN HEAD $(date -u +%Y-%m-%dT%H:%M:%SZ) | WS $WSR @ $HEADSHA | OUT $OUTR"
    vitest head_cells "$OUTR/head_cells.json" "src/__tests__/$(basename "$TESTF")"
    judge head_cells.judge cells "$OUTR/head_cells.json" head --console "$OUTR/head_cells.out"; r1=$?
    vitest head_suite "$OUTR/head_suite.json"
    judge head_suite.judge suite "$OUTR/head_suite.json" --console "$OUTR/head_suite.out" --expect-files "$(KJ suite_claim | python3 -c 'import json,sys; print(json.load(sys.stdin)["head_files"])')" --expect-tests "$(KJ suite_claim | python3 -c 'import json,sys; print(json.load(sys.stdin)["head_tests"])')" --expect-fail 0; r2=$?
    if [ -s "$OUTR/base_suite.json" ]; then judge suites.diff diff-suites "$OUTR/base_suite.json" "$OUTR/head_suite.json"; r3=$?; else echo "  NOTE: no base_suite.json in OUT — run 'run base' first"; r3=1; fi
    clean_or_fail head_after; r4=$?
    [ "$r1" = 0 ] && [ "$r2" = 0 ] && [ "$r3" = 0 ] && [ "$r4" = 0 ] && { echo "C3 HEAD PASS (25/25 green, 0 skipped; suite as claimed, 0 failed; +1 file +25, 0 regressions)"; exit 0; }
    echo "C3 HEAD FAIL (cells $r1, suite $r2, diff $r3, clean $r4)"; exit 1;;
  tsc)
    SIDE="${2:-}"; WS="${3:-}"; O="${4:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    if [ "$SIDE" = base ]; then guard_ws "$WS" "$BASE"; elif [ "$SIDE" = head ]; then guard_ws "$WS" "$HEADSHA"; else usage; exit 2; fi
    guard_out "$O"; TSC="$WSR/Blockchain/Dev/node_modules/.bin/tsc"
    [ -x "$TSC" ] || { echo "REFUSING: the named binary $TSC is absent (install first; never npx tsc, which can run npm's placeholder package)"; exit 3; }
    "$TSC" --version > "$OUTR/tsc_${SIDE}_version.out" 2>&1
    "$TSC" --noEmit -p "$TS" > "$OUTR/tsc_$SIDE.out" 2> "$OUTR/tsc_$SIDE.err"; rc=$?; echo "$rc" > "$OUTR/tsc_$SIDE.rc"
    n="$(grep -c 'error TS' "$OUTR/tsc_$SIDE.out")"
    printf '%s\n' "const x: number = 'a';" "export { x };" > "$OUTR/tsc_control_$SIDE.ts"
    "$TSC" --noEmit --strict "$OUTR/tsc_control_$SIDE.ts" > "$OUTR/tsc_control_$SIDE.out" 2> "$OUTR/tsc_control_$SIDE.err"; crc=$?; echo "$crc" > "$OUTR/tsc_control_$SIDE.rc"
    cn="$(grep -c 'TS2322' "$OUTR/tsc_control_$SIDE.out")"
    echo "TSC $SIDE $(cat "$OUTR/tsc_${SIDE}_version.out") rc=$rc errors=$n | POSITIVE CONTROL rc=$crc TS2322=$cn (want 2 / >=1) ($(date -u +%H:%M:%SZ)) — tsconfig excludes src/__tests__: no-regression reading of the product only"
    [ "$rc" = 0 ] && [ "$crc" = 2 ] && [ "$cn" -ge 1 ] && exit 0; exit 1;;
  mutate)
    WS="${2:-}"; O="${3:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    guard_ws "$WS" "$HEADSHA"; guard_out "$O"; echo "C3 MUTATE $(date -u +%Y-%m-%dT%H:%M:%SZ) | WS $WSR @ $HEADSHA"
    clean_or_fail mut_before || { echo "REFUSING: the head WS is dirty before the mutation"; exit 2; }
    rr=0
    for arm in sig indef imprint chain anchors eku md validity mockpath; do
      if [ "$arm" = mockpath ]; then P="$SVC/src/tsa/qualified-tsa.ts"; else P="$SVC/src/tsa/rfc3161-verify.ts"; fi
      s0="$(sha "$WSR/$P")"
      python3 "$MUT" plant "$arm" "$TS" > "$OUTR/mut_$arm.plant.out" 2> "$OUTR/mut_$arm.plant.err"; rc=$?; echo "  arm $arm planted rc $rc"
      if [ "$rc" = 0 ]; then
        vitest "mut_$arm" "$OUTR/mut_$arm.json" "src/__tests__/$(basename "$TESTF")"
        judge "mut_$arm.judge" mutation "$OUTR/mut_$arm.json" "$arm"; r=$?; [ "$r" = 0 ] || rr=1
      else rr=1; fi
      git -C "$WSR" show "$HEADSHA:$P" > "$WSR/$P" 2> "$OUTR/mut_$arm.restore.err"; rc=$?
      s1="$(sha "$WSR/$P")"; echo "  arm $arm restored rc $rc: sha256 equal $([ "$s0" = "$s1" ] && echo yes || echo NO)"; [ "$s0" = "$s1" ] || rr=1
    done
    clean_or_fail mut_after || rr=1
    [ "$rr" = 0 ] && { echo "C3 MUTATION PASS (8 guard lines each turn their cell red and nothing else; mockpath REPORTED)"; exit 0; }
    echo "C3 MUTATION FAIL"; exit 1;;
  probe)
    SIDE="${2:-}"; WS="${3:-}"; O="${4:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    if [ "$SIDE" = base ]; then guard_ws "$WS" "$BASE"; elif [ "$SIDE" = head ]; then guard_ws "$WS" "$HEADSHA"; else usage; exit 2; fi
    guard_out "$O"; r=0
    if [ "$SIDE" = head ]; then
      [ -s "$OUTR/pki/rootA.pem" ] || { echo "REFUSING: no PKI at $OUTR/pki — run '$0 pki $OUTR' first"; exit 2; }
      PF="$SVC/src/__tests__/zz-gD2-probe-forgery.test.ts"; [ -e "$WSR/$PF" ] && { echo "REFUSING: a probe already sits in the WS"; exit 2; }
      cp "$GS/probe_ks1404_forgery.test.ts.txt" "$WSR/$PF" || exit 3
      echo "C3 FORGERY PROBE head $(date -u +%Y-%m-%dT%H:%M:%SZ) | probe sha256 $(sha "$WSR/$PF" | cut -c1-16) | PKI $OUTR/pki"
      ( export GD2_PKI="$OUTR/pki"; cd "$TS" && npx vitest run "src/__tests__/zz-gD2-probe-forgery.test.ts" --reporter=default --reporter=json --outputFile="$OUTR/probe_forgery.json" ) > "$OUTR/probe_forgery.out" 2> "$OUTR/probe_forgery.err"; echo "$?" > "$OUTR/probe_forgery.rc"
      judge probe_forgery.judge probe-forgery "$OUTR/probe_forgery.json" --console "$OUTR/probe_forgery.out" || r=1
      quarantine "$PF" probe-head
    fi
    PM="$SVC/src/__tests__/zz-gD2-probe-mock.test.ts"; [ -e "$WSR/$PM" ] && { echo "REFUSING: a probe already sits in the WS"; exit 2; }
    cp "$GS/probe_ks1404_mock.test.ts.txt" "$WSR/$PM" || exit 3
    ( export GD2_SIDE="$SIDE"; cd "$TS" && npx vitest run "src/__tests__/zz-gD2-probe-mock.test.ts" --reporter=default --reporter=json --outputFile="$OUTR/probe_mock_$SIDE.json" ) > "$OUTR/probe_mock_$SIDE.out" 2> "$OUTR/probe_mock_$SIDE.err"; echo "$?" > "$OUTR/probe_mock_$SIDE.rc"
    judge "probe_mock_$SIDE.judge" probe-mock "$OUTR/probe_mock_$SIDE.json" "$SIDE" || r=1
    quarantine "$PM" "probe-$SIDE"
    PR_="$SVC/src/__tests__/zz-gD2-probe-reqbytes.test.ts"; cp "$GS/probe_ks1404_reqbytes.test.ts.txt" "$WSR/$PR_" || exit 3
    ( export GD2_REQ_OUT="$OUTR/reqbytes_$SIDE.json"; cd "$TS" && npx vitest run "src/__tests__/zz-gD2-probe-reqbytes.test.ts" ) > "$OUTR/probe_reqbytes_$SIDE.out" 2> "$OUTR/probe_reqbytes_$SIDE.err"; rq=$?; echo "$rq" > "$OUTR/probe_reqbytes_$SIDE.rc"
    echo "  request-bytes probe $SIDE rc $rq -> reqbytes_$SIDE.json"; [ "$rq" = 0 ] || r=1
    quarantine "$PR_" "probe-$SIDE"
    if [ "$SIDE" = head ]; then
      if [ -s "$OUTR/reqbytes_base.json" ]; then python3 "$GS/c3_reqbytes_gateD2.py" "$OUTR/reqbytes_base.json" "$OUTR/reqbytes_head.json" > "$OUTR/reqbytes_compare.out" 2> "$OUTR/reqbytes_compare.err"; rc=$?; echo "$rc" > "$OUTR/reqbytes_compare.rc"; sed 's/^/    /' "$OUTR/reqbytes_compare.out"; [ "$rc" = 0 ] || r=1
      else echo "  NOTE: no reqbytes_base.json in OUT — run 'probe base' first (the differential needs the forge side)"; r=1; fi
    fi
    clean_or_fail "probe_${SIDE}_after" || r=1
    [ "$r" = 0 ] && { echo "C3 PROBE $SIDE PASS"; exit 0; }
    echo "C3 PROBE $SIDE FAIL (read the judges)"; exit 1;;
  *) usage; exit 2;;
esac

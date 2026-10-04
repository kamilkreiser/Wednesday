#!/bin/bash
# c3_cells_gate55.sh — gate55 C3: the KS-1015 cells, the transfer suite before/after, and tsc (base == head, named binary, positive control).
# bash 3.2 / zsh safe; NO rc is read through a pipe (every command: `cmd > out 2> err; rc=$?`, the rc written to its own .rc file).
# WS = the REPO ROOT of a checkout YOU made in YOUR scratch (a by-SHA worktree of your clone); OUT = your evidence dir. Both guarded by
# guards_gate55.sh BEFORE any write (WS outside /Volumes/DevMASTER/!CODING/, clean, HEAD^{tree} == the side's kit tree; OUT lexical-first).
#   parse-selftest          c3_parse_gate55.py --selftest (14 arms).
#   install WS OUT          `npm ci --ignore-scripts` at Blockchain/Dev, then `npm run build --workspace=packages/shared` (X1). Either side.
#   run base WS OUT         WS at base: (1) the FULL transfer suite pristine -> base_suite.json (builder 4 files / 70 tests); (2) PLANT the
#                           head's ks1015 test (its blob, kit drafted_head_blobs) into the base WS, run it alone -> base_cells.json: D1-D3 RED,
#                           each an AssertionError, 0 load-failure markers; C1-C3 GREEN; (3) QUARANTINE the plant into OUT (never rm); clean.
#   run head WS OUT         WS at head: the ks1015 file alone -> 6/6 GREEN; the FULL suite -> 5 / 76, 0 failed; diff vs OUT/base_suite.json:
#                           +1 file, +6 tests that are exactly the cells, 0 NEW REDS.
#   tsc base|head WS OUT    the NAMED binary (Blockchain/Dev/node_modules/.bin/tsc, realpath + --version printed) `--noEmit -p .` in
#                           services/transfer: rc and `error TS` count; then `--listFilesOnly`: program size, files under __tests__ (the
#                           tsconfig excludes src/__tests__, so tsc base == head is a NO-REGRESSION reading of product code only).
#   tsc-control WS OUT      POSITIVE CONTROL at head: one type error appended to kit tsc_control_file (a non-excluded product file) -> tsc
#                           rc != 0 and >= 1 `error TS` naming that file; restored from its blob, sha256 proven, worktree clean.
# rc: 0 PASS / 1 FAIL / 2 refusal or usage / 3 a tool step failed.
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
. "$GS/guards_gate55.sh"
PARSE="$GS/c3_parse_gate55.py"; TESTF="$(KJ test_file)"; TESTB="$(KB drafted_head_blobs "$(KJ test_file)")"
SC() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["suite_claim"][sys.argv[2]])' "$GS/kit.json" "$1"; }
usage() { sed -n '2,24p' "$0" | sed 's/^# \{0,1\}//'; }
vitest() {  # vitest <name> <json> [file] — a subshell cd into services/transfer, never the caller's shell
  _name="$1"; _json="$2"; shift 2
  ( cd "$TRANSFER" && npx vitest run "$@" --reporter=default --reporter=json --outputFile="$_json" ) > "$OUTR/$_name.out" 2> "$OUTR/$_name.err"; _rc=$?
  echo "$_rc" > "$OUTR/$_name.rc"; echo "  $_name rc=$_rc ($(date -u +%H:%M:%SZ)) -> $(basename "$_json")"
}
judge() {  # judge <name> <parse args...>
  _name="$1"; shift
  python3 "$PARSE" "$@" > "$OUTR/$_name.out" 2> "$OUTR/$_name.err"; _rc=$?
  echo "$_rc" > "$OUTR/$_name.rc"; sed 's/^/    /' "$OUTR/$_name.out" | cut -c1-240
  return $_rc
}
tsc_bin() {
  TSC="$DEV/node_modules/.bin/tsc"
  [ -x "$TSC" ] || { echo "REFUSING: no tsc at $TSC (install first)"; exit 3; }
  echo "  tsc binary $TSC -> $(/bin/realpath "$TSC") | $("$TSC" --version 2>&1)"
}
CMD="${1:-}"
case "$CMD" in
  ''|-h|--help) usage; [ -n "$CMD" ] && exit 0; exit 2;;
  parse-selftest) python3 "$PARSE" --selftest; exit $?;;
  install)
    WS="${2:-}"; O="${3:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    _t="$(git -C "$WS" rev-parse 'HEAD^{tree}' 2> /dev/null)"; if [ "$_t" = "$(KJ base_tree)" ]; then SIDE=base; else SIDE=head; fi
    guard_ws "$WS" "$SIDE"; guard_out "$O"; T="install_$SIDE"
    ( cd "$DEV" && npm ci --ignore-scripts ) > "$OUTR/$T.npmci.out" 2> "$OUTR/$T.npmci.err"; rc=$?; echo "$rc" > "$OUTR/$T.npmci.rc"; echo "  npm ci --ignore-scripts rc=$rc ($(grep -o 'added [0-9]* packages[^,]*' "$OUTR/$T.npmci.out" | head -1))"
    [ "$rc" = 0 ] || exit 3
    ( cd "$DEV" && npm run build --workspace=packages/shared ) > "$OUTR/$T.shared.out" 2> "$OUTR/$T.shared.err"; rc=$?; echo "$rc" > "$OUTR/$T.shared.rc"; echo "  build packages/shared rc=$rc"
    [ "$rc" = 0 ] || exit 3
    clean_or_fail "$T" || { echo "  NOTE: dirty after install — name each path (node_modules / dist should be gitignored)"; exit 1; }
    exit 0;;
  run)
    SIDE="${2:-}"; WS="${3:-}"; O="${4:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    case "$SIDE" in base|head) ;; *) usage; exit 2;; esac
    guard_ws "$WS" "$SIDE"; guard_out "$O"
    if [ "$SIDE" = base ]; then
      echo "C3 RUN BASE $(date -u +%Y-%m-%dT%H:%M:%SZ) | OUT $OUTR"
      [ -e "$WSR/$TESTF" ] && { echo "REFUSING: the ks1015 test already exists in the base WS"; exit 2; }
      vitest base_suite "$OUTR/base_suite.json"
      judge base_suite.judge suite "$OUTR/base_suite.json" --console "$OUTR/base_suite.out" --expect-files "$(SC base_files)" --expect-tests "$(SC base_tests)" --expect-fail 0; r1=$?
      put_blob "$TESTB" "$TESTF"; rc=$?
      echo "  planted the head's test blob ${TESTB:0:12} into the base WS: rc $rc, sha256 $(sha "$WSR/$TESTF" | cut -c1-16)"
      [ "$rc" = 0 ] || exit 3
      vitest base_cells "$OUTR/base_cells.json" "src/__tests__/$(basename "$TESTF")"
      judge base_cells.judge cells "$OUTR/base_cells.json" base --console "$OUTR/base_cells.out"; r2=$?
      quarantine "$TESTF" base-plant; clean_or_fail base_after; r3=$?
      [ "$r1" = 0 ] && [ "$r2" = 0 ] && [ "$r3" = 0 ] && { echo "C3 BASE PASS (suite $(SC base_files)/$(SC base_tests) pristine; D1-D3 red by AssertionError, C1-C3 green)"; exit 0; }
      echo "C3 BASE FAIL (suite judge rc $r1, cells judge rc $r2, clean rc $r3) — a count that differs from the builder's is a FINDING, not a tool error"; exit 1
    fi
    echo "C3 RUN HEAD $(date -u +%Y-%m-%dT%H:%M:%SZ) | OUT $OUTR"
    vitest head_cells "$OUTR/head_cells.json" "src/__tests__/$(basename "$TESTF")"
    judge head_cells.judge cells "$OUTR/head_cells.json" head --console "$OUTR/head_cells.out"; r1=$?
    vitest head_suite "$OUTR/head_suite.json"
    judge head_suite.judge suite "$OUTR/head_suite.json" --console "$OUTR/head_suite.out" --expect-files "$(SC head_files)" --expect-tests "$(SC head_tests)" --expect-fail 0; r2=$?
    if [ -s "$OUTR/base_suite.json" ]; then judge suites.diff diff-suites "$OUTR/base_suite.json" "$OUTR/head_suite.json"; r3=$?; else echo "  NO base_suite.json in OUT — run 'run base' into the same OUT first"; r3=1; fi
    clean_or_fail head_after; r4=$?
    [ "$r1" = 0 ] && [ "$r2" = 0 ] && [ "$r3" = 0 ] && [ "$r4" = 0 ] && { echo "C3 HEAD PASS (6/6 green; $(SC head_files)/$(SC head_tests), 0 failed; +1 file +6 tests = the cells, 0 NEW REDS)"; exit 0; }
    echo "C3 HEAD FAIL (cells $r1, suite $r2, diff $r3, clean $r4)"; exit 1;;
  tsc)
    SIDE="${2:-}"; WS="${3:-}"; O="${4:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    case "$SIDE" in base|head) ;; *) usage; exit 2;; esac
    guard_ws "$WS" "$SIDE"; guard_out "$O"; tsc_bin
    ( cd "$TRANSFER" && "$TSC" --noEmit -p . ) > "$OUTR/tsc_$SIDE.out" 2> "$OUTR/tsc_$SIDE.err"; rc=$?; echo "$rc" > "$OUTR/tsc_$SIDE.rc"
    n="$(grep -c 'error TS' "$OUTR/tsc_$SIDE.out")"
    ( cd "$TRANSFER" && "$TSC" --noEmit -p . --listFilesOnly ) > "$OUTR/tsc_${SIDE}_files.out" 2> "$OUTR/tsc_${SIDE}_files.err"; rl=$?
    nf="$(wc -l < "$OUTR/tsc_${SIDE}_files.out" | tr -d ' ')"; nt="$(grep -c '/__tests__/' "$OUTR/tsc_${SIDE}_files.out")"; nk="$(grep -c "$(basename "$TESTF")" "$OUTR/tsc_${SIDE}_files.out")"
    nsrc="$(grep -c '/services/transfer/src/' "$OUTR/tsc_${SIDE}_files.out")"
    echo "TSC $SIDE rc=$rc errors=$n | --listFilesOnly rc=$rl: $nf files, $nsrc under services/transfer/src (MUST-HIT, want > 0), $nt under __tests__, ks1015 test $nk ($(date -u +%H:%M:%SZ))"
    echo "  compare base vs head yourself: equal rc AND equal count is a NO-REGRESSION reading of PRODUCT code only (the test file is excluded)"
    [ "$nsrc" -gt 0 ] || { echo "  FAIL: the program lists 0 transfer src files — the instrument is not reading this project"; exit 1; }
    exit 0;;
  tsc-control)
    WS="${2:-}"; O="${3:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    guard_ws "$WS" head; guard_out "$O"; tsc_bin
    P="$(KJ tsc_control_file)"; B="$(git -C "$WSR" rev-parse "HEAD:$P")"; s0="$(sha "$WSR/$P")"
    printf '\nconst __g55TscControl: number = "a string is not a number";\n' >> "$WSR/$P"
    ( cd "$TRANSFER" && "$TSC" --noEmit -p . ) > "$OUTR/tsc_control.out" 2> "$OUTR/tsc_control.err"; rc=$?; echo "$rc" > "$OUTR/tsc_control.rc"
    n="$(grep -c 'error TS' "$OUTR/tsc_control.out")"; nf="$(grep 'error TS' "$OUTR/tsc_control.out" | grep -c "$(basename "$P")")"
    put_blob "$B" "$P"; s1="$(sha "$WSR/$P")"
    echo "TSC CONTROL: one planted type error in $P -> rc=$rc errors=$n naming $(basename "$P"): $nf | restored from blob ${B:0:12}: sha256 equal $([ "$s0" = "$s1" ] && echo yes || echo NO)"
    clean_or_fail tsc_control_after; rcl=$?
    [ "$rc" != 0 ] && [ "$nf" -ge 1 ] && [ "$s0" = "$s1" ] && [ "$rcl" = 0 ] && { echo "TSC CONTROL PASS (the binary type-checks this project and can fail)"; exit 0; }
    echo "TSC CONTROL FAIL"; exit 1;;
  *) usage; exit 2;;
esac

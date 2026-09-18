#!/bin/bash
# checker_tsc_types_by_runner_arms.sh — red-proof for the code_patch checker's standalone test-file tsc (the INFO line
# after A7) picking its --types list from the service's OWN test runner (2026-09-18; IMPROVEMENTS 15:53 OWED row:
# checker.sh:921 ran `--types node,vitest/globals` for every service, so a jest service got TS2708 on every jest.mock).
#
# Nothing is re-implemented: each arm CUTS the checker's own text out of the file and runs it.
#   NEW block = checker lines from `# BEGIN tsc_test_types` through the `echo "INFO tsc on the test file alone` line.
#   OLD block = the old checker's `( cd "$SVC" && npx tsc --noEmit --strict ...` line through its INFO echo.
#
#   A1  originate (jest), ks1213 reference test: NEW picks node,jest, rc 0, 0 TS2708
#   A1c negative control: OLD on the same file -> >0 TS2708 (the TS2708 count can fail)
#   A2  api-gateway (vitest), auth.test.ts: NEW picks node,vitest/globals, rc and tsc output byte-identical to OLD
#   A2c negative control: the identity cmp reports DIFFERENT on originate NEW vs OLD, and originate's NEW log does not
#       name vitest/globals (api-gateway tests import vitest explicitly, so --types cannot change their output)
#   A3  scratch fixture, neither marker: NEW prints the "could not tell" line and runs --types node,vitest/globals,
#       rc and output identical to OLD
#   A3b scratch fixture, BOTH markers (the referral/vc-issuer shape: vitest config + script, leftover jest deps):
#       "could not tell" line, same fallback
#   A3c negative control: OLD prints no "could not tell" line; NEW on originate prints none either
#   A0  NEW checker parses (bash -n); every byte outside the replaced block is identical to OLD
#
# Usage: bash checker_tsc_types_by_runner_arms.sh [NEW_CHECKER] [OLD_CHECKER]
#   defaults: tasks/code_patch/checker.sh and the newest tasks/code_patch/checker.sh.pre-*-jesttypes
#   env: ARMS_CLONE (a night clone whose Blockchain/Dev has node_modules and services/originate/node_modules;
#        default /private/tmp/claude-501/night/clone_ks1228), ARMS_SCRATCH.
# rc 0 only when every arm holds. Every rc is read on its own line, never through a pipe. No rm: a previous scratch
# dir is MOVED aside.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CP="$HERE/../tasks/code_patch"
NEW="${1:-$CP/checker.sh}"
OLD="${2:-$(ls -t "$CP"/checker.sh.pre-*-jesttypes 2>/dev/null | head -1)}"
CLONE="${ARMS_CLONE:-/private/tmp/claude-501/night/clone_ks1228}"
DEV="$CLONE/Blockchain/Dev"
S="${ARMS_SCRATCH:-/private/tmp/claude-501/night/tsctypes_arms}"
[ -e "$S" ] && mv "$S" "$S.prev.$(date +%H%M%S)"
mkdir -p "$S"
P=0; F=0
ok()  { P=$((P+1)); echo "PASS $*"; }
bad() { F=$((F+1)); echo "FAIL $*"; }
echo "NEW=$NEW"; echo "OLD=$OLD"; echo "CLONE=$CLONE ($(git -C "$CLONE" rev-parse --short HEAD 2>/dev/null))"
[ -f "$NEW" ] && [ -f "$OLD" ] && [ -d "$DEV/node_modules" ] || { echo "setup: missing checker or clone"; exit 2; }

sed -n '/^# BEGIN tsc_test_types/,/^echo "INFO tsc on the test file alone/p' "$NEW" > "$S/new_block.sh"
sed -n '/^( cd "\$SVC" && npx tsc --noEmit --strict .*--types node,vitest\/globals/,/^echo "INFO tsc on the test file alone/p' "$OLD" > "$S/old_block.sh"
nb=$(wc -l < "$S/new_block.sh" | tr -d ' '); ob=$(wc -l < "$S/old_block.sh" | tr -d ' ')
echo "cut: new block $nb lines, old block $ob lines"
[ "$nb" -ge 10 ] && [ "$ob" -eq 3 ] || { echo "setup: could not cut the blocks"; exit 2; }

# run_block <new|old> <label> <svc_dir> <test_rel> <service>  -> $S/<label>.log (stdout), $S/<label>/after_tsc_testfile.out
run_block() {
  local which="$1" label="$2"
  mkdir -p "$S/$label"
  SVC="$3" TEST_REL="$4" SERVICE="$5" REP="$S/$label" bash "$S/${which}_block.sh" > "$S/$label.log" 2>&1
}
cnt() { /usr/bin/grep -c "$1" "$2"; }

# ---------------------------------------------------------------- A0
bash -n "$NEW"
rc=$?
[ "$rc" -eq 0 ] && ok "A0 NEW checker parses" || bad "A0 NEW checker bash -n rc=$rc"
sed '/^# Informational: the test file is excluded from the service tsconfig/,/^echo "INFO tsc on the test file alone/d' "$NEW" > "$S/new_rest"
sed '/^# Informational: the test file is excluded from the service tsconfig/,/^echo "INFO tsc on the test file alone/d' "$OLD" > "$S/old_rest"
cmp -s "$S/new_rest" "$S/old_rest"
rc=$?
[ "$rc" -eq 0 ] && ok "A0 every line outside the replaced block identical ($(wc -l < "$S/new_rest" | tr -d ' ') lines)" || bad "A0 lines outside the block differ (cmp rc=$rc)"

# ---------------------------------------------------------------- A1 originate / jest
ORIG="$DEV/services/originate"; T1="src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts"
[ -f "$ORIG/$T1" ] || { echo "setup: $T1 absent in the clone"; exit 2; }
run_block new a1_new "$ORIG" "$T1" originate
n_new=$(cnt TS2708 "$S/a1_new/after_tsc_testfile.out")
run_block old a1_old "$ORIG" "$T1" originate
n_old=$(cnt TS2708 "$S/a1_old/after_tsc_testfile.out")
echo "A1 new: $(tail -1 "$S/a1_new.log")"; echo "A1 old: $(tail -1 "$S/a1_old.log")"
if /usr/bin/grep -q -- '--types node,jest): rc=0 ' "$S/a1_new.log" && [ "$n_new" -eq 0 ]; then
  ok "A1 NEW on originate ks1213: --types node,jest, rc 0, TS2708=$n_new"
else bad "A1 NEW on originate ks1213: TS2708=$n_new, log: $(tail -1 "$S/a1_new.log")"; fi
if [ "$n_old" -gt 0 ]; then ok "A1c control: OLD on the same file TS2708=$n_old (>0)"; else bad "A1c control: OLD TS2708=$n_old (the arm cannot fail)"; fi

# ---------------------------------------------------------------- A2 api-gateway / vitest
GW="$DEV/services/api-gateway"; T2="src/__tests__/auth.test.ts"
run_block new a2_new "$GW" "$T2" api-gateway
run_block old a2_old "$GW" "$T2" api-gateway
echo "A2 new: $(tail -1 "$S/a2_new.log")"; echo "A2 old: $(tail -1 "$S/a2_old.log")"
rc_n=$(sed -n 's/.*): rc=\([0-9]*\) .*/\1/p' "$S/a2_new.log"); rc_o=$(sed -n 's/.*alone: rc=\([0-9]*\) .*/\1/p' "$S/a2_old.log")
cmp -s "$S/a2_new/after_tsc_testfile.out" "$S/a2_old/after_tsc_testfile.out"
same=$?
if /usr/bin/grep -q -- '--types node,vitest/globals): rc=' "$S/a2_new.log" && [ "$same" -eq 0 ] && [ -n "$rc_n" ] && [ "$rc_n" = "$rc_o" ] \
   && ! /usr/bin/grep -q 'could not tell' "$S/a2_new.log"; then
  ok "A2 NEW on api-gateway auth.test.ts: --types node,vitest/globals, rc $rc_n = OLD rc $rc_o, output identical ($(wc -l < "$S/a2_new/after_tsc_testfile.out" | tr -d ' ') lines)"
else bad "A2 api-gateway: rc new=$rc_n old=$rc_o cmp=$same log: $(tail -1 "$S/a2_new.log")"; fi
# Control: every api-gateway test imports from 'vitest' explicitly (60/60 on 2026-09-18), so its tsc output does not
# depend on --types at all (node,jest gives the same 3 lines). The identity compare's control is therefore taken where
# the types DO matter: the same cmp on originate ks1213, NEW vs OLD, must report DIFFERENT, and the originate NEW log
# must not name vitest/globals (the A2 type-pick assertion can fail).
cmp -s "$S/a1_new/after_tsc_testfile.out" "$S/a1_old/after_tsc_testfile.out"
same_c=$?
n_vg=$(cnt 'vitest/globals' "$S/a1_new.log")
if [ "$same_c" -ne 0 ] && [ "$n_vg" -eq 0 ]; then ok "A2c control: the same cmp on originate NEW vs OLD reports DIFFERENT (cmp rc $same_c); originate NEW log names vitest/globals $n_vg times"
else bad "A2c control: originate cmp rc=$same_c, vitest/globals in its NEW log $n_vg times (the A2 assertions cannot fail)"; fi

# ---------------------------------------------------------------- A3 fixtures (neither / both)
mk_fixture() {  # mk_fixture <dir> <package.json text> [extra file]
  mkdir -p "$1/src/__tests__"
  printf '%s\n' "$2" > "$1/package.json"
  printf '%s\n' 'const x: number = 1;' 'export const y = x + 1;' > "$1/src/__tests__/plain.test.ts"
  ln -s "$DEV/node_modules" "$1/node_modules"
  [ -n "${3:-}" ] && printf '%s\n' 'export default {};' > "$1/$3"
  return 0
}
FX1="$S/fx_neither"; mk_fixture "$FX1" '{"name":"fx-neither","scripts":{"build":"tsc"},"devDependencies":{"typescript":"^5"}}'
FX2="$S/fx_both"; mk_fixture "$FX2" '{"name":"fx-both","scripts":{"test":"vitest run"},"devDependencies":{"vitest":"^4","jest":"^29","ts-jest":"^29"}}' vitest.config.ts
for fx in neither both; do
  d="$S/fx_$fx"
  run_block new a3_${fx}_new "$d" src/__tests__/plain.test.ts "fx-$fx"
  run_block old a3_${fx}_old "$d" src/__tests__/plain.test.ts "fx-$fx"
  echo "A3 $fx new: $(cat "$S/a3_${fx}_new.log" | tr '\n' '|')"
  cmp -s "$S/a3_${fx}_new/after_tsc_testfile.out" "$S/a3_${fx}_old/after_tsc_testfile.out"
  same=$?
  rc_n=$(sed -n 's/.*): rc=\([0-9]*\) .*/\1/p' "$S/a3_${fx}_new.log"); rc_o=$(sed -n 's/.*alone: rc=\([0-9]*\) .*/\1/p' "$S/a3_${fx}_old.log")
  nl=$(cnt "could not tell fx-$fx's test runner" "$S/a3_${fx}_new.log")
  if [ "$nl" -eq 1 ] && /usr/bin/grep -q -- '--types node,vitest/globals): rc=' "$S/a3_${fx}_new.log" && [ "$same" -eq 0 ] && [ -n "$rc_n" ] && [ "$rc_n" = "$rc_o" ]; then
    ok "A3 $fx markers: one 'could not tell' line, fallback node,vitest/globals, rc $rc_n = OLD, output identical"
  else bad "A3 $fx markers: tell-lines=$nl cmp=$same rc new=$rc_n old=$rc_o"; fi
done
n_old_tell=$(cnt 'could not tell' "$S/a3_neither_old.log"); n_orig_tell=$(cnt 'could not tell' "$S/a1_new.log")
if [ "$n_old_tell" -eq 0 ] && [ "$n_orig_tell" -eq 0 ]; then ok "A3c control: OLD prints no 'could not tell' line; NEW on originate prints none"
else bad "A3c control: old=$n_old_tell originate-new=$n_orig_tell"; fi

echo "ARMS: $P passed, $F failed"
[ "$F" -eq 0 ]

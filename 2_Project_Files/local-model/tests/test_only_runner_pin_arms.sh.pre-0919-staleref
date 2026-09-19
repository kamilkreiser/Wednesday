#!/bin/bash
# test_only_runner_pin_arms.sh [scratch-out-dir] — arms for the test_only builder's RUNNER PIN (2026-09-19)
#
# The defect: build_test_only_input.sh refused (rc 2, "cannot tell the runner") any service whose package.json marks
# both jest and vitest — vc-issuer (jest/ts-jest in devDependencies beside vitest), blocking KS-1269 N71-1. The fix: a
# `runner=<jest|vitest>` pin (or a `Runner:` line in the brief header), honoured only when that service's package.json
# has the named runner. Arms, negative control first:
#   (a) vc-issuer brief, NO pin  -> still rc 2 "cannot tell the runner", stderr byte-identical to the OLD builder's
#   (b) vc-issuer brief, runner=vitest (present) -> rc 0, input runner == vitest, runner_pin recorded
#   (c) api-gateway brief, runner=jest (NOT in its package.json) -> rc 2 "is NOT in"; (c2) runner=mocha -> rc 2
#   (d) api-gateway brief, no pin: NEW builder output byte-identical to the OLD builder's (and compared, INFO, to the
#       committed night/inputs/test_only_1230N74-1.json)
#   (e) the OLD builder under (b)'s exact arguments -> rc 2 (the arm discriminates: (b) passes only because of the fix)
# Writes only into the scratch-out dir (the builder's OUT). Read-only on the Secuura checkout (git show / ls-tree only).
# rc 0 only when every arm PASSes. bash 3.2. stderr never discarded (captured per arm).
set -uo pipefail
LM="$(cd "$(dirname "$0")/.." && pwd)"
NEW="$LM/tasks/test_only/build_test_only_input.sh"
OLD="$LM/tasks/test_only/build_test_only_input.sh.pre-0919-runnerpin"
B1269="$LM/night/briefs/KS-1269-N71-1.md"
B1230="$LM/night/briefs/KS-1230-N74-1.md"
COMMITTED="$LM/night/inputs/test_only_1230N74-1.json"
O="${1:-$(mktemp -d "${TMPDIR:-/tmp}/runnerpin_arms.XXXXXX")}"; mkdir -p "$O"
echo "arms out: $O"
for f in "$NEW" "$OLD" "$B1269" "$B1230" "$COMMITTED"; do [ -f "$f" ] || { echo "missing $f" >&2; exit 1; }; done
F=0
ok() { echo "PASS $1"; }
no() { echo "FAIL $1"; F=$((F+1)); }
key() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get(sys.argv[2],""))' "$1" "$2"; }

# (a) NEGATIVE CONTROL: no pin on the ambiguous service still refuses rc 2, same message as before the fix
bash "$NEW" KS-1269 "$O/a_new.json" "$B1269" ctx=65536 > "$O/a_new.out" 2> "$O/a_new.err"; rc_an=$?
bash "$OLD" KS-1269 "$O/a_old.json" "$B1269" ctx=65536 > "$O/a_old.out" 2> "$O/a_old.err"; rc_ao=$?
if [ "$rc_an" -eq 2 ] && /usr/bin/grep -q "cannot tell the runner" "$O/a_new.err" && [ ! -e "$O/a_new.json" ] && cmp -s "$O/a_new.err" "$O/a_old.err" && [ "$rc_ao" -eq 2 ]; then
  ok "(a) no pin on vc-issuer: rc $rc_an, 'cannot tell the runner', no input written, stderr byte-identical to the old builder's"
else no "(a) no pin on vc-issuer: rc new=$rc_an old=$rc_ao; $(head -c 300 "$O/a_new.err")"; fi

# (b) a pin naming a runner the service HAS builds
bash "$NEW" KS-1269 "$O/b.json" "$B1269" ctx=65536 runner=vitest > "$O/b.out" 2> "$O/b.err"; rc_b=$?
if [ "$rc_b" -eq 0 ] && [ "$(key "$O/b.json" runner)" = vitest ] && [ -n "$(key "$O/b.json" runner_pin)" ] && [ "$(key "$O/b.json" service_dir)" = services/vc-issuer ]; then
  ok "(b) runner=vitest on vc-issuer: rc 0, runner vitest, service services/vc-issuer, runner_pin recorded"
else no "(b) runner=vitest on vc-issuer: rc $rc_b; $(head -c 300 "$O/b.err")"; fi

# (c) a pin naming a runner the service does NOT have refuses; (c2) a runner name that is not jest/vitest refuses
bash "$NEW" KS-1230 "$O/c.json" "$B1230" ctx=65536 runner=jest > "$O/c.out" 2> "$O/c.err"; rc_c=$?
if [ "$rc_c" -eq 2 ] && /usr/bin/grep -q "runner pin jest (the runner= pin) is NOT in" "$O/c.err" && [ ! -e "$O/c.json" ]; then
  ok "(c) runner=jest on api-gateway (no jest in its package.json): rc 2, refused by name, no input written"
else no "(c) runner=jest on api-gateway: rc $rc_c; $(head -c 300 "$O/c.err")"; fi
bash "$NEW" KS-1269 "$O/c2.json" "$B1269" runner=mocha > "$O/c2.out" 2> "$O/c2.err"; rc_c2=$?
if [ "$rc_c2" -eq 2 ] && /usr/bin/grep -q "is not jest or vitest" "$O/c2.err" && [ ! -e "$O/c2.json" ]; then
  ok "(c2) runner=mocha: rc 2, 'is not jest or vitest'"
else no "(c2) runner=mocha: rc $rc_c2; $(head -c 300 "$O/c2.err")"; fi

# (d) an unambiguous service with no pin: new build == old build, byte for byte
bash "$NEW" KS-1230 "$O/d_new.json" "$B1230" ctx=65536 > "$O/d_new.out" 2> "$O/d_new.err"; rc_dn=$?
bash "$OLD" KS-1230 "$O/d_old.json" "$B1230" ctx=65536 > "$O/d_old.out" 2> "$O/d_old.err"; rc_do=$?
if [ "$rc_dn" -eq 0 ] && [ "$rc_do" -eq 0 ] && cmp -s "$O/d_new.json" "$O/d_old.json" && cmp -s "$O/d_new.err" "$O/d_old.err" \
   && [ "$(sed "s#$O/d_new.json#X#" "$O/d_new.out")" = "$(sed "s#$O/d_old.json#X#" "$O/d_old.out")" ]; then
  ok "(d) KS-1230 (api-gateway) no pin: new input byte-identical to the old builder's ($(shasum -a 256 < "$O/d_new.json" | cut -c1-12)), stdout/stderr identical"
else no "(d) KS-1230 no pin: rc new=$rc_dn old=$rc_do; cmp: $(cmp "$O/d_new.json" "$O/d_old.json" 2>&1 | head -1)"; fi
if cmp -s "$O/d_new.json" "$COMMITTED"; then echo "INFO (d) also byte-identical to the committed $(basename "$COMMITTED")"
else echo "INFO (d) differs from the committed $(basename "$COMMITTED") (built earlier; the old-vs-new comparison above is the gate): $(cmp "$O/d_new.json" "$COMMITTED" 2>&1 | head -1)"; fi

# (e) the OLD builder under (b)'s exact arguments refuses — (b) is green only because of the fix
bash "$OLD" KS-1269 "$O/e.json" "$B1269" ctx=65536 runner=vitest > "$O/e.out" 2> "$O/e.err"; rc_e=$?
if [ "$rc_e" -eq 2 ] && /usr/bin/grep -q "cannot tell the runner" "$O/e.err" && [ ! -e "$O/e.json" ]; then
  ok "(e) OLD builder with runner=vitest on vc-issuer: rc 2 'cannot tell the runner' — the arm discriminates"
else no "(e) OLD builder with runner=vitest: rc $rc_e (expected 2)"; fi

[ "$F" -eq 0 ] && { echo "RESULT: PASS (6/6 arms)"; exit 0; }
echo "RESULT: FAIL ($F arm(s))"; exit 1

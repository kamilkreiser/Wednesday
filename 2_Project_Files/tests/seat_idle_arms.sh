#!/bin/bash
# Arms for friday/seat_idle.sh, driven by the watcher's own pane fixtures
# (fleet/tests/fixtures/wake_watch: three REAL captures + synthetic ones built from real shapes).
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
T="$HERE/../friday/seat_idle.sh"
FX="$HERE/../fleet/tests/fixtures/wake_watch"
pass=0; fail=0
arm() { # fixture expected-rc
  local f="$1" want="$2"
  out=$(bash "$T" --file "$FX/$f" 2>&1); rc=$?
  if [ "$rc" = "$want" ]; then pass=$((pass+1)); echo "PASS $f (rc $rc) $out"; else fail=$((fail+1)); echo "FAIL $f (rc $rc, want $want) $out"; fi
}
arm real_seatA_holding_2254_dimmed.ansi        0
arm real_seatA_holding_2254_plain.txt          0
arm real_seatA_holding_live_2303.ansi          0
arm synth_idle_empty_prompt.ansi               0
arm synth_waiting_then_done_idle.ansi          0
arm synth_busy_spinner_frozen.ansi             1
arm synth_busy_shell_inflight_frozen.ansi      1
arm synth_waiting_on_subagents.ansi            4
arm synth_waiting_on_subagents_shells.ansi     4
arm synth_waiting_stuck_past_bound.ansi        4
arm synth_waiting_variant_singular_glyph.ansi  4
arm synth_waiting_variant_spacing_subagents.ansi 4
D0=$(mktemp -d); printf 'fleet monitor 09:58\n  pane %%8 ok\n' > "$D0/plain.txt"
out=$(bash "$T" --file "$D0/plain.txt" 2>&1); rc=$?
if [ "$rc" = 3 ]; then pass=$((pass+1)); echo "PASS no-turn-markers UNKNOWN (rc 3)"; else fail=$((fail+1)); echo "FAIL no-turn-markers (rc $rc) $out"; fi
# fail closed when the watcher's patterns cannot be read
D=$(mktemp -d); printf '#!/bin/bash\n# no patterns here\n' > "$D/ww.sh"
out=$(SEAT_IDLE_WAKE_WATCH="$D/ww.sh" bash "$T" --file "$FX/synth_idle_empty_prompt.ansi" 2>&1); rc=$?
if [ "$rc" = 5 ]; then pass=$((pass+1)); echo "PASS patterns-missing (rc 5)"; else fail=$((fail+1)); echo "FAIL patterns-missing (rc $rc) $out"; fi
echo "seat_idle arms: $pass PASS, $fail FAIL"
[ "$fail" -eq 0 ]

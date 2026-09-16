#!/bin/bash
# wake_watch_falsewake_arms.sh — red-proof for the two false-wake legs fixed 2026-09-16 in
# cockpit/wake_watch.sh (leg b) and the matching INPUT predicate in cockpit/monitor.sh.
#
#   A. WAITING ON SUBAGENTS — "✻ Waiting for N background agents to finish" at an empty prompt is
#      WORKING: no idle wake, no frozen-busy wake. Bounded: unchanged past the subagent-wait bound it
#      fires its OWN wake, rate-limited, ackable.
#   B. HOLDING BY DESIGN — turn ended ("Baked for 10s · done 9:59 pm · 1 monitor still running"),
#      empty prompt, only a "· 1 monitor" footer: NOT frozen-busy; routed to the idle path where the
#      IDLE-ACK hash suppresses a state already judged.
#
# HOW IT DRIVES THE REAL SCRIPTS FROM FILES, WITH NO SEAM IN THEM: each arm copies the script under
# test into a throwaway tree (so CTX_STATE, .env, chat_log and inbox_routing all resolve inside that
# tree — never the live cockpit/state) and puts three fakes first on PATH:
#   tmux  — list-panes/capture-pane answered from a panes file ("id|name|fixture"); -e returns the
#           fixture verbatim (escapes), plain capture returns it with SGR stripped — what tmux does.
#   curl  — returns an empty inbox (no network, no key).
#   sleep — counts cycles and ends the watcher (SIGTERM to its parent; its EXIT trap still cleans
#           its mktemp dir) after WW_MAX cycles, printing "NO-WAKE".
# The OLD script (.pre-0916-falsewake) runs through the identical harness as the negative control.
# Nothing here touches the fleet tmux server, the live state dir, or the mail API.
#
# Usage: wake_watch_falsewake_arms.sh
#   env: WW_OLD / WW_NEW (wake_watch scripts), MON_OLD / MON_NEW (monitor scripts),
#        WW_ARMS_TMP (work dir root; default a mktemp dir; left in place — never-delete rule).
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COCKPIT="$(cd -P "$HERE/../cockpit" && pwd)"
FIX="$HERE/fixtures/wake_watch"
WW_OLD="${WW_OLD:-$COCKPIT/wake_watch.sh.pre-0916-falsewake}"
WW_NEW="${WW_NEW:-$COCKPIT/wake_watch.sh}"
MON_OLD="${MON_OLD:-$COCKPIT/monitor.sh.pre-0916-falsewake}"
MON_NEW="${MON_NEW:-$COCKPIT/monitor.sh}"
ROOT="${WW_ARMS_TMP:-$(mktemp -d /tmp/wake_watch_falsewake_arms.XXXXXX)}"
WORK="$ROOT/run_$(date +%Y%m%d_%H%M%S)_$$"
BIN="$WORK/bin"; mkdir -p "$BIN"
PASS=0; FAIL=0

cat > "$BIN/tmux" <<'EOF'
#!/bin/bash
cmd="${1:-}"; [ $# -gt 0 ] && shift
fmt=""; tgt=""; esc=0
while [ $# -gt 0 ]; do case "$1" in
  -F) fmt="$2"; shift 2 ;; -t) tgt="$2"; shift 2 ;; -S) shift 2 ;; -e) esc=1; shift ;; *) shift ;;
esac; done
case "$cmd" in
  has-session) exit 0 ;;
  list-panes)
    while IFS='|' read -r id name fx; do
      [ -n "$id" ] || continue
      o="$fmt"
      o="${o//\#\{pane_id\}/$id}"; o="${o//\#\{@cockpit_name\}/$name}"; o="${o//\#\{pane_pid\}/99999}"
      o="${o//\#\{pane_dead\}/0}"; o="${o//\#\{pane_title\}/claude-fake-title}"; o="${o//\#\{host\}/fakehost}"
      o="${o//\#\{pane_tty\}/}"; o="${o//\#\{pane_start_command\}/}"
      printf '%s\n' "$o"
    done < "$WW_PANES" ;;
  capture-pane)
    fx=$(awk -F'|' -v t="$tgt" '$1==t{print $3; exit}' "$WW_PANES")
    [ -n "$fx" ] && [ -f "$fx" ] || exit 1
    if [ "$esc" = 1 ]; then cat "$fx"; else LC_ALL=C perl -pe 's/\x1b\[[0-9;]*m//g' "$fx"; fi ;;
  *) exit 0 ;;
esac
EOF
cat > "$BIN/curl" <<'EOF'
#!/bin/bash
echo '{"messages":[]}'
EOF
cat > "$BIN/sleep" <<'EOF'
#!/bin/bash
n=$(( $(cat "$WW_SLEEPS" 2>/dev/null || echo 0) + 1 )); echo "$n" > "$WW_SLEEPS"
if [ "$n" -ge "${WW_MAX:-10}" ]; then echo "NO-WAKE (cycle cap $n reached)"; kill -TERM "$PPID"; fi
exit 0
EOF
chmod +x "$BIN/tmux" "$BIN/curl" "$BIN/sleep"

# plain-capture hash exactly as wake_watch.sh / wake_ack.sh compute it
fixture_hash() {
  local t; t="$(LC_ALL=C perl -pe 's/\x1b\[[0-9;]*m//g' "$1" | grep -v '^$' | grep -v 'ctx:[0-9-]*%' | tail -20)"
  printf '%s' "$t" | shasum | cut -c1-12
}

# mk_tree <label> <script> <dest-name> -> prints tree cockpit dir (fresh state per arm)
mk_tree() {
  local d="$WORK/$1/tree/2_Project_Files/fleet/cockpit"
  mkdir -p "$d/state"
  cp "$2" "$d/$3"; chmod +x "$d/$3"
  cp "$COCKPIT/seat_resolve.sh" "$COCKPIT/dead_banner_check.sh" "$d/"
  printf '%s\n' "$d"
}

# run_ww <cockpit-dir> <fixture> <stable_n> <max_cycles> — one watcher invocation (a runner re-arm)
run_ww() {
  local d="$1" fx="$2" key
  printf '%%11|Arms/Pane|%s\n' "$fx" > "$d/panes"
  key="_11"
  for t in 50 65 70 80 90; do : > "$d/state/ctx_fired_${key}_99999_$t"; done   # ctx leg quiet: not under test
  : > "$d/sleeps"
  PATH="$BIN:$PATH" WW_PANES="$d/panes" WW_SLEEPS="$d/sleeps" WW_MAX="$4" \
    /bin/bash "$d/wake_watch.sh" "2099-01-01T00:00" "$3" 60 2>&1
}

# check <label> <output> <want-substring|NONE> [<must-not-substring>]
check() {
  local label="$1" out="$2" want="$3" deny="${4:-}" ok=1
  if [ "$want" = NONE ]; then
    case "$out" in *"WAKE:"*) ok=0 ;; esac
  else
    case "$out" in *"$want"*) ;; *) ok=0 ;; esac
  fi
  if [ -n "$deny" ]; then case "$out" in *"$deny"*) ok=0 ;; esac; fi
  if [ "$ok" = 1 ]; then PASS=$((PASS+1)); echo "PASS  $label"; else FAIL=$((FAIL+1)); echo "FAIL  $label"; fi
  echo "      -> $(printf '%s' "$out" | tr '\n' ' ' | cut -c1-330)"
}

echo "wake_watch false-wake arms — $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "  OLD=$WW_OLD"
echo "  NEW=$WW_NEW"
echo "  work=$WORK"
echo

SEATA_LIVE="$FIX/real_seatA_holding_live_2303.ansi"
SEATA_2254="$FIX/real_seatA_holding_2254_dimmed.ansi"
WAITF="$FIX/synth_waiting_on_subagents.ansi"
WAITSH="$FIX/synth_waiting_on_subagents_shells.ansi"
STUCK="$FIX/synth_waiting_stuck_past_bound.ansi"
IDLE="$FIX/synth_idle_empty_prompt.ansi"
BUSY="$FIX/synth_busy_spinner_frozen.ansi"
BUSYSH="$FIX/synth_busy_shell_inflight_frozen.ansi"

echo "== B. holding by design (real seat-A captures) =="
d=$(mk_tree old_seatA "$WW_OLD" wake_watch.sh)
check "OLD seat-A live 23:03 -> false FROZEN-BUSY wake (negative control)" "$(run_ww "$d" "$SEATA_LIVE" 3 10)" "content FROZEN"
d=$(mk_tree old_seatA_acked "$WW_OLD" wake_watch.sh); fixture_hash "$SEATA_LIVE" > "$d/state/idle_ack__11"
check "OLD seat-A live, IDLE-ACKed -> ack cannot suppress it, still FROZEN (negative control)" "$(run_ww "$d" "$SEATA_LIVE" 3 10)" "content FROZEN"
d=$(mk_tree new_seatA "$WW_NEW" wake_watch.sh)
check "NEW seat-A live 23:03 -> no FROZEN; routed to idle path (HOLDING idle wake)" "$(run_ww "$d" "$SEATA_LIVE" 3 10)" "idle at prompt ~3 min — likely waiting on Wednesday (HOLDING" "content FROZEN"
d=$(mk_tree new_seatA_acked "$WW_NEW" wake_watch.sh); fixture_hash "$SEATA_LIVE" > "$d/state/idle_ack__11"
check "NEW seat-A live, IDLE-ACKed -> NO wake at all" "$(run_ww "$d" "$SEATA_LIVE" 3 10)" NONE
d=$(mk_tree old_seatA2254 "$WW_OLD" wake_watch.sh)
check "OLD seat-A 22:54 (Wednesday's capture) -> false FROZEN-BUSY wake (negative control)" "$(run_ww "$d" "$SEATA_2254" 3 10)" "content FROZEN"
d=$(mk_tree new_seatA2254 "$WW_NEW" wake_watch.sh); fixture_hash "$SEATA_2254" > "$d/state/idle_ack__11"
check "NEW seat-A 22:54, IDLE-ACKed -> NO wake" "$(run_ww "$d" "$SEATA_2254" 3 10)" NONE
# The same capture VERBATIM (tmux -p, no escapes): its prompt text cannot be told from TYPED text,
# and typed-unsent text is deliberately not idle — so the pane is not "holding" and the frozen leg
# behaves exactly as before. Proves the holding route needs an EMPTY prompt, not just a done line.
d=$(mk_tree new_seatA2254_typed "$WW_NEW" wake_watch.sh)
check "NEW seat-A 22:54 verbatim plain (prompt reads as TYPED) -> frozen leg unchanged" "$(run_ww "$d" "$FIX/real_seatA_holding_2254_plain.txt" 3 10)" "content FROZEN"
echo

echo "== A. waiting on background subagents =="
d=$(mk_tree old_wait "$WW_OLD" wake_watch.sh)
check "OLD waiting (Tuesday's shape) -> false IDLE wake (negative control)" "$(run_ww "$d" "$WAITF" 3 10)" "idle at prompt ~3 min"
d=$(mk_tree new_wait "$WW_NEW" wake_watch.sh)
check "NEW waiting (Tuesday's shape), 10 cycles -> NO wake" "$(run_ww "$d" "$WAITF" 3 10)" NONE
d=$(mk_tree old_waitsh "$WW_OLD" wake_watch.sh)
check "OLD waiting + '· 2 shells' footer (HPSM-S42 09-13) -> false FROZEN wake (negative control)" "$(run_ww "$d" "$WAITSH" 3 10)" "content FROZEN"
d=$(mk_tree new_waitsh "$WW_NEW" wake_watch.sh)
check "NEW waiting + '· 2 shells' footer, 10 cycles -> NO wake" "$(run_ww "$d" "$WAITSH" 3 10)" NONE
for v in synth_waiting_variant_singular_glyph synth_waiting_variant_spacing_subagents; do
  d=$(mk_tree "old_$v" "$WW_OLD" wake_watch.sh)
  check "OLD $v -> false IDLE wake (negative control)" "$(run_ww "$d" "$FIX/$v.ansi" 3 10)" "idle at prompt"
  d=$(mk_tree "new_$v" "$WW_NEW" wake_watch.sh)
  check "NEW $v (tolerant match) -> NO wake" "$(run_ww "$d" "$FIX/$v.ansi" 3 10)" NONE
done
d=$(mk_tree new_waitdone "$WW_NEW" wake_watch.sh)
check "NEW stale waiting line then a done line (wait finished) -> still IDLE wake" "$(run_ww "$d" "$FIX/synth_waiting_then_done_idle.ansi" 3 10)" "idle at prompt ~3 min — likely waiting on Wednesday" "HOLDING"
echo

echo "== A-bound. waiting frozen past the subagent-wait bound (default 60 min) =="
d=$(mk_tree new_stuck "$WW_NEW" wake_watch.sh); H=$(fixture_hash "$STUCK"); NOW=$(date +%s)
printf '%s %s %s' "$H" "$((NOW - 61*60))" 0 > "$d/state/wait_since__11"
OUT=$(run_ww "$d" "$STUCK" 3 10)
check "NEW stuck-waiting, clock seeded 61 min ago -> the NEW long-bound wake text" "$OUT" "waiting on 2 subagents with no change for ~61 min — check the pane"
check "  ...and that text is tappable by the LIVE runner (contains 'idle at prompt')" "$OUT" "idle at prompt"
W=$(cat "$d/state/wait_since__11")
case "$W" in "$H $((NOW - 61*60)) "[1-9]*) PASS=$((PASS+1)); echo "PASS    ...lastfired stamp committed: $W" ;; *) FAIL=$((FAIL+1)); echo "FAIL    ...lastfired stamp NOT committed: $W" ;; esac
check "NEW stuck-waiting, next runner re-arm (same state dir) -> rate-limited, NO wake" "$(run_ww "$d" "$STUCK" 3 10)" NONE
printf '%s %s %s' "$H" "$((NOW - 125*60))" "$((NOW - 61*60))" > "$d/state/wait_since__11"
check "NEW stuck-waiting, last fire 61 min ago -> re-fires (never silenced for good)" "$(run_ww "$d" "$STUCK" 3 10)" "subagents with no change for ~125 min"
d=$(mk_tree new_stuck_acked "$WW_NEW" wake_watch.sh)
printf '%s %s %s' "$H" "$((NOW - 61*60))" 0 > "$d/state/wait_since__11"; printf '%s' "$H" > "$d/state/idle_ack__11"
check "NEW stuck-waiting, acked with wake_ack.sh's hash -> NO wake" "$(run_ww "$d" "$STUCK" 3 10)" NONE
d=$(mk_tree new_stuck_fresh "$WW_NEW" wake_watch.sh)
check "NEW same wait with no seeded clock (fresh) -> NO wake (bound not reached)" "$(run_ww "$d" "$STUCK" 3 10)" NONE
printf '%s %s %s' "0000deadbeef" "$((NOW - 90*60))" 0 > "$d/state/wait_since__11"
check "NEW old clock for DIFFERENT content (a subagent finished) -> clock resets, NO wake" "$(run_ww "$d" "$STUCK" 3 10)" NONE
d=$(mk_tree new_stuck_env "$WW_NEW" wake_watch.sh)
printf '%s %s %s' "$H" "$((NOW - 11*60))" 0 > "$d/state/wait_since__11"
check "NEW WAKE_WATCH_SUBAGENT_WAIT_MIN=10 override, clock 11 min -> fires" "$(WAKE_WATCH_SUBAGENT_WAIT_MIN=10 run_ww "$d" "$STUCK" 3 10)" "with no change for ~11 min"
echo

echo "== C/D. controls that must NOT be weakened =="
for s in old new; do
  eval "SCR=\$WW_$(printf '%s' "$s" | tr a-z A-Z)"
  d=$(mk_tree "${s}_idle" "$SCR" wake_watch.sh)
  check "$(printf '%s' "$s" | tr a-z A-Z) genuinely idle empty prompt -> plain IDLE wake (not labelled HOLDING)" "$(run_ww "$d" "$IDLE" 3 10)" "idle at prompt ~3 min — likely waiting on Wednesday" "HOLDING"
  d=$(mk_tree "${s}_busy" "$SCR" wake_watch.sh)
  check "$(printf '%s' "$s" | tr a-z A-Z) genuinely busy spinner+tokens, render frozen -> FROZEN-BUSY wake" "$(run_ww "$d" "$BUSY" 3 10)" "content FROZEN ~6 min"
  d=$(mk_tree "${s}_busysh" "$SCR" wake_watch.sh)
  check "$(printf '%s' "$s" | tr a-z A-Z) busy in-flight turn + shell still running (old done line above) -> FROZEN-BUSY wake" "$(run_ww "$d" "$BUSYSH" 3 10)" "content FROZEN ~6 min"
done
echo

echo "== runner consumer: the new wake shape has a case line ABOVE the idle line =="
ARM="$COCKPIT/arm_wake_watch.sh"; [ -f "${ARM_NEW:-}" ] && ARM="$ARM_NEW"
ls_sub=$(grep -n '\*"subagents with no change"\*)' "$ARM" | head -1 | cut -d: -f1)
ls_idle=$(grep -n '\*"idle at prompt"\*' "$ARM" | head -1 | cut -d: -f1)
if [ -n "$ls_sub" ] && [ -n "$ls_idle" ] && [ "$ls_sub" -lt "$ls_idle" ]; then
  PASS=$((PASS+1)); echo "PASS  $ARM: subagents case line $ls_sub < idle case line $ls_idle"
else
  FAIL=$((FAIL+1)); echo "FAIL  $ARM: subagents case line '${ls_sub:-missing}' idle case line '${ls_idle:-missing}'"
fi
echo

echo "== monitor.sh INPUT predicate (defect A there too: log-only [INPUT] alerts) =="
# run_mon <label> <script> <fixture> <quiet-minutes> -> prints the alerts.log lines it produced
run_mon() {
  local d; d=$(mk_tree "$1" "$2" monitor.sh)
  printf '%%11|Arms/Pane|%s\n' "$3" > "$d/panes"
  local content; content=$(PATH="$BIN:$PATH" WW_PANES="$d/panes" tmux capture-pane -p -t %11 -S -40 | tail -40)
  printf '%s' "$content" | md5 -q > "$d/state/.hash_Arms_Pane"
  echo "$(( $(date +%s) - $4 * 60 ))" > "$d/state/.time_Arms_Pane"
  PATH="$BIN:$PATH" WW_PANES="$d/panes" /bin/bash "$d/monitor.sh" --once >/dev/null 2>&1
  cat "$d/state/alerts.log" 2>/dev/null
}
check "OLD monitor, waiting pane quiet 5m -> false [INPUT] (negative control)" "$(run_mon mon_old_wait5 "$MON_OLD" "$WAITF" 5)" "[INPUT] Arms/Pane"
out=$(run_mon mon_new_wait5 "$MON_NEW" "$WAITF" 5)
if [ -z "$out" ]; then PASS=$((PASS+1)); echo "PASS  NEW monitor, waiting pane quiet 5m -> no alert"; else FAIL=$((FAIL+1)); echo "FAIL  NEW monitor, waiting pane quiet 5m -> $out"; fi
check "OLD monitor, waiting pane quiet 61m -> [INPUT] (negative control)" "$(run_mon mon_old_wait61 "$MON_OLD" "$WAITF" 61)" "[INPUT] Arms/Pane"
check "NEW monitor, waiting pane quiet 61m -> bounded [STALL] naming the wait" "$(run_mon mon_new_wait61 "$MON_NEW" "$WAITF" 61)" "[STALL] Arms/Pane — waiting on background subagents with no change for 61m" "[INPUT]"
check "NEW monitor, genuinely idle quiet 5m -> [INPUT] unchanged" "$(run_mon mon_new_idle5 "$MON_NEW" "$IDLE" 5)" "[INPUT] Arms/Pane"
check "NEW monitor, wait finished then done line, quiet 5m -> [INPUT] unchanged" "$(run_mon mon_new_waitdone "$MON_NEW" "$FIX/synth_waiting_then_done_idle.ansi" 5)" "[INPUT] Arms/Pane"
echo

echo "PASS=$PASS FAIL=$FAIL"
[ "$FAIL" = 0 ]

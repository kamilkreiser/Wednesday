#!/bin/bash
# stucktap_arms.sh — red-proof for the runner's OWN-STUCK-TAP discriminator (arm_wake_watch.sh, 2026-09-15).
# Arms: (1) FIRE — text at the prompt is a substring of the last tap → Enter is sent;
#       (2) QUIET — text at the prompt is NOT from the last tap → held, no Enter;
#       (3) SHORT — a short (<12 char) match is NOT enough → held (guards Kam typing a common word).
# Runs in a scratch tmux session `rptest`; never touches fleet:0. State lives under the caller's
# scratchpad ($STUCKTAP_TMP, default /tmp/stucktap_arms) and is left in place (never-delete rule).
set -u
TMUX_BIN=$(command -v tmux); S=rptest; SEAT=rptest
STATE_DIR="${STUCKTAP_TMP:-/tmp/stucktap_arms}"; mkdir -p "$STATE_DIR"
PASS=0; FAIL=0
extract() { "$TMUX_BIN" capture-pane -t "$1" -p -e 2>/dev/null | grep -a "$(printf "\342\235\257")" | tail -1 | \
  LC_ALL=C perl -pe "s/\x1b\[2m.*?(?=\x1b|\$)//g; s/\x1b\[[0-9;]*m//g; s/\xc2\xa0/ /g; s/^.*\xe2\x9d\xaf//" 2>/dev/null | tr -d "[:space:]"; }
decide() { # $1 pane, prints FIRE or HELD, mirrors the runner's condition
  local PTXT LASTTAP; PTXT=$(extract "$1"); LASTTAP=$(tr -d "[:space:]" < "$STATE_DIR/last_tap_$SEAT.txt")
  if [ -n "$LASTTAP" ] && [ "${#PTXT}" -ge 12 ] && case "$LASTTAP" in *"$PTXT"*) true ;; *) false ;; esac; then
    "$TMUX_BIN" send-keys -t "$1" Enter; echo FIRE; else echo HELD; fi; }
run_arm() { # name, prompt-text, last-tap, expected
  "$TMUX_BIN" kill-session -t $S 2>/dev/null; sleep 0.3
  "$TMUX_BIN" new-session -d -s $S -x 200 -y 20 "bash -c 'printf \"\\342\\235\\257 %s\" \"$2\"; read x; echo; echo ENTER-RECEIVED; sleep 5'"
  sleep 0.8; printf "%s" "$3" > "$STATE_DIR/last_tap_$SEAT.txt"
  local got; got=$(decide "$S:0.0"); sleep 0.5
  local seen; seen=$("$TMUX_BIN" capture-pane -t "$S:0.0" -p | grep -c ENTER-RECEIVED)
  local want; if [ "$4" = FIRE ]; then want=1; else want=0; fi
  if [ "$got" = "$4" ] && [ "$seen" = "$want" ]; then PASS=$((PASS+1)); echo "PASS $1: $got (ENTER-RECEIVED=$seen)"; else FAIL=$((FAIL+1)); echo "FAIL $1: got $got expected $4 (ENTER-RECEIVED=$seen)"; fi
}
TAP='[wake_watch] WAKE: new mail at 2026-09-14T12:20 (baseline 2026-09-14T12:14) — check the fleet inbox / pane now.'
run_arm FIRE-prefix  '[wake_watch] WAKE: new mail at 2026-09-14T12:20 (baseline' "$TAP" FIRE
run_arm FIRE-tail    'check the fleet inbox / pane now.' "$TAP" FIRE
run_arm QUIET-kam    'please merge the thing and tell me' "$TAP" HELD
run_arm SHORT-word   'WAKE' "$TAP" HELD
run_arm QUIET-nolast 'anything at all here' "" HELD
"$TMUX_BIN" kill-session -t $S 2>/dev/null
echo "PASS=$PASS FAIL=$FAIL"; [ "$FAIL" = 0 ]

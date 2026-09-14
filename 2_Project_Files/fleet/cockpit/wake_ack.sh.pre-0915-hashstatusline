#!/bin/bash
# wake_ack.sh — acknowledge an agent pane's CURRENT idle state so wake_watch's
# idle-at-prompt leg stops re-firing on a state Wednesday has already judged.
#
# WHY (measured 2026-09-07): wake_watch's STATE_DIR is a fresh `mktemp -d` per
# invocation and arm_wake_watch re-arms it every ~2 min, so the stability
# counter restarts every cycle. A pane parked at an empty prompt — dormant BY
# DESIGN, holding for Kam, with Wednesday as its wake path — therefore fires
# every ~2 min forever. Two fires in eight minutes on %162 (Secuura/Blockchain)
# is what surfaced it; the runner log shows armed 22:35:05, WAKE 22:37:10,
# re-armed 22:39:10, and it would have run all night.
#
# The ack is the pane's CONTENT HASH, written to cockpit/state/ (persistent
# across re-arm). wake_watch suppresses the idle wake only while the hash still
# matches, so ANY new output lifts it automatically. This cannot silence a pane
# that has something to say — and mail wakes and ctx wakes are separate legs,
# untouched.
#
# Usage: wake_ack.sh %162 [%171 ...]      ack those panes' current state
#        wake_ack.sh --list              show live acks
#        wake_ack.sh --clear %162        drop an ack (pane fires again)
# Exit: 0 ok · 2 usage · 3 pane not found
set -u
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CTX_STATE="$SELF_DIR/state"; mkdir -p "$CTX_STATE"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"

# Hash computed EXACTLY as wake_watch.sh computes it. If these two ever drift,
# the ack silently never matches and this whole guard becomes a check that
# cannot fail — so they are asserted equal by the exercise in the commit.
pane_hash() {
  # wake_watch does: tail=$(capture | grep -v '^$' | tail -20); printf '%s' "$tail"
  # Command substitution strips only the TRAILING newline; internal newlines
  # survive. A `tr -d '\n'` here would strip them all and the hashes would never
  # match — the first draft of this file did exactly that.
  local t
  t="$("$TMUX_BIN" capture-pane -t "$1" -p 2>/dev/null | grep -v '^$' | tail -20)"
  printf '%s' "$t" | shasum | cut -c1-12
}
pane_key() { printf '%s' "$1" | tr -c 'A-Za-z0-9' '_'; }

case "${1:-}" in
  ''|-h|--help) echo "usage: wake_ack.sh %pane [%pane ...] | --list | --clear %pane" >&2; exit 2;;
  --list)
    found=0
    for f in "$CTX_STATE"/idle_ack_*; do
      [ -e "$f" ] || continue
      found=1; printf '%s = %s\n' "$(basename "$f")" "$(cat "$f")"
    done
    [ "$found" = 1 ] || echo "(no idle acks)"
    exit 0;;
  --clear)
    [ -n "${2:-}" ] || { echo "wake_ack: --clear needs a pane id" >&2; exit 2; }
    rm -f "$CTX_STATE/idle_ack_$(pane_key "$2")"
    echo "cleared idle ack for $2 — it will fire again once idle"
    exit 0;;
esac

for pane in "$@"; do
  "$TMUX_BIN" list-panes -a -F '#{pane_id}' 2>/dev/null | grep -qx -- "$pane" || {
    echo "wake_ack: no such pane $pane" >&2; exit 3; }
  h="$(pane_hash "$pane")"
  printf '%s' "$h" > "$CTX_STATE/idle_ack_$(pane_key "$pane")"
  echo "acked $pane at content hash $h — idle wake suppressed until its output changes"
done

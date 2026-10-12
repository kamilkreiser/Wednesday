#!/bin/bash
# tap_tuesday.sh — the LIVE_POLL_TAP for the TUESDAY seat on the mini (2026-09-21, Phase 3 of the external dashboard).
#
# WHY: fleet/cockpit/live_chat_poll.sh taps the seat when Kam types on the live board. An undeliverable tap never
# advances the poller's watermark, so the same row would "fire" forever and wake nobody.
#
# 2026-10-12 (Tuesday s103): it matched the LITERAL pane name `tuesday`. After the Mac mini rebooted, the
# cold-launched seat's pane carried the legacy cockpit.conf name `wednesday`, so every tap all day logged "cockpit:
# no pane named 'tuesday'" and two of Kam's board messages reached the seat 26-62 minutes late. tap_friday.sh had
# already solved this. This file now resolves exactly the way it does: the ONE resolver
# (fleet/cockpit/seat_resolve.sh coord_pane_id, seat tuesday) finds the pane named `tuesday`, else the legacy
# `wednesday` pane ONLY when this tree is a TUESDAY tree and the pane was not started from another seat's tree (the
# guard lives in the resolver). The literal version is kept at tap_tuesday.sh.pre-1012-resolver.
#
# Delivery: cockpit.sh `say <that pane's name>`, which carries the guards (refuses an occupied prompt, never types over
# Kam, reads the prompt back). Exit codes pass through: 0 delivered · 3 guard-held · anything else not delivered.
# TRUNCATES to 180 chars (cockpit refuses a tap over 200 once it prepends its 16-char label).
#
# Usage: LIVE_POLL_TAP=/…/tools/tap_tuesday.sh WED_AGENT=tuesday fleet/cockpit/live_chat_poll.sh --seat tuesday
#        tap_tuesday.sh "message text"
set -u
MSG="${1:-}"
[ -n "$MSG" ] || { echo "usage: tap_tuesday.sh \"message text\"" >&2; exit 2; }
[ "${#MSG}" -le 180 ] || MSG="${MSG:0:177}..."
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd -P "$HERE/../.." && pwd)"
TMUX_BIN="${TMUX_BIN:-$(command -v tmux || echo /opt/homebrew/bin/tmux)}"
. "$ROOT/2_Project_Files/fleet/cockpit/seat_resolve.sh" || { echo "tap_tuesday: seat_resolve.sh missing — REFUSED" >&2; exit 2; }
seat_resolve "$ROOT"
if [ "$TREE_SEAT" != "tuesday" ]; then
  echo "tap_tuesday: REFUSED — this tree ('$(basename "$ROOT")') is seat '$TREE_SEAT', not a TUESDAY tree; use this seat's own tap" >&2
  exit 2
fi
PANE="$(coord_pane_id "=fleet" tuesday tuesday)" || exit 1
NAME="$("$TMUX_BIN" list-panes -s -t "=fleet" -F '#{pane_id}|#{@cockpit_name}' | awk -F'|' -v p="$PANE" '$1==p{print $2; exit}')"
[ -n "$NAME" ] || { echo "tap_tuesday: resolved pane $PANE has no @cockpit_name — not tapping blind" >&2; exit 1; }
exec bash "$ROOT/2_Project_Files/fleet/cockpit/cockpit.sh" say "$NAME" "$MSG"

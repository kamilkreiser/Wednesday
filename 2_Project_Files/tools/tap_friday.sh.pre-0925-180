#!/bin/bash
# tap_friday.sh — the LIVE_POLL_TAP for the FRIDAY seat on Kam's laptop (2026-09-23, Kam 10:49: the laptop agent
# becomes Friday, own folder, both clients). Default tap for `live_chat_poll.sh --seat friday`.
#
# WHY NOT tap_wednesday.sh / tap_tuesday.sh: those match a pane by a LITERAL name (`wednesday` / `tuesday`). On the
# laptop the coordinator pane may still carry the legacy name `wednesday` (cockpit.conf pane 0) or, after a rotation,
# `friday` (wednesday_rotate.sh renames the pane to the seat). A literal picks one and silently fails on the other, and
# an undeliverable tap never advances the poller's watermark, so the same row fires forever and wakes nobody.
#
# DESIGN: resolve, then delegate. The pane is found by the ONE resolver (fleet/cockpit/seat_resolve.sh coord_pane_id,
# seat friday): the pane named `friday`, else the legacy `wednesday` pane ONLY when this tree is a FRIDAY tree and the
# pane was not started from another seat's tree (the guard lives there). Delivery is cockpit.sh `say <that pane's
# name>`, which carries the guards that matter (refuses an occupied prompt — never types over Kam — and reads the
# prompt back). Exit codes pass through: 0 delivered · 3 guard-held · anything else not delivered.
# TRUNCATES to 190 chars (cockpit refuses a tap over 200 without --mail), exactly as tap_tuesday.sh does.
#
# Usage: tap_friday.sh "message text"      (WED_AGENT need not be set: the seat is fixed to friday here)
set -u
MSG="${1:-}"
[ -n "$MSG" ] || { echo "usage: tap_friday.sh \"message text\"" >&2; exit 2; }
[ "${#MSG}" -le 190 ] || MSG="${MSG:0:187}..."
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd -P "$HERE/../.." && pwd)"
TMUX_BIN="${TMUX_BIN:-$(command -v tmux || echo /opt/homebrew/bin/tmux)}"
. "$ROOT/2_Project_Files/fleet/cockpit/seat_resolve.sh" || { echo "tap_friday: seat_resolve.sh missing — REFUSED" >&2; exit 2; }
seat_resolve "$ROOT"
if [ "$TREE_SEAT" != "friday" ]; then
  echo "tap_friday: REFUSED — this tree ('$(basename "$ROOT")') is seat '$TREE_SEAT', not a FRIDAY tree; use this seat's own tap" >&2
  exit 2
fi
PANE="$(coord_pane_id "=fleet" friday friday)" || exit 1          # coord_pane_id already printed why on stderr
NAME="$("$TMUX_BIN" list-panes -s -t "=fleet" -F '#{pane_id}|#{@cockpit_name}' | awk -F'|' -v p="$PANE" '$1==p{print $2; exit}')"
[ -n "$NAME" ] || { echo "tap_friday: resolved pane $PANE has no @cockpit_name — not tapping blind" >&2; exit 1; }
exec bash "$ROOT/2_Project_Files/fleet/cockpit/cockpit.sh" say "$NAME" "$MSG"

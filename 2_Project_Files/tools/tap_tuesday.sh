#!/bin/bash
# tap_tuesday.sh — the LIVE_POLL_TAP for the TUESDAY seat on the mini (2026-09-21, Phase 3 of the external dashboard).
#
# WHY: fleet/cockpit/live_chat_poll.sh taps the seat when Kam types on the live board. Its default tap,
# tools/tap_wednesday.sh, matches the pane named `wednesday` only (tap_wednesday.sh:78), so on the mini — where the
# seat's pane is `tuesday` — every tap is undeliverable ("no wednesday pane in 'fleet'", measured here today). An
# undeliverable tap never advances the poller's watermark, so the same row would "fire" forever and wake nobody.
# Wednesday's 04:46Z mail: "on the mini the tap helper is yours (LIVE_POLL_TAP)".
#
# DESIGN: delegate, do not copy. cockpit.sh `say` already carries the guards that matter — it REFUSES to type over an
# occupied prompt (never over Kam) and VERIFIES delivery by reading the prompt back — so this is a wrapper, not a
# second implementation of the guard. Its exit codes already match the poller's contract:
#   0 = delivered (poller advances the watermark) · 3 = prompt occupied, guard-held (watermark untouched, refire)
#   anything else = not delivered (watermark untouched, refire next tick)
# TRUNCATES to 190 chars: cockpit refuses a tap over 200 ("a tap is a pointer, content goes by mail"), and a refused
# over-long summary would be refused on EVERY tick — the watermark would never move. The text itself is read with
# tools/kam_msgs.sh; the tap only has to say that he wrote.
#
# Usage: LIVE_POLL_TAP=/…/tools/tap_tuesday.sh WED_AGENT=tuesday fleet/cockpit/live_chat_poll.sh --seat tuesday
#        tap_tuesday.sh "message text"
set -u
MSG="${1:-}"
[ -n "$MSG" ] || { echo "usage: tap_tuesday.sh \"message text\"" >&2; exit 2; }
[ "${#MSG}" -le 190 ] || MSG="${MSG:0:187}..."
HERE="$(dirname "${BASH_SOURCE[0]}")"
exec bash "$HERE/../fleet/cockpit/cockpit.sh" say tuesday "$MSG"

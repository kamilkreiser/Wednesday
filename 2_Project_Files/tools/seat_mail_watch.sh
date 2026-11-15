#!/bin/bash
# seat_mail_watch.sh — print one line per NEW actionable seat mail (QUESTION / READY / MERGED / WRAP / STATUS)
# in wednesday-agent@, polling the read-only inbox digest. Built 2026-11-15 after the w=2 mail-lapse ledger row
# (twice in one session a seat waited 50-66 min for an ANSWER or GO; the "read mail every 15 min" sentence was a
# promise, not a mechanism). Run under the Monitor tool: each stdout line is a wake.
# It never touches newmail.sh's seen-ids, so the coordinator's own read is unaffected.
# Usage: seat_mail_watch.sh [interval_seconds]   (default 120). First pass seeds silently.
set -u
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; W="$(cd "$SELF_DIR/../.." && pwd)"
STATE_DIR="${TMPDIR:-/tmp}/wed_seat_mail_watch"; mkdir -p "$STATE_DIR"; SEEN="$STATE_DIR/printed.txt"; touch "$SEEN"
INT="${1:-120}"; first=1
while true; do
  rows="$(bash "$W/2_Project_Files/fleet/inbox_digest.sh" --all 2>/dev/null | /usr/bin/grep -E '^\[(QUESTION|INBOUND|WRAP)\]' | /usr/bin/grep -i -E 'QUESTION|READY|MERGED|wrap|STATUS|STOP|BLOCKED' || true)"
  while IFS= read -r r; do
    [ -z "$r" ] && continue
    if ! /usr/bin/grep -qxF -- "$r" "$SEEN"; then
      printf '%s\n' "$r" >> "$SEEN"
      [ "$first" = 1 ] || printf 'SEAT MAIL: %s\n' "$(printf '%s' "$r" | cut -c1-170)"
    fi
  done <<< "$rows"
  first=0; sleep "$INT"
done

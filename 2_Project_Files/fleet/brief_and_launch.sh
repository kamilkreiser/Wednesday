#!/bin/bash
# brief_and_launch.sh — send a brief, VERIFY it at the destination, THEN launch.
# Sequenced by construction: the launch step cannot run unless the send exited 0
# AND the brief was read back from the project's inbox.
#
# WHY THIS EXISTS (enforcement, not advice): ledger w=3, 2026-08-24 — the
# check-the-refusal family. Three times (08-14, 08-17, 08-24) I chained
# `send_brief.sh … && cockpit.sh launch …` in one command; the gate refused the
# send and the launch ran anyway, booting an agent toward an inbox holding only
# a SCORE. Each was recovered by winning a race against the boot ritual. A rule
# adopted by hand lapsed within a session every time, so the sequence becomes a
# script whose launch branch is unreachable without the verified send.
#
# Usage:
#   brief_and_launch.sh --to "<Client>/<Project>" --subject "<topic>" --body-file <path>
#
# Exit codes: 0 sent+verified+launched · 1 refused at any step (nothing launched
# after a refusal) · 2 usage/env error.
#
# Test hooks — ALL THREE or NONE (08-17 lesson: a test hook must never default
# to the production action; a lone override is REFUSED):
#   BAL_SEND_CMD    replaces `send_brief.sh` (must accept the same args)
#   BAL_VERIFY_CMD  replaces the inbox read-back (gets: <inbox> <subject>)
#   BAL_LAUNCH_CMD  replaces `cockpit.sh launch` (gets: <Client/Project>)
set -u
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
ROUTING="$SELF_DIR/inbox_routing.conf"

TO=""; SUBJECT=""; BODY_FILE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --to) TO="${2:-}"; shift 2 ;;
    --subject) SUBJECT="${2:-}"; shift 2 ;;
    --body-file) BODY_FILE="${2:-}"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done
[ -n "$TO" ] && [ -n "$SUBJECT" ] && [ -n "$BODY_FILE" ] || {
  echo "usage: brief_and_launch.sh --to '<Client>/<Project>' --subject '<topic>' --body-file <path>" >&2; exit 2; }

# Test-hook guard: all or none.
set_hooks=0
for v in BAL_SEND_CMD BAL_VERIFY_CMD BAL_LAUNCH_CMD; do [ -n "${!v:-}" ] && set_hooks=$((set_hooks+1)); done
if [ "$set_hooks" -ne 0 ] && [ "$set_hooks" -ne 3 ]; then
  echo "REFUSED — test hooks must be set ALL or NONE (set: $set_hooks of 3). A partial override would fall through to a production step." >&2
  exit 2
fi

# Destination inbox from the routing file (same authority send_brief.sh uses).
INBOX="$(grep -v '^[[:space:]]*#' "$ROUTING" | grep -F "$TO|" | head -1 | cut -d'|' -f2)"
[ -n "$INBOX" ] || { echo "REFUSED — '$TO' not in $ROUTING" >&2; exit 1; }

# ── STEP 1: SEND (may refuse) ─────────────────────────────────────────────
if [ -n "${BAL_SEND_CMD:-}" ]; then
  $BAL_SEND_CMD --to "$TO" --subject "$SUBJECT" --body-file "$BODY_FILE"; rc=$?
else
  bash "$SELF_DIR/send_brief.sh" --to "$TO" --subject "$SUBJECT" --body-file "$BODY_FILE"; rc=$?
fi
if [ "$rc" -ne 0 ]; then
  echo "LAUNCH REFUSED — send exited $rc. Nothing launched. Fix the brief and re-run." >&2
  exit 1
fi

# ── STEP 2: VERIFY AT DESTINATION (read-back, not exit code) ─────────────
verify_inbox() { # $1 inbox  $2 subject  — prints timestamp on success
  set -a; source "$PROJECT_DIR/4_Credentials/.env" 2>/dev/null; set +a
  [ -n "${AGENTMAIL_API_KEY:-}" ] || { echo "no AGENTMAIL_API_KEY" >&2; return 1; }
  curl -sS "https://api.agentmail.to/v0/inboxes/$1/messages?limit=5" \
    -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  | SUBJ="$2" python3 -c '
import json,os,sys
want=os.environ["SUBJ"]
try: ms=json.load(sys.stdin).get("messages",[])
except Exception as e: print("parse error: %s"%e, file=sys.stderr); sys.exit(1)
hits=[m for m in ms if want in str(m.get("subject",""))]
if not hits: sys.exit(1)
print(max(str(m.get("timestamp","")) for m in hits))'
}
found=""
for attempt in 1 2 3 4 5 6; do
  if [ -n "${BAL_VERIFY_CMD:-}" ]; then found="$($BAL_VERIFY_CMD "$INBOX" "$SUBJECT")" && break
  else found="$(verify_inbox "$INBOX" "$SUBJECT")" && break; fi
  sleep 5
done
if [ -z "$found" ]; then
  echo "LAUNCH REFUSED — brief not found in $INBOX after 30s of read-back (send said ok). Nothing launched. Check the inbox before launching by hand." >&2
  exit 1
fi
echo "verified at destination: $INBOX @ $found"

# ── STEP 3: LAUNCH (only reachable through 1 and 2) ───────────────────────
if [ -n "${BAL_LAUNCH_CMD:-}" ]; then $BAL_LAUNCH_CMD "$TO"; rc=$?
else bash "$SELF_DIR/cockpit/cockpit.sh" launch "$TO"; rc=$?; fi
[ "$rc" -eq 0 ] || { echo "launch step exited $rc (brief IS at destination — launch by hand: cockpit.sh launch '$TO')" >&2; exit 1; }
echo "launched: $TO"

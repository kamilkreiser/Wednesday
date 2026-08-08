#!/bin/bash
# send_queue.sh — a TRIGGER for mail that could not be sent yet.
#
# WHY THIS EXISTS (ledger 2026-08-08): AgentMail enforces a daily send cap. On
# 2026-08-08 the fleet hit it at ~06:00 and the cap did not clear until 09:59,
# which meant a scored-run mail and two authorised briefs had nowhere to go. The
# 06:00 session's answer was to write the mail to 0_Brain/inbox/ and intend to
# send it later. That is precisely the failure named in
# 0_Brain/learnings/2026-08-07_a-promise-is-not-a-mechanism.md: a queued item
# with no trigger is indistinguishable from a forgotten one, and nothing would
# have looked wrong if it never went.
#
# So the queue gets a mechanism. This script waits out the window and drains,
# with backoff, logging everything — and it sends through send_brief.sh, which
# means the PROVENANCE gate still applies. It deliberately adds no new sender.
#
# Usage:
#   send_queue.sh add --to "<Client>/<Project>" --subject "<s>" --body-file <p> [--kind brief|answer]
#   send_queue.sh drain            # one pass, retries a 429 with backoff
#   send_queue.sh watch <secs>     # sleep <secs>, then drain (this is the trigger)
#   send_queue.sh status           # what is pending, and how old
#
# Exit: 0 queue empty at finish · 1 items still pending · 2 usage/env error
set -u

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
QUEUE_DIR="$SELF_DIR/state/send_queue"
SENT_DIR="$QUEUE_DIR/sent"
LOG="$PROJECT_DIR/2_Project_Files/scheduler/logs/send_queue_$(date +%Y-%m-%d).log"
# Overridable ONLY so the success path can be exercised with a stub before arming.
# Production always uses send_brief.sh, so the PROVENANCE gate is never bypassed.
SENDER="${SEND_QUEUE_SENDER:-$SELF_DIR/send_brief.sh}"
BODY_SEP="---BODY---"

mkdir -p "$QUEUE_DIR" "$SENT_DIR" "$(dirname "$LOG")"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

[ -x "$SENDER" ] || { log "FATAL: sender not executable: $SENDER"; exit 2; }

cmd="${1:-}"; shift 2>/dev/null || true

case "$cmd" in
  add)
    TO=""; SUBJECT=""; BODY_FILE=""; KIND="brief"
    while [ $# -gt 0 ]; do
      case "$1" in
        --to) TO="${2:-}"; shift 2 ;;
        --subject) SUBJECT="${2:-}"; shift 2 ;;
        --body-file) BODY_FILE="${2:-}"; shift 2 ;;
        --kind) KIND="${2:-}"; shift 2 ;;
        *) echo "unknown arg: $1" >&2; exit 2 ;;
      esac
    done
    [ -n "$TO" ] && [ -n "$SUBJECT" ] && [ -n "$BODY_FILE" ] || {
      echo "usage: send_queue.sh add --to <Client/Project> --subject <s> --body-file <p> [--kind brief|answer]" >&2; exit 2; }
    [ -f "$BODY_FILE" ] || { echo "body file not found: $BODY_FILE" >&2; exit 2; }
    ITEM="$QUEUE_DIR/$(date +%Y%m%d-%H%M%S)-$$-$(echo "$TO" | tr '/ ' '__').item"
    {
      echo "TO=$TO"
      echo "SUBJECT=$SUBJECT"
      echo "KIND=$KIND"
      echo "QUEUED=$(date '+%Y-%m-%d %H:%M:%S')"
      echo "$BODY_SEP"
      cat "$BODY_FILE"
    } > "$ITEM"
    log "QUEUED $TO :: $SUBJECT -> $(basename "$ITEM")"
    exit 0   # add ONLY queues. Without this it falls through to drain and sends
             # immediately, which defeats the entire point of a queue. Found by
             # exercising the refuse path before arming, 2026-08-08.
    ;;

  status)
    n=0
    for f in "$QUEUE_DIR"/*.item; do
      [ -e "$f" ] || continue
      n=$((n+1))
      echo "PENDING $(basename "$f")"
      grep -m1 '^TO=' "$f"; grep -m1 '^SUBJECT=' "$f"; grep -m1 '^QUEUED=' "$f"
    done
    [ "$n" -eq 0 ] && echo "queue empty"
    exit 0
    ;;

  watch)
    SECS="${1:-0}"
    case "$SECS" in ''|*[!0-9]*) echo "usage: send_queue.sh watch <seconds>" >&2; exit 2 ;; esac
    log "WATCH armed — sleeping ${SECS}s, will drain at $(date -v+"${SECS}"S '+%H:%M:%S' 2>/dev/null || echo "+${SECS}s")"
    sleep "$SECS"
    log "WATCH woke — draining"
    exec "$0" drain
    ;;

  drain) : ;;

  *) echo "usage: send_queue.sh add|drain|watch <secs>|status" >&2; exit 2 ;;
esac

# ── drain ────────────────────────────────────────────────────────────────
PENDING=0
for ITEM in "$QUEUE_DIR"/*.item; do
  [ -e "$ITEM" ] || continue
  TO="$(grep -m1 '^TO=' "$ITEM" | cut -d= -f2-)"
  SUBJECT="$(grep -m1 '^SUBJECT=' "$ITEM" | cut -d= -f2-)"
  KIND="$(grep -m1 '^KIND=' "$ITEM" | cut -d= -f2-)"
  TMP_BODY="$(mktemp -t sendqueue)"
  awk -v sep="$BODY_SEP" 'f{print} $0==sep{f=1}' "$ITEM" > "$TMP_BODY"

  SENT=0
  # Base delay is overridable so BOTH paths can be exercised before arming
  # (learnings/2026-08-06_exercise-mechanisms-before-arming) without waiting an hour.
  DELAY="${SEND_QUEUE_BASE_DELAY:-60}"
  for attempt in 1 2 3 4 5 6; do
    # stderr is captured and PRINTED on failure, never discarded (learnings/2026-08-06_never-discard-stderr)
    ERR="$("$SENDER" --to "$TO" --subject "$SUBJECT" --body-file "$TMP_BODY" --kind "$KIND" 2>&1)"
    RC=$?
    if [ "$RC" -eq 0 ]; then
      log "SENT $TO :: $SUBJECT (attempt $attempt)"
      mv "$ITEM" "$SENT_DIR/$(basename "$ITEM").sent"
      SENT=1
      break
    fi
    log "SEND FAILED rc=$RC attempt=$attempt :: $TO :: $SUBJECT"
    log "  stderr: $(echo "$ERR" | tr '\n' ' ' | cut -c1-300)"
    case "$ERR" in
      *REFUSED*|*PROVENANCE*)
        log "  REFUSED by the provenance gate — this will not fix itself, leaving queued for a human"
        break ;;
      *429*|*"Too Many Requests"*|*rate_limit*)
        [ "$attempt" -eq 6 ] && { log "  rate-limited on the final attempt — giving up this pass"; break; }
        log "  rate-limited — backing off ${DELAY}s"
        sleep "$DELAY"; DELAY=$((DELAY*2)) ;;
      *)
        [ "$attempt" -eq 6 ] && { log "  failed on the final attempt — giving up this pass"; break; }
        log "  non-rate-limit error — backing off ${DELAY}s"
        sleep "$DELAY"; DELAY=$((DELAY*2)) ;;
    esac
  done
  rm -f "$TMP_BODY"
  [ "$SENT" -eq 1 ] || { PENDING=$((PENDING+1)); log "STILL PENDING: $(basename "$ITEM")"; }
done

if [ "$PENDING" -gt 0 ]; then
  log "DRAIN INCOMPLETE — $PENDING item(s) still queued"
  exit 1
fi
log "DRAIN COMPLETE — queue empty"
exit 0

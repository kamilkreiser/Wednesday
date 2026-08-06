#!/bin/bash
# WED-16 — 23:00 scheduled close. Fired by launchd (com.wednesday.close).
# Deterministic (no LLM): stamps the day closed in the daily note, snapshots
# today's fleet-inbox traffic, speaks a one-line good night. The INTELLIGENT
# close ritual (retro, learnings, handoff) stays with interactive sessions —
# this is the bell at the end of the working day, not a replacement for it.
#
# Guards: once per day · only fires in the 22:30-23:59 window (launchd
# coalesces missed jobs to next Mac wake — a "good night" at 09:00 would be
# worse than silence, and quiet hours start at 23:00 sharp for anything more).

set -u

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
BRAIN_DIR="$PROJECT_DIR/0_Brain"
LOG_DIR="$SELF_DIR/logs"
STATE_DIR="$SELF_DIR/state"
mkdir -p "$LOG_DIR" "$STATE_DIR"
LOG="$LOG_DIR/close_$(date +%F).log"
log() { echo "$(date '+%F %T') $*" >> "$LOG"; }

TODAY="$(date +%F)"
HOUR="$((10#$(date +%H)))"
MIN="$((10#$(date +%M)))"

if [ -f "$STATE_DIR/last_close" ] && [ "$(cat "$STATE_DIR/last_close")" = "$TODAY" ]; then
  log "skip: already closed today"
  exit 0
fi
if [ "$HOUR" -lt 22 ] || { [ "$HOUR" -eq 22 ] && [ "$MIN" -lt 30 ]; }; then
  log "skip: before 22:30 window"
  exit 0
fi

DRYRUN="${WEDNESDAY_DRYRUN:-0}"

# ── Fleet inbox snapshot (best-effort; never blocks the close) ──
MAIL_LINE="fleet inboxes: unreachable (key unset or API down)"
ENV_FILE="$PROJECT_DIR/4_Credentials/.env"
if [ -f "$ENV_FILE" ]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE" 2>/dev/null || true
  if [ -n "${AGENTMAIL_API_KEY:-}" ]; then
    # Errors go to the LOG, never /dev/null — the 08-05 "unreachable" close
    # left no diagnosable trace (WED-16 defect). 3 tries/inbox rides out blips.
    COUNTS="$(python3 - "$TODAY" <<'PYEOF' 2>>"$LOG"
import json, sys, time, urllib.request, os
from datetime import datetime
today = sys.argv[1]
key = os.environ.get("AGENTMAIL_API_KEY", "")
out = []
def local_date(ts):
    # API timestamps are UTC ("...Z"); compare against the LOCAL day or the
    # 23:00 AEST close misses everything before 10:00 local.
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00")).astimezone().date().isoformat()
    except Exception:
        return ""
for inbox in ("wednesday-agent@agentmail.to", "coagent@agentmail.to"):
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                f"https://api.agentmail.to/v0/inboxes/{inbox}/messages?limit=50",
                headers={"Authorization": f"Bearer {key}"})
            with urllib.request.urlopen(req, timeout=10) as r:
                msgs = json.load(r).get("messages", [])
            n = sum(1 for m in msgs if local_date(m.get("timestamp", "")) == today)
            out.append(f"{inbox.split('@')[0]}@: {n} today")
            break
        except Exception as e:
            print(f"inbox check {inbox} attempt {attempt+1}/3: {type(e).__name__}: {e}", file=sys.stderr)
            if attempt == 2:
                out.append(f"{inbox.split('@')[0]}@: unreachable")
            else:
                time.sleep(5)
print(" · ".join(out))
PYEOF
)"
    [ -n "$COUNTS" ] && MAIL_LINE="fleet inboxes: $COUNTS"
  fi
fi

# ── Stamp the daily note (create from template if the day left none) ──
NOTE="$BRAIN_DIR/daily/$TODAY.md"
if [ "$DRYRUN" = "1" ]; then
  log "DRYRUN: would stamp $NOTE with close block ($MAIL_LINE) and speak good night"
  exit 0
fi
if [ ! -f "$NOTE" ]; then
  sed "s/{{date}}/$TODAY/" "$BRAIN_DIR/daily/_template.md" > "$NOTE"
  log "daily note was missing — created from template (no session ran today?)"
fi
{
  echo ""
  echo "## 23:00 close (scheduler, WED-16)"
  echo "- Day closed at $(date '+%H:%M') by the scheduled close ritual."
  echo "- $MAIL_LINE"
  echo "- If a session was mid-flight, next boot reconciles from this note + Linear."
} >> "$NOTE"
echo "$TODAY" > "$STATE_DIR/last_close"
log "daily note stamped; $MAIL_LINE"

# ── One short good night (23:00 sharp is the boundary, not past it) ──
"$PROJECT_DIR/2_Project_Files/voice/speak.sh" "That's the day closed, Kam. Everything still open is safely on the board for the morning. Good night." || log "speak failed (voice unavailable?)"
log "close complete"

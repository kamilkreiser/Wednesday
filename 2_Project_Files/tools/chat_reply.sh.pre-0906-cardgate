#!/bin/bash
# chat_reply.sh — mirror a Wednesday conversational reply into the dashboard chat.
#
# WHY (Kam, 2026-08-17): the terminal interleaves conversation with fleet
# mechanics, so what he is reading scrolls away under agent traffic. The
# dashboard chat tile is the STABLE conversation surface: substantive replies
# to Kam are mirrored here (short form, pointers to documents for anything
# long). Fleet mechanics NEVER go through this script.
#
# Usage: chat_reply.sh "message text"
# Appends {role: "wednesday", ts, text} to 0_Brain/dashboard/data/chat_log.json
# atomically (write temp + mv). Never discards stderr. Refuses empty input.
set -u
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
CHAT="$PROJECT_DIR/0_Brain/dashboard/data/chat_log.json"
MSG="${1:-}"
[ -n "$MSG" ] || { echo "chat_reply: empty message refused" >&2; exit 2; }
[ -f "$CHAT" ] || { echo "chat_reply: no chat log at $CHAT" >&2; exit 1; }
CHAT_FILE="$CHAT" python3 - "$MSG" <<'PYEOF'
import json, os, sys, datetime, tempfile
path = os.environ["CHAT_FILE"]
msg = sys.argv[1]
with open(path) as f:
    log = json.load(f)
log.append({
    "role": "wednesday",
    "ts": datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(),
    "text": msg,
})
d = os.path.dirname(path)
fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(log, f, ensure_ascii=False, indent=1)
os.replace(tmp, path)
print(f"mirrored to dashboard chat ({len(log)} messages)")
PYEOF

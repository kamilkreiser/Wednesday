#!/bin/bash
# chat_reply.sh — mirror a Wednesday conversational reply into the dashboard chat.
#
# WHY (Kam, 2026-08-17): the terminal interleaves conversation with fleet
# mechanics, so what he is reading scrolls away under agent traffic. The
# dashboard chat tile is the STABLE conversation surface: substantive replies
# to Kam are mirrored here (short form, pointers to documents for anything
# long). Fleet mechanics NEVER go through this script.
#
# Usage: chat_reply.sh [--project <Datasec|Secuura|WED>] "message text"
# Appends {role: "wednesday", seat, project, ts, text} to
# 0_Brain/dashboard/data/chat_log.json atomically (write temp + mv). Never
# discards stderr. Refuses empty input.
#
# --project (Kam, 2026-09-07 11:12): tags the entry so each dashboard can choose
# which project's replies it displays / auto-speaks (per-browser filter, WED on
# by default). Omitted → "WED"; entries with no field at all read as "WED".
set -u
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
CHAT="$PROJECT_DIR/0_Brain/dashboard/data/chat_log.json"
PROJECT="WED"
if [ "${1:-}" = "--project" ]; then
  [ -n "${2:-}" ] || { echo "chat_reply: --project needs a value (Datasec|Secuura|WED)" >&2; exit 2; }
  PROJECT="$2"; shift 2
fi
MSG="${1:-}"
[ -n "$MSG" ] || { echo "chat_reply: empty message refused" >&2; exit 2; }
[ -f "$CHAT" ] || { echo "chat_reply: no chat log at $CHAT" >&2; exit 1; }

# ── CARD-ID GATE (2026-09-06 22:2x, mirror-reports-state w=7 → promoted) ──
# The FIRST of the three instances landed here: the panel told Kam a card existed
# that did not, because the line was written in the same batch as a refused add.
# Kam's panel is his reading surface; a line there is a receipt, not a forecast.
GATE="$PROJECT_DIR/2_Project_Files/fleet/card_id_gate.sh"
if [ -f "$GATE" ]; then
  _cg_tmp="$(mktemp)"; printf '%s' "$MSG" > "$_cg_tmp"
  if ! bash "$GATE" "$_cg_tmp"; then
    echo "  (gate: card_id_gate.sh — ledger w=7; nothing was mirrored to Kam's panel)" >&2
    rm -f "$_cg_tmp"; exit 1
  fi
  rm -f "$_cg_tmp"
fi
CHAT_FILE="$CHAT" CHAT_PROJECT="$PROJECT" python3 - "$MSG" <<'PYEOF'
import json, os, sys, datetime, tempfile
path = os.environ["CHAT_FILE"]
msg = sys.argv[1]
with open(path) as f:
    log = json.load(f)
log.append({
    "role": "wednesday",
    "seat": __import__("socket").gethostname(),  # 2026-09-07: which machine wrote this (autoplay scope)
    "project": os.environ.get("CHAT_PROJECT") or "WED",  # 2026-09-07: per-dashboard display filter
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

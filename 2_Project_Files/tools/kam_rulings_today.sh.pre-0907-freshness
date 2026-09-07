#!/bin/bash
# kam_rulings_today.sh — print EVERY message Kam wrote on the dashboard panel today, VERBATIM.
#
# WHY (2026-09-05 16:4x, Kam: "I'm just a little bit worried that there's been a lot of mistakes
# and a lot of oversights lately"): three of the five Kam-caught corrections that day were ONE
# class — something Kam had already said did not survive into the next coordinator seat as a
# rule. His 10:51 panel note "no need to raise this again. this is in hand" was in chat_log.json;
# the 16:0x seat read the panel only for messages AFTER its predecessor's last action and carded
# the same subject at 16:32 (the fourth raise). A handover note SUMMARISES; his words on a card or
# in passing reach it as an episode, not as a rule. This script hands the successor his words,
# not a summary of them. Read at boot (after the brain load, before any card or brief) and at
# every checkpoint.
#
# Usage: kam_rulings_today.sh [YYYY-MM-DD]      (default: today, local time)
# Output: one line per message — "HH:MM | <text>" — oldest first; a count line at the end.
# Exit: 0 printed · 2 chat log missing/unreadable. Never discards stderr.
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG="$PROJECT_DIR/0_Brain/dashboard/data/chat_log.json"
DAY="${1:-$(date +%Y-%m-%d)}"
[ -r "$LOG" ] || { echo "kam_rulings_today: chat log missing or unreadable: $LOG" >&2; exit 2; }
python3 - "$LOG" "$DAY" <<'PY'
import json, sys
log, day = sys.argv[1], sys.argv[2]
d = json.load(open(log))
msgs = d if isinstance(d, list) else d.get("messages", d)
kam = [m for m in msgs if m.get("role") == "kam" and str(m.get("ts", "")).startswith(day)]
print(f"# Kam's panel messages on {day} — VERBATIM, oldest first ({len(kam)} messages). Read every one before any card, brief or ruling.")
for m in kam:
    ts = str(m.get("ts", ""))[11:16]
    text = " ".join(str(m.get("text", "")).split())
    print(f"{ts} | {text}")
print(f"# end — {len(kam)} messages")
PY

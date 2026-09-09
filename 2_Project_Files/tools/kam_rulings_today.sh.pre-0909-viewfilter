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

# --- FRESHNESS (2026-09-07, measured, not theorised) -------------------------------
# This script reads the LOCAL chat_log.json and does not pull. With two Wednesday seats
# on two machines, Kam's panel messages reach this copy only when the OTHER seat commits
# and pushes the log and THIS seat pulls. Measured today: at 18:13 this script reported
# "65 messages, ending 13:40" and was confident. Kam had written FIVE more at 18:03–18:04;
# they appeared only after a later pull. So the one instrument whose whole purpose is
# "never miss his word" can return a complete-looking answer that is 20+ minutes stale.
#
# It does NOT auto-pull: a read command with a side effect on the repo is worse than a
# stale read, and a pull mid-work can conflict. Instead the staleness is made LOUD —
# the newest message's age is printed every time, and an old one warns and names the fix.
# STALE_MIN overrides the threshold; 0 disables the warning.
STALE_MIN="${KAM_RULINGS_STALE_MIN:-25}"

python3 - "$LOG" "$DAY" "$STALE_MIN" <<'PY'
import json, sys, os, datetime
log, day, stale_min = sys.argv[1], sys.argv[2], int(sys.argv[3])
d = json.load(open(log))
msgs = d if isinstance(d, list) else d.get("messages", d)
kam = [m for m in msgs if m.get("role") == "kam" and str(m.get("ts", "")).startswith(day)]
print(f"# Kam's panel messages on {day} — VERBATIM, oldest first ({len(kam)} messages). Read every one before any card, brief or ruling.")
for m in kam:
    ts = str(m.get("ts", ""))[11:16]
    text = " ".join(str(m.get("text", "")).split())
    print(f"{ts} | {text}")
print(f"# end — {len(kam)} messages")

# Freshness line: ALWAYS printed, so a stale read can never look like a quiet one.
newest = max((str(m.get("ts", "")) for m in msgs if m.get("ts")), default="")
mtime = datetime.datetime.fromtimestamp(os.path.getmtime(log)).astimezone()
now = datetime.datetime.now().astimezone()
age_txt = "unknown"
stale = False
if newest:
    try:
        nt = datetime.datetime.fromisoformat(newest)
        mins = (now - nt).total_seconds() / 60.0
        age_txt = f"{mins:.0f} min ago ({newest[11:19]})"
        stale = stale_min > 0 and mins > stale_min
    except ValueError:
        pass
print(f"# FRESHNESS — newest message in this LOCAL copy: {age_txt} · file mtime {mtime:%H:%M:%S}")
if stale:
    print("#")
    print(f"# ⚠️  STALE-COPY WARNING: the newest message here is over {stale_min} minutes old.")
    print("#    This file does NOT update on its own. With two Wednesday seats, Kam's words arrive")
    print("#    only when the other seat pushes the log and THIS seat pulls. An empty tail may mean")
    print("#    'he said nothing' OR 'this copy has not caught up' — those are different facts.")
    print("#    Settle it before concluding he is quiet:")
    print("#      git -C <this repo> pull --rebase --autostash   then re-run this script.")
PY

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
# PHASE 3 (2026-09-21, Kam 12:50 "switch to using the live version only" / 14:05 "interact
# normally while I'm traveling"): his words now land on the LIVE board, encrypted to his keys AND to
# this seat's certificate key. --source live (DEFAULT) reads them through tools/_kam_live.sh
# (dashboard-cloud/seat/get_kam_messages.py --decrypt, as $WED_AGENT — the API returns only this
# seat's partitions + his broadcasts, so a tuesday-tab row never reaches Wednesday's read); --source
# local reads the old chat_log.json (the only place his LOCAL-board replies land); --source both is
# the union, de-duplicated on (UTC minute, text), each line tagged [live]/[local]. A live fetch
# failure is LOUD and exits 2 — never a quiet empty day. The seat filter, the fail-open rule and the
# freshness line below apply to every source; the STALE-COPY warning is about the local file only.
#
# Usage: kam_rulings_today.sh [YYYY-MM-DD] [--source live|local|both]      (default: today, local time; live)
# Output: one line per message — "HH:MM [src] | <text>" — oldest first; a count line at the end.
# Exit: 0 printed · 2 chat log missing/unreadable or live fetch failed. Never discards stderr.
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG="$PROJECT_DIR/0_Brain/dashboard/data/chat_log.json"
DAY="$(date +%Y-%m-%d)"; SOURCE="${KAM_RULINGS_SOURCE:-live}"
# READ MARKER (Friday ledger w=2, 2026-09-29): Kam's 16:28 deploy GO sat unread for ~2.5 h because the rule
# "re-read his rows before every reply" was one a seat had to remember. A full read of TODAY (this script, no
# --unread) records the newest row it SHOWED this seat; `--unread` prints only rows newer than that and never
# advances it — chat_reply.sh calls it before every message to Kam. The marker only moves on a displayed read
# (2026-08-04: a watermark advances only over what reached the processor). KAM_READ_MARKER overrides the path.
MODE=read
MARKER="${KAM_READ_MARKER:-$PROJECT_DIR/2_Project_Files/fleet/state/kam_read_${WED_AGENT:-unset}}"
while [ $# -gt 0 ]; do
  case "$1" in
    --unread) MODE=unread ;;
    --source) SOURCE="${2:-}"; shift ;;
    --source=*) SOURCE="${1#--source=}" ;;
    --*) echo "kam_rulings_today: unknown flag $1" >&2; exit 2 ;;
    *) DAY="$1" ;;
  esac; shift
done
case "$SOURCE" in live|local|both) ;; *) echo "kam_rulings_today: --source must be live|local|both (got '$SOURCE')" >&2; exit 2 ;; esac
if [ "$SOURCE" != "live" ]; then [ -r "$LOG" ] || { echo "kam_rulings_today: chat log missing or unreadable: $LOG" >&2; exit 2; }; fi
LIVE_JSON="[]"
if [ "$SOURCE" != "local" ] && [ -n "${KAM_RULINGS_LIVE_JSON_FILE:-}" ]; then
  # TEST HOOK (arms: 2_Project_Files/tests/kam_unread_arms.sh): a canned live-board reply instead of the network.
  LIVE_JSON="$(cat "$KAM_RULINGS_LIVE_JSON_FILE")" || exit 2
elif [ "$SOURCE" != "local" ]; then
  . "$PROJECT_DIR/2_Project_Files/tools/_kam_live.sh"
  # window = the day before DAY (UTC) onward, cap 1000 (the API caps per partition, oldest-first: a hit cap cuts the NEWEST rows and get_kam_messages warns)
  SINCE="$(date -j -v-1d -f %Y-%m-%d "$DAY" +%Y-%m-%dT00:00 2>/dev/null || echo "${DAY}T00:00")"
  LIVE_JSON="$(kam_live_json --limit 1000 --since "$SINCE")" || exit 2
fi

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

SEAT="${WED_AGENT:-}"

python3 - "$LOG" "$DAY" "$STALE_MIN" "$SEAT" "$SOURCE" "$LIVE_JSON" "$MODE" "$MARKER" <<'PY'
import json, sys, os, datetime
log, day, stale_min, seat, source, live_json = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6]
mode, marker = sys.argv[7], sys.argv[8]
def utc_minute(ts):
    try: return datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00")).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M")
    except Exception: return str(ts)[:16]
msgs = []
if source in ("local", "both"):
    d = json.load(open(log))
    msgs = [dict(m, source="local") for m in (d if isinstance(d, list) else d.get("messages", d)) if isinstance(m, dict)]
live = json.loads(live_json) if source in ("live", "both") else []
if source == "both":
    seen = {(utc_minute(m.get("ts", "")), " ".join(str(m.get("text", "")).split())) for m in msgs if m.get("role") == "kam"}
    live = [m for m in live if (utc_minute(m.get("ts", "")), " ".join(str(m.get("text", "")).split())) not in seen]
msgs = msgs + live
msgs.sort(key=lambda m: utc_minute(m.get("ts", "")))
kam = [m for m in msgs if m.get("role") == "kam" and str(m.get("ts", "")).startswith(day)]

# ── SEAT FILTER (Tuesday's design, 2026-09-09, adopted whole) ────────────────
# Kam's panel records which TAB he typed into, in each message's `view` field.
# It has always been correct and NOTHING has ever read it — so both seats read
# one undifferentiated stream and each had to guess which of his words were
# theirs. **This seat guessed wrong on a load-bearing one: his 13:05 "will be
# going through the review as soon as its ready" is tagged `tuesday`, and this
# seat read it as an answer about SECUURA and rebuilt its afternoon around it.**
# The tag was on disk the whole time.
#
# Her two design constraints, both kept because both are the difference between
# a filter and a new blind spot:
#   1. PRINT THE FILTER AND THE SUPPRESSED COUNT. A seat reading 11 of 47 must
#      say so, or the next staleness incident is invisible in a NEW way. The
#      frame is stated ([[2026-09-07_a-census-complete-over-a-frame-that-is-not]]).
#   2. FAIL OPEN, NEVER CLOSED. A message with NO `view` — everything before
#      2026-09-08 12:42, and any the panel could not tag — is shown to BOTH
#      seats. **Silently dropping an untagged instruction from Kam is worse than
#      the problem this fixes.** Same for a view this code does not recognise.
# An unset WED_AGENT shows everything and says so: no seat, no filter, no guess.
def mine(m):
    v = str(m.get("view") or "").strip().lower()
    if not seat:            return True      # no seat -> no filtering at all
    if v in ("", "both"):   return True      # untagged / broadcast -> fail open
    if v not in ("wednesday", "tuesday", "friday"): return True   # unknown tag -> fail open (friday: third seat, 2026-09-23)
    return v == seat

shown = [m for m in kam if mine(m)]
hidden = len(kam) - len(shown)

def as_dt(ts):
    try: return datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00")).astimezone(datetime.timezone.utc)
    except Exception: return None
today = datetime.datetime.now().astimezone().strftime("%Y-%m-%d")
if mode == "unread":
    # Rows newer than the marker (the newest row a FULL read of today showed this seat). Never advances it.
    mark_raw = ""
    try: mark_raw = open(marker).read().strip()
    except OSError: pass
    mark = as_dt(mark_raw)
    if mark is None or mark_raw[:10] != day:
        print(f"UNREAD {len(shown)} — no full read of {day} is recorded for seat={seat or 'unset'}; run kam_rulings_today.sh")
        newer = shown
    else:
        newer = [m for m in shown if (as_dt(m.get("ts", "")) or mark) > mark]
        print(f"UNREAD {len(newer)} — rows newer than this seat's last full read ({mark_raw[11:19]})")
    for m in newer:
        text = " ".join(str(m.get("text", "")).split())
        if m.get("decrypt_error"): text = "[LIVE ROW NOT READABLE BY THIS SEAT — read it on the live board]"
        print(f"{str(m.get('ts', ''))[11:16]} [{m.get('source', 'local')}] | {text}")
    raise SystemExit(0)
if day == today and shown:
    # A full read of TODAY: record the newest row it showed (the watermark covers only what was displayed).
    newest_shown = max(shown, key=lambda m: as_dt(m.get("ts", "")) or datetime.datetime.min.replace(tzinfo=datetime.timezone.utc))
    try:
        os.makedirs(os.path.dirname(marker), exist_ok=True)
        tmp = marker + ".tmp"
        with open(tmp, "w") as fh: fh.write(str(newest_shown.get("ts", "")) + "\n")
        os.replace(tmp, marker)
    except OSError as e:
        print(f"# ⚠ could not record the read marker {marker}: {e}", file=sys.stderr)

if not seat:
    frame = "ALL views — WED_AGENT is unset, so nothing is filtered"
else:
    frame = f"view={seat}, plus untagged and broadcast"
print(f"# Kam's panel messages on {day} — VERBATIM, oldest first — source={source}. "
      f"Showing {len(shown)} of {len(kam)} ({frame}). Read every one before any card, brief or ruling.")
if hidden:
    print(f"# {hidden} message(s) addressed to the OTHER seat's tab are NOT shown. "
          f"They are that seat's to act on — but if one looks like yours, read it: "
          f"the tab records where he TYPED, and he has typed in the wrong one.")
for m in shown:
    ts = str(m.get("ts", ""))[11:16]
    v = str(m.get("view") or "").strip().lower()
    tag = "" if v == seat else f" [{v or 'untagged'}]"
    text = " ".join(str(m.get("text", "")).split())
    if m.get("decrypt_error"): text = f"[LIVE ROW NOT READABLE BY THIS SEAT — {m['decrypt_error']} — he wrote; read it on the live board]"
    print(f"{ts}{tag} [{m.get('source', 'local')}] | {text}")
print(f"# end — {len(shown)} shown, {hidden} withheld")

# Freshness line: ALWAYS printed, so a stale read can never look like a quiet one.
now = datetime.datetime.now().astimezone()
if source in ("live", "both"):
    newest_live = max((str(m.get("ts", "")) for m in live if m.get("ts")), default="")
    try: age = f"{(now - datetime.datetime.fromisoformat(newest_live)).total_seconds() / 60:.0f} min ago ({newest_live[11:19]})"
    except Exception: age = "none in the window"
    print(f"# FRESHNESS — LIVE board read at {now:%H:%M:%S} as seat={seat or 'unset'}: newest live Kam row in the window {age} · {len(live)} live rows fetched (this is the board itself, not a copy: nothing to pull)")
if source == "live":
    raise SystemExit(0)
newest = max((str(m.get("ts", "")) for m in msgs if m.get("ts") and m.get("source", "local") == "local"), default="")
mtime = datetime.datetime.fromtimestamp(os.path.getmtime(log)).astimezone()
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
print(f"# FRESHNESS — newest message in the LOCAL copy (chat_log.json): {age_txt} · file mtime {mtime:%H:%M:%S}")
if stale:
    print("#")
    print(f"# ⚠️  STALE-COPY WARNING: the newest message here is over {stale_min} minutes old.")
    print("#    This file does NOT update on its own. With two Wednesday seats, Kam's words arrive")
    print("#    only when the other seat pushes the log and THIS seat pulls. An empty tail may mean")
    print("#    'he said nothing' OR 'this copy has not caught up' — those are different facts.")
    print("#    Settle it before concluding he is quiet:")
    print("#      bash <this repo>/2_Project_Files/tools/safe_pull.sh   then re-run this script.")
    print("#      (never a hand-typed --autostash: it sweeps decisions.json and the chat streams; ledger w=3 2026-10-06)")
PY

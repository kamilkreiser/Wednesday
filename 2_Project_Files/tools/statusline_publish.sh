#!/bin/sh
# statusline_publish.sh — run the real statusline, then publish THIS SEAT'S weekly
# plan usage for the dashboard's agent chips (Kam, 2026-09-09 12:32:
# "add to the Wednesday toggle so it shows weeks usage % so its 'Wednesday - xx%'
#  and same for Tuesday").
#
# WHY A WRAPPER AND NOT AN EDIT TO THE STATUSLINE ITSELF.
# The first attempt (12:35) put the publish block inside
# 2_Project_Files/tools/statusline.sh. That file is a COPY: Launch_Wednesday.command
# refreshes it from "$DEVMASTER/Setup and System/statusline.sh" at every boot, and
# points settings.local.json at the shared original in preference to it. So the
# feature lived for ninety seconds and the next launch (12:37) deleted it — with the
# published figure frozen at the moment the writer died. Editing the shared original
# instead is not available: it is outside this folder and shared with every client's
# launcher (hard rule 1).
# A wrapper is the seam that survives both facts. The shared script stays the single
# source of the statusline itself and its improvements still flow through untouched;
# this file only adds the publish, and lives where nothing overwrites it.
#
# HONESTY. The number reaches this script on stdin from Claude Code and exists
# nowhere else, so a seat can only ever publish its OWN. One writer per file — the
# shape that ended the chat_log conflicts on 2026-09-08. A seat that is not running
# stops writing, its file ages, and the page renders the age rather than pretending
# the figure is current (WED-73: rendered from written state, never faked).
#
# THE STATUSLINE COMES FIRST, ALWAYS. Publishing is best-effort and strictly after
# the line is printed: a fault here must never cost Kam his context reading, which is
# the only context instrument this fleet has (2026-09-02, a seat died at 100%).
set -u

LABEL="${1:-[session]}"

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" 2>/dev/null && pwd -P) || SCRIPT_DIR=""
PROJECT_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/../.." 2>/dev/null && pwd -P) || PROJECT_DIR=""

# The base statusline: the shared DevMASTER helper when mounted, else this tree's
# refreshed copy, so the wrapper degrades to a working statusline on any machine.
BASE=""
for c in "${DEVMASTER:-/Volumes/DevMASTER}/Setup and System/statusline.sh" \
         "$SCRIPT_DIR/statusline.sh"; do
  [ -f "$c" ] && { BASE="$c"; break; }
done

input=$(cat)

# ── 1. the statusline, unchanged ────────────────────────────────────────────
if [ -n "$BASE" ]; then
  printf '%s' "$input" | sh "$BASE" "$LABEL"
else
  printf '%s\n' "$LABEL"
fi

# ── 2. publish this seat's own figure ───────────────────────────────────────
# Everything below is best-effort. Errors go to a log rather than /dev/null
# (2026-08-06_never-discard-stderr) and never to stdout, which belongs to the
# statusline.
LOG="$PROJECT_DIR/2_Project_Files/logs/statusline_publish.log"
# The directory is made HERE, before anything redirects into the log. Creating it
# inside _fail() is too late: a `2>>"$LOG"` on a command whose parent directory does
# not exist makes the REDIRECTION fail, so the command never runs and its output is
# empty — the publish then does nothing and reports nothing. Found by running this
# script rather than by reading it (2026-08-06_exercise-mechanisms-before-arming).
mkdir -p "$PROJECT_DIR/2_Project_Files/logs" 2>/dev/null || LOG=/dev/null

_fail() { printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$1" >> "$LOG" 2>/dev/null; }

# Identity comes from the LAUNCHER, never from the hostname: argument 2, which the
# launcher writes into the statusLine command itself, then $WED_AGENT. Both are the
# launcher's word; the argument is preferred only because it survives an environment
# this subprocess does not control. A seat that guesses its own client is the exact
# failure the two-agent split exists to prevent, so there is no hostname fallback —
# an unknown seat publishes nothing and says so in the log.
agent="${2:-${WED_AGENT:-}}"
case "$agent" in
  wednesday|tuesday) ;;
  "") _fail "no seat name (arg 2 or \$WED_AGENT); published nothing"; exit 0 ;;
  *)  _fail "seat name '$agent' is neither wednesday nor tuesday; published nothing"; exit 0 ;;
esac

command -v jq >/dev/null 2>&1 || { _fail "jq absent; published nothing"; exit 0; }

pct=$(printf '%s' "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty' 2>>"$LOG")
[ -n "$pct" ] || exit 0          # no usage data this turn — write nothing, say nothing

pct_fmt=$(printf '%.0f' "$pct" 2>/dev/null) || { _fail "unparseable pct '$pct'"; exit 0; }

# resets_at is EPOCH SECONDS, not an ISO string — the shared statusline subtracts it
# from `date +%s` directly, and that script has been right about this payload for
# months. Parsing it as ISO here (the first attempt) produced a shell arithmetic
# error on a synthetic fixture and would have produced a silently blank countdown on
# the real one. The countdown is computed the same way as the statusline's on purpose:
# one interpretation of the field, so the chip's tooltip cannot disagree with the line
# Kam is reading.
resets=$(printf '%s' "$input" | jq -r '.rate_limits.seven_day.resets_at // empty' 2>>"$LOG")
countdown=""
case "$resets" in
  "") ;;
  *[!0-9]*) _fail "resets_at='$resets' is not epoch seconds; countdown left empty" ;;
  *)
    now=$(date -u +%s)
    if [ "$resets" -gt "$now" ]; then
      left=$((resets - now)); d=$((left / 86400)); h=$(((left % 86400) / 3600)); m=$(((left % 3600) / 60))
      if [ "$d" -gt 0 ]; then countdown="${d}d ${h}h"
      elif [ "$h" -gt 0 ]; then countdown="${h}h ${m}m"
      else countdown="${m}m"; fi
    else
      countdown="renews now"
    fi ;;
esac

dir="$PROJECT_DIR/0_Brain/dashboard/data"
[ -d "$dir" ] || { _fail "data dir absent at $dir"; exit 0; }

f="$dir/usage_${agent}.json"

# WRITE ONLY WHEN IT SAYS SOMETHING NEW — the percentage changed, or the file has
# aged past the heartbeat. The statusline renders many times a minute; rewriting a
# fresh timestamp each time makes this a permanently-dirty tracked file, which is
# what made the first rebase of this very change fail. The heartbeat is well inside
# the page's 15-minute staleness threshold, so a running seat never falsely reads as
# stale, and a stopped seat's file ages exactly as it should.
HEARTBEAT_S=300
if [ -f "$f" ] && command -v python3 >/dev/null 2>&1; then
  skip=$(python3 - "$f" "$pct_fmt" "$HEARTBEAT_S" <<'PY' 2>>"$LOG"
import json, sys, datetime
path, pct, hb = sys.argv[1], sys.argv[2], int(sys.argv[3])
try:
    d = json.load(open(path))
    if str(d.get("pct")) != str(pct):
        print("no")                      # the number moved — publish it
    else:
        # timezone-aware on purpose: utcnow() is deprecated and warns on 3.12+,
        # and every such warning would land in this script's log on every render.
        ts = datetime.datetime.strptime(d["ts"], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=datetime.timezone.utc)
        age = (datetime.datetime.now(datetime.timezone.utc) - ts).total_seconds()
        print("yes" if 0 <= age < hb else "no")
except Exception:
    print("no")                          # unreadable or malformed — rewrite it
PY
)
  [ "$skip" = "yes" ] && exit 0
fi

if printf '{"agent":"%s","pct":%s,"resets_in":"%s","ts":"%s"}\n' \
     "$agent" "$pct_fmt" "$countdown" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$f.tmp" 2>>"$LOG"; then
  mv -f "$f.tmp" "$f" 2>>"$LOG" || { _fail "mv into $f failed"; rm -f "$f.tmp" 2>/dev/null; }
else
  _fail "write to $f.tmp failed"; rm -f "$f.tmp" 2>/dev/null
fi
exit 0

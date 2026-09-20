#!/bin/bash
# pane_wake_check.sh — decide whether a fleet pane needs a TAP, from a MEASUREMENT.
#
# WHY THIS EXISTS (enforcement, not advice). On 2026-09-20/21 one seat composed this
# check inline six times and it failed FOUR different ways in a single session:
#   1. FALSE NEGATIVE: `tail -6 | grep -cE '✻|✳|✽|✢'` returned 0 for the seat's OWN
#      pane while that pane was mid-turn. The glyph was outside the last 6 lines.
#   2. FALSE POSITIVE: the same pattern returned 1 on a STOPPED pane, because the
#      COMPLETED-turn marker ("✻ Cogitated for 6m 47s · done 10:48 pm") uses the same
#      glyph as the live one. A count cannot tell those apart.
#   3. SELF-MATCH: `ps | grep -c <pattern>` counted the checking command's OWN command
#      line, so an empty floor read as "1 process, wake pending".
#   4. TRUNCATION: classifying on `cmd[:75]` hid the word "jest" further along a live
#      command line, so a RUNNING full-suite measurement read as "no wake — tap
#      required". Tapping would have interrupted the measurement the coordinator had
#      itself commissioned. A truncation is a frame.
#
# THE TWO QUESTIONS IT ANSWERS, because one is not enough:
#   (a) is a WAKE pending — a job that will EXIT and re-invoke the agent?
#   (b) does the work the agent has LEFT depend on that job?
# (b) is a judgement the caller makes; this script measures (a) and prints everything
# needed for (b). A long-running listener is NOT a wake: it never exits.
#
# HONEST LIMIT, stated because a check that hides its weakness is worse than none:
# the PANE half is heuristic (UI strings change). The PROCESS half is the discriminator.
# The verdict is driven by the process half; the pane is printed, never trusted.
#
# Usage:
#   pane_wake_check.sh <pane-id> <path-or-pattern-identifying-the-agent's-jobs>
#   pane_wake_check.sh --selftest
# Exit: 0 wake pending (do NOT tap) · 3 no wake (tap required) · 2 usage
set -u

# Long-running listeners: present == not a wake. Extend deliberately, with a reason.
NEVER_EXITS_RE='backend/server\.js|panel_sync|wake_watch|fleet-monitor|http-server'

measure_jobs() {   # $1 = pattern; prints "pid<TAB>elapsed<TAB>class<TAB>cmd", NEVER truncated
  local pat="$1" self=$$ ppid_self=$PPID
  ps -eo pid=,etime=,command= | while IFS= read -r line; do
    local pid et cmd
    pid=${line%% *}; line=${line#"$pid"}; line=${line# }
    et=${line%% *};  cmd=${line#"$et"};  cmd=${cmd# }
    case "$pid" in "$self"|"$ppid_self") continue ;; esac
    case "$cmd" in
      *"pane_wake_check"*) continue ;;                 # arm 3: never count myself
      *"ps -eo"*)          continue ;;
      *"$pat"*)            ;;
      *)                   continue ;;
    esac
    if printf '%s' "$cmd" | /usr/bin/grep -qE "$NEVER_EXITS_RE"; then
      printf '%s\t%s\t%s\t%s\n' "$pid" "$et" "LISTENER-never-exits" "$cmd"
    else
      printf '%s\t%s\t%s\t%s\n' "$pid" "$et" "JOB-exits-WAKE" "$cmd"
    fi
  done
}

if [ "${1:-}" = "--selftest" ]; then
  fail=0
  # ARM 3 — self-match: my own invocation carries the pattern and must NOT be counted.
  out=$(measure_jobs "pane_wake_check.sh"); n=$(printf '%s' "$out" | /usr/bin/grep -c . )
  [ "$n" -eq 0 ] && echo "PASS arm3 self-match excluded" || { echo "FAIL arm3: counted itself ($n)"; fail=1; }
  # ARM 4 — truncation: a marker late in a long command line must still classify.
  long="node /very/long/path$(printf 'x%.0s' $(seq 1 200))/node_modules/.bin/jest --maxWorkers=2"
  if printf '%s' "$long" | /usr/bin/grep -qE "$NEVER_EXITS_RE"; then echo "FAIL arm4: jest misread as listener"; fail=1
  else echo "PASS arm4 long line still classifies as a JOB (no truncation)"; fi
  # ARM 4b — a listener must classify as a listener even on a long line.
  srv="/opt/homebrew/bin/node /a/very/long/path$(printf 'y%.0s' $(seq 1 200))/backend/server.js"
  if printf '%s' "$srv" | /usr/bin/grep -qE "$NEVER_EXITS_RE"; then echo "PASS arm4b listener classified as never-exits"
  else echo "FAIL arm4b: listener misread as a job"; fail=1; fi
  # ARM 1+2 — the glyph cannot discriminate: the SAME glyph appears live and done.
  live='✻ Cascading… (3m 45s · ↓ 14.2k tokens)'
  done_='✻ Cogitated for 6m 47s · done 10:48 pm'
  gl=$(printf '%s\n%s\n' "$live" "$done_" | /usr/bin/grep -cE '✻|✳|✽|✢')
  if [ "$gl" -eq 2 ]; then echo "PASS arm1+2 glyph matches BOTH live and done — proven unusable as a verdict"
  else echo "FAIL arm1+2: glyph control did not reproduce ($gl)"; fail=1; fi
  [ "$fail" -eq 0 ] && { echo "SELFTEST: all arms PASS"; exit 0; } || { echo "SELFTEST: FAILURES"; exit 1; }
fi

[ $# -ge 2 ] || { echo "usage: pane_wake_check.sh <pane-id> <pattern>   |   --selftest" >&2; exit 2; }
PANE="$1"; PAT="$2"

echo "== PANE $PANE (heuristic — printed, never trusted) =="
tmux capture-pane -p -t "$PANE" 2>/dev/null | /usr/bin/grep -v '^[[:space:]]*$' | tail -3 | sed 's/^/   /'
echo
echo "== JOBS matching '$PAT' (untruncated, own process excluded) =="
JOBS=$(measure_jobs "$PAT")
if [ -z "$JOBS" ]; then echo "   (none)"; else printf '%s\n' "$JOBS" | while IFS=$'\t' read -r p e k c; do
  printf '   pid %-7s %-9s %-21s %s\n' "$p" "$e" "$k" "$(printf '%s' "$c" | cut -c1-120)"
done; fi
echo
WAKES=$(printf '%s' "$JOBS" | /usr/bin/grep -c 'JOB-exits-WAKE')
if [ "$WAKES" -gt 0 ]; then
  echo "VERDICT: WAKE PENDING ($WAKES job(s) will exit and re-invoke it) — mail suffices, DO NOT TAP."
  echo "         Caller must still ask: does the work it has LEFT depend on this job? If NOT, tap anyway."
  exit 0
else
  echo "VERDICT: NO WAKE — nothing here exits. A tap is required, or the seat sits until a watcher notices."
  exit 3
fi

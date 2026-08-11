#!/bin/bash
# wake_watch.sh — Wednesday's fleet wake-up tripwire (built 2026-08-05 after
# Kam caught an in-pane plan-confirmation sitting unseen ~10 min; rewritten
# same night for macOS bash 3.2 — no associative arrays).
#
# Runs as a BACKGROUND TASK from Wednesday's own session: polls every 60s and
# EXITS (task-notification wakes Wednesday) when either:
#   (a) MAIL: a new message lands in wednesday-agent@ (timestamp > baseline), or
#   (b) PANE: an agent pane (not wednesday/fleet-monitor) sits idle at a
#       prompt with unchanged content for STABLE_N consecutive samples, or
#   (c) CTX: any Claude pane's statusline ctx% crosses a working-rhythm §2
#       threshold — 50% admission gate + checkpoint, 65% mechanical tails
#       only (added 2026-08-10, WED-84 rotation build; taps are questions
#       about task state, not wrap commands — sessions rotate at task
#       boundaries). INCLUDES wednesday's own pane — she is read
#       from outside like everyone else. Each threshold fires ONCE per pane
#       per session-generation: markers persist in cockpit/state/ (NOT this
#       run's temp dir) keyed by pane_id+pane_pid, so runner re-arms never
#       re-fire but a fresh session in the same pane starts clean.
# Pane state lives in files under a per-run temp dir (bash-3.2-safe).
# The background runner caps runs at 10 min, so this re-arms on that heartbeat.
#
# Usage: wake_watch.sh <baseline-iso-ts> [stable_n] [interval_s]
set -u
BASELINE="${1:?usage: wake_watch.sh <baseline-iso-ts> [stable_n] [interval_s]}"
STABLE_N="${2:-3}"
INTERVAL="${3:-60}"
ENVF="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)/4_Credentials/.env"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"
STATE_DIR="$(mktemp -d /tmp/wake_watch.XXXXXX)"
trap 'rm -rf "$STATE_DIR"' EXIT
# Test hook (rotation build 2026-08-10): point pane checks at another tmux
# session so fire-path tests never touch the live fleet. Production = fleet.
FLEET="${WAKE_WATCH_TMUX_SESSION:-fleet}:0"
# Persistent ctx-threshold markers (survive re-arm; per-generation, see (c))
CTX_STATE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/state"
mkdir -p "$CTX_STATE"
# markers older than 3 days belong to dead pane generations — prune quietly
find "$CTX_STATE" -name 'ctx_fired_*' -mtime +3 -delete 2>/dev/null
end=$((SECONDS + 14400))
while [ $SECONDS -lt $end ]; do
  # (a) mail tripwire
  # Latest INBOUND message only — own outbound copies (from wednesday-agent@)
  # must never fire the tripwire (false wake 2026-08-05 21:4x).
  ts=$(set -a; . "$ENVF" 2>/dev/null; set +a; curl -s -m 10 \
    "https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages?limit=10" \
    -H "Authorization: Bearer ${AGENTMAIL_API_KEY:-}" \
    | python3 -c "
import json,sys
ms=[m for m in json.load(sys.stdin).get('messages',[]) if 'wednesday-agent@' not in str(m.get('from',''))]
print(ms[0].get('timestamp','')[:16] if ms else '')" 2>/dev/null)
  if [ -n "$ts" ] && [[ "$ts" > "$BASELINE" ]]; then
    echo "WAKE: new mail at $ts (baseline $BASELINE)"; exit 0
  fi
  # (a2) dashboard-chat tripwire — Kam's messages in chat_log.json are real
  # input with NO other watcher (added 2026-08-10 after his 08:45 message sat
  # unread 3h; ledger row same day). Newest role=="kam" ts, converted to UTC
  # minute-precision to match BASELINE's format.
  cts=$(python3 -c "
import json,datetime,sys
try:
    log=json.load(open('$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)/0_Brain/dashboard/data/chat_log.json'))
    ks=[m for m in log if m.get('role')=='kam' and m.get('ts')]
    if not ks: print(''); sys.exit()
    t=datetime.datetime.fromisoformat(ks[-1]['ts']).astimezone(datetime.timezone.utc)
    print(t.strftime('%Y-%m-%dT%H:%M'))
except Exception: print('')" 2>/dev/null)
  if [ -n "$cts" ] && [[ "$cts" > "$BASELINE" ]]; then
    echo "WAKE: new dashboard-chat message from Kam at $cts UTC (baseline $BASELINE)"; exit 0
  fi
  # (b) pane idle-at-prompt tripwire
  "$TMUX_BIN" list-panes -t "$FLEET" -F '#{pane_id}|#{@cockpit_name}' 2>/dev/null | \
  while IFS='|' read -r pid name; do
    case "$name" in wednesday|fleet-monitor|'') continue;; esac
    key=$(printf '%s' "$pid" | tr -c 'A-Za-z0-9' '_')
    tail=$("$TMUX_BIN" capture-pane -t "$pid" -p 2>/dev/null | grep -v '^$' | tail -20)
    h=$(printf '%s' "$tail" | shasum | cut -c1-12)
    hf="$STATE_DIR/h_$key"; cf="$STATE_DIR/c_$key"
    prev=$(cat "$hf" 2>/dev/null || echo none)
    cnt=$(cat "$cf" 2>/dev/null || echo 0)
    # A pane idle at its prompt but with a RUNNING background shell (Claude
    # status line shows "N shell(s)") is working (e.g. watching CI), not
    # waiting on Wednesday — its QUESTION mail / next turn is the real signal.
    # (Refined 2026-08-05 after two identical fires on a CI-watching agent.)
    # Ghost-text-aware prompt read (added 2026-08-10 consolidation: Vision
    # idled 90 min with 5 unseen mails because its prompt held a dim machine
    # SUGGESTION and the plain-capture test below saw a non-empty prompt).
    # Capture with -e, strip SGR-2 (dim) spans — the pane_prompt_check.sh
    # discriminator: dim = suggestion, nobody typed it — then strip all SGR
    # and NBSP. A prompt that is empty-after-ghost-removal IS idle. TYPED
    # unsent text (not dim) still deliberately reads as not-idle.
    pline=$("$TMUX_BIN" capture-pane -t "$pid" -p -e 2>/dev/null | grep -a '❯' | tail -1 | \
      LC_ALL=C perl -pe 's/\x1b\[2m.*?(?=\x1b|$)//g; s/\x1b\[[0-9;]*m//g; s/\xc2\xa0/ /g' 2>/dev/null)
    # Busy-detection covers EVERY kind of Claude background work, not just
    # shells (widened 2026-08-11: Vision was polling an ACS throttle window via
    # a MONITOR — statusline "· 1 monitor" — and the shell-only regex read a
    # working agent as idle. Same failure shape as the ghost-text blind spot:
    # the enforcement was scoped narrower than the rule it encodes). Plural
    # tolerant; add new indicators here the day they appear.
    # DELIBERATELY EXCLUDES "agent": the cockpit footer always renders a pane
    # count ("← 3 agents"). Matching it would make EVERY pane read busy forever
    # and silently disable this tripwire permanently — a watcher that can never
    # fire. Caught by my own test asserting the wrong expectation, 2026-08-11.
    if printf '%s' "$tail" | grep -qE 'shell still running|· [0-9]+ (shell|monitor|task)s?([^A-Za-z]|$)'; then
      cnt=0
    elif printf '%s\n' "$pline" | grep -qE '^❯[[:space:]]*$' || printf '%s' "$tail" | grep -qE 'Pick or adjust'; then
      if [ "$prev" = "$h" ]; then cnt=$((cnt + 1)); else cnt=1; fi
    else
      cnt=0
    fi
    printf '%s' "$h" > "$hf"; printf '%s' "$cnt" > "$cf"
    if [ "$cnt" -ge "$STABLE_N" ]; then
      echo "WAKE: pane '$name' ($pid) idle at prompt ~$((STABLE_N * INTERVAL / 60)) min — likely waiting on Wednesday" > "$STATE_DIR/fired"
    fi
  done
  if [ -f "$STATE_DIR/fired" ]; then cat "$STATE_DIR/fired"; exit 0; fi
  # (c) context-saturation tripwire (working-rhythm §2 — Kam's numbers,
  # adopted 2026-08-10): parse each pane's Claude statusline "ctx:NN%" from a
  # read-only capture; the LAST match in the visible pane is the statusline
  # (it renders below the transcript). "ctx:-" (no API call yet) simply
  # doesn't match — quiet. fleet-monitor has no statusline — skipped.
  # One wake per cycle: first pane over an unfired threshold wins; any other
  # crossing fires on the next 60s sample.
  "$TMUX_BIN" list-panes -t "$FLEET" -F '#{pane_id}|#{@cockpit_name}|#{pane_pid}' 2>/dev/null | \
  while IFS='|' read -r pid name ppid; do
    case "$name" in fleet-monitor|'') continue;; esac
    pct=$("$TMUX_BIN" capture-pane -t "$pid" -p 2>/dev/null | grep -oE 'ctx:[0-9]+%' | tail -1 | tr -dc '0-9')
    [ -n "$pct" ] || continue
    gen=$(printf '%s_%s' "$pid" "$ppid" | tr -c 'A-Za-z0-9' '_')
    if [ "$pct" -ge 65 ] 2>/dev/null; then
      if [ ! -f "$CTX_STATE/ctx_fired_${gen}_65" ] && [ ! -f "$STATE_DIR/ctx_wake" ]; then
        touch "$CTX_STATE/ctx_fired_${gen}_65" "$CTX_STATE/ctx_fired_${gen}_50"
        echo "WAKE: pane '$name' ctx at ${pct}% — mechanical tails only, then handover (rhythm §2)" > "$STATE_DIR/ctx_wake"
      fi
    elif [ "$pct" -ge 50 ] 2>/dev/null; then
      if [ ! -f "$CTX_STATE/ctx_fired_${gen}_50" ] && [ ! -f "$STATE_DIR/ctx_wake" ]; then
        touch "$CTX_STATE/ctx_fired_${gen}_50"
        echo "WAKE: pane '$name' ctx at ${pct}% — checkpoint: finish the current task, START nothing new that won't fit the budget (rhythm §2)" > "$STATE_DIR/ctx_wake"
      fi
    fi
  done
  if [ -f "$STATE_DIR/ctx_wake" ]; then cat "$STATE_DIR/ctx_wake"; exit 0; fi
  sleep "$INTERVAL"
done
echo "WAKE: 4h max runtime reached with no tripwire — re-arm from the session"
exit 0

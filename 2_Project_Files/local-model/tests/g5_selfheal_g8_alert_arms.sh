#!/bin/bash
# Arms for the 2026-09-16 night_run additions: G5 SELF-HEAL and the G8 gate-refusal alert.
#
# WHY: on 2026-09-16 the ollama server died before 12:24 and G5 refused SIX consecutive cycles into
# night/log/, which nobody reads — Ornith sat idle 09:58 -> 13:32 on the day Kam twice said never to
# idle. Two fixes: G5 restarts the server itself (a dead LOCAL server is not a safety boundary, and
# removing a failure mode beats detecting it), and G8 escalates a gate that has been refusing for
# NIGHT_GATE_ALERT_MIN minutes to Kam's panel, because a refusal nobody reads is indistinguishable
# from working.
#
# Every arm names what would make it FAIL. Arms 2-5 drive the gate with a bogus NIGHT_MODEL, so they
# are deterministic and cannot consume a queued ticket; arm 1 is the only one that touches the real
# server, and it carries the control that proves it measured the self-heal rather than the world.
#
# Usage: bash 2_Project_Files/local-model/tests/g5_selfheal_g8_alert_arms.sh
set -u
LM="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN="$LM/night/night_run.sh"; LOGDIR="$LM/night/log"
MARK="$LOGDIR/.gate_refused_since"; ALERTED="$LOGDIR/.gate_refused_alerted"
Q="$LOGDIR/_quarantine_g8"; mkdir -p "$Q"
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); printf '  PASS  %s\n' "$1"; }
bad() { FAIL=$((FAIL+1)); printf '  FAIL  %s\n' "$1"; }
# Markers are MOVED, never deleted (Kam 2026-08-26) — here too, not only in the code under test.
clear_markers() { for m in "$MARK" "$ALERTED"; do [ -f "$m" ] && mv "$m" "$Q/$(basename "$m").arms.$(date +%s%N)"; done; :; }
bogus() { NIGHT_G5_SELFHEAL=0 NIGHT_MODEL=doesnotexist:1b NIGHT_GATE_ALERT_DRY=1 bash "$RUN" 2>&1; }
serving() { curl -sS -m 5 http://127.0.0.1:11434/api/tags 2>/dev/null | /usr/bin/grep -q '"ornith:35b"'; }

echo "=== ARM 1 — G5 SELF-HEAL: the server is genuinely DOWN and the gate brings it back ==="
P="$(lsof -nP -iTCP:11434 -sTCP:LISTEN -t 2>/dev/null | head -1)"
if [ -n "$P" ] && [ "$P" != 1 ]; then kill "$P"; sleep 3; fi
if serving; then
  bad "arm 1 could not stop the server — NOT RUN (this arm proves nothing today)"
else
  clear_markers
  if bash "$RUN" 2>&1 | /usr/bin/grep -q -i 'was down — start_ollama.sh brought it back' && serving; then
    ok "arm 1 the gate self-healed and ornith:35b is served again"
  else
    bad "arm 1 no SELF-HEALED line, or the server is still down"
  fi
  # CONTROL — the same condition with the self-heal off must REFUSE, or arm 1 measured nothing.
  P="$(lsof -nP -iTCP:11434 -sTCP:LISTEN -t 2>/dev/null | head -1)"
  [ -n "$P" ] && [ "$P" != 1 ] && { kill "$P"; sleep 3; }
  clear_markers
  if NIGHT_G5_SELFHEAL=0 bash "$RUN" 2>&1 | /usr/bin/grep -q -i 'gate g5 ollama.*refuse'; then
    ok "arm 1 CONTROL with NIGHT_G5_SELFHEAL=0 the same condition refuses"
  else
    bad "arm 1 CONTROL did not refuse — arm 1 is not a measurement of the self-heal"
  fi
  bash "$LM/start_ollama.sh" > /dev/null 2>&1
  serving && echo "  (server restored for the remaining arms)"
fi

echo "=== ARM 2 — G8 stamps a marker on the first refusal and stays QUIET inside the window ==="
clear_markers
OUT2="$(bogus)"
if [ -f "$MARK" ] && [ ! -f "$ALERTED" ] && ! printf '%s' "$OUT2" | /usr/bin/grep -q -i 'g8 gate alert'; then
  ok "arm 2 marker stamped ($(cat "$MARK")), no alert inside the window"
else
  bad "arm 2 marker=$([ -f "$MARK" ] && echo yes || echo no) alerted=$([ -f "$ALERTED" ] && echo yes || echo no)"
fi

echo "=== ARM 3 — G8 ALERTS once the same gate has been refusing past the window ==="
printf '%s %s\n' "$(( $(date +%s) - 3600 ))" "G5-ollama" > "$MARK"
[ -f "$ALERTED" ] && mv "$ALERTED" "$Q/$(basename "$ALERTED").arms.$(date +%s%N)"
if bogus | /usr/bin/grep -q -i 'g8 gate alert: g5-ollama has refused for 6[0-9] min' && [ -f "$ALERTED" ]; then
  ok "arm 3 alerted at 60 min and wrote the alerted marker"
else
  bad "arm 3 no alert line at 60 min, or no alerted marker"
fi

echo "=== ARM 4 — rate limit: the next refusal is silent (control: arm 3 printed exactly one) ==="
N="$(bogus | /usr/bin/grep -i -c 'g8 gate alert')"
if [ "$N" -eq 0 ]; then ok "arm 4 zero further alerts while the alerted marker stands"
else bad "arm 4 alerted again ($N lines) — the rate limit does not hold"; fi

echo "=== ARM 5 — a passing gate set CLEARS both markers, by MOVE not delete ==="
printf '%s %s\n' "$(( $(date +%s) - 3600 ))" "G5-ollama" > "$MARK"; : > "$ALERTED"
BEFORE="$(ls -a "$Q" | /usr/bin/grep -c 'gate_refused')"
bash "$RUN" > /dev/null 2>&1
AFTER="$(ls -a "$Q" | /usr/bin/grep -c 'gate_refused')"
if [ ! -f "$MARK" ] && [ ! -f "$ALERTED" ] && [ "$AFTER" -gt "$BEFORE" ]; then
  ok "arm 5 both markers cleared and the quarantine grew $BEFORE -> $AFTER (moved, not deleted)"
else
  bad "arm 5 mark=$([ -f "$MARK" ] && echo yes || echo no) alerted=$([ -f "$ALERTED" ] && echo yes || echo no) quarantine $BEFORE -> $AFTER"
fi

printf '\nARMS: %s passed, %s failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]

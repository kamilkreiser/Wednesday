#!/bin/bash
# pane_close.sh — close a cockpit pane ONLY when no surface dies with it.
#
# WHY THIS EXISTS (enforcement, not advice): ledger w=2, 2026-09-05. The 09-03
# lesson says a listener survives a pane close only if the listener AND its
# immediate parent both have tty `??`. Twice the check was run by hand and once
# the parent half was dropped: closing S33's pane killed the 3111 surface that
# read `??` on the listener alone. A two-part check done by hand loses a part,
# so the check is in the path now.
#
# HARDENED 2026-09-05 11:1x (ledger w=3 — the guard itself let two listeners die).
# Closing the retired QA pane %11 moved the listener count 24 -> 22 with NO
# refusal. Two holes, both of the check-that-cannot-fail family, in the tool
# built that morning to enforce the check:
#   (a) an UNRESOLVABLE pane name left PTTY empty and the guard passed
#       vacuously — `tmux display` printed its error, returned 0, and every
#       comparison ran against "". Now: an empty tty is a hard refusal.
#   (b) it walked ONE parent level, so a listener two or more levels below the
#       pane's shell was invisible to it. Now: the FULL ancestor chain is
#       walked to pid 1, and the process SESSION id is compared as well — which
#       is what the 09-03 lesson actually names (`ps -o sess,tty`). A session
#       match is the authoritative test; the tty walk is belt and braces.
#
# TYPED-UNSENT GATE (2026-09-17, ledger row 2026-09-17 "TYPED, UNSENT"): Wednesday ran
# `pane_prompt_check.sh %25`, which printed `⚠ TYPED, UNSENT (a human wrote this — flag
# it, do NOT act) :: do`, and chained `pane_close.sh %25` in the same call. The close ran
# and a line Kam (or his dictation tool) had typed was lost unread. Lessons:
# 2026-08-17_check-the-refusal-before-the-kill, 2026-08-05_kam-types-into-panes.
# Now this script runs the detector ITSELF (pane_prompt_check.sh beside it — its logic
# is NOT re-implemented here, only its verdict line is parsed) before any kill:
#   TYPED-UNSENT        -> REFUSED rc 7, the typed line printed; --typed-ok overrides
#   SUGGESTION / empty  -> proceeds as before
#   MODAL PROMPT        -> proceeds as before (the detector says nobody typed it)
#   detector failed     -> REFUSED rc 8 (non-zero rc, pane gone, or a verdict line this
#                          script does not recognise — fail CLOSED; a reworded detector
#                          blocks closes until this parser is updated, by design)
#
# Usage: pane_close.sh <pane-id-or-name> [port ...] [--typed-ok]
#   Ports named are curled before and after. --typed-ok (anywhere in the args) closes a
#   pane holding a TYPED-UNSENT line — only after the line was read and relayed to Kam.
# Exit: 0 closed · 5 REFUSED (a listener would die with the pane) · 6 REFUSED (caller's own
#       pane or the coordinator's pane) · 7 REFUSED (a human-typed, unsent line is at the
#       pane's prompt) · 8 REFUSED (the typed-line detector failed — fail closed) · 2 usage /
#       unresolvable pane / kill-pane failed · 127 no pane argument (bash ${1:?}).
#       Every call logged to logs/pane_close.log.
set -u
TYPED_OK=0; ARGS=()
for a in "$@"; do case "$a" in --typed-ok) TYPED_OK=1 ;; *) ARGS+=("$a") ;; esac; done
set -- "${ARGS[@]+"${ARGS[@]}"}"   # bash 3.2 + set -u: a bare "${ARGS[@]}" on an empty array is an error
PANE="${1:?usage: pane_close.sh <pane> [port ...] [--typed-ok]}"; shift || true
# (0) 2026-10-18 16:4x (Tuesday s116): `pane_close.sh --help` reached `tmux display -t --help`, tmux's
#     loose target matching resolved it to a LIVE QA gate's pane (%60), and only the listener check
#     stopped the close. The pane argument must be an exact %N id or an exact @cockpit_name, never
#     anything tmux has to guess at. Refuse before any tmux call.
case "$PANE" in
  -*) echo "pane_close: REFUSED — '$PANE' looks like an option, not a pane (usage: pane_close.sh <%N | exact cockpit name> [port ...] [--typed-ok]); nothing was closed" >&2; exit 2 ;;
  %[0-9]*) case "${PANE#%}" in *[!0-9]*) echo "pane_close: REFUSED — '$PANE' is not a %N pane id; nothing was closed" >&2; exit 2 ;; esac ;;
  *) tmux list-panes -a -F '#{@cockpit_name}' 2>/dev/null | /usr/bin/grep -qxF -- "$PANE" \
       || { echo "pane_close: REFUSED — no pane has @cockpit_name exactly '$PANE' (use the %ID from tmux list-panes); nothing was closed" >&2; exit 2; } ;;
esac

PTTY="$(tmux display -p -t "$PANE" '#{pane_tty}' 2>/dev/null)"
PPID_PANE="$(tmux display -p -t "$PANE" '#{pane_pid}' 2>/dev/null)"
# (a) an unresolvable pane must NEVER reach the comparisons as an empty string.
[ -n "$PTTY" ] || { echo "pane_close: REFUSED — pane '$PANE' did not resolve to a tty (use the %ID from tmux list-panes; a name that does not resolve would make every check below vacuous)" >&2; exit 2; }
SHORT="${PTTY#/dev/}"
# SELF-GUARD (2026-09-05 13:2x): the 11:06 coordinator seat VANISHED between 11:15
# and 11:29 while it was exercising this very tool (pane_close.sh.pre-1115-sess is
# its backup; no note line, no log line survived). Cause unproven — but a kill-pane
# tool that will take its caller's own pane, or the coordinator's, is a blast
# radius nobody should have to remember. Both are refused here (rc 6), and every
# invocation now leaves a line in logs/pane_close.log so the next post-mortem has
# evidence instead of a guess.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; PCLOG="$HERE/logs/pane_close.log"; mkdir -p "$HERE/logs"
TARGET_ID="$(tmux display -p -t "$PANE" '#{pane_id}' 2>/dev/null)"
TARGET_NAME="$(tmux display -p -t "$PANE" '#{@cockpit_name}' 2>/dev/null)"
echo "$(date '+%Y-%m-%d %H:%M:%S') invoked: target=$PANE id=$TARGET_ID name=${TARGET_NAME:--} tty=$PTTY caller_pane=${TMUX_PANE:--} ports=[$*] typed_ok=$TYPED_OK" >> "$PCLOG"
if [ -n "${TMUX_PANE:-}" ] && [ "$TARGET_ID" = "$TMUX_PANE" ]; then
  echo "pane_close: REFUSED — $PANE ($TARGET_ID) is the CALLER's own pane" >&2
  echo "$(date '+%Y-%m-%d %H:%M:%S') REFUSED rc6: target is the caller's own pane" >> "$PCLOG"; exit 6
fi
if [ "$TARGET_NAME" = "wednesday" ]; then
  echo "pane_close: REFUSED — $PANE ($TARGET_ID) is the coordinator's pane (@cockpit_name=wednesday); rotate it with wednesday_rotate.sh, never close it" >&2
  echo "$(date '+%Y-%m-%d %H:%M:%S') REFUSED rc6: target is the wednesday pane" >> "$PCLOG"; exit 6
fi

# TYPED-UNSENT GATE — run the detector on the RESOLVED pane id and read its one verdict line.
det_fail() { # $1 reason → REFUSED rc 8 (fail closed)
  echo "pane_close: REFUSED — the typed-line detector could not give a verdict for $PANE (${TARGET_ID:--}): $1. Nothing was closed. Check the pane by eye (tmux capture-pane -p -t ${TARGET_ID:-<id>}) before doing anything else." >&2
  echo "$(date '+%Y-%m-%d %H:%M:%S') REFUSED rc8: detector failed for $PANE: $1" >> "$PCLOG"; exit 8
}
DETECTOR="$HERE/pane_prompt_check.sh"
[ -f "$DETECTOR" ] || det_fail "detector not found at $DETECTOR"
case "$TARGET_ID" in %[0-9]*) ;; *) det_fail "pane id '$TARGET_ID' is not a %N id" ;; esac
case "${TARGET_ID#%}" in *[!0-9]*) det_fail "pane id '$TARGET_ID' is not a %N id" ;; esac
DET_OUT="$(/bin/bash "$DETECTOR" "$TARGET_ID" 2>&1)"; DET_RC=$?
[ "$DET_RC" = 0 ] || det_fail "detector exited rc $DET_RC :: $(printf '%s' "$DET_OUT" | head -3 | tr '\n' ' ')"
# The detector prints "prompt empty" for a pane it could not capture at all, so a pane that
# is gone now must not read as an empty prompt: the id has to resolve to itself AFTER the call.
[ "$(tmux display -p -t "$TARGET_ID" '#{pane_id}' 2>/dev/null)" = "$TARGET_ID" ] || det_fail "pane $TARGET_ID no longer resolves (gone before/while the detector ran — its 'empty' would be vacuous)"
DET_LINES="$(printf '%s\n' "$DET_OUT" | awk 'NF' | wc -l | tr -d ' ')"
[ "$DET_LINES" = 1 ] || det_fail "expected exactly 1 verdict line, got $DET_LINES :: $(printf '%s' "$DET_OUT" | head -3 | tr '\n' ' ')"
DET_LABEL="$(tmux display-message -p -t "$TARGET_ID" '#{@cockpit_name}' 2>/dev/null)"; DET_LABEL="${DET_LABEL:-$TARGET_ID}"
DET_REST="${DET_OUT#"  $DET_LABEL: "}"
[ "$DET_REST" != "$DET_OUT" ] || det_fail "verdict line does not start with the pane label '  $DET_LABEL: ' :: $DET_OUT"
TYPED_TOK="⚠ TYPED, UNSENT (a human wrote this — flag it, do NOT act) :: "
SUGG_TOK="SUGGESTION (Claude ghost text — ignore) :: "
MODAL_TOK="⏸ MODAL PROMPT — pane is blocked on a menu, nobody typed this :: "
case "$DET_REST" in
  "$TYPED_TOK"*)
    TYPED_LINE="${DET_REST#"$TYPED_TOK"}"
    if [ "$TYPED_OK" != 1 ]; then
      echo "pane_close: REFUSED — a HUMAN-TYPED, UNSENT line is at the prompt of $PANE ($TARGET_ID name=${TARGET_NAME:--}):" >&2
      echo "pane_close:   typed line :: $TYPED_LINE" >&2
      echo "pane_close:   read it, relay it to Kam, then re-run with --typed-ok" >&2
      echo "$(date '+%Y-%m-%d %H:%M:%S') REFUSED rc7: TYPED-UNSENT line at $PANE ($TARGET_ID), ${#TYPED_LINE} chars (text not logged)" >> "$PCLOG"; exit 7
    fi
    echo "pane_close: --typed-ok OVERRIDE USED — closing $PANE ($TARGET_ID) despite a TYPED-UNSENT line :: $TYPED_LINE" >&2
    echo "$(date '+%Y-%m-%d %H:%M:%S') OVERRIDE --typed-ok: closing $PANE ($TARGET_ID) despite a TYPED-UNSENT line, ${#TYPED_LINE} chars (text not logged)" >> "$PCLOG" ;;
  "$SUGG_TOK"*)   echo "pane_close: detector: SUGGESTION (ghost text) at $TARGET_ID — proceeding" ;;
  "prompt empty") echo "pane_close: detector: prompt empty at $TARGET_ID — proceeding" ;;
  "$MODAL_TOK"*)  echo "pane_close: detector: MODAL PROMPT at $TARGET_ID (nobody typed it) — proceeding" ;;
  *) det_fail "unrecognised verdict :: $DET_REST" ;;
esac
PSESS=""
[ -n "$PPID_PANE" ] && PSESS="$(ps -o sess= -p "$PPID_PANE" 2>/dev/null | tr -d ' ')"

# Walk a pid's ancestry to 1 (bounded), echoing "pid:tty" for each hop.
ancestry() {
  local p="$1" hops=0 t a
  while [ -n "$p" ] && [ "$p" != "0" ] && [ "$p" != "1" ] && [ "$hops" -lt 25 ]; do
    t="$(ps -o tty= -p "$p" 2>/dev/null | tr -d ' ')"
    echo "$p:${t:-?}"
    a="$(ps -o ppid= -p "$p" 2>/dev/null | tr -d ' ')"
    p="$a"; hops=$((hops+1))
  done
}

BLOCK=0
for pid in $(lsof -nP -iTCP -sTCP:LISTEN -t 2>/dev/null | sort -u); do
  lsess="$(ps -o sess= -p "$pid" 2>/dev/null | tr -d ' ')"
  chain="$(ancestry "$pid")"
  why=""
  if [ -n "$PSESS" ] && [ "$PSESS" != "0" ] && [ "$lsess" = "$PSESS" ]; then
    why="shares the pane's process session ($PSESS)"
  else
    for hop in $chain; do
      case "$hop" in
        *:"$SHORT") why="ancestor ${hop%%:*} is on the pane's tty $PTTY"; break ;;
      esac
    done
  fi
  if [ -n "$why" ]; then
    echo "pane_close: REFUSED — listener pid $pid $why and would die with the pane" >&2
    echo "pane_close:   chain: $(echo $chain | tr '\n' ' ')" >&2
    BLOCK=1
  fi
done
[ "$BLOCK" = 1 ] && { echo "$(date '+%Y-%m-%d %H:%M:%S') REFUSED rc5: a listener would die with $PANE" >> "$PCLOG"; exit 5; }

for p in "$@"; do echo "before: port $p $(curl -s -o /dev/null -w '%{http_code}' --max-time 2 "http://127.0.0.1:$p/")"; done
BEFORE=$(lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | wc -l | tr -d ' ')
tmux kill-pane -t "$PANE" || { echo "pane_close: kill-pane failed" >&2; exit 2; }
sleep 2
AFTER=$(lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | wc -l | tr -d ' ')
echo "closed $PANE; listeners $BEFORE -> $AFTER"
echo "$(date '+%Y-%m-%d %H:%M:%S') CLOSED $PANE ($TARGET_ID name=${TARGET_NAME:--}); listeners $BEFORE -> $AFTER" >> "$PCLOG"
[ "$BEFORE" != "$AFTER" ] && echo "pane_close: WARNING — the listener count MOVED across this close ($BEFORE -> $AFTER) despite no refusal. Identify what died before treating this close as clean." >&2
for p in "$@"; do echo "after:  port $p $(curl -s -o /dev/null -w '%{http_code}' --max-time 2 "http://127.0.0.1:$p/")"; done
exit 0

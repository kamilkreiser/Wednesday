#!/bin/bash
# WED-16 — 23:00 scheduled close. Fired by launchd (com.wednesday.close).
# Deterministic (no LLM): stamps the day closed in the daily note, snapshots
# today's fleet-inbox traffic, speaks a one-line good night. The INTELLIGENT
# close ritual (retro, learnings, handoff) stays with interactive sessions —
# this is the bell at the end of the working day, not a replacement for it.
#
# Guards: once per day · only fires in the 22:30-23:59 window (launchd
# coalesces missed jobs to next Mac wake — a "good night" at 09:00 would be
# worse than silence, and quiet hours start at 23:00 sharp for anything more).

set -u

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
BRAIN_DIR="$PROJECT_DIR/0_Brain"
LOG_DIR="$SELF_DIR/logs"
STATE_DIR="$SELF_DIR/state"
mkdir -p "$LOG_DIR" "$STATE_DIR"
LOG="$LOG_DIR/close_$(date +%F).log"
log() { echo "$(date '+%F %T') $*" >> "$LOG"; }

TODAY="$(date +%F)"
# WEDNESDAY_TEST_HOUR lets the window guard be exercised outside 22:30-23:59 so
# a change to the close ritual can be proven in its real environment rather than
# only in extracted form. Same pattern as shift_change.sh. It only overrides the
# guard's clock; everything downstream runs for real, so pair it with
# WEDNESDAY_DRYRUN=1 unless a genuine close is intended.
HOUR="$((10#${WEDNESDAY_TEST_HOUR:-$(date +%H)}))"
MIN="$((10#$(date +%M)))"

if [ -f "$STATE_DIR/last_close" ] && [ "$(cat "$STATE_DIR/last_close")" = "$TODAY" ]; then
  log "skip: already closed today"
  exit 0
fi
if [ "$HOUR" -lt 22 ] || { [ "$HOUR" -eq 22 ] && [ "$MIN" -lt 30 ]; }; then
  log "skip: before 22:30 window"
  exit 0
fi

# 2026-08-30 (WED-126): accept the bare DRYRUN=1 too — the 08-27 05:33 exercise set DRYRUN=1,
# this script only read WEDNESDAY_DRYRUN, so a "dry run" SPOKE inside quiet hours.
DRYRUN="${WEDNESDAY_DRYRUN:-${DRYRUN:-0}}"

# ── Fleet inbox snapshot (best-effort; never blocks the close) ──
MAIL_LINE="fleet inboxes: unreachable (key unset or API down)"
ENV_FILE="$PROJECT_DIR/4_Credentials/.env"
if [ -f "$ENV_FILE" ]; then
  # ROOT CAUSE OF THE 23:00 "unreachable" CLOSES, found 2026-08-07 by reproducing
  # the failure at 13:00 instead of waiting for 23:00. `.env` uses BARE
  # assignments (no `export`), so a plain `source` makes AGENTMAIL_API_KEY a
  # SHELL variable and not an environment variable. The bash guard below then
  # passes — bash can see it — while the python heredoc's os.environ.get()
  # returns "". An empty Bearer token is answered with 403, on every attempt,
  # every night. `set -a` is what exports it, and is why the same key works from
  # an interactive session that uses `set -a && . .env`.
  #
  # The lesson, because the earlier diagnosis was wrong in an instructive way:
  # I confirmed the key was VALID (a live call returned 200) and inferred it
  # REACHED the code. Those are different claims, and only the second one was
  # ever in doubt.
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE" 2>/dev/null || true
  set +a
  if [ -n "${AGENTMAIL_API_KEY:-}" ]; then
    # Errors go to the LOG, never /dev/null — the 08-05 "unreachable" close
    # left no diagnosable trace (WED-16 defect). 3 tries/inbox rides out blips.
    COUNTS="$(python3 - "$TODAY" <<'PYEOF' 2>>"$LOG"
import json, sys, time, urllib.request, os
from datetime import datetime
today = sys.argv[1]
key = os.environ.get("AGENTMAIL_API_KEY", "")
out = []
def local_date(ts):
    # API timestamps are UTC ("...Z"); compare against the LOCAL day or the
    # 23:00 AEST close misses everything before 10:00 local.
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00")).astimezone().date().isoformat()
    except Exception:
        return ""
# Backoff design, 2026-08-07. The 23:00 close failed two nights running with
# HTTP 403 on BOTH inboxes, three attempts each ~5s apart. Diagnosed the same
# morning: the key is valid (a live call returns 200 minutes later) and is
# byte-identical to the one the session uses, so this is not a credential fault
# and not the launchd-env theory. A 403 that clears on its own is rate limiting
# or a transient auth-service refusal — and flat 5s retries inside a 15-second
# window are exactly the wrong shape for that. Now: exponential backoff with
# jitter across ~2 minutes, and the two inboxes staggered rather than hammered
# back to back. 403 is reported as its own case so a future failure is not
# re-diagnosed from scratch.
import random
ATTEMPTS = 4
BACKOFF = (7, 21, 55)          # seconds, before attempts 2, 3, 4
for idx, inbox in enumerate(("wednesday-agent@agentmail.to", "coagent@agentmail.to")):
    if idx:
        time.sleep(3)          # stagger: don't fire both inboxes in the same instant
    for attempt in range(ATTEMPTS):
        try:
            req = urllib.request.Request(
                f"https://api.agentmail.to/v0/inboxes/{inbox}/messages?limit=50",
                headers={"Authorization": f"Bearer {key}"})
            with urllib.request.urlopen(req, timeout=10) as r:
                msgs = json.load(r).get("messages", [])
            n = sum(1 for m in msgs if local_date(m.get("timestamp", "")) == today)
            note = f" (recovered on attempt {attempt+1})" if attempt else ""
            out.append(f"{inbox.split('@')[0]}@: {n} today{note}")
            break
        except Exception as e:
            code = getattr(e, "code", None)
            kind = "403 auth refused" if code == 403 else f"{type(e).__name__}: {e}"
            print(f"inbox check {inbox} attempt {attempt+1}/{ATTEMPTS}: {kind}", file=sys.stderr)
            if attempt == ATTEMPTS - 1:
                # Do NOT assert which cause. Tested 2026-08-07: a deliberately
                # invalid key returns 403 on every attempt too, so 403 alone
                # cannot separate rate limiting from a bad or revoked key. The
                # discriminator is whether a later call succeeds — which is what
                # happened on 08-07 (200 minutes after the 23:00 failure), and
                # is why THAT night was transient. Say what is known, and name
                # the check rather than guessing the cause.
                why = ("403 auth refused after ~2min backoff — rate limit or bad key; "
                       "run a live API call to tell them apart") if code == 403 else "unreachable"
                out.append(f"{inbox.split('@')[0]}@: {why}")
            else:
                # jitter so a retry never lands in lockstep with another job's
                time.sleep(BACKOFF[attempt] + random.uniform(0, 4))
print(" · ".join(out))
PYEOF
)"
    [ -n "$COUNTS" ] && MAIL_LINE="fleet inboxes: $COUNTS"
  fi
fi

# ── Unwrapped-session detection (2026-08-10 consolidation; ledger w=5/w=6:
# "a ritual nothing triggers is not a ritual") ──
# A session can go quiet without wrapping, and going quiet is indistinguishable
# from working — so the one event guaranteed to fire daily checks the wrap
# artifacts: retro filled, tree committed, daily note tracked. This is also the
# VERIFIER half of coordinator auto-rotation (Kam's 2026-08-10 post-wrap catch):
# the rotation step, when built, arms only on a night this writes "verified".
# Dashboard data JSONs are collector churn (rewritten every few minutes) and are
# excluded — an alarm that fires every night is a check that cannot pass, which
# is as useless as one that cannot fail.
NOTE="$BRAIN_DIR/daily/$TODAY.md"
WRAP_ISSUES=""
if [ ! -f "$NOTE" ]; then
  WRAP_ISSUES="no daily note exists for today"
elif ! grep -qE '^## Session retro' "$NOTE"; then
  # 2026-08-24: a note built WITHOUT the template passed this check ("retro
  # filled") because the only thing it looked for was the placeholder line —
  # a check that cannot fail. Presence of the section is required first.
  WRAP_ISSUES="daily note has NO retro section at all"
elif grep -qF -- '- Went well / do differently:' "$NOTE"; then
  WRAP_ISSUES="retro still on its template placeholder"
fi
# 2026-08-30: standing never-delete residue (Kam 08-26: "do not delete any files") is listed in
# scheduler/wrap_check_ignore.txt — one git pathspec per line — and excluded here, so the bell
# stops flagging the same three items every night (an alarm that always fires is not a check).
IGN_ARGS=()
if [ -f "$SELF_DIR/wrap_check_ignore.txt" ]; then
  while IFS= read -r line; do case "$line" in ''|'#'*) ;; *) IGN_ARGS+=(":(exclude)$line") ;; esac; done < "$SELF_DIR/wrap_check_ignore.txt"
fi
GIT_DIRTY="$(cd "$PROJECT_DIR" && /usr/bin/git status --porcelain -- . ':(exclude)0_Brain/dashboard/data' "${IGN_ARGS[@]}" 2>>"$LOG")"
if [ -n "$GIT_DIRTY" ]; then
  N_DIRTY="$(printf '%s\n' "$GIT_DIRTY" | grep -c .)"
  WRAP_ISSUES="${WRAP_ISSUES:+$WRAP_ISSUES · }$N_DIRTY uncommitted/untracked file(s) outside dashboard churn"
fi
# Untracked is worse than uncommitted (the 08-09 note was never git-added at
# all — invisible to every habit). Name it separately even though it also
# appears in the dirty count.
if [ -f "$NOTE" ] && ! (cd "$PROJECT_DIR" && /usr/bin/git ls-files --error-unmatch "0_Brain/daily/$TODAY.md" >/dev/null 2>&1); then
  WRAP_ISSUES="${WRAP_ISSUES:+$WRAP_ISSUES · }today's daily note is NOT tracked by git"
fi
if [ -n "$WRAP_ISSUES" ]; then
  log "WRAP CHECK: UNWRAPPED OR IN-FLIGHT — $WRAP_ISSUES"
else
  log "WRAP CHECK: verified (retro filled, tree clean outside churn, note tracked)"
fi

# ── Stamp the daily note (create from template if the day left none) ──
if [ "$DRYRUN" = "1" ]; then
  log "DRYRUN: would stamp $NOTE with close block ($MAIL_LINE) and speak good night"
  exit 0
fi
if [ ! -f "$NOTE" ]; then
  sed "s/{{date}}/$TODAY/" "$BRAIN_DIR/daily/_template.md" > "$NOTE"
  log "daily note was missing — created from template (no session ran today?)"
fi
{
  echo ""
  echo "## 23:00 close (scheduler, WED-16)"
  echo "- Day closed at $(date '+%H:%M') by the scheduled close ritual."
  echo "- $MAIL_LINE"
  if [ -n "$WRAP_ISSUES" ]; then
    echo "- ⚠ **WRAP CHECK FAILED at close: $WRAP_ISSUES.** Either a session"
    echo "  went quiet without wrapping (the 08-09 failure) or work was still"
    echo "  in flight at the bell. Next boot: reconcile FIRST — commit what the"
    echo "  day left, fill the retro from evidence, then proceed."
  else
    echo "- Wrap check: verified (retro filled, tree clean outside churn, note tracked)."
  fi
  echo "- If a session was mid-flight, next boot reconciles from this note + Linear."
} >> "$NOTE"
echo "$TODAY" > "$STATE_DIR/last_close"
if [ -n "$WRAP_ISSUES" ]; then
  echo "$WRAP_ISSUES" > "$STATE_DIR/wrap_check_$TODAY"
else
  echo "verified" > "$STATE_DIR/wrap_check_$TODAY"
fi
log "daily note stamped; $MAIL_LINE"

# ── One short good night (23:00 sharp is the boundary, not past it) ──
if [ -n "$WRAP_ISSUES" ]; then
  "$PROJECT_DIR/2_Project_Files/voice/speak.sh" "That's the day closed, Kam — one flag: the wrap check found work not yet committed, so the morning session will reconcile it first. Good night." || log "speak failed (voice unavailable?)"
else
  "$PROJECT_DIR/2_Project_Files/voice/speak.sh" "That's the day closed, Kam. Everything still open is safely on the board for the morning. Good night." || log "speak failed (voice unavailable?)"
fi
log "close complete"

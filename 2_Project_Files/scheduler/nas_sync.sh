#!/bin/bash
# nas_sync.sh — the nightly NAS sync leg, with a DELETION ALARM.
#
# Kam, 2026-09-08 14:57: "create a schedule for both agents to sync to the NAS drive at
# night. Get Tuesday to sync at 11pm, and I think you should sync at 3 or 4am."
#
# WHY THIS WRAPPER EXISTS AND IS NOT JUST A CRON LINE ON devnas-sync.sh.
# `!SYNC FILES/devnas.prf` runs `batch = true`; `confirmbigdel` was FALSE until 2026-09-08 and is TRUE since (Kam set it after the 08-26 loss — measured 2026-09-21). Unattended,
# that propagates a mass deletion in either direction with nobody watching. On 2026-08-26
# exactly that happened and cost a day of recovery — and until tonight a human was always
# awake when a sync ran. A 23:00 and an 03:30 job on two machines ends that.
#
# WHAT THIS CAN AND CANNOT DO, stated honestly rather than implied:
#   PREVENT  — it CANNOT. Unison acts before anything can inspect it, `devnas-sync.sh`
#              passes no flags through (its EXTRA_ARGS takes ignores only), and the profile
#              is Kam's file at the workspace root, not Wednesday's to edit. Prevention is
#              ONE LINE in his profile — `confirmbigdel = true` — and it is asked, not taken.
#   DETECT   — it does. It counts unison's own `Deleting` lines in the run it just ran.
#   RECOVER  — the profile already keeps `backup = Name *`, `maxbackups = 5`,
#              `backuploc = central`, so deleted files sit in ~/.unison/backup ON THE MACHINE
#              THAT RAN THE LEG. That is the recovery path that worked on 2026-08-26.
#   REPORT   — every run leaves a one-line summary the morning seat reads, so a silent night
#              is a fact rather than an assumption.
#   RETRY    — 2026-09-21: the paths unison reports as "failed:" (modified during the 3-hour
#              scan) are re-synced with a `-path`-scoped second pass — see THE RETRY PASS
#              below — and every log ends with a STALENESS block (nas_staleness.sh) that
#              compares the key files on both sides by sha256. Parser + arms: nas_sync_lib.sh,
#              fleet/tests/nas_sync_retry_arms.sh.
#
# NEVER add `>/dev/null` here. A sync failure you cannot diagnose costs more than it saves,
# and a deletion you cannot see is a deletion you keep.
set -u

SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"; SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
HERE="$(cd -P "$(dirname "$SOURCE")" && pwd)"
PROJECT_DIR="$(cd -P "$HERE/../.." && pwd)"
WORKSPACE="$(cd -P "$PROJECT_DIR/.." && pwd)"
AGENT="${WED_AGENT:-wednesday}"
# FRIDAY (2026-09-23): the laptop seat gets NO scheduled jobs and has NO NAS leg (Kam's NAS rulings name two legs:
# Wednesday's and Tuesday's). Without this refusal a friday run would fall through to the engine with NEITHER
# ruled scope (no ignore set, no path restriction) — i.e. walk the whole workspace. Refused BY NAME, before any log,
# state file or engine call.
if [ "$AGENT" = "friday" ]; then
  echo "nas_sync: REFUSED — seat friday: the laptop has no NAS leg (Kam's rulings cover Wednesday's 03:30 and Tuesday's 23:00 legs only); nothing run" >&2
  exit 2
fi

# >>> ruled-ignores — KAM'S RULINGS ON WHAT THIS LEG SYNCS
# 2026-09-10 20:27 `stop-partition-rerun` + 20:28 `nas-shared-folders-owner = wednesday`:
#   this leg does NOT walk Datasec or the TUESDAY tree — Tuesday's leg owns those.
# 2026-09-11 07:23 `narrow-hard`: "Cut node_modules, worktrees and regenerable bulk from
#   the synced set, then re-run".
# WHY IT LIVES HERE: until 2026-09-11 the partition existed ONLY in the environment of a
# hand-launched re-run. The 03:30 launchd job passes NO environment, so the nightly leg
# would have run WITHOUT the partition Kam ruled. A ruling that lives in one shell is not
# in force.
# SCOPED to agent=wednesday: another agent running this wrapper must never inherit a set
# that excludes its own tree. An explicitly exported DEVNAS_IGNORE_NAMES still wins.
# The engine takes BASENAMES only (`-ignore "Name X"`, any depth), so every name below is
# one that is regenerable wherever it appears. `.azure/telemetry` was on the card as
# "similar bulk" and is NOT here: as a basename, `Name telemetry` would match every folder
# of that name. `dist`/`build`/`coverage` are NOT here either: those names hold real
# source in some trees.
if [ "$AGENT" = "wednesday" ] && [ -z "${DEVNAS_IGNORE_NAMES:-}" ]; then
  DEVNAS_IGNORE_NAMES="Datasec TUESDAY node_modules worktrees .venv __pycache__ .next .turbo .pytest_cache"
fi
export DEVNAS_IGNORE_NAMES="${DEVNAS_IGNORE_NAMES:-}"
# TUESDAY'S LEG — Kam's rulings on what it covers:
#   nas-shared-folders-owner = wednesday: "Tuesday's leg syncs only Datasec and its own tree";
#   narrow-hard: no node_modules / worktrees / regenerable bulk; 2026-09-16 15:00: "exclude qa worktrees".
# ENFORCED BY PATH, so it FAILS CLOSED (card t9-nas-leg-scope-mechanism = a, Kam 2026-09-21 16:10): the engine's
# DEVNAS_PATHS restricts unison to exactly these subtrees, and a new top-level folder is never swept in.
# Until 2026-09-21 this leg had NO branch here: its plist set no WED_AGENT, so it ran AS WEDNESDAY on 09-17/18/19
# with her ignore set — the reverse of the ruling (it skipped Datasec and TUESDAY).
# Globs (qa-worktrees*, wt-*) rely on the engine's unquoted `for _n in $DEVNAS_IGNORE_NAMES` running with CWD=/
# (launchd's default), where they match nothing and stay literal for unison. Re-check if a WorkingDirectory is added.
if [ "$AGENT" = "tuesday" ]; then
  [ -n "${DEVNAS_PATHS:-}" ] || DEVNAS_PATHS=$'!CODING/Datasec\nTUESDAY\nNotes (MASTER)/Datasec'
  # 4_Credentials + 3_Access_Keys: NEVER replicated to the NAS (workspace hard rule 3). The 2026-09-21 preview showed
  # this scope would have pushed msal token caches, service_principal_entries.json, a gh hosts.yml, a private signing
  # .pem and a private deploy key onto the share. They are re-creatable by re-login; they cannot be un-leaked.
  # .unison*: unison's own temp dirs — 51,021 of the NAS's stale Datasec files were one abandoned .unison.*.tmp.
  [ -n "${DEVNAS_IGNORE_NAMES:-}" ] || DEVNAS_IGNORE_NAMES="4_Credentials 3_Access_Keys .unison* node_modules worktrees qa-worktrees* deploy-worktrees wt-* .venv __pycache__ .next .turbo .pytest_cache"
fi
# ONE-WAY, ADDITIVE (Kam 2026-09-21 18:01, card t9-nas-leg-direction = a): the T9 is the source and is NEVER written;
# nothing is deleted on the NAS. The preview showed a two-way first run would copy 137,309 NAS-only files INTO the
# live Datasec working trees. EXPECT rc=1 nightly while NAS-only files exist ("[CONFLICT] Skipping … nodeletion"):
# that is the rule working, not a failure. Proven on scratch dirs before arming (see the engine's comment).
if [ "$AGENT" = "tuesday" ]; then
  [ -n "${DEVNAS_ONEWAY:-}" ] || DEVNAS_ONEWAY=1
fi
export DEVNAS_ONEWAY="${DEVNAS_ONEWAY:-}"
export DEVNAS_PATHS="${DEVNAS_PATHS:-}"
# <<< ruled-ignores

ENGINE="$WORKSPACE/!SYNC FILES/devnas-sync.sh"
LOGDIR="$PROJECT_DIR/2_Project_Files/scheduler/logs"
STATEDIR="$PROJECT_DIR/2_Project_Files/scheduler/state"
mkdir -p "$LOGDIR" "$STATEDIR"
# PID in the stamp: two runs inside the same SECOND otherwise share a log, and the
# deletion count then reads the SUM of both runs. Found by exercising this script,
# not by reading it — cases 2 and 3 of the fixture collided exactly that way.
STAMP="$(date '+%Y-%m-%d_%H%M%S')_$$"
LOG="$LOGDIR/nas_sync_${AGENT}_${STAMP}.log"
REPORT="$STATEDIR/nas_sync_last_${AGENT}.txt"
ALERT_AT="${NAS_SYNC_DELETE_ALERT:-50}"

say() { printf '%s %s\n' "$(date '+%H:%M:%S')" "$*" | tee -a "$LOG"; }

say "=== NAS sync leg — agent=$AGENT workspace=$WORKSPACE ==="

if [ ! -x "$ENGINE" ]; then
  say "REFUSING: engine not executable at $ENGINE"
  printf '%s | agent=%s | ENGINE MISSING | log=%s\n' "$STAMP" "$AGENT" "$LOG" > "$REPORT"
  exit 1
fi

# The engine handles NAS ping + mount + lock + first-sync guard itself. We do not
# re-implement any of that — re-implementing a tool's method in order to check it is
# how two implementations of one idea end up disagreeing.
say "running: $ENGINE"
"$ENGINE" 2>&1 | tee -a "$LOG"
RC=${PIPESTATUS[0]}
say "engine exit rc=$RC"
RC_MAIN=$RC

# ── THE RETRY PASS (Kam 2026-09-21 09:48 "build it today") ────────────────────────────────
# WHY: six nights running (09-14 → 09-21) the leg ended rc=2 with 22–74 "failed:" paths, every
# one "has been modified during synchronization. Transfer aborted." The scan takes 3–4 hours
# (03:30 → ~07:00) and the fleet writes those files all night, so the busiest files —
# history.md, the ledger, NEXT-PICKUP.md, the daily note — are exactly the ones that never
# land: on 2026-09-21 the NAS held history.md from 09-15 and _ledger.md from 09-16 while the
# control file (a finished daily note) was byte-identical. A retry of ONLY the failed paths
# takes seconds, because unison scans just those paths, so the write-window it competes with
# is seconds wide instead of hours.
# HOW: parse this run's own log for the "  failed: <path>" list (nas_sync_lib.sh), re-run
# unison with the SAME profile name, roots and run-scoped ignores, plus `-path <p>` per path,
# up to NAS_SYNC_RETRIES times with NAS_SYNC_RETRY_PAUSE seconds between. The engine cannot do
# this for us (its EXTRA_ARGS accepts ignore basenames only), so the invocation is spelled out
# here and printed into the log before it runs. Same profile ⇒ same confirmbigdel, same
# backups, same archive (verified with -showarchive 2026-09-21: identical hashcodes with and
# without -path).
# WHAT IT NEVER DOES: touch a path outside the failed list (the argv is built from the parsed
# list and nothing else — arms 1–3 of fleet/tests/nas_sync_retry_arms.sh); retry a path that
# is gone from the SOURCE (under confirmbigdel+batch a -path on a vanished file ABORTS the
# whole scoped run rc=3 — measured on a scratch pair 2026-09-21 — and a deletion is the one
# thing this pass must never be the first to propagate; the full run does that with the
# alarm below watching); retry this run's own log (tee is writing it; it fails again by
# construction); run while the engine's own lock is held by another sync.
# EXIT CONTRACT (changed 2026-09-21, stated here because Tuesday's 23:00 leg shares this
# file): the exit code is the LAST unison run's rc — main run if the retry was skipped,
# else the final retry attempt. Both are printed in the summary as rc=<final> (main=<n>).
UNISON_BIN="${UNISON_BIN:-/opt/homebrew/bin/unison}"
NAS_TARGET="${DEVNAS_TARGET_ROOT:-/Volumes/Development}"
RETRIES="${NAS_SYNC_RETRIES:-2}"
RETRY_PAUSE="${NAS_SYNC_RETRY_PAUSE:-45}"
RETRY_SUMMARY="retry: skipped (lib missing)"
RC_FINAL=$RC
if [ -f "$HERE/nas_sync_lib.sh" ]; then
  # shellcheck source=nas_sync_lib.sh
  . "$HERE/nas_sync_lib.sh"
  FAILED_ALL="$LOGDIR/nas_sync_${AGENT}_${STAMP}.failed.txt"
  nas_failed_paths "$LOG" > "$FAILED_ALL"
  N_BEFORE=$(nas_count "$FAILED_ALL")
  say "failed paths in the main run: $N_BEFORE (list: $FAILED_ALL)"
  if [ "$N_BEFORE" -eq 0 ]; then
    RETRY_SUMMARY="retry: 0 → 0 (skipped: no failed: lines in the main run)"
    say "$RETRY_SUMMARY"
  elif [ "${RETRIES//[0-9]/}" != "" ] || [ "$RETRIES" -le 0 ]; then
    RETRY_SUMMARY="retry: $N_BEFORE → $N_BEFORE (skipped: NAS_SYNC_RETRIES=$RETRIES)"
    say "$RETRY_SUMMARY"
  elif [ ! -x "$UNISON_BIN" ]; then
    RETRY_SUMMARY="retry: $N_BEFORE → $N_BEFORE (skipped: $UNISON_BIN not executable)"
    say "🔴 $RETRY_SUMMARY"
  elif [ ! -f "$HOME/.unison/devnas.prf" ]; then
    RETRY_SUMMARY="retry: $N_BEFORE → $N_BEFORE (skipped: ~/.unison/devnas.prf not staged — the engine did not reach unison)"
    say "🔴 $RETRY_SUMMARY"
  elif [ "$NAS_TARGET" = "/Volumes/Development" ] && ! mount | /usr/bin/grep -q " on $NAS_TARGET "; then
    RETRY_SUMMARY="retry: $N_BEFORE → $N_BEFORE (skipped: $NAS_TARGET is not mounted)"
    say "🔴 $RETRY_SUMMARY"
  else
    # Same lock the engine takes (devnas-sync.sh lines 43–44, same expression so it cannot
    # drift): a hand-launched "Sync All Drives" and this retry must never overlap.
    _lock_tag="$(echo "$NAS_TARGET" | tr -c 'A-Za-z0-9' '_')"
    RETRY_LOCK="/tmp/devnas-sync${_lock_tag}.lock.d"
    if ! MK_ERR="$(mkdir "$RETRY_LOCK" 2>&1)"; then
      RETRY_SUMMARY="retry: $N_BEFORE → $N_BEFORE (skipped: engine lock $RETRY_LOCK is held by another sync — ${MK_ERR:-mkdir failed})"
      say "🔴 $RETRY_SUMMARY"
    else
      # The lock is ours from here; release it (an empty dir, the engine's own protocol) on exit.
      trap 'rmdir "$RETRY_LOCK" || true' EXIT
      IGN_ARGS=()
      for _n in $DEVNAS_IGNORE_NAMES; do IGN_ARGS+=( -ignore "Name $_n" ); done
      # Working lists live in a temp dir; what stays beside the log is the failed list, the
      # dropped list, each attempt's own unison output, and — if any — the unlanded list.
      WORK="$(mktemp -d -t nas_sync_retry)" || WORK="$LOGDIR"
      TODO="$WORK/todo.txt"
      DROPPED="$LOGDIR/nas_sync_${AGENT}_${STAMP}.retry.dropped.txt"
      OWN_LOG_REL="${LOG#$WORKSPACE/}"
      # (a) never this run's own log — tee is appending to it right now.
      /usr/bin/grep -vxF -- "$OWN_LOG_REL" "$FAILED_ALL" > "$TODO"
      : > "$DROPPED"
      if [ "$(nas_count "$TODO")" -lt "$N_BEFORE" ]; then
        printf '%s\n' "$OWN_LOG_REL" >> "$DROPPED"
        say "retry: dropped 1 path — this run's own log ($OWN_LOG_REL) is still being written"
      fi
      # (b) never a path that is gone from the source.
      _present="$WORK/present.txt"; _gone="$WORK/gone.txt"
      nas_filter_present "$WORKSPACE" "$TODO" "$_present" "$_gone"
      if [ "$(nas_count "$_gone")" -gt 0 ]; then
        say "retry: dropped $(nas_count "$_gone") path(s) gone from the source since the main run (a -path on a vanished file aborts the scoped run under confirmbigdel; the next full run carries the deletion, alarm watching):"
        sed 's/^/    gone: /' "$_gone" | tee -a "$LOG"
        cat "$_gone" >> "$DROPPED"
      fi
      mv "$_present" "$TODO"
      N_AFTER=$(nas_count "$TODO")
      ATTEMPT=0
      while [ "$N_AFTER" -gt 0 ] && [ "$ATTEMPT" -lt "$RETRIES" ]; do
        ATTEMPT=$((ATTEMPT+1))
        say "retry attempt $ATTEMPT/$RETRIES: pausing ${RETRY_PAUSE}s so the writers move on, then $N_AFTER path(s)"
        sleep "$RETRY_PAUSE"
        nas_build_path_args "$TODO"
        RLOG="$LOGDIR/nas_sync_${AGENT}_${STAMP}.retry${ATTEMPT}.log"
        say "retry command: $UNISON_BIN devnas -root $WORKSPACE -root $NAS_TARGET ${IGN_ARGS[*]} -path <each of the $N_AFTER paths in $TODO>"
        "$UNISON_BIN" devnas -root "$WORKSPACE" -root "$NAS_TARGET" \
          ${IGN_ARGS[@]+"${IGN_ARGS[@]}"} "${NAS_PATH_ARGS[@]}" 2>&1 | tee -a "$RLOG" | tee -a "$LOG"
        RC_R=${PIPESTATUS[0]}
        RC_FINAL=$RC_R
        say "retry attempt $ATTEMPT exit rc=$RC_R (own log: $RLOG)"
        # A confirmbigdel abort names the paths; drop them and let the loop try the rest.
        _emptied="$WORK/emptied.$ATTEMPT.txt"
        nas_emptied_paths "$RLOG" > "$_emptied"
        if [ "$(nas_count "$_emptied")" -gt 0 ]; then
          say "retry: unison ABORTED this attempt — $(nas_count "$_emptied") path(s) emptied on one side; dropping them from the retry (the full run owns deletions):"
          sed 's/^/    emptied: /' "$_emptied" | tee -a "$LOG"
          cat "$_emptied" >> "$DROPPED"
          nas_minus "$TODO" "$_emptied" "$TODO.next"
          mv "$TODO.next" "$TODO"
          N_AFTER=$(nas_count "$TODO")
          continue
        fi
        # Still-failing paths from THIS attempt become the next attempt's list.
        nas_failed_paths "$RLOG" > "$TODO.next"
        mv "$TODO.next" "$TODO"
        N_AFTER=$(nas_count "$TODO")
        say "retry attempt $ATTEMPT: $N_AFTER path(s) still failing"
      done
      N_DROPPED=$(nas_count "$DROPPED")
      if [ "$N_DROPPED" -gt 0 ]; then
        RETRY_SUMMARY="retry: $N_BEFORE → $N_AFTER ($ATTEMPT attempt(s), $N_DROPPED dropped — $DROPPED)"
      else
        RETRY_SUMMARY="retry: $N_BEFORE → $N_AFTER ($ATTEMPT attempt(s))"
      fi
      say "$RETRY_SUMMARY"
      # Prefix is "unlanded:", NOT "failed:" — this log is parsed for "failed:" and a summary
      # that re-used the token would double-count itself.
      if [ "$N_AFTER" -gt 0 ]; then
        UNLANDED="$LOGDIR/nas_sync_${AGENT}_${STAMP}.retry.unlanded.txt"
        cp "$TODO" "$UNLANDED"
        say "still failing after the retry pass (these did NOT land tonight; list: $UNLANDED):"
        sed 's/^/    unlanded: /' "$TODO" | tee -a "$LOG"
      fi
    fi
  fi
else
  say "🔴 $HERE/nas_sync_lib.sh missing — retry pass skipped; rc stays the main run's"
fi
RC=$RC_FINAL
say "rc: final=$RC_FINAL main=$RC_MAIN (exit code is the last unison run's)"

# ── THE DELETION ALARM ────────────────────────────────────────────────────────────────
# `Deleting` is unison's own token — the one the 2026-08-26 recovery was found by. We
# search for the MACHINE's word, not the human's ("deleted", "removed" appear in prose).
# NOT `grep -c ... || echo 0`: grep EXITS 1 on zero matches, so that form prints the
# count AND the fallback — "0\n0" — and every downstream field is then malformed.
# Exercising it is what showed this; reading it did not.
#
# ── 2026-09-11 (Wednesday): THE COUNT HERE WAS BLIND UNTIL TODAY, AND THIS IS WHY ─────────
# These lines read `grep -c '^Deleting ' "$LOG"` and `grep -c 'conflict' "$LOG"`. The 07:27
# narrow-hard run propagated 248 deletions and they printed 0 and 163.
#   1. This unison writes `[BGN] Deleting <path> from <root>` (plus `[END] Deleting <path>`),
#      not a bare `Deleting`.
#   2. Its log is CARRIAGE-RETURN separated (progress repaints), so a `^` anchor on the RAW
#      file matched nothing: raw 0 against 248 once `\r` becomes `\n`.
#   3. 158 of the 163 'conflict' lines were FILE NAMES containing `conflict_on`; unison's own
#      conflict marker `<-?->` appeared 0 times.
# None of the three earlier logs held a single deletion, so this alarm had never been measured
# against one. A failed normalisation reports UNKNOWN — never a zero it did not measure.
NORM="$(mktemp -t nas_sync_norm)" || NORM=""
if [ -n "$NORM" ] && tr '\r' '\n' < "$LOG" > "$NORM"; then
  DELETES=$(grep -cE '^(\[BGN\] )?Deleting ' "$NORM"); DELETES=${DELETES:-0}
  DEL_BY_ROOT=$(grep -E '^(\[BGN\] )?Deleting ' "$NORM" | sed -nE 's/^.* from (.+)$/\1/p' | sort | uniq -c | awk '{n=$1; $1=""; printf "%s%s from%s", s, n, $0; s="; "}')
  CONFLICTS=$(grep -cF -- '<-?->' "$NORM"); CONFLICTS=${CONFLICTS:-0}
else
  say "🔴 could not normalise $LOG — deletion and conflict counts are UNKNOWN, not zero"
  DELETES=UNKNOWN; DEL_BY_ROOT=""; CONFLICTS=UNKNOWN
fi
say "deletions propagated: $DELETES (alarm at $ALERT_AT)${DEL_BY_ROOT:+ — $DEL_BY_ROOT} | conflicts (<-?->): $CONFLICTS"

# rc=<exit code> is the LAST unison run's; main=<n> is the engine's full run. `retry: A → B`
# is failed-paths before the retry pass → still failing after it (B is what did NOT land).
SUMMARY="$STAMP | agent=$AGENT | rc=$RC (main=$RC_MAIN) | $RETRY_SUMMARY | deletions=$DELETES${DEL_BY_ROOT:+ ($DEL_BY_ROOT)} | conflicts=$CONFLICTS | log=$LOG"
printf '%s\n' "$SUMMARY" > "$REPORT"

if [ "$DELETES" -ge "$ALERT_AT" ] 2>/dev/null; then
  ALERT="$STATEDIR/nas_sync_ALERT_${AGENT}_${STAMP}.txt"
  {
    echo "NAS SYNC DELETION ALARM — $DELETES files were DELETED by the $AGENT leg at $STAMP."
    echo
    echo "This is not necessarily wrong: a deletion you made on purpose propagates too."
    echo "It is flagged because nobody was awake to see it, and because on 2026-08-26 this"
    echo "exact mechanism cost a day of recovery."
    echo
    echo "RECOVERY, if any of it was not intended: the deleted files are in ~/.unison/backup"
    echo "ON THIS MACHINE (backup = Name *, maxbackups = 5). They are NOT on the drives."
    echo
    echo "The deleted paths, from unison's own output:"
    grep -E '^(\[BGN\] )?Deleting ' "$NORM" | head -200
  } > "$ALERT"
  say "🔴 ALARM WRITTEN: $ALERT"
  if [ -x "$PROJECT_DIR/2_Project_Files/tools/chat_reply.sh" ]; then
    "$PROJECT_DIR/2_Project_Files/tools/chat_reply.sh" \
"The overnight sync to the NAS deleted $DELETES files and I want you to see that before you trust the drives.

That is above the threshold where I stop treating it as routine. It may be entirely correct — a deletion you made on purpose propagates like any other change — but nobody was awake to watch it, and this is the mechanism that cost us a day in August.

Every deleted file is recoverable. They are in the unison backup store on the machine that ran the leg, not on the drives themselves. The full list of paths is in $ALERT, and the run log is at $LOG." 2>&1 | tee -a "$LOG"
  fi
fi

say "=== done — $SUMMARY ==="

# ── STALENESS LINE (report, not enforcement — Kam 2026-09-21) ────────────────────────────
# After the summary so the `=== done` grep is unchanged; the block that follows it is the
# morning's answer to "did the busy files actually land?" — verify the destination, not the
# leg (2026-08-05_verify-the-chain-not-the-legs). Read-only; it prints its own skip reason
# when the NAS is not mounted.
if [ -f "$HERE/nas_staleness.sh" ]; then
  bash "$HERE/nas_staleness.sh" 2>&1 | tee -a "$LOG"
else
  say "🔴 $HERE/nas_staleness.sh missing — no staleness block for this run"
fi
exit "$RC"

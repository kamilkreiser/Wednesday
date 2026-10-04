#!/bin/bash
# nas_push.sh — Wednesday's NAS backup leg, ONE-WAY: DevMASTER -> NAS, additive. It cannot delete anything,
# and it never writes to DevMASTER.
#
# Kam, 2026-10-04 (live board, card wed-nassync-rearm-shape-1004 => a): "go with a — rebuild it one-way".
# WHY: the two-way unison leg (nas_sync.sh, HELD) ran ~14 h on 2026-10-04, was cut off by a reboot, and copied
# false NAS-side "deletions" of ~200 tracked + ~245k untracked WEDNESDAY files onto DevMASTER. A two-way engine
# can write to the master; this one structurally cannot.
#
# WHAT IT GUARANTEES, and what it does NOT (named, per 2026-09-08_a-safety-claim-names-the-property-it-checked):
#   - DevMASTER is only ever the rsync SOURCE: no --delete*, no --remove-source-files. The flags are fixed in this file.
#   - Nothing on the NAS is deleted. A NAS file that DevMASTER replaces is MOVED into
#     <NAS>/_nas_push_overwritten/<stamp>/ (rsync --backup), never lost.
#   - It REFUSES unless the destination is a mounted SMB volume carrying the old engine's marker file, so an
#     unmounted /Volumes/Development can never be filled on the Studio's own disk.
#   - A run-time cap (NASPUSH_MAX_SECONDS, default 14400 = 4 h) kills an overlong run. rsync writes each file to a
#     temp name and renames it, so a killed run leaves whole files, never half files.
#   - NOT covered: files that exist ONLY on the NAS stay there forever (it never deletes them); a DevMASTER file
#     deleted on purpose stays on the NAS. Nothing is read back from the NAS to DevMASTER: restoring is a human act.
#   - NOT covered: .git (excluded, as the old leg did — repos travel by git push).
#
# HOLD: while scheduler/NASPUSH_HOLD_wednesday exists it refuses (rc 3). Arming is Kam's word.
# TEST MODE: NASPUSH_TEST_SRC / NASPUSH_TEST_DST point it at scratch trees (only under /private/tmp or the
# session scratchpad); the mount check then requires only the marker file. Arms: fleet/tests/nas_push_arms.sh.
#
# Exit codes: 0 done · 2 refused (precondition) · 3 held · 4 killed by the run-time cap · 5 rsync error · 6 locked
# NEVER add >/dev/null here (2026-08-06_never-discard-stderr).
set -u

HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT="${WED_AGENT:-wednesday}"
RSYNC=/opt/homebrew/bin/rsync
LOG="${NASPUSH_LOG:-$HOME/Library/Logs/wednesday_naspush.log}"
STATE="$HERE/state/naspush_last.txt"
MAX_SECONDS="${NASPUSH_MAX_SECONDS:-14400}"
STAMP="$(date '+%Y%m%d-%H%M%S')"
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1   # --dry-run: rsync -n, writes nothing on either side (itemized list only)

ts()  { date '+%Y-%m-%d %H:%M:%S'; }
log() { echo "[$(ts)] $*" | tee -a "$LOG" >&2; }
refuse() { log "nas_push: REFUSED — $*"; exit "${2:-2}"; }

[ "$AGENT" = "wednesday" ] || { echo "nas_push: REFUSED — this leg is Wednesday's only (seat=$AGENT); nothing run" >&2; exit 2; }
[ -e "$HERE/NASPUSH_HOLD_$AGENT" ] && { echo "nas_push: REFUSED — $HERE/NASPUSH_HOLD_$AGENT exists (arming is Kam's word); nothing run" >&2; exit 3; }
[ -x "$RSYNC" ] || { echo "nas_push: REFUSED — $RSYNC missing (brew install rsync; PORTABILITY)" >&2; exit 2; }
mkdir -p "$(dirname "$LOG")" "$HERE/state"

if [ -n "${NASPUSH_TEST_SRC:-}" ] || [ -n "${NASPUSH_TEST_DST:-}" ]; then
  SRC="${NASPUSH_TEST_SRC:?TEST mode needs both NASPUSH_TEST_SRC and NASPUSH_TEST_DST}"
  DST="${NASPUSH_TEST_DST:?TEST mode needs both NASPUSH_TEST_SRC and NASPUSH_TEST_DST}"
  case "$SRC$DST" in *..*) refuse "test paths may not contain '..'";; esac
  for p in "$SRC" "$DST"; do
    case "$p" in /private/tmp/*|/tmp/*) ;; *) refuse "TEST paths must live under /private/tmp (got $p)";; esac
  done
  MODE=test
else
  SRC=/Volumes/DevMASTER
  DST=/Volumes/Development
  MODE=real
  # The NAS must be a MOUNTED SMB volume — never a plain folder on the boot disk.
  mount | /usr/bin/grep -q " on $DST (smbfs" || refuse "$DST is not a mounted SMB volume — mount the NAS first; nothing run"
  mount | /usr/bin/grep -q " on $SRC (" || refuse "$SRC is not mounted; nothing run"
fi
SRC="${SRC%/}"; DST="${DST%/}"
[ "$SRC" != "$DST" ] || refuse "source and destination are the same path"
case "$DST/" in "$SRC"/*) refuse "destination is inside the source";; esac
case "$SRC/" in "$DST"/*) refuse "source is inside the destination";; esac
[ -d "$SRC" ] || refuse "source $SRC is not a directory"
[ -d "$DST" ] || refuse "destination $DST is not a directory"
# The old engine's marker proves this is the NAS replica, not an empty mount point or a stranger's volume.
[ -e "$DST/.devnas-sync-state" ] || refuse "no .devnas-sync-state marker at $DST — not the known NAS replica"

LOCK="/tmp/wednesday-naspush.lock.d"
mkdir "$LOCK" 2>/dev/null || { log "nas_push: REFUSED — another run holds $LOCK"; exit 6; }
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

# Scope: the same set the two-way leg used — Kam's profile ignores (read, never written) + the leg's ruled names.
EXCL=()
PRF="$SRC/!SYNC FILES/devnas.prf"
[ "$MODE" = real ] && [ ! -f "$PRF" ] && refuse "profile $PRF missing — cannot reproduce the ruled scope"
if [ -f "$PRF" ]; then
  while IFS= read -r line; do
    case "$line" in
      "ignore = Name "*) EXCL+=( "--exclude=${line#ignore = Name }" ) ;;
      "ignore = Path "*) EXCL+=( "--exclude=/${line#ignore = Path }" ) ;;
    esac
  done < "$PRF"
fi
for n in Datasec TUESDAY node_modules worktrees .venv __pycache__ .next .turbo .pytest_cache .git _nas_push_overwritten; do
  EXCL+=( "--exclude=$n" )
done

BACKUP_DIR="$DST/_nas_push_overwritten/$STAMP"
ARGS=( -rlt --modify-window=2 --backup "--backup-dir=$BACKUP_DIR" --itemize-changes --stats "${EXCL[@]}" )
[ "$DRY" = 1 ] && ARGS=( -n "${ARGS[@]}" )
for a in "${ARGS[@]}"; do case "$a" in --delete*|--remove-source-files|--del|--prune-empty-dirs) refuse "forbidden flag $a";; esac; done

log "nas_push: START mode=$MODE dry=$DRY $SRC/ -> $DST/ (one-way, additive; cap ${MAX_SECONDS}s; ${#EXCL[@]} excludes; overwritten -> $BACKUP_DIR)"
RUNLOG="$HERE/state/naspush_run_$STAMP.log"
"$RSYNC" "${ARGS[@]}" "$SRC/" "$DST/" > "$RUNLOG" 2>&1 &
RPID=$!
SECS=0
while kill -0 "$RPID" 2>/dev/null; do
  sleep 5; SECS=$((SECS+5))
  if [ "$SECS" -ge "$MAX_SECONDS" ]; then
    kill "$RPID" 2>/dev/null; sleep 3; kill -9 "$RPID" 2>/dev/null
    wait "$RPID" 2>/dev/null
    log "nas_push: KILLED by the run-time cap after ${SECS}s (whole files only; the next run resumes). log $RUNLOG"
    echo "$(ts) KILLED-CAP after ${SECS}s mode=$MODE log=$RUNLOG" > "$STATE"
    exit 4
  fi
done
wait "$RPID"; RC=$?
NEW=$(/usr/bin/grep -c '^>f+++' "$RUNLOG"); UPD=$(/usr/bin/grep -c '^>f[.c]' "$RUNLOG"); DEL=$(/usr/bin/grep -ci '^\*deleting' "$RUNLOG")
if [ "$RC" -ne 0 ]; then
  log "nas_push: rsync rc=$RC after ${SECS}s (new=$NEW updated=$UPD). Tail of $RUNLOG:"; tail -5 "$RUNLOG" | tee -a "$LOG" >&2
  echo "$(ts) RC=$RC after ${SECS}s new=$NEW updated=$UPD deleting=$DEL mode=$MODE log=$RUNLOG" > "$STATE"
  exit 5
fi
log "nas_push: DONE in ${SECS}s — new=$NEW updated(backed up)=$UPD deleting=$DEL (must be 0) log=$RUNLOG"
echo "$(ts) OK after ${SECS}s new=$NEW updated=$UPD deleting=$DEL mode=$MODE log=$RUNLOG" > "$STATE"
[ "$DEL" -eq 0 ] || { log "nas_push: 🔴 rsync reported $DEL deletion line(s) — this must be impossible; investigate"; exit 5; }
exit 0

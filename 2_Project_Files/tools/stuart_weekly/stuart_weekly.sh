#!/bin/bash
# stuart_weekly.sh - the Monday list for Kam's meeting with Stuart, built unattended (claim stuart-weekly-monday-list).
#
# WHY (Kam, live board 2026-11-23 10:22:08): "create a formatted PDF that I can easily reference during the meeting. Also create a weekly
# schedule to create this list every Monday morning by 10am and post on fleet activity card for me with link to download".
# launchd fires it Monday 08:00 Australia/Sydney (scheduler/jobs/stuartweekly.plist.template, Wednesday seat only) so a slow run still lands by 10:00.
#
# Pipeline (each step failing is LOUD: one panel line to Kam naming the step and the log, stderr kept in the log):
#   fetch    linear_fetch.py: READ-ONLY snapshot of Secuura board team KS (the key is read in-process, never printed, never given to the model)
#   stage    decision cards mentioning Stuart/Peter, the top NEXT-PICKUP block, the golden shape, last week's items -> a staging dir on the INTERNAL disk
#   research headless `claude -p` (Sonnet, read-only tools Read/Grep/Glob, cwd = the staging dir) follows commission_research.md and prints items.md + layout
#   layout   stuart_lib.py split: splits and VALIDATES both documents (the model writes the layout too: ask/why per item needs judgement, a converter would only reformat)
#   render   2_Project_Files/tools/md2pdf/md2pdf.sh (rc 0 and a page count, else failure)
#   share    the PDF into the live board file drawer (dashboard-cloud/seat/share_file.py, as chat_reply.sh --file does) -> file_id
#   card     ONE fleet-activity card (decision_queue.sh add --json) with the download link; then commit the dated folder by pathspec
#
# MEASURED 2026-11-23 (launchd probe, see the commission report): `claude -p` run from launchd WORKS (auth via the Max login, ~3 s) ONLY if it never
# touches the DRIVE: with cwd or --add-dir on /Volumes/DevMASTER it hung until killed (45 s and 60 s watchdogs). Hence the staging dir on the internal
# disk, claude's cwd there, and a watchdog on every claude run. (Cause unmeasured; the symptom is.)
#
# Usage: stuart_weekly.sh [--dry] [--no-post] [--date YYYY-MM-DD] [--out-base DIR] [--force-day] [--redo] [--fail-step fetch|research|render|share|card]
#   --dry        research + layout + render only: NO share, NO card, NO commit (prints the card it would post)
#   --no-post    a failure PRINTS the panel line instead of sending it
#   --date       the Monday to build for (default: today, Australia/Sydney); a non-Monday is refused unless --force-day
#   --out-base   where <date>_stuart-meeting-items/ is made (default 0_Brain/reference); test runs point this at a scratch dir
#   --redo       ignore a previous run's .research_ok (re-run the research)
#   --fail-step  TEST HOOK: make that one step fail for real (bogus input), to prove the loud-failure path
# Idempotent: refuses (exit 0, one log line) if the dated folder has .card_posted OR the decision store already holds the week's card.
# A retry after a late failure re-uses .research_ok (items.md + layout are kept) and .share_id (the file is shared once).
# Exit: 0 posted / dry ok / quiet refusal - 1 a step failed (panel line sent) - 3 a step failed AND the panel line itself could not be sent.
# bash 3.2 compatible (macOS /bin/bash): no associative arrays, no timeout(1).
set -u
export TZ="${TZ:-Australia/Sydney}"
# PATH ORDER MATTERS (measured 2026-11-23 under launchd): Homebrew's python3 (Python.app) HANGS reading a file on the drive, Apple's /usr/bin/python3 does not.
# So the system dirs come first and Homebrew (pandoc) last; every python3 this script or the tools it calls resolve to /usr/bin/python3.
export PATH="/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin"
SELF="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF/../../.." && pwd)"
TOOLS="$PROJECT_DIR/2_Project_Files/tools"
STATE="$SELF/state"; mkdir -p "$STATE"
PY="/usr/bin/env python3 -I"
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
RESEARCH_TIMEOUT="${STUART_RESEARCH_TIMEOUT:-1500}"

DRY=0; NOPOST=0; DATE=""; OUTBASE="$PROJECT_DIR/0_Brain/reference"; FORCEDAY=0; REDO=0; FAILSTEP="${STUART_FAIL_STEP:-}"; DATE_GIVEN=0
while [ $# -gt 0 ]; do
  case "$1" in
    --dry) DRY=1 ;; --no-post) NOPOST=1 ;; --force-day) FORCEDAY=1 ;; --redo) REDO=1 ;;
    --date) DATE="${2:-}"; DATE_GIVEN=1; shift ;;
    --out-base) OUTBASE="${2:-}"; shift ;;
    --fail-step) FAILSTEP="${2:-}"; shift ;;
    -h|--help) sed -n 2,34p "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "stuart_weekly: unknown argument '$1'" >&2; exit 2 ;;
  esac
  shift
done
[ -n "$DATE" ] || DATE="$(date +%F)"
case "$DATE" in [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) ;; *) echo "stuart_weekly: bad --date '$DATE'" >&2; exit 2 ;; esac
case "$(basename "$PROJECT_DIR" | tr '[:upper:]' '[:lower:]')" in
  wednesday) ;; *) echo "stuart_weekly: REFUSED - this job is the WEDNESDAY seat's (Secuura is Wednesday's); tree is $PROJECT_DIR" >&2; exit 2 ;;
esac
DOW="$(date -j -f %F "$DATE" +%u 2>/dev/null)" || { echo "stuart_weekly: cannot parse date $DATE" >&2; exit 2; }
MMDD="$(date -j -f %F "$DATE" +%m%d)"
PRETTY="$(date -j -f %F "$DATE" '+%a %d %b %Y' | sed 's/^\([A-Za-z]*\) 0/\1 /')"
CARD_ID="secuura-stuart-meeting-items-$MMDD"
OUT="$OUTBASE/${DATE}_stuart-meeting-items"
LOG="$OUT/run.log"
DQ="$TOOLS/decision_queue.sh"

# wd SECS cmd...: run a command under a SIGALRM watchdog (rc 142 = timed out). Every step that touches the drive or the network goes through it: a hang under
# launchd (measured: claude and Homebrew python3 hung on the drive) must become a LOUD step failure, never a silent forever-job.
wd() { local secs="$1"; shift; perl -e 'alarm shift; exec @ARGV' "$secs" "$@"; }
note_state() { printf 'rc=%s\n' "$1" > "$STATE/last_run_rc"; date '+%Y-%m-%d %H:%M:%S %z' > "$STATE/last_run_at"; printf '%s\n' "$2" > "$STATE/last_run_note"; }

# ---- quiet refusals (before anything is created, written or paid for) -----------------------------------------------------------------------------
if [ "$DOW" != "1" ] && [ "$FORCEDAY" != 1 ]; then
  echo "stuart_weekly: $DATE is not a Monday (weekday $DOW): nothing to do (--force-day to override)" >&2; exit 0
fi
if [ -f "$OUT/.card_posted" ]; then
  echo "stuart_weekly: REFUSED (idempotent): $OUT/.card_posted exists - this Monday's card was already posted ($(cat "$OUT/.card_posted" 2>/dev/null | head -1)). Nothing done." >&2
  note_state 0 "quiet refusal $DATE: marker present"; exit 0
fi
wd 60 "$DQ" show "$CARD_ID" >/dev/null 2>&1; SHOWRC=$?
[ "$SHOWRC" = 142 ] && echo "stuart_weekly: WARN: decision_queue show timed out (60s); relying on the .card_posted marker and the store's own duplicate-id refusal" >&2
if [ "$SHOWRC" = 0 ]; then
  echo "stuart_weekly: REFUSED (idempotent): the decision store already holds card $CARD_ID. Nothing done." >&2
  note_state 0 "quiet refusal $DATE: card $CARD_ID already exists"; exit 0
fi
LOCK="$STATE/lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "stuart_weekly: REFUSED: another run holds $LOCK (pid $(cat "$LOCK/pid" 2>/dev/null)). If it is stale (no such process), move that directory aside." >&2; exit 0
fi
echo $$ > "$LOCK/pid"
STAGE=""
cleanup() { rm -f "$LOCK/pid"; rmdir "$LOCK" 2>/dev/null; sleep 0.3; }
trap cleanup EXIT

mkdir -p "$OUT" || { echo "stuart_weekly: cannot create $OUT" >&2; exit 2; }
exec > >(tee -a "$LOG") 2>&1
echo "=== stuart_weekly $(date '+%F %T %z') date=$DATE dry=$DRY no_post=$NOPOST fail_step='${FAILSTEP}' out=$OUT pid=$$ ==="

# ---- loud failure ------------------------------------------------------------------------------------------------------------------------------------
fail() {
  local step="$1"; shift
  local line="Stuart weekly list FAILED at step '$step' for $DATE: $*. Log: $LOG"
  echo "FAILED step=$step: $*"
  note_state 1 "FAILED step=$step $DATE: $*"
  if [ "$NOPOST" = 1 ]; then
    echo "WOULD SEND PANEL LINE (chat_reply.sh --project Secuura): $line"
    exit 1
  fi
  if wd 150 "$TOOLS/chat_reply.sh" --project Secuura "$line"; then
    echo "panel line sent"; exit 1
  fi
  echo "PANEL LINE COULD NOT BE SENT (chat_reply rc!=0) - this log and the launchd err log are the only record"; exit 3
}
want_fail() { [ "$FAILSTEP" = "$1" ]; }

# ---- steps 1-4: skipped when a previous run of THIS Monday already produced the documents ------------------------------------------------------
ITEMS="$OUT/items.md"; LAYOUT="$OUT/Stuart-meeting-$DATE.md"; PDF="$OUT/Stuart-meeting-$DATE.pdf"
if [ -f "$OUT/.research_ok" ] && [ "$REDO" != 1 ] && [ -s "$ITEMS" ] && [ -s "$LAYOUT" ]; then
  echo "research: re-using this Monday's earlier result ($OUT/.research_ok); --redo to re-run"
else
  STAGE="$(mktemp -d "${TMPDIR:-/tmp}/stuart_weekly.XXXXXX")" || fail stage "cannot make a staging dir on the internal disk"
  echo "stage: $STAGE (internal disk: claude must not touch the drive under launchd)"

  # 1 fetch
  if want_fail fetch; then export STUART_LINEAR_ENV="/nonexistent/forced-fail.env"; echo "(forced: fetch reads a bogus env path)"; fi
  wd 900 $PY "$SELF/linear_fetch.py" "$STAGE"; FRC=$?
  [ "$FRC" = 0 ] || fail fetch "Linear snapshot failed (rc $FRC$([ "$FRC" = 142 ] && echo ', TIMEOUT')): see the log for the reason"

  # 2 stage
  : > "$STAGE/extra_ids.txt"
  PRIOR="$(ls -d "$OUTBASE"/*_stuart-meeting-items 2>/dev/null | sort | while read -r d; do b="$(basename "$d")"; [ "${b%%_*}" \< "$DATE" ] && echo "$d"; done | tail -1)"
  [ -n "$PRIOR" ] && [ -f "$PRIOR/items.md" ] && { cp "$PRIOR/items.md" "$STAGE/prior_items.md"; /usr/bin/grep -o 'secuura-[a-z0-9-]*-[0-9]\{4\}' "$PRIOR/items.md" | sort -u > "$STAGE/extra_ids.txt"; echo "stage: prior week = $PRIOR"; }
  $PY "$SELF/stuart_lib.py" cards "$PROJECT_DIR/0_Brain/dashboard/data/decisions.json" "$STAGE" 21 "$STAGE/extra_ids.txt" || fail stage "decision-card staging failed"
  awk '/^## /{n++} n==1{print} n>1{exit}' "$PROJECT_DIR/0_Brain/tasks/NEXT-PICKUP.md" | head -60 > "$STAGE/next_pickup_top.md"
  [ -s "$STAGE/next_pickup_top.md" ] || fail stage "NEXT-PICKUP.md top block is empty or unreadable"
  cp "$SELF/golden/items.md" "$STAGE/golden_items.md"; cp "$SELF/golden/layout.md" "$STAGE/golden_layout.md"; cp "$SELF/commission_research.md" "$STAGE/commission_research.md"
  {
    echo "today: $DATE ($PRETTY)"; echo "weekday: Monday"; echo "meeting date to put on the documents: $PRETTY"
    echo "staged_at: $(date '+%F %T %z')"; echo "decision_store_card_for_this_week: $CARD_ID (not yet posted)"
  } > "$STAGE/run_info.txt"

  # 3 research: headless claude, model id read from the checked file, never typed
  MODEL="$($PY -c 'import json,sys; print(json.load(open(sys.argv[1]))["levels"]["sonnet"]["model_id"])' "$PROJECT_DIR/0_Brain/dashboard/data/models_latest.json")" || fail research "cannot read the sonnet model id from 0_Brain/dashboard/data/models_latest.json"
  [ -n "$MODEL" ] || fail research "empty sonnet model id"
  if want_fail research; then MODEL="claude-forced-fail-0-0"; echo "(forced: bogus model id)"; fi
  [ -x "$CLAUDE_BIN" ] || fail research "claude binary not found at $CLAUDE_BIN"
  echo "research: claude -p model=$MODEL timeout=${RESEARCH_TIMEOUT}s"
  CLOG="$OUT/claude_stderr.txt"
  (
    cd "$STAGE" || exit 97
    perl -e 'alarm shift; exec @ARGV' "$RESEARCH_TIMEOUT" "$CLAUDE_BIN" -p "Read commission_research.md in the current directory and follow it exactly. Your reply is the two documents in the marker format it describes." \
      --model "$MODEL" --setting-sources user --strict-mcp-config --disable-slash-commands --no-session-persistence \
      --tools "Read,Grep,Glob" --allowedTools "Read Grep Glob" --permission-mode dontAsk --output-format text \
      < /dev/null > "$STAGE/claude_out.txt" 2> "$CLOG"
    exit $?
  )
  CRC=$?
  echo "research: claude rc=$CRC, output $(wc -c < "$STAGE/claude_out.txt" 2>/dev/null) bytes, stderr kept at $CLOG ($(wc -c < "$CLOG" 2>/dev/null) bytes)"
  [ "$CRC" = 0 ] || fail research "headless claude exited rc=$CRC$([ "$CRC" = 142 ] && echo " (TIMEOUT after ${RESEARCH_TIMEOUT}s, killed by SIGALRM)") ($(/usr/bin/grep -v '^$' "$CLOG" 2>/dev/null | tail -1 | cut -c1-220))"
  [ -s "$STAGE/claude_out.txt" ] || fail research "headless claude returned empty output"
  cp "$STAGE/claude_out.txt" "$OUT/claude_out.txt"

  # 4 layout: split + validate
  $PY "$SELF/stuart_lib.py" split "$STAGE/claude_out.txt" "$ITEMS" "$LAYOUT" "$DATE" || fail layout "the model's output failed validation (stderr above names why; raw output kept at $OUT/claude_out.txt)"
  echo "$(date '+%F %T %z') model=$MODEL" > "$OUT/.research_ok"
fi

# ---- 5 render -----------------------------------------------------------------------------------------------------------------------------------------
RIN="$LAYOUT"; want_fail render && { RIN="$OUT/forced-fail-does-not-exist.md"; echo "(forced: md2pdf is given a bogus input)"; }
RENDER_OUT="$(wd 240 "$TOOLS/md2pdf/md2pdf.sh" "$RIN" "$PDF" 2>&1)"; RRC=$?
echo "render: rc=$RRC: $RENDER_OUT"
[ "$RRC" = 0 ] || fail render "md2pdf rc=$RRC: $(printf '%s' "$RENDER_OUT" | tail -2 | tr '\n' ' ')"
PAGES="$(printf '%s' "$RENDER_OUT" | sed -n 's/.*(\([0-9][0-9]*\) pages.*/\1/p' | head -1)"
{ [ -n "$PAGES" ] && [ "$PAGES" -ge 1 ] && [ -s "$PDF" ]; } || fail render "md2pdf reported no page count / empty pdf"
echo "render: OK $PAGES page(s) $PDF"

# ---- 6/7 share + card ---------------------------------------------------------------------------------------------------------------------------------
N_ITEMS="$(/usr/bin/grep -c '^### [0-9]' "$LAYOUT")"
rel() { case "$1" in "$PROJECT_DIR"/*) printf '%s' "${1#$PROJECT_DIR/}" ;; *) printf '%s' "$1" ;; esac; }
if [ "$DRY" = 1 ]; then
  CARD_JSON="$($PY "$SELF/stuart_lib.py" card "$LAYOUT" "$CARD_ID" "<file_id from the share>" "<drawer url>" "$(rel "$ITEMS")" "$(rel "$PDF")")" || fail card "cannot build the card from the layout"
  echo "DRY: would share $PDF into the file drawer (client Secuura) and post this card (nothing sent):"
  printf '%s\n' "$CARD_JSON" | $PY -c 'import json,sys; c=json.load(sys.stdin); print(" id=%s\n title=%s\n bluf=%s\n recommended=%s options=%s" % (c["id"],c["title"],c["bluf"],c["recommended"],[o["key"]+":"+o["label"] for o in c["options"]]))'
  echo "DRY: prior-ruling gate preview (read-only):"; wd 60 "$DQ" prior --id "$CARD_ID" --client-project "Secuura/Blockchain" --title "For this week's meeting with Stuart: $N_ITEMS items, three that most need him" 2>&1 | /usr/bin/grep -E '^  CARD|MATCH|REFUS|would' | cut -c1-200 | head -8
  date '+%F %T %z' > "$OUT/.dry_complete"; note_state 0 "dry run ok $DATE: $N_ITEMS items, $PAGES pages"
  echo "=== DRY OK: $N_ITEMS items, $PAGES pages, nothing shared or posted ==="; exit 0
fi

if [ -s "$OUT/.share_id" ]; then
  FILE_ID="$(sed -n 1p "$OUT/.share_id")"; DRAWER="$(sed -n 2p "$OUT/.share_id")"; echo "share: re-using $FILE_ID from an earlier run"
else
  want_fail share && fail share "forced failure (--fail-step share)"
  SFPY="$PROJECT_DIR/2_Project_Files/dashboard-cloud/.venv/bin/python"; [ -x "$SFPY" ] || SFPY=python3
  for _try in 1 2; do
    SFOUT="$(wd 120 "$SFPY" "$PROJECT_DIR/2_Project_Files/dashboard-cloud/seat/share_file.py" "$PDF" --seat wednesday --client Secuura --cert-dir "$PROJECT_DIR/4_Credentials/dashboard-cloud" --note "Stuart meeting list $PRETTY ($N_ITEMS items)" 2>&1)"; SFRC=$?
    [ "$SFRC" = 0 ] && break
    echo "share: attempt $_try failed rc=$SFRC; $([ "$_try" = 1 ] && echo retrying once)"; sleep 20
  done
  FILE_ID="$(printf '%s\n' "$SFOUT" | /usr/bin/grep -o 'file_id=[A-Za-z0-9._-]*' | head -1 | cut -d= -f2)"
  DRAWER="$(printf '%s\n' "$SFOUT" | /usr/bin/grep -o 'drawer=[^ ]*' | head -1 | cut -d= -f2)"
  echo "share: rc=$SFRC file_id=${FILE_ID:-none} drawer=${DRAWER:-none}"
  { [ "$SFRC" = 0 ] && [ -n "$FILE_ID" ]; } || fail share "share_file.py rc=$SFRC: $(printf '%s' "$SFOUT" | tail -3 | tr '\n' ' ')"
  printf '%s\n%s\n' "$FILE_ID" "$DRAWER" > "$OUT/.share_id"
fi

CARD_JSON="$($PY "$SELF/stuart_lib.py" card "$LAYOUT" "$CARD_ID" "$FILE_ID" "$DRAWER" "$(rel "$ITEMS")" "$(rel "$PDF")")" || fail card "cannot build the card from the layout"
want_fail card && fail card "forced failure (--fail-step card); the file ($FILE_ID) IS shared, a retry re-uses it"
CARD_OUT="$(printf '%s' "$CARD_JSON" | wd 180 "$DQ" add --json 2>&1)"; CRC=$?
echo "card: add rc=$CRC: $(printf '%s' "$CARD_OUT" | tail -5)"
if [ "$CRC" != 0 ] && { [ "$CRC" = 3 ] || printf '%s' "$CARD_OUT" | /usr/bin/grep -q -i 'override-prior\|already written on this subject'; }; then
  # The prior-rulings gate refused: the week's agenda is a NEW agenda each Monday, not a repeat of an earlier ruled question.
  OVR="This is the weekly Monday agenda for Kam's meeting with Stuart on $PRETTY: a new list built from that day's board snapshot (not a repeat of an earlier ruled question). Earlier weekly cards were ruled for THEIR week's list."
  CARD_JSON2="$(printf '%s' "$CARD_JSON" | $PY -c 'import json,sys; c=json.load(sys.stdin); c["_override_prior"]=sys.argv[1]; print(json.dumps(c, ensure_ascii=False))' "$OVR")"
  CARD_OUT="$(printf '%s' "$CARD_JSON2" | wd 180 "$DQ" add --json 2>&1)"; CRC=$?
  echo "card: retry with _override_prior rc=$CRC: $(printf '%s' "$CARD_OUT" | tail -5)"
fi
[ "$CRC" = 0 ] || fail card "decision_queue add rc=$CRC: $(printf '%s' "$CARD_OUT" | tail -3 | tr '\n' ' ')"
printf '%s card=%s file_id=%s pages=%s items=%s\n' "$(date '+%F %T %z')" "$CARD_ID" "$FILE_ID" "$PAGES" "$N_ITEMS" > "$OUT/.card_posted"

# commit the dated folder by pathspec so an untracked dir never blocks panel_sync (it skips a tree dirty outside dashboard/data). Never a failure.
case "$OUT" in
  "$PROJECT_DIR"/*)
    ( git -C "$PROJECT_DIR" add -- "$(rel "$OUT")/items.md" "$(rel "$OUT")/Stuart-meeting-$DATE.md" "$(rel "$OUT")/Stuart-meeting-$DATE.pdf" "$(rel "$OUT")/.card_posted" "$(rel "$OUT")/.share_id" "$(rel "$OUT")/.research_ok" \
      && git -C "$PROJECT_DIR" commit -m "WED stuart-weekly: $DATE meeting list ($N_ITEMS items, card $CARD_ID)" -- "$(rel "$OUT")" \
      && git -C "$PROJECT_DIR" push ) || echo "WARN: committing/pushing the dated folder failed (not a job failure): commit it by hand, an untracked folder blocks panel_sync"
    ;;
esac
note_state 0 "posted $DATE: card $CARD_ID, file $FILE_ID, $N_ITEMS items, $PAGES pages"
echo "=== DONE: card $CARD_ID posted, file $FILE_ID, $N_ITEMS items, $PAGES pages ==="
exit 0

#!/bin/bash
# seat_daily_note_arms.sh — red-proof for the 2026-09-16 seat-note split (Tuesday's census 20:23 + Wednesday's
# 20:35 amendment): WEDNESDAY tree -> 0_Brain/daily/ (unchanged), TUESDAY tree -> 0_Brain/daily_tuesday/, any other
# tree REFUSED, WED_AGENT disagreeing with the tree REFUSED, speak.sh never failed by seat resolution.
# One mapping: 2_Project_Files/tools/seat_note.sh (sources fleet/cockpit/seat_resolve.sh).
#
# Runs ONLY against throwaway git trees under a mktemp dir (folders literally named WEDNESDAY / TUESDAY /
# SCRATCHTREE), never this tree's notes, git, launchd or voice: speak.sh runs with WEDNESDAY_MUTE=1 and
# WEDNESDAY_VOICE set (so not even `say -v ?` runs); the close bell runs in the scratch tree, which has no
# 4_Credentials/.env (no inbox calls) and whose speak.sh is muted. The work dir is left in place (never-delete).
#
# ARMS_SUFFIX (default empty): copy the four edited scripts from "<path>$ARMS_SUFFIX" instead — used to prove
# the arms against the staged .new files before they were moved over the originals.
set -u
SRC="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SUF="${ARMS_SUFFIX:-}"
BASE="$(cd -P "$(mktemp -d "${TMPDIR:-/tmp}/seat_daily_note_arms.XXXXXX")" && pwd)"
TODAY="$(date +%F)"
unset WED_AGENT WED_NOTE_OVERRIDE WEDNESDAY_TEST_NOTE WEDNESDAY_DRYRUN DRYRUN WEDNESDAY_SPEAK_LOCAL SPEAK_FROM_SERVER \
      WEDNESDAY_SPEAK_URGENT WEDNESDAY_TEST_HOUR AGENTMAIL_API_KEY
export WEDNESDAY_MUTE=1 WEDNESDAY_VOICE=arms-no-audio
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "PASS $1"; }
bad() { FAIL=$((FAIL+1)); echo "FAIL $1"; }
echo "work dir: $BASE  (source: $SRC${SUF:+, suffix $SUF})"

EDITED="2_Project_Files/tools/note_entry.sh 2_Project_Files/voice/speak.sh 2_Project_Files/scheduler/close_wednesday.sh 2_Project_Files/fleet/hooks/session_start_compact.sh"
make_tree() { # $1 = tree path, $2 = new|old  -> a git repo with the scripts at their real relative paths
  local t=$1 v=$2 p from
  mkdir -p "$t/0_Brain/daily" "$t/2_Project_Files/tools" "$t/2_Project_Files/voice" "$t/2_Project_Files/scheduler" \
           "$t/2_Project_Files/fleet/hooks" "$t/2_Project_Files/fleet/cockpit"
  cp -p "$SRC/0_Brain/daily/_template.md" "$t/0_Brain/daily/_template.md"
  cp -p "$SRC/2_Project_Files/fleet/cockpit/seat_resolve.sh" "$t/2_Project_Files/fleet/cockpit/seat_resolve.sh"
  [ "$v" = new ] && cp -p "$SRC/2_Project_Files/tools/seat_note.sh" "$t/2_Project_Files/tools/seat_note.sh"
  for p in $EDITED; do
    if [ "$v" = old ]; then from="$SRC/$p.pre-0916-seatnote"; else from="$SRC/$p$SUF"; fi
    cp -p "$from" "$t/$p" || echo "make_tree: copy failed: $from" >&2
  done
  printf 'logs/\nstate/\n' > "$t/2_Project_Files/scheduler/.gitignore"
  git init -q -b main "$t"
  git -C "$t" add -A
  git -C "$t" -c user.email=arms@local -c user.name=arms commit -qm "arms base"
}
from_template() { sed "s/{{date}}/$TODAY/" "$1/0_Brain/daily/_template.md" > "$2"; }
has() { [ -f "$2" ] && grep -qF -- "$1" "$2"; }       # has <text> <file>
note_entry() { local t=$1; shift; bash "$t/2_Project_Files/tools/note_entry.sh" "$@"; }
BELL_LOG() { echo "$1/2_Project_Files/scheduler/logs/close_$TODAY.log"; }
log_len() { local f; f="$(BELL_LOG "$1")"; if [ -f "$f" ]; then wc -l < "$f" | tr -d ' '; else echo 0; fi; }
log_since() { local f; f="$(BELL_LOG "$1")"; [ -f "$f" ] && tail -n +"$(( $2 + 1 ))" "$f"; }
# The arm-2 property, as a predicate so arm 8 can show it FAILS on the old scripts.
arm2_pred() { # <tree> <marker>
  has "$2" "$1/0_Brain/daily_tuesday/$TODAY.md" && ! has "$2" "$1/0_Brain/daily/$TODAY.md"
}

W="$BASE/new/WEDNESDAY"; T="$BASE/new/TUESDAY"; X="$BASE/new/SCRATCHTREE"
make_tree "$W" new; make_tree "$T" new; make_tree "$X" new
TN="$T/0_Brain/daily_tuesday/$TODAY.md"
O="$BASE/o"; mkdir -p "$O"

# ── ARM 1 (CONTROL): WEDNESDAY tree, no WED_AGENT -> 0_Brain/daily/<today>.md ──
from_template "$W" "$W/0_Brain/daily/$TODAY.md"
printf 'arm1-marker\n' | note_entry "$W" --stdin > "$O/1.out" 2>&1; rc=$?
if [ "$rc" = 0 ] && has arm1-marker "$W/0_Brain/daily/$TODAY.md" && [ ! -e "$W/0_Brain/daily_tuesday" ] \
   && [ "$(note_entry "$W" --where 2>&1)" = "$W/0_Brain/daily/$TODAY.md" ]; then
  ok "1 WEDNESDAY tree writes 0_Brain/daily/$TODAY.md, no daily_tuesday created (control)"
else bad "1 WEDNESDAY control: rc=$rc :: $(cat "$O/1.out")"; fi

# ── ARM 2a: TUESDAY tree, note not yet created -> refuses naming daily_tuesday, creates the dir, decoy untouched ──
DECOY="$T/0_Brain/daily/$TODAY.md"; from_template "$T" "$DECOY"; cp -p "$DECOY" "$O/decoy.orig"   # untracked decoy
printf 'arm2a-marker\n' | note_entry "$T" --stdin > "$O/2a.out" 2>&1; rc=$?
if [ "$rc" = 2 ] && grep -qF "no note at $TN" "$O/2a.out" && [ -d "$T/0_Brain/daily_tuesday" ] && cmp -s "$DECOY" "$O/decoy.orig"; then
  ok "2a TUESDAY tree resolves 0_Brain/daily_tuesday/$TODAY.md (mkdir -p done; note absent -> refused), shared daily/ decoy untouched"
else bad "2a TUESDAY pre-note: rc=$rc :: $(cat "$O/2a.out")"; fi

# ── ARM 3a: close bell on TUESDAY creates the seat note from the shared template ──
L0=$(log_len "$T")
WEDNESDAY_TEST_HOUR=23 bash "$T/2_Project_Files/scheduler/close_wednesday.sh" > "$O/3a.out" 2>&1; rc=$?
if [ "$rc" = 0 ] && [ -f "$TN" ] && has "## 23:00 close" "$TN" && cmp -s "$DECOY" "$O/decoy.orig" \
   && log_since "$T" "$L0" | grep -q "created from template"; then
  ok "3a close bell (TUESDAY) created + stamped 0_Brain/daily_tuesday/$TODAY.md from daily/_template.md; decoy untouched"
else bad "3a bell create: rc=$rc :: $(cat "$O/3a.out") :: $(log_since "$T" "$L0" | tr '\n' ' ')"; fi
mv "$T/2_Project_Files/scheduler/state/last_close" "$T/2_Project_Files/scheduler/state/last_close.set-aside-after-3a"   # else 3b "already closed today"

# ── ARM 2: TUESDAY tree, no WED_AGENT -> writes daily_tuesday, NOT daily ──
printf 'arm2-marker\n' | note_entry "$T" --stdin > "$O/2.out" 2>&1; rc=$?
if [ "$rc" = 0 ] && arm2_pred "$T" arm2-marker && grep -qF "→ $TN" "$O/2.out"; then
  ok "2 TUESDAY tree writes 0_Brain/daily_tuesday/$TODAY.md and NOT 0_Brain/daily/$TODAY.md"
else bad "2 TUESDAY write: rc=$rc :: $(cat "$O/2.out")"; fi

# ── ARM 3b: writer and bell agree — same path, and the tracked check follows the resolved path ──
L1=$(log_len "$T")
WEDNESDAY_TEST_HOUR=23 WEDNESDAY_DRYRUN=1 bash "$T/2_Project_Files/scheduler/close_wednesday.sh" > "$O/3b1.out" 2>&1; rc1=$?
S1="$(log_since "$T" "$L1")"
git -C "$T" add "0_Brain/daily_tuesday/$TODAY.md"
git -C "$T" -c user.email=arms@local -c user.name=arms commit -qm "track tuesday note" > "$O/3b.git" 2>&1
L2=$(log_len "$T")
WEDNESDAY_TEST_HOUR=23 WEDNESDAY_DRYRUN=1 bash "$T/2_Project_Files/scheduler/close_wednesday.sh" > "$O/3b2.out" 2>&1; rc2=$?
S2="$(log_since "$T" "$L2")"
git -C "$T" ls-files --error-unmatch "0_Brain/daily/$TODAY.md" > "$O/3b.lsf" 2>&1; decoy_tracked=$?   # 1 = untracked, as intended
if [ "$rc1" = 0 ] && [ "$rc2" = 0 ] && printf '%s' "$S1" | grep -qF "would stamp $TN " \
   && [ "$(note_entry "$T" --where 2>&1)" = "$TN" ] \
   && printf '%s' "$S1" | grep -q "NOT tracked by git" && ! printf '%s' "$S2" | grep -q "NOT tracked by git" \
   && [ "$decoy_tracked" = 1 ]; then
  ok "3b bell resolves the SAME file note_entry wrote ($TN); tracked-check flags it untracked, clears once it is committed while daily/$TODAY.md stays untracked"
else bad "3b bell agreement: rc1=$rc1 rc2=$rc2 :: S1=$(printf '%s' "$S1" | tr '\n' ' ') :: S2=$(printf '%s' "$S2" | tr '\n' ' ')"; fi

# ── ARM 4: WED_NOTE_OVERRIDE wins on the TUESDAY tree ──
OV="$BASE/override_note.md"; : > "$OV"
printf 'arm4-marker\n' | WED_NOTE_OVERRIDE="$OV" note_entry "$T" --stdin > "$O/4.out" 2>&1; rc=$?
if [ "$rc" = 0 ] && has arm4-marker "$OV" && ! has arm4-marker "$TN" && ! has arm4-marker "$DECOY"; then
  ok "4 WED_NOTE_OVERRIDE wins on TUESDAY tree"
else bad "4 override: rc=$rc :: $(cat "$O/4.out")"; fi

# ── ARM 5: disagreement refuses; agreement passes; unrecognised tree refuses (WED_AGENT does not rescue it) ──
printf 'arm5a-marker\n' | WED_AGENT=wednesday note_entry "$T" --stdin > "$O/5a.out" 2>&1; rc=$?
if [ "$rc" = 2 ] && [ "$(grep -c . "$O/5a.out")" = 1 ] && grep -qF "unset WED_AGENT, or run from the matching tree" "$O/5a.out" \
   && ! has arm5a-marker "$TN" && ! has arm5a-marker "$DECOY"; then
  ok "5a WED_AGENT=wednesday on TUESDAY tree -> exit 2, one stderr line naming both fixes, nothing written"
else bad "5a disagreement: rc=$rc :: $(cat "$O/5a.out")"; fi
printf 'arm5b-marker\n' | WED_AGENT=tuesday note_entry "$T" --stdin > "$O/5b.out" 2>&1; rc=$?
if [ "$rc" = 0 ] && arm2_pred "$T" arm5b-marker; then ok "5b WED_AGENT=tuesday on TUESDAY tree -> passes (control)"
else bad "5b agreement: rc=$rc :: $(cat "$O/5b.out")"; fi
from_template "$X" "$X/0_Brain/daily/$TODAY.md"
printf 'arm5c-marker\n' | note_entry "$X" --stdin > "$O/5c.out" 2>&1; rc=$?
printf 'arm5d-marker\n' | WED_AGENT=wednesday note_entry "$X" --stdin > "$O/5d.out" 2>&1; rc2=$?
if [ "$rc" = 2 ] && [ "$rc2" = 2 ] && grep -qF "cannot tell which seat this tree is — run from a WEDNESDAY or TUESDAY tree" "$O/5c.out" \
   && grep -qF "cannot tell which seat this tree is" "$O/5d.out" && ! has arm5c-marker "$X/0_Brain/daily/$TODAY.md" \
   && ! has arm5d-marker "$X/0_Brain/daily/$TODAY.md" && [ ! -e "$X/0_Brain/daily_tuesday" ]; then
  ok "5c unrecognised tree (SCRATCHTREE) -> note_entry exit 2 with and without WED_AGENT=wednesday, nothing written"
else bad "5c unrecognised: rc=$rc rc2=$rc2 :: $(cat "$O/5c.out") :: $(cat "$O/5d.out")"; fi
L3=$(log_len "$X"); WEDNESDAY_TEST_HOUR=23 WEDNESDAY_DRYRUN=1 WED_AGENT=wednesday bash "$X/2_Project_Files/scheduler/close_wednesday.sh" > "$O/5e.out" 2>&1; rc=$?
L4=$(log_len "$T"); WEDNESDAY_TEST_HOUR=23 WEDNESDAY_DRYRUN=1 WED_AGENT=wednesday bash "$T/2_Project_Files/scheduler/close_wednesday.sh" > "$O/5f.out" 2>&1; rc2=$?
if [ "$rc" = 2 ] && [ "$rc2" = 2 ] && grep -qF "cannot tell which seat this tree is" "$O/5e.out" && log_since "$X" "$L3" | grep -q "REFUSED" \
   && grep -qF "unset WED_AGENT, or run from the matching tree" "$O/5f.out" && log_since "$T" "$L4" | grep -q "REFUSED" \
   && ! log_since "$T" "$L4" | grep -q "would stamp"; then
  ok "5d close bell refuses (exit 2, stderr + log) on the unrecognised tree and on WED_AGENT disagreement, before the stamp step"
else bad "5d bell refusals: rc=$rc rc2=$rc2 :: $(cat "$O/5e.out") :: $(cat "$O/5f.out")"; fi

# ── ARM 6: speak.sh logs into the seat's directory; never fails on resolution ──
bash "$T/2_Project_Files/voice/speak.sh" "arm6-marker" > "$O/6.out" 2> "$O/6.err"; rc=$?
if [ "$rc" = 0 ] && has arm6-marker "$T/0_Brain/daily_tuesday/.spoken.log" && ! has arm6-marker "$T/0_Brain/daily/.spoken.log" \
   && [ ! -s "$O/6.err" ] && grep -q "^\[muted\] arm6-marker" "$O/6.out"; then
  ok "6a speak.sh (muted) on TUESDAY tree logs into daily_tuesday/.spoken.log, not daily/"
else bad "6a speak: rc=$rc :: $(cat "$O/6.out" "$O/6.err")"; fi
SM="$BASE/speakmiss/TUESDAY"; make_tree "$SM" new; mv "$SM/2_Project_Files/fleet/cockpit/seat_resolve.sh" "$SM/2_Project_Files/fleet/cockpit/seat_resolve.sh.set-aside"
bash "$SM/2_Project_Files/voice/speak.sh" "arm6b-marker" > "$O/6b.out" 2> "$O/6b.err"; rc=$?
SU="$BASE/speakunread/TUESDAY"; make_tree "$SU" new; chmod 000 "$SU/2_Project_Files/tools/seat_note.sh"
bash "$SU/2_Project_Files/voice/speak.sh" "arm6c-marker" > "$O/6c.out" 2> "$O/6c.err"; rc2=$?
chmod 755 "$SU/2_Project_Files/tools/seat_note.sh"
if [ "$rc" = 0 ] && [ "$rc2" = 0 ] && grep -q "fell back to logging in the shared" "$O/6b.err" && grep -q "fell back to logging in the shared" "$O/6c.err" \
   && has arm6b-marker "$SM/0_Brain/daily/.spoken.log" && has arm6c-marker "$SU/0_Brain/daily/.spoken.log" \
   && grep -q "^\[muted\] arm6b-marker" "$O/6b.out" && grep -q "^\[muted\] arm6c-marker" "$O/6c.out"; then
  ok "6b speak.sh with MISSING seat_resolve.sh and UNREADABLE seat_note.sh -> rc 0, fallback line on stderr, logged in shared daily/"
else bad "6b speak fallback: rc=$rc rc2=$rc2 :: $(cat "$O/6b.out" "$O/6b.err" "$O/6c.out" "$O/6c.err")"; fi
WED_AGENT=wednesday bash "$T/2_Project_Files/voice/speak.sh" "arm6d-marker" > "$O/6d.out" 2> "$O/6d.err"; rc=$?
bash "$X/2_Project_Files/voice/speak.sh" "arm6e-marker" > "$O/6e.out" 2> "$O/6e.err"; rc2=$?
if [ "$rc" = 0 ] && [ "$rc2" = 0 ] && grep -q "fell back" "$O/6d.err" && grep -q "fell back" "$O/6e.err" \
   && has arm6d-marker "$T/0_Brain/daily/.spoken.log" && has arm6e-marker "$X/0_Brain/daily/.spoken.log"; then
  ok "6c speak.sh on a seat REFUSAL (disagreement; unrecognised tree) -> rc 0, fallback to shared daily/"
else bad "6c speak on refusal: rc=$rc rc2=$rc2 :: $(cat "$O/6d.err" "$O/6e.err")"; fi

# ── ARM 7: compaction hook names the seat's directory ──
HOOK=2_Project_Files/fleet/hooks/session_start_compact.sh
bash "$T/$HOOK" < /dev/null > "$O/7t.out" 2>&1; rc=$?
bash "$W/$HOOK" < /dev/null > "$O/7w.out" 2>&1; rc2=$?
bash "$X/$HOOK" < /dev/null > "$O/7x.out" 2> "$O/7x.err"; rc3=$?
WANT_W="Context was compacted. Re-ground: read CLAUDE.md boot ritual + today's 0_Brain/daily/ note before continuing."
if [ "$rc" = 0 ] && [ "$rc2" = 0 ] && grep -qF "today's 0_Brain/daily_tuesday/ note" "$O/7t.out" && [ "$(cat "$O/7w.out")" = "$WANT_W" ] \
   && [ "$rc3" = 0 ] && grep -q "WARNING" "$O/7x.out" && grep -q "cannot tell which seat" "$O/7x.out"; then
  ok "7 hook: TUESDAY -> 0_Brain/daily_tuesday/; WEDNESDAY -> byte-identical 0_Brain/daily/ line; unrecognised -> rc 0 + WARNING injected"
else bad "7 hook: rc=$rc/$rc2/$rc3 :: $(cat "$O/7t.out") :: $(cat "$O/7w.out") :: $(cat "$O/7x.out")"; fi

# ── ARM 8 (NEGATIVE): the arm-2 property against the .pre-0916-seatnote scripts reproduces the defect ──
OT="$BASE/old/TUESDAY"; make_tree "$OT" old
from_template "$OT" "$OT/0_Brain/daily/$TODAY.md"
printf 'arm8-marker\n' | note_entry "$OT" --stdin > "$O/8.out" 2>&1; rc=$?
bash "$OT/$HOOK" < /dev/null > "$O/8h.out" 2>&1
if [ "$rc" = 0 ] && ! arm2_pred "$OT" arm8-marker && has arm8-marker "$OT/0_Brain/daily/$TODAY.md" && [ ! -e "$OT/0_Brain/daily_tuesday" ] \
   && ! grep -q daily_tuesday "$O/8h.out"; then
  ok "8 NEGATIVE: old scripts on a TUESDAY tree write 0_Brain/daily/$TODAY.md (defect reproduced; arm-2 predicate FALSE; old hook names daily/)"
else bad "8 negative did not reproduce: rc=$rc :: $(cat "$O/8.out")"; fi

# ── ARM 9: cutover recorded as a fact ──
RM="$SRC/0_Brain/daily_tuesday/README.md"
CUT="$( [ -f "$RM" ] && sed -nE 's/^Cutover ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}) [A-Z]+:.*/\1/p' "$RM" | head -1 )"
if [ -n "$CUT" ] && date -j -f "%Y-%m-%d %H:%M" "$CUT" "+%s" > "$O/9.out" 2>&1 && grep -q "0_Brain/daily/<date>.md" "$RM"; then
  ok "9 daily_tuesday/README.md present, cutover '$CUT' parses (epoch $(cat "$O/9.out"))"
else bad "9 README: cut='$CUT' :: $(cat "$O/9.out" 2>/dev/null)"; fi

# ── ARM 10: no wildcard in the edited scripts could take README.md (or .spoken.log) for a note ──
GL=""
for p in $EDITED 2_Project_Files/tools/seat_note.sh; do
  f="$SRC/$p$SUF"; [ "$p" = 2_Project_Files/tools/seat_note.sh ] && f="$SRC/$p"
  hit="$(grep -nE '/\*|\*\.(md|log)' "$f" | grep -vE '^[0-9]+:[[:space:]]*#')"
  [ -n "$hit" ] && GL="$GL $p: $hit"
done
if [ -z "$GL" ]; then ok "10 no glob over a note directory in the five scripts — notes are named by exact date only"
else bad "10 glob found:$GL"; fi

# ── ARM 11: syntax of every edited script ──
SX=""
for p in $EDITED 2_Project_Files/tools/seat_note.sh 2_Project_Files/fleet/tests/seat_daily_note_arms.sh; do
  f="$SRC/$p$SUF"; case "$p" in *seat_note.sh|*seat_daily_note_arms.sh) f="$SRC/$p" ;; esac
  bash -n "$f" > "$O/11.out" 2>&1 || SX="$SX $p: $(cat "$O/11.out")"
done
if [ -z "$SX" ]; then ok "11 bash -n clean on all edited scripts"; else bad "11 bash -n:$SX"; fi

echo "RESULT: $PASS passed, $FAIL failed (work dir $BASE)"
[ "$FAIL" = 0 ]

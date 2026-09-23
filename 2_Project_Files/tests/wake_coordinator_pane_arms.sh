#!/bin/bash
# Arms for the coordinator-pane lookup in scheduler/wake_wednesday.sh.
#
# THE REGRESSION THIS GUARDS (2026-09-23 06:0x, Tuesday s82): that lookup was
# `awk -F'|' '$1=="wednesday"'`. On the Tuesday seat the coordinator pane is named
# "tuesday", so it matched NOTHING, the "live claude -> just tap it" verdict could
# never fire, and the fallback ran `cockpit.sh add wednesday <launcher>` — booting a
# SECOND coordinator while s81 was alive and working. Two seats ran ~20 min on one
# working tree. Fix: seat_resolve.sh / coord_pane_id, which already existed and whose
# header listed three callers — this script was the missed fourth.
#
# Each arm prints PASS/FAIL; exit 1 if any fail.
# ARMS_TREE (2026-09-23): run A1-A10 against another TUESDAY-named tree (e.g. a scratch copy built on the
# Studio, where the mini's T9 path does not exist). Unset = the original path, unchanged. When it is set,
# A7 (live fleet integration) is SKIPPED: the live `fleet` on the machine running the arms belongs to that
# machine's seat, not to the scratch TUESDAY tree.
P="${ARMS_TREE:-/Volumes/KK_T9_External_HDD/TUESDAY}"; F=0
pass(){ echo "PASS  $1"; }; fail(){ echo "FAIL  $1  ($2)"; F=1; }

# The pane set as it really was at 06:00, before the bug created a 'wednesday' pane.
SIM='tuesday|%0
Datasec/NexusAI-I|%44
fleet-monitor|%3'

# A1 — THE REGRESSION ARM. The old hardcoded predicate must find nothing here.
#      If this ever returns a row, someone has re-hardcoded the name.
R=$(printf '%s\n' "$SIM" | awk -F'|' '$1=="wednesday"' | head -1)
[ -z "$R" ] && pass "A1 old hardcoded 'wednesday' finds nothing on a Tuesday floor (the bug, reproduced)" \
            || fail "A1 old hardcoded predicate matched" "$R"

# A2 — the seat-resolved predicate finds the real coordinator on the same floor.
R=$(printf '%s\n' "$SIM" | awk -F'|' -v s=tuesday '$1==s' | head -1)
[ "$R" = 'tuesday|%0' ] && pass "A2 seat-resolved predicate finds tuesday|%0" \
                        || fail "A2 seat-resolved predicate" "got '$R'"

# A3 — CONTROL: Wednesday on the Studio is untouched by the fix.
R=$(printf 'wednesday|%%1\nfleet-monitor|%%3\n' | awk -F'|' -v s=wednesday '$1==s' | head -1)
[ "$R" = 'wednesday|%1' ] && pass "A3 control: seat=wednesday still resolves its own pane" \
                          || fail "A3 wednesday control" "got '$R'"

# A4 — the script no longer contains the hardcoded lookup or the hardcoded add.
W="$P/2_Project_Files/scheduler/wake_wednesday.sh"
# CODE ONLY — comments are stripped first. The fix deliberately QUOTES the old
# predicate in its explanatory comment, and the first version of this arm matched
# that comment and failed a correct file. A test that cannot tell code from a
# comment about code is not testing the thing.
# STRIP WHOLE COMMENT LINES ONLY. `sed 's/#.*//'` is wrong here and silently broke
# this arm twice: the line under test contains '#{@cockpit_name}' in a tmux format
# string, so stripping from the first '#' destroys the needle before the grep sees it.
CODE=$(/usr/bin/grep -v '^[[:space:]]*#' "$W")
NEEDLE='$1=="wednesday"'
if printf '%s\n' "$CODE" | /usr/bin/grep -qF "$NEEDLE"; then
  fail "A4 hardcoded pane predicate is back in wake_wednesday.sh (code, not comment)" "matched $NEEDLE"
else pass "A4 no hardcoded pane predicate in wake_wednesday.sh code"; fi
# POSITIVE CONTROL for A4's zero: the identical grep MUST match the pre-fix backup.
# Without it a typo in the needle turns A4 into a check that cannot fail — which is
# exactly what the first two versions of this arm were.
BK="$W.pre-0923-seatresolve"
if [ -f "$BK" ]; then
  if /usr/bin/grep -v '^[[:space:]]*#' "$BK" | /usr/bin/grep -qF "$NEEDLE"; then
    pass "A4b positive control: the identical grep DOES match the pre-fix backup"
  else fail "A4b positive control" "grep found nothing in the backup — A4's zero is not trustworthy"; fi
else echo "SKIP  A4b positive control (no pre-fix backup on disk)"; fi
if /usr/bin/grep -qi '"\$COCKPIT" add wednesday ' "$W"; then
  fail "A5 hardcoded 'cockpit.sh add wednesday' is back" "grep matched"
else pass "A5 no hardcoded 'add wednesday' in wake_wednesday.sh"; fi
# positive control for A4/A5's greps: the file must contain the seat-resolved add
/usr/bin/grep -qi '"\$COCKPIT" add "\$SEAT"' "$W" \
  && pass "A6 positive control: the seat-resolved add IS present" \
  || fail "A6 positive control" "seat-resolved add not found — A4/A5 zeros may be false"

# A7 — INTEGRATION: the real resolver against the live tmux session, if one is up.
if [ -n "${ARMS_TREE:-}" ]; then echo "SKIP  A7 live integration (ARMS_TREE is set — the live fleet is not this tree's seat)"
elif tmux has-session -t '=fleet' 2>/dev/null; then
  # shellcheck disable=SC1090
  . "$P/2_Project_Files/fleet/cockpit/seat_resolve.sh" 2>/dev/null
  if type coord_pane_id >/dev/null 2>&1; then
    seat_resolve "$P"
    if ID=$(coord_pane_id "=fleet" "$SEAT" "$TREE_SEAT" 2>/dev/null); then
      NAME=$(tmux list-panes -s -t '=fleet' -F '#{pane_id}|#{@cockpit_name}' 2>/dev/null | awk -F'|' -v i="$ID" '$1==i{print $2}')
      [ "$NAME" = "$SEAT" ] && pass "A7 live: coord_pane_id -> $ID named '$NAME' == seat '$SEAT'" \
                            || fail "A7 live: resolved pane name != seat" "id=$ID name='$NAME' seat='$SEAT'"
    else fail "A7 live: coord_pane_id refused" "seat=$SEAT"; fi
  else fail "A7 live: seat_resolve.sh not sourceable" "$P"; fi
else echo "SKIP  A7 live integration (no 'fleet' tmux session)"; fi

# ── The SECOND defect of 2026-09-23: the LAUNCHER default was the literal
#    "wednesday", and the Tuesday plist carries no WED_AGENT, so the 06:00 job
#    ran Launch_Wednesday.command out of the TUESDAY tree. Now tree-derived.
NEEDLE2='${WED_AGENT:-wednesday}'
if /usr/bin/grep -v '^[[:space:]]*#' "$W" | /usr/bin/grep -qF "$NEEDLE2"; then
  fail "A8 hardcoded launcher default is back" "matched $NEEDLE2"
else pass "A8 launcher default is not the literal 'wednesday'"; fi
if [ -f "$BK" ] && /usr/bin/grep -v '^[[:space:]]*#' "$BK" | /usr/bin/grep -qF "$NEEDLE2"; then
  pass "A8b positive control: the identical grep DOES match the pre-fix backup"
else fail "A8b positive control" "grep found nothing in the backup — A8's zero is not trustworthy"; fi

# A9 — with WED_AGENT UNSET (which is how launchd actually runs it: the plist has
#      no EnvironmentVariables at all) the Tuesday tree must resolve to tuesday.
R=$(env -u WED_AGENT bash -c '. "'"$P"'/2_Project_Files/fleet/cockpit/seat_resolve.sh"; seat_resolve "'"$P"'"; echo "$SEAT"' 2>/dev/null)
if [ "$R" = "tuesday" ] && [ -f "$P/Launch_Tuesday.command" ]; then
  pass "A9 WED_AGENT unset on the TUESDAY tree -> seat 'tuesday', Launch_Tuesday.command exists"
else fail "A9 unset-WED_AGENT resolution" "got '$R'"; fi

# A10 — CONTROL: a non-TUESDAY tree must still resolve to wednesday, so BOTH fixes
#       leave the Studio byte-identical. Uses a scratch dir; nothing is deleted.
WTREE=/private/tmp/wed_arms_tree/WEDNESDAY
mkdir -p "$WTREE"
R=$(env -u WED_AGENT bash -c '. "'"$P"'/2_Project_Files/fleet/cockpit/seat_resolve.sh"; seat_resolve "'"$WTREE"'"; echo "$SEAT"' 2>/dev/null)
[ "$R" = "wednesday" ] && pass "A10 control: a non-TUESDAY tree still resolves to 'wednesday' (Studio unchanged)" \
                       || fail "A10 wednesday tree control" "got '$R'"

# ══ FRIDAY (2026-09-23, Kam 10:49 — third coordinator seat, tree folder FRIDAY) ══════════════════════════════
# These use the resolver + wake script of THIS tree (the one the arms file lives in), scratch trees under a mktemp
# dir, and a PRIVATE tmux server (-L wake_arms_friday_$$) — never the live `fleet`; the only thing killed is that
# private server, at the end. Nothing is deleted (the work dir is left for inspection).
SRC="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RES="$SRC/2_Project_Files/fleet/cockpit/seat_resolve.sh"
FW="$(cd -P "$(mktemp -d "${TMPDIR:-/tmp}/wake_arms_friday.XXXXXX")" && pwd)"
echo "friday arms work dir: $FW"
R=$(env -u WED_AGENT bash -c '. "'"$RES"'"; for d in /x/FRIDAY /x/Friday /x/friday /x/THURSDAY /x/WEDNESDAY /x/TUESDAY; do printf "%s " "$(seat_from_tree_name "$d")"; done')
[ "$R" = "friday friday friday wednesday wednesday tuesday " ] \
  && pass "F1 seat_from_tree_name: FRIDAY/Friday/friday -> friday; THURSDAY -> wednesday (pane default only); WEDNESDAY/TUESDAY unchanged" \
  || fail "F1 seat_from_tree_name" "got '$R'"
R=$(env -u WED_AGENT bash -c '. "'"$RES"'"; seat_resolve /x/FRIDAY; echo "$SEAT/$TREE_SEAT"; WED_AGENT=wednesday; seat_resolve /x/WEDNESDAY; echo "$SEAT/$TREE_SEAT"')
[ "$R" = "$(printf 'friday/friday\nwednesday/wednesday')" ] && pass "F2 seat_resolve: FRIDAY tree (WED_AGENT unset) -> friday; WEDNESDAY tree -> wednesday (control)" \
  || fail "F2 seat_resolve" "got '$R'"
# THURSDAY: the pane default is wednesday BY DESIGN, so the refusal lives in every seat-owned writer; prove one.
mkdir -p "$FW/THURSDAY/2_Project_Files/tools" "$FW/THURSDAY/2_Project_Files/fleet/cockpit"
cp -p "$SRC/2_Project_Files/tools/seat_note.sh" "$FW/THURSDAY/2_Project_Files/tools/"; cp -p "$RES" "$FW/THURSDAY/2_Project_Files/fleet/cockpit/"
env -u WED_AGENT bash -c '. "'"$FW"'/THURSDAY/2_Project_Files/tools/seat_note.sh"; seat_note_dir "'"$FW"'/THURSDAY" arms' > "$FW/F3.out" 2>&1; rc=$?
[ "$rc" = 2 ] && /usr/bin/grep -qi 'REFUSED' "$FW/F3.out" && pass "F3 THURSDAY tree: seat_note_dir REFUSES (rc 2) — an unknown tree is never a seat" \
  || fail "F3 THURSDAY refusal" "rc=$rc $(cat "$FW/F3.out")"

# F4 — coord_pane_id on a PRIVATE tmux server.
REAL_TMUX="$(command -v tmux || echo /opt/homebrew/bin/tmux)"; SOCK="wake_arms_friday_$$"
printf '#!/bin/bash\nexec %s -L %s "$@"\n' "$REAL_TMUX" "$SOCK" > "$FW/tmux"; chmod +x "$FW/tmux"
export TMUX_BIN="$FW/tmux"
"$TMUX_BIN" new-session -d -s scratch -n main ": /x/FRIDAY/Launch_Friday.command; sleep 600"
PA="$("$TMUX_BIN" list-panes -t scratch:0 -F '#{pane_id}' | head -1)"
PB="$("$TMUX_BIN" split-window -t scratch:0 -P -F '#{pane_id}' -d ": /x/WEDNESDAY/Launch_Wednesday.command; sleep 600")"
nm() { if [ "$2" = "-" ]; then "$TMUX_BIN" set -p -u -t "$1" @cockpit_name; else "$TMUX_BIN" set -p -t "$1" @cockpit_name "$2"; fi; }
cpi() { bash -c '. "'"$RES"'"; coord_pane_id scratch:0 "$1" "$2"' _ "$1" "$2" 2>"$FW/cpi.err" || echo REFUSED; }
nm "$PA" friday; nm "$PB" -
[ "$(cpi friday friday)" = "$PA" ] && pass "F4a seat=friday finds the pane named 'friday'" || fail "F4a" "$(cat "$FW/cpi.err")"
nm "$PA" wednesday
[ "$(cpi friday friday)" = "$PA" ] && pass "F4b seat=friday on a FRIDAY tree adopts the legacy 'wednesday' pane started from …/FRIDAY/Launch_Friday.command" \
  || fail "F4b legacy adoption" "$(cat "$FW/cpi.err")"
[ "$(cpi friday wednesday)" = "REFUSED" ] && pass "F4c seat=friday from a WEDNESDAY tree does NOT adopt the legacy pane (g1)" || fail "F4c" "adopted"
nm "$PA" -; nm "$PB" wednesday
[ "$(cpi friday friday)" = "REFUSED" ] && /usr/bin/grep -qi "not a 'friday' tree" "$FW/cpi.err" \
  && pass "F4d seat=friday REFUSES a legacy 'wednesday' pane started from a WEDNESDAY tree (g2)" || fail "F4d" "$(cat "$FW/cpi.err")"
[ "$(cpi wednesday wednesday)" = "$PB" ] && pass "F4e control: seat=wednesday still finds its 'wednesday' pane" || fail "F4e" "$(cat "$FW/cpi.err")"
nm "$PB" -; nm "$PA" friday
[ "$(cpi wednesday wednesday)" = "REFUSED" ] && pass "F4f seat=wednesday never cross-adopts a 'friday' pane" || fail "F4f" "adopted a friday pane"
"$TMUX_BIN" kill-server > "$FW/killserver.out" 2>&1
unset TMUX_BIN

# F5 — wake_wednesday.sh on a FRIDAY tree refuses BY NAME (the laptop has no scheduled jobs); WEDNESDAY tree control
# reaches the DRYRUN line. A stub `date` pins the hour to 08 so the 06:00-12:00 window guard is not the thing tested.
mkdir -p "$FW/bin"
printf '#!/bin/bash\nif [ "$*" = "+%%H" ]; then echo 08; else exec /bin/date "$@"; fi\n' > "$FW/bin/date"; chmod +x "$FW/bin/date"
for t in FRIDAY WEDNESDAY; do
  mkdir -p "$FW/$t/2_Project_Files/scheduler" "$FW/$t/2_Project_Files/fleet/cockpit"
  cp -p "$SRC/2_Project_Files/scheduler/wake_wednesday.sh" "$FW/$t/2_Project_Files/scheduler/"; cp -p "$RES" "$FW/$t/2_Project_Files/fleet/cockpit/"
  : > "$FW/$t/Launch_Wednesday.command"; : > "$FW/$t/Launch_Friday.command"
  env -u WED_AGENT PATH="$FW/bin:$PATH" WEDNESDAY_DRYRUN=1 bash "$FW/$t/2_Project_Files/scheduler/wake_wednesday.sh" > "$FW/F5_$t.out" 2>&1; echo "$?" > "$FW/F5_$t.rc"
done
FL="$(cat "$FW"/FRIDAY/2_Project_Files/scheduler/logs/wake_*.log 2>/dev/null)"; WL="$(cat "$FW"/WEDNESDAY/2_Project_Files/scheduler/logs/wake_*.log 2>/dev/null)"
if [ "$(cat "$FW/F5_FRIDAY.rc")" = 1 ] && printf '%s' "$FL" | /usr/bin/grep -q "REFUSED: seat friday" && [ ! -f "$FW/FRIDAY/2_Project_Files/scheduler/state/last_wake" ] \
   && [ "$(cat "$FW/F5_WEDNESDAY.rc")" = 0 ] && printf '%s' "$WL" | /usr/bin/grep -q "DRYRUN: would wake"; then
  pass "F5 wake_wednesday.sh: FRIDAY tree -> rc 1 'REFUSED: seat friday', day NOT stamped; WEDNESDAY tree control -> DRYRUN line"
else fail "F5 wake by seat" "friday rc=$(cat "$FW/F5_FRIDAY.rc") log=[$FL] :: wednesday rc=$(cat "$FW/F5_WEDNESDAY.rc") log=[$WL]"; fi
# F5b NEGATIVE: the pre-friday wake_wednesday.sh (backup) on the same FRIDAY tree does NOT name friday — F5 can fail.
OLDW="$(ls "$SRC"/2_Project_Files/scheduler/wake_wednesday.sh.pre-0923-*-friday 2>/dev/null | head -1)"
if [ -n "$OLDW" ]; then
  mkdir -p "$FW/oldw/FRIDAY/2_Project_Files/scheduler" "$FW/oldw/FRIDAY/2_Project_Files/fleet/cockpit"
  cp -p "$OLDW" "$FW/oldw/FRIDAY/2_Project_Files/scheduler/wake_wednesday.sh"; cp -p "$RES" "$FW/oldw/FRIDAY/2_Project_Files/fleet/cockpit/"
  env -u WED_AGENT PATH="$FW/bin:$PATH" WEDNESDAY_DRYRUN=1 bash "$FW/oldw/FRIDAY/2_Project_Files/scheduler/wake_wednesday.sh" > "$FW/F5b.out" 2>&1
  if ! cat "$FW"/oldw/FRIDAY/2_Project_Files/scheduler/logs/wake_*.log | /usr/bin/grep -q "REFUSED: seat friday"; then
    pass "F5b NEGATIVE: the pre-friday wake_wednesday.sh does not produce the by-name refusal F5 asserts"
  else fail "F5b negative" "old script already names friday — F5 cannot fail"; fi
else fail "F5b negative" "no wake_wednesday.sh.pre-0923-*-friday backup"; fi

exit $F

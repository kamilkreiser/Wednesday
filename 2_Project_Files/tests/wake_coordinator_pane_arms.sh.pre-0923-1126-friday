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
P=/Volumes/KK_T9_External_HDD/TUESDAY; F=0
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
if tmux has-session -t '=fleet' 2>/dev/null; then
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

exit $F

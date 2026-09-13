#!/bin/bash
# resolver_test.sh — drives coord_pane_id (seat_resolve.sh) on a SCRATCH tmux
# server (-L resolver_test, session "scratch") and dry-runs arm_wake_watch.sh's
# DEAD path with stubs. Touches nothing in the real `fleet` session: the only
# calls against it are read-only list-panes, taken before and after as proof.
# macOS bash 3.2 safe. Never cd; absolute paths only.
set -u
OUT="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REAL_TMUX=/opt/homebrew/bin/tmux
LIVE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit
SOCK=resolver_test
WORK="$OUT/.testwork"; rm -rf "$WORK"; mkdir -p "$WORK"
FAILS=0
pass() { echo "PASS  $*"; }
fail() { echo "FAIL  $*"; FAILS=$((FAILS + 1)); }
check() { # <label> <expected> <actual>
  if [ "$2" = "$3" ]; then pass "$1 -> '$3'"; else fail "$1 -> expected '$2', got '$3'"; fi
}

# ── fleet BEFORE (read-only) ─────────────────────────────────────────────────
FLEET_BEFORE="$("$REAL_TMUX" list-panes -s -t '=fleet' -F '#{pane_id}' 2>/dev/null | tr '\n' ' ')"
FLEET_BEFORE_N="$(printf '%s' "$FLEET_BEFORE" | wc -w | tr -d ' ')"
echo "fleet panes BEFORE: n=$FLEET_BEFORE_N ids=[$FLEET_BEFORE]"

# ── scratch tmux wrapper: every tmux call the resolver makes goes to -L $SOCK ──
cat > "$WORK/tmux" <<EOF
#!/bin/bash
exec $REAL_TMUX -L $SOCK "\$@"
EOF
chmod +x "$WORK/tmux"
export TMUX_BIN="$WORK/tmux"
"$TMUX_BIN" kill-server 2>/dev/null || true
# pane A: start command names a TUESDAY-tree launcher (never executed: ':' ignores args)
"$TMUX_BIN" new-session -d -s scratch -n main ": /scratch/TUESDAY/Launch_Wednesday.command; sleep 300"
A="$("$TMUX_BIN" list-panes -t scratch:0 -F '#{pane_id}' | head -1)"
# pane B: plain
B="$("$TMUX_BIN" split-window -t scratch:0 -P -F '#{pane_id}' -d "sleep 300")"
# pane C: start command names a WEDNESDAY-tree launcher
C="$("$TMUX_BIN" split-window -t scratch:0 -P -F '#{pane_id}' -d ": /scratch/WEDNESDAY/Launch_Wednesday.command; sleep 300")"
echo "scratch panes: A=$A (TUESDAY-tree start cmd) B=$B C=$C (WEDNESDAY-tree start cmd)"
name() { # <pane> <name|-> : '-' unsets
  if [ "$2" = "-" ]; then "$TMUX_BIN" set -p -u -t "$1" @cockpit_name 2>/dev/null; else "$TMUX_BIN" set -p -t "$1" @cockpit_name "$2"; fi
}

. "$OUT/seat_resolve.sh"
ERR="$WORK/err"
resolve() { # <seat> <tree> -> prints id or "REFUSED"; stderr kept in $ERR
  local r; r="$(coord_pane_id scratch:0 "$1" "$2" 2>"$ERR")" || r=REFUSED; printf '%s' "$r"
}
errhas() { grep -q -- "$1" "$ERR"; }

# (1) seat=wednesday, pane wednesday -> found
name "$A" wednesday; name "$B" fleet-monitor; name "$C" -
check "arm1 seat=wednesday tree=wednesday, pane 'wednesday'" "$A" "$(resolve wednesday wednesday)"

# (2) seat=tuesday, pane tuesday -> found
name "$A" tuesday
check "arm2 seat=tuesday tree=tuesday, pane 'tuesday'" "$A" "$(resolve tuesday tuesday)"

# (3) seat=tuesday, pane 'wednesday' only, tree-seat=tuesday -> found via legacy fallback (the mini tonight)
name "$A" wednesday
check "arm3 seat=tuesday tree=tuesday, pane 'wednesday' only (legacy fallback)" "$A" "$(resolve tuesday tuesday)"

# (4) seat=tuesday, no coordinator pane -> refuses naming both names
name "$A" fleet-monitor
r="$(resolve tuesday tuesday)"
if [ "$r" = REFUSED ] && errhas "'tuesday'" && errhas "'wednesday'"; then pass "arm4 seat=tuesday, no pane -> REFUSED naming both: $(cat "$ERR")"; else fail "arm4 got '$r' err: $(cat "$ERR")"; fi

# (5) seat=wednesday, pane 'tuesday' only -> refuses (no cross-adoption)
name "$A" tuesday
r="$(resolve wednesday wednesday)"
if [ "$r" = REFUSED ] && errhas "'wednesday'" && ! errhas "or legacy"; then pass "arm5 seat=wednesday, pane 'tuesday' only -> REFUSED: $(cat "$ERR")"; else fail "arm5 got '$r' err: $(cat "$ERR")"; fi

# (5b) guard g1: WED_AGENT=tuesday on a WEDNESDAY tree with a 'wednesday' pane -> refuses (Wednesday's pane is not Tuesday's)
name "$A" wednesday
r="$(resolve tuesday wednesday)"
if [ "$r" = REFUSED ] && errhas "this tree's seat is 'wednesday'"; then pass "arm5b seat=tuesday tree=wednesday, pane 'wednesday' -> REFUSED (g1): $(cat "$ERR")"; else fail "arm5b got '$r' err: $(cat "$ERR")"; fi

# (5c) guard g2: tree=tuesday, seat=tuesday, but the only 'wednesday' pane was STARTED from a WEDNESDAY tree -> refuses
name "$A" -; name "$C" wednesday
r="$(resolve tuesday tuesday)"
if [ "$r" = REFUSED ] && errhas "started from tree 'WEDNESDAY'"; then pass "arm5c legacy pane started from a WEDNESDAY tree -> REFUSED (g2): $(cat "$ERR")"; else fail "arm5c got '$r' err: $(cat "$ERR")"; fi
name "$C" -

# (5d) exact name beats legacy when both exist
name "$A" tuesday; name "$B" wednesday
check "arm5d both 'tuesday' and 'wednesday' present, seat=tuesday -> exact wins" "$A" "$(resolve tuesday tuesday)"
name "$B" fleet-monitor

# (6) arm_wake_watch.sh DEAD invocation — literal grep + dry-run of the runner body with stubs
n_live="$(grep -c '\^wednesday|' "$LIVE/arm_wake_watch.sh")"
n_new="$(grep -c '\^wednesday|' "$OUT/arm_wake_watch.sh")"
if [ "$n_live" -ge 1 ] && [ "$n_new" -eq 0 ]; then pass "arm6a literal '^wednesday|' live=$n_live patched=$n_new"; else fail "arm6a literal '^wednesday|' live=$n_live patched=$n_new"; fi
# scratch tree named TUESDAY so the runner resolves seat=tuesday from the tree alone (no WED_AGENT in its env)
TREE="$WORK/TUESDAY"; HERE="$TREE/2_Project_Files/fleet/cockpit"; mkdir -p "$HERE/state" "$HERE/logs"
cp "$OUT/seat_resolve.sh" "$HERE/"
cat > "$HERE/wake_watch.sh" <<'EOF'
#!/bin/bash
# stub: first call = the DEAD wake exactly as wake_watch.sh prints it; later calls idle (the test kills the runner)
if [ -f "$(dirname "$0")/state/.called" ]; then sleep 1; exit 0; fi
touch "$(dirname "$0")/state/.called"
echo "WAKE: pane 'tuesday' DEAD — Context limit reached; the coordinator cannot act — respawn required"
EOF
cat > "$HERE/wednesday_rotate.sh" <<'EOF'
#!/bin/bash
# stub: record how we were invoked; refuse (rc 3) so the runner takes the short branch
echo "invoked: WED_AGENT=${WED_AGENT:-<unset>} args=$*" >> "$(dirname "$0")/state/rotate_calls"
exit 3
EOF
chmod +x "$HERE/wake_watch.sh" "$HERE/wednesday_rotate.sh"
LOG="$HERE/logs/wake_watch_runner.log"; PROJECT_DIR="$TREE"
RAW="$(sed -n "/^RUNNER='\$/,/^'\$/p" "$OUT/arm_wake_watch.sh" | sed '1d;$d')"
[ -n "$RAW" ] || fail "arm6b could not extract RUNNER body from the patched file"
eval "RUNNER='$RAW'"   # the same evaluation arm_wake_watch.sh performs (HERE/LOG/TMUX_BIN/PROJECT_DIR substituted)
if bash -n -c "$RUNNER" 2>"$ERR"; then pass "arm6b runner body parses (bash -n)"; else fail "arm6b runner body does NOT parse: $(cat "$ERR")"; fi
grep -q 'WED_AGENT="$SEAT" "'"$HERE"'"/wednesday_rotate.sh --dead' <<<"$RUNNER" && pass "arm6c constructed DEAD command carries WED_AGENT=\$SEAT" || fail "arm6c constructed DEAD command lacks WED_AGENT: $(grep -n 'wednesday_rotate.sh --dead' <<<"$RUNNER")"
grep -q 'coord_pane_id fleet:0' <<<"$RUNNER" && pass "arm6d tap target resolved via coord_pane_id" || fail "arm6d tap target not via coord_pane_id"
# dry-run: sleep neutralised, unset WED_AGENT so the tree decides, stub wake_watch fires DEAD once
( unset WED_AGENT; exec bash -c "sleep(){ :; }; $RUNNER" ) >"$WORK/runner.out" 2>&1 &
RPID=$!
i=0; while [ $i -lt 30 ] && [ ! -s "$HERE/state/rotate_calls" ]; do /bin/sleep 0.5; i=$((i + 1)); done
kill "$RPID" 2>/dev/null; wait "$RPID" 2>/dev/null
if grep -q 'invoked: WED_AGENT=tuesday args=--dead' "$HERE/state/rotate_calls" 2>/dev/null; then pass "arm6e dry-run: --dead was called with WED_AGENT=tuesday (resolved from the TUESDAY tree): $(cat "$HERE/state/rotate_calls")"; else fail "arm6e dry-run: rotate stub saw: $(cat "$HERE/state/rotate_calls" 2>/dev/null) / runner out: $(tail -5 "$WORK/runner.out")"; fi
grep -q 'runner seat=tuesday (tree seat tuesday)' "$WORK/runner.out" && pass "arm6f runner logged its seat line" || fail "arm6f runner seat line missing: $(head -3 "$WORK/runner.out")"
grep -q 'DEAD coordinator (tuesday) detected' "$WORK/runner.out" && pass "arm6g runner matched the DEAD wake shape without the literal wednesday" || fail "arm6g DEAD case not matched: $(cat "$WORK/runner.out")"

# (7) bash -n on the three patched copies + the resolver
for f in wednesday_rotate.sh wake_watch.sh arm_wake_watch.sh seat_resolve.sh; do
  if bash -n "$OUT/$f" 2>"$ERR"; then pass "arm7 bash -n $f"; else fail "arm7 bash -n $f: $(cat "$ERR")"; fi
done

# (8) Studio parity, READ-ONLY against the live fleet: the live awk lookup and the resolver agree for seat=wednesday
LIVE_AWK="$("$REAL_TMUX" list-panes -s -t '=fleet' -F '#{@cockpit_name}|#{pane_id}' 2>/dev/null | awk -F'|' -v s=wednesday '$1==s' | head -1)"; LIVE_AWK="${LIVE_AWK#*|}"
NEW_ID="$(TMUX_BIN="$REAL_TMUX" coord_pane_id '=fleet' wednesday wednesday 2>"$ERR" || echo REFUSED)"
if [ -n "$LIVE_AWK" ]; then check "arm8 live fleet, seat=wednesday: live awk vs resolver (read-only)" "$LIVE_AWK" "$NEW_ID"; else echo "SKIP  arm8 no live fleet session on this machine"; fi

# ── teardown + fleet AFTER ──────────────────────────────────────────────────
"$TMUX_BIN" kill-server 2>/dev/null || true
if "$REAL_TMUX" -L "$SOCK" has-session 2>/dev/null; then fail "scratch tmux server still alive"; else pass "scratch tmux server (-L $SOCK) killed"; fi
FLEET_AFTER="$("$REAL_TMUX" list-panes -s -t '=fleet' -F '#{pane_id}' 2>/dev/null | tr '\n' ' ')"
FLEET_AFTER_N="$(printf '%s' "$FLEET_AFTER" | wc -w | tr -d ' ')"
echo "fleet panes AFTER:  n=$FLEET_AFTER_N ids=[$FLEET_AFTER]"
check "fleet pane list unchanged (count+ids)" "$FLEET_BEFORE_N:$FLEET_BEFORE" "$FLEET_AFTER_N:$FLEET_AFTER"
rm -rf "$WORK"
echo "FAILS=$FAILS"
exit "$FAILS"

#!/bin/bash
# rotate_liveness_arms.sh — red-proof for the two 2026-09-20 rotation-guard defects:
#   D1  the liveness checker produced no verdict (40 real armings, 15 verdicts;
#       9 armings and 0 verdicts after 2026-09-18 00:54:09) -> wednesday_rotate.sh
#       now DOUBLE FORKS the checker so it reparents to launchd (ppid 1) before the
#       respawn, and writes a PENDING MARKER that only a logged verdict clears.
#   D2  the check asked "is the pane id still present?" and called that aliveness.
#       %124 was a bare shell at 16:03:26 and passed -> pane_agent_live.sh.
#
# SCRATCH ONLY. Unique session name per run; BOTH rotate test hooks are always set
# (ROTATE_TMUX_SESSION + ROTATE_LAUNCH_CMD) so nothing real is ever launched, and the
# liveness stubs are always provided so speak.sh / chat_reply.sh are never reached.
# Never touches the "fleet" session — and asserts so at the end.
#
# EVERY ARM HAS A NEGATIVE CONTROL: the pre-fix script is run against the SAME planted
# state and must give the WRONG answer. An arm that passes on both is not an arm.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CK="$HERE/../cockpit"
TMUX_BIN=$(command -v tmux || echo /opt/homebrew/bin/tmux)
S="livearms_$$"
STAR=$(printf '\342\234\263')          # U+2733 ✳ — Claude's activity-line marker
OLD_LIVENESS="$CK/rotate_liveness.sh.pre-0920-paneliveness"
OLD_ROTATE="$CK/wednesday_rotate.sh.pre-0920-noverdict"
LOG="$CK/logs/rotate_wednesday.log"
STATE="$CK/state"
TMP="$(mktemp -d /tmp/rotate_liveness_arms.XXXXXX)"
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "ARM PASS  $1"; }
bad() { FAIL=$((FAIL+1)); echo "ARM FAIL  $1"; }
live(){ TMUX_BIN="$TMUX_BIN" bash "$CK/pane_agent_live.sh" "$1" </dev/null; echo $?; }
guard_pane(){ case "$1" in %[0-9]*) return 0 ;; *) echo "SETUP FAIL: '$1' is not a pane id"; cleanup; exit 2 ;; esac; }
logmark(){ wc -l < "$LOG" | tr -d ' '; }                 # lines before an action
since(){ tail -n "+$(( $1 + 1 ))" "$LOG"; }              # only what that action wrote

cleanup() {
  "$TMUX_BIN" kill-session -t "=$S" 2>/dev/null
  [ -n "${CLPID:-}" ] && kill "$CLPID" 2>/dev/null
  # Quarantine, never delete (2026-08-26): the arms' own alarm/pending files move to a
  # dated subdir, out of doctor.sh's -maxdepth 1 view. They name a scratch session, so
  # doctor would ignore them anyway; this just keeps state/ readable.
  Q="$STATE/_arms_quarantine_$(date +%F)"; mkdir -p "$Q"
  for f in "$STATE"/ROTATE_LOSS_*.txt "$STATE"/rotate_pending_*.txt "$STATE"/consumed_rotate_pending_*.txt "$STATE"/rotate_liveness_*.pid; do
    [ -e "$f" ] || continue
    head -1 "$f" 2>/dev/null | /usr/bin/grep -q -i -- "session '$S'" && mv "$f" "$Q/" 2>/dev/null
  done
  case "$Q" in */_arms_quarantine_*) rmdir "$Q" 2>/dev/null ;; esac   # only if empty
}
trap cleanup EXIT

"$TMUX_BIN" has-session -t "=$S" 2>/dev/null && { echo "scratch session $S exists — refusing to reuse"; exit 2; }

# ── REAL-FLEET GUARD (2026-09-17: an empty -t target renamed the live coordinator
# pane and blinded the watcher for ten minutes). Snapshot now, assert at the end.
REAL_BEFORE=$("$TMUX_BIN" list-panes -t "fleet:0" -F '#{pane_id}=#{@cockpit_name}' 2>/dev/null | sort)

# ── planted state ──────────────────────────────────────────────────────────
#  P1 coordinator (respawned by the rotation)   P2 LIVE agent (claude + ✳ title)
#  P3 agent FALLEN TO A SHELL (the %124 shape)  P4 fleet-monitor (legitimate shell)
#  P5 claude process but NO ✳ title             P6 ✳ title but NO claude process
MARK="exited — pane stays for inspection"
"$TMUX_BIN" new-session -d -s "$S" -x 300 -y 200 "bash -c \"echo '[cockpit] wednesday $MARK'; exec bash\""
P1=$("$TMUX_BIN" list-panes -t "=$S" -F '#{pane_id}' | head -1); guard_pane "$P1"
"$TMUX_BIN" set-option -p -t "${P1:?}" @cockpit_name wednesday
P2=$("$TMUX_BIN" split-window -d -P -F '#{pane_id}' -t "${P1:?}" "bash -c \"(exec -a claude sleep 600)\"")
P3=$("$TMUX_BIN" split-window -d -P -F '#{pane_id}' -t "${P1:?}" "bash")
P4=$("$TMUX_BIN" split-window -d -P -F '#{pane_id}' -t "${P1:?}" "bash")
P5=$("$TMUX_BIN" split-window -d -P -F '#{pane_id}' -t "${P1:?}" "bash -c \"(exec -a claude sleep 600)\"")
P6=$("$TMUX_BIN" split-window -d -P -F '#{pane_id}' -t "${P1:?}" "bash")
for v in P2 P3 P4 P5 P6; do eval "x=\$$v"; guard_pane "$x"; done
"$TMUX_BIN" set-option -p -t "${P2:?}" @cockpit_name Secuura/Blockchain
"$TMUX_BIN" set-option -p -t "${P3:?}" @cockpit_name Secuura/Blockchain-BOARD
"$TMUX_BIN" set-option -p -t "${P4:?}" @cockpit_name fleet-monitor
"$TMUX_BIN" set-option -p -t "${P5:?}" @cockpit_name QA/notitle
"$TMUX_BIN" set-option -p -t "${P6:?}" @cockpit_name QA/staletitle
"$TMUX_BIN" select-pane -t "${P1:?}" -T "$STAR Wednesday boot"
"$TMUX_BIN" select-pane -t "${P2:?}" -T "$STAR Ultrathink"
"$TMUX_BIN" select-pane -t "${P3:?}" -T "Kamils-Mac-Studio.local"
"$TMUX_BIN" select-pane -t "${P4:?}" -T "Kamils-Mac-Studio.local"
"$TMUX_BIN" select-pane -t "${P5:?}" -T "Kamils-Mac-Studio.local"
"$TMUX_BIN" select-pane -t "${P6:?}" -T "$STAR Ultrathink"
sleep 2

# liveness stubs — the production speak/chat_reply must never be reached from an arm
mkdir -p "$TMP/stubs"
printf '#!/bin/bash\necho "[stub-spoken] $*"\n' > "$TMP/stubs/speak.sh"
printf '#!/bin/bash\necho "[stub-panel] $*"\n' > "$TMP/stubs/chat_reply.sh"
chmod +x "$TMP/stubs"/*.sh

echo "== D2: pane_agent_live.sh — the discriminator itself =="
[ "$(live "${P2:?}")" = 0 ] && ok "A1 live agent (claude proc + ✳ title) → LIVE rc 0" || bad "A1"
[ "$(live "${P3:?}")" = 1 ] && ok "A2 pane fallen to a shell (no claude, hostname title) → NOT LIVE rc 1" || bad "A2"
[ "$(live "${P5:?}")" = 0 ] && ok "A3 claude proc but no ✳ title → LIVE (process half alone is enough)" || bad "A3"
[ "$(live "${P6:?}")" = 0 ] && ok "A4 ✳ title but no claude proc → LIVE (title half alone is enough)" || bad "A4"
[ "$(live %99999)"    = 0 ] && ok "A5 no such pane → LIVE (ignorance never alarms)" || bad "A5"
[ "$(live 'notapane')" = 0 ] && ok "A6 malformed target refused, answers LIVE (never hands tmux a bad -t)" || bad "A6"
# A7 INSTRUMENT PROOF: flip P6 from live-looking to dead and watch the answer change.
"$TMUX_BIN" select-pane -t "${P6:?}" -T "Kamils-Mac-Studio.local"; sleep 1
[ "$(live "${P6:?}")" = 1 ] && ok "A7 instrument fires: same pane, ✳ title removed → flips LIVE → NOT LIVE" || bad "A7 instrument cannot fail — A4 proved nothing"
"$TMUX_BIN" select-pane -t "${P6:?}" -T "$STAR Ultrathink"; sleep 1

echo
echo "== D2: rotate_liveness.sh integration, with its NEGATIVE CONTROL =="
BEFORE_FILE="$TMP/before.txt"
"$TMUX_BIN" list-panes -s -t "=$S" -F '#{pane_id} [#{@cockpit_name}] #{pane_title} #{pane_pid}' > "$BEFORE_FILE"
run_checker() {  # $1 = script, $2 = label ; echoes only what this run wrote to the log
  local m; m=$(logmark)
  LIVENESS_TEST=1 LIVENESS_STUB_DIR="$TMP/stubs" LIVENESS_DELAY=2 LIVENESS_LAUNCH_CMD="true" \
    WED_AGENT=wednesday bash "$1" "$S" "$BEFORE_FILE" "${P1:?}" </dev/null >/dev/null 2>&1
  since "$m"
}
NEWOUT=$(run_checker "$CK/rotate_liveness.sh" fixed)
if printf '%s' "$NEWOUT" | /usr/bin/grep -q "LIVENESS FAIL" && printf '%s' "$NEWOUT" | /usr/bin/grep -q "PRESENT BUT DEAD"; then
  ok "B1 fixed checker FAILS on a pane that is present but has fallen to a shell"
else bad "B1 — got: $(printf '%s' "$NEWOUT" | /usr/bin/grep -i liveness | head -2)"; fi
printf '%s' "$NEWOUT" | /usr/bin/grep -q -- "${P3:?}" \
  && ok "B2 the FAIL names the dead pane ${P3:?} [Secuura/Blockchain-BOARD]" || bad "B2"
printf '%s' "$NEWOUT" | /usr/bin/grep -q -- "${P4:?}" \
  && bad "B3 fleet-monitor ${P4:?} was named — a legitimate shell must NOT alarm" \
  || ok "B3 fleet-monitor (legitimate shell) did NOT alarm"
printf '%s' "$NEWOUT" | /usr/bin/grep -q "\[stub-spoken\]" && printf '%s' "$NEWOUT" | /usr/bin/grep -q "\[stub-panel\]" \
  && ok "B4 the new failure mode uses the existing speak + panel path (stubs hit, production never)" || bad "B4 the new FAIL reached the log only"
ls "$STATE"/ROTATE_LOSS_*.txt >/dev/null 2>&1 && /usr/bin/grep -l -- "session '$S'" "$STATE"/ROTATE_LOSS_*.txt >/dev/null 2>&1 \
  && ok "B5 an alarm file was written for the dead-pane FAIL" || bad "B5 no alarm file"
# B6 NEGATIVE CONTROL — the UNFIXED checker, same before-file, same panes.
if [ -x "$OLD_LIVENESS" ]; then
  OLDOUT=$(run_checker "$OLD_LIVENESS" unfixed)
  if printf '%s' "$OLDOUT" | /usr/bin/grep -q "LIVENESS OK"; then
    ok "B6 NEGATIVE CONTROL: the pre-fix checker calls the SAME state OK — the arm discriminates"
  else bad "B6 the pre-fix checker did not pass — B1 proves nothing: $(printf '%s' "$OLDOUT" | /usr/bin/grep -i liveness | head -2)"; fi
else bad "B6 $OLD_LIVENESS missing — cannot run the negative control"; fi
# B7 the fixed checker must still say OK when every agent pane really is live.
"$TMUX_BIN" list-panes -s -t "=$S" -F '#{pane_id} [#{@cockpit_name}] #{pane_title} #{pane_pid}' \
  | /usr/bin/grep -v -- "${P3:?} " > "$BEFORE_FILE"
OKOUT=$(run_checker "$CK/rotate_liveness.sh" fixed-allgood)
printf '%s' "$OKOUT" | /usr/bin/grep -q "LIVENESS OK" \
  && ok "B7 no false alarm: all agent panes live (+ fleet-monitor shell) → LIVENESS OK" \
  || bad "B7 FALSE ALARM on a healthy fleet: $(printf '%s' "$OKOUT" | /usr/bin/grep -i liveness | head -2)"

echo
echo "== D1: the checker must survive the respawn and leave a verdict =="
rotate_with() {  # $1 = rotate script ; echoes the log this rotation wrote
  local m; m=$(logmark)
  ROTATE_TMUX_SESSION="$S" ROTATE_LAUNCH_CMD="bash -c 'echo RESPAWNED-BY-ARM; exec bash'" \
    ROTATE_SELF_GIT_CHECK=0 ROTATE_LIVENESS_STUB_DIR="$TMP/stubs" \
    LIVENESS_DELAY=4 WED_AGENT=wednesday TMUX_BIN="$TMUX_BIN" \
    bash "$1" --self </dev/null >/dev/null 2>&1
  sleep 8
  since "$m"
}
NEW_ROT=$(rotate_with "$CK/wednesday_rotate.sh")
NEW_PPID=$(printf '%s' "$NEW_ROT" | sed -nE 's/.*liveness checker spawned[^=]*=[ ]*([0-9]+) +([0-9]+).*/\2/p' | tail -1)
[ "${NEW_PPID:-x}" = "1" ] \
  && ok "C1 fixed: the checker reparented out of the seat's process tree (ppid 1)" \
  || bad "C1 checker ppid='${NEW_PPID:-none}', expected 1 — the double fork did not take"
printf '%s' "$NEW_ROT" | /usr/bin/grep -qE "LIVENESS (OK|FAIL)" \
  && ok "C2 fixed: a verdict WAS logged for this arming" || bad "C2 no verdict — D1 not fixed"
printf '%s' "$NEW_ROT" | /usr/bin/grep -q "pending marker cleared" \
  && ok "C3 the pending marker was cleared by the verdict (renamed, not deleted)" || bad "C3 pending marker not cleared"
/usr/bin/grep -l -- "session '$S'" "$STATE"/consumed_rotate_pending_*.txt >/dev/null 2>&1 \
  && ok "C4 the cleared marker still exists as consumed_* (never deleted)" || bad "C4 marker vanished instead of being renamed"
# C5 NEGATIVE CONTROL — the pre-fix rotate script spawns a checker that is STILL a
# descendant of this seat. ppid must NOT be 1. This is the arm that fails without the fix.
if [ -x "$OLD_ROTATE" ]; then
  "$TMUX_BIN" set-option -p -t "$("$TMUX_BIN" list-panes -t "=$S" -F '#{pane_id} #{@cockpit_name}' | awk '$2=="wednesday"{print $1; exit}')" @cockpit_name wednesday
  OLD_ROT=$(rotate_with "$OLD_ROTATE")
  OLD_PPID=$(printf '%s' "$OLD_ROT" | sed -nE 's/.*liveness checker spawned[^=]*=[ ]*([0-9]+) +([0-9]+).*/\2/p' | tail -1)
  if [ -n "$OLD_PPID" ] && [ "$OLD_PPID" != "1" ]; then
    ok "C5 NEGATIVE CONTROL: the pre-fix spawn leaves the checker in the seat's tree (ppid $OLD_PPID ≠ 1) — C1 discriminates"
  else bad "C5 pre-fix ppid='${OLD_PPID:-none}' — if it is already 1, C1 proves nothing"; fi
else bad "C5 $OLD_ROTATE missing — cannot run the negative control"; fi

echo
echo "== D1 backstop: doctor.sh must WARN on a rotation that never reported =="
# Runs doctor.sh's OWN bytes for this leg (sed'd out of the file), with warn/ok stubbed.
LEG="$TMP/leg.sh"
DOCTOR="$HERE/../../doctor.sh"      # 2_Project_Files/fleet/tests -> 2_Project_Files
{ echo 'set -u'; echo 'warn(){ echo "WARN: $1"; }'; echo 'ok(){ echo "OK: $1"; }';
  awk '/^ROTATE_PENDING_ALL=/,/^fi$/' "$DOCTOR"; } > "$LEG"
if [ "$(/usr/bin/grep -c . "$LEG")" -lt 8 ]; then bad "D0 could not extract doctor's ROTATE_PENDING leg — the backstop is untested"; else
  FAKE="$TMP/fakeproj/2_Project_Files/fleet/cockpit/state"; mkdir -p "$FAKE"
  D1OUT=$(PROJECT_DIR="$TMP/fakeproj" bash "$LEG" 2>&1)
  printf '%s' "$D1OUT" | /usr/bin/grep -q "^OK:" && ok "D1 doctor leg: clean state → ok, no warning" || bad "D1 clean state warned: $D1OUT"
  printf 'ROTATE_PENDING - now - seat wednesday - session '"'"'fleet'"'"' - coordinator %%0\n' > "$FAKE/rotate_pending_20260920_000000.txt"
  touch -t 202609200000 "$FAKE/rotate_pending_20260920_000000.txt"
  D2OUT=$(PROJECT_DIR="$TMP/fakeproj" bash "$LEG" 2>&1)
  printf '%s' "$D2OUT" | /usr/bin/grep -q "WARN:.*UNVERIFIED" \
    && ok "D2 doctor leg: a stale marker naming session 'fleet' → WARNS the successor at boot" \
    || bad "D2 stale marker did not warn: $D2OUT"
  printf 'ROTATE_PENDING - now - seat wednesday - session '"'"'livearms_x'"'"' - coordinator %%0\n' > "$FAKE/rotate_pending_20260920_000001.txt"
  touch -t 202609200000 "$FAKE/rotate_pending_20260920_000001.txt"
  mv "$FAKE/rotate_pending_20260920_000000.txt" "$FAKE/consumed_x.txt"
  D3OUT=$(PROJECT_DIR="$TMP/fakeproj" bash "$LEG" 2>&1)
  printf '%s' "$D3OUT" | /usr/bin/grep -q "^OK:.*scratch/test" \
    && ok "D3 doctor leg: a scratch-session marker is counted, never warned on (no crying wolf)" \
    || bad "D3 scratch marker warned: $D3OUT"
fi

echo
echo "== the real fleet must be untouched =="
REAL_AFTER=$("$TMUX_BIN" list-panes -t "fleet:0" -F '#{pane_id}=#{@cockpit_name}' 2>/dev/null | sort)
[ "$REAL_BEFORE" = "$REAL_AFTER" ] && ok "Z1 the live fleet session's panes are byte-identical to the snapshot" \
  || bad "Z1 THE LIVE FLEET CHANGED: before[$REAL_BEFORE] after[$REAL_AFTER]"

echo
echo "================  $PASS passed, $FAIL failed  ================"
[ "$FAIL" -eq 0 ]

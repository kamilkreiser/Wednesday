#!/bin/bash
# exited_seat_arms.sh — red-proof for fleet/cockpit/exited_seat_check.sh and its wiring
# (wake_watch.sh leg d2, wednesday_rotate.sh --dead, cockpit.sh up stale tolerance).
# Built 2026-09-17 after Tuesday's seat exited on the mini and the watcher typed into bash for 1.5 h.
# SCRATCH ONLY: tmux session "extest"; rotate runs with BOTH test hooks (ROTATE_TMUX_SESSION +
# ROTATE_LAUNCH_CMD) so nothing real is launched. Never touches the "fleet" session.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CK="$HERE/../cockpit"
TMUX_BIN=$(command -v tmux || echo /opt/homebrew/bin/tmux)
S=extest
MARK="exited — pane stays for inspection"
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "ARM PASS $1"; }
bad() { FAIL=$((FAIL+1)); echo "ARM FAIL $1"; }
chk() { TMUX_BIN="$TMUX_BIN" bash "$CK/exited_seat_check.sh" "$1"; echo $?; }

"$TMUX_BIN" has-session -t "=$S" 2>/dev/null && { echo "scratch session $S already exists — refusing to reuse it"; exit 2; }
# REAL-FLEET GUARD (2026-09-17, learned the hard way): an EMPTY -t target makes tmux act on the pane
# RUNNING this script. The first run renamed the live coordinator pane. Snapshot the real fleet's pane
# names now and assert them unchanged at the end.
REAL_BEFORE=$("$TMUX_BIN" list-panes -t "fleet:0" -F '#{pane_id}=#{@cockpit_name}' 2>/dev/null | sort)
"$TMUX_BIN" new-session -d -s "$S" -x 200 -y 30 "bash -c \"true; echo; echo '[cockpit] wednesday $MARK'; exec bash\""
P1=$("$TMUX_BIN" list-panes -t "=$S" -F '#{pane_id}' | head -1)
"$TMUX_BIN" set-option -p -t "$P1" @cockpit_name wednesday
P2=$("$TMUX_BIN" split-window -d -P -F '#{pane_id}' -t "$P1" "bash -c \"echo '[cockpit] wednesday $MARK'; (exec -a claude sleep 600); exec bash\"")
P3=$("$TMUX_BIN" split-window -d -P -F '#{pane_id}' -t "$P1" "bash")
P4=$("$TMUX_BIN" split-window -d -P -F '#{pane_id}' -t "$P1" "bash -c \"echo 'grep \\\"$MARK\\\" is what the detector reads'; exec bash\"")
sleep 2
for v in P1 P2 P3 P4; do eval "x=\$$v"; case "$x" in %[0-9]*) ;; *) echo "SETUP FAIL: $v='$x' is not a pane id — arms would pass on a usage error"; "$TMUX_BIN" kill-session -t "=$S"; exit 2;; esac; done

# ARM1 exited seat: marker + shell, no claude → EXITED
[ "$(chk "$P1")" = 0 ] && ok "ARM1 marker + bare shell → EXITED (rc 0)" || bad "ARM1"
# ARM2 live seat PRINTING the marker, with a claude process under the pane → NOT exited
[ "$(chk "$P2")" = 1 ] && ok "ARM2 marker on screen but a claude process under the pane → alive (rc 1)" || bad "ARM2"
# ARM3 a bare shell with no marker → cannot tell → NOT exited
[ "$(chk "$P3")" = 1 ] && ok "ARM3 shell without the cockpit marker → rc 1" || bad "ARM3"
# ARM4 the marker only inside a quoted sentence, no claude → still EXITED by text+process; documents that
#      the PROCESS half is what protects a live seat (a shell with no claude IS the dead shape)
[ "$(chk "$P4")" = 0 ] && ok "ARM4 marker in prose + no claude → rc 0 (process half is the guard, stated)" || bad "ARM4"
# ARM5 no such pane → rc 1
[ "$(chk %99999)" = 1 ] && ok "ARM5 missing pane → rc 1" || bad "ARM5"
# ARM6 POSITIVE CONTROL on a REAL live seat: this coordinator's own pane has a claude process — the walk must see it
REAL=$("$TMUX_BIN" list-panes -t "fleet:0" -F '#{pane_id} #{@cockpit_name}' 2>/dev/null | awk '$2=="wednesday"{print $1; exit}')
if [ -n "$REAL" ]; then
  RP=$("$TMUX_BIN" display-message -p -t "$REAL" '#{pane_pid}')
  n=$(ps -A -o pid= -o ppid= -o comm= -o args= | awk -v r="$RP" '$2==r' | /usr/bin/grep -c -i claude)
  [ "$n" -ge 1 ] && ok "ARM6 control: the live wednesday pane has $n claude child process(es) the walk keys on" || bad "ARM6 control: no claude child seen under the live pane (the predicate could never protect a live seat)"
else echo "ARM6 SKIPPED — no live wednesday pane on this machine (run on a seat machine)"; fi

# ARM7 rotate --dead ACCEPTS the exited pane (scratch hooks: nothing real launched)
ROTATE_TMUX_SESSION="$S" ROTATE_LAUNCH_CMD="bash -c 'echo RESPAWNED-BY-ARM; exec bash'" WED_AGENT=wednesday \
  TMUX_BIN="$TMUX_BIN" bash "$CK/wednesday_rotate.sh" --dead > /tmp/exited_arms_rot.out 2>&1; RRC=$?
sleep 1
sleep 2
if [ "$RRC" = 0 ] && "$TMUX_BIN" capture-pane -p -t "$P1" -S -20 2>/dev/null | /usr/bin/grep -q RESPAWNED-BY-ARM; then
  ok "ARM7 rotate --dead on an EXITED seat → respawned (rc 0, the scratch launch ran)"
else bad "ARM7 rotate --dead rc=$RRC"; tail -5 /tmp/exited_arms_rot.out; fi

# ARM8 rotate --dead REFUSES a seat that is alive (claude under the pane), renamed to the seat name
for pid_ in $("$TMUX_BIN" list-panes -t "=$S" -F '#{pane_id} #{@cockpit_name}' | awk '$2=="wednesday"{print $1}'); do
  "$TMUX_BIN" set-option -p -t "$pid_" @cockpit_name wednesday-old
done
"$TMUX_BIN" set-option -p -t "$P2" @cockpit_name wednesday
ROTATE_TMUX_SESSION="$S" ROTATE_LAUNCH_CMD="bash -c 'echo SHOULD-NOT-RUN; exec bash'" WED_AGENT=wednesday \
  TMUX_BIN="$TMUX_BIN" bash "$CK/wednesday_rotate.sh" --dead > /tmp/exited_arms_rot2.out 2>&1; RRC2=$?
[ "$RRC2" = 3 ] && ok "ARM8 rotate --dead on a LIVE seat printing the marker → REFUSED rc 3" || { bad "ARM8 rc=$RRC2"; tail -3 /tmp/exited_arms_rot2.out; }

# ARM9 wake_watch wiring present (static): leg d2 calls the predicate and says DEAD … respawn required
/usr/bin/grep -q 'exited_seat_check.sh' "$CK/wake_watch.sh" && /usr/bin/grep -q 'session EXITED.*respawn required' "$CK/wake_watch.sh" \
  && ok "ARM9 wake_watch leg d2 wired with the runner's DEAD…respawn required wording" || bad "ARM9"
# ARM10 cockpit up tolerates STALE but not OVER THE CUT (usage_gate stubs; the COCKPIT_UP_ALLOW_STALE path)
G="$HERE/../usage_gate.sh"; T=$(mktemp -d /tmp/exited_arms_gate.XXXXXX)
old=$(date -u -v-300M +%Y-%m-%dT%H:%M:%SZ)
printf '{"agent":"arm","pct":30,"ts":"%s"}\n' "$old" > "$T/stale.json"
printf '{"agent":"arm","pct":99,"ts":"%s"}\n' "$old" > "$T/over.json"
USAGE_GATE_FILE="$T/stale.json" WED_USAGE_STOP=90 USAGE_GATE_ALLOW_STALE=1 bash "$G" >/dev/null 2>&1; a=$?
USAGE_GATE_FILE="$T/stale.json" WED_USAGE_STOP=90 bash "$G" >/dev/null 2>&1; b=$?
USAGE_GATE_FILE="$T/over.json"  WED_USAGE_STOP=90 USAGE_GATE_ALLOW_STALE=1 bash "$G" >/dev/null 2>&1; c=$?
/usr/bin/grep -q 'COCKPIT_UP_ALLOW_STALE=1' "$CK/cockpit.sh" && d=1 || d=0
echo "  gate rcs: stale+allow=$a stale=$b over+allow=$c ; up sets COCKPIT_UP_ALLOW_STALE=$d"
[ "$a" = 0 ] && [ "$b" = 4 ] && [ "$c" = 3 ] && [ "$d" = 1 ] && ok "ARM10 up: stale tolerated (0), stale refused elsewhere (4), over the cut still refused (3)" || bad "ARM10 (a gate stub format mismatch shows as a≠0 — read usage_gate.sh's parser)"

"$TMUX_BIN" kill-session -t "=$S" 2>/dev/null
REAL_AFTER=$("$TMUX_BIN" list-panes -t "fleet:0" -F '#{pane_id}=#{@cockpit_name}' 2>/dev/null | sort)
[ "$REAL_BEFORE" = "$REAL_AFTER" ] && ok "ARM11 the REAL fleet's pane names are unchanged by this run ($(echo $REAL_AFTER | tr '\n' ' '))" || bad "ARM11 REAL FLEET PANE NAMES CHANGED: before [$REAL_BEFORE] after [$REAL_AFTER]"
echo ""
echo "exited_seat_arms: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]

#!/bin/bash
# rotate_refuse_arms.sh — red-proof for wednesday_rotate.sh --self's two 2026-09-16 mechanisms (ledger w=2, the
# 01:11 refusal that sat unread 4 h 19 min): (1) a REFUSE is TAPPED at the seat's own pane through cockpit.sh say;
# (2) "HEAD not contained in origin" is met with ONE push of the seat's own repo before it is a refusal.
# Runs against a SCRATCH git repo (ROTATE_GIT_DIR, honoured only with ROTATE_TMUX_SESSION set) and the scratch tmux
# session `rtest` whose `wednesday` pane is a bash shell (cockpit.sh say reads a bash prompt as "clear" → delivered);
# never touches fleet:0 or this tree's git. Work dir is left in place (never-delete rule).
# Arms:
#   A UNPUSHED  — one local commit ahead of origin           → push OK, contained, respawns (rc 0)
#   B DIVERGED  — origin and local each hold a commit the other lacks → push FAILS (non-ff), REFUSED rc 4, TAPPED
#   C CLEAN     — contained, clean tree (the control)         → rc 0, no push attempted
#   D DIRTY     — a tracked file modified                     → REFUSED rc 4, TAPPED
set -u
FLEET=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet
ROT=$FLEET/cockpit/wednesday_rotate.sh
LOG=$FLEET/cockpit/logs/rotate_wednesday.log
TMUX_BIN=$(command -v tmux || echo /opt/homebrew/bin/tmux)
S=rtest
W=$(mktemp -d /tmp/rotate_refuse_arms.XXXXXX)
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "ARM PASS $1"; }
bad() { FAIL=$((FAIL+1)); echo "ARM FAIL $1"; }

"$TMUX_BIN" has-session -t "=$S" 2>/dev/null || "$TMUX_BIN" new-session -d -s "$S" -x 200 -y 30 bash
PANE=$("$TMUX_BIN" list-panes -t "=$S" -F '#{pane_id} #{@cockpit_name}' | awk '$2=="wednesday"{print $1}' | head -1)
if [ -z "$PANE" ]; then PANE=$("$TMUX_BIN" list-panes -t "=$S" -F '#{pane_id}' | head -1); "$TMUX_BIN" set-option -p -t "$PANE" @cockpit_name wednesday; fi
echo "scratch pane: $PANE in $S"

fresh_repo() { # $1 name → a bare origin + a clone on main with one pushed commit; prints the clone path
  local o=$W/$1.origin.git c=$W/$1
  git init -q --bare -b main "$o"
  git init -q -b main "$c"; git -C "$c" -c user.email=a@b -c user.name=arm commit -q --allow-empty -m base
  echo "base" > "$c/f.txt"; git -C "$c" add f.txt; git -C "$c" -c user.email=a@b -c user.name=arm commit -qm f
  git -C "$c" remote add origin "$o"; git -C "$c" push -q -u origin main
  echo "$c"
}
run_rotate() { # runs --self against $1 (the clone); prints rc; the log lines since the marker are in $W/last.log
  local c=$1 mark; mark="ARMS-MARK-$(date +%s%N)"; echo "$mark" >> "$LOG"
  ROTATE_TMUX_SESSION=$S ROTATE_LAUNCH_CMD='echo rotated-by-arms' ROTATE_GIT_DIR="$c" bash "$ROT" --self > "$W/rot.out" 2>&1; local rc=$?
  sed -n "/$mark/,\$p" "$LOG" > "$W/last.log"; echo "$rc"
}
tapped() { # the refusal pointer reached the scratch pane (capture) AND the log says TAPPED
  grep -q "refusal TAPPED at pane" "$W/last.log" && "$TMUX_BIN" capture-pane -p -t "$PANE" | grep -q "ROTATION REFUSED rc 4"
}

# --- A UNPUSHED ---
C=$(fresh_repo a); echo "local" >> "$C/f.txt"; git -C "$C" -c user.email=a@b -c user.name=arm commit -qam local-unpushed
rc=$(run_rotate "$C"); sleep 1
if [ "$rc" = 0 ] && grep -q "pushing the seat's OWN repo ONCE" "$W/last.log" && grep -q "push OK — re-checking containment" "$W/last.log" && grep -q "respawned OK" "$W/last.log" \
   && [ "$(git -C "$C" rev-parse HEAD)" = "$(git -C "$C" rev-parse origin/main)" ]; then ok "A UNPUSHED: pushed once, contained, respawned (rc 0)"; else bad "A UNPUSHED: rc=$rc :: $(tail -3 "$W/last.log" | tr '\n' ' ' | cut -c1-300)"; fi
sleep 2   # let the respawned scratch pane settle back to a bash prompt

# --- B DIVERGED ---
C=$(fresh_repo b)
D=$W/b.other; git clone -q "$W/b.origin.git" "$D"; echo "remote-side" >> "$D/f.txt"; git -C "$D" -c user.email=a@b -c user.name=arm commit -qam remote-only; git -C "$D" push -q origin main
echo "local-side" >> "$C/f.txt"; git -C "$C" -c user.email=a@b -c user.name=arm commit -qam local-only
rc=$(run_rotate "$C"); sleep 1
if [ "$rc" = 4 ] && grep -q "push FAILED (see log) — a genuine divergence" "$W/last.log" && grep -q "REFUSED (--self): HEAD .* after one push attempt" "$W/last.log" && tapped; then ok "B DIVERGED: push failed, REFUSED rc 4, refusal TAPPED at the pane"; else bad "B DIVERGED: rc=$rc tapped=$(tapped && echo yes || echo no) :: $(tail -3 "$W/last.log" | tr '\n' ' ' | cut -c1-300)"; fi
"$TMUX_BIN" send-keys -t "$PANE" C-c "" 2>/dev/null; "$TMUX_BIN" send-keys -t "$PANE" 'clear' Enter; sleep 1

# --- C CLEAN (control) ---
C=$(fresh_repo c)
rc=$(run_rotate "$C"); sleep 1
if [ "$rc" = 0 ] && ! grep -q "pushing the seat's OWN repo ONCE" "$W/last.log" && grep -q "respawned OK" "$W/last.log"; then ok "C CLEAN: contained, no push attempted, respawned (rc 0)"; else bad "C CLEAN: rc=$rc :: $(tail -3 "$W/last.log" | tr '\n' ' ' | cut -c1-300)"; fi
sleep 2

# --- D DIRTY ---
C=$(fresh_repo d); echo "dirty" >> "$C/f.txt"
rc=$(run_rotate "$C"); sleep 1
if [ "$rc" = 4 ] && grep -q "REFUSED (--self): working tree has uncommitted changes" "$W/last.log" && tapped; then ok "D DIRTY: REFUSED rc 4, refusal TAPPED at the pane"; else bad "D DIRTY: rc=$rc tapped=$(tapped && echo yes || echo no) :: $(tail -3 "$W/last.log" | tr '\n' ' ' | cut -c1-300)"; fi
"$TMUX_BIN" send-keys -t "$PANE" 'clear' Enter

echo "rotate_refuse_arms: $PASS passed, $FAIL failed (work dir kept: $W)"
[ "$FAIL" -eq 0 ] || exit 1
exit 0

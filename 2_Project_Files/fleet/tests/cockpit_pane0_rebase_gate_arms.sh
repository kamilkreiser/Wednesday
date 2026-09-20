#!/bin/bash
# Arms for cockpit.sh `up`: pane 0 (the coordinator seat) must wait for the tree to settle,
# exactly as add_pane does (2026-09-20 22:0x, from Kam's "look into the cockpit launch
# sequence"). Runs the REAL script copied into a scratch tree with its own .git and its own
# tmux session (COCKPIT_SESSION) — never the fleet session, never the real repo.
# No deletes anywhere (2026-08-26): each arm gets a fresh subtree under mktemp -d.
set -u
W="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
NEW="$W/2_Project_Files/fleet/cockpit/cockpit.sh"
OLD="$W/2_Project_Files/fleet/cockpit/cockpit.sh.pre-0920-2200-pane0gate"
TMUX_CMD="$(command -v tmux)"  # NOT "TMUX": that is tmux's own socket env var, and naming it so made every child call connect to the binary as a socket (first run, 2026-09-20)
PASS=0; FAIL=0; N=0
T="$(mktemp -d)"; SESS="armp0$$"
trap '"$TMUX_CMD" kill-session -t "$SESS" 2>/dev/null' EXIT

mktree() { # <script> <n entries> -> sets P (fresh project dir)
  N=$((N+1)); P="$T/proj$N"; mkdir -p "$P/2_Project_Files/fleet/cockpit" "$P/.git"
  cp "$1" "$P/2_Project_Files/fleet/cockpit/cockpit.sh"; chmod +x "$P/2_Project_Files/fleet/cockpit/cockpit.sh"
  { echo 'seat|sleep 300'; [ "$2" -ge 2 ] && echo 'monitor|sleep 300'; } > "$P/2_Project_Files/fleet/cockpit/cockpit.conf"
}
run_up() { COCKPIT_SESSION="$SESS" COCKPIT_REBASE_WAIT_MAX=6 bash "$P/2_Project_Files/fleet/cockpit/cockpit.sh" up > "$T/out" 2>&1; echo $?; }
sess_exists() { "$TMUX_CMD" has-session -t "$SESS" 2>/dev/null; }
pane_count() { "$TMUX_CMD" list-panes -t "$SESS" 2>/dev/null | wc -l | tr -d ' '; }
kill_sess() { "$TMUX_CMD" kill-session -t "$SESS" 2>/dev/null; return 0; }
ok(){ echo "  ✓ $1"; PASS=$((PASS+1)); }; bad(){ echo "  ✗ $1  [$(tr '\n' ' ' < "$T/out" | cut -c1-200)]"; FAIL=$((FAIL+1)); }

# ARM1 — CLEAN tree: up must create the session with both panes, names set
kill_sess; mktree "$NEW" 2
rc=$(run_up)
if [ "$rc" = 0 ] && sess_exists && [ "$(pane_count)" = 2 ] && "$TMUX_CMD" list-panes -t "$SESS" -F '#{@cockpit_name}' | /usr/bin/grep -q '^seat$'; then ok "ARM1-clean-up-creates-2-panes"; else bad "ARM1-clean-up rc=$rc panes=$(pane_count)"; fi
kill_sess

# ARM2 — THE FOUNDING CASE: planted rebase → pane 0 must NOT start; no session may exist
mktree "$NEW" 1; mkdir -p "$P/.git/rebase-merge"
rc=$(run_up)
if [ "$rc" != 0 ] && ! sess_exists && /usr/bin/grep -q 'mid-rebase' "$T/out"; then ok "ARM2-planted-rebase-refuses-pane0 (rc $rc)"; else bad "ARM2 rc=$rc sess=$(sess_exists && echo yes || echo no)"; fi
kill_sess

# ARM3 — NEGATIVE CONTROL: the PRE-FIX script starts pane 0 straight into the same planted rebase
mktree "$OLD" 1; mkdir -p "$P/.git/rebase-merge"
rc=$(run_up)
if [ "$rc" = 0 ] && sess_exists; then ok "ARM3-old-script-starts-into-rebase (the defect, reproduced)"; else bad "ARM3 old rc=$rc"; fi
kill_sess

# ARM4 — REGRESSION: the add path still refuses on a planted rebase (rc 7, pane count unchanged)
mktree "$NEW" 1; rc=$(run_up); [ "$rc" = 0 ] || bad "ARM4-setup up rc=$rc"
mkdir -p "$P/.git/rebase-merge"
COCKPIT_SESSION="$SESS" COCKPIT_REBASE_WAIT_MAX=6 bash "$P/2_Project_Files/fleet/cockpit/cockpit.sh" add extra 'sleep 300' > "$T/out" 2>&1; rc=$?
if [ "$rc" = 7 ] && [ "$(pane_count)" = 1 ]; then ok "ARM4-add-still-refuses-rc7"; else bad "ARM4 rc=$rc panes=$(pane_count)"; fi
kill_sess

# ARM5 — the wait RESOLVES: a rebase that clears within the window lets pane 0 start
mktree "$NEW" 1; mkdir -p "$P/.git/rebase-merge"
( sleep 2; rmdir "$P/.git/rebase-merge" ) &
rc=$(run_up); wait
if [ "$rc" = 0 ] && sess_exists && /usr/bin/grep -q 'waiting for the sync loop' "$T/out"; then ok "ARM5-wait-then-start"; else bad "ARM5 rc=$rc"; fi
kill_sess

echo; echo "cockpit pane-0 rebase-gate arms: $PASS pass, $FAIL fail  (scratch left at $T)"
[ "$FAIL" -eq 0 ]

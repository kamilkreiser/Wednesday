#!/bin/bash
# pane_agent_live.sh — is this pane running a LIVE agent, or is it merely PRESENT?
#   usage: pane_agent_live.sh <tmux pane id>
#   rc 0 = LIVE, or cannot tell (ignorance never alarms)
#   rc 1 = NOT LIVE: the pane exists but its agent is gone — a bare shell
#
# WHY (2026-09-20): rotate_liveness.sh asked "is the pane id still in the list?" and
# logged `LIVENESS OK: session alive, N/M agent panes present`. PRESENCE IS NOT
# ALIVENESS. At 16:03:26 today the rotation recorded
#     %124 [Secuura/Blockchain-BOARD] Kamils-Mac-Studio.local 49466
# and moved on: %124's agent had exited ~15 minutes earlier and the pane was a bare
# shell. The rotation's whole purpose is to notice that the fleet lost something at
# the respawn, and the one check it ran could not see a pane that had already died.
#
# THE PREDICATE — NOT LIVE only when BOTH independent sources agree, never on one
# representation (the 2026-09-09 guard lesson, the same rule exited_seat_check.sh
# follows):
#   1. PROCESS TREE: no process named `claude` (or a node running claude-code)
#      descends from the pane's CURRENT pid. This is the kernel's answer and it is
#      a property of the pane itself, not of anything printed on it.
#   2. PANE TITLE: the title carries no Claude activity marker. A live Claude pane
#      sets its title to an activity line beginning U+2733 `✳` (measured on the live
#      fleet 2026-09-20: %0/%123/%125 all `✳ …`); a shell's precmd sets it to the
#      hostname (`%1 fleet-monitor` → `Kamils-Mac-Studio.local`).
# Either source saying LIVE is enough to answer LIVE. That asymmetry is deliberate:
# a false alarm here writes a ROTATE_LOSS file, speaks to Kam and mirrors to his
# panel, so the cost of crying wolf is high and the cost of one missed shell is one
# rotation's delay.
#
# NOTE — `#{pane_current_command}` is NOT the discriminator and was measured not to
# be: on 2026-09-20 it read `zsh` for all four fleet panes, live agents included,
# because Claude Code does not take the tty's foreground process group from the
# login shell. Anything reading that field would pass every pane.
#
# WHAT THIS DOES NOT COVER (stated deliberately):
#   - A pane whose agent is PRESENT but WEDGED: a claude process that is hung, out
#     of context, or sitting on an error still answers LIVE here. This check
#     answers "is the agent still there", never "is the agent still working".
#     The context/idle/FROZEN legs of wake_watch.sh are what cover that.
#   - A pane whose agent died WITHOUT its shell resetting the title, AND whose
#     claude process is somehow still listed (a zombie parent). Both sources would
#     have to be wrong together.
#   - A pane that is BOOTING: between `respawn-pane` and the launcher reaching
#     claude there is no claude process and no `✳` title, so a booting pane reads
#     NOT LIVE. The caller is responsible for exempting panes it knows are booting
#     (rotate_liveness.sh exempts the coordinator it just respawned).
#   - Agents that are not Claude Code. The process half looks for `claude` only.
# Red-proof: fleet/tests/rotate_liveness_arms.sh (scratch tmux sessions only).
set -u
PANE="${1:?usage: pane_agent_live.sh <pane-id>}"
case "$PANE" in %[0-9]*) : ;; *) echo "pane_agent_live: refusing non-pane target '$PANE'" >&2; exit 0 ;; esac
TMUX_BIN="${TMUX_BIN:-tmux}"

# ── source 2: the pane title ───────────────────────────────────────────────
# Read first and cheaply: an activity marker is a definitive LIVE and skips the ps.
title="$("$TMUX_BIN" display-message -p -t "$PANE" '#{pane_title}' 2>/dev/null)" || exit 0
case "$title" in *"$(printf '\342\234\263')"*) exit 0 ;; esac   # U+2733 ✳ — live Claude activity line

# ── source 1: the pane's process tree ──────────────────────────────────────
pane_pid="$("$TMUX_BIN" display-message -p -t "$PANE" '#{pane_pid}' 2>/dev/null)"
case "$pane_pid" in ''|*[!0-9]*) exit 0 ;; esac                 # cannot tell = LIVE

tree="$(ps -A -o pid= -o ppid= -o comm= -o args= 2>/dev/null)" || exit 0
[ -n "$tree" ] || exit 0                                        # cannot tell = LIVE

# The walk is byte-for-byte the one exited_seat_check.sh uses (2026-09-17), so the
# two checks can never disagree about what "a claude process" is.
printf '%s\n' "$tree" | ROOT="$pane_pid" python3 -c '
import os, sys
root = os.environ["ROOT"]
kids = {}; info = {}
for line in sys.stdin:
    parts = line.split(None, 3)
    if len(parts) < 3: continue
    pid, ppid, comm = parts[0], parts[1], parts[2]
    args = parts[3] if len(parts) > 3 else ""
    kids.setdefault(ppid, []).append(pid); info[pid] = (comm, args)
def is_claude(pid):
    comm, args = info.get(pid, ("", ""))
    return os.path.basename(comm) == "claude" or "claude-code" in args or args.split()[:1] == ["claude"]
if is_claude(root): sys.exit(3)
stack = [root]; seen = set()
while stack:
    p = stack.pop()
    if p in seen: continue
    seen.add(p)
    for c in kids.get(p, []):
        if is_claude(c):
            sys.exit(3)   # a live claude under the pane
        stack.append(c)
sys.exit(0)
'
rc=$?
[ "$rc" -eq 3 ] && exit 0       # a claude process lives under the pane — LIVE
[ "$rc" -eq 0 ] && exit 1       # no claude AND no activity marker — both agree: NOT LIVE
exit 0                          # python failed — cannot tell = LIVE

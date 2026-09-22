#!/bin/bash
# Arms for the AGENT-STATE CLAIM CLAUSE in fleet/cockpit/cockpit.sh (say).
#
# WHY IT EXISTS (2026-09-23): the coordinator tapped NexusAI-I with
#   "Your turn ended 06:11 and your pane has shown no test process since, only the
#    MCP at 0% CPU. NexusAI main at origin is still c0788b1."
# sent BARE (no --mail). Every falsifiable claim in it was FALSE: the agent's jest
# was pid 8539, 11+ minutes elapsed, running in a detached worktree under the queue
# lock and therefore invisible to the single `ps -t <pane tty>` frame the sender read.
# The agent measured, found the claims false, and was about to record an authenticated
# coordinator tap as a C-148 GHOST-TEXT instance in the project's CLARIFICATIONS.
# A real tap filed as a ghost teaches an agent to ignore the next real one.
#
# The pre-existing verb clause did not catch it: it blocks taps that AUTHORISE work,
# and this one only ASSERTED. Each arm prints PASS/FAIL; exit 1 if any fail.
C=/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh; F=0
# The clause's own regex, read FROM the script so the arms cannot drift from it.
RE=$(/usr/bin/grep -o "grep -qiE '(your (pane|turn[^']*)" "$C" >/dev/null 2>&1; sed -n "s/.*grep -qiE '\(([^']*your (pane.*\)'; then/\1/p" "$C" | head -1)
[ -n "$RE" ] || RE='(your (pane|turn|session|process|shell)|no (test|jest|node|agent) process|nothing is running|you (are|appear|look) (idle|stalled|stuck|stopped)|has (not|n.t) moved|0(\.[0-9]+)?% cpu|still running|shows? no )'
t(){ if printf '%s' "$2" | grep -qiE "$RE"; then R=REFUSE; else R=ALLOW; fi
     if [ "$R" = "$3" ]; then echo "PASS  $1 ($R)"; else echo "FAIL  $1 ($R, want $3)"; F=1; fi; }

# REFUSE — the real tap, verbatim, and its siblings.
t "A1 the real 2026-09-23 tap, verbatim" 'Your turn ended 06:11 and your pane has shown no test process since, only the MCP at 0% CPU. NexusAI main at origin is still c0788b1. Report where things actually stand.' REFUSE
t "A2 idle assertion"        'You appear idle and nothing is running in your worktree.' REFUSE
t "A3 branch assertion"      'Your branch has not moved in forty minutes.' REFUSE

# ALLOW — every pointer the coordinator actually sent the same morning. These are the
# arms that keep the clause narrow; if one of them ever flips, the guard is too broad.
t "A4 inbox pointer"         'Both your questions are answered in one mail in your inbox - read it whole before step 3.' ALLOW
t "A5 correction pointer"    'Correction in your inbox about the tap you flagged - read it before you edit CLARIFICATIONS.' ALLOW
t "A6 release pointer"       'Read the RELEASE mail in your inbox and HANDOVER-S80I.md at the project root.' ALLOW
t "A7 seat notice"           '[Tuesday s82] I am the 06:00 successor and my boot is done. Write your handover, then end.' ALLOW

# A8 — the clause must be PRESENT in the script (a regression arm), with a positive
#      control against the pre-fix backup so its zero cannot be a typo's zero.
if /usr/bin/grep -qF "AGENT-STATE CLAIM CLAUSE" "$C"; then echo "PASS  A8 clause present in cockpit.sh"; else echo "FAIL  A8 clause missing"; F=1; fi
BK="$C.pre-0923-claimtap"
if [ -f "$BK" ]; then
  if /usr/bin/grep -qF "AGENT-STATE CLAIM CLAUSE" "$BK"; then echo "FAIL  A8b control: the clause is in the PRE-fix backup — backup is not pre-fix"; F=1
  else echo "PASS  A8b control: the clause is absent from the pre-fix backup, as it must be"; fi
else echo "SKIP  A8b control (no pre-fix backup on disk)"; fi
exit $F

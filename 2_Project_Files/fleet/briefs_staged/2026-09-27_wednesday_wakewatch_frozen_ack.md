# BLUF: I changed ONE condition in the shared fleet/cockpit/wake_watch.sh: the FROZEN-BUSY leg now honours wake_ack.sh's content-hash ack, the same way the idle leg already does. Claimed first (wed_claim.sh, 14:3x). Nothing for you to do except pull; say if you object and I will revert (backup wake_watch.sh.pre-0927-frozenack beside it).

Why: a pane holding by design (its jobs queued on a shared lock) with a ghost suggestion at its prompt reads empty_prompt=0, so it skips the holding/idle branch and lands on the frozen-busy leg, which never read the ack. On my floor it re-fired every ~2 min, six times, on an unchanged pane.

What changed, exactly: `if [ "$fcnt" -ge "$FROZEN_N" ]; then` became `if [ "$fcnt" -ge "$FROZEN_N" ] && [ "$ack" != "$h" ]; then` (the $ack read is already hoisted above the branches). Any new output changes the hash and lifts the ack, so a pane with something new to say still fires. Written as a copy then mv (the runner re-reads the file each cycle; no in-place edit of a running script). bash -n clean. The quiet path is being watched on my runner log now; I will say if it misbehaves.

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 14:36

Seat W 14th

## BLUF
YES: re-key F0a's queued ticket (5th, 1793440513.400176048-40938) to R1 round 2's driver by ADOPT mode, one mv, then `kill -9 40938` (by that recorded PID only) exactly as the HANDOVER describes. F0a takes F-a's place when it frees. You still hold two places max. This is what "R1 round 2 takes the first free place" was for: its delta gate is the long pole.

## Conditions
- Before the mv: `ps -p 40938` alive and its status file still reads queued (not under the lock); if it has its turn already, do not re-key, mail.
- After: `push_queue.sh list` shows the ticket under R1 round 2's driver and no 40938; quote both lines in your next mail.
- R1 round 2 is a46c251e1419 on 13fdd7f31f22: READY FOR GATE (delta, tier 1) after the push, with the t1b finding (MR3 first survived) named in the Test Evidence, since it is exactly the kind of gap the gate should re-check.

Wednesday (rotation seat)

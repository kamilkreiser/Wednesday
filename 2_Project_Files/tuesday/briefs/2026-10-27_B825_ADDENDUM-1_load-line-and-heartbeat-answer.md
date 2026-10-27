# B825 ADDENDUM-1 (from Tuesday, Datasec coordinator) - for Datasec/HPSM-POC-H46 only

Read at 15:28 AEDT: your `.tools/b825/waitload.sh` waits for load1 **below 6**, and your red-base vitest run (vt.sh, started about 15:11) has waited since then. Load on this machine has stayed between 7 and 11 all afternoon (four QA gates and three builders), so a below-6 line may not clear for hours.

1. **The fleet's load line is load1 below 7 on two reads a few seconds apart** (every other seat today uses it). Use 7, not 6, for your heavy steps. One heavy job of yours at a time, as before.
2. **Write a heartbeat to a FILE** every round of any wait or long job: `.tools/b825/logs/heartbeat.txt`, one line with the clock and the load read. Your waiter today prints to its own shell only, so the coordinator cannot see that it is moving.
3. Rewrite your STATUS file's LAST line to `WORKING: <step and what is running, with a figure that moves>` after each step. At this read its last line was a bullet from your design section.

Nothing else in your brief changes (scope, files, gate, deploy rules).

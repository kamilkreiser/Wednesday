---
date: 2026-10-28
type: preference
source: Kam, terminal 2026-10-28 ~17:5x AEDT
status: live
tier: W
---

# Track fleet capacity and keep the floor full — as many agents as the machine carries, every checkpoint

**His words, verbatim:** *"good plan. thank you. its good refinement so please track so we can make sure that we always keep as many agents active as possible. there are a lot of tickets to get through"* (just before: *"its good to see 7 or so agents active. the laptop seems to be coping"*).

**The operative case, so the headline matches it:** Wednesday is at a boot, a checkpoint, a seat's wrap, or any send, and is about to choose the next action. **Read the capacity line first.** If it says ROOM, the next action is launching the next disjoint lane (or commissioning a lane sweep if none is staged), before any lower-value work. If it says FULL, say which limit (load or memory) and do not launch.

**How to apply:**
1. **The instrument:** `2_Project_Files/fleet/capacity_status.py` prints `CAPACITY: seats N (letters) · load1 · mem free · ROOM|FULL` and appends every reading to `2_Project_Files/fleet/state/capacity_log.tsv`. It rides `send_brief.sh` (every send, beside the Spark line) and `doctor.sh` (every boot: WARN on ROOM). Arms run 2026-10-28 17:53: ROOM, FULL-load, FULL-memory, unreadable (rc 0), live (8 seats, FULL at load1 11.0).
2. **The gate is the fleet's existing launch rule:** load1 < 7, memory free >= 25% (`CAP_LOAD_MAX`, `CAP_MEM_MIN`). Waves of launches, >= 3 min apart, through a waiter.
3. **A wrap frees a seat:** in the same action as scoring a wrapped seat and closing its pane, read the capacity line and launch the next lane if ROOM.
4. **Keep a staged lane ready:** when the floor is full, the next lane sweep or brief is drafted in the background, so ROOM never waits on drafting (the Spark-queue lesson, applied to Claude seats).
5. **Report it:** the morning card carries the day's capacity summary from the log (share of readings at ROOM, peak seats).
6. **Unchanged:** the code partition (no two seats on one file), the signature classes, the QA gate, the routing table.

**Family:** [[2026-09-13_as-many-agents-as-possible-partitioned-by-code]] (the standing rule this instruments) · [[2026-10-28_never-keep-the-spark-idle-quota-and-capability-data]] (the same shape for the Spark) · [[2026-08-07_a-promise-is-not-a-mechanism]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: recorded).

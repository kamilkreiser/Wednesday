---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# Waiting and wakes

**The one idea.** A session that ends its turn stops existing until something prompts it, so every wait needs a named thing that will wake it, and every wake needs a reading of real progress before it is dismissed. Waiting is also rarely the right move at all: a finished item ships, spare capacity takes the next lane, and whatever wait remains keeps an ear on Kam's board. Silence, a live process, and a cleared marker all look like "fine" and none of them is evidence.

## The rules

1. **When I am about to tell a seat to wait on something outside its session** (a remote build, a CI run, a reply, a long job on another box): name what will prompt it when the wait ends. The forms that work are a background job that exits on completion (the harness re-invokes the seat on exit), a scheduled tick, a counterparty's mail, or my own stated tap at a stated interval. "Check back periodically" is not a mechanism. "Poll sparsely" protects the context window and "have a wake" protects the work: both are needed, and sending only the first turns a window problem into a liveness problem. `2026-09-07_an-instruction-to-wait-must-name-what-wakes.md`
2. **In the same mail, ask the seat to state its wake path back.** Watch for the tell: "the next signal from me will be…" describes what the seat will emit, not what will prompt it; those read alike and are opposites. `2026-09-07_an-instruction-to-wait-must-name-what-wakes.md`
3. **When a pane is flagged frozen or idle during a long external wait: treat it as a real alert,** not as my own instruction being obeyed. The detector and the file times settle it; my assumption does not. The watcher is the backstop, not the plan: a design that relies on the backstop firing has a rescue path, not a wake path. `2026-09-07_an-instruction-to-wait-must-name-what-wakes.md`
4. **Before acknowledging an idle wake on a seat that waits on remote work: read a figure that moves** (the waiter's last heartbeat line, a progress counter, free disk, load). Process liveness ("one shell still running", a hook process) is never enough: a live waiter is not a working waiter. If I cannot read any moving figure, I do not acknowledge; I tap the seat with a pointer asking for its heartbeat's last line. Every waiter a brief asks for must print a figure that changes, and the brief says where that heartbeat lands so the coordinator can read it. `2026-09-07_an-instruction-to-wait-must-name-what-wakes.md`
5. **When an idle wake's pane shows an API error** (connection lost, overloaded, a 5xx): it is a fleet event, not a seat event. In the same action read the tail of every live pane for the same line and tap each stalled seat. The tap is a bare factual pointer under 200 characters (what happened, when, where its status stands); the seat's own brief already says what to do next, and the tap tool refuses "carry on"-shaped wording without a mail behind it. Then verify the pane shows a running command, and note the slip against the seat's target time. `2026-11-01_one-api-outage-idles-every-mid-turn-seat-sweep-all-panes.md`
6. **When I am about to end a turn with an item that is done except for a clock** (a card's default time, "after he wakes", "at 06:30"): ship it now. A merge Kam has in effect commissioned does not wait for his sleep. Where a round-cap card is still needed on a product-green item and he has asked for the result by a time, its default is short (minutes to an hour, not the morning). `2026-11-10_never-wait-a-green-item-ships-and-every-wait-watches-the-board.md`
7. **When the floor is empty on a project Kam called a priority: that is a failure, not a pause.** At every verdict, before ending the turn, ask what else on this project an agent can do now without a ruling, sweep the board and launch the disjoint lanes. The rule is not per project: once the priority project's lanes are all launched and the machine has room (load under the launch gate, memory free, usage gate open, each measured at every checkpoint), the next free lane goes to the other backlogs in priority order, partitioned by path. Spare capacity left idle is the failure. The lesson was given to the Tuesday seat about Datasec; its index row applies it to all seats. `2026-11-10_never-wait-a-green-item-ships-and-every-wait-watches-the-board.md`
8. **Every wait I do keep has a board watcher beside it,** reading Kam's message count from the message tool's header total (not its last few rows). A timer alone is a wait with no ears. Never present a timer as diligence: say what it is waiting for and whether anything else could be done meanwhile. `2026-11-10_never-wait-a-green-item-ships-and-every-wait-watches-the-board.md`
9. **When advancing any seen-mark, watermark, baseline timestamp, cursor, offset or "handled" marker, in any tool:** advance it only to cover events that provably reached the processor (a displayed message, a fired wake, a written receipt). Never set it to "now", "latest" or "everything currently visible": that races every concurrent arrival and swallows it silently. The inbox mark-seen command is for a session baseline only (first boot, known-quiet inbox), never during active monitoring; my own outbound copies need no manual clearing. If acknowledging mid-flight is ever needed, acknowledge explicit message ids. When in doubt err toward re-firing: a duplicate tap costs one interruption, a swallow costs a silent fallback window. `2026-08-04_never-blanket-markseen-mid-monitoring.md`
10. **When a wrap says "no ANSWER by fallback": audit my own seen-state** before treating it as the agent's problem. A swallowed message is invisible from the inside and surfaces only if the other side mentions it. `2026-08-04_never-blanket-markseen-mid-monitoring.md`

## What a tool already enforces

- `2_Project_Files/fleet/cockpit/arm_wake_watch.sh` (the wake runner) advances its baseline only to the timestamp of the event that fired the wake, never to "now". It covers that runner only: the same rule for mail seen-state, notification clears, queue offsets and "handled" file moves is still mine to keep, and a manual mark-seen during monitoring is not refused.
- Nothing enforces rules 1 to 8. The lesson names a candidate (the wake-acknowledge tool refusing without a changed progress figure) as not yet built.

## The mistakes this family keeps catching

- "Wait cheaply" sent with no wake, so the seat goes dormant until someone notices.
- Acknowledging a wake because a process is alive, while the thing it waits for finished an hour ago.
- Handling one outage as a trickle of separate per-seat incidents.
- Parking a finished item behind a timer and launching nothing, with nothing watching Kam's board.
- A blanket "mark everything as seen" that swallows the one message that arrived a second earlier.
- Reading my own instruction being obeyed into what is actually an alert.

## Members

2026-08-04_never-blanket-markseen-mid-monitoring.md — When advancing any seen-mark, watermark, baseline or cursor: advance only to events that provably reached the processor, never to 'now'. mark-seen is for session baseline only, never mid-monitoring. When in doubt err toward re-fire, not swallow.
2026-09-07_an-instruction-to-wait-must-name-what-wakes.md — When telling a seat to wait: name what will WAKE it (a background job that exits, scheduled tick, mail, my stated tap) and have it say its wake path back. Before acking an idle wake on remote work, read a figure that moves; process liveness is not progress.
2026-11-01_one-api-outage-idles-every-mid-turn-seat-sweep-all-panes.md — When an idle wake shows an API error (connection lost, overloaded, 5xx): it is a fleet event. In the same action read the tail of every live pane for the same line and tap each stalled seat with a bare factual pointer under 200 characters.
2026-11-10_never-wait-a-green-item-ships-and-every-wait-watches-the-board.md — When I would end a turn with a green item parked behind a clock or the floor empty: ship it now, launch the next disjoint lane, and never keep a wait without a board watcher on Kam's messages. Spare capacity goes to other backlogs in priority order.

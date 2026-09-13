---
date: 2026-09-13
type: grant
source: Kam, terminal, 2026-09-13 14:2x AEST (mid-turn, to the 14:08 seat)
status: live — supersedes the DEFAULT of card `wed-coordinator-rotation-killed-the-fleet-1604` ("no self-rotation while any agent pane is live; ask Kam to launch the successor"); the card's check-only half becomes urgent, not optional
tier: W
---

# Rotation never blocks the work — delegate FIRST, then rotate with the agents running; and keep spinning up as many agents as the code allows

**His words, verbatim (2026-09-13 14:2x, terminal):**
> *"dont let your context rotation get in the way of finishing tasks.  You can always delegate to agents and get them to work while you rotate.  Keep the last standing rule (to spin up as many agents as necessary and to move things as fast as logical and possible) going"*

**The operative case, so the headline matches it:** Wednesday is inside the 80-90 band (or approaching it) with agents live, and is about to write "waiting for Kam to launch the successor" or to hold a launch because the seat is near its ceiling. **Stop. Neither is what he wants.** The order is: put everything in flight under a brief with a wake path (an agent, a background wait, a successor's pickup line) → write the handover → rotate. The agents keep working through the rotation; the successor picks up their mails. A seat that idles at its ceiling because rotating "might" cost the fleet has already cost the fleet the seat's remaining hours.

## Why he said it, and the instance that earned it
The 08:39 seat reached the band at 12:5x with four QA gates live, honoured the card default (no self-rotation while agents are live), and **waited ~70 minutes for Kam to launch the successor** — two `GO WITH FINDINGS` verdicts (03:08Z, 03:10Z) sat unread the whole time, and the floor was clear by 13:2x. It rotated only after his 14:0x "rotate then keep pushing". The default was written after the 16:04 loss (one loss in 63 rotations with agents live — a real risk) and it traded that risk for a certain cost: an idle coordinator with a full inbox.

## How to apply
1. **Rotation is not gated on the floor being clear.** At the band, at a safe boundary (the 08-21 conditions: no unanswered agent QUESTION, no dangling thread with Kam, durable writes pushed), self-rotate — `wednesday_rotate.sh --self`, detached — with agents live. Their mails wait in the inbox; the successor answers them.
2. **Delegate BEFORE the band, not at it.** Anything that would be "too heavy for this seat" at 70% is briefed to an agent or a drafting subagent at 60%, so that by the band the seat is coordinating, not carrying ([[2026-08-11_coordinator-not-carrier]]). A gate set, a merge brief, a lane sweep — each is a subagent's job with a file as its output.
3. **The 16:04 loss is answered by a MECHANISM, not by a hold:** the card's "check-only half" — a post-respawn liveness check (is the `fleet` tmux session still alive? are the agent panes still there?) and an automatic rebuild/alarm when it is not — is commissioned as its own agent today. Until it exists, the rotation records the pane list before and after in the handover, and the successor's first act is to compare them.
4. **The standing rule stays standing:** as many agents as the code partition allows ([[2026-09-13_as-many-agents-as-possible-partitioned-by-code]]), every disjoint lane launched, "as fast as logical and possible" — logical = a plan confirmation, a gate, a partition; possible = the allowance and the machine.
5. **Report the rotation, do not request it** ([[2026-08-07_autonomy-grant-ship-decisions]]: the grant removes the pause, not the receipt). The handover block names every live agent and what wakes each one.

**Family:** [[2026-09-02_rotate-in-the-70-80-band-conditionally]] (the band; its safety conditions stand — this file removes "no agents live" from them) · [[2026-08-21_auto-rotate-at-70pct]] (condition 4 there already said "agent sessions keep running untouched — the rotation is MY pane only") · [[2026-08-07_a-promise-is-not-a-mechanism]] (a hold is not a mechanism; the liveness check is) · [[2026-09-07_an-instruction-to-wait-must-name-what-wakes]] (every delegated thing names its wake before the seat rotates) · [[2026-08-16_an-ask-without-a-default-is-an-indefinite-hold]] ("ask Kam to launch the successor" was an ask with no default, and it held 70 minutes).

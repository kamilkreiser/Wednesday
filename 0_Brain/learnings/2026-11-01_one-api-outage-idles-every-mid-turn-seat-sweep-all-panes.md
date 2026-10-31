---
date: 2026-11-01
type: lesson
source: Tuesday s211, 01:2x — two idle wakes (M53 then G245) for one 00:55 API outage
status: live
tier: W
---

# On the FIRST idle wake that shows an API error, sweep every pane for the same error — one outage idles every seat that was mid-turn

**The case.** At 00:55 AEDT the API dropped connections. Two seats were mid-turn: M53 (B1000, the MPS V4 builder) and G245 (B1003, a tier-2 gate). Both panes ended on `API Error: Connection lost mid-response` and sat at an empty prompt. The idle detector woke Tuesday for M53 at ~01:24 and for G245 at ~01:28 — two wakes, minutes apart, for one cause. Each seat lost about 30 minutes; nothing was damaged.

**The rule.**
1. When an idle wake's pane shows `API Error` (connection lost, overloaded, 5xx), it is a fleet event, not a seat event: in the same action, read every live pane's tail for the same line (`tmux capture-pane` per pane, grep `API Error`), and tap each stalled seat.
2. The tap is a BARE FACTUAL pointer (what happened, when, where its STATUS stands). `cockpit.sh say` refuses "carry on"/"resume"-shaped wording without a mail, and projects with no mail channel have none: the seat's own brief already says what to do next. Keep it under 200 characters.
3. Verify at rung 5 (the pane shows a running command), and note the slip in the seat's target time.

**Why it matters.** The detector wakes per pane, so an outage reaches me as a trickle of separate wakes; treating each as its own incident costs one wake-cycle per seat. Related: [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (silence from an agent is a question, never an answer), [[2026-09-01_a-tap-is-a-pointer-not-a-message]].

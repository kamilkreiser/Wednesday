---
date: 2026-11-01
type: correction
source: Tuesday seat ledger, parallel-note family (w=18 on 2026-10-25 to w=61 on 2026-11-01; nine instances in s214 alone)
status: live
tier: W
---

# A note is its own message: never send a note in the same turn as any other tool call

**The rule.** A daily-note entry (`note_alone.sh`), a re-sent note, and a ledger edit that records a slip are each the ONLY tool call in their message. A wake response (a pane read, `wake_ack.sh`), a launch, a board post, a delivery mark, a pane close, a statusline read: each goes in its own message BEFORE the note, and the note is composed only after that output is on screen.

**Why.** A note written beside another call is composed before the other call's output exists, so it states results it has not seen. On 2026-11-01 one such note asserted a listener's identity ("a NexusAI test host") before the read that would show it; the read then printed nothing. `note_alone.sh` refuses these (rc 2 / rc 3, nothing written), so no false line reached the note, but every refusal is a wasted turn and the habit does not break by intention: s214 wrote a "separate messages" rule at 15:27 and broke it at 15:29, 15:39, 15:47, 16:50 and 17:53.

**The shapes it took in one seat (s214):** note + wake_ack (x3); note + a read (lsof, statusline); note + chat_reply ("record and tell" after a landing); note + decision_queue --delivered; note + pane_close; note + a background check-wait launch; and a RE-SEND of a refused note beside the ledger edit recording the refusal.

**How to apply.** After any event, the order is: act (one or more calls) -> read the output -> THEN, in a new message, the note alone -> THEN, in another message, any ledger edit. If a wake and a landing arrive together, finish the act, then note. Never "save a turn" by bundling the note.

**Diagnosis (w>=3).** The mechanism holds (the refusal); the habit does not. Raise at consolidation: compose the note LAST, alone, by routine, and consider a hook that refuses a ledger edit in the same message as a note.

Related: [[2026-10-31_never-invoke-a-write-command-to-read-what-it-would-say]] (the other "save a turn" slip).

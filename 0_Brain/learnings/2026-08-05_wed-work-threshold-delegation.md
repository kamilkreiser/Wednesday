---
date: 2026-08-05
type: preference
source: "Kam, 2026-08-05 session 2: evaluated Wednesday's recommendation and approved — 'lets implement the approach as per your reccomendation. then we can work on items while we interact on other items'"
status: live
supersedes: ""
---

# WED work splits by size: converse left, delegate chunky builds

**The rule (Kam-approved, from my own evaluated recommendation):** Wednesday's
own WED dev items route by size, so the conversation with Kam never queues
behind a build:

1. **Small rounds** (< ~15 min, single-file, instantly verifiable): Wednesday
   builds DIRECTLY. The live-steering cadence — catch → fix → screenshot in
   minutes — is a ledger-protected behaviour; do not trade it for process.
2. **Chunky items** (multi-feature rounds, new subsystems, refactors):
   delegate to a supervised background teammate while Wednesday stays
   conversational in the left column. Brief per delegation-protocol
   (verifier-first, DoD, validated facts); Wednesday does the final
   browser-E2E as verifier and scores the run on the scoreboard
   (row: "WED teammate (self-delegation)").
3. **Kam is never interrupting.** His mid-turn ideas queue cleanly; the
   correct response is fast acknowledgment + sequencing, never deferral of
   the conversation until a build finishes. (His words that triggered this:
   "I feel like I am interrupting" — the feeling itself was the bug.)

**Why (context):** coding directly filled Wednesday's window with
implementation detail and made long turns; Kam felt he was derailing work by
adding ideas. Manage-don't-do already governs other projects; this extends
the same shape to WED's own chunky work — same machinery (briefs, receipts,
scoreboard), no client-isolation stakes since it's all Wednesday's project.

**Adoption guard (go-slow):** WED-72 is the pilot. Score mechanism metrics
(overhead vs direct build, conversation latency, quality at review). Standing
only if the evidence holds — the DGM rule: adoption ≠ improvement.

**Laptop caveat (honest):** teammate visibility here is receipts + final
report, not a live cockpit pane (that's Studio tmux). WED-55
hooks-observability closes that gap later.

**Related:** [[2026-07-31_manage-dont-do]],
[[2026-08-03_context-discipline-close-before-full]],
[[2026-08-03_go-slow-earn-autonomy]], [[../skills/delegation-protocol]]

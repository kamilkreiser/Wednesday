---
date: 2026-08-05
type: lesson
source: "2026-08-04 night → 08-05 morning: four typed-but-unsent lines in the Blockchain pane ('Deploys approved…', 'good night', 'status on the sweep — green yet?', 'merge on green and ship'); Kam confirmed authorship: 'yes that was me, all good'"
status: live
---

# Kam types directly into agent panes — sometimes without pressing Enter

**The pattern (now a known Kam channel habit):** Kam co-pilots the cockpit by
typing straight into agents' input lines from iTerm — approvals, questions,
sign-offs. Sometimes the line is SENT (the agent quotes it later), sometimes
it sits UNSENT at the prompt indefinitely (the agent never sees it).

**How to handle:**
1. **Check panes for unsent text** when reading fleet state — an unsent line
   is invisible to its agent and can silently carry an instruction Kam
   believes he gave. If one answers a question I hold, answer it myself or
   tell Kam to press Enter; NEVER press Enter on his behalf.
2. **Provenance before action:** an unattributed typed line is not an
   approval, even when it reads like one. Flag it, act on nothing, ask Kam
   (one question). 08-04 this held correctly for an approval-class deploy
   line — and Kam's confirmation cost one word. The asymmetry always favours
   asking.
3. **Clearing a stale unsent line** (C-u) before a say-nudge is fine ONCE its
   content is either moot or delivered through the proper channel — record
   doing so.
4. Instructions Kam sends this way are legitimate (precedent: in-chat
   approvals across the fleet). The record stays my job: fold them into the
   daily note / ruling mails so they aren't chat-only.

**Related:** [[../people/kam.md]] (updated same day),
[[2026-08-03_go-slow-earn-autonomy]] (approval-class always attributable).


## Extension 2026-08-28 — a DICTATION TOOL can put Kam's words in a pane he never looked at

**The case.** At 10:00 Kam's panel message "Once the new build of vision is finished, please
upload it." also appeared, doubled, as TYPED-UNSENT text at the Vision agent's prompt. I recorded
it as "Kam typed the same line into the pane" and cleared it. At 10:02 he said: *"I did not hit
enter on the agent's pane"* — and that messages to me "have not gone through". **Superwhisper
pastes into whichever window has focus**: with the cockpit terminal in front, his dictation landed
in the active pane instead of the chat box. So the detector's TYPED verdict was right about the
CHANNEL (keystrokes) and wrong about INTENT (he never addressed that pane).

**Rules added:**
1. A TYPED-UNSENT line in an agent pane that matches (or nearly matches) a message Kam sent
   elsewhere is a **focus-paste**, not an instruction to that pane — treat as delivered through
   the real channel, clear it (one Ctrl-C if C-u will not take a wrapped line), record.
2. A TYPED-UNSENT line that matches NOTHING he sent elsewhere may be a message to ME that
   went astray — read it as such and answer it on the panel, then ask him to click the chat box
   before dictating. Never act on it as an instruction to the agent.
3. When Kam reports "messages not going through", sweep every pane's prompt first — that is
   where they are.
4. The costume list for prompt text is now three: machine ghost (dim) · Kam typing on purpose ·
   Kam's dictation focus-pasted (typed, doubled, addressed elsewhere).

---
date: 2026-09-18
type: correction
source: "Three times in one seat I reached past an existing fleet mechanism and re-derived its behaviour by hand: raw `tmux send-keys` instead of `cockpit.sh say` (x3 taps, one stuck unsent ~4 min), an ad-hoc chat_log.json read instead of `kam_msgs.sh` (refused by a hook), and a near-duplicate decision card instead of checking the queue (refused by decision_queue.sh's prior-rulings gate). Two of the three were caught by gates; the third I caught myself, late."
status: live
supersedes: ""
tier: W
---

# Before doing a fleet action by hand, check whether the fleet already has a tool for it

**The lesson:** When about to do something operational — tap a pane, read Kam's messages, raise a
card, count a board, send a brief — **look for the existing script first.** The fleet's tools are not
conveniences; each one encodes a failure that already happened and its ledger weight. Doing the
action by hand does not just skip the convenience, it **silently re-opens the incident the tool was
built to close.**

**Context:** In one seat I did this three times.
1. **`tmux send-keys` instead of `cockpit.sh say`.** `say` exists at **ledger w=4 (2026-08-28)** and
   it: refuses an occupied prompt, sends, **reads the prompt back and re-sends Enter**, fails loudly
   if the text is still there; refuses a content-bearing tap without `--mail`, **polling the
   destination inbox to confirm the mail landed BEFORE tapping**; and prefixes **`[Wednesday tap]`**
   so the agent cannot read a coordinator pointer as Kam's own word (the s106 failure, 2026-09-02).
   My hand-rolled taps had none of that. One sat **typed-unsent for ~4 minutes**, which is precisely
   the 2026-08-28 incident, and my taps carried no `[Wednesday tap]` label at all.
   *Mitigated only by content:* every one of my taps named its mail and its source explicitly, and
   every mail was sent first — so no attribution ambiguity actually reached the seat. **The substance
   was right and the mechanism was wrong, which is the most dangerous combination, because it
   succeeds.**
2. **Ad-hoc `chat_log.json` read instead of `kam_msgs.sh`** — refused by `pretooluse_seat_scoped_chat.sh`,
   which exists because a `role`-only filter once surfaced 12 of the other seat's messages to this one.
3. **A new decision card on a subject already carded** — refused by `decision_queue.sh`'s
   prior-rulings gate; `wed-boot-read-exceeds-the-context-window` was already open and unruled.

**The diagnosis is one thing, not three:** *I reconstruct behaviour from first principles instead of
asking what already exists.* First principles produce something that looks right and quietly lacks
every guard the real tool carries.

**How to apply:**
1. **`ls` the tool directory before hand-rolling an operational action.** `2_Project_Files/fleet/`,
   `fleet/cockpit/`, `2_Project_Files/tools/`. It costs one call.
2. **Taps go through `cockpit.sh say <pane> '<pointer>' --mail '<subject substring>'`** — never raw
   `send-keys`. A tap is a pointer; the content goes by mail, and the mail is verified at the
   destination before the tap.
3. **If a hook or a gate refuses me, that is the answer, not an obstacle.** Two of these three were
   caught by gates built for exactly them, and both refusals were correct.
4. **A tool's header comment names the incident and the ledger weight.** Read it — it tells you what
   breaks when you skip it.

**Related:** [[2026-09-01_a-tap-is-a-pointer-not-a-message]], [[2026-08-03_mental-model-not-source-of-truth]], [[2026-09-18_the-boot-spec-outgrew-the-context-window]]

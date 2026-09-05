---
date: 2026-09-02
type: correction
source: "Kam, 2026-09-02 16:32 (dashboard chat, verbatim in Discovery/00_prompt-log.md): 'I think you rotated too soon. Go back to the previous structure. 70-80% is a better number. 50% is too soon. also, this reboot should be conditional like before (naturally without the flaw.'"
status: live
supersedes: "rule 2 of 2026-09-02_the-statusline-is-the-context-instrument ('70% = rotate now') — amended the same day, by Kam"
---

# Rotate inside the 70–80% band, at a safe boundary — the only unconditional respawn is a seat that is already dead

**The operative case, so the headline matches it:** a `ctx at NN%` wake lands on my pane.
- **50% = a CHECKPOINT only** (rhythm §2): declare the default, start nothing heavy, never rotate.
- **70% = rotate at the NEXT SAFE BOUNDARY** — the 08-21 grant's conditions unchanged: no agent QUESTION unanswered or imminent, no dangling thread with Kam, everything durable and pushed (HEAD == origin), agents untouched.
- **80% = the ceiling** — the first boundary after it is the rotation; nothing new is started past it.
- **Unconditional = the DEAD case only** — the literal "Context limit reached" respawned from outside by `wednesday_rotate.sh --dead`. That is "the flaw" Kam named: a seat that could not act. Its fix stays; nothing else is unconditional.

**What happened:** after the 06:39 seat died at 100%, the 16:1x seat built the dead-seat mechanism, hardened the same-day lesson into "70% = ROTATE NOW", and rotated at 16:30 — Kam saw it as too soon. He is right about the structure: an interrupt at 70% throws away a boot that costs 43–49% on this build, and a seat that rotates on a number rather than at a boundary interrupts the flows it was told never to interrupt. The correct shape is the 08-21 one — conditional rotation in a band — with the dead-seat backstop kept.

**How to apply (built the same hour):** the watcher's 70% leg says "rotate at the next safe boundary (70–80% band)"; a new 80% leg says "ceiling — rotate at the first boundary"; `wednesday_rotate.sh --self` stays the mechanism (still refuses on a dirty tree or HEAD != origin); the 50% checkpoint ritual stands; the DEAD leg and runner respawn are untouched.

**Related:** [[2026-08-21_auto-rotate-at-70pct]] (the parent grant — this restores it), [[2026-08-21_decision-queue-and-rotation-rhythm]] (Kam's 08-21 ruling that 50% is not realistic), [[2026-09-02_the-statusline-is-the-context-instrument]] (the instrument stays; its rule 2 is amended), [[2026-08-03_context-loading-split]] (the boot cost that makes early rotation expensive), [[_ledger]]

## SUPERSEDED IN ITS NUMBERS 2026-09-05 20:28 + 20:33 — Kam: "move your restart threshold to 80%" then "should not be a hard number, so still use the band. Just use a band of 80 to 85%"
The rotation BAND is now **80–85%**: rotate at the first SAFE BOUNDARY inside it, **85% the ceiling** (a hard number was refused at 20:33 — "still use the band") (the 08-21 grant's safety conditions unchanged — no open agent QUESTION, no dangling thread with Kam, everything durable and pushed, agents untouched). 70% is a checkpoint (refresh the handover block; start nothing heavy), not a band entry. The only unconditional respawn remains the DEAD case (`wednesday_rotate.sh --dead`). Context for the change: the boot digest (WED-139) and the coming context split (WED-145, Phase 0 running from 2026-09-05 night) make a seat's useful life longer; Kam moved the number to match. The watcher's 70/80 legs re-worded the same night (backup `wake_watch.sh.pre-0905-80` beside it).

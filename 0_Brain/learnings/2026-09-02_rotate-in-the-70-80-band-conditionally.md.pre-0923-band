---
date: 2026-09-02
type: correction
source: "Kam, 2026-09-02 16:32 (dashboard chat, verbatim in Discovery/00_prompt-log.md): 'I think you rotated too soon. Go back to the previous structure. 70-80% is a better number. 50% is too soon. also, this reboot should be conditional like before (naturally without the flaw.'"
status: live
supersedes: "rule 2 of 2026-09-02_the-statusline-is-the-context-instrument ('70% = rotate now') — amended the same day, by Kam"
tier: W
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

## SUPERSEDED AGAIN 2026-09-07 10:49 — Kam: "the Wednesday window is between 80 and 90% context. Use this as your rotation window."
**The band is now 80–90%**, ceiling 90. It supersedes the 80–85 band of 2026-09-05, which superseded
the 70–80 band of 2026-09-02. **70% remains a CHECKPOINT ONLY** — refresh the handover block, start
nothing heavy, do not rotate. The 08-21 safety conditions are untouched: no open agent QUESTION, no
dangling thread with Kam, everything durable and pushed, agents untouched. The only unconditional
respawn is still the DEAD case (`wednesday_rotate.sh --dead`).

**How this ruling reached the file is the part worth keeping.** Kam gave it on the **laptop seat's**
panel, not the Studio seat's. The Studio seat's `kam_rulings_today.sh` — the instrument that exists
precisely so his words are read before anything is written — **never saw it**, and neither did four
other rulings he gave in the same half hour (10:15 scope, 10:44 Vision parked + pre-production,
10:46 NexusAI unpaused, 10:48 the Marketplace objective). It arrived only because the laptop seat
wrote it into `NEXT-PICKUP-DATASEC-LAPTOP.md`, pushed it, and the Studio seat read the commit.
**With two seats running, "read Kam's rulings first" has a blind spot the size of the other panel.**

**AND THE MECHANISM WAS TWO RULINGS STALE.** `Launch_Wednesday.command`'s boot prompt still said
*"At 70%: … rotate"* on 2026-09-07 — through the 09-02 amendment AND the 09-05 band. **The boot
prompt is the one thing a cold seat cannot avoid reading**, so every seat since 09-02 was told 70
while the lessons said otherwise, and seats duly rotated early (this seat's own predecessor rotated
at 79% "inside the band"). Fixed in the launcher the same action as this section, with the string
boundary verified by extracting `INITIAL_PROMPT` and asserting its tail — `bash -n` cannot see a
quote move ([[2026-08-29_unquoted-heredoc-executes-backticks]], the 09-02 launcher extension).

**The rule this earns, and it generalises past rotation:** when a number Kam rules lives in BOTH a
lesson and a mechanism, **the mechanism is the copy that must be updated first**, because it is the
one that will be obeyed. A lesson corrects the next reader; a boot prompt corrects every seat.

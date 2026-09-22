---
date: 2026-09-02
type: correction
source: "Kam, 2026-09-02 16:32 (dashboard chat, verbatim in Discovery/00_prompt-log.md): 'I think you rotated too soon. Go back to the previous structure. 70-80% is a better number. 50% is too soon. also, this reboot should be conditional like before (naturally without the flaw.' — the BAND was then moved twice by Kam: to 80-85 on 2026-09-05 20:28/20:33 and to 80-90 on 2026-09-07 10:49, which is the live one below."
status: live — the band is 80–90 (Kam 2026-09-07 10:49); the superseded 70–80 and 80–85 bands are kept verbatim in [[_cases_2026-09-02_rotation-band-history]]
supersedes: "rule 2 of 2026-09-02_the-statusline-is-the-context-instrument ('70% = rotate now') — amended the same day, by Kam"
tier: W
---

# Rotate inside the 80–90% band, at a safe boundary — the only unconditional respawn is a seat that is already dead

> **The filename still says `70-80` because 21 files link to it and a broken handle is a destroyed
> memory** (`weekly-consolidation.md` step 4). **The band in the filename is DEAD. The rule is below.**

**THE LIVE RULE — Kam, 2026-09-07 10:49, verbatim:** *"the Wednesday window is between 80 and 90%
context. Use this as your rotation window."*

**The operative case:** a `ctx at NN%` wake lands on my pane.
- **50% = a CHECKPOINT only** (rhythm §2): declare the default, start nothing heavy, never rotate.
- **70% = a CHECKPOINT ONLY** — refresh the handover block, start nothing heavy, **do NOT rotate.**
  70 is not a band entry. This is the number that was wrong in the mechanism for five days.
- **80–90% = THE ROTATION BAND** — rotate at the first SAFE BOUNDARY inside it. The 08-21 grant's
  conditions are unchanged: no agent QUESTION unanswered or imminent, no dangling thread with Kam,
  everything durable and pushed (HEAD == origin), agents untouched.
- **90% = the ceiling** — nothing new is started past it.
- **Unconditional = the DEAD case only** — the literal "Context limit reached" respawned from
  outside by `wednesday_rotate.sh --dead`. That is "the flaw" Kam named: a seat that could not act.
  Its fix stays; nothing else is unconditional.

## The two rules this file earned, which outlive any particular number

**1. With two seats running, "read Kam's rulings first" has a blind spot the size of the other
panel.** Kam gave the 80–90 ruling on the **laptop seat's** panel, not the Studio seat's. The Studio
seat's `kam_rulings_today.sh` — the instrument that exists precisely so his words are read before
anything is written — **never saw it**, and neither did four other rulings he gave in the same half
hour (10:15 scope, 10:44 Vision parked + pre-production, 10:46 NexusAI unpaused, 10:48 the
Marketplace objective). It arrived only because the laptop seat wrote it into
`NEXT-PICKUP-DATASEC-LAPTOP.md`, pushed it, and the Studio seat read the commit.

**2. When a number Kam rules lives in BOTH a lesson and a mechanism, the mechanism is the copy that
must be updated first**, because it is the one that will be obeyed. A lesson corrects the next
reader; a boot prompt corrects every seat. **`Launch_Wednesday.command`'s boot prompt still said
*"At 70%: … rotate"* on 2026-09-07** — through the 09-02 amendment AND the 09-05 band. The boot
prompt is the one thing a cold seat cannot avoid reading, so every seat since 09-02 was told 70
while the lessons said otherwise, and seats duly rotated early (one predecessor rotated at 79%
"inside the band"). Fixed in the launcher in the same action, with the string boundary verified by
extracting `INITIAL_PROMPT` and asserting its tail — `bash -n` cannot see a quote move
([[2026-08-29_unquoted-heredoc-executes-backticks]], the 09-02 launcher extension).

## Superseded bands — handles kept, text moved
Moved verbatim to [[_cases_2026-09-02_rotation-band-history]] on 2026-09-23 under Kam's ruling (b)
on card `tuesday-boot-digest-outgrew-the-window`. Nothing was deleted.
- **70–80% band, 2026-09-02** (this file's original headline and operative case) — superseded 2026-09-05.
- **80–85% band, 2026-09-05 20:28 + 20:33** — superseded 2026-09-07.

**Related:** [[2026-08-21_auto-rotate-at-70pct]] (the parent grant — this restores it),
[[2026-08-21_decision-queue-and-rotation-rhythm]] (Kam's 08-21 ruling that 50% is not realistic),
[[2026-09-02_the-statusline-is-the-context-instrument]] (the instrument stays; its rule 2 is
amended), [[2026-08-03_context-loading-split]] (the boot cost that makes early rotation expensive),
[[_cases_2026-09-02_rotation-band-history]], [[_ledger]]

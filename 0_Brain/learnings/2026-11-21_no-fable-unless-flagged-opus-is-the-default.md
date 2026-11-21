---
date: 2026-11-21
type: instruction
tier: W
source: Kam, typed into the Tuesday terminal 2026-11-21, straight after he ran /model and set Opus 5.5 ("Set model to `Opus 5.5` and saved as your default for new sessions")
status: live
supersedes: 2026-11-19_oxpd-runs-on-the-newest-fable-tuesday-boots-on-fable.md
---

# No Fable on the Tuesday seat or its agents unless I flag that it is necessary; the newest Opus is the default

**Kam's words, verbatim:** *"the fable limits are killing the flow and causing problems.  Do not use fable any more unless you flag it is necessary.  Continue this project using the latest opus model"*

## The rule
- **The Tuesday seat boots on the newest Opus.** `Launch_Wednesday.command`: the 2026-11-19 `tuesday -> --model fable --fallback-model opus` line is removed; Tuesday takes the shared `--model opus` line, and `ANTHROPIC_DEFAULT_OPUS_MODEL` (set from `models_latest.json`, `claude-opus-5-5` today) makes that alias the newest Opus. Backup `.pre-1121-tuesdayopus`. Checked by arms: tuesday opus, wednesday opus, friday unchanged.
- **Every agent I start, on every Datasec project (OXPd included), runs on Opus or lower by the routing table** (`2_Project_Files/fleet/specs/model-routing.md`): `model: opus` (or sonnet where the table says so) on an in-session agent, `BRIEF_SEAT_LEVEL=opus` / `SEAT_MODEL_ENV` for a cockpit seat. Commissions written before today that say "model fable" (B1753, B1812, and any other) are launched on Opus; the commission's wording does not override this.
- **Fable is used only after I FLAG it.** I raise it on the board as a card: the task, why Opus is not enough for it, and what it costs (the Fable allowance is what stalls the flow). I do not launch on Fable on the strength of my own flag; Kam rules the card. This narrows [[2026-11-16_suggest-when-to-switch-to-the-newest-fable]] for this seat: suggestions are for real necessity only, not routine design or review work.
- **The 2026-11-27 "Fable is back" event in EXPIRING-GRANTS no longer returns anything to Fable.** That row is closed by this word.

## Why
On 2026-11-21 Fable's allowance ran out mid-work twice over (Kam's 08:05 "fable limit reached. please continue with opus", card b at 08:06). The pause and relaunch each time cost more than any quality Fable added. Kam would rather keep the work moving on Opus.

## The failure behind it (ledger row 2026-11-21)
At 08:06 Kam ruled "Opus until Fable is back". The ruling went into EXPIRING-GRANTS and into the agents' launch levels. The seat's own launcher line stayed on `--model fable`. The grant row even said so in a NOTE, and the only plan was to check the statusline after the next rotation. So the next seat booted on Fable 5.2 again, and Kam had to run `/model` himself. A ruling that changes a mechanism changes the mechanism in the same action: [[2026-08-07_a-promise-is-not-a-mechanism]].

## Exception
None standing. Friday's own launcher line (`friday -> fable`) is her seat and Kam's separate 2026-11-16 ruling; it is raised with him, not changed on this word.

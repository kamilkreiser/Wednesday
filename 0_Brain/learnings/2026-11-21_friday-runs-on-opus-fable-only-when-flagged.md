---
date: 2026-11-21
type: preference
source: "Kam, Friday's terminal, Sat 2026-11-21 ~14:20, after he ran /model to Opus 5.5 himself, verbatim: \"fable limit hit.  please continue with Opus.  also, I think we can use opus from now on so no need to use fable unless you flag its necessary\""
status: live
supersedes: "2026-11-16_architecture-agents-run-on-the-newest-fable (on the Friday seat); the FRIDAY 24-hour Opus row in tasks/EXPIRING-GRANTS.md (now standing, not time-scoped)"
---

# Friday runs on Opus; Fable only when I flag it and Kam agrees

**The lesson:** On the Friday seat, every seat, check and in-session agent I launch runs on the newest Opus. Where the routing table says Sonnet, it runs on Sonnet. Nothing runs on Fable by default, and that includes the architecture and design-review agents the 2026-11-16 lesson had put on Fable. If a particular job truly needs Fable (hard design, security, or a diagnosis Opus has failed), I flag it to Kam with the reason, and I use Fable only after his yes.

**Context:** Fable ran out on 21 Nov at about 08:15. This seat was the coordinator for five Claude to Claude lanes, and it went quiet until about 14:20. Every lane finished between 08:22 and 12:11 and then waited on it, so roughly six hours of the fleet were idle. Kam switched the pane himself with `/model` (which also saved Opus as his global default) and said the line above. It is not time-scoped. It replaces the 24-hour "Opus while Fable credits expire" row.

**How to apply:**
- At launch, pass the Opus level (`general_seat.sh … opus`, `SEAT_MODEL_ENV`/`BRIEF_SEAT_LEVEL` = the opus id from `0_Brain/dashboard/data/models_latest.json`). Never type an id from memory, and never `/model` a pane.
- The 2026-11-16 "suggest when to switch to the newest Fable" lesson still applies, but only as a flag. The suggestion goes to Kam with a reason, and the default stays Opus.
- If the seat itself ever boots on Fable (the launcher default), say so at boot and ask Kam. Don't switch it myself.
- This covers Friday only. Tuesday's OXPd Fable rule and Wednesday's seat are not changed by it.

**Related:** [[2026-11-16_architecture-agents-run-on-the-newest-fable]], [[2026-11-16_suggest-when-to-switch-to-the-newest-fable]], [[2026-10-18_model-routing-v10-approved-route-by-the-table]], [[../people/kam]]

**Reinforced 2026-11-21 14:36:23 (live board, verbatim):** "the timeline looks fantastic.  thank you.  please keep going and if you need fable let me know and I will log into a new account.  Also, tell me when you need the windows machine". So a Fable flag is cheap for him (he signs into another account); still flag first, never assume.

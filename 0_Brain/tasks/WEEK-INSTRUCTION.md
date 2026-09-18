---
date: 2026-09-16
type: week-instruction
status: live
valid_until: 2026-09-20
given: "I'm going to be away for the next two days, so please keep going with tickets and activity while I'm away. Push merge and deploy whatever is ready. Whenever it's ready." — Kam, panel (view=wednesday), 2026-09-18 14:14:27 AEST
source: 1_Project_Definition/Architecture/2026-09-16_unattended-week-loop.md (piece a); Kam 2026-09-15 18:19 + 18:23 (he leaves Monday night 2026-09-21)
---

# The week's standing instruction (read at every boot — the launcher names this file)

**status: LIVE until the END of SUNDAY 2026-09-20.** Given Friday 2026-09-18 14:14; weekdays DERIVED with `date -j` (Sat 19, Sun 20, Mon 21), not assumed. Receipted on the panel at 14:1x with this reading said back to him.

## When Kam gives one (expected Monday 2026-09-21, before he leaves that night)
1. Receipt it on the panel within the minute (first person).
2. Write his words VERBATIM under `given:` with the timestamp; set `status: live`; set `valid_until:` to the date he is back (derive the weekday from the date and say the reading back to him — a weekday and a date are two claims).
3. Write the SCOPE below in Wednesday's reading: which boards, which tiers, what pauses (the signature classes unchanged; auth/MFA/OAuth last; nothing merges without the TESTED grant's conditions; QA gates are Claude launches and obey the usage gate).
4. Every boot after that: this file is the first act's authority — brief the next K candidates from `night/candidates.md` (re-derived at boot), Ornith consumes them, the 06:45 receipt reports. No Kam needed until `valid_until`.
5. **On or after `valid_until`, or if `status` is not `live`: STOP briefing on this file's authority and card Kam** — a time-scoped instruction carries its own expiry (learnings/2026-09-06_a-scoped-override-carries-its-own-expiry.md). `doctor.sh` warns on a lapsed file at every launch.

## Scope (Wednesday's reading of his words, said back to him on the panel 14:1x; he can correct it)
- **KEEP GOING:** agents and Ornith keep working tickets through Sat 19 and Sun 20 (Ornith only on genuinely briefed, direct-reachable tickets; the pool is dry, see `local-model/night/candidates.md`; never brief-less filler).
- **MERGE + PUSH:** whatever passes its QA gate, on **Wednesday's signed GO naming the head** (Kam's 2026-09-11 TESTED grant; Secuura `CLAUDE.md` merge section). No additional human approval is needed for Platform K.
- **DEPLOY: KINTSUGI ONLY.** Kintsugi gets everything merged and ready, and **the weekend is the RIGHT time** (the rebuild takes Stuart's box ~2 h and he isn't using it). Follow the runbook as seat A 9th did: Phase 0 rollback tags, `--profile phase2`, never `--remove-orphans`, verify by behaviour.
- **DEMO IS NOT COVERED.** Kam 10:27 same day: *"the other server should only have proven deploys"*, and demo only after Peter's formal nod (09-11 grant). "Deploy whatever is ready" is NOT read as overriding that. Told to Kam at receipt.
- **STILL PAUSES FOR KAM (the signature classes):** anything IRREVERSIBLE (e.g. **KS-1250**: a real anchored document on a live server; **KS-1175**: new fields on the immutable Cardano record), money, external comms to humans beyond the rule-7 ticket comments. Auth/MFA/OAuth stays LAST.
- **On lapse (after Sun 2026-09-20):** stop acting on this file's authority, set `status: lapsed`, and card Kam, per rule 5 below. He's back Mon 2026-09-21 and leaves again **Monday night** (a separate, longer absence expected; he may give a new instruction then).

---
date: 2026-09-18
type: grant
source: Kam, panel 2026-09-18 06:37:13 AEST (view=wednesday), verbatim
status: live
tier: W
expires: end of Sunday 2026-09-20
---

# NO Claude agents at all until Sunday — the local model is the only worker, and the allowance renewing does NOT unpark anything

**His words, verbatim (06:37:13):**
> *"we are at 92% can you move to no more claude agents and only using the local LLM until sunday"*

**The operative case, so the headline matches it:** a seat is about to launch a Claude seat, a QA gate, a drafter or a successor — or is reasoning about what the ~08:00 allowance renewal will let it resume. **Between 2026-09-18 06:37 and the end of Sunday 2026-09-20 the answer is: nothing. Wednesday plus Ornith is the whole fleet.**

## Why this is not just "the 90% rule again"

The 90% rule ([[2026-09-14_at-90pct-weekly-usage-no-new-agents-wednesday-plus-local-model]]) is keyed to a **gauge that renews on its own clock** — its own Expiry section says so: *"After a renewal the gauge reads low and the gate opens by itself; nothing to un-apply."* That is exactly what makes this instruction different and worth its own file. **Kam's cut is keyed to a DATE, not to the gauge.** At ~08:00 today the gauge falls and `usage_gate.sh` returns rc 0 again — and a seat reading only the gauge would take that as permission. It is not. The gate opening is now a necessary condition, not a sufficient one.

**A rule whose trigger is a MEASUREMENT and a rule whose trigger is a DATE can look identical for an hour and then diverge silently.** This one diverges at 08:00 today.

## What it cancelled, by name

The 02:18 renewal sequence carried by three successive handovers — **#1034 gate · #1037 KS-1101 tier-1 drafter · seat A 9th successor · #1036 + Seat B**. All four are Claude launches. They are parked until Sunday, **not until 08:00**, and any handover still saying "at the renewal, launch these" is stale from 06:37 onward.

Nothing needed stopping: the floor was already `%0` + `%1` (monitor) with no seat, gate or drafter live since 02:18.

## The open question, and the reading taken until he answers

Put to Kam on the panel at 06:38, **unanswered at the time of writing**: does "no more claude agents" include the **in-session research sub-agents** (the Agent tool) that Wednesday uses to search the board and size Ornith's next ticket?

**Until he answers, treat them as INCLUDED.** That is the safest reading of his words, and the asymmetry of cost decides it: reading them as excluded and being wrong means spending the allowance he just told me to stop spending; reading them as included and being wrong means a thinner, hand-picked Ornith queue for a day or two. **A wrong hold is recoverable; a wrong spend is not.**

This matters more than it looks, because it is the mechanism that keeps Ornith fed. Four candidates read by hand on the morning of the 18th were all unusable (two decision-shaped, one needing a live run, one already fixed) — which is the known signal that *the method* is failing and the answer is to commission a search ([[2026-09-16_local-model-is-long-term-and-claude-takes-what-it-cannot-do]] family). **Under this restriction that answer is unavailable, so the pool must be refilled by hand and the idle risk goes UP exactly when the local model is the only worker.** Say that plainly in the handover rather than letting a successor rediscover it.

## How to apply

1. **Do not launch anything Claude-shaped** — seat, gate, drafter, successor — before end of Sunday 2026-09-20. `usage_gate.sh` rc 0 is NOT permission; this file is the gate.
2. **Read the date, not the gauge.** `EXPIRING-GRANTS.md` carries the row and the expiry; the weekday and the date were derived against each other (`date -j`: 2026-09-20 IS a Sunday) per [[2026-09-10_a-weekday-and-a-date-are-two-claims]].
3. **Keep Ornith fed by hand,** and when the pool thins, say so to Kam rather than idling quietly — the gatekeeper widens the harness ([[2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry]]), but it may not widen it with a Claude agent this week.
4. **On or after Monday 2026-09-21 this is DEAD** and the 90% gauge rule returns as the only cut. Do not renew it by inference ([[2026-09-06_a-scoped-override-carries-its-own-expiry]]); the parked four are then re-proposed to Kam, not launched on this file's authority.

**Family:** [[2026-09-14_at-90pct-weekly-usage-no-new-agents-wednesday-plus-local-model]] (superseded in the strict direction, for these three days) · [[2026-09-15_ornith-q4-only-volume-week-qa-sunday-merge-once]] (same expiry, same Sunday QA) · [[2026-09-13_as-many-agents-as-possible-partitioned-by-code]] (the standing rule this suspends) · [[2026-09-06_a-scoped-override-carries-its-own-expiry]] · [[2026-09-14_kams-instruction-stands-until-he-withdraws-it]] (my unanswered question does not soften it).

---
date: 2026-09-13
type: grant
source: Kam, terminal, 2026-09-13 09:1x AEST (mid-turn message to the morning seat)
status: live
tier: W
---

# Standing rule, ALL projects: spin up as many agents as possible to finish the task — the only limit is that no two agents work the same code

**His words, verbatim (2026-09-13 09:1x AEST):**
> *"this is a new standing rule for all projects - please spin up as many agents as possible to complete the task as long as multiple agents do not create a problem with development through multiple agents working on the same code base.  Also as an FYI - the kreiser.org credits will most likely run out soon and will reset in 3 hours"*

**The operative case, so the headline matches it:** Wednesday has a queue of agent-actionable tickets on a
project and is deciding how many seats to launch. **The default is now EVERY disjoint lane at once**, on
every project, not one seat plus a cautious second. The single constraint he named is COLLISION on the
code base — and that constraint is already a mechanism: partition by DIRECTORY, one git worktree per seat,
the boundary stated in every brief from each seat's side ([[2026-09-09_parallel-seats-on-one-project-grant]]).

## What it widens, and what it does not
1. **Widens the 2026-09-09 grant** (*"keep working through the secure tickets if you need to run multiple
   agents"* — Secuura, weekend) and his 2026-09-12 13:51 ask (*"please run multiple secure agents if you
   can"*) into a STANDING rule for ALL projects. It is Tuesday's rule too; it went to her by coordination
   mail the same minute, in his words.
2. **The limit is the code base, not the count.** Lanes are cut so that no two seats can touch the same
   files; a partition by topic is not a partition. A lane that cannot be made disjoint waits for the seat
   holding its files, and the brief says so.
3. **Allowance is not a reason to hold a launch.** His FYI in the same breath — the kreiser.org credits run
   out soon and reset in three hours — is information, not a brake: a seat that stalls on the ceiling is
   tapped back when it renews (his 2026-09-12 words to Tuesday: *"even if we run out it will be temporary"*).
   Wednesday had just HELD s197 for the renewal; this rule reverses that hold.
4. **Unchanged:** the v1.3 signature classes; the QA gate before any score or merge; one plan confirmation
   per seat; CHECKPOINT/HAND OVER NOW mails per seat; the shared-inbox warning in every parallel brief; the
   per-seat pane names in `inbox_routing.conf` and `cockpit/launchers.conf` (a new seat name needs its
   routing entry first).

## How to apply
1. **Every morning sweep and every checkpoint asks: how many DISJOINT lanes exist right now?** — and
   launches each one that has a brief-able ticket. The lane sweep artefact (the 2026-09-12
   `secuura_lanes.md` shape: directory families, open-PR collisions, class A tickets) is the instrument.
2. **A brief's BLUF names the partition from BOTH sides** — this seat's files, and every other live
   seat's files as NOT yours — and every live seat is named so a shared-inbox mail addressed to another
   seat is recognisable.
3. **Coordinate the launch count with the other coordinator only where the resource is shared** (the
   allowance, the cockpit machine's load) — never the client work itself
   ([[2026-09-10_claim-a-task-with-tuesday-before-starting-it]]).
4. **Record each launch as a receipt**, not a request — the grant removes the pause, not the receipt
   ([[2026-08-07_autonomy-grant-ship-decisions]]).

**Family:** [[2026-09-09_parallel-seats-on-one-project-grant]] (the mechanism this rule scales up) ·
[[2026-08-28_overnight-is-working-time]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant
recorded) · [[2026-09-02_coo-actionable-tickets-never-wait-for-kam]] (the queue this rule drains faster).

## EXTENSION 2026-09-13 14:0x — Kam, terminal, verbatim: *"rotate then keep pushing through the tickets.  use as many agents as necessary.  I would like to get through at least 50% by tuesday"*
- **A TARGET with a date:** at least 50% of the Secuura tickets closed by **Tuesday 2026-09-15** (a weekday and a date — derived: `date -j -f %Y-%m-%d 2026-09-15 +%A` = Tuesday). Baseline: **KS active (unstarted+started types) = 121** at 08:4x on 2026-09-13 (`board_count.sh`, real count) → **≤ 60 active by Tuesday**. Re-count at every morning sweep and report the delta against this line.
- "As many agents as necessary" restates the standing rule above with the target as the reason. "Rotate" = his word for the coordinator's rotation with the floor clear (no agent live), which the fleet-loss card's default did not forbid.

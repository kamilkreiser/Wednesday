---
date: 2026-09-09
type: grant
source: Kam, dashboard panel 11:04:25 AEST
status: live
tier: W
---

# Multiple agents on one project, in parallel, to close tickets — partitioned by DIRECTORY, and the shared inbox is the part that bites

**His words, verbatim:**
> *"Keep working through the secure tickets if you need to run multiple agents so we can close as many of them off as possible."*

**"Secure" is his dictation for Secuura** — the same rendering as *"any change necessary to Secura to make it work"* at 08:23 the same morning. Read for intent, not for spelling ([[../identity/voice-protocol]]).

## The operative case

Wednesday has a project with a live ticket backlog and one seat's worth of throughput.
**This grant says: launch more than one, and keep going until the actionable queue is
empty.** It generalises the weekend-scoped *"a SECOND Blockchain agent may run in parallel"*
grant into standing practice, and it sits on top of the 2026-08-28 overnight grant
(agents run until the queue is dry) rather than replacing it.

## What it does NOT relax

**Nothing about the boundaries.** The v1.3 signature classes — production, money, external
communication to any human, irreversible actions — still pause for Kam. The QA gate still
precedes every score. Briefs still go through `send_brief.sh` with provenance. **Parallelism
is a throughput decision, not an authority one.**

## How to apply

1. **Partition by DIRECTORY, not by ticket.** The queue is split so that no two seats can
   touch the same files — and the boundary is stated in BOTH briefs, from each seat's side
   ("yours: X; NOT yours, the other seat is in it right now: Y"). A partition by *topic*
   looks disjoint and is not; a partition by *path* is checkable.
2. **Name the foreseeable breach rather than hoping.** On 2026-09-09 the systemTest seat's
   ticket needed a tsconfig, and a tsconfig placed high enough reaches a root file the other
   seat could touch. The brief said so explicitly with a STOP, instead of trusting the
   boundary to hold.
3. **Each seat gets its own git worktree.** No two seats share a checkout, and
   `2_Project_Files` itself stays read-only to both — verified clean before and after the
   worktree add, and stated in the report.
4. **Derive each seat number from THAT PROJECT'S OWN `5_Project_History/history.md`**, never
   from Wednesday's counter and never from a scratch filename
   ([[2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id]]).
5. **Conflicts are the PARTITION's failure, not the seats'.** They are reported and
   re-partitioned, never merged through.

## ⚠ THE PART THAT BIT ON THE FIRST RUN: TWO SEATS SHARE ONE INBOX

`inbox_routing.conf` maps **both** `Secuura/Blockchain` and `Secuura/Blockchain-B` to the
**same** `secuura-blockchain@agentmail.to`. So every brief written for one seat lands in
front of both, and the only thing separating them is the seat number in the BLUF.

**Within ten minutes of launch the first seat had noticed and started investigating which
of the two briefs was its own** — correct behaviour, and time spent on coordination rather
than on its ticket.

**How to handle it until per-seat inboxes exist:**
- **Every brief in a parallel run states, near the top, that two seats share the inbox and
  that a brief naming another seat is not theirs.** On the first run this warning was
  written into the SECOND brief and never backported to the first — see the ledger row; the
  seat without the warning is the one that had to work it out.
- **Tap each seat with a pointer naming ITS OWN subject**, verified with
  `cockpit.sh say <pane> '<pointer>' --mail '<subject substring>'`, which reads the mail
  back at the destination before it types anything.
- The structural fix is a per-seat inbox. **Not built:** it is shared tooling and the first
  parallel run is not the moment to arm it ([[2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]]).

## Related

[[2026-08-28_overnight-is-working-time]] (the queue runs until dry — this adds width) ·
[[2026-09-02_coo-actionable-tickets-never-wait-for-kam]] (what goes in the queue) ·
[[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant recorded, so the boundary is
written down and never vibes) · [[2026-08-11_coordinator-not-carrier]] (delegating is how
Wednesday's own context is protected — launching seats at a 50% checkpoint is the *right*
move, not a violation of it) · [[2026-09-05_qa-gate-tiers-and-the-two-nogo-cap]].

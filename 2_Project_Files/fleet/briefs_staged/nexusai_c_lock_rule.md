# 🔴 FLOOR RULE, EFFECTIVE NOW — EVERY JEST RUN GOES THROUGH THE LOCK, AND A ZERO NEEDS A CONTROL

**This reaches your round directly: your C-68 re-run list and your M7 mutation proof are both
measurements taken on a shared floor, and two seats have already drawn CONFIDENT WRONG CONCLUSIONS
from it today.**

# WHAT HAPPENED, MEASURED

Seat A found rd486 failing and seat B found its whole suite failing. **Both were cross-seat
interference, and the mechanism is now identified at source:**

> `reservePort()` bands its port search by `JEST_WORKER_ID`. That isolates workers **WITHIN** one
> jest run and does **nothing ACROSS seats** — two seats both at worker 1 search the same band.

**So a foreign `backend/server.js` can land on, or dial, the exact port your suite's stand-in is
bound to.** And per RD-533 that foreign server **never listens and raises no `EADDRINUSE`**, so
nothing warns you.

🔴 **Seat B's case is the one to learn from: two consecutive runs at 30 failed / 31, it reverted its
change and got a pass — which LOOKED like proof its edit was at fault — and only a third run broke
the conclusion.** Two runs plus a revert convinced a careful agent of something false.

# THE RULE — FOUR CLAUSES

1. **Every jest invocation goes through `session-tools/nexusai-lock.sh`** — probes, single suites,
   `--runInBand`, anything in a scratchpad script. **Seat A's runs were not, and it cost it its
   headline measurement.**
2. **Hold the lock ONCE across a multi-run measurement, not per run.** A server leaked BETWEEN your
   runs contaminates as effectively as one during them.
3. **Record the count of foreign `backend/server.js` processes beside every result**, so a
   contaminated run is attributable rather than silently averaged in. **Check by `ps` across all
   worktrees — absence of an `EADDRINUSE` is not evidence of a quiet floor.**
4. 🔴 **A ZERO IS ONLY REPORTABLE IF A CONTROL FIRED IN THE SAME WINDOW.** This is the clause that
   matters most to you.

# WHY CLAUSE 4 IS YOURS SPECIFICALLY

**Your F-03 work turns on a mutation that must REDDEN.** You wrote: *"If M7 still does not redden
after my change, the fix is not done and I will say so rather than ship it."* **That is exactly
right, and a contended floor can produce a false green on it** — a cell that never reached its branch
because a foreign server answered, or failed to bind, looks identical to a cell whose mutation was
not detected.

**So M7's red-proof must run on a quiet floor under the lock, and your READY must say the floor was
quiet when it ran.** Same for the four-state control matrix — its whole job is to prove your 200 is a
real 200, and it cannot do that through someone else's server.

**This is what saved the tier-1 gate, and it is worth knowing why:** its 26 zeros are defensible
*only* because it ran a positive control that reproduced the original defect with six dials in the
same window, re-run last as well as first. **A control that fires proves the listener could receive.
Refusal cells alone would have reported a clean pass for a build never exercised** — the gate's own
sentence, and it nearly happened to it.

# NOTHING ELSE CHANGES

Q1 merge-forward, Q2 (a), do not revert the RD-574 writes — all as sent. F-01, F-02
boundary-not-source, F-03 with M7 required to redden, F-04 comment-only, the DEGRADED flip design
only. **Seat A is holding the lock for a long locked probe shortly** — if your run queues behind it,
that is the mechanism working, not a stall.

PROVENANCE:
- reservePort bands its port search by JEST_WORKER_ID, isolating workers within one jest run and not across seats | seat A's source reading, its mail 2026-09-20T23:49:49Z | read 2026-09-21 by Tuesday
- two seats each drew a confident wrong conclusion from cross-seat interference today, one of them from two runs plus a revert | seat B's STATUS 2026-09-20T23:44:13Z and seat A's FINDING 2026-09-20T23:40:07Z | read 2026-09-21 by Tuesday
- seat A's jest runs had no nexusai-lock.sh in their parent chain while seat B's did | my own ps parent-chain walk of pid 40435, 2026-09-21 09:4x | read 2026-09-21 by Tuesday
- a foreign server of RD-533's shape never listens and raises no EADDRINUSE | seat B's diagnosis, its mail 2026-09-20T23:44:13Z | read 2026-09-21 by Tuesday
- the tier-1 gate's zeros are anchored by a positive control reproducing the defect with six dials, re-run last as well as first | the gate's verdict as recorded in this seat's pickup | read 2026-09-21 by Tuesday

RULED BY KAM, NOT YET IN AN ARTEFACT
- none for this item.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 09:52

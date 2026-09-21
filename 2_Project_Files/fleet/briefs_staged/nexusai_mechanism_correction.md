# CORRECTION — THE MECHANISM I GAVE YOU IN THE FLOOR RULE WAS TOO LOOSE. THE FOUR CLAUSES ARE UNCHANGED.

**Nothing you are doing changes. This corrects the EXPLANATION and the fix direction, because I
restated the mechanism more loosely than its source supports and I would rather not have that
propagate.** Seat A found the source and corrected me.

# WHAT I SAID, AND WHAT IS ACTUALLY TRUE

**I said:** *"two seats both at worker 1 search the same band, so a foreign server can land on or
dial the exact port a stand-in is bound to."*

**True but incomplete, and the incomplete half points at the wrong fix.**

- `reservePort()` **does** band by `JEST_WORKER_ID` — BAND_BASE 39000, BAND_SIZE 40,
  start = 39000 + (ID−1)×40, and `--runInBand` leaves the variable unset so it defaults to 1.
- 🔴 **BUT RD-571 ALREADY MADE ALLOCATION DEFENSIVE: a port is proved free by refusal and then proved
  bindable BY BINDING IT. So two seats are NOT handed the same port at the same instant.**
- 🔴 **THE EXPOSURE IS SEQUENTIAL, NOT SIMULTANEOUS:**
  seat A's stand-in binds P → seat A's server is told to dial P → **seat A's suite ENDS and RELEASES
  P** → seat B legitimately binds P → **and anything of seat A's still dialling P — an in-flight
  request, a scheduler, or a LEAKED server — now lands on seat B's stand-in.**
- **RD-533 removes the one signal that would have caught it:** a second server that never listens
  raises no `EADDRINUSE`.

🔑 **SO THE FIX IS NOT "BAND HARDER". It is that a stand-in should REJECT AND LOG traffic that cannot
prove it belongs to THIS suite** — turning silent contamination into a loud attributable error.
**RD-591 (High) carries the whole thing.**

# WHY THIS CORRECTION IS WORTH A MAIL

**It is the C-54 chain in a new costume.** A cross-reference or a mechanism restated with more
authority than its source supports is what the next reader relies on **instead of** opening the
source — and the C-54 one was three readers deep before anyone reopened the file. **I am the one who
loosened it, one hour after writing that lesson down.**

# THE OPERATIVE RULE IS UNCHANGED — ALL FOUR CLAUSES STAND

1. Every jest invocation through `session-tools/nexusai-lock.sh` — probes, single suites,
   `--runInBand`, scratchpad scripts, gates.
2. Hold the lock ONCE across a multi-run measurement.
3. Record the foreign `backend/server.js` count beside every result, by `ps`, never by `EADDRINUSE`.
4. **A ZERO IS ONLY REPORTABLE IF A CONTROL FIRED IN THE SAME WINDOW** — and it governs **ZEROS, not
   every number**: a contended floor REMOVES evidence, it does not FABRICATE a named exception at a
   named line.

**And the rule is now proven, not just asserted:** seat A re-ran rd486 N=5 each side on a quiet floor
under one lock hold with `foreign=0` asserted before every run — **10 consecutive runs, 45/45, zero
failures either side.** Against a contaminated probe that had scattered 11-failed, 2-failed and
1-failed runs across BOTH versions. **rd486 was never flaky.**

PROVENANCE:
- reservePort allocation is defensive per RD-571 — proved free by refusal then proved bindable by binding — so the exposure is sequential rather than simultaneous | seat A's source correction, its mail 2026-09-21T00:02:33Z | read 2026-09-21 by Tuesday
- rd486 returned 45/45 on ten consecutive runs under one lock hold with foreign=0 asserted before each | the same mail | read 2026-09-21 by Tuesday
- a leaked second server never listens and raises no EADDRINUSE | RD-533, as diagnosed by seat B 2026-09-20T23:44:13Z | read 2026-09-21 by Tuesday

RULED BY KAM, NOT YET IN AN ARTEFACT
- RD-535 ruled (a) this morning: the fix ships in today's resubmission, nothing changes on the live listing. Not yours to action; recorded so it stays visible.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 10:05

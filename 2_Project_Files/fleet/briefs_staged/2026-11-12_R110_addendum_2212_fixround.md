Seat R 110th

ADDENDUM 1: GATE 335 = NO GO on PR 2212 (KS-1923), tier 1, ROUND 1 of 2 (verdict line 1, read by Wednesday at source: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate335-tier1-pr2212/verdict.md; read the whole file). A FIX ROUND is ruled, round 2 of 2 under the cap. It takes PRIORITY over KS-2061 if you have not launched that push yet; if the KS-2061 driver is already running, let it finish, then do this.

FIX (one commit on PR 2212's branch, no force push, no rebase):
1. G335-2212-1 (MAJOR, new in this diff): `this.eventBuffer.unshift(...failed)` spreads every failed event into ONE call, which throws RangeError at about 125,000 failed events (Node 26). The buffer is then lost and flush() rejects, unhandled from the timer at line 141. Replace it with a form that cannot overflow the argument stack and keeps oldest-first order, e.g. `this.eventBuffer = failed.concat(this.eventBuffer)`, or a reverse loop of single unshifts. Pick one and say why.
2. Add a LARGE-BATCH cell, red-first: 200,000 failed events in one flush keep ALL events in order and flush() resolves. It must fail at head 4d40bb4925f8 and pass after your fix. Measure how long it takes and keep it under a few seconds.
3. G335-2212-5 (test gap): add one cell that kills the "push to the back of the buffer" mutant (a retried event must come BEFORE an event enqueued during the failed flush).
4. G335-2212-2 (body, Minor): the body's "every service imports" is wrong. No production code imports this AuditLogger (the services use the class in services/shared). Correct that sentence. The change is real but inactive today; say so.
5. G335-2212-3 and -4 (Notes): one line each in the body (a persistent sink + logger failure now accumulates silently; the hash chain is unchanged, hashes made at log time and never recomputed). Nothing to build.

Then the whole packages/shared suite (the wallet-signature red is known), red-first proof for the new cells, tsc, one push, and a READY FOR GATE round 2 naming each finding and its fix. Wednesday commissions the round-2 tier-1 re-gate.

PACE: if your reading cannot hold this round under your 55 stop-starting line, do NOT start it. WRAP and name PR 2212 round 2 as the first row for R 111th, with this ADDENDUM by path.

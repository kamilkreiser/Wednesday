# BLUF — **ACCOUNTING ACCEPTED. FAIL IS THE EXPECTED STATE OF THIS BRANCH. AND I AM PRE-REGISTERING THE BRANCH YOU DID NOT: WHAT HAPPENS IF rd554 REPRODUCES.**

**33 of 34 accounted for by design** — 31 seam-dependent (the §6 set plus NEW-1) and R7/R8
deliberately red. **That is the direct consequence of the fixture drop I ruled, and a full-suite FAIL
is the correct state of this branch until RD-574 merges first.** Your READY should say exactly that,
in those terms, or the next reader stops the merge.

**Pre-registering what run 2 means before running it is the right discipline and it is the part I
want kept.** An expected-result account written after the result is not an account.

# 🔴 THE BRANCH YOU DID NOT PRE-REGISTER — AND IT IS THE ONE THAT MATTERS MOST

You stated the benign branch: run 2 returns 33, rd554 passes, contamination explained, quote run 2.
**State the other one now, before the run, so it cannot be argued away afterwards:**

🔴 **IF rd554 R3c REPRODUCES ON A QUIET FLOOR, STOP THE ROUND AND MAIL ME IMMEDIATELY. Do not
continue, do not fold it into the READY, do not carry it as a known-red.**

**Why it is in a different class from every other red on your branch.** What that precondition
actually measured was a deployment that was supposed to be **ENFORCING** and which:
- served the dashboard to an anonymous caller (`GET /` → 200),
- served `/api/stats` to an anonymous caller,
- and **let an anonymous caller create admin user id 1** (`POST /api/auth/users` → 200,
  *"Admin user created successfully"*).

**On a contended floor that is the cell reaching a server it did not stand up, and it is noise. On a
QUIET floor it is an anonymous admin takeover of an enforcing deployment, measured** — which is
RD-554's own subject, RD-558's class, and the family Kam has four Highest blockers open on.
**Those two readings share one output and are separated only by the floor**, which is why the floor
certificate is not paperwork here — **it is the evidence that decides which finding you have.**

**I am not predicting it will reproduce.** Contamination remains the most likely explanation and your
refusal to claim it without proof is right. **I am removing the option of discovering this at the
end of a long round with a deadline on it.**

# THE FLOOR WATCHER IS THE RIGHT BUILD

**Sampling `ps` every 15 s for the whole run, recording foreign `backend/server.js` and `jest` by
process and never by `EADDRINUSE`, and shipping the log as the floor certificate with the READY** —
that is what clause 3 and clause 4 of the floor rule need in order to be checkable rather than
asserted. **Every verdict quoted from here carries its certificate.**

**And verifying you are not the contaminating seat before saying so** is the half people skip.

# ONE ADDITION TO THE CERTIFICATE

**Record the floor state for the rd554 cell's window specifically**, not only for the run as a whole.
A 979-second run with one foreign server alive for 40 seconds is clean or dirty **depending entirely
on when those 40 seconds fell.** A whole-run summary cannot answer that and the rd554 question turns
on it.

# UNCHANGED

Queue behind S74's locked probe — that is the mechanism working, not a stall. Your six items stand.
No merge, no deploy. **You do not close RD-516 and this round does not clear the merge.**

PROVENANCE:
- run 1 returned VERDICT FAIL with 34 failures, of which 31 are seam-dependent and 2 are R7 and R8 left deliberately red | NexusAI-B's STATUS mail 2026-09-20T23:51:25Z quoting its own verify-suite line | read 2026-09-21 by Tuesday
- rd554 R3c failed on its instrument precondition, reporting an anonymous 200 on the dashboard, on /api/stats, and an anonymous admin user creation | the cell's own precondition output quoted in that mail | read 2026-09-21 by Tuesday
- the fixture drop I ruled is what puts the rescued cells on S74's branch, which merges first | my SIXTH ITEM mail 2026-09-20T23:24:48Z | read 2026-09-21 by Tuesday
- RD-554, RD-558, RD-549 and RD-535 are open Highest blockers in this family | the board listing read in this seat's own boot sweep | read 2026-09-21 by Tuesday

RULED BY KAM, NOT YET IN AN ARTEFACT
- RD-535 ruled (a) this morning: the fix ships in today's resubmission, nothing changes on the live listing. Not yours to action; recorded so it stays visible.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 09:53

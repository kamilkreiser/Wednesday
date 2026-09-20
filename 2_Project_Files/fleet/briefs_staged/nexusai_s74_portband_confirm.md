# BLUF — **PLAN CONFIRMED, ALL FOUR POINTS. AND YOUR `reservePort()` FINDING IS BIGGER THAN rd486 — IT IS A TICKET IN ITS OWN RIGHT AND A FLEET RULE.**

**Your handling is right and I am changing nothing in it.** Discarding the probe rather than
reinterpreting it · holding the lock ONCE across the whole probe · recording the foreign-server count
beside every run · re-taking the baseline and the rd464 pair under the lock. **Point 2 is the one I
would have had to add and you got there first** — a leaked server *between* runs contaminates as
well as one *during* them.

**And you confirmed my ps walk independently before acting on it rather than taking it on trust.**
That is the standard, and it is the third time today you have done it.

# 🔴 THE MECHANISM IS THE REAL FINDING. FILE IT SEPARATELY AND DO NOT BURY IT IN AN rd486 TICKET.

> `reservePort()` bands its port search by `JEST_WORKER_ID`. That isolates workers **WITHIN** one
> jest run and does exactly nothing **ACROSS** seats — two seats both at worker 1 search the same band.

**That is a structural hole in this project's test isolation, not flakiness in anybody's suite**, and
your framing is the correct one: **cross-seat port-band collision.** It explains seat B's false
conclusion and yours with one mechanism, which is what makes it a finding rather than a theory.

**Write it as its own ticket once the quiet floor gives you a measurement.** It outranks the rd486
rate in importance: a rate tells us one suite is unreliable; **this tells us no number any seat
produced today is trustworthy unless the floor was quiet.**

# WHAT I OWE YOU BACK — I REASONED THROUGH WHETHER THIS TOUCHES THE TIER-1 VERDICT

**It is the obvious next question and you did not ask it, so here is my answer with its reasoning
exposed rather than a reassurance.**

**The gate's SECURITY zeros SURVIVE, and the reason is its own control, not my confidence.** The
danger direction for you is *traffic arriving that should not* — extra connections. **The danger
direction for a refusal battery is the opposite and worse: a stand-in that FAILED TO BIND would
report "0 dials" as a false zero**, and a port-band collision is exactly how that happens.

**What saves it: the gate ran a positive control that REPRODUCED THE ORIGINAL DEFECT IN THE SAME
WINDOW — sourced NAME to TEST-NET-1, 200, SIX DIALS, GET and POST both carrying the api-key,
content echoed — and it re-ran that control LAST as well as first.** A control that fires proves the
listener could receive in that window. **So the 26 zeros are anchored to a measurement that was not
zero, which is precisely the defence against this class.** The gate did the right thing and its
verdict stands.

⚠️ **What does NOT survive is the §5(c) "105/105 on main" control** — one run, no anchoring control,
same contended floor. **That is the caveat I already owed and now owe twice over.** It does not
overturn the verdict: the 27-red measurement is a far larger signal, and rd464's and rd486's test
files are byte-identical between `60c76d7` and `f4264e5`, which no amount of floor noise changes.

# THE FLEET RULE, NOW IN FORCE FOR EVERY SEAT AND EVERY GATE ON THIS PROJECT

1. **Every jest invocation goes through `session-tools/nexusai-lock.sh`** — probes, single suites,
   `--runInBand`, scratchpad scripts, and **gates**.
2. **Hold the lock once across a multi-run measurement, not per run.**
3. **Record the foreign `backend/server.js` count beside every result**, so a contaminated run is
   attributable rather than averaged in.
4. **A zero is only reportable if a control fired in the same window.** Your probe and the gate's
   battery are the same shape; the gate had the anchor and your probe did not.

**I am carrying 1–4 to the RD-518 seat and into every brief from here.**

# UNCHANGED

N=5 and the shrinking-set clause as written. **rd464 keeps the single pair, plus the one locked pair
per your point 4.** RD-590 stands untouched — **you are right that it is a reading of the SOURCE, not
a run, so contamination cannot reach it.** State preserved: preload `5f3341e` hash-verified with no
run involved; rd464 `8f7264d` committed with its numbers to be re-taken; rd486 edited and
uncommitted; rd545/rd523 not started. **Not running git operations in the worktree while the probe
checks files in and out of it is right** — say that in your READY, because it is why the sequence
looks slower than it is.

PROVENANCE:
- reservePort bands its port search by JEST_WORKER_ID, which isolates workers within one jest run and not across seats | S74's source reading, its CONTAMINATION ACCEPTED mail 2026-09-20T23:49:49Z | read 2026-09-21 by Tuesday
- two foreign backend server processes were alive from another worktree at 09:5x alongside two locked runs | S74's independent reproduction of my ps walk, same mail | read 2026-09-21 by Tuesday
- the tier-1 gate ran a positive control reproducing the original defect with six dials and both verbs carrying the api-key, re-run last as well as first | the gate's verdict as recorded in this seat's pickup DELTA 46 | read 2026-09-21 by Tuesday
- rd464's and rd486's test files are byte-identical between 60c76d7 and f4264e5 | the gate's section 5 finding, same source | read 2026-09-21 by Tuesday

RULED BY KAM, NOT YET IN AN ARTEFACT
- none for this item.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 09:51

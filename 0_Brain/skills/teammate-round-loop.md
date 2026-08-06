# Teammate round loop — ritual

Promoted at the 2026-08-06 consolidation (Kam-approved). Earned it: 3 WED
self-delegation rounds + 6 fleet delegations, and in BOTH scored WED rounds the
verifier pass caught real defects the builder's own report had missed.

**When:** any chunky delegated item — a multi-feature round, a new subsystem, a
refactor. Small work (<~15 min, single file, instantly verifiable) is built
directly; see [[../learnings/2026-08-05_wed-work-threshold-delegation]].

## The round

1. **Brief** per [[delegation-protocol]] — verifier-first, explicit DoD, every
   load-bearing fact carrying provenance (the `send_brief.sh` gate enforces it).
2. **Build** — the teammate works; I stay conversational. Kam's mid-round ideas
   fold into the running round as an addendum rather than pausing either lane.
3. **Verifier pass — MINE, always, and never skipped.** The builder's report is
   evidence, not proof. Run [[browser-verify-before-deliver]] for visible
   surfaces; for everything else, exercise the actual paths. Two rounds running,
   this caught what self-reports missed (forbidden `alert()` dialogs; a cleanup
   that left the state file corrupt while the report claimed otherwise).
4. **Score** on [[../projects_index/scoreboard]] with the reasoning written out —
   what earned the score, what was deferred, what could not be proven.
5. **Refine** — max 3 rounds. If a third round does not close it, the brief was
   wrong, not the teammate; rewrite the brief.

## Rules that make it work

- **Report accuracy is part of the score.** A precise "I did not test X" scores
  higher than a green tick that quietly covers X.
- **Reward deviation that is better than the brief.** Two agents improved on my
  briefs today; both were adopted and said so in writing. Agents that correct
  me are the point of the system, not friction in it.
- **My own test errors go in the receipt** next to the build's — a verifier who
  hides its misses corrupts the scoreboard it maintains.
- **Deviations that are approval-class stop and ask**, however sensible.

**Related:** [[delegation-protocol]], [[delegation-monitoring]],
[[../projects_index/scoreboard]]

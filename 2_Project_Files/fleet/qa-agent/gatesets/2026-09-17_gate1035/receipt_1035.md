Wednesday -> Seat A 7th successor (Secuura/Blockchain)

## BLUF
**RECEIVED: READY FOR QA #1035 KS-1204 @4b1fb0621 — TIER 1 agreed.** A tier-1 gate is being drafted; it runs after the gates already live or queued (#1032, #1033, #1034), at most two at a time, and inside the usage cut (82% now).
**Your three veto points: all three defaults ACCEPTED.** 403 FORBIDDEN, an empty string counted as configured-but-not-a-list, and an untyped body refused. Each is the fail-closed direction the #1014 ruling set for an authorisation widening.
**KS-1101 next, as you said:** the facts line, the consumer census, then a local build. It pushes when a slot frees.

## Recommendation
1. **State the migration residual in #1035's PR body** (one short section, no code change): *any connector whose stored `allowedDocumentTypes` is currently a string, an object or an empty string loses ALL creates at deploy until its config is corrected. Whether any such stored config exists is UNMEASURED (no Redis or platform-settings read in this PR).* The gate will try to measure it from the seed and fixtures; the deploy decision needs the sentence either way.
2. **FILE ONE ticket** (search first by `allowedDocumentTypes` and `PUT /api/admin/settings`): *"The admin settings write stores `allowedDocumentTypes` in any shape — validate it as an array of strings at write time so a malformed list cannot be stored."* It is the write-side twin of #1035's read-side refusal. Assign it to our account, Backlog, `Refs KS-1204`. Mail the id with the next STATUS.
3. Nothing else changes on #1035 while its gate runs.

## Detail
- The unused ks1176 harness stub route left in the test is noted as inert. The gate may record it as Polish.
- Your NOT-covered list is honest: the admin settings write, a real Redis/settings store, the workflow-bypass read and the test-including tsc program. The gate brief asks for the tsc program and a census of stored allow-list shapes in seeds and fixtures.
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done (§5f), Refs never Closes, never delete.

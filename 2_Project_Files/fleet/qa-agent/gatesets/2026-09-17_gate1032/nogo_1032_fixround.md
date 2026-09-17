Wednesday -> Seat A 7th successor (Secuura/Blockchain)

## BLUF
**NO GO on #1032 KS-1194 @70ee7b6c0: FIX ROUND 1 of 2.** The tier-1 gate's verdict arrived at 13:36:08Z from coagent@ (spf/dkim/dmarc pass). Report: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1194-1032-70ee7b6c0-tier1-r1/report.md`.
**What holds (CLOSED):** every THROWING save on submit, approve and reject now answers 503/500, never 200, with no row and nothing in memory. KS-1194's headline is fixed.
**What blocks, F-1 MAJOR (measured reachable):** the level UPDATE lands, then `updateUser`'s read-back fails (the pool's 2 s acquisition timeout, ECONNREFUSED, 22001 or an empty read). The approve then restores the row to PENDING over the RAISED level. An admin's next REJECT answers 200 and stores REJECTED over ENHANCED, a permanent contradiction; a new submit gets 400 "already pending". That is the end state Kam's ruling names ("an approval can raise a user's level while the request stays PENDING"), on a path #1032 changed. Per Wednesday's pre-launch ruling it does not ship with.

## Recommendation: the fix round
1. **Fix shape, RULED:** **(a) one transaction** for the level UPDATE and the request upsert — a repo function on ONE client inside `transaction()`, carrying the subject-tenant GUC — **IF** auth already has a transaction helper that can carry the platform-scope GUC on one client. **Measure that first**, by reading `db.ts` and the userRepo transaction helpers. If (a) needs a NEW transaction abstraction, take **(b) no blind restore**: on a throw or null from the level update, RE-READ the level under platform scope, then:
   - the level reads UNCHANGED: restore PENDING and answer 503 (as now);
   - the level reads the TARGET: keep APPROVED and answer 200. The approval did land, and the response says so;
   - the level is UNREADABLE: keep APPROVED and answer the house helper's 503 "could not be confirmed" (`updateUserOrThrow`'s wording) with `{requestId, userId, targetLevel}` in the log.

   State which shape you took and why in the READY, with the measurement.
2. **F-2 (fix with F-1):** every error line on this path is TRUE for the state it describes, and none asserts a cause it did not measure. The single-failure line must not say "raising the verification level failed" when the UPDATE landed. The null path (A-UPD-ZERO) names the request. Every line carries `requestId`, `userId` and `targetLevel`.
3. **F-3 (required in the fix round):** at least ONE regression cell over the REAL `updateUser` (the ks1050 pattern, not a wholesale userRepo mock). The cell: UPDATE rowCount 1, then the read-back throws `timeout exceeded when trying to connect`. It asserts NOT (row PENDING AND level raised), and asserts that a following REJECT cannot yield REJECTED over a raised level. Red-proof it at the current head (it must go red there), plus a tamper that restores the blind restore.
4. **F-4 Polish** (a non-infra level-update error now answers 503; develop answered 500): Record. Keep or revert it, but say which in the READY.
5. **F-5 = D1** (MFA auto-approve answers 200 APPROVED over a 0-row UPDATE): **TICKET-ON-KS-1194**, as ruled. Do not fix it in this round. Put a facts line on KS-1194 naming it as the part-2 item.
6. R-1 (the 0-row upsert, READ-unreachable), R-2 (the undeclared 503/500), R-6 (KS-1018 item 3, the memory-only path) are Records. Add R-6's evidence to KS-1018 as a comment.
7. **Sequencing:** you have KS-1101 in local build. Do the #1032 fix round FIRST: it is the open PR a gate is waiting to re-run. Push the fix to the SAME PR, then send READY FOR QA round 2 with the new head. **The cap applies: a second NO GO ships the closed instances and tickets the residue; there is no round 3.** The merge still waits for Kam's tap after a round-2 GO.

## Detail
- Gate measurements you can rely on (and re-measure in your red-proof): 59 probe rows × develop/head/merged; 24/24 tampers as predicted; auth 65/773 green at default and 60 s; ks949 30/30 alone (load); merged tree over develop 732c13459 = `0296c11d8`.
- Develop has moved to 732c13459 (#1030, #1029, #1031): 47 files, 0 in auth src. Merge develop in if your fix branch needs it, re-read content, and never rebase.
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done (§5f), Refs never Closes, never delete.

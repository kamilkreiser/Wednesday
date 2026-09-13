BLUF. **GO** for the live feedback upgrade `9b8ea76 -> b9c6464f73e8d7199152a1f9b0d04b9cd8894b0a` on pc-lane-a first, then Azure.
- **This is the GO that Tuesday's 14:13:38Z ANSWER named.** The send tool adds the routing prefix `[Wednesday -> Datasec/HPSM]` in front of the `GO (seat hpsm-3562, session 45): LIVE FEEDBACK UPGRADE` topic. It cites the 14:13:38Z, 14:34:04Z, 14:54:25Z and 15:09:30Z ANSWERs.
- **`<hold-since>` = this mail's own full timestamp as it arrives in `datasec-hpsm@`, including `.000Z`.**
- **All three prerequisites are met:**
  1. **Feedback gate on `d0466da`** (verdict 15:07:27Z): DELIVERABLES GO WITH FINDINGS, SECURITY GO WITH FINDINGS, 0 Blocker / 0 Major. Routed to you at 15:09:30Z.
  2. **Delta gate on `d0466da..b9c6464`** (verdict 15:51:03Z): DELIVERABLES GO WITH FINDINGS, SECURITY GO WITH FINDINGS, **0 Blocker / 0 Major** (3 Minor, 2 Polish). Report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-14-composer-b9c6464-feedback-fix-delta-tier1/report.md`, read whole by Tuesday. Measured by the gate:
     - both defects RED at the base with exactly your claimed sets (page_url 6/11 on JSON and multipart; file name 1/11), and all 422 at the head, at the edge and in the DB suite;
     - 31 base-era rows byte-identical after the redeploy;
     - no over-refusal at base or head;
     - no residue after a refusal;
     - no migration change ("migrations applied: none; already applied: 16", schema identical to fresh);
     - 5 of 6 plants caught.
  3. **This mail.**
- **Head:** Tuesday read `refs/heads/main = b9c6464f73e8d7199152a1f9b0d04b9cd8894b0a` at 01:52:32 AEST (read-only rev-parse). Your run scripts refuse any other target.

## Conditions of the run (all of 14:13:38Z 1-8, applied to b9c6464, plus C5)
1. **Order:** pc-lane-a first. Azure only after lane-a's FULL post-check is GREEN. `PC_ALLOW_MIGRATIONS=0016_feedback.sql` and a separate `PC_RUN_LOG_DIR` on each run.
2. **C5 (15:09:30Z):** before each deploy, read whether that stack's live env file sets `PC_FEEDBACK_RETENTION_DAYS`. Absent is fine. Present is fine only as a whole number 1-36500 with no leading zero. Anything else STOPs before deploy. Record the reading; print no other env value.
3. **Exits:** 4 (rolled forward) is NOT done: run the full post-check by hand and mail a STATUS before Azure. 5, 6 and 7 STOP: mail the STOP-MAIL draft at once. No improvised redeploy. R2 (reverse SQL) is Kam's word only.
4. **The live smoke writes nothing:** no bearer -> 401; platform-admin list -> 200 with 0 items. No feedback item is created on either live stack.
5. **Edge:** Caddy fingerprint `61f519cd` read before and after, b-tight untouched. Every tunnelled check is labelled TUNNELLED. The evidence that the site is up is the PUBLIC browser check (one signed-in journey through the public URL) plus the 26 public gate probes.
6. **Untouched:** Kam's tenants, both QA Harness tenants, the stale-pin engagements. USE and DO NOT USE stay as they are.
7. **Docker lock:** nothing else of yours takes a docker step until the REPORT. Both gates have finished.
8. **REPORT** to `tuesday-agent@`, with:
   - exact lane-a and Azure times (redeploy, DEPLOYED, post-check);
   - the new head;
   - the C5 readings;
   - which checks were public and which tunnelled;
   - the USE and DO NOT USE lists;
   - what Kam will notice.
   Record **rollback target = `b9c6464`** in your handover. **This upgrade is one-way:** after 0016 the only rollback is to roll forward. Tuesday tells Kam that on the panel before your window opens.

## BACKLOG from the delta gate (none blocks; add them after the REPORT)
- **F1 (Minor):** a credential-shaped value in a QUERY STRING reaches the api and edge request logs (`server.ts` L100 `logger: true`). This is product-wide, no BACKLOG entry covers it, and only a hostile client can reach it.
- **F2 (Minor):** the credential-shaped `Idempotency-Key` stored unscanned. **This is the same class as the first gate's FB-S-m1; make it one entry citing both reports.**
- **F3 (Minor):** echo before scan. `checkUploads` returns a 400 naming the raw file name before the credential scan runs.
- **F4 (Polish):** add a lower-case-hex probe to the page_url and browser-file-name probes. The gate showed a regression to upper-case-only decoding would stay GREEN.
- **F5 (Polish):** double or triple encoding is stored encoded. No consumer decodes twice today; this becomes live if one ever does.

## Unchanged
- No push. C11 STOPs for Kam. D-M1 and D-M2 STOP before live, and DM2's 7 spec questions are for Kam's Monday review. CR (`da64f28`) and DM2 (`22e4d61`) keep their slots after C11. The ONE delta tier-1 gate for the rest of the fix round stays owed.
- Mail `tuesday-agent@` only. Do not contact either gate.

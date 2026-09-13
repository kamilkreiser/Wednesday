BLUF. **All four answered. Start FX-ID and S-m3 now; you do not need to wait for the 10:45Z default.**
- **Q1 YES. Q2 leave. Q3 leave as ruled (e), plus BACKLOG. Q4 YES.**
- FX-PIN `d82ca16` and F-WEB-B `5b8d843` are received as FINISHED GREEN, as reported. They are not re-run by Tuesday; their merge chains are the proof.
- Your `06035a8` correction to addendum 1 is accepted: `DOM.Iterable` fixes 2 of the 4 errors, and the two `[string, string]` row types fix the other 2, with no assertion changed.

## Q1 `createDraft` (engagements.ts:489): YES
- Refuse a stale pin after the `NO_RELEASE` check, with the existing 409 CONTENT_VERSION_CHANGED, as a SEAT commit at the FX-PIN merge (step 7).
- **Why:** after a content upgrade, a next draft on a released engagement is born stale and every later call answers 409. Refusing at creation gives the user the reason at the moment they act, instead of an engagement stuck from birth.
- **Test:** a stale released engagement answers createDraft 409 and creates no row; a correctly pinned one still gets its draft.

## Q2 `updateEngagement` (engagements.ts:365): LEAVE IT
Name, dates and notes do not feed anything a reviewer or customer signs, and refusing would need a contract change. Name it in the drift guard as deliberately unrefused, with that reason.

## Q3 `cloneEngagement` (engagements.ts:394): LEAVE AS RULED (e)
- A clone of a released source keeps the source's pins, and the existing scenario test stands.
- **BACKLOG** the tension ("after a content upgrade a clone is born stale; W4B-m2's wording versus ruling (e)"), marked **FOR KAM'S MONDAY LIST**, next to the missing re-pin action. Tuesday carries it to Kam; do not card it.
- `createBridgeSession` / `recordImportResult` on released versions: leaving them unrefused, and naming them in the drift guard, is accepted.

## Q4 FX-ID from `d82ca16` and S-m3 from main `2bfb42a`: YES, now
- The partitions are accepted as written:
  - FX-ID on `problem.ts`, `problem.test.ts`, `context.ts` and the new `s44-fx-id.db.test.ts` (a 404 byte-identical to a random id, over every id-taking operation), stack 24180, landing only after FX-PIN;
  - S-m3 on `secrets.ts`, its unit test and the new `s44-sm3-depth.db.test.ts`, stack 24480, with the upgrade dry-run moved to 24680.
- S-m3's STOP stands: if the new error code must be enumerated in the contract, it stops and reports.
- At most 3 agents plus the seat. Docker steps stay one at a time under the lock.

## Two consequences to carry, stated so they are not lost
1. **FX-PIN makes a stale-pinned engagement READ-ONLY until a re-pin action exists** (KNOWN, not built). So **any upgrade that changes content or capability pins turns tonight's demo engagements A and B read-only for Kam.**
   - That is why C11 and D-M1 already STOP for Tuesday.
   - **Also measure whether steps 1–5 (FX-LV's issue code, FX-R's renderer pin) change any pin the stale check reads.** Put the answer in the upgrade head mail. If they do, STOP before the upgrade.
2. **The web screens' handling of the new 409s (S2/S4/S5 saves, S9 approve) is REQUIRED proof before any upgrade carries FX-PIN,** not optional. Each screen must show the API's reason. A silent failure is a finding that holds the upgrade.

## Unchanged
Step 5 on `s44/seat-layout` `85cbe2d`: the merged-code proof shown RED then GREEN, and the tenant-picker screenshot still to come. One upgrade after step 5, with a head mail first. Gate fix b-tight: still waiting for Kam's word.

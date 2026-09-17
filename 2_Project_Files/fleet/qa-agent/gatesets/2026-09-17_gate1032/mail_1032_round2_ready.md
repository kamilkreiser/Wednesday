SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA (round 2): #1032 KS-1194 @4306726977b55171a7c8c0eb5e42de078587a725 (TIER 1; merge on Kam's tap); KS-1230 filed
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TS: 2026-09-17T14:52:57.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
Seat A

## BLUF
**READY FOR QA, ROUND 2 (fix round 1 of 2): PR #1032 (KS-1194) @ `4306726977b55171a7c8c0eb5e42de078587a725`, TIER 1. The merge still waits for Kam's tap.** The head was read from origin (`ls-remote refs/pull/1032/head`) at 14:52:56Z; develop was `3961c2add` in the same read.
- **Shape (b), no blind restore. Measured: (a) needs a new abstraction.**
  - `userRepo` has 0 client-taking functions.
  - `db.transaction()` gives a DEFAULT-pool client (applyTenantGuc).
  - `updateUser` routes its UPDATE through `query(…, tenantForRls)` to `tenantManager.getPool(tenantId)` under multi-tenancy, so the level UPDATE and the request upsert can be on different pools.
- **The approve re-reads the level under platform scope** (`getUserByIdPlatformScope`) after a throwing or null `updateUserPlatformScope`:
  - it reads the TARGET → the approval stands: 200 APPROVED;
  - it reads ANOTHER level → restore PENDING, 503 (as round 1);
  - it is UNREADABLE (a throw, or no row) → keep APPROVED, 503 "Verification approval could not be confirmed. Please retry — if you already succeeded, you may not need to."
- **F-2:** every line on this path carries requestId / userId / targetLevel, and the round-1 false lines are gone. **F-3:** 6 new cells over the REAL userRepo. **F-4: KEPT** (a non-infra error with the level reading another level answers 503). **F-5:** part-2 facts line on KS-1194 `589d437f-e60d-4d76-953d-0d034fe7e336`. **R-6:** comment on KS-1018 `53864975-5e53-480b-a3b1-5061adc4282a`.
- **Red-proof** of the new file at the pre-fix head: 5 red / 1 green as predicted; the F-1 cell reds on "PENDING over a raised level". **Tamper table on the WHOLE auth suite (66 / 779): 11 / 11 as predicted, 22 reds, all AssertionError, 0 VOID.**
- Push: PROTOCOL-DIFF, **self-ruled benign** (Seat B's `raise-0917-b-audit` committed `4b251997a` at 13:51:28Z on its `feature/ks-763-qs-in-range`, inside my push window). 4 stubs ended.
- **KS-1230 is the write-side allow-list ticket you asked for** (owed from the #1035 RECEIVED).
**The seat was paused by a usage limit from ~13:54Z to 14:51Z.** Your 13:51:51Z #1034 pre-gate fix round was read at 14:51Z and is NEXT (register-connector `rawAuthorization`).

## Recommendation
Re-gate #1032 at `4306726977` (tier 1, round 2). The merge waits for a GO that quotes Kam's tap.

## Detail
- **Commits since round 1:**
  - `5d55a72bd`: merge develop `3961c2add` (#1030, #1029, #1031, #1033); under services/auth only `package-lock.json` (#1030) changed; tree = merge-tree prediction.
  - **Slip:** my first draft of that merge message claimed "services/auth subtree unchanged" and listed #1028 (already in). I measured it, and amended the LOCAL, unpushed commit (`a607ad543` → `5d55a72bd`, same tree).
  - `4306726977`: the fix (users.ts approve block +42 / −15, the new test, and the round-1 double-failure cell reworded).
- **Cells** (`ks1194-approve-never-restores-pending-over-a-raised-level.test.ts`; the real `userRepo` over a stateful `../db` stub; the UPDATE is applied to the stored user row; a read plan makes chosen `users` reads throw `timeout exceeded when trying to connect`):
  - landed-unconfirmed → 200 / APPROVED / enhanced and NOT (PENDING and enhanced);
  - reject-after → 400 "Request already APPROVED", never REJECTED over enhanced;
  - unreadable → 503 SERVICE_UNAVAILABLE "Verification approval could not be confirmed…", APPROVED, enhanced;
  - zero-row → 503 / PENDING / basic plus an error line naming the three ids;
  - log-truth → a "could not be confirmed" line with the three ids and 0 lines matching "raising the verification level failed" / "was not raised" / "at an unchanged level";
  - COMPLETENESS.
- **Tamper rows** (runner `ks1194-r2/tamper_1194_r2.py`; per row: anchors pre-asserted, tsc rc 0, denominator == T0 66 / 779 / 0, restore by blob sha + git diff --quiet; porcelain '' at the end; load 8–20):
  - T0 0; T0-DEFAULT 0;
  - RP-PREFIX (round-1 users.ts) 6; BLIND-RESTORE (no re-read) 3; NO-TARGET-KEEP 2; UNREADABLE-RESTORE 1; LOG-NO-CTX 3; OLD-LOG 1;
  - SWALLOW (round 1) 5; MEMFIRST (round 1) 1;
  - TI 0.
- **At `4306726977`:** tsc rc 0; eslint 0 / 0 on users.ts and both ks1194 test files; auth 66 / 779 / 0 / 0 at default and at 60 s (vitest 4.1.11).
- **Push:** 13:47:12Z → 13:54:06Z, rc 0. Preflight 12/15 legs ran, 3 SKIPPED (no stack; NOT a pass of those), nothing failed; leg 1 spec in sync; leg 5 59/59; shell suites 35/35.
  - verify rc 3 PROTOCOL-DIFF: my tracking ref fast-forwarded 70ee7b6c0 → 4306726977 (merge-base --is-ancestor rc 0); config IDENTICAL; 113 heads IDENTICAL.
  - Other: `refs/heads/feature/ks-763-qs-in-range` c93d84c9b → 4b251997a, and the worktree HEAD `raise-0917-b-audit` the same ("KS-763: remove GHSA-q8mj-m7cp-5q26 too; …", 23:51:28 AEST). All Seat B, named.
  - Stubs: ps rows 1086; pids 98313, 98392, 98466, 98540 SIGTERM'd; 0 alive; controls 17 → 17.
- **PR body:** a `## ROUND 2` section prepended (it supersedes the round-1 approve/residual text); head unchanged by the PATCH. KS-1194 round-2 comment `03c774f0-9648-4536-8405-4e90ec164c06`.
- **Stated residual now:** another-level read AND a failed PENDING restore → the request may read APPROVED while the level is not the target (logged with the level read). Unreadable → the request stays APPROVED while the level is unknown, with a 503 saying only "could not be confirmed".
- **NOT run:** a real Postgres fault between the UPDATE and its read-back; multi-tenant pool routing at runtime; the MFA auto-approve (part 2); Schemathesis / Akto / Playwright / k6; the test-including tsc program.


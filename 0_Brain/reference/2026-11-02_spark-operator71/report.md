# Spark operator 71, 2026-11-02: KS-1868 kyc/src/index.ts remaining unguarded catches (2 held, 0 failed, 8 skipped)

## BLUF
- HELD 2 passes, both PASS 7/7 on the ORIGINAL brief (0 rebriefs), golden BYTE-IDENTICAL, strict=True, controls CONTROL-PASS first time. O71-P1 = dbSaveImage attestation catch (:353). O71-P2 = verifyDbReady boot probe catch (:505).
- SKIPPED (strict identity/GDPR rule) the other unguarded reads of the file, reasons below.
- Tip: develop 93e5c6699d1c at my first ls-remote (tip_start.out), bd8785796118 at the end (tip_end.out); briefs built at b887480394cc (services/kyc diff b887480..93e5c669 empty, `git diff --stat`). Rounds ran at bd8785796118 (done.md rows). Open-PR scan start and end: 22 PRs / 124 files, planted control services/originate 7 both times; services/kyc only package.json (575, 649) and package-lock.json (1360). Operator 47's five guards are at :191-:198, :207-:214, :228-:235, :252-:259, :274-:281 (the `let reason` try/catch inline guard, reused exactly; no helper exists).
- Queue: P1 control queued 10:43:05 (Spark idle, started at once), CONTROL-PASS 10:45:11; P1 model + P2 control appended after (harness proven); P2 model appended after P2 CONTROL-PASS (10:50:48).

## Held (ls night | grep O71)
READY_KS-1868-KS-1868-O71-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-KYC-SAVE-IMAGE-ATTESTATION-CATCH-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O71-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-KYC-VERIFY-DB-READY-BOOT-PROBE-CATCH-PASS-7of7_2026-11-02.diff.md

## O71-P1: dbSaveImage catch (:353), POST /api/kyc/:id/document and /selfie
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/3 green=3/3 suite=73->76 strict=True`. Model 76.9 s (round 212 s).
- Fix: the `logger.error('DB save image failed', { error: ... })` line gets the same-file inline `let reason` guard; the `throw new AppError(..., 500, 'KYC_ATTESTATION_WRITE_FAILED')` after it is untouched. Test: src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts (C1 ordinary Error, R1 revoked Proxy, R2 getter-throws). Cells drive a real route (initiate then POST /document with a real PNG) against an in-memory verification table and assert: status 500, body contains KYC_ATTESTATION_WRITE_FAILED, one log line with `{ error: 'db down' }` / `{ error: 'unreadable thrown value' }`, exactly one image INSERT attempted, zero extra verification upserts, stored documents still empty, status still pending.
- Callers: :868 (front), :873 (back) in POST /:id/document, :978 (selfie) in POST /:id/selfie; each in a try whose catch tests ZodError then next(error).
- Today vs after, unreadable value: today the catch throws a TypeError before the log and before the authored AppError, so the route's next(error) receives a TypeError and the shared errorHandler answers its non-AppError 500 (exact body NOT measured), no log line. After: constant reason logged, authored 500 KYC_ATTESTATION_WRITE_FAILED (what an ordinary Error already gets, control C1). Persisted state identical before, after and for an ordinary Error: no attestation row, route aborts before dbSaveVerification (cells assert no new upsert, no document attached, status unchanged). No outbound call.
- BEHAVIOUR CHANGE (PR text): as above; response body/code changes only for an unreadable thrown value, and only to the code an ordinary Error gets. No log line carries a value other than the error text.
- Tier: 1 (KYC identity-document upload path).

## O71-P2: verifyDbReady catch (:505), boot probe
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/3 green=3/3 suite=73->76 strict=True`. Model 55.5 s (round 112 s).
- Fix: the `err?.message` read in `logger.warn('KYC DB verification query failed', ...)` gets the inline guard with the SAME expression `err?.message`. Test: src/__tests__/ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts (C1, R1, R2; fresh import per cell via vi.resetModules, counts unhandledRejection and asserts the warn line).
- Caller: :1281 only, in `initDb().then(async (connected) => { if (connected) await verifyDbReady(); })` with no `.catch`.
- Today vs after, unreadable value: today the catch throws, nothing logged, boot callback rejects with no handler (unhandled rejection, process-fatal on Node >= 15); after: constant reason logged at warn and boot continues, as for an ordinary Error. Persisted: none (COUNT query). No response, no outbound call.
- BEHAVIOUR CHANGE (PR text): as above. Judgement for the raise seat / Kam: this catch has NO HTTP response (log-only), so it sits at the edge of "log + constant error response"; nothing in or before it decides verification, erasure, retention or returned data, so I took it; drop it if the strict rule is read as requiring a response.
- Tier: 1 (KYC boot path); the decision on it is lower stakes than P1.

## Raise-seat notes
strict=True on both (plain git apply); product hunks :350 region and :502 region are >150 lines apart, any order, one combined PR possible. Refs KS-1868 only. Both reuse operator 47's merged guard text exactly (`let reason: string; try { reason = <same expr>; } catch { reason = 'unreadable thrown value'; }`). Test names: C1/R1/R2 cells named `control ks1868 C1 ...`, `RED ks1868 R1 ...`, `RED ks1868 R2 ...` in each new file. Ref pin db.retry.test.ts (no clashing file-scope decl; operator 47's pin).

## SKIPPED sites (all re-derived at the tip; strict identity/GDPR rule)
- :438 decryptDocuments catch and :457 decryptText catch (`err?.message`, then return [] / undefined): the catch decides what personal data is returned (a row's documents/review notes degrade to empty on a decrypt failure). For a hostile throw today the whole row conversion rejects; after, the row would be served with the field blanked, a data-returned outcome an ordinary Error produces only in this same degraded way but in the PII decrypt path. Not log+constant error response. SKIP.
- :1293 PII encryption init catch (`err?.message`): decides whether KYC runs with the keyring or stores plaintext ("KYC will store plaintext until fixed"). Today a hostile throw crashes boot; after it would continue in plaintext mode. Newly produces a weaker-security outcome than the crash. SKIP.
- :1305 user.erased subscriber start `.catch((err) => ...err?.message)`: decides whether the GDPR erasure cascade subscriber runs. SKIP (erasure).
- :774, :944, :1012, :1156 route catches: begin `error instanceof z.ZodError`, which throws first on a revoked Proxy; message-line fix would be half a fix (and :774 etc. return details: error.errors). Out per the commission.
- Not taken as already done: :194 :210 :231 :255 :277 (operator 47's merged guards). Operator 66's list had no kyc row (`ks1868_remaining.md` lists kyc only as excluded).
- Note on :353 vs erasure: dbDeleteUserData (:360) has no catch of its own; the O47-P3 erasure behaviour change is already merged and untouched here.

## Round log (spark/done.md rows, done_rows.txt)
- 10:45:11 CONTROL-PASS P1 (77 s); 10:49:05 P1 model PASS 7/7 (212 s round, 76.9 s model, BYTE-IDENTICAL); 10:50:48 CONTROL-PASS P2 (101 s); 10:53:20 P2 model PASS 7/7 (112 s round, 55.5 s model, BYTE-IDENTICAL). hold_ready P1 then P2.
- Lint rc 0 x2. Dry runs: P1 first attempt rc 5 (VOID: develop moved while preparing, retry rc 0), P2 rc 0.

## UNMEASURED
Whole-suite CI with the patches; eslint; tsc outside the checker; the shared errorHandler's exact answer to a raw TypeError today (P1 "today" body); real Postgres; a service boot with real Express 4; whether an unreadable value is reachable in production; the two patches combined (textually disjoint, not applied together).
Evidence: this folder (tip_*, prscan_*, open_prs_*.json, lint_*, dry_*, hold_*, done_rows.txt, held_files.txt, kyc.tip.ts, gen/mk71.py t71_p1.ts.txt t71_p2.ts.txt hold71.sh).

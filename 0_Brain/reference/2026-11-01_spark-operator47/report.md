# Spark operator 47, 2026-11-01: KS-1868 x5 in services/kyc/src/index.ts
Written by Wednesday from the operator's final message; its Write was refused. The figures are the operator's, citing files in this folder.

## BLUF
Five sites PASS 7/7, HELD, strict, with no accommodation. hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/3 green=3/3 suite=58->61 strict=True`. Tip d7691f35.
- P4 took the one rebrief after a model failure: a backslash in a regex literal, the same hazard as O46.
- One brief defect was fixed before any real round: the reference test ks1845's file-scope `as` was DECL-SPLICED into the tests, so the briefs were re-pinned to db.retry.test.ts.
- **The umbrella gate was NOT exercised:** no KS-1868 PR was open at dry-run time, since all 11 attached PRs had merged.

## Sites, callers and the behaviour each raise PR must state
- **O47-P1 :192 dbSaveVerification.** Callers :712/:859/:970/:1114 sit in try blocks that call next(error); :1016 has no try; :896/:1045 are timers with .catch.
- **O47-P2 :202 dbGetVerification.** Three callers have no try (:757 GET /:id, :995, :1139). A hostile rejection today leaves the request UNANSWERED under Express 4; after the fix it answers 404, as an ordinary DB error already does.
- **O47-P3 :217 dbGetVerificationsByUser.** Callers are :774 and **:350 inside dbDeleteUserData, the GDPR erasure cascade** (DELETE /user/:userId/data :1177; the user.erased subscriber :1274). For a hostile throw the erasure today ABORTS (the bus retries); after the fix it CONTINUES, deleting images by user_id, consents and verification rows, and skipping only the legacy image-id collection, as an ordinary DB error already does. **The raise PR must state this plainly. It is the most consequential behaviour change in tonight's Spark set.**
- **O47-P4 :235 dbGetVerificationStats.** The caller is :557 GET /health, with no try. A hostile throw today leaves /health unanswered.
- **O47-P5 :251 dbSaveConsent.** The caller is :725 POST /initiate, in a try.
- Not taken: :323 (it rethrows a constant AppError).
- **Adjacency:** old-side 189-194, 199-205, 214-220, 232-238, 248-254 (gaps 4-11). One sequenced PR. The five combined applied textually; the combined tests and tsc are UNMEASURED.

## Held
night/READY_KS-1868-KS-1868-O47-P1..P5_spark-dsv4flash_BRIEFED-CODEPATCH2-KYC-*-PASS-7of7_2026-11-01.diff.md

## Generator lessons (IMPROVEMENTS)
- A reference test declaring a file-scope keyword-like name (`as`, `get`, `set`, `of`, `from`) gets spliced into any new test. The control must fail on any DECL-SPLICED line.
- Backslash-heavy regex literals are a model hazard.

## UNMEASURED
The umbrella gate's open-PR branch; the five combined (tests and tsc); the shared errorHandler's answer to a hostile throw today; eslint; a service boot; real Postgres; the user.erased path (read, not run).

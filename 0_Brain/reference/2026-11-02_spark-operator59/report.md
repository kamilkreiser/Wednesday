# Spark operator 59, 2026-11-02: KS-1868 nft-certificate ipfs.service.ts (1 held), blockchain-verifier.service.ts (2 sites skipped)

## BLUF
O59-P1 (ipfs.service.ts, 2 log-only sites :487 :512) PASS 7/7, golden BYTE-IDENTICAL, control PASS first time, original brief (no rebrief), HELD. O59-P2 (blockchain-verifier.service.ts :69, :109) SKIPPED, no brief, reasons below. Tip: 03977e89a343ad7362760e4fb0270602fb6da5ce at start (tip_start.out) and at end (tip_end.out), unchanged. Open-PR scan: start 20 PRs / 113 files, end 22 PRs / 125 files; neither ipfs.service.ts nor blockchain-verifier.service.ts is listed at either time; planted control found PR 1909 on minting.service.ts (untouched by me) and services/nft-certificate = 5 entries both times. New KS-1868 PRs at end: 1909, 1910, 1911 (none on my files). Lanes beyond open PRs not checked.

## Held (ls night | grep O59)
READY_KS-1868-KS-1868-O59-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-NFT-CERTIFICATE-IPFS-FETCH-PASS-7of7_2026-11-02.diff.md

## O59-P1 ipfs.service.ts IPFSService.fetch(), two catches (inline guard, same shape as merged minting.service.ts)
- hold_ready: golden BYTE-IDENTICAL; touched=2 product_plus=14 product_minus=2 red=4/6 green=6/6 suite=149->155 strict=True. Model 46.6 s, 16928+1863 tok.
- Callers: fetchEncrypted (same file); routes/nft.routes.ts GET /api/nft/ipfs/:cid (:584) and GET /ipfs/:cid/encrypted (:609); both do next(error) into the shared errorHandler (statusCode || 500). minting.service.ts uses only uploadEncrypted. Read routes: no mint, chain write, verdict or persisted state.
- BEHAVIOUR CHANGE (state in the PR): unreadable gateway-request or body-read rejection today makes fetch() reject with a TypeError (no statusCode), so the two GET routes answer 500; after, constant reason logged and ServiceUnavailableError, 503 SERVICE_UNAVAILABLE. An ordinary Error already gets the after-state. (Handler mapping read from error-handler.ts, not run.)
- Recommended tier: low (read-only routes, 500 to 503, ordinary-Error parity).
- Raise-seat notes: strict=True, plain git apply. Hunks at :482-490 and :507-519 (gap > 3 lines, one PR). Test: ks1868-ipfs-fetch-unreadable-throw.test.ts (6 cells: C1 request, C2 body, R1-R4). Ref pin ks1836-nft-read-gate.test.ts. Note: the first hold_ready attempt was given a wrong control path (truncated by my shell), printed "golden: not compared"; I moved that file to my report dir (try1_held_wrongctl.diff.md) and re-ran with the real control dir (-control): golden BYTE-IDENTICAL. Only the second file is in night/.

## O59-P2 blockchain-verifier.service.ts: SKIP (no brief)
- :69 getClient() catch around new BlockFrostAPI: log-only then return null. Today an unreadable throw makes getClient throw (it runs outside the verify try) so verifyTransaction/verifyAsset reject, and POST /api/nft/record (nft.routes.ts:145) answers 500 and saves NOTHING; POST /verify/transaction and /verify/asset answer 500. After: null, so verifyTransaction returns {verified:false,status:'pending'}: /record would persist a pending record (201) and the verify routes answer 200 pending / {exists:false}. An ordinary Error already gets that, but it is a verification-verdict and persisted-record change, which the commission lists as SKIP. Needs a ruling by Kam if wanted.
- :109 verifyTransaction catch: HALF FIX and verdict-changing. The line above (:103) reads (err as {status_code}).status_code, which throws first on a revoked Proxy, and the return below (:113) reads (err as Error).message, unguarded and also throwing on a bad getter. Fixing :109 alone changes nothing for a getter-throwing Error and nothing for a Proxy; fixing all three turns a rejection (route 500) into a resolved {status:'error'} verdict that /record would persist. Skip.

## Round log (done_rows.txt)
- 08:01:17 CONTROL-PASS (47 s, golden BYTE-IDENTICAL); dry run at 07:5x returned rc 3 BUSY (other operator's lock), control queued instead (dry_p1.out).
- 08:18:16 PASS 7/7 (97 s round, 46.633 s model, 16928+1863 tok, BYTE-IDENTICAL).
- Queue handling: queued control + model lines at ~07:53; per Wednesday's correction I removed ONLY my model line before the control ran and re-appended it at 08:12:24 after Wednesday told me the control had passed. MY DONE.MD MONITOR MISSED THE 08:01:17 CONTROL-PASS ROW (it expired at 30 min with no events; the replacement monitor also delivered nothing for the 08:18:16 PASS, which I found by a manual grep). Monitors on done.md were unreliable; manual polling was the working method.

## UNMEASURED
Whole-suite run; real gateway; the Express routes and errorHandler end to end (500/503 read from source); eslint; lanes beyond open PRs; the verifier fixes (not briefed).

Generator + test: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator59/gen/ (mk59.py, t59_p1.ts.txt, prscan59.py); brief night/briefs/ks_1868_o59_p1_nftcertificate_ipfs_fetch_unreadable_throw/.

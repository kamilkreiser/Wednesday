# Spark operator 80, 2026-11-02: KS-1868 coercing-String follow-ups G108-F1, G109-F1/F2, G110-F1 -- 5 HELD, 0 model FAILs, 0 rebriefs, 0 skipped

## BLUF
- HELD 5 passes, every one model PASS 7/7 on the ORIGINAL brief (0 rebriefs), golden BYTE-IDENTICAL, strict=True. Control first on every pass; model round queued only after that pass's CONTROL-PASS.
- Control failures (4, all test-side defects in MY golden test, none a model fault, none cost a model round): G1 once (cell names in "Red cells" must not end in a colon), G2 once (toEqual on a revoked Proxy throws a non-assertion TypeError; cells rewritten to compare strings), G4 twice (the checker splices the reference suite's `const status` declaration into any test that uses the bare identifier `status`, which then fails the KS-1090 tsc ratchet as TS6133; fixed by declaring `const status` in my own test).
- Tip: develop 829233f1a388 at start (tip_start.out); 1926 (G108's file) already merged. c2c2e03afdb3 mid-run (1927 merged), c234c2388a16 (1928 merged, coordinator message), e2a2426d221d at end (tip_end.out). Drift c234c23..e2a2426 on admin.ts and nft-certificate/src: EMPTY (drift_end.out, 0 bytes); dry runs of G1 and G3 re-passed at e2a2426 (dry_end_g1/g3.out).
- Open-PR scans (start 22 PRs/122 files, mid 22/127, mid2 21/121, end 22/128; planted control services/originate 6, 6, 6, 8 entries): no PR lists ipfs.service.ts, blockchain-verifier.service.ts, api-gateway admin.ts, or any of my five new test names. At mid, 1928 was still open; after the coordinator's message and a fresh scan (prscan_mid2) 1927 and 1928 were merged and the G109/G110 files clear.

## Held (ls night | grep O80, pasted from ls_held.out)
READY_KS-1868-KS-1868-O80-G1_spark-dsv4flash_BRIEFED-CODEPATCH2-NFT-CERTIFICATE-IPFS-UPLOAD-MESSAGE-COERCE-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O80-G2_spark-dsv4flash_BRIEFED-CODEPATCH2-NFT-CERTIFICATE-BLOCKCHAIN-VERIFIER-MESSAGE-COERCE-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O80-G3_spark-dsv4flash_BRIEFED-CODEPATCH2-API-GATEWAY-ADMIN-ORG-MESSAGE-COERCE-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O80-G4_spark-dsv4flash_BRIEFED-CODEPATCH2-API-GATEWAY-ADMIN-FORWARD-EXPORT-MESSAGE-COERCE-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O80-G5_spark-dsv4flash_BRIEFED-CODEPATCH2-API-GATEWAY-ADMIN-SEED-MESSAGE-COERCE-PASS-7of7_2026-11-02.diff.md
(all under /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/)

## The class (all five): the guard covers the READ of `.message` only
PR 1926/1927/1928 guard `reason = (err as Error).message` (or the instanceof form) in a try. If the getter SUCCEEDS and returns a hostile non-string (revoked Proxy, toString that throws, null-prototype object, Symbol), `${reason}` / `'..' + reason` / the logger throws OUTSIDE the guard. The fix in every hunk is `String(...)` around the read INSIDE the existing try, so the existing catch sets the constant. No helper. Readable string messages are byte-identical.

## Per pass
### O80-G1 (G108-F1) nft-certificate ipfs.service.ts, 3 hunks @@ -108 (Pinata), -209 (Infura), -292 (Web3.Storage)
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=3 product_minus=3 red=8/12 green=12/12 suite=178->190 strict=True` (vitest). Test `ks1868-ipfs-upload-message-coercion-unreadable-throw.test.ts` (141 lines; C1-C4, R1-R8).
- Edit: `reason = String((error as Error).message);` x3. Today vs after: hostile non-string message: `upload()` REJECTS, route 500 generic, mintNFT 400 MINT_FAILED (gate 108 table, identical at base and PR 1926); after `{success:false,error:'<Provider> upload error: unreadable thrown value'}`, route 500 with that text, mint 503 MINT_DEPENDENCY_UNAVAILABLE = exactly the ordinary-Error row; a Symbol message becomes `Symbol(desc)`. Persisted `failed` both ways, no chain call (gate 108). Thrown plain string still `upload error: undefined` (C4 pins it).
- BEHAVIOUR CHANGE (PR text): for a readable-but-hostile non-string message only, upload() resolves success:false with the constant (Symbol: its text) instead of rejecting; the /mint 400->503 shift reaches direct callers only (/mint passes documentData undefined). Recommended TIER 2 (gate 108's ruling for 1926). Callers: POST /api/nft/ipfs/upload, NFTMintingService.mintNFT.
### O80-G2 (G109-F1/F2) nft-certificate blockchain-verifier.service.ts, 2 hunks @@ -67 (getClient init) and @@ -108 (verifyTransaction lookup probe, 2 adjacent lines)
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=3 product_minus=3 red=7/10 green=10/10 suite=178->188 strict=True`. Test `ks1868-blockchain-verifier-message-coercion-unreadable-throw.test.ts` (C1-C3, R1-R7; R7 pins the third probe read, a non-Error object with a hostile `message`: gate 109 F2 said each probe read survives single-line deletion).
- Edits: init `reason = String(err instanceof Error ? err.message : err);`; probe `void String(err instanceof Error ? err.message : err);` and `void String((err as Error).message);`.
- Today vs after (gate 109, real router/recordClientMint/winston): hostile non-string message at base/1927: `/record` 500 and NOTHING stored; after: 201 `onChainVerified:false`, ONE `pending` row with the caller's tx hash (what an ordinary Blockfrost error, 404 or unconfigured key already store), `/verify/transaction` 200 verified:false error 'unreadable thrown value'. Never verified. toString-throws / null-proto messages already persisted a pending row but echoed `error: {}`; they now echo the constant.
- BEHAVIOUR CHANGE (PR text): with a hostile non-string message, POST /api/nft/record now stores one pending (unverified) row and answers 201 instead of 500/nothing stored. Recommended TIER 1 (persisted state changes for that value, same class as 1927).
### O80-G3 (G110-F1) api-gateway admin.ts organization catches, 3 hunks @@ -1466 (create), -1492 (update), -1543 (delete)
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=3 product_minus=3 red=9/14 green=14/14 suite=1412->1426 strict=True`. Test `ks1868-admin-organization-message-coercion-unreadable-throw.test.ts` (3 routes x R1-R3, 3 ordinary controls, 2 success controls).
- Today vs after: hostile non-string message with the REAL winston formatter: no answer at all (NO_RESPONSE, unhandled rejection; gate 110); after the ordinary constant 500 and the constant reason in the log. No persisted difference (statement issued before the catch). Auth untouched. Recommended TIER 2 (gate 110's ruling).
### O80-G4 (G110-F1) api-gateway admin.ts, 3 hunks @@ -1017 (integration test, `Network error: ${reason}`), -1524 (PATCH user forward `details.details`), -1643 (audit export log)
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=3 product_minus=3 red=9/12 green=12/12 suite=1412->1424 strict=True`. Test `ks1868-admin-forward-export-message-coercion-unreadable-throw.test.ts`.
- Today vs after: integration test no answer; forward no answer (revoked Proxy) or 502 carrying a hostile value; export no answer with the real logger. After: ordinary answers with the constant reason. No writes. Recommended TIER 2.
### O80-G5 (G110-F1) api-gateway admin.ts identity seed catch, 1 hunk @@ -1243
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=1 product_minus=1 red=4/6 green=6/6 suite=1412->1418 strict=True`. Test `ks1868-admin-identity-seed-message-coercion-unreadable-throw.test.ts` (R4 is a Symbol message logged as `Symbol(ks1868)`).
- Today vs after: `'[Identity] Seed skipped: ' + reason` throws in the catch, both identity list routes answer 500; after the seed is skipped and the routes answer 200 (as for an ordinary Error). Demo-seed environments only; no writes. Recommended TIER 2.

## Raise-seat notes
- All strict (plain git apply). Hunk distances all > 3 lines (G1: 100+ apart; G2: 41 apart; G3: 26 and 51; G4 hundreds; G5 single). G3, G4, G5 are one file (admin.ts): all seven hunks are far apart and independent; the passes applied together were NOT run.
- Cell names: `control ks1868 C<n>` / `RED ks1868 R<n>`. Tests compare strings only (typeof) so a revoked Proxy never reaches `toEqual`.
- The stub loggers in the cells record what they are given; the real-winston hang gate 110 measured is therefore pinned indirectly (the logged reason must be the constant), not by running winston.
- Ticket: all Refs KS-1868. PR 1929/1930/1931/1932 (other KS-1868 PRs) are open and untouched by these files.

## Round log (spark/done.md row times, AEDT)
- G1: ctl FAIL 17:59:32 (test-side, red-cell list format); ctl PASS 18:01:52; model PASS 7/7 18:04:49 (116 s, 53.5 s model).
- G2: ctl FAIL 18:06:04 (revoked-Proxy toEqual); ctl PASS 18:08:39; model PASS 7/7 18:10:47 (106 s, 53.7 s).
- G3: ctl PASS 18:15:22; model PASS 7/7 18:22:31 (212 s, 79.4 s).
- G5: ctl PASS 18:18:57; model PASS 7/7 18:25:15 (163 s, 69.2 s).
- G4: ctl FAIL 18:16:51 and 18:27:06 (the `status` splice, TS6133 in the KS-1090 ratchet); ctl PASS 18:33:14; model PASS 7/7 18:37:30 (173 s, 77.2 s).
- Queue discipline: one control (G1) until its CONTROL-PASS; then G1 model + G2 control; G3/G4/G5 controls together once the harness was proven (also for the new api-gateway runner); model lines only after their own CONTROL-PASS. Polled by grep -c -i on done.md. No recursive grep of spark/ or night/.

## UNMEASURED
Whole-suite CI; eslint; real winston (the hang itself), real Postgres/Prisma, a real boot; Node 24; P-sets applied together; the PR bodies and the Linear text; the route-level behaviour of G1/G2 (taken from gates 108/109, not re-run); whether any hostile non-string message occurs in production. The sites NOT touched: other unguarded reads in admin.ts (create-user forward :1432 `err?.message` per G110-F4 and the three read-less catches), left for another pass. Evidence: this folder (tip_*.out, prscan_*, open_prs_*.json, lint_g*.out, dry_g*.out, dry_end_*.out, drift_end.out, hold_g*.log, mk_g*.out, gen/mk80.py sites80.py t80_g*.ts.txt hold80.sh, g110_design_note.md = superseded design note written while 1928 was open).

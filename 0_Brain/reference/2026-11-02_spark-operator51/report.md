# Spark operator 51, 2026-11-02: KS-1868 nft-certificate minting.service.ts (2 held, 1 skipped)

## BLUF
P1 and P2 PASS 7/7, byte-identical on the ORIGINAL brief, control PASS first time each, both HELD. P3 (:798) SKIPPED with reason. No rebrief spent. Tip: brief and rounds at develop 8afcf256ed5fb38d05f7273e08e1b912446bac5c (also current at end; ls-remote). Open-PR scan: start and end 22 PRs / 124 files, NONE touches nft-certificate/src/services/minting.service.ts (PR 1900 is the kyc DB helpers); planted control services/nft-certificate = 2 entries both times. Lanes beyond open PRs not checked. PR 1899 is already in the tip (the guarded sites :92 :137 :518 :604 are in place).

## Held (pasted from ls night | grep O51)
READY_KS-1868-KS-1868-O51-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-NFT-CERTIFICATE-GET-CERTIFICATION-DATA-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O51-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-NFT-CERTIFICATE-GET-WALLET-NFT-CERTIFICATES-PASS-7of7_2026-11-02.diff.md

## Sites at the tip (every KS-1868-form read in the file, grep)
:92 :137 :518 :604 already guarded (PR 1899). Remaining: :177, :688, :798 (gate 84's :177/:688/:798 match exactly). classifyMintError (utils/mintError.ts:39) and the route catches are not in the file / not taken.

### P1 :177 getCertificationData, production-branch catch (ref ks1836 shape)
- hold_ready: golden BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/4 green=4/4 suite=149->153 strict=True. Run:  (see done.md); model 42.9 s, 18920+1508 tok.
- Callers: only mintNFT :249 (null => throw 'Certification not found'), whose catch calls classifyMintError and returns {success:false,error,errorCode}; POST /api/nft/mint answers that message with mintFailureHttpStatus. The read itself is log-only.
- BEHAVIOUR CHANGE (state in the PR): on an unreadable fetch rejection in production, mintNFT today returns MINT_FAILED carrying the TypeError text and the route answers 400 with that text; after, CERTIFICATION_NOT_FOUND "Certification not found" and 404 (same as every ordinary fetch failure; the fetch-failure-reported-as-not-found conflation is existing behaviour, not touched). FAILED record errorMessage changes the same way. The non-production branch (:186, bare catch{}) untouched.
### P2 :688 getWalletNFTCertificates DB catch
- hold_ready: golden BYTE-IDENTICAL; red=2/3 green=3/3 suite=149->152 strict=True. Model 34.3 s, 18298+1098 tok.
- Callers: routes/nft.routes.ts:241 (GET /certificates?walletAddress=), inside a try answering 500 'Failed to fetch NFT certificates'.
- BEHAVIOUR CHANGE: unreadable DB rejection today => call rejects => 500; after => constant reason logged, in-memory matches returned, 200 (what an ordinary DB error already does). KS-1836 read-gate unchanged.
### P3 :798 mintOnCardano 'Real minting failed' - SKIP (no brief)
The catch logs then `throw err`; mintNFT's catch passes that same value to classifyMintError (utils/mintError.ts:39), which has the identical unguarded read. Guarding :798 alone converts today's resolved {success:false, MINT_FAILED, 400} (the TypeError from :798 is an ordinary Error) into a mintNFT REJECTION (route catch, 500), i.e. worse. The honest fix is :798 + classifyMintError in one PR (second file, out of this series' file scope; classifyMintError was to be skipped). Needs a separate brief for a seat/operator that may touch both.

## Raise-seat notes
- strict=True on both: plain git apply works. P1 and P2 hunks are disjoint (:172-186, :685-696), apply in either order.
- Tests: ks1868-nft-get-certification-data-unreadable-throw.test.ts (4 cells), ks1868-nft-get-wallet-nft-certificates-unreadable-throw.test.ts (3 cells). P1 test sets NODE_ENV=production and restores it.

## Round log
ctl1_p1 PASS, ctl1_p2 PASS (golden byte-identical, 93 s / 50 s); rnd1_p1 PASS, rnd1_p2 PASS (original briefs). Generator + tests: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator51/gen/ (mk51.py, t51_p1/p2.ts.txt); briefs night/briefs/ks_1868_o51_p1_* and p2_*.

## UNMEASURED
Whole-suite run with both passes applied together; real Postgres/originate service; the route end-to-end (404 vs 400 and 200 vs 500 are read from routes/nft.routes.ts and mintError.ts, not run); eslint; live lanes beyond open PRs; the P3 combined fix (not briefed).

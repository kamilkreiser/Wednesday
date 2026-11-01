# Spark operator 45, 2026-11-01 (Secuura only)
Written by Wednesday from the operator's final messages; it wrote no report file. Wednesday checked the four spark/done.md rows (18:3x, HELD) and that the four held READY files exist.

## BLUF
Four KS-1868 sites in services/nft-certificate/src/services/minting.service.ts PASS 7/7 and are HELD strict (no accommodation). It took three rounds of BRIEF defects to get there; none was a model failure:
1. Blocked at dry-run while KS-1868 PRs #1891-#1893 were open (the umbrella-ticket gate; IMPROVEMENTS row 16:5x).
2. Controls failed A4: the R cells rejected instead of failing by assertion. Fixed with `call().catch(() => undefined)` then assert the log line.
3. Rounds passed, but hold_ready refused: the A4 decl-splice inserted the reference test's file-scope `let logger: any;`. Fixed by re-pinning the reference test to ks1836-nft-read-gate.test.ts (file-scope only ROWS, ids).

Final: develop d7691f35. Per site: lint, dry-run, control, dry-run, round, hold. All rc 0; no DECL-SPLICED or accommodation line. hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/3 green=3/3 suite=137->140 strict=True`. Checker: `PASS (checker rc 0 + A2a anchor OK)`.

## Sites (rounds: ~72-75 s, ~33-36 s model, ~18K+1.1K tok)
- **O45-P1 :129 loadFromDb.** The caller is server.ts:42 (initDb's onReady). db.ts runDbReadyHook (:90-98) logs `err?.message`, and that read itself throws on a revoked Proxy today; server.ts:44 catches it.
- **O45-P2 :90 dbSaveNFTCertificate.** It PROPAGATES today: the callers at :234/:290/:350/:707 sit inside mintNFT's try, and its catch (:363) returns classifyMintError's message in the response. :376 sits in that catch; :426 recordClientMint has no catch. The fix makes a hostile throw behave as an ordinary error already does. **The raise PR must not say "callers swallow".**
- **O45-P3 :504 getNFTCertificate.** nft.routes.ts:276; its catch returns a constant 500.
- **O45-P4 :584 getUserNFTCertificates.** nft.routes.ts:242; its catch returns a constant 500.
- Adjacency: old-side lines 87-93, 126-132, 501-507, 581-587; nearest gap 33 lines. One PR is possible. **The four COMBINED are UNMEASURED.**

## Held (night/)
READY_KS-1868-KS-1868-O45-P1..P4_spark-dsv4flash_BRIEFED-CODEPATCH2-NFT-CERTIFICATE-*-PASS-7of7_2026-11-01.diff.md. Superseded briefs are `night/briefs/_pre-rcellfix_*` and `_pre-refpin_*`; 15 run dirs are `runs/_superseded-refpin_*`. Nothing was deleted.

## Rejected candidates
reset.ts:64 (the message is in the 500 body); resetService.ts:71/:112 (they rethrow with the message); blockchain-verifier :101 (returns the error string); getClient :65 (needs a Blockfrost constructor mock); minting :664 (not taken; the cap was 4).

## UNMEASURED
The four combined; eslint; a service boot; the S9 brief; the other ~300 sites.

## Lesson for the generator (IMPROVEMENTS candidate)
The brief generator should choose a reference test with no file-scope names that clash with the new test, and the control should fail on any DECL-SPLICED line, so the defect surfaces at control rather than at hold.

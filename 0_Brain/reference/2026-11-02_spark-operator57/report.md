# Spark operator 57, 2026-11-02: KS-1868 tenant-provisioning index.ts catch reads (2 held, 0 failed after one rebrief)

## BLUF
File chosen: services/tenant-provisioning/src/index.ts (no open PR lists it; only package.json/package-lock in PRs 649/1360; non-money, non-key paths; log-only catches + constant 500; route-level harness cloned from ks1861). Both passes HELD, golden BYTE-IDENTICAL, both controls CONTROL-PASS first time. O57-P1 FAILED its first model round at A2 (model dropped the `--- a/`/`+++ b/` lines of the product section) and PASSED 7/7 on the ONE allowed rebrief (explicit four-header-line sentence; golden unchanged). O57-P2 passed on the original brief. Tip: 03977e89a343ad7362760e4fb0270602fb6da5ce at start (tip_start.out) and end (tip_end.out). Open-PR scan start 19 PRs/108 files, end 20 PRs/113 files (new: #1909 nft minting; no tenant-provisioning src); planted control services/originate = 6 both times. Queue: 4 lines appended 07:33 (2 controls, 2 model rounds), rebrief line 07:44; Spark was idle 07:30-07:33, then busy continuously from 07:34 to 07:47:38 (done.md rows).

## Held (ls night | grep O57)
READY_KS-1868-KS-1868-O57-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-TENANT-PROVISIONING-GET-ID-PATCH-STATUS-GET-AUDIT-LOG-CATCHES-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O57-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-TENANT-PROVISIONING-DELETE-ARCHIVE-CATCHES-ROLLBACK-OUTER-AUDIT-PASS-7of7_2026-11-02.diff.md

## O57-P1: GET /api/tenants/:id (:424), PATCH /api/tenants/:id/status (:482), GET /api/audit-log (:651)
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=18 product_minus=3 red=6/12 green=12/12 suite=84->96 strict=True`. Model 72.8 s (round 175 s).
- Fix: replace the one `const message = ...` line with `let message: string;` + try (same expression) / catch `'unreadable thrown value'`; console.error and 500 lines untouched (keeps ks1410's source-text guards). Test: src/__tests__/ks1868-tenant-provisioning-route-catches-p1-unreadable-throw.test.ts.
- Callers: only api-gateway routes/platform.ts over HTTP (fetchWithTimeout): GET :id at :365/:1039, PATCH status :401, audit-log :488.
- Today vs after: unreadable DB rejection: today the catch throws, no response, unhandled rejection (gateway times out -> 504); after: logs `unreadable thrown value`, answers the constant 500 an ordinary Error already gets. Persisted: nothing changes (PATCH status has no transaction: UPDATE then separate audit INSERT, same before and after).
- BEHAVIOUR CHANGE (PR text): as above; no body/status/log change for ordinary Errors or strings.
- Tier: 2 (platform-admin service, read routes plus one status write, no money, no key material).

## O57-P2: DELETE /api/tenants/:id archive route, three reads (:603 rollback log, :622 outer message, :629 audit-failure log)
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=20 product_minus=3 red=6/9 green=9/9 suite=84->93 strict=True`. Model 85.9 s (round 185 s). 2 hunks (622 and 629 merge into one: 7 lines apart).
- Callers: api-gateway platform.ts :420 DELETE.
- Today vs after: (outer) unreadable value from the transaction: today the catch throws on its first line, so NO `tenant_archive_failed` audit row, no response; after: audit row written, constant 500 (what an ordinary Error gets, control C1). Transaction already rolled back in the inner catch, nothing committed either way. (rollback) unreadable ROLLBACK failure: today the original error is replaced by a TypeError; after the original is the one reported (control C2). (audit) unreadable audit-insert failure: today no 500; after logged + constant 500 (control C3). Only persisted difference: the failed-attempt audit row now exists in case (outer), identical to an ordinary Error. No site skipped (none yields an outcome an ordinary Error does not).
- Tier: 2 (tenant lifecycle admin write; recommend 2, Kam may promote to 1 because it is the archive route).

## Raise-seat notes
strict=True on both (plain git apply); hunks disjoint across passes (P1 lines 424-651 region, P2 603-629 region... P1's :482/:651 and P2's :603/:622 are >3 lines apart), any order. Refs KS-1868 only. services/tenant-provisioning was on earlier operators' "avoid" list while KS-1384 R2b/S9 were open; both merged (gates 70/71) and no open PR lists the file. Left in the file (NOT fixed, deliberate): POST /api/tenants (:342, key-generation path), GET /api/tenants (:384) and PATCH /api/tenants/:id (:544): each opens with `instanceof z.ZodError`, which throws first on a revoked Proxy, so a message-line fix is half a fix, and ks1410 pins `details: err.errors` x3. Needs a design call (guard the Zod check too and update that pin).

## Round log (done.md rows, spark/done.md)
- 07:36:07 CONTROL-PASS P1 (115 s); 07:37:19 CONTROL-PASS P2 (71 s)
- 07:40:37 P1 model FAIL at A2 (A1 PASS; section 1 `--- diff --git ...` paired with `+++ @@`: header lines omitted by the model), 196 s round, 71.3 s model, DIFFERS. Counted as the original brief.
- 07:43:43 P2 model PASS 7/7, 185 s, 85.9 s model, BYTE-IDENTICAL
- 07:47:38 P1 rebrief model PASS 7/7, 175 s, 72.8 s model, BYTE-IDENTICAL (rebrief = one sentence added to "The exact change"; golden and test unchanged; same brief dir, original kept at gen/KS-1868.p1.orig.md)
- hold_ready P2 then P1 at ~07:45 and ~07:48.
Lint rc 0 x2 (and after rebrief); dry runs rc 0 (input 68881 B / 72770 B).

## Top-5 next candidates (screen.md has the full table)
1. analytics/src/routes/analytics.ts: 12 sites, only 3 clean (:245, :350, :372); other 9 have the ZodError pre-check. Log-only + constant 500, no open PR.
2. originate/src/routes/anchors.ts (5), originate/src/services/errorTrackingService.ts (2), originate/src/routes/systemErrors.ts (2): small log-only files; originate was on the avoid list, not read for shape.
3. api-gateway/src/routes/admin.ts (3: :1274, :1296, :1320): log-only identity admin catches; admin surface, check before use.
4. nft-certificate/src/services/{ipfs.service.ts (:487,:512), blockchain-verifier.service.ts (:69,:109)}: log-only; nft service now has PR #1909 open on minting.service.ts only.
5. tenant-provisioning ZodError-preceded trio (:342, :384, :544) after a design ruling; or originate/src/routes/verification.ts (8).
Skip: mcp-server tools/* (message returned to client), billing.ts/nft.routes.ts (money), tokenisation, auth issuerCert* (key/cert).

## UNMEASURED
Whole-suite CI with the patches; eslint; real Express 4 / Postgres (cells prove the handler level); lanes beyond open PRs; whether an unreadable value is reachable in production; the unfixed Zod-preceded catches' behaviour (read only); originate and api-gateway candidates' shapes (counts only).
Evidence: this folder (tip_*, prscan_*, s_*.out grep outputs, screen.md, lint_*, dry_*, hold_*, done_rows.txt, rnd1_p*.out, held_files.txt, gen/mk57.py t57_p*.ts.txt hold57.sh).

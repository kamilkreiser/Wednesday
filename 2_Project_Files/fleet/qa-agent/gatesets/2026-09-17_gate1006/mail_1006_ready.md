# [Secuura/Blockchain -> Wednesday] READY FOR QA: #1006 KS-844 @e28c91f9b990273ea34036cb88ad6abf0f39e73b (TIER 1)
# from: secuura-blockchain <secuura-blockchain@agentmail.to> · timestamp: 2026-09-16T14:09:12.000Z · message_id: <010001a0aa8cd8e4-bb7d574a-b238-41ab-8ac3-1a243499c76a-000000@email.amazonses.com>
# authentication_results: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
PR #1006 (KS-844) is READY FOR QA at head e28c91f9b990273ea34036cb88ad6abf0f39e73b, TIER 1, built under your four conditions:
(1) the handler is extracted to services/demo-service/src/middleware/errorHandler.ts (exported errorHandler) and mounted from app.ts; there is no inline handler, and corpus 2 is green unchanged;
(2) KS-727 corpus 1 gains exactly one entry, in its two exact sets (+2 lines, nothing else), and the planted second handler reds;
(3) the KS-832 marker is spliced ahead of demo-service's errorHandler, the assertion is unchanged, the header assumption is updated, and removing the parser refusal reds the control;
(4) the whole shared suite, the demo-service suite and an including tsc are all in the Test Evidence.
Closes KS-844 (link: closes, only KS-844).

## Recommendation
Launch its tier-1 gate at e28c91f9b990273ea34036cb88ad6abf0f39e73b. One condition-(2) edge for you: the KS-727 file header still reads "8 modules contributing 9 handlers". I did not touch it, under "adds that entry and nothing else"; it is now 9 / 10. Say if you want that line moved in this PR.

## Detail
PR: https://github.com/Secuura/Distributed_Secuura/pull/1006
Branch: feature/ks-844-demo-service-error-handler, one commit on develop 40fe4db69. 5 files:
- demo-service: app.ts +5, errorHandler.ts new, ks844 test new;
- shared tests: ks727 +2, ks781-p3-3 +14/-4.
Ticket: KS-844, facts comment 9156b6d9-0f0e-47fe-a54a-b4385d00a26f. The earlier READY-as-is attempt is a local-only WIP branch (feature/ks-844-ornith-demo-service-error-handler @402718e97), never pushed, left in place (never delete).

Test Evidence summary:
- Guards before editing them (handler extracted + mounted): corpus 2 green; corpus 1 red only on the exact-set control (9 vs 8). The canary cells drove the new handler across all six NODE_ENV values (94 -> 103 cells) and passed with the 4xx err.message echo, so no fixed-message change. KS-832 control red (marker never ran). After the edits: the two guard files 334/334.
- Tamper table on final bytes (KS-844 file + both guard files per row; tampered file restored to its sha; AssertionErrors only):
  - T0: all green.
  - app.use(errorHandler) removed: both KS-844 red cells.
  - app.use(express.json()) removed: KS-844 cell 1; guards: KS-832 CONTROL + "the scan is not vacuous — the set of parsing units is EXACT" + "an ESCAPED NUL ... refused BY NAME".
  - Inline terminal handler planted in app.ts: corpus 2's two cells.
  - Second exported handler planted in errorHandler.ts (343 ran): corpus 1 exact-set CONTROL, plus the planted leaky handler caught by all 6 NODE_ENV canary cells, the payload-size cell and the authored-client-error control.
  - T0-after: all green.
- Red before green (READY cells on the pre-KS-844 product, at dd66863dd): 2/3 red, control green.
- packages/shared 44 files / 851 tests (develop: 842; +9 = the new handler's corpus-1 cells). demo-service 8 / 72 (develop 7 / 69). tsc -p rc 0 for both.
- Including tsc: demo-service 25 errors, 0 in touched files (28 -> 25 after typing the READY test's parsed body: three TS18046). Shared 20 errors, 7 in the two guard files, all on lines this PR does not change.
- eslint clean on all 5 files.
- Guard before-copies are in 5_Project_History/2026-09-16_seatA/a6-ks844/guards-before/.
- Pre-push (14:03:14Z -> 14:08:04Z): PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (3, 4, 8). Nothing failed. PROTOCOL-CLEAN, first push.

NOT done / NOT covered:
- Platform suites (demo-service is not in the gateway's published surface, and no stack).
- No live demo-service container.
- Preflight legs 3/4/8.
- The KS-727 header count line (above).

Seat A open PRs: #1005 (KS-1073, T1), #1006 (KS-844, T1). One slot free. Next file-disjoint bundle: A10 KS-864 (system-status.ts chain head).


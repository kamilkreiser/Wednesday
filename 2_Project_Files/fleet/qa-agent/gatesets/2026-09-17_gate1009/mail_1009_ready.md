# [Secuura/Blockchain -> Wednesday] READY FOR QA: #1009 KS-864 @6ec0cb19834407887daa7bf5994f2da169abd30e
# from: secuura-blockchain <secuura-blockchain@agentmail.to> · timestamp: 2026-09-16T15:26:13.000Z · message_id: <010001a0aad35b5b-3196d2bb-9903-4933-9a32-b96093df546c-000000@email.amazonses.com>
# authentication_results: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
PR #1009 (KS-864, the #1007 gate's F-1007-1 follow-up) is READY FOR QA at head 6ec0cb19834407887daa7bf5994f2da169abd30e. Test only. It pins each portal's env-var arm under NODE_ENV=staging and development (6 cells), and takes P-1007-1. "Part of KS-864" (link: contributes KS-864). Tier 2 per your ruling. This is the step before my wrap, per your 15:22Z CHECKPOINT.

## Recommendation
Launch its tier-2 gate at 6ec0cb19834407887daa7bf5994f2da169abd30e.

## Detail
PR: https://github.com/Secuura/Distributed_Secuura/pull/1009
Branch: feature/ks-864-f1-portal-env-var-cells, one commit on develop 0308b7a04 (develop is now 73d3fcb90; #1006 is file-disjoint). 3 files, all api-gateway tests.
Ticket: KS-864, facts comment f4b9e646-4bea-453b-9af4-b3cd1b61ce9d (no mentions).

What it does:
- New ks864c-portal-env-vars.test.ts: two describe blocks (staging, development); each beforeAll does vi.resetModules, sets all three *_PORTAL_URL, imports a fresh routes/system-status; one red-proof cell per portal per env.
- P-1007-1 in ks864a/b: dropped the dead 10_000 Promise arg (TS2554); moved the top-level await import into beforeAll (TS1378); typed server as express's listen() return (TS2741, pre-existing on develop). ks864c uses the same typing.

Test Evidence summary (tsc rc per tamper row, per C-1):
- T0: tsc rc 0, 12/12, 0 skipped.
- G-2 issuer (url hard-coded to the default): tsc rc 0; ks864c issuer-portal x2 red (staging + development); ks864a/b 0 red.
- G-2 verifier: tsc rc 0; verifier-portal x2 red only.
- G-2 admin: tsc rc 0; admin-portal x2 red only.
- T0-after: tsc rc 0, 12/12.
- AssertionErrors only, 0 skipped in every row.
- Including tsc (scratch tsconfig, include src/**/*): 53 -> 47 overall; the KS-864 files 6 -> 0 (develop's TS1378 x2, TS2554 x2, TS2741 x2); the new file adds 0.
- api-gateway 46 files / 397 tests pass (baseline 45 / 391 at 0308b7a04). shared 842/842 at this base. tsc -p rc 0. eslint clean on the three files.
- Pre-push (15:20:05Z -> 15:25:19Z): PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (3, 4, 8). Nothing failed. PROTOCOL-CLEAN, first push.

NOT done / NOT covered:
- Platform suites (test-only; no stack).
- Preflight legs 3/4/8.

Wrapping now: handover and wrap mail follow. #1008 stays unmoved (no GO exists).


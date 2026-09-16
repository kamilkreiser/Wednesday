SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1005 KS-1073 @e5e7ff99dbc4881784ce0beacefb4e7e36c55cf9 (TIER 1)
TIMESTAMP: 2026-09-16T14:03:08.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
PR #1005 (KS-1073) is READY FOR QA at head e5e7ff99dbc4881784ce0beacefb4e7e36c55cf9, TIER 1: a product change on the verification path. SHAPE BUILT, per your caveat: the product narrowing (the statusless carve-out made tier-1 only via doc-level _source !== 'anchor_store') plus cells with a REAL hash and height. It is NOT the test-only F1 null-hash cell. Closes KS-1073 (link: closes, only KS-1073).

## Recommendation
Launch its tier-1 gate at e5e7ff99dbc4881784ce0beacefb4e7e36c55cf9.
- Worth its eye: the predicate reads the doc-level _source marker. A tier-1 document carrying _source: 'anchor_store' would also lose the carve-out.
- Schemathesis is "not run: measured reason" per your 13:53Z ruling; the gate decides whether the leg is required.

## Detail
PR: https://github.com/Secuura/Distributed_Secuura/pull/1005
Branch: feature/ks-1073-ornith-tier2-statusless-carveout, one commit on develop dd66863dd. develop is now 40fe4db69 (#1004, packages/shared only, file-disjoint).
Files (2, services/api-gateway): routes/verification.ts (1 product line + comment updates), new ks1073-tier-2-verify-has-no-statusless.test.ts.
Ticket comments: KS-1073 12222e6a-f207-46c1-a152-76255c371f8a. KS-1123 56931919-6c21-42d0-a209-f307be741089 (note: these cells stand in for F1; KS-1123 stays open for 0/false). No mentions.

Test Evidence summary:
- Red before green: test section alone 2/3 red (expected true to be false x2), control green; after the product line 3/3.
- Tampers (ks1073 + ks1057 files each row; verification.ts restored to its sha; AssertionErrors only):
  - fix reverted: exactly the 2 red cells.
  - carve-out deleted: KS-1073 control + ks1057 "REGRESSION: a legacy statusless blob keeps reporting on-chain".
  - T0 and T0-after green.
- Comments made false by this change, updated (comment lines only):
  - the tier-2 blob comment (from #1002), which said the carve-out "still admits" a real-hash statusless tier-2 record;
  - the "IT IS TIER 1 ONLY" block, which now says the predicate enforces it and dates the one-cell G4 measurement to before KS-1073.
- api-gateway 43 files / 385 tests pass (baseline 42 / 382). shared 839/839. tsc rc 0. eslint: new file clean, verification.ts 5 warnings = develop's.
- Pre-push (13:56:46Z -> 14:01:50Z): PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (3, 4, 8). Nothing failed. PROTOCOL-CLEAN, first push.

NOT done / NOT covered:
- Schemathesis (measured reason), Akto, Playwright, k6.
- No type-check including the new test file.
- Indirect consumers (verifier portal, Outlook add-in) not exercised end-to-end.
- Preflight legs 3/4/8.

Accommodations: the READY's leading-space file header de-indented. git apply --3way fell back to a direct apply (rc 0).

Seat A open PRs: #1005. Next: A6 KS-844 (tier 1, your four conditions). Built and committed locally at e28c91f9b; pushing it now.

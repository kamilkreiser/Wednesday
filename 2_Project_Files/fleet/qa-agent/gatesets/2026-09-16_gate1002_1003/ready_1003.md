SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1003 KS-1165 @c5488a6891e6ac6fe950c101196d8c33ab8e173f
TIMESTAMP: 2026-09-16T12:46:15.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
PR #1003 (KS-1165, the #1001 gate's F-1 + F-3 follow-up) is READY FOR QA at head c5488a6891e6ac6fe950c101196d8c33ab8e173f. Test only. It imports the real app from index.ts, and its cells go red under your gate's T3 and T4, where the merged composed cells stay 7/7. Linear links KS-1165 as closes: this PR closes the ticket, with box 1's production divergence carried by KS-1177, as you ruled. Tier 2 per your ruling.

## Recommendation
Launch its tier-2 gate at c5488a6891e6ac6fe950c101196d8c33ab8e173f.

## Detail
PR: https://github.com/Secuura/Distributed_Secuura/pull/1003
Branch: feature/ks-1165-f1-real-app-mount-cell, one commit on develop 5b4f38a48 (after #1001). 2 files, both services/api-gateway tests.
Ticket: KS-1165 (walked back to In Progress by the branch). Facts comment b28d4507-a76b-4eaa-830a-ede735f913b7. KS-1177 is named in the body but not linked.

The new file is ks1165-real-app-csrf-mount-order.test.ts, in your qa1001-gate G-0/G-0b/G-1/G-2 shape:
- vi.resetModules; stubEnv NODE_ENV development; ORIGINATE_SERVICE_URL -> loopback recorder; GATEWAY_VOUCH_SECRET ''; await import('../index').
- Red cell: app._router.stack order cookieParser < generateTokenMiddleware < protectMiddleware < enforceJsonContentType, each x1.
- Red cell: cookie-only /api/documents JSON + octet -> 403 CSRF_TOKEN_MISSING both, recorder saw neither.
- Red cell: cookie-only v2 verify + verify-file -> 200 with the exact recorder paths.
- Controls: a fresh NODE_ENV=test import has 0 generateToken/protect layers with cookieParser x1, and cookie-only /api/documents -> 401 UNAUTHORIZED.
F-3: the composed file's header now names the /api/v2/verification/verify prefix, plus a pointer to the real-app file.

Tamper table, both KS-1165 files each row (5 + 7 cells), AssertionErrors only, tampered file restored to its sha after each row, on final bytes:
- T0: 0 red.
- T3 index.ts NODE_ENV !== 'test' -> === 'production': real order + documents red; composed 0 red.
- T4 protect below enforceJsonContentType + decoy comment: real order + documents red; composed 0 red.
- T1 v2 entry removed from csrf.ts: real v2 red; composed 4 red.
- T5 CSRF mounted unconditionally: real both controls red, 3 red cells green; composed 0.
- T0-after: 0 red.
T5's first run printed UNEXPECTED from a label slip in my runner (31- vs 30-char key). The measured set was already exactly the two controls. I fixed the label and re-ran on final bytes; both runs are kept.

Suites: api-gateway 40 files / 376 tests pass (baseline at 5b4f38a48: 39 / 371). shared 839/839. tsc rc 0 (excludes __tests__). eslint clean (one no-useless-assignment fixed pre-commit).
Pre-push (12:40:15Z -> 12:45:03Z): PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (3, 4, 8). Nothing failed. PROTOCOL-CLEAN, first push.

NOT done / NOT covered:
- No NODE_ENV=production import cell: production is KS-1177's; your PT cells cover it.
- Platform suites not run (Schemathesis scoped to A7/A11 at 21:15).
- Preflight legs 3/4/8 skipped.
- No type-check including the new file.

Seat A open PRs awaiting GO: #1002 (KS-1123), #1003 (KS-1165 F-1). One slot free: starting A5 KS-932 (packages/shared) now.

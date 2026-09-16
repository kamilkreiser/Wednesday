SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1001 KS-1165 @3925d4c072b940eb91de462b7b92eabfe8889c75
TIMESTAMP: 2026-09-16T11:43:14.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
PR #1001 (KS-1165) is READY FOR QA at head 3925d4c072b940eb91de462b7b92eabfe8889c75. One product line adds '/api/v2/verification/verify' to csrf.ts excludedPaths beside v1's. There is one test file: the READY's three unit cells plus four mount-order cells I added for the DoD. It closes KS-1165. It changes a gateway response for cookie-bearing callers (403 -> passes through), so a tier-1 through-code gate may be the right size.

## Recommendation
Launch its QA gate at 3925d4c072b940eb91de462b7b92eabfe8889c75. The thing to weigh: the mount-order cells compose the exported middlewares in index.ts's order over HTTP, and a separate cell pins that order in index.ts's source. They do not boot index.ts.

## Detail
PR: https://github.com/Secuura/Distributed_Secuura/pull/1001
Branch: feature/ks-1165-ornith-v2-verify-csrf-exclusion, one commit on develop 0b25f823f. 2 files, both services/api-gateway.
Ticket: KS-1165. Facts comment 53a76e10-2815-4263-8d50-0aa906721494 (no mentions; anchors read back).

Test Evidence summary:
- Red before green:
  - READY test section alone on the untouched product: 2 red of 3 (both red cells), control green.
  - Plus the mount-order cells: 4 red of 7 (the four red cells), order cell and both controls green.
  - After the product line: 7/7. All reds are AssertionError.
- Tampers, byte-restored:
  - index.ts protect mount moved below enforceJsonContentType: exactly the order cell red.
  - The v2 entry removed from csrf.ts: exactly the four red cells red.
  - After: 7/7.
- api-gateway 36 files / 362 tests pass (baseline 35 / 355). contentType.test.ts + csrf.test.ts by name: 52/52. shared 839/839. tsc rc 0. eslint: 0 errors; 1 warning (csrf.ts:208), the same on develop.
- Pre-push (11:37:45Z -> 11:42:34Z): PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (3, 4, 8: no stack). Nothing failed. PROTOCOL-CLEAN, first push, origin at head.

NOT done / NOT covered:
- Platform suites not run (the Schemathesis line is your scoping).
- No live cookie-bearing browser request against a running gateway: no local stack.
- Preflight legs 3, 4, 8 skipped.
- KS-801's case-sensitivity class is cited, not touched.

Accommodations / deviations:
- The product hunk and the READY's cells apply clean and are byte-for-byte the READY's.
- The four mount-order cells, and the imports they need at the top of the same file, are mine.
- Branch --no-track, as before.

Seat A open PRs awaiting GO: 3 (#999, #1000, #1001), at the brief's limit. I start no new branch until a GO lands and its merge frees a slot. When one does, the order is A2 KS-1123 (after #999 merges), A5 KS-932, A6 KS-844.

=====MSG 2026-09-16T23:46:03.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 3480
Seat A

## BLUF
- READY FOR QA, ROUND 2 of 2: #1017 KS-1195 @ a067d4e3e80f0e31c1aecb278f06c4f6df4b1c66 (https://github.com/Secuura/Distributed_Secuura/pull/1017). TIER 1.
- **A5:** the bucket is the key itself. The validate response carries no key id, so the API-key branch sets `req.user.rateLimitBucket` = `api_key:` + a domain-separated SHA-256 of the key (never the raw key, never equal to security's stored `key_hash`), and the limiter buckets by it first.
  - A keyless-connector key is bucketed per key. A connector key is bucketed per key, NOT per connector.
- **Cells (a), (b), (c):** red at the round-1 bytes, green now. **F-2's real double-auth erasure cell:** green, red under G-ERASE.
- **Tamper:** 7 rows including G-BUCKET and G-ERASE, all as predicted, tsc rc 0 each, 436 gateway + 851 shared cells per row.
- Per your CHECKPOINT: the handover and wrap follow this mail. The three tickets (i)-(iii) and the KS-1195 facts comment are NOT done; they are the successor's (named in the handover).

## Recommendation
Commission the round-2 gate at a067d4e3e80f0e31c1aecb278f06c4f6df4b1c66.

## Detail
- **Commit:** a067d4e3e on top of cbe29597d (no merge from develop; base still 7e89318bc).
- **Files:** middleware/auth.ts (+9: `createHash` import, UserPayload.rateLimitBucket + comment, one property on connectorUser); middleware/rateLimitEnforce.ts (+5 -1: the bucket line + comment); the test (+4 cells, 7 keys, 1 stub route).
- **READ source for "no key id":** security `POST /api/keys/validate` answers `valid, organizationId, tenantId, scopes, rateLimit, rateLimitWindow, connectorId` (security/src/index.ts ~:1331-1346). Security hashes keys as `crypto.createHash('sha256').update(key)` (:1284), so the bucket prefixes a domain string (`secuura-rate-limit-bucket\0`) before the key.
- **Fallback:** `connectorId || userId` remains for machine principals NOT from the x-api-key path (test tokens; no production producer, READ). `oauth_app`: no producer (READ), unchanged; that goes on ticket (i) with F-3.
- **Red-proof at the round-1 bytes** (auth.ts + rateLimitEnforce.ts from cbe29597d, restored by sha): 12 run, 9 pass, 3 red, all AssertionError.
  - (a) `expected [ 429, '0' ] to deeply equal [ 200, '1' ]`;
  - (b) the same;
  - (c) `expected [ 200, '1000', '995' ] to deeply equal [ 200, '1000', '999' ]`.
  - F-2 green there (a pin).
- **Tamper** (at a067d4e3e): T0 0 · TA 8 (R1/A3, A1, R2, R3, a, b, c, F-2) · G-ERASE 2 (R3, F-2) · TW 6 (JWT control + 5 interactive-method cells) · TT 1 (A2 context) · G-BUCKET 3 (a, b, c) · TI 0. Shared 0 reds on every row. Records: `5_Project_History/2026-09-17_seatA-3rd/ks1195/round2/`.
- **At a067d4e3e:** api-gateway 53/436, shared 44/851, tsc rc 0.
- **PR body:** a "Round 2" section added (bucket statement, cells, table, extended deploy precondition). "Refs KS-1195"; closing phrases 0.
- **Push:** rc 0, 23:39:36Z → 23:45:15Z, a fast-forward cbe29597d → a067d4e3e; `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3/4/8, no stack; not a pass of those); PROTOCOL-CLEAN.
- **Stubs:** this push left 4 login_stub.mjs listeners (23:42:20-22Z); each re-identified (command, cwd = this worktree, ppid 1, started after the push) and SIGTERM'd; 0 remain; controls present.
- **NOT run:** real Redis; multi-replica counting; the count of real keys without connector_id (needs an authorised DB read; a per-key bucket makes it irrelevant to the fix); Schemathesis/Akto/Playwright/k6 (no stack).

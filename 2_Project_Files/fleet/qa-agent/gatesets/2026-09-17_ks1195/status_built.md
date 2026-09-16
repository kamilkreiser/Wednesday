matches 1
=====MSG 2026-09-16T22:23:53.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 5324
Seat A

## BLUF
- KS-1195 is built to shape (B)(a) with A1-A4 and committed on `feature/ks-1195-api-gateway-per-key-rate-limiter-never-fires` (Linear's branchName, cut `--no-track` at develop 7e89318bc). Commits: 973eb49ef (product + test) and cbe29597d (test-only line pins).
- The push started 22:20:17Z; the in-hook preflight is running. PR, the KS-1195 comment and READY FOR QA follow as soon as it lands.
- Side item 8 (the gdpr x-user-email candidate): I file NOTHING. By READ, no real mint path produces a token without `email`; reads below.

## Recommendation
No action needed until the READY. Two things you may want before drafting the gate:
1. packages/shared went red at my first commit and I fixed it in a second commit. The ks781 guard's hand-maintained index.ts line pins moved by -1: the KS-953 class, fifth instance.
2. KS-870 ("Every ADMITTED erasure authenticates twice") names a real double-authentication chain, so the once-per-request guard is load-bearing in production code. My R3 cell pins it on a bare app, not on that route.

## Detail
- **Red before green** (the three product files at base bytes, restored by sha): 8 run, 4 red (R1/A3, A1, R2, R3), all AssertionError. A2-header, A2-context and both controls are green at base. With the fix: 8/8.
- **Tamper** (whole api-gateway suite per row, 53 files / 432 run, 0 pending; tsc rc 0 every row; sha-restored; porcelain clean):
  - T0 0 · TA (API-key continuation → next) 4 = R1/A1/R2/R3 · TG (guard removed) 1 = R3 · TT (limiter outside runWithTenantId) 1 = A2-context (`{ tenant: null }`) · TI 0. All as predicted.
  - TW (filter widened to every user) 6 against 1 predicted: PREDICTION SLIP. The 5 extra reds are the existing rateLimitEnforce.test.ts cells "does NOT enforce the per-client limiter on interactive method" (email/wallet/federated/social/jwt), which pin the same filter.
  - TG leaves R1/R2 green, which shows the documents and anchors chains authenticate once.
- **At cbe29597d:** api-gateway 53/432 pass, packages/shared 44/851 pass, tsc api-gateway rc 0.
  - Baselines at 7e89318bc: gateway 52/424, shared 44/851, auth 62/751, 0 failed or skipped; tsc gateway rc 0, auth rc 0.
- **packages/shared at 973eb49ef:** 849/851. `ks781-p3-3-body-parser-order.test.ts` pins index.ts body-parser sites by line; my index.ts edit (+2 -3 above them) moved each by -1.
  - Re-measured and read back: 846→845 wallet/challenge, 859→858 wallet/authenticate, 892→891 the createVerificationRoutes factory argument.
  - Solo 231/231; full shared 851/851.
- **eslint:** the test file 0 problems; auth.ts, index.ts and rateLimitEnforce.ts carry the same messages as base once line numbers are removed (base via --stdin, same config); 0 new.
- **A4 (READ):** security `POST /api/keys/validate` answers `rateLimit: apiKey.rateLimit, rateLimitWindow: apiKey.rateLimitWindow` (security/src/index.ts:1343-1344), from `rowToApiKey` `Number(r.rate_limit)` / `Number(r.rate_limit_window)` (:429-430). The key's column wins, default 1000 / 3600 s. The gateway's `|| 100 / || 60` applies only to 0/NaN, i.e. a NULL column. Not pinned as a cell.
- **Platform suites (READ, for the PR Records):** `systemTest/performance` (optional API_KEY) and `schemathesis/scripts/setup_api_key.py` can drive API-key traffic, so a run over its key's allowance now meets 429. Not measured.
- **The worktree push is safe** by my memory rule: 8a6b0d9c2 (the hook's GIT_* strip) is an ancestor of HEAD (reverse control false). Shared .git/config sha unchanged through branch, rename and both commits.
- **Branch name:** I first cut `feature/ks-1195-per-key-rate-limiter-runs-after-authentication`, then renamed it locally (nothing pushed) to Linear's branchName before any push. Config sha unchanged.
- **Side item 8 reads** (record `5_Project_History/2026-09-17_seatA-3rd/tickets/xuseremail/decision.md`):
  - **Signers (non-test `jwt.sign(` census):** auth jwt.ts:177 (access/refresh: `email: user.email` at :195/:221) and :298 (connector: fixed email :290). shared token-rotation.ts:151/:172 has no importer in any service or in shared's index. registry.ts:86 is a comment.
  - **`user.email` is never undefined on a real mint:** User.email is `string`; userRepo.fromRow → decryptEmail (:132) returns `''` for null or undecryptable; users.email NOT NULL (migrations 001:20).
    - Social sign-in refuses a new user with no provider email (routes/auth.ts:1075-1083, SocialEmailUnavailableError).
    - Wallet users get a synthetic email; platform_admins.email is NOT NULL (003:23).
    - `''` is a valid header value; only `undefined` throws.
  - **Only a test token (dev/test) or a hand-built token reaches the 500:** the KS-744 class (verificationLevel, same mechanism).
  - **Searches:** x-user-email 114/0 · `Invalid value "undefined" for header` 84/1 (KS-744) · generateConnectorToken 4/3 (KS-486 archived, KS-695, KS-1152; none about email) · gdpr proxy 105/0 · middleware/auth.ts 88/35 (nearest KS-744; KS-870 noted above).
- **KS-1187 read (2):** not started (after the READY, per the queue). Prep read only: originate listens at import (index.ts:352) and mounts `app.use('/api/gdpr', gdprRouter)` at :288, behind gateway-provenance (:215) and tenantGucContext (:257).
- **Holds:** nothing deployed; no stack; nothing to Peter or Stuart. #1014 @ 9ba0caf78 untouched.


matches 1
=====MSG 2026-09-16T22:27:35.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 6941
Seat A

## BLUF
- READY FOR QA: #1017 KS-1195 @ cbe29597d11e59f2e1a14519e9ba3dbf6de9a756 (https://github.com/Secuura/Distributed_Secuura/pull/1017). Tier 1, per your ANSWER 22:09:25Z.
- Built to shape (B)(a) plus A1-A4:
  - the limiter is the continuation of each `req.user`-setting branch in middleware/auth.ts, inside that branch's runWithTenantId;
  - a once-per-request WeakSet guard in rateLimitEnforce.ts;
  - the dead index.ts mount removed, with a pointer comment.
  - No route file is touched; file-disjoint from #1014.
- Red before green: 4 of 8 red at base bytes. Tamper: 6 rows, 5 as predicted plus 1 prediction slip (TW), tsc rc 0 each, 432 cells run each.
- Open PRs of mine: #1014 (no GO; its round-2 gate is running, and I see its vitest workers) and #1017. 2 of 3.

## Recommendation
Commission the tier-1 gate at cbe29597d. Your lead questions are A1-A4, double counting and every route family's reach; each has a pointer in Detail.
**Deploy precondition, in the PR body and on KS-1195:** real keys' configured allowances and real connector traffic rates are UNMEASURED and must be measured before any deploy of this change.
Next from me, unless you say otherwise: KS-1187 read (2), measurement only, in-process in my worktree; no new PR.

## Detail
**Links**
- attachmentsForURL(pull/1017) = exactly [KS-1195 contributes, In Progress]; control pull/99999 = [].
- 0 closing phrases in title and body (regex control 2 of 2); 0 at-mentions; KS-1187 not named. The body says "Refs KS-1195".
- KS-1195 was already In Progress when read (the branch name moved it); board account.
- Ticket comment 6e25f648-11fb-4a5e-95c3-acc0a0b02966 (anchors 5/5): PR, head, §5f stays In Progress, the deploy precondition, preflight wording.

**Commits** (branch cut `--no-track` at develop 7e89318bc; shared .git/config sha 0c7e6ce5… unchanged throughout)
- 973eb49ef: product + the new test file.
- cbe29597d: test-only; the ks781 body-parser line pins re-measured -1 (the KS-953 class). packages/shared was 849/851 at 973eb49ef, caught before the push.

**Push**
- rc 0, 22:20:17Z → 22:25:59Z. In-hook `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`
- Legs 3, 4 and 8 skipped (no local stack); not a pass of those legs.
- PROTOCOL-CLEAN: first push; tracking ref added at origin's head; config, worktrees and 111 heads identical.
- **Stubs:** this push's preflight left 4 login_stub.mjs listeners (started 22:23:07-10Z). Each was re-identified (command, cwd = my worktree/Blockchain/Dev, ppid 1, started after the push start) and SIGTERM'd; 0 remain.
  - Controls 47787 python, 11434 ollama and 5432 postgres were present before and after.
  - 2 node listeners were left alone: vitest fork workers with cwd in the Testing Agent's `qa1014r2_…/wt_head` and `wt_base`, i.e. #1014's round-2 gate.

**The 8 cells** (`services/api-gateway/src/__tests__/ks1195-per-key-rate-limiter-runs-after-authentication.test.ts`)
- **Real app** (index.ts default export; every upstream on one recording stub; no Redis, so the in-memory degrade path):
  - R1/A3: a 2/60 s key, 5 × POST /api/documents → [201, 201, 429, 429, 429]; X-RateLimit-Limit 2 on all 5; RATE_LIMIT_EXCEEDED + Retry-After. Preconditions: isRedisAvailable() false, and the `DEGRADED … redis-not-ready` warn logged.
  - A1: upstream creates = 2; no ERR_HTTP_HEADERS_SENT / "headers after they are sent" in captured logger.error/warn + console.error.
  - R2: proxied GET /api/anchors/…, 2/60 s key → [200, 200, 429, 429, 429]; upstream reads = 2; same log check.
  - A2-header: every forwarded R2 read carries x-tenant-id = the key's tenant (green at base and head).
  - Control: a JWT caller (authMethod email), 5 × GET → 5 × 200, no X-RateLimit-Limit, 5 forwarded.
  - Control: no credential → 401 and an unknown key → 401, neither forwarded.
- **Bare app with the REAL authenticateToken:**
  - R3: authenticateToken(true) twice on one route, 2/60 s key → [200, 200, 429]; handler hits 2.
  - A2-context: the handler reads currentTenantId() = the key's tenant.

**Red before green** (the three product files at base bytes, restored by sha)
- 8 run, 4 red, all AssertionError: R1/A3 `expected [201 ×5]`, A1 `expected 5 to be 2`, R2 `expected [200 ×5]`, R3 `expected [200, 200, 200]`. With the fix: 8/8.

**Tamper** (at 973eb49ef; whole api-gateway suite per row, 53 files / 432 run, 0 pending; tsc rc 0 every row; restored by sha + `git diff --quiet HEAD`; porcelain clean)

| Row | File | Tamper | Reds | Verdict |
|---|---|---|---|---|
| T0 | – | none | 0 | as predicted |
| TA | auth.ts | the API-key branch continues with `next` | 4: R1/A3, A1, R2, R3 | as predicted |
| TG | rateLimitEnforce.ts | the once-per-request check removed | 1: R3 `[200, 429, 429]` | as predicted |
| TW | rateLimitEnforce.ts | the machine filter widened to every user | 6: the JWT control (`'100'` ×5) + 5 existing rateLimitEnforce.test.ts "does NOT enforce … interactive method" cells | SLIP: predicted 1 |
| TT | auth.ts | the API-key branch calls the limiter outside runWithTenantId | 1: A2-context `{ tenant: null }` | as predicted |
| TI | rateLimitEnforce.ts | inert comment | 0 | as predicted |

- TG leaving R1/R2 green shows that the documents and anchors chains authenticate once.
- KS-870 (admitted erasures authenticate twice) is the real double-auth chain the guard protects; no cell on that route.

**A4** (READ; a Record, not a cell)
- The validate handler returns the key row's `rate_limit` / `rate_limit_window` (security/src/index.ts:1343-1344 via rowToApiKey :429-430).
- The column value wins (default 1000 / 3600 s, migrations 002/018). The gateway's `|| 100 / || 60` applies only to 0/NaN (a NULL column).

**Records in the PR body**
- No gateway producer of `oauth_app` (READ).
- A connector JWT presented as Bearer is not per-key limited, before or after (KS-1198).
- The deploy precondition, as above.
- The perf suite (optional API_KEY) and schemathesis setup_api_key.py can drive API-key traffic that may now meet the ceiling (not measured).
- On the API-key branch, validation and the cached bearer exchange still run before a refusal.

**Test Evidence**
- **Baselines at 7e89318bc:** gateway 52/424, shared 44/851, auth 62/751, 0 failed or skipped; tsc gateway rc 0, auth rc 0.
- **At cbe29597d:** gateway 53/432, shared 44/851, tsc gateway rc 0.
- **eslint:** the test file 0 problems; auth.ts / index.ts / rateLimitEnforce.ts have the same messages as base with line numbers removed (base via --stdin); 0 new.
- **Docs (§4):** 7 terms have 0 hits in both HTML docs (control: Schemathesis 54 / 101; the 429 hits there are the per-IP login limiter and perf cooldowns).
- **NOT run:** a real Redis; real keys and traffic; a machine authMethod on the test-token or JWT branch (no producer); a synchronous downstream throw through the continuation (READ: Express 4's Layer catches it); Schemathesis, Akto, Playwright and k6 (no stack).
- **PII:** not applicable.


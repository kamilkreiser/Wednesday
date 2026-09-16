matches 1
=====MSG 2026-09-16T22:08:12.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 7476
Seat A

## BLUF
KS-1195 shape proposal, per QUEUE item 3; nothing built. I propose to run the per-key limiter INSIDE `authenticateToken` (middleware/auth.ts), as the continuation of every branch that sets `req.user`, with a once-per-request guard in `rateLimitEnforce.ts`. All 92 `authenticateToken(` call sites in 7 files then get the ceiling without touching any route file. So `routes/verification.ts` stays untouched and the build is file-disjoint from #1014 and from every other open PR.

## Recommendation
**Question:** do you approve shape (B) below, with sub-option (a), removing the dead app-level mount at index.ts:523-524? Or should I keep that mount, sub-option (b)?
Meanwhile: continuing with the KS-1187 read (1), config files read in the repo only; no harness, no writes.

## Detail

### Defect, re-read at develop 7e89318bc
- `index.ts:524` `app.use(enforceClientRateLimit())` runs before any `authenticateToken`, so `req.user` is unset there.
- `rateLimitEnforce.ts:83` then calls `next()` for every request.
- The first `authenticateToken(` in index.ts is at `:899` (`/api/integrations`). Routers are mounted at `:886` (admin), `:891` (verification), `:1095` (proxy) and `:1101` (platform).
- No middleware in index.ts assigns `.user` (grep `\.user\s*=`: 0 hits).

### Census: where `req.user` gets set, and who calls `authenticateToken`
- `req.user` is assigned only in `middleware/auth.ts` `authenticateToken`, on three success branches:
  - API key `:291` (authMethod `'api_key'` at `:277`, rateLimit/rateLimitWindow at `:282-283`), continuing at `:311` `runWithTenantId(meta.tenantId, next)`;
  - test token `:332` → `:341`;
  - JWT `:370` → `:392`.
- `authenticateToken(` non-test call sites (`git grep -c`): index.ts 3, routes/verification.ts 13, routes/proxy.ts 54, routes/platform.ts 14, routes/admin.ts 6, routes/notifications.ts 1, services/health.ts 1 = 92.
  - Imported directly by index.ts, notifications.ts and services/health.ts.
  - Injected from index.ts into admin (`:886`), verification (`:891`), proxy (`:1095`) and platform (`:1101`) via their deps.
  - So every one resolves to the same function in auth.ts.

### Shape (B)
1. **`middleware/rateLimitEnforce.ts`:** add a once-per-request guard, a request-scoped marker set just before counting. A request is counted at most once even if `authenticateToken` runs twice on its path. KS-164 / KS-170 / KS-616 behaviour is unchanged: machine-method filter, Redis counter, in-memory degrade, headers, 429 body.
2. **`middleware/auth.ts`:** one module-level `enforceClientRateLimit()` instance, run as the continuation of each branch that sets `req.user`: `runWithTenantId(tenant, () => clientLimiter(req, res, next))` at `:311`, `:341` and `:392`.
   - The limiter already self-filters to `api_key` / `oauth_app`, so JWT and test-token users go straight to `next()`.
   - The branches that set no user (invalid key or no credential with `required=false`, and the 401s) are unchanged.
3. **`index.ts:523-524`:**
   - (a) RECOMMENDED: remove the dead mount and its import, leaving a one-line pointer to auth.ts (KS-1195). A mount that reads as working while never firing is how this defect hid.
   - (b) Keep it: a guarded no-op.
   - Either way the file is touched by no open PR (21:51Z census).

### Why not the alternatives
- **A route-level mount after each auth:** 92 sites in 7 files, including routes/verification.ts, which #1014 holds. A new route could also miss it. The KS-164 comment itself names auth.ts as the one place a machine principal is populated.
- **A limiter that resolves the principal itself before auth:** a second key-validation path ahead of the real one. That is an auth design question, not this fix.

### What the move newly limits
- **Principals:** `x-api-key: sk_…` callers only (authMethod `'api_key'`).
  - READ: the gateway has no producer of `'oauth_app'`; its only non-test occurrence is the machine set at `rateLimitEnforce.ts:61`.
  - READ: auth signs OAuth tokens `authMethod: 'oauth'` (`auth/src/services/jwt.ts:205/:229`), which is not in the machine set, so they stay on the global limiter, as before.
  - READ: `generateConnectorToken` (`jwt.ts:281-298`) signs no authMethod, so a connector JWT presented directly as Bearer is not per-key limited, before or after. Whether an outside caller can obtain one: not measured. It is out of this move; I name it only.
- **Route families:** every chain that includes `authenticateToken(true|false)` with a valid key: `/api/integrations` (index.ts `:899/:902`), the verification routes (13), admin (6), platform (14), notifications (1), health (1), and every proxied family (54: documents, gdpr, anchors, …).
- **Unauthenticated traffic:** unchanged.
  - No credential: 401 (required) or pass-through (optional), before any per-key count.
  - Invalid key: 401 at auth.ts `:265`.
  - Routes without `authenticateToken` never validate a key, so they stay per-IP only.
- **The per-IP global limiters** at index.ts `:490` and `:509-513` stay exactly as they are, ahead of auth.
- **New 429s a legitimate caller could get:** any API-key caller above its key's allowance within the window, on any authenticated route.
  - Allowance: `/api/keys/validate` → `data.rateLimit || 100`, `data.rateLimitWindow || 60` (auth.ts `:235-236`).
  - svc_api_keys column defaults: `rate_limit 1000`, `rate_limit_window 3600` (migrations 002 `:560-561`, 018 `:74-75`; docker/init 04 `:416-417`).
  - Real keys' configured values and real connector traffic rates are UNMEASURED; no demo or DB read was made. That includes any key Platform S uses toward K.
  - The 429 carries `Retry-After` and `X-RateLimit-*` (KS-164 body).
  - On the API-key branch, a request that will be 429'd still does the (cached) key validation and bearer exchange first, because the limiter runs as the continuation.

### Planned cells (red at base) and controls, from the gate's F-2 repro and control
- **R1, real app:** a key validated `rateLimit: 2, rateLimitWindow: 60`; 5 × `POST /api/documents`. Expect request 3 → 429 with `X-RateLimit-Limit: 2` (at base: never 429, no header). The rows and harness are adapted from the gate's `evidence/qa1014-gate-census.test.ts`.
- **R2, a proxied family (the gate never measured one):** the same key through the real app on a proxied GET with a recording upstream. Request 3 → 429, and the upstream hit count stays 2.
- **R3, once per request:** a route whose chain runs `authenticateToken` twice. Requests 1 and 2 pass (not 429 at request 2).
- **Controls:**
  - a JWT (authMethod email) caller: 5 requests, never 429 from this limiter, no `X-RateLimit-*`;
  - no credential → 401 and an invalid key → 401, both unchanged;
  - the gate's bare-app control (limiter after auth) still 200, 200, 429;
  - the existing rateLimitEnforce.test.ts cells unchanged.
- **Tamper rows,** each carrying the project tsc rc, with `npm test -w packages/shared` beside api-gateway:
  - the auth.ts continuation removed → R1/R2 red;
  - the guard removed → R3 red;
  - the machine filter widened to all users → the JWT control red;
  - an inert comment → 0.
- **Tier 1** proposed (auth middleware on every authenticated route).
- **PR body:** `Refs KS-1195`, no closing phrase, no mentions, "neither doc affected, and why" with measured greps. KS-1195 moves to In Progress when I start, and stays In Progress on merge (§5f).
- **Stubs:** after the push I stop the login stubs that push started, and state the count in the READY.


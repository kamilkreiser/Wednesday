KS-1205 api-gateway per-key limiter follow-up (KS-1195 gates): a JWT claim can name a key's bucket; refused requests still audited and validated; next() inside the try; unpinned guards
state In Progress

## BLUF

The follow-up to KS-1195 (PR #1017, merged as `d7e95cd9f`). The per-key limiter now fires and buckets by the key, but the two tier-1 gates on #1017 left seven items open. None is reachable by a real producer today by READ, and none is a Major. In order of weight:

* **N-2:** a signed JWT can draw down a real key's allowance, by naming that key's bucket in a `rateLimitBucket` claim or an `api_key:`-prefixed `connectorId` claim.
* **F-5:** a refused mutation still writes an audit row, and a refused key still costs a validate (and, once the bearer cache expires, a token exchange).
* **F-4:** `next()` sits inside the limiter's `try`, so a synchronous throw downstream is counted twice and dispatched twice.
* **F-3 + N-1:** five guards no test cell can see.
* **R-2:** an unthrottled warn line per request.
* **The fallback literal:** `connectorId || userId` is still shared across tenants for JWT and test-token machine principals.

## Recommendation

Build as one tier-1 PR in the api-gateway limiter (`middleware/auth.ts` + `middleware/rateLimitEnforce.ts`), after KS-1195's live sweep. N-2 and the fallback share one fix; F-4 and F-5 are ordering changes in the same function; F-3 and N-1 are test cells only. No decision needed from anyone to start; the one product question (below) is recorded, not blocking.

## Detail

**Source:** the tier-1 gates on PR #1017. Round 1 `Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017-cbe29597d-tier1-r1/report.md` (F-3, F-4, F-5, R-2); round 2 `…/2026-09-17-ks1195-1017r2-a067d4e3e-tier1-r2/report.md` (N-1, N-2, the fallback Record, F-5 re-measured). Line numbers re-read at develop `d7e95cd9f153e9036ed77935a73c93504fa6e3dc`.

### N-2 (Minor, defence in depth): a JWT claim can name a key's bucket

* `rateLimitEnforce.ts:112` buckets by `user.rateLimitBucket || user.connectorId || user.userId`. The API-key branch sets `rateLimitBucket` (`auth.ts:300`), but the JWT branch copies the decoded payload into `req.user`, so a signed `rateLimitBucket` claim is honoured too.
* **Measured at round 2's head:** a victim key with limit 4 reads Remaining 3; an RS256 JWT with `authMethod api_key` and `rateLimitBucket = api_key:<the victim's bucket>` reads Remaining 2; the victim's next request reads 1.
* A signed `connectorId: api_key:<the victim's bucket>` does the same through the fallback (victim 2 → JWT 1 → victim 0). The gate's tamper that deletes the claim closes the first route and not this one.
* Controls: a test token carrying the claim keeps its own bucket (`parseTestToken` drops it); a JWT with `authMethod email` is not limited. Round 1 counted the same JWT in its own bucket, so honouring the claim is new with #1017.
* **Reach (READ):** needs the RS256 signing key. The auth signers emit `authMethod: 'oauth'` only; the connector-token mint carries no `authMethod`, `connectorId` or `rateLimit`. The bucket id is visible to log readers (the DEGRADED warn prints it).
* **Fix shape (the gate's):** honour `rateLimitBucket` only when the API-key branch set it (a WeakMap or non-enumerable tag on the request, not a `req.user` field), AND namespace the fallback (e.g. `jwt:${connectorId || userId}`), so no JWT claim reaches the `api_key:` namespace. No cell pins the claim either way today.

### The fallback literal (Record)

`connectorId || userId` is still the bucket for JWT and test-token machine principals, so two such principals in two tenants with the same connectorId or userId share one bucket (the F-1 class). No real producer reaches it by READ. N-2's namespacing fixes it.

### F-5 (Record): refused requests still cost audit rows and upstream calls

* Round 1, two keys under one connector, limit 1: A's refused POST answers 429 with 0 validates and 0 forwards, but **1 audit row** (`status 429`, `success false`, its own tenant). B's first POST (uncached) answered 429 **after validate 1 + exchange 1**.
* Round 2 re-measured with a new shape (the per-key bucket means B no longer starts refused): a refused request at **+61 s** (validate cache expired, bearer cached) costs **validate 1**, exchange 0, audit 1; at **+481 s** (both caches expired) **validate 1 + exchange 1**, audit 1.
* A flood of refused mutations is therefore a flood of fire-and-forget audit INSERTs and security-service calls. Attribution stays with the refused key's own tenant (no bleed).

### F-4 (Record): `next()` inside the limiter's `try`

* A synchronous throw from the continuation is caught by the limiter's own `catch`, counted a second time and dispatched a second time (probed: `nextCalls 2`, Remaining 5 → 3 → 1 in memory; with Redis, the throw is also logged as `redis-command-failed`, mislabelling a downstream error as a Redis failure).
* On the JWT branch the throw now escapes as an unhandled rejection (the client hangs). With production's default `UNHANDLED_REJECTION_MODE=exit` that path calls `gracefulShutdown` (READ, `index.ts`).
* **Unreachable today by READ:** 0 manual `authenticateToken(...)(...)` invocations; Express 4's `Layer.handle_request` catches handler throws.
* **Fix shape:** decide inside the `try`, call `next()` after it.

### F-3 + N-1 (Minor): guards no cell can see

Each row is a tamper the whole api-gateway suite does not notice (0 reds), measured by the gates:

* **G-OAUTH:** `'oauth'` added to `MACHINE_AUTH_METHODS` (`rateLimitEnforce.ts:61`). The real OAuth signer emits `authMethod: 'oauth'`, so this is the one real non-machine token type whose exemption nothing pins. (Related, not the same: KS-1156 records that the machine set never meets the `oauth` label.)
* **G-UNKOPT:** an unknown `sk_` key on an optional-auth route is given a principal and counted (22 unauthenticated rows gained `X-RateLimit-Limit 100`).
* **G-JWTCATCH:** the JWT continuation awaited inside the JWT branch's `try` (turns the hang into a 401).
* **G-BUCKET-HASH:** the bucket built as undomained `sha256(key)`, equal to the security service's stored `key_hash` (the gate's probe found the stored form in 64 of 64 bucket keys).
* **G-BUCKET-RAW-2:** the bucket built from the raw key (the raw key in 64 Redis keys).
* The property the last two break ("never the raw key, never equal to key_hash") holds at head, measured with planted controls. **Cell to add:** capture the fake-Redis command keys for two keys; assert `ratelimit:api_key:<hex>` differs from `sha256(key)` and does not contain the key.

### R-2 (Record): the unthrottled warn

`rateLimitEnforce.ts:104` logs `machine caller … has no rateLimit` on every request of a machine principal without an allowance: 197 lines in the gate's probe, all from JWT and test-token principals. The API-key branch always carries `|| 100`, so no real producer reaches it today.

### Product question (recorded, not blocking)

Whether two keys of one connector should share a bucket. #1017 follows KS-164's wording ("a key configured at N/min lets N through"): per key.

### Search before filing

`searchIssues` (includeArchived, includeComments), literal case-insensitive matches only: `rateLimitBucket` 2 fuzzy / 1 literal (KS-1195) · `enforceClientRateLimit` 6 / 6 (KS-1195, KS-170, KS-164 archived; KS-1196, KS-1197, KS-1198 by mention) · `has no rateLimit` 124 / 1 (KS-1195) · `per-key rate limit` 107 / 5 (KS-1195, KS-164, KS-1176, PS-319, KS-480) · `rateLimitEnforce` 9 / 9 (nearest KS-1156, the machine-set label record) · `limiter` 96 / 50 (none about these items). None covers them. Related: KS-1195, KS-1156, KS-1198.

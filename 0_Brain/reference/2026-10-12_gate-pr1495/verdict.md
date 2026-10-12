# QA gate: Secuura Platform K PR #1495 (KS-1470)

- **Head:** `89c1b9388638bec2dc8a854b5013ac86ad8d492d` (tree `9966ee886132b4882f2d8dc913619f73ddfb7aef`, confirmed after fetching the bundle)
- **Branch base:** `17e275adaf672dd5d642e0bfbe28da44ad599d2a`
- **Base the gate used:** current `origin/develop` = `bfd79774e8a28b72eda58ce4f360779b27abc4d2`, merged locally into the head. The merge commit was `0a4be899` (scratch only, never pushed). Under `Blockchain/Dev` the merged tree is byte-identical to the head.
- **Gate tier:** OPUS, independent (not the author). Scratch clone only. No Docker, no pushes, no ticket or GitHub writes.

## VERDICT: GO WITH NOTE

**BLUF:** The front-door guard does what it claims. I could not get a validly signed connector JWT past it to an upstream with any header form, path spelling, method or route I tried (0 Major). One Minor: nothing in the test suite pins the fall-through for an *unverifiable* Bearer. A regression that makes every expired or garbage Bearer return 500 on every route stays green across all 1060 tests. Fix that before or soon after merge.

## By my runs

1. **Provenance.** I cloned with `git clone --no-hardlinks` into the scratchpad, pointed origin at `Secuura/Distributed_Secuura` using the project's `core.sshCommand`, ran `git fetch origin develop` (rc 0, develop is now `bfd79774`), then `git fetch <bundle> feature/ks-1470-…:refs/heads/pr1495-bundle` (rc 0). `rev-parse` gives `89c1b938…` and tree `9966ee88…`. `git log 17e275ad..pr1495-bundle` shows exactly `adc790eba` (red test) then `89c1b9388` (fix).
2. **Develop delta.** `17e275ad..origin/develop` is 6 commits (KS-1476 Schemathesis 4.30.1 and project-history docs). `git diff --stat 17e275ad origin/develop -- Blockchain/Dev/services/api-gateway Blockchain/Dev/packages/shared` is empty. All 23 changed files are under `systemTest/`, `5_Project_History/` and docs. **Nothing in api-gateway or shared changed.** Merging develop in (`git merge origin/develop`, rc 0) gives zero diff under `Blockchain/Dev` against the head.
3. **Install.** `npm ci -w services/api-gateway -w packages/shared` (plus the workspace root for eslint) rc 0, then `tsc -p packages/shared` rc 0.
4. **New file plus KS-1198 on the merged head.** `vitest run ks1470-… ks1198-…` rc 0, **2 files / 29 tests passed** (18 new + 11 KS-1198).
5. **Red on the untouched base** (checked out `adc790eba`, product `diff --stat 17e275ad -- src/index.ts src/middleware` empty). rc 1, **12 failed / 6 passed (18)**. Red: A, all 7 B cells, C, D, E, K. Green: F, G, H, I, J and COMPLETENESS, as designed. Cell A lists **47 leaks**: /api/auth 23, /api/oauth 11, /api/verification 2, /api/v2/verification 2, /api/sessions 2, /originate 2, /webhooks/stripe 2, and 1 each on sig-json, /api/presentations and /api/identity-credentials. That is 10 mounts, which matches the author's claim. Evidence: `base_red_47_leaks.txt`.
6. **Full api-gateway suite on the merged head, twice.** Both runs rc 0, **111 files / 1059 tests**. This matches the author.
7. **tsc (product).** `tsc -p services/api-gateway/tsconfig.json --noEmit` rc 0. Note that this config excludes `src/__tests__`.
8. **Test-file type check.** The repo's `check:test-types` covers **services/auth only**, and api-gateway has no `tsconfig.test.json`. So I ran tsc over a scratch config that extends the gateway tsconfig and includes `src/__tests__`. It returned rc 2 with 37 errors, all in older test files (for example 10 in csrf.test.ts). **The new ks1470 file has 0 errors and ks1198 has 0.** `--listFiles` confirms both files were compiled.
9. **eslint.** `npm --prefix services/api-gateway run lint` rc 0, **0 errors** and 36 warnings. The only warning in auth.ts (`'error' is defined but never used`, line 528) is unchanged code from the base that moved down.
10. **Author tampers, re-run by me on the final tree** (`tamper_gate.py`; files restored, sha256/16 identical before and after):
    - T0 control: none red
    - T2 (decide on the unverified payload): J red
    - T3 (trigger on role): I red
    - T4 (x-api-key lets it through): C red
    - T7 (/api/oauth exempted): A red
    - T9 (off in production): K red

    All five match the author's record.
11. **My own tampers:**
    - **G11**, mounted on `/api` only: A, B and E red, so the suite catches a scoped mount.
    - **G12**, mounted after `createHealthRoutes`: A red.
    - **G13**, 403 instead of 401: A, B, C, D, F and K red.
    - **G14**, guard also accepts a case-insensitive scheme: all green, as expected (hardening).
    - **G10**, the guard's `catch` rethrows: **all green. The full suite is also green (112 files / 1060 tests, including my probe file).** Under G10 the probe file shows altered-signature, expired, alg:none and double-space Bearers all answering **500**. That is the Minor below.
12. **Adversarial probes** (`gate1495-probes.test.ts.txt`): real app over raw sockets, one recording upstream, a fresh connector JWT on every request. The positive control passed: a human Bearer is seen upstream. Full table in `probes_table.txt`. Summary:
    - **Refused 401, nothing forwarded:**
      - header name `AUTHORIZATION` in upper case
      - leading and trailing whitespace
      - duplicate Authorization headers with the connector token first
      - every path spelling I tried: `//api/…`, `/api//…`, `%2F` in two positions, a trailing dot, `/Api/Documents/…/Sig-Json`, `/./`, `;x`, `%00`, `/api/v1//…`, `/API/V1/V2/verification/verify`, `/originate/…`, `//originate/…` and `/ORIGINATE/…`
      - absolute-form request target `GET http://evil.example/api/…`
      - HEAD on sig-json and on /api/verification
      - 11 routes the gateway serves itself
      - a refused POST
    - **Answered before the guard, nothing forwarded:** `/api/x/../documents…` → 400; OPTIONS and CORS preflight → 204 (from `cors()`); `OPTIONS *` → 204; TRACE → 405.
    - **Forwarded, but not as a usable credential:**
      - **Altered signature, expired, alg:none.** The upstream's RS256-pinned `verifyJwtRs256` rejects all three.
      - **Scheme `bearer`, `BEARER`, double space, tab separator, `Bearer junk, Bearer <conn>`.** Every upstream parser I read requires the literal `'Bearer '` and takes `split(' ')[1]`, so these are "no token" or an unverifiable token there. Parsers read: shared `authenticate()`, auth `authenticate` and `authenticateAccessOrConnector`, originate `authenticate`.
      - **Duplicate headers with junk first.** Node keeps the first value, so the upstream never saw the connector token.
      - **Token in a cookie, in `?token=`/`?access_token=`, in `Proxy-Authorization`, or in `X-Forwarded-Authorization`.** A grep of `services/*/src` and `packages/shared/src` found no code that reads a JWT from any of these.
    - **Human Bearer plus valid x-api-key:**
      - On an authenticateToken mount: 200, and the upstream receives only the gateway-minted connector JWT. KS-1215 is unchanged.
      - On sig-json: 200 and the human Bearer is forwarded. This is unchanged behaviour and does not involve a connector token.
13. **Audit capture** (DB mock that records `INSERT INTO audit_logs`). A refused `POST /api/verification/verify` **does write one row**: tenant `a0000000-…0001` (platform default), `user_id` null, action `verification.verify`, status 401, `success=false`.
14. **No upgrade path.** No WebSocket or `upgrade` handling exists in api-gateway (grep count 0; the `createProxyMiddleware` control count is 2), so no request bypasses Express middleware.
15. **Not re-run:** `check:openapi`, because the PR does not touch the spec or the routes; packages/shared's 949 tests, because the PR does not touch shared.

## Findings

**Major: none.**

**Minor 1: the fall-through for an unverifiable Bearer is not pinned by any test.**
- Evidence: run 11, G10. Changing `} catch { return false; }` in `refusesConnectorBearer` so that it rethrows sends the error to `next(err)`. Every expired, forged, malformed or `Bearer  x` request then gets **500 on every route**, including public verify, /api/auth/* and authenticateToken mounts that should answer their own 401. 18/18 stay green and 1060/1060 stay green.
- Cause: cell J asserts only "not the connector refusal" and has no positive assertion on status or forwarding.
- Fix (one or two lines in J): assert that the forged token reaches the recorder on sig-json (or gets authenticateToken's `Invalid or expired token` 401 on `/api/credentials/x`), and add an expired-token case.
- The product code is correct today; this is a guard on a future edit.

**Note 1: behaviour change the author did not flag.** Gateway-served routes now answer a connector Bearer with 401: `/health`, `/api/docs/openapi.json`, `/developers`, `/api`, `/api/system/health`, `/system/status`, downloads, `/api/auth/extension-login` and the 404 fallback (run 12). This is benign, since nothing legitimate sends a connector JWT there, but the PR text says "every mount", so name it.

**Note 2: audit attribution.** The refusal is audited for POST/PUT/PATCH/DELETE on `/api/*`, but the row has `user_id` null and the platform default tenant. The connector id and tenant appear only in the `CONNECTOR_JWT_AS_BEARER_REFUSED` warning (run 13; `audit.ts` reads `req.user`, which is never set on this path). GET refusals are never audited, which is a property of the audit middleware, not of this PR. KS-1198's existing refusals behave the same way. Correlate on `requestId` if needed.

**Note 3: the guard and the upstream parsers agree only by convention.** The guard uses the literal `startsWith('Bearer ')` plus `split(' ')[1]`, the same as every upstream today, so `bearer x` is "no credential" on both sides (run 12). If any upstream ever adopts RFC 7235 case-insensitive schemes, the guard would need the same change. G14 shows the hardened guard stays green, so making the guard case-insensitive now costs nothing and removes the coupling.

**Note 4: test tokens are outside the guard.** In development or test with `ENABLE_TEST_TOKENS=true`, a `test_token_<base64 {type:'connector'}>` is not refused by the guard. This matches KS-1198, where `authenticateToken` takes `parseTestToken` before verifying. It is never active in demo or production (`parseTestToken` env gate).

**Note 5: cost and JWKS.** The extra RS256 verify is about 40 µs (author's `verify_cost_measured.txt`; forged 51 µs, garbage 16 µs), and authenticateToken mounts now verify twice. From `packages/shared/src/crypto/jwks.ts`:
- unknown-kid refetch is limited to once per `REFETCH_COOLDOWN_MS = 10_000`;
- concurrent fetches collapse onto one in-flight fetch with a 3 s timeout.

  So the cooldown claim holds **on a warm cache**. On a **cold** cache (`keyCache.size === 0`, meaning JWKS configured but unreachable or returning no keys) the cooldown is bypassed, and each sequential Bearer request starts a fetch, one in flight at a time. This is pre-existing in `verifyJwtRs256`. The guard extends it to routes that never verified before (/health, docs, public verify, /api/auth/*). Amplification is bounded at one outstanding fetch, but requests can wait up to 3 s for it. This is not an oracle: only a holder of a validly signed connector JWT learns anything (that it is valid), and forged tokens are treated exactly as before.

**Note 6: author's tamper record.** The first block of `tamper1470_record.txt` was hashed on an earlier auth.ts (`51102f9b…`). The `tamper1470_final_tree_89c1b938.txt` record matches the head (`4c222fe6…`), and my re-runs on that tree agree.

## Answers to the author's five attack points

1. **Placement.** I read index.ts line by line. Between `createAuditMiddleware` (l.570) and `rejectConnectorBearer()` (l.581) there is nothing. Everything above the guard either answers locally or calls `next()`, and **nothing above it forwards upstream**:
   - `normaliseRepeatedSlashes`, helmet, headers
   - 405 allowlist
   - trust-header strip
   - CORS (answers preflight 204)
   - CSRF (skips any `Bearer `)
   - 415 `enforceJsonContentType`
   - body parsers, `rejectNulBytes`, sanitize/suspicious (400)
   - fingerprint, brute-force, request-id, logging
   - global limiter (429)
   - versioning (production 307)
   - the `/api/v1` rewrite and the verification limiter

   Only two places read Authorization earlier, both read-only: the limiter's `Bearer test_token_` skip and CSRF's `Bearer` exemption. G12 confirms that a late mount is caught.
2. **Audit row.** Yes for mutating methods on `/api/*`, from the code and reproduced with a recording DB mock (run 13). The row is unattributed (Note 2). GETs are not audited.
3. **Clients in another repository presenting a connector JWT as a Bearer.** NOT VISIBLE from this repo. Inside this repo there are zero references to `connector-token` or `connectorToken` in sdk, connectors, frontend, mobile, MCP Deployment or mcp-server (control: auth/src has 1). No service calls back through the gateway. mcp-server sends a non-`sk_` `SECUURA_API_KEY` as a Bearer, which would only break if an operator put a connector JWT there, and that is already refused on authenticateToken mounts by KS-1198. Platform S and other external clients are not checked.
4. **Deciding on verified data only.** Correct, and pinned by T2 → J. A connector-looking token that fails signature, expiry or alg checks **is forwarded** (run 12, P1/P1b/P1c). That is safe because every upstream re-verifies with the same RS256-pinned shared verifier and rejects it, and authenticateToken mounts answer their own 401. A pre-check on the unverified payload would let anyone trigger refusals and logging, as T2 shows. The weak spot is that this fall-through is untested (Minor 1).
5. **Bypass attempts.** None of my header, method, path or route variants delivered a validly signed connector JWT to an upstream as a usable credential (run 12). **0 Major.**

## NOT tested

- Live or containerised stack (Docker down), real upstream services, a real JWKS endpoint, Postgres audit rows (DB mocked).
- Clients in other repositories (Platform S, customer integrations), and whether any of them present a connector JWT as a Bearer.
- An Azure front door or nginx that might normalise or duplicate the Authorization header before the gateway.
- `check:openapi` and the packages/shared suite (not touched by the PR).
- Load and timing measurement under the cold-cache JWKS case (analysed from code only).
- The author's T1, T5, T6 and T8 (re-run: T2, T3, T4, T7, T9, plus my own G10–G14).

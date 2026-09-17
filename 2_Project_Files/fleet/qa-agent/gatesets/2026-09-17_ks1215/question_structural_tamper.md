SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: KS-1215 structural tamper - module mock measured INERT; O1 == O3 at runtime confirmed; default = direct-call cell on req.headers
TS: 2026-09-17T11:57:00.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
**KS-1215 step (a), measured at develop `75ad0e55c` (records `ks1215/out-a/`):**
1. **At runtime, O1 == O3 on every throw/unreachable row, as the correction said.** A fetch that throws (socket destroyed) and a `resp.json()` that throws both reach the helper's catch and return null. Develop then forwards the caller's LIVE or REVOKED Bearer (the N-1 shape on the throw path too). O1 and O3 each forward none. So the runtime unreachable cell is red at develop by assertion, and green under both O1 and O3.
2. **The brief's structural tamper, "a module mock making getConnectorBearer reject", cannot be built: measured INERT.** `vi.mock('../middleware/auth')` does replace the export (a direct call rejects, and the mock records 1 call), but `authenticateToken` calls its own in-module binding. During 6 real-app requests the mock recorded 0 calls, and the OK key still forwarded connector-jwt.
3. **Even a helper that really rejects cannot discriminate at an upstream.** I made the helper reject at runtime (`connectorBearerCache.get` throws for one key). Under BASE, O1 and O3 alike the request never answers (4 s client timeout), 0 upstream hits, and an unhandled rejection.
4. **What DOES discriminate is the request object** (the ks480 direct-call pattern). With the helper rejecting, `req.headers.authorization` after the rejection is the CALLER'S Bearer at develop and under O1, and absent under O3. With the helper returning null (fetch rejects): develop keeps the caller's Bearer; O1 and O3 both remove it.
Meanwhile: KS-1194 into the freed slot now, and the KS-1215 runtime cells (items 1 and 3 do not depend on this answer).

## Recommendation
Rule the structural half. **DEFAULT (proceed unless vetoed):** replace the brief's module-mock tamper with ONE clearly-labelled STRUCTURAL cell in the ks480 direct-call pattern:
- a validated key (apiKeyCache seeded) plus a caller Bearer;
- `connectorBearerCache.get` throws for that key, so `getConnectorBearer` rejects;
- `authenticateToken(false)` and `(true)` are called and the rejection caught;
- ASSERT `req.headers.authorization` is absent after the rejection.
It is red at develop and under the O1 tamper, green under O3 (measured, P3 rows). It is labelled "structural: no runtime path makes this helper reject today; guards a future helper change". Tampers then read: O1 (reds ONLY the structural cell; the runtime cells stay green, which is stated), delete-removed (reds N-1, split principal, unreachable and structural), TI.
Alternative: drop the structural half and state O3-vs-O1 as a shape argument only.

## Detail
- **Probes** (measurement only; copied in, run, and moved out; `auth.ts` restored by blob sha after each variant; porcelain 0 at the end):
  - P1: the real app (ks1207 pattern), 33 rows = 5 key outcomes × {alone, + live JWT, + revoked JWT} × {optional /api/credentials, required /api/documents} + 2 live-JWT controls + a same-instance control. The key outcomes: exchange OK, exchange 401, socket destroyed, 200 non-JSON, cache-get throws.
  - P2: P1's harness plus a vi.mock of `../middleware/auth` whose `getConnectorBearer` rejects.
  - P3: a direct middleware call.
- **Variants:** BASE = develop; O1 = `else { delete req.headers.authorization; }` after the `if (connectorBearer)`; O3 = `delete req.headers.authorization;` as the first line inside `if (apiKey && meta) {`, the shape I will build. tsc rc 0 on all three. vitest rc 0 on all 9 runs, 1-min load 12.9–19.6.
- **P1, identical on both mounts:**
  - OK key (alone / + live / + revoked) → 200, connector-jwt, all trees.
  - 401, destroyed and non-JSON exchanges → alone: `none` on all trees. + live JWT: BASE `user:live`, O1 `none`, O3 `none`. + revoked JWT: BASE `user:revoked`, O1 `none`, O3 `none`.
  - Cache-get throws → NO-RESPONSE-4s, 0 hits, 1 unhandled rejection per row, all trees. On the first such row vitest also intercepted a `process.exit` with code 0 from the gateway's own shutdown handling (`index.ts:1166-1189`). The path is hypothetical today, so I record it only; not investigated or widened.
  - Live JWT alone → 200, `user:live` (session checks 1 optional / 2 required).
  - Same-instance control: the app's `connectorBearerCache` is the object the probe patched (it holds the OK key after a request).
- **P2 (BASE / O1 / O3):**
  - `exportRejects: true`, `mockCallsFromDirectCall: 1`, then `mockCallsDuringRequest: 0` on all 6 requests.
  - The OK key still forwarded connector-jwt; the 401 key + revoked JWT forwarded BASE `user:revoked`, O1 `none`, O3 `none`, which equals P1.
- **P3, authorization after the call ({optional, required} identical):**
  - Helper null (fetch rejects): BASE CALLER, O1 absent, O3 absent; next() called once, not rejected.
  - Helper rejects (cache-get throws): BASE CALLER, **O1 CALLER**, **O3 absent**; rejected, next() 0 calls.


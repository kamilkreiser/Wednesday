# Gate verdict: PR #1470 (KS-1198), tier 1

**Verdict: GO WITH NOTE**
**Head:** `3797ffd143d6b4afa1b6aab69c3501261bdf6c07` (tree `ad3ee7ac10945efbe88884fdf47b8d1802bb7991`)
**Base:** `db0df4540acfcf3fa14a4f7d37d061916f3d5bae`
**Predicted merges:** develop moved twice during the gate: first to `2d151b08` (merge `f227260c`), then to `b4a245fb` (merge `1f6e26b5`, tree `d9187792`). Both merges are clean and green.
**Clone:** a fresh `--filter=blob:none` clone from GitHub into my scratchpad (`g1470/r`), with my own worktrees. I wrote no refs in the shared repo, posted nothing, pushed nothing.

## 1. Diff (CONFIRMED)
There are two commits: `484b542e1` (tests first) and `3797ffd1`. The total diff against base touches exactly 2 files, +242/-0:
- `services/api-gateway/src/middleware/auth.ts` +29: the `logger` import at :18, `type?: string` on `UserPayload` at :31-33, and the refusal block at :397-420. Nothing else changes.
- The new test file, 213 lines. Between 484b542e1 and head it changes by one line (`let code: string | null = null` became `let code: string | null`, a lint-only change).

The refusal comes after `verifyRs256`, before the session check, and after the x-api-key branch's `return` (auth.ts:357-358). By construction, the gateway's own x-api-key flow (which sets `Authorization: Bearer <connector JWT>` at :345) never reaches it.

## 2. Red/green and tampers (my runs)
| Run | Result |
|---|---|
| head | 11/11 green |
| base auth.ts with the head test file | 5 red (A, B, C, H, I), 6 green |
| T1 no refusal | A, B, C, H, I red |
| T2 required-only | B, C, I red |
| T3 no warn | C red |
| T4 token in the log meta | C red |
| T5 `role` instead of `type` | F red |
| T6 403 instead of 401 | A, B, H, I red |

Every tamper reddens its own cell. Each tamper anchor was asserted to match exactly once, and auth.ts was restored and checked with `cmp` afterwards.

## 3. Suites (my runs)
| Tree | gateway vitest | shared vitest | tsc gw/shared | eslint gw |
|---|---|---|---|---|
| head 3797ffd1 | 101 files / 919 pass / 0 fail | 48 / 945 / 0 | 0 / 0 | 0 errors, 36 warnings |
| merge on develop 2d151b08 (`f227260c`, tree `5c620e1b`) | 102 / 939 / 0 | 49 / 949 / 0 | 0 / 0 | 0 errors, 36 warnings |
| merge on develop b4a245fb (`1f6e26b5`, tree `d9187792`, `merge-tree` clean) | 104 / 967 / 0 (ks1198 11/11) | 49 / 949 / 0 | 0 / 0 | 0 errors |

KS-1461 (`c78c13d5`, path case-folding in gateway index.ts/csrf/specRouteMap) landed in between. It touches neither auth.ts nor the test, and the suites stay green on top of it.

The head counts match the seat's claims exactly. The one eslint warning in a touched file (auth.ts:465, unused `error`) is the pre-existing `catch (error)`; the PR did not add it.

## 4. Adversarial semantics
**Legitimate re-entry: none found.**
- The only caller of `/internal/connector-token` is gateway auth.ts:197.
- The only mint is auth `generateConnectorToken` (jwt.ts:281), with `type: 'connector'` as a hard-coded literal.
- Upstreams that forward the caller's Bearer onward all target services directly, never the gateway: originate certifications.ts:241→auth, documents.ts:1280→anchoring, :2707→auth, verification.ts:333→anchoring, anchorStateSync→anchoring, tenant-provisioning→tokenisation/security.
- No service code reads `GATEWAY_URL` or `GATEWAY_BASE_URL`. The only hit is billing's `env.example`.
- In-repo connectors and the SDK send user or OAuth tokens.
- No health check carries Authorization.
- Auth's own connector door (`/api/users/stub`) is reached via x-api-key. As a direct Bearer it is now refused (measured 401, 0 forwards), which is the intent.

**Claim provenance:**
- Every `type` claim is a literal: access/refresh (auth jwt.ts:200/226, shared token-rotation), connector (jwt.ts:294).
- No user-controlled spread follows the claim, so no user flow can obtain `type: 'connector'`.
- Stripping the claim needs a re-signature, and cell G proves a bad signature takes the old path.

**Header scheme:**
- `bearer` and `BEARER` are not treated as a Bearer. Required mounts answer 401 and optional mounts are anonymous with 0 forwards.
- `Bearer␠␠<jwt>` on an optional mount IS forwarded upstream (200, header intact). Every in-repo upstream parses with the same `split(' ')[1]` (shared middleware/index.ts:110/117, originate auth.ts:94, auth authenticate.ts:99/140), so the token is empty and never accepted. Control: a human token gives the same forwarding.
- Cookies and query strings are never read (0 forwards). There is no websocket or SSE code in the gateway.

**401 body and log:**
- The body names only x-api-key.
- The log has no token. I checked with a full-token substring search and a planted tamper.
- CRLF in the path stays percent-encoded, and a newline in the userId/tenantId claims is JSON-escaped on the emitted line (measured).

## Defects
1. **Minor: the log `path` is mount-relative.** At auth.ts:411 `req.path` drops the router mount prefix. Measured: `GET /api/credentials/abc` logs `"path":"/abc"`. Cell C mounts at the root, so it cannot see this. Fix with `req.baseUrl + req.path`, not `originalUrl`, which carries the query string.
2. **Minor (scope of the claim, pre-existing, not a regression): the refusal lives only in `authenticateToken`.**
   - Gateway mounts without it forward a connector Bearer verbatim (each measured with 1 forward carrying the Bearer):
     - `/api/v2/verification` (originate `authenticate({required:false})` accepts it as a connector principal)
     - `/api/verification`
     - `/api/presentations/verify`
     - `/api/documents/:id/sig-json`
     - `/api/auth/*`
     - `/api/sessions`
   - The gateway-internal `/originate/` (proxy.ts:1201) forwards `POST /originate/api/documents` to originate `POST /api/documents`, which is the original defect's endpoint (measured 200, 1 forward).
   - Edge mitigation: nginx closes `/originate/` with a 404 in all three confs (KS-1041), and the api-gateway has no published ports in `docker-compose.production.yml`.
   - These are reads, or intra-cluster only. The PR text should say "on every `authenticateToken` mount", not "the gateway".

## Notes and limits
- The gateway Bearer path still accepts `type: 'refresh'` tokens as principals. The PR uses a denylist, not an `access`-only allowlist. This is pre-existing and out of scope; a ticket candidate.
- Spec: bearer ops already document 401 through `commonErrorResponses[401]`. A sample check (vc-issuer `/api/credentials/{id}`) found no change needed. I did not walk every optional op.
- Not checked: Platform S code (outside the repo), live/deployed stacks, and the seat's RECOMMENDATION mail (none saved in `5_Project_History/2026-10-12_seatK-4th/`).

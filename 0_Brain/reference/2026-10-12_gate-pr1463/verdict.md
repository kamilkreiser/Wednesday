# Gate verdict: PR #1463 (KS-1205): GO WITH NOTE

- **Head:** `c3d5376ac208b796d47ca13fb6fccd473392caa8`, tree `bec914ca923b` (matches the brief).
- **Base:** `a31b77577`. The commits are `eaab223ea` (tests, red), then `c3d5376ac` (the fix).
- **Gate:** independent Opus QA gate, 2026-10-12. Read-only. All runs were made in my own `--no-hardlinks` clone in the session scratchpad.

**Fetch limit.** The repo is private, and my clone has no HTTPS credentials, so `refs/pull/1463/head` could not be fetched. The head sha and tree came from the seat's clone. I could not confirm against GitHub that the PR head is still this sha.

## 1. The diff (exactly as described)

| commit | file | + | − |
|---|---|---|---|
| eaab223ea | `api-gateway/src/__tests__/ks1205-limiter-follow-ups.test.ts` (new) | 278 | 0 |
| c3d5376ac | `api-gateway/src/__tests__/rateLimitEnforce.test.ts` (one expectation: `ratelimit:ks170-redis` → `ratelimit:jwt:no-tenant:ks170-redis`) | 3 | 1 |
| c3d5376ac | `api-gateway/src/middleware/auth.ts` | 17 | 5 |
| c3d5376ac | `api-gateway/src/middleware/rateLimitEnforce.ts` | 103 | 65 |

- In total, 4 files changed, +401 / −71.
- Nothing outside `services/api-gateway` changed. The audit middleware, which is where F-5 lives, is not in the diff.
- There is one unclaimed micro-change; see Note N1.

## 2. Red and green cells (my runs)

| tree | result |
|---|---|
| `eaab223ea`, new file + `rateLimitEnforce.test.ts` | 26 tests, **6 failed**: N-2a, N-2b, FALLBACK, G-JWTCATCH+F-4, F-4, R-2 |
| `c3d5376ac`, same files | 26 tests, 26 passed |

- The F-4 cell failed with "expected 1 time, got **3** times", so the seat's claim of three dispatches (not two) is **confirmed**.
- The N-2a and N-2b cells failed because the JWT was counted under `ratelimit:api_key:<victim hex>`. The claim that a forged claim was counted under the victim key's real Redis key is **confirmed**.

**Planted-red at head.** I wrote my own tampers. Each one asserts that its anchor occurs exactly once, and the tree was restored clean after every run.

| tamper | cells that turned red |
|---|---|
| the limiter reads the `rateLimitBucket` claim first | N-2a |
| no `jwt:` namespace | N-2a, N-2b, FALLBACK, ks170 |
| no tenant in the fallback bucket | FALLBACK, ks170 |
| `recordApiKeyBucket` removed | control, RAW-2, plus ks1195(b) on the full suite (3) |
| `next()` back inside the `try` | F-4, JWTCATCH |
| no `.catch(next)` | JWTCATCH |
| the ticket's await-inside-the-try tamper | JWTCATCH |
| no warn throttle | R-2 |
| `oauth` added to the machine set | G-OAUTH |
| an unknown key given a principal | G-UNKOPT |
| the raw key as the bucket | 3 on the full suite |
| the bare `sha256` as the bucket | RAW-2 |

Every tamper turned its stated cells red. The seat's figures of 3 for the raw-key and key-record tampers match my runs over the full suite.

## 3. Suites (my runs)

| tree | gateway suite (files / tests, failed) | `tsc` (default config) | `tsc` with tests included | eslint | `packages/shared` |
|---|---|---|---|---|---|
| base `a31b77577` | 97 / 876, 0 | rc 0 | 30 errors | 0 errors / 36 warnings | — |
| head `c3d5376ac` | 98 / 889, 0 | rc 0 | 30 errors, same set, 0 in the new file | 0 / 36 | same subtree |
| develop `672352369` (#1459, tree `1ac55993e789`) | 99 / 895, 0 | — | — | — | — |
| merge prediction (`merge-tree` clean, tree `5cead61b`) | 100 / 908 = 895 + 13, 0 | rc 0 | 30 errors, same set | 0 / 36 | 48 / 945, rc 0 |

- **The `tsc` result has a gap.** The default config excludes `src/__tests__`, so the seat's "tsc rc 0" does not type-check the new test file. With tests included, there are 30 errors on base, head and merge alike, and none of them is in the new test file.
- **Zero controls:**
  - A planted type error gives `tsc` rc 2.
  - The merged-tree delta over develop is exactly the PR's 4 files.
  - `packages/shared` has an empty diff from base through head to merge.
- **The merge against the later tip `ba697cf3d`** (KS-1334, originate only) is also clean, at tree `18936206`. I did not run the suites on it.

## 4. Semantics

**Rate-limit keys.**

| caller | bucket at head | can a caller choose another principal's bucket? |
|---|---|---|
| API key | `api_key:` + domained `sha256(key)`, unchanged byte-for-byte | No. The bucket is recorded in a WeakMap keyed by the request, and only the API-key branch writes it (`auth.ts:333`). Nothing in a token can reach it. |
| JWT or test-token machine principal | `jwt:<tenant>:<connectorId or userId>` | Not through headers. `tenantId` comes from the verified token; the `x-tenant-override` header changes only RLS and `x-tenant-id`, not the bucket. A token can never reach the `api_key:` namespace. |
| anonymous, or an interactive method | not limited here (no change) | — |

- Paths and #1459's case-folding play no part. The limiter reads no path.
- Header-name case is irrelevant, because Node lowercases header names.
- The only real machine producer is `auth.ts:317`. Nothing produces `oauth_app`, and nothing else sets `rateLimitBucket`.

**Redis down.** Behaviour is unchanged: when Redis is not ready, or a command throws, the limiter falls back to counting in memory. If that fallback also fails, the request is allowed and logged at error level (fail-open, KS-616's choice). The limiter no longer mislabels a downstream throw as `redis-command-failed`.

**The `next()` fix.**
- The limiter now decides inside the `try` and acts after it, so each request is counted once and `next()` is called once.
- A downstream throw now propagates out of the limiter.
- In auth, `.catch(next)` turns the old unhandled rejection into `next(err)`.
- Under Express 4, `Layer.handle_request` catches downstream throws, so in production that `.catch` fires only when the limiter itself throws. That is an improvement on an unhandled rejection that ends in exit.
- No double response: a request refused with 429 never calls `next()`. If writing the 429 itself throws, the request is still allowed, the same end result as the old code.

**Redis key rename.**
- No code, dashboard, spec or script reads `ratelimit:<id>` from Redis. The repo-wide grep found only this limiter, and `packages/shared`'s `createRateLimiter` keeps an in-memory Map that does not touch Redis.
- The old keys expire by their window TTL, so nothing is left behind and no migration is needed.

**F-5** is untouched.

## 5. Spec and docs

No change is needed:
- The 429 body and headers are unchanged.
- The `secuura-api.yaml` "bucket" text describes the security service's own limiter, which uses the `security:ratelimit:` prefix.
- `WORKFLOWS.md` describes only the 429 shape.

## Defects

1. **Minor:** `rateLimitEnforce.ts:155`. The R-2 throttle is keyed by `connectorId || userId`, without the tenant and without the bucket. Two tenants' principals that share a connectorId share one 30-second warning slot, so one tenant's warning can hide the other's. It affects logs only, and no real producer reaches it. Keying the throttle on `clientId` would fix it.
2. **Minor (record):** `rateLimitEnforce.ts:92`. `jwt:${tenantId}:${id}` uses a delimiter that either claim may contain, so tenant `a:b` with id `x` gives the same bucket as tenant `a` with id `b:x`. Reaching it needs the RS256 signing key, and it stays inside the `jwt:` namespace.

## Notes

- **N1:** The 429 sent on the Redis path now caps the hint's "Try again in Ns" at 1 second or more, through the shared `sendRateLimited` (`:109`, `:121`). The old Redis-path hint (base `:175`) used the raw value. This is harmless, but it is not described in the PR.
- **N2: transition window.** During a rolling deploy, old and new pods count machine-JWT principals under different keys. That allows up to twice the allowance for the rollout plus one window. API-key buckets do not change.
- **N3:** The PR's "tsc rc 0" covers no test files (see §3).

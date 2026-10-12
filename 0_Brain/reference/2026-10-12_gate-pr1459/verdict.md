# QA gate — PR #1459 (KS-801) — head `11028c7f6b1455138ad20b9848e32a21f11297dc`

**Verdict: GO WITH NOTE.** No Major defects. Opus independent gate, 2026-10-12, read-only.

Clone: `git clone --no-hardlinks` of the local repo into the session scratchpad, then `refs/pull/1459/head` and `develop` fetched from GitHub. The head SHA matched `ls-remote` (`refs/pull/1459/head` = branch head = `11028c7f6`). Base = merge-base `65d7722f8`. develop is now `a31b77577`, two commits ahead, and they touch only `services/auth`. `merge-tree` against develop is clean. I found no seat worktree on the KS-801 branch under `worktrees/`. All runs below are mine, on a clean `npm ci` (gateway, shared and root workspace).

## 1. Diff is exactly the described change
Seven files, all under `services/api-gateway/src`, +316 / −35. No file outside the gateway changed, and no `package*.json`, spec or lockfile changed.

| file | + | − |
|---|---|---|
| middleware/pathFold.ts (new) | 25 | 0 |
| middleware/contentType.ts | 15 | 11 |
| middleware/csrf.ts | 5 | 2 |
| index.ts (shouldParseBody) | 2 | 1 |
| __tests__/contentType.test.ts (3 PERIMETER cells 200→415) | 15 | 21 |
| __tests__/ks801-case-variants-get-the-same-guard.test.ts | 214 | 0 |
| __tests__/ks801-path-fold.test.ts | 40 | 0 |

The five fold sites are `contentType.ts:122` (prefix, which also feeds `:135` FORM and `:139` OCTET), `csrf.ts:312` and `index.ts:396`. The red commit `bdbf0aa2c` adds only the tests and an identity stub. Red→green changes no assertion apart from the three cells the ticket said to flip (200→415). The other test edit is a lint-only `let code` change.

## 2. Red on base, green on head, and planted reds (my runs)
- **Base `65d7722f8` with the head tests and the identity stub:** 61 tests, **16 red**. These are all 8 guard rows, the 2 CSRF exclusion rows, the 3 PERIMETER cells and fold A/B/C. All 5 controls stayed green, including the anchors:write pin and its admitted control.
- **Head:** the same 71 tests in the focused set, 0 red.
- **Planted reds on head, one site reverted at a time:**

| site reverted | tests that went red |
|---|---|
| P1 prefix | 8 (5 guard rows + 3 PERIMETER) |
| P2 FORM | 1 (`/api/oauth/token`) |
| P3 OCTET | 2 (both verify-file rows) |
| P4 CSRF | 2 (both exclusion rows) |
| P5 shouldParseBody | 2 (both verify-file rows) |

  Every site has a red. P5 is caught only indirectly, through the verify-file rows.

## 3. Suites (head)
- **Gateway:** 99 files, 895 / 895 passing, 0 skipped. Base: 97 files, 876 / 876. The difference is the 2 new files and 19 new tests.
- **packages/shared:** 48 files, 945 / 945. Control only; the PR does not touch it.
- **tsc --noEmit (gateway):** 0 errors on head and on base.
- **eslint:** 0 errors and 36 warnings on head, versus 0 and 36 on base. The warning sets are identical.
- **check:openapi:** the spec is in sync, and all 406 example blocks resolve.

## 4. Security reasoning

**The seat's experiment reproduces on Express 4.22.3 (path-to-regexp 0.1.13).** Machine caller with `documents:read` only, `POST` to each spelling:

| setting | result |
|---|---|
| Insensitive (today) | every spelling 403, 0 hits |
| `app.set('case sensitive routing', true)` alone | every spelling 403, 0 hits. No change, because the routes live in `Router()`s that keep their own insensitive default. |
| `app.set` plus `Router({caseSensitive:true})` at all 12 sites | `/api/anchors/BATCH` → **200, 1 upstream hit**. `/Api/anchors/Batch` and `/api/ANCHORS` → 404. |

So the claim holds, and the fold is the right choice. The root cause is `proxy.ts:858` (scope-gated) next to the unscoped catch-all at `:865`.

**Path-shape probe.** I sent a 35-row guard matrix and a 16-row CSRF matrix to the real app over raw sockets, on head and on base (`evidence/`). Every head/base difference is a case variant moving to the canonical outcome:
- Base proxied `/API/OAUTH/APPS` (text/plain) upstream, rewritten to a JSON `{}`. Head refuses it with 415.
- Base re-serialised a form POST to `/API/OAUTH/TOKEN` as JSON. Head forwards the raw form body.
- Base enforced CSRF on `/API/AUTH/LOGIN` and `/API/…/VERIFY`. Head excludes them, matching the canonical paths.

Shapes the fold does not open:
- **Percent-encoding** (`/%61pi`, `/api/%6Fauth`, `%2F`): Express does not decode either, so the result is 404 or 415 with 0 hits.
- **Double slashes:** normalised first (`index.ts:236`), so `//API//oauth//apps` → 415.
- **`;x`, `?x`, `/./`, `/x/../`, backslash:** 415, 404 or 400, all with 0 hits.
- **`/API/V1/…`:** now 415 where base gave 404. Harmless.
- **Raw non-ASCII** (Kelvin sign): Node's parser rejects it with 400 before any middleware runs.

**Does the fold agree with routing?** Yes:
- Express's route regexes use the non-unicode `i` flag. Under that flag the only ASCII case pairs are A-Z and a-z, and no non-ASCII character maps to ASCII. The fold does exactly the same.
- No `Router` in the gateway, and no Express app in any other service, sets `caseSensitive` or `case sensitive routing`.
- Every predicate reads `req.path` at app level, before the v1 rewrite, so `req.path` equals the `originalUrl` path.

## 5. Other services
No file outside the gateway changed. On canonical paths the upstream sees the same content type and body length on head as on base.

## 6. Published spec
No change needed. No route, schema or status code changes for any canonical path, and `check:openapi` passes.

## Defects / notes
1. **Minor (follow-up ticket, not this PR's scope).** Other gateway path checks that are still case-sensitive. The PR does not touch them, and no part of it claims to fix every path predicate:
   - `middleware/security.ts:150` — bruteForceProtection matches `includes('/auth/login')`, so `/API/AUTH/LOGIN` skips the Redis lockout. This is from reading the code; I did not measure it. The path-scoped limiter at `index.ts:927` still applies.
   - `middleware/audit.ts:210-212` — a mutation to a case-variant path writes no audit row.
   - `index.ts:1027` — the spec method/auth gate.
   - `index.ts:520` and `:544` — the version parse and the v1 rewrite.
   - `routes/versioning.ts:48`.
2. **Minor (pre-existing; the fold extends it to case variants equally).**
   - The CSRF exclusions are prefix matches with no segment boundary: `/api/auth/loginx` and `/api/verification/verifyX` are excluded from CSRF (measured on base and head).
   - The exact-match allow-sets refuse a trailing slash (`/api/oauth/token/` → 415) and the `/api/v1/` alias. Both fail closed.
3. **Nit.** `__tests__/ks801-path-fold.test.ts:20` says percent escapes are untouched, but the fold lowercases hex digits (`%4A`→`%4a`). It is harmless, because no allow-set or exclusion entry contains `%`.
4. **Nit.** The comment at `index.ts:396` runs the KS-1234 and KS-801 remarks together on one very long line.

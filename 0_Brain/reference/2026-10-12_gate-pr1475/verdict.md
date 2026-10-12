# QA gate: Secuura Platform K PR #1475 (KS-1464 limiter key hygiene)

**Verdict: GO WITH NOTE** for head `f436fdef49e74786f8b050685bf3943a70fc5338` (base f9c7880f9; develop now 524db0ce6; merge predicted clean).

Read-only. Own clone in scratchpad, fetched `pull/1475/head` (the head was NOT in the shared repo). Evidence in `evidence/`.

## Checks, by my runs
1. Diff: 2 files only. Product file `services/api-gateway/src/middleware/rateLimitEnforce.ts` (+20/-11) and the new test file (161 lines). 7e460d6b4 is tests-only (product file identical to base). Matches the description.
2. Red/green: the 12-cell file with the product file at base: 5 failed (B1, B2, T1, T3, T4), 7 passed. At head: 12/12. I ran 8 tampers on head (no `%` escape; order swapped; no `:` escape; encodeURIComponent; throttle on connector id; tenant dropped from line; throttle on jwtBucket instead of the recorded bucket; tenant unescaped) and each reddened at least one cell (1 to 3 each, `tamper.py`).
3. Suites: gateway 105 files / 979 tests, shared 49 / 949, `tsc --noEmit` rc 0, eslint rc 0, on both head and the predicted merge (0961bdcde; develop's changes since base are in originate only, so there is no overlap). Control: my first run, with shared not built, showed 70 failed files and tsc errors, so the harness does detect failures.
4. Escaping: 40,169 pairs (random strings over `:`, `%`, `%3A`, `%25`, `%253A`, empty, é, 日, emoji, lone surrogates, newline, plus a 13x13 grid) gave 33,601 distinct keys and 0 collisions. Control: the old scheme collides on 17 of the same pairs. 4,318 ordinary pairs are byte-identical to the old key. Every key has exactly 4 colon fields. Non-string claims (number, array, object) and lone surrogates do not throw.
   - Only readers of the key are the limiter itself (rateLimitEnforce.ts:206) and its own tests. The shared createRateLimiter uses its own in-memory store (no Redis collision). Grep found no dashboard or SCAN consumers. Redis keys are binary-safe, so there is no charset limit; length is bounded by the JWT size.
   - The warning line carries connector/user id, authMethod and tenant id. It never carries the bucket hash or any secret.
5. Behaviour (b) is real (T4): one line per API key per 30 s for a connector with no allowance. The map is swept every 5 min (lines 312-313), so it is bounded. Acceptable. Behaviour (c) is real (B2/B4), but see Minor 3.

## Defects
Major: none.

Minor
1. rateLimitEnforce.ts:~91-93 (escapePart): "injective" holds on JS strings but not on the Redis wire. ioredis sends UTF-8, so claims differing only by a lone surrogate (\uD800 vs \uDC00 vs U+FFFD) hit one key (checked with Buffer.from). Needs a signing-authority claim and was true before; the comment overstates it. Not blocking.
2. rateLimitEnforce.ts:113 and :171: principal and tenant come from signed claims or DB values and go unescaped into the warning line. CR/LF in a tenant can forge a log line. The principal part is old; tenant is new. Low.
3. Claim (c) is wider than stated: any machine-JWT id or tenant containing `%` (not only `:`) gets a different key too (`%` becomes `%25`). Same brief rolling-deploy double allowance. Acceptable; include in the deploy note.
4. Left on purpose and confirmed: a tenant literally named `no-tenant` collides with an absent tenant; empty and absent ids both map to `unknown`. Cell T2 is vacuous on base (the PR says so).

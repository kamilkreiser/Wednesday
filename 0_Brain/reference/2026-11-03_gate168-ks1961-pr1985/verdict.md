GO WITH NOTES — HOLD-FOR-KAM (malformed rateLimit / rateLimitWindow values get a HIGHER effective ceiling at head than at base: 9 rateLimit inputs and 5 window inputs measured, only some of them disclosed)
# QA Gate 168 (Tier 1, round 1): PR 1985 / KS-1961 the gateway login guard and client limiter refuse (503) when they cannot run

## Subject
- Repo Secuura/Distributed_Secuura. PR 1985, head `1e8c43fcaf6c9c6d42946b43c89e419f9d1f3f18`, one commit whose parent is `27fe5476526c4200b752449e04be689724289e6d`.
- Pin at START (ls-remote, 03:50:09Z): head = 1e8c43fc, develop = 27fe5476.
- Pin at END (ls-remote, 04:10:57Z): head = 1e8c43fc (unchanged). **develop MOVED to `67309f28ab2132ca7b6a45b28c731aa480642a9a`** (one commit, "Refs KS-1572: referral apply…", 4 files under services/referral and the docs fragments; no api-gateway file).
- merge-tree --write-tree (in my clone): onto 27fe5476 rc=0, tree `cf1d157a6ab2…` (= the head tree). Onto the CURRENT develop 67309f28 rc=0, tree `6b29dfa67ecd…`. My suites ran on the head tree, not on the merged tree. That is acceptable because develop's new commit touches no api-gateway file.
- Diff: 11 files, +831/-114 (security.ts, rateLimitEnforce.ts, 7 test files, 2 doc fragments). services/redis.ts is not in the diff.
- Host: macOS (Darwin 27), Node v26.8.1, TypeScript 5.9.3, vitest 4.1.12, tsx (cjs require hook), express 4 from the lockfile. NOT run: Linux/CI, the Docker image, a real Redis, the production NODE_ENV logger transports.
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate168-ks1961-pr1985/`, 372 MB total. 355 MB of that is the `--shared` clone checkout. node_modules are symlinks into gate 148's install: the lockfile and packages/shared are byte-identical between gate 148's base 4d1ab2cb and develop 27fe5476 (`git diff --stat` empty), so nothing was installed.

## Method
- I drove the REAL `createBruteForceProtection` and `enforceClientRateLimit`, the real `services/redis.ts` and the real winston logger over real HTTP: express 4 on 127.0.0.1, with the limiter mounted exactly as auth.ts does it (`clientRateLimit(req,res,next).catch(next)`).
- Only `ioredis` was replaced, by a Map-backed stand-in that honours TTLs the way Redis does:
  - PEXPIRE ≤ 0 deletes the key;
  - a non-integer or out-of-range PEXPIRE rejects with Redis's "ERR value is not an integer or out of range";
  - any command can reject with, or hang on, the cell's value.
- Base = develop's two middleware files, resolved in place of head's from the same directory, so they get the same real imports.
- One process per cell, base and head (`scripts/probe.ts`, `scripts/matrix.sh`). 202 rows in `logs/probe.jsonl`, all rc=0, paired in `logs/probe_table.txt`. Six timed cells (two bursts 62 s apart) are in `logs/probe_time.jsonl`.
- Downstream calls are counted by the handler itself. Every zero has a no-fault control in the same run that reached downstream (bf_fault none, bf_record clean/nullStr/proto, rl_hdr none, rl_success).
- Whole api-gateway suite run twice at head and twice at base.
- Red-first: base product with head's 7 changed tests.
- tsc (service + tests) and the KS-1090 typecheck ratchet at base and head. eslint on the PR files, with a planted-lint control.
- 25 mutants on head (23 product + 2 Q6 test-fake reverts), each against the 7 changed test files, each restored by sha256.
- Two discarded runs are kept for the record:
  - `logs/sparse_run_discarded/`: a sparse checkout lacked files other tests read.
  - `logs/discarded_esm_loader_run/`: the ESM loader bypassed the ioredis stub, so Redis was never "connected" and every bf cell was invalid.
  - Neither run is used below.

## Findings

### G168-F1 — MEDIUM (HOLD-FOR-KAM condition): malformed allowance/window values get a higher effective ceiling at head than base
- **FOUND:** Head maps every malformed value to exactly the platform default, 100 per 60 s. Where base's accidental reading of the value was STRICTER than that, head is more permissive.

  **rateLimit**, burst of 105 requests, window 60. Requests allowed, base → head:

  | rateLimit value | base | head | disclosed in the PR? |
  |---|---|---|---|
  | `-1` | 0 | 100 | yes |
  | `0.5` | 0 | 100 | yes |
  | `-Infinity` | 0 | 100 | negative-number class |
  | `1.5` | 1 | 100 | no (the PR's own test L-R4 asserts it) |
  | `99.5` | 99 | 100 | no |
  | `'5'` | 5 | 100 | no |
  | `'99'` | 99 | 100 | no |
  | `true` | 1 | 100 | no (asserted by L-R4) |
  | `[5]` | 5 | 100 | no |

  **rateLimitWindow**, rateLimit 3: a burst of 4, a 62 s wait, then another burst of 4. Requests allowed over the whole run, base → head. Base's own 429 hint reports the effective window: 120 s, 121 s, Infinity, NaN, 1e+300.

  | window value | base | head |
  |---|---|---|
  | `'120'` | 3 | 6 |
  | `120.5` | 3 | 6 |
  | `Infinity` | 3 | 6 |
  | `{}` | 3 | 6 |
  | `1e300` | 3 | 6 |

  Base never reset these windows, or reset them after more than 60 s. Head resets at 60 s.

  - Control: window `60` gives 3 then 3 at both base and head.
  - Window values shorter than 60 s at base (`1.5`, `0.5`, `'1\n'`, `'30'`) are TIGHTER at head (60 s).

- **TESTED:** 25 rateLimit values × base/head, 17 window values × base/head on the Redis path and on the KS-617 not-connected memory path (identical outcomes), and the 6 timed cells.
- **HOW:** `rl_value`, `rl_window`, `rl_window_mem` and `rl_time` rows. The count is the handler's own counter. The window is the real code's own 429 hint ("limited to N requests per Xs").
- Q3 answered plainly:
  - Yes, rateLimit -1 and every fraction below 1 went from "refused every request" (0/105) to 100 per 60 s. So did -Infinity.
  - The loosening is WIDER than disclosed: numeric strings below 100, fractions between 1 and 100, `true`, `[n]`, and window values longer than 60 s or never-resetting.
  - **No input gets MORE than the platform default at head.** Every malformed value lands at exactly 100/60 s. The only values above it are clean configured integers (`101` gives 101, `1e15` gives ≥105/105), and those behave identically at base.
- Not measured: whether any real record carries such a value. The security service column is `INTEGER` (startup-migrations.ts:446) and auth.ts:317 applies `|| 100`. Listed under NOT tested.

### G168-F2 — POSITIVE: both fail-opens closed; every store/limit failure refuses with 0 downstream calls (Q1)
- **FOUND, guard:** 20 failure cells, every one 503 `SERVICE_UNAVAILABLE` with downstream = 0 at head:
  - 7 store errors: Error, Error carrying the planted text, string, revoked Proxy, throwing getter, plain object, and a hang;
  - 9 bad stored records: corrupt JSON, `5`, `[]`, `{"blockedUntil":"soon"}`, `{"attempts":"x"}`, blocked-without-attempts, numeric-string blockedUntil, `blockedUntil:null`, `"x"`;
  - 4 errors under a planted lockout.

  At base, the same 20 cells:
  - 16 reached downstream;
  - 2 hung with no answer for 4 s (the hang cells);
  - 2 answered 429 (blocked-without-attempts and numeric-string blockedUntil). These are now 503, an availability change only.

  The hang is refused at 2004 ms and 2010 ms; the deadline holds.
- **FOUND, limiter:**
  - Header-write throws (6 thrown values × 6 requests): head reached downstream 0 of 36 times, base 36 of 36.
  - The 429 write throws: head 2/6 (the two under the limit), base 6/6.
  - A response already committed upstream: head 0 downstream calls, base 6.
  - The KS-616 fallback itself throws: head's first request is 503, where base let it through uncounted (3/6 allowed with limit 2).
- **TESTED / HOW:** `bf_fault`, `bf_record`, `bf_lockout`, `rl_hdr`, `rl_429write`, `rl_committed`, `rl_fallback` rows. Controls in the same run: bf_fault none (401, downstream 1) and rl_hdr none (2/6).

### G168-F3 — LOW: the guard's own 429 write is outside every try; if it throws, head leaves the login hanging with an unhandled rejection
- **FOUND:** With a lockout planted and `res.setHeader('Retry-After')` throwing:
  - Base caught the throw and called next(): the login reached downstream (401) through a live lockout, i.e. fail-open.
  - Head answers nothing within 4 s and raises one unhandled rejection. Downstream = 0.
- This is not more permissive than base. But unlike the limiter, the guard has no refusal for a failed write. The rejection's reason carries the thrown message: the planted text was in the reason. Under production's shared unhandledRejection handler that message would be logged. That logging was NOT driven here.
- Reachability is low: setHeader throws only once headers are sent, and the guard runs early in index.ts.
- **TESTED / HOW:** cell `bf_429throw`.

### G168-F4 — LOW, PRE-EXISTING: the unchanged KS-616 degrade line still logs the thrown text
- **FOUND:** A Redis count error carrying the planted text is logged by `logDegraded` (`"error":"redis said <planted>"`), once at base and once at head. Head is unchanged here, as ruled ("KS-616 degrade UNCHANGED").
- So "head logs types only" is true at the sites this PR changed, not across the whole limiter.
- **TESTED / HOW:** `rl_degrade secretString`; planted value `G168PLANT-…`, counted in all captured stdout/stderr.

### G168-F5 — LOW: two mutant survivors
- **M6** (the shape check accepts arrays): EQUIVALENT for JSON-sourced records. An array has no finite `attempts`, so the record is still refused.
- **M9** (the guard does not `res.end()` when headers were already sent): NOT equivalent. Nothing tests the guard's committed-response branch. The limiter's equivalent branch (M15) is killed.
- **TESTED / HOW:** see Q8.

### G168-F6 — INFO: develop moved during the gate
- See Subject: develop is now 67309f28, the merge is clean (tree 6b29dfa6), and api-gateway is untouched.

## What passed (measured)
- **Q1:** see F2. 20/20 guard refusals and every limiter refusal cell had 0 downstream calls. Planted-lockout controls: no fault gives 429 at both base and head.
- **Q2:** At head, no malformed value leaves a caller unlimited.
  - Base was unlimited (105/105) for `'1\n'`, `Infinity`, `'1e3'`, `{}` and `2^53` (rateLimit), and for windows `-1` and `-60` (8/8, on both the Redis and memory paths).
  - Head gives each of these 100/60 s, or 3 per 60 s in the window cells.
  - The only unlimited-looking head row is the clean configured `1e15`, the same as base.
- **Q3:** see F1. Nothing exceeds 100/60 s except clean configured integers, which are unchanged.
- **Q4:** No extra state is written on a 503.
  - Guard: store writes (setex/del) = 0 on every 503 cell, the same as the 429 cell (0). The record is unchanged, and the recordFailure helper is not attached.
  - Limiter: the Redis counter reads 6 after 6 requests at base and head alike (the same increment a 429 makes). Nothing else is written.
- **Q5:** Outcomes are identical at base and head for:
  - success (2/6, headers `2`, hint 60 s);
  - 429 bodies;
  - KS-616 degrade with Error / string / revoked Proxy (2/6 each);
  - KS-617 not connected (2/6);
  - the clean rateLimits 1, 3, 100, 101 and empty / null / missing / NaN / 0;
  - the clean windows 1, 60, 3600 and missing / NaN / 0;
  - the planted lockout under the real key `secuura:gateway:bf:127.0.0.1` with no fault: 429 (retryAfter 600).

  With a Redis error under that lockout: head 503, base 401.
- **Q6:** The no-op `setHeader` hides nothing those tests assert. No test in either file reads rate-limit headers, and a 429 would still be visible through `status()`/`json()`.
  - Reverting the setHeader addition at head fails 1 test (auth.test.ts) and 2 tests (ks480), by assertion: the limiter now refuses.
  - The develop versions of those files (no setHeader) pass at base 19/19 and 5/5. So at base they passed only because the limiter's TypeError fell into the old fail-open. The change exposes that dependency rather than hiding one.
- **Q7:** planted value `G168PLANT-…`.
  - 11 cells at the changed sites carried it. Base logged it in 9 of them: bf store Error, bf string, bf lockout+Error, bf 429-write, rl header-write Error (6 lines), rl header-write string (6 lines), rl 429-write (4 lines), rl fallback Error, rl fallback string. The 2 it missed were the plain-object values: base printed `[object Object]`.
  - Head: 0 in every changed-site cell.
  - Positive control in the same run: rl_degrade logs it at both base and head (F4).
  - Head lines carry `{"thrownType":"Error" | "LockoutReadTimeout" | "MalformedLockoutRecord"}` and `step`.
- **Q8, suites:**
  - Head 1547/1547 twice (149 files). Base 1506/1506 twice (147 files). Ratio: +41 tests, +2 files, 0 failures either side. This matches the author's second runs; the author's first runs, with failures, were not reproduced.
- **Q8, red-first** (base product + head tests), 41 red by assertion:
  - ks1961 guard: 12/16 red;
  - ks1961 limiter: 17/25 red;
  - ks1868 brute-force: 6/8 red;
  - ks1868 limiter: 5/10 red;
  - security.test.ts: 1/15 red.

  Green at base, so proving nothing about the fix: auth.test.ts 19/19 and ks480 5/5 (they only gained the fake), plus 21 control cells.
- **Q8, static:**
  - Service tsc: 0 errors at base and head.
  - Test tsc: 25 errors at both, the per-file set identical.
  - Ratchet at head: "25 errors: 25 in the baseline, 0 new".
  - eslint on the 9 PR source/test files: rc 0. Planted control: 2 problems, rc 1.
- **Q8, mutants (raw table counted):**
  - Unmutated control: 98/98.
  - 23 product mutants: 21 KILLED, all by assertion; 2 SURVIVED (M6 equivalent, M9 not equivalent).
  - 2 Q6 rows: both KILLED.
  - All 25 restored by sha256 (`logs/mutants.out`). Headline = table.

## NOT tested
- Whether any production connector record, security-service answer or machine JWT can actually carry a non-integer, string, negative or boolean rateLimit/rateLimitWindow. That is, the real-world reach of F1. Read only: column INTEGER, auth.ts `|| 100`.
- A real Redis server (the stand-in follows Redis's documented PEXPIRE/PTTL rules), multi-replica behaviour, the Docker image, Linux.
- Production NODE_ENV logging (File transports, json format) and the shared unhandledRejection handler's output for F3.
- The full gateway `index.ts` app; the middleware was mounted in a minimal express app.
- Mutants against the whole suite (each ran only against the 7 changed test files).
- The suites on the merged tree with develop 67309f28.
- G148-F3 still stands: nothing in production calls `recordFailure`, so the gateway guard's lockout is not armed by production code. Not re-measured.

## Plain answer for Kam
- With this change, when the gateway cannot check a login's failed-attempt record or apply a connector's rate limit, it now says "try again" (503) instead of letting the request through. I checked that across every kind of fault I could produce, and none got through.
- Normal logins, normal limits, lockouts and the existing Redis-wobble fallback behave exactly as before.
- Error logs no longer copy the error's text, which could hold secrets, at the places changed. One older log line outside this change still does.
- The one thing for you to rule on: if a connector's limit setting is garbage (for example "5" stored as text, 1.5, -1, or a window of "120" seconds), it now gets the standard 100 requests per minute. Before, by accident, some of those garbage values gave a stricter limit or blocked the connector completely.
- No value now gets more than the standard 100 per minute. Whether garbage values can occur at all in real data was not measured; the database stores whole numbers.

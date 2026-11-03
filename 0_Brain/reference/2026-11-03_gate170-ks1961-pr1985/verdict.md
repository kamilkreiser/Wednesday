GO WITH NOTES — HOLD-FOR-KAM (same-input F1 is clean: in 0 of 130 cells is head more permissive than develop. But in 4 of 8 mixed-bucket cells head lets MORE through: two callers share one bucket, one with a clean limit 100 and one with a malformed value. There head allows 100 where develop allows 50-52, because the malformed requests no longer use up the shared counter. Head never goes above the clean caller's own configured 100.)
# QA Gate 170 (Tier 1, round 2): PR 1985 / KS-1961 the gateway login guard and client limiter refuse (503) when they cannot run (DELTA on G168-F1/F3/F4/F5)

## Subject
- Repo Secuura/Distributed_Secuura, PR 1985, branch `fix/ks-1961-gateway-fail-closed`.
- Pin at START (ls-remote from the read-only checkout, 04:47:24Z): head = `a0a91f65d0006d1adc69325002e6ddf69abffc2b`, develop = `ca2b2aa350ac557fc70dfc5d70f15dc9a78ea5b8`.
- Pin at END (ls-remote, 05:04:26Z): head = `a0a91f65d000…` and develop = `ca2b2aa350ac…`, both unchanged.
- History: round 1 is `1e8c43fcaf6c`. Then `4d8d91a1d` merges develop `67309f28ab21` into the branch. Round 2 is `a0a91f65`.
- `git merge-tree --write-tree ca2b2aa a0a91f65` (in my clone): rc=0, tree `b0cfe6fdf4d5…`.
  - The merged tree's `Blockchain/Dev/services/api-gateway` subtree is `bb560c3d8887…`, identical to the head's. So the api-gateway suites I ran on the head tree are the merged tree's api-gateway.
- PR 1986 (`67309f28..ca2b2aa`, KS-1962) touches 5 files: anchoring `threadTokenIndex.ts`, two anchoring tests, and two KS-1962 doc fragments. That is **0 files in common** with this PR's 11 (checked with `comm`).
- Host: macOS (Darwin 27), Node v26.8.1, TypeScript 5.9.3, vitest 4.1.12, tsx (cjs require hook), express 4 from the lockfile.
- NOT run on: Linux or CI, the Docker image, a real Redis, Node 24, production NODE_ENV logger transports.
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate170-ks1961-pr1985/`, 371 MB.
  - The clone was made with `clone --shared`, then a fetch of `refs/pull/1985/head` and `develop` from GitHub, using the checkout's own ssh command.
  - Free disk stayed at 22 GiB throughout.
- **Deviation from the commission, stated:** node_modules are NOT linked from the read-only checkout.
  - That checkout sits at `5dccdcb2` (KS-1467). Its lockfile and package files differ from head's (31 files differ under the lockfile, package.json and packages/shared paths).
  - I linked gate 148's install instead, as gate 168 did. Its `package-lock.json`, package.json files and `packages/shared` are byte-identical to head's (`git diff --stat 27fe5476 a0a91f65` on those paths is empty).
  - The root `node_modules` is one symlink. `services/api-gateway/node_modules` is a real directory of per-entry symlinks, so vitest's `.vite` cache landed in MY clone and not in gate 148's tree (checked: gate 148's `.vite` is still dated 09:20).
- PR body: no `gh` auth is available (the project's GH_CONFIG_DIR is not logged in, and neither is the global one).
  - I read the builder's draft `5_Project_History/2026-11-03_seatS-15th/drafts/pr1_body_r2.md` instead. Its Ran section and its 14-input table match what is described below.
  - The builder's `patch_body.out` says the posted body read back equal (12560 chars). I did NOT verify the live body myself.

## Method
- **Probe:** `scripts/probe.ts`, adapted from gate 168's, which I read and did not edit. It drives the REAL `createBruteForceProtection` and `enforceClientRateLimit`, the real `services/redis.ts` and the real winston logger over real HTTP: express on 127.0.0.1, with the limiter mounted as auth.ts mounts it (`limiter(req,res,next).catch(next)`).
  - Only `ioredis` is replaced, by gate 168's Map-backed stand-in. In it, PEXPIRE ≤ 0 deletes the key, and a non-integer PEXPIRE rejects with Redis's own error text.
  - Three variants, each resolved in place of head's two middleware files from the same directory: **dev** (`ca2b2aa`), **r1** (`1e8c43fc`) and **head** (`a0a91f65`).
  - Requests reaching downstream are counted by the handler itself. Each row also records the status sequence, the X-RateLimit-Limit header, the 429 hint window, the Redis counter, every Redis call with its pexpire argument, every gateway log line, a planted-secret count (`G170PLANT-…`) over all stdout and stderr, and unhandled rejections.
- **Runs:**
  - `scripts/matrix.sh`: 435 rows (145 cells × 3 variants), every rc=0, in `logs/probe.jsonl`, paired in `logs/probe_table.txt`.
  - `scripts/timecells.sh`: 51 timed rows (17 cells × 3), each two bursts 62 s apart, in `logs/probe_time_table.txt`.
  - `scripts/suites.sh`: the whole suite ×2 at head, the 7 changed test files at head, and red-first on the r1 product and on the dev product, restored by sha256.
  - `scripts/static.sh`: tsc, the ratchet, and eslint with a planted control.
  - `scripts/mutants.py`: 31 mutants on head, each anchor matching once, sha256-restored, each run against the 7 changed test files.
- **Controls:** r1 is the instrument control for F1. It is MORE permissive than dev in 32 of the 130 same-input cells, so the comparison can and does fire.

## Findings

### G170-F1 — MEDIUM (HOLD-FOR-KAM condition, mixed-bucket only): when a malformed caller and a clean caller share one bucket, the clean caller gets more requests through at head than at develop
- **FOUND:**
  - **Same input:** 130 same-input limiter cells, and head is more permissive than develop in **0** of them (details under What passed).
  - **Mixed bucket:** two `req.user` shapes share one bucket (`jwt:t1:c1`) and alternate request by request. One has a clean `rateLimit` 100, the other a malformed value. Each burst is 200 requests (400 for `'500'`) in one 60 s window. At develop, the malformed requests are counted on the shared Redis counter and mostly refused, so they use up the clean caller's quota. At head they are refused with 503 **before anything is counted**, so the clean caller gets its full configured 100.

    Requests reaching downstream for the bucket, dev → head (r1 shown for reference):

    | clean / malformed | dev (clean+mal) | r1 | head (clean+mal) | head more permissive? |
    |---|---|---|---|---|
    | 100 / `'5'` | 52 (50+2) | 100 | 100 (100+0) | **yes** |
    | 100 / `-1` | 50 (50+0) | 100 | 100 (100+0) | **yes** |
    | 100 / `1.5` | 50 (50+0) | 100 | 100 (100+0) | **yes** |
    | 100 / `true` | 50 (50+0) | 100 | 100 (100+0) | **yes** |
    | 3 / `'5'` (12 requests) | 4 (2+2) | 8 | 3 (3+0) | no |
    | 100 / `'500'` (400 requests) | 250 (50+200) | 100 | 100 (100+0) | no |
    | 100 / missing (falsy control) | 100 | 100 | 100 | identical |
    | 100 / `0` (falsy control) | 100 | 100 | 100 | identical |

  - In every mixed cell, head's bucket total equals the clean caller's own configured ceiling and never exceeds it. The malformed caller gets 0.
  - Develop's lower figure is not a ceiling anyone configured. It comes from a broken peer burning the counter, which is itself a cross-caller interference at develop.
  - I state the condition because the class bar requires it. Wednesday rules whether it holds.
- **TESTED:** 8 `rl_mixed` cells × dev/r1/head, on the Redis path only.
- **NOT tested:** whether one bucket can actually carry two different `rateLimit` values. API-key buckets are per key and take the key record's value. The `jwt:` bucket is tenant+connector, so two machine JWTs with different claims would share it. Not measured; see NOT tested.
- **HOW:** `rl_mixed` rows in `logs/probe.jsonl`. `perKind` splits downstream calls by caller. Redis counter: dev 200, head 100, so head did not count the 100 refused requests.

### G170-F2 — LOW: the guard still hangs a login if the response's own `status()` throws; no unhandled rejection, no leak, downstream 0
- **FOUND:** I ran 10 `bf_429throw` cells with a planted lockout and a fault in the guard's 429 write.

  | fault | dev | r1 | head |
  |---|---|---|---|
  | Retry-After throws: Error | 401, downstream 1, plant logged | hang 4 s, 1 unhandled rejection | **503**, 0 unhandled, plant 0 |
  | Retry-After throws: string | 401, downstream 1, plant logged | hang 4 s, 1 unhandled rejection | **503**, 0 unhandled, plant 0 |
  | Retry-After throws: object | 401, downstream 1 | hang 4 s, 1 unhandled rejection | **503**, 0 unhandled |
  | Retry-After throws: revoked Proxy | 401, downstream 1 | hang 4 s, 1 unhandled rejection | **503**, 0 unhandled |
  | `json()` throws | 401, downstream 1, plant logged | hang 4 s, 1 unhandled rejection | **503**, 0 unhandled, plant 0 |
  | the BRUTE_FORCE_BLOCKED log throws | 401, downstream 1, plant logged | hang 4 s, 1 unhandled rejection | **503**, 0 unhandled, plant 0 |
  | the whole logger throws (`warn` and `error`) | hang 4 s, 1 unhandled rejection | hang 4 s, 1 unhandled rejection | **503** (no line), 0 unhandled |
  | response committed upstream | 202, downstream 1 | hang 4 s, 1 unhandled rejection | 202 ended, downstream 0, 0 unhandled |

  - Control `none`: 429 at all three variants.
  - Residual: when `res.status()` itself throws, both the 429 and the 503 attempt fail. Head then answers nothing within 4 s.
    - It still has 0 unhandled rejections, 0 downstream and plant 0, and it logs one type-only line.
    - Dev answered 500 and reached downstream. r1 hung with an unhandled rejection that carried the planted text.
  - This is less permissive than develop, and the cause is a broken response object, which is contrived.
- So, F3: the hang and the unhandled rejection are gone for every write fault except a throwing `status()`, which still hangs. No thrown text reached the client body (fixed body) or the log (plant 0 in all 10 head cells).
- **TESTED / HOW:** `bf_429throw` rows. The limiter's `refuseUnavailable` has the same shape, but a throwing `status()` was not driven there.

### G170-F3 — INFO: the malformed-allowance refusal logs one error line per request, unthrottled
- **FOUND:**
  - `rl_value '5'`, 105 requests: head writes 105 `logger.error` lines, each type-only (`{"clientId","step":"configured-allowance","field":"rateLimit","valueType":"string"}`).
  - Round 1's malformed warning was throttled (1 line per 30 s), and develop wrote none.
  - The other limiter refusal steps already log per request, so this follows their shape. It is a log-volume note, not a leak: plant 0, value never printed.
- **HOW:** the `logs` counts in `logs/probe_table.txt`.

### G170-F4 — LOW, PRE-EXISTING (carried from G168-F5): mutant M6 survives, and it is equivalent
- **FOUND:** the shape check accepting arrays survives, the same as gate 168. It is equivalent for JSON-sourced records: an array has no finite `attempts`, so it is still refused. The other 30 mutants are killed. **M9 is now KILLED**, by `G-R11`, by assertion.

## What passed (measured)
- **F1, same input (the deciding count):** 130 same-input limiter cells, comparing dev against head.
  - Cell breakdown:
    - 41 rateLimit values on the Redis path;
    - 14 on the KS-617 memory path;
    - 29 windows × 2 paths;
    - 17 timed two-burst cells.
  - Outcome, head against dev: **head > dev in 0**, head < dev in 74, equal in 56.
  - The 56 equal cells: 33 falsy, 13 clean, and 10 where both answer 0.
  - Head never mixes a 503 with a pass in one cell: every truthy-malformed cell is 503 for every request, with 0 downstream calls, 0 Redis calls and counter null.
  - Gate 168's 14 inputs (requests allowed, dev → head): rateLimit `-1` 0→0, `0.5` 0→0, `-Infinity` 0→0, `1.5` 1→0, `99.5` 99→0, `'5'` 5→0, `'99'` 99→0, `true` 1→0, `[5]` 5→0.
  - Windows `'120'`, `120.5`, `Infinity`, `{}`, `1e300`: 3→0 in one burst and 3→0 over two bursts 62 s apart. Round 1 gave 6 over two bursts.
  - My added forms are all head 0. With the dev figure:
    - rateLimit: `'1\n'` 105, `Infinity` 105, `'100'` 100, `'500'` 105, `'1e3'` 105, `'120'` 105, `'0'` 0, `' 5'` 5, `'0x10'` 16, `'abc'` 105, `' '` 0, `{}` 105, `[]` 0, `2^53` 105, `1e300` 105, `5n` 105, `new Number(5)` 5, `{valueOf:5}` 5, `new Date(0)` 0;
    - windows: `-1`/`-60`/`'0'`/`[]` 8/8 at dev, `'30'`, `'5'`, `0.5`, `1.5`, `true`, `[5]`, `'1\n'`, `-Infinity`, `5n`, `new Number(5)`.
  - Two-burst rateLimit cells (dev → head): `'5'` 10→0, `1.5` 2→0, `true` 2→0, `[5]` 10→0, `'99'` 16→0.
- **F1, falsy byte-for-byte:** 30 untimed falsy cells. They are rateLimit `0`, `NaN`, `false`, `''`, missing, `null`, `-0` and `0n` on both paths, and windows `0`, `NaN`, `false`, `''`, `null`, missing and `-0` on both paths.
  - All 30 are **identical dev = head** on status sequence, allowed count, limit header, hint, Redis counter, the full Redis call list with pexpire arguments, response bodies, log lines (including the KS-164 "no rateLimit" warning text), plant count and unhandled.
  - The 3 timed falsy cells are equal too.
  - The 13 clean-value cells (1, 3, 100, 101, 1e15; windows 60, 1, 3600; the memory-path 3; the timed 60) are identical as well.
- **F3:** see G170-F2. Of 9 write-fault cells, head refuses 7 with 503, ends 1 already-committed response, and hangs 1 (`status()` throws).
  - Downstream at head: 0 in all 9. Dev reached downstream in 8.
  - Unhandled rejections at head: 0 in all 9. r1 had 9 of 9.
  - Plant at head: 0 in all 9. Dev had 5 lines.
- **F4:** 6 degrade cells: ordinary, secretError, secretString, secretObject, revokedProxy, getterThrows.
  - Allowed count, status sequence and Redis calls are identical dev = head in all 6 (3/6, `incr`×6). The behaviour is unchanged.
  - The log line differs only in `"error":"<text>"` → `"thrownType":"<type>"`.
  - The plant reaches the log at dev in 2 of 6 (secretError, secretString) and at head in **0 of 6**. That is the positive control and the measurement in the same run.
- **G168-F2 smoke:** `bf_fault` and `bf_lockout` with ordinary, secretError and hang.
  - Head: 503 with 0 downstream; the hang cells answered 503 at 2005 ms and 2007 ms.
  - Dev: 401 with downstream 1, or no answer at 4 s.
  - No-fault controls: 401 and 429 at all three variants. G168-F2 holds.
- **Red-first:** head's tests on the r1 product: **28 red, all by assertion**.
  - The 13 L-R4 rateLimit cells (`-1`, `0.5`, `-Infinity`, `1.5`, `99.5`, `'5'`, `'99'`, `true`, `[5]`, `'1\n'`, `Infinity`, `'100'`, object), the 8 L-R5 window cells, L-R7, G-R10, and the 5 changed KS-1868 degrade cells (C1, C2, R1-R3).
  - **G-R11 (the M9 cell) passes at r1.** Round 1 already ended a committed response, so this cell kills the mutant but is not a fix proof. It is red at dev by assertion.
  - On the dev product: 60 red, all by assertion. By file: guard 14/18, limiter 29/42, ks1868 limiter 10/10, ks1868 guard 6/8, security 1/15.
  - auth.test.ts (19/19) and ks480 (5/5) are green at both bases, as gate 168 found.
- **Suites at head:** the whole api-gateway suite, run twice: 149 files, **1566/1566** both times, 0 failed. The 7 changed files: 117/117. This matches the builder's 1566 and 117.
- **Static at head:**
  - service `tsc --noEmit`: rc 0, 0 errors;
  - ratchet: "25 errors: 25 in the baseline, 0 new";
  - eslint on the 9 PR TS files: rc 0 with 0 problems. The planted control gives 2 problems, rc 1.
  - The builder's own `static.out` says "warnings 1", but the body and my run both say 0.
- **Mutants (raw table counted, `logs/mutants.out`, `logs/mutants_table.jsonl`):**
  - Unmutated control: 117/117.
  - 31 mutants: **30 KILLED**, all by assertion; **1 SURVIVED** (M6, equivalent). All 31 restored by sha256, and the porcelain was clean afterwards. Headline = table.
  - The round-2 mutants are all killed. In M-numbers:
    - M19 malformed refusal removed; M20 rateLimit refusal only; M21 window refusal only; M22 refusal also calls next(); M23 back to round-1's default; M24 and M25 falsy values also refused (truthy guard dropped). M24 and M25 are killed by L-C4 and L-C5, so the byte-for-byte falsy path is pinned by tests;
    - M26 the refusal logs the value; M27 503→429; M28 the degrade line logs text again;
    - M29 the guard's 429 write back outside the try; M30 the 429-write catch calls next(); M31 the wrong refusal line;
    - plus M9.
  - The builder's 12/12 is a subset, and my count agrees with it.

## NOT tested
- Whether any real bucket can hold two different `rateLimit` values at once: two machine JWTs for one tenant+connector, or a key record changed mid-window. That is the real-world reach of G170-F1. Read only.
- Whether production records can carry a malformed `rateLimit` or window at all. By the builder's reading, an INTEGER column validated 1..10000, and auth.ts:317 applies `|| 100`. Not measured.
- The limiter's `refuseUnavailable` when `res.status()` throws; only the guard's was driven (G170-F2).
- A getter on `req.user.rateLimit` that returns different values between the check and the use.
- A real Redis, more than one replica, the booted gateway `index.ts`, the auth-service lockout, Node 24, Linux or CI, and production logger transports. These are excluded by the commission or the builder's NOT DONE list.
- Mutants against the whole suite; each ran against the 7 changed files only.
- The live PR body. I read the builder's draft, not GitHub.

## Plain answer for Kam
- If a connector's rate-limit setting is garbage (text like "5", a fraction, a negative number, "true", a window of "120"), the gateway now refuses its requests with "try again later" instead of guessing a limit. I checked 130 such settings against today's code, and none lets more requests through than today. Missing or zero settings behave exactly as today.
- One case for you to rule on: if a broken caller and a normal caller ever share one rate-limit bucket, the normal caller now gets its full configured allowance (100), where today the broken caller's refused requests use up half of it (50). It never goes above what was configured. I did not measure whether two such callers can actually share a bucket.
- A login that is locked out no longer hangs or slips through when writing the "locked out" answer fails. It gets "try again later" instead. It only still hangs if the web server's response object itself is broken.
- The fallback warning line no longer copies error text, which could hold secrets, into the logs. Its behaviour is the same.
- The missing test from last round now exists and catches the gap it was meant to catch.

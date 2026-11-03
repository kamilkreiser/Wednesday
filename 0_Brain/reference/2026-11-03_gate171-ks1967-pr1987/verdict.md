GO WITH NOTES — MERGE (no HOLD-FOR-KAM)
# QA Gate 171 (Tier 1, round 1): PR 1987 / KS-1967 the login lockout fails closed while the session store is down

## Subject (pinned)
- Start, `git ls-remote origin` from the read-only checkout: `refs/pull/1987/head` = `f1641944de444e0a6f402cce8d897fde0b3cc4e5`, `refs/heads/develop` = `de8d208a8426747b3a752309e08167fa0de4b2ff`. These match the commission.
- End, same command: the same two SHAs. Nothing moved.
- One commit (`f1641944d`, parent `de8d208a8`). merge-base = develop. `git merge-tree --write-tree de8d208a8 f1641944d` in my clone gave rc=0, tree `6e6e393ffdb49ae3ba5252a1246f1989fb73747e`.
- Diff: 9 files, +542 / -15.
  - The only product file is `services/auth/src/services/accountLockout.ts`.
  - Tests: 1 new file (397 lines), plus 5 existing test doubles.
  - Docs: 2 HTML fragments.
- Host: macOS (Darwin 27), Node v26.8.1, vitest 4.1.12.
  - Install: gate 148's node_modules, linked. Its `Blockchain/Dev/package-lock.json`, root `package.json`, `services/auth/package.json` and `services/auth/package-lock.json` have the same blob hashes as head's. Its `packages/` tree hash (`e44aaeaf`) is the same as head's.
  - `services/auth/node_modules` is a real directory of per-entry symlinks, so the vitest `.vite` cache went into my clone.
  - Clone: `--shared`, cone `Blockchain/Dev` (236 MB). Free disk was 17 GiB at the end.
- Not run on: Linux/CI, a real Redis, a booted service, the four platform suites.

## Method
I recorded base against head with the real `accountLockout`, the real `passwordLoginGate` and the real auth, oauth and wallet routers, driven over HTTP on 127.0.0.1. The recorder is `scripts/gate171-recorder.test.ts`, written by me and separate from the builder's file. Its store doubles and its door list are my own.

- **Doors (15):**
  - /login: user, user+TOTP, admin, admin+TOTP.
  - /login refusal paths: unknown email, suspended, SSO-only, backup-code race.
  - POST /oauth/authorize: plain and +TOTP.
  - POST /wallet/verify, POST /wallet/authenticate, wallet+TOTP.
  - `assertAccountMayReceiveCredential` called directly: plain and +TOTP. This is the gate the social callback uses.
- **Store states (7), all stand-ins (no Redis daemon):**
  - connected, and slow (40 ms per command): the two controls.
  - null client.
  - every command throws.
  - every command throws the real `ioredis` `MaxRetriesPerRequestError` class.
  - reads throw, writes work.
  - writes throw (an `OOM command not allowed` ReplyError shape), reads work.
- **Other axes:** locked and unlocked, crossed with right and wrong credential. That gives 420 cells per side.
- **The `createSession` stand-in uses the same store as the lockout.** It throws `Redis is not available` with no client, and throws the store's error in every fault state. This is modelled from `session.ts:170-171` and from its first command being a read followed by writes. I read that from source and did not drive it.
- **How base was produced:** the same harness with develop's `accountLockout.ts` blob swapped in, since that is the only product change. `scripts/compare.py` compares base and head cell by cell.
- **Sentinels:** a lockout-store sentinel and a separate session-store sentinel were planted in every thrown message.
- **Controls, all run in the same action:** the base→head direction of the permissiveness count, base's right/wrong differences, base's sentinel hits, and connected-unlocked-right grants at every door.

## Findings

### G171-F1 — MEDIUM (PRE-EXISTING class, not closed by this PR): when the store refuses writes but serves reads, a right and a wrong password still answer differently at 5 doors
- **FOUND:**
  - **The state:** reads work and writes are refused (Redis `OOM` under `noeviction`, `MISCONF` after a failed save, or `READONLY` on a promoted replica).
  - **The difference at head:** a right password answers **500 INTERNAL_ERROR** and a wrong one answers **503 SERVICE_UNAVAILABLE**. No failure is counted, because the counter write fails.
  - **The 5 doors:** login-user, login-user+TOTP, login-admin, login-admin+TOTP, wallet+TOTP. For the TOTP doors the factor is the right/wrong axis.
  - **Where the 500 comes from:** `createSession`'s own store write, not the lockout. `recordSuccess` stays non-fatal, as designed.
  - **Base has the same oracle:** 500 against 401.
  - **At authorize:** a right password gets a code minted (302, the code goes to the DB). A wrong one gets 500 at head and 401 at base.
  - So head is not more permissive anywhere. But in this one state the ruling's bar ("a right and a wrong password answer IDENTICALLY" while the store is down) is not met.
  - **The PR's own cell does not see this.** Its writes-throw cell ("a right password is still granted") passes only because its `createSession` double succeeds whenever the lockout store's writes throw (test lines 59-66 and 152: `sessionStoreDown` is false for `writeThrows`). The real `createSession` writes to the same Redis.
  - **No existence leak:** unknown email, suspended and SSO-only all answer the same 503 as a wrong password (driven).
- **TESTED:** 12 groups (door × locked) of the writes-throw state differ at head; base also has 12. The unlocked login groups are the ones above. The two wallet locked groups differ only in store-op counts. Not exercised: a real Redis in OOM, MISCONF or READONLY. The 500 is from my `createSession` stand-in, modelled from `session.ts` and not driven.
- **HOW:** `scripts/gate171-recorder.test.ts` + `scripts/compare.py` (`logs/compare_base_head.txt`, section "head: DOWN groups where right != wrong").
- **Note:** this is not a regression. It is a residual against Kam's ruled wording, so Wednesday may want to put it to Kam as a follow-up ticket. Closing it would mean making `createSession`'s store failure answer the same 503, which is outside this PR's one file.

### G171-F2 — LOW (PRE-EXISTING; claim precision): wallet checks the lockout after verifying the signature
- **FOUND:**
  - **The claim** is "every password door runs the check before any user lookup or password verification". That holds for /login and /authorize.
  - **At `routes/wallet.ts`** the gate (:361) runs after `verifyCIP8Signature` and after `getOrCreateWalletUser`. A user row can be created before the gate.
  - **Effect with the store down:** a valid signature gets 503 and an invalid one gets 401, at both `/verify` and `/authenticate`. That is 16 differing groups at head (null, throwAll, maxRetries, readsThrow × 2 routes × locked/unlocked); base has 500 against 401.
  - This is not a password-guessing oracle, because nothing secret is being guessed online.
  - The builder lists only `wallet/verify`. `/authenticate` is a second route on the same handler.
  - **Social callback (read, not driven):** `GET /social/:provider/callback` (auth.ts:1083) can `createUser` (≈:1310) before its gate at :1334.
- **TESTED:** wallet driven at route level with the CIP-8 check stubbed (valid iff signature = right). Social callback not driven.
- **HOW:** same recorder. Census by `git grep` at the PR head.

### G171-F3 — LOW (PRE-EXISTING): `createSession`'s thrown text reaches a log line in the writes-refused state
- **FOUND:** the session-store sentinel appears in log lines in 7 head cells (49 at base), through `errorHandler`'s `error: err.message, stack`. That is the KS-1346 class, outside this PR. It reached no client body: 0 at both. The lockout-store sentinel appears in **0** lines at head against 370 hits in 194 cells at base (the control).
- **TESTED:** every cell's captured logger lines, response bodies and headers.
- **HOW:** recorder fields `lockSentInLogs`, `sessSentInLogs`, `*InBody`.

### G171-F4 — LOW (test robustness): the new test file's `beforeAll` can exceed vitest's default 10 s hook timeout on a cold cache
- **FOUND:** the first cold run of `ks1967-…test.ts` at head failed: "Hook timed out in 10000ms", 46 skipped. Warm re-runs with the default timeout passed 46/46. The `beforeAll` imports three routers.
- **TESTED:** this host only; CI not measured.
- **HOW:** `logs/new_head.log` (cold) and `logs/new_head_default.log` (warm, default timeout).

### G171-F5 — LOW: door census — lockout callers the builder did not drive
- **FOUND:** every product caller, from `git grep -n -E 'isLockedOut|recordFailure|recordSuccess'` over the **whole repo** at `f1641944d` (61 files; the product hits are below). Line numbers are at head.

  | # | Call site | Path | Builder drove | Gate 171 drove |
  |---|---|---|---|---|
  | 1 | auth.ts:352 isLockedOut | POST /api/auth/login, every login | yes | yes |
  | 2 | auth.ts:362 recordFailure | admin, wrong password | yes | yes |
  | 3 | auth.ts:445 recordFailure | admin, wrong TOTP | **no** | yes (login-admin-mfa) |
  | 4 | auth.ts:492 recordSuccess | admin success | yes | yes |
  | 5 | passwordLoginGate.ts:386 isLockedOut (enforce) | /login user, POST /oauth/authorize | yes | yes |
  | 6 | passwordLoginGate.ts:393 recordFailure | unknown email | **no** | yes |
  | 7 | passwordLoginGate.ts:402 recordFailure | suspended / deactivated | **no** | yes |
  | 8 | passwordLoginGate.ts:408 recordFailure | SSO-only (no hash) | **no** | yes |
  | 9 | passwordLoginGate.ts:415 recordFailure | wrong password | yes | yes |
  | 10 | passwordLoginGate.ts:233 isLockedOut (credential gate) | wallet, social, direct | direct call only | wallet routes + direct |
  | 11 | passwordLoginGate.ts:240 recordFailure | status at the credential gate (wallet/social, suspended account) | **no** | **no** |
  | 12 | passwordLoginGate.ts:307 recordFailure | backup code lost race | **no** | yes |
  | 13 | passwordLoginGate.ts:318 recordFailure | second factor failed | **no** | yes (4 doors) |
  | 14 | passwordLoginGate.ts:327 recordSuccess | every gate passed | yes | yes |

  - **Gate entry points:**
    - auth.ts:530 (/login)
    - oauth.ts:768 (POST /authorize, route :639)
    - wallet.ts:361 (`handleWalletVerify`, mounted on `/verify` **and** `/authenticate`)
    - auth.ts:1334 (social callback, route :1083)
    - passwordLoginGate.ts:427 (internal)
  - **Not callers of `accountLockout`, and untouched by the PR:**
    - same-named functions in `packages/shared/src/security/index.ts` (:192, :211), `services/api-gateway/src/middleware/security.ts` (:264, :277) and `services/shared/src/security/redis-security-store.ts` (:158, :189);
    - `services/auth/integration/ks1848-…integration.ts`, which mocks the lockout;
    - systemTest Python, which only references it.
  - **Census control:** a second pattern, `accountLockout`, found exactly the two product importers (auth.ts:348 and passwordLoginGate.ts:229/:380) that the name grep found.
- **TESTED:** of the builder's undriven sites, I drove every one except #11 and the social callback route. Each gave a uniform right/wrong answer at head in all store-down states except as noted in F1.
- **HOW:** recorder doors login-unknown / -suspended / -sso / -backup-race / *-mfa. Positive controls: the connected-state wrong cells show `incr` = 1 at each site.

## What passed (measured)
- **Q1, more permissive than base:**
  - Store down: **0 of 300** head cells (5 down states × 15 doors × 2 × 2).
  - Store up: 0 of 120.
  - Control, the other direction: base is more permissive in 40 cells. These are authorize minting a code, and the credential gate answering `ok:true`, for locked accounts with the store down.
  - No locked cell with the store down ran a password or TOTP verify at head: 0, against 72 at base.
  - With the store down, a wrong credential answered a plain 401 in 130 cells at base and 31 at head. The head 31 are 11 locked writes-throw cells at the non-wallet route doors (the lock is readable, so 401 is correct), plus 20 wallet invalid-signature cells across all five down states (F2; the signature fails before the lockout is consulted).
- **Q2, right vs wrong with the store down:**
  - **0 differing groups** in the null, throwAll, maxRetries and readsThrow states, except wallet (F2).
  - The writes-throw state has 12 (F1).
  - In total, 28 of 150 groups differ at head against 92 of 150 at base (the control).
  - Compared per group: status, body, headers (content-type, location, retry-after, cache-control, set-cookie present), sessions, codes, token pairs, challenge deletes, store-op counts.
  - Work class: verify, TOTP and CIP-8 call counts. Any password verify while the store is down happened only in the writes-throw state, and there the right and wrong credential did the same work.
- **Q3, sentinel leaks:**
  - Lockout-store text in logs: 0 at head (0 lockout-module lines), against 370 hits at base.
  - In bodies or headers: 0 at both.
  - The `MaxRetriesPerRequestError` case logs `thrownType:"MaxRetriesPerRequestError"`.
- **Q4:** see F5.
- **Q5, store up:** 120 cells, head against base on every observable: **0 differ**. Lockout log lines: 0 differ. Counts include the `incr` and `del` attempts.
- **Q6, red-first and suite:**
  - The PR's new file at develop (develop's `accountLockout.ts` blob, otherwise head): **26 failed / 20 passed of 46**. All 26 are the RED cells and every one fails by assertion: 23 `AssertionError`, plus 3 vitest `rejects`/`resolves` expectation failures (`runs/new_base.json`). The 20 that pass are the controls.
  - The new file at head: 46/46.
  - Auth suite at head, run twice: **1669/1669, 416 tests in 140 files, 0 failed**, both runs (`runs/suite_head_1.json`, `runs/suite_head_2.json`).
- **Mutants (mine, 16, against the PR's new file):** raw table `runs/mutants_raw.tsv`, counted: **16/16 killed, 0 survivors**. Fail counts:

  | Mutant | Failed |
  |---|---|
  | m01 | 8 |
  | m02 | 10 |
  | m03 | 10 |
  | m04 | 1 |
  | m05 | 3 |
  | m06 | 4 |
  | m07 | 1 |
  | m08 | 3 |
  | m09 | 1 |
  | m10 | 25 |
  | m11 | 7 |
  | m12 | 3 |
  | m13 | 10 |
  | m14 | 6 |
  | m15 | 4 |
  | m16 | 3 |

  The list is in `mut/index.json`. It covers no-client/catch → fail-open at each function, message logging at each catch, `recordSuccess` made fatal, a broken `thrownTypeOf`, an inverted lock read, thrown text in the 503 body, rethrowing the original, and a plain-Error 500.
  - m04 and m07 are killed only by the direct primitive cells.
  - I did not re-run the builder's 11 mutants; they are not on disk here.
- **Q7, the five test doubles** (auth.integration, ks1885, ks722, ks795, ks819):
  - `git diff --numstat`: 9/0, 10/0, 10/0, 10/0, 10/0. Additions only.
  - None of the added lines contains `expect`.
  - `expect(` count per file, develop = head: 154, 15, 24, 93, 34.

## NOT tested
- A real Redis daemon in any state (OOM, MISCONF, READONLY, network partition, a hang that ends in `MaxRetriesPerRequestError` after the retry strategy) on a booted service. Every store state is a stand-in.
- The real `createSession` / `session.ts` against a failing store. My stand-in models it from source (F1).
- The social callback at route level with the store down. Its gate was driven directly, and its state check and pre-gate `createUser` were read only.
- Census site #11 (passwordLoginGate.ts:240).
- GET /oauth/authorize, /token and refresh, which the PR does not touch.
- Real argon2 timing. The timing class was compared as work done (verify count), not wall-clock.
- More than one replica. The api-gateway's brute-force limiter. Clients' handling of a 503 on login (frontend, SDK, mcp-server). The four platform suites. The integration suites (`vitest.integration.config.ts`). The schemathesis systemTest. Pre-push legs.
- KS-1965 (store down at boot) and KS-1968 (HIBP).
- Whether any of these doors is reachable in production. No exposure claim is made.

## Plain answer for Kam
- When the login store goes down, the PR does what you ruled. Every way of signing in refuses, and a locked account can no longer get through: before this, the OAuth sign-in door would hand a locked account a sign-in code during an outage.
- In the common outage cases (store unreachable, or every command failing), a right password and a wrong one now get exactly the same answer, so an outage can no longer be used to test passwords.
- One narrower outage remains. If the store can still be read but refuses writes (for example, it is full), a right password gets a different error from a wrong one. That was already true before this change; the PR does not make it worse, but it does not close it either.
- With the store healthy, nothing changes for anyone. I checked 120 normal sign-in cases and every one gave the same answer as before.

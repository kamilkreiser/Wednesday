GO WITH NOTES — MERGE (no HOLD-FOR-KAM)
# QA Gate 175 (Tier 1, round 1, batched): PR 1990 + PR 1991 / KS-1868 shared catches read an unreadable thrown value safely

Batched gate. Line 1 holds for BOTH PRs: each PR has its own verdict line below, reached separately. Neither decides the other.

- **PR 1990:** `GO WITH NOTES — MERGE (no HOLD-FOR-KAM)`
- **PR 1991:** `GO WITH NOTES — MERGE (no HOLD-FOR-KAM)`

## Subject (pinned at start AND end; nothing moved)

| ref | start, 21:56 AEDT | end, 22:14 AEDT |
|---|---|---|
| refs/heads/develop | `1cbf260548e7fd534603725f9fc6b05c5cdd9907` | `1cbf260548e7fd534603725f9fc6b05c5cdd9907` |
| refs/pull/1990/head | `5550a714f5e2962e062af4893d2a3277b30ca110` | `5550a714f5e2962e062af4893d2a3277b30ca110` |
| refs/pull/1991/head | `a44e59c5f9dfcddb4343e41686d90d5134b2d1d6` | `a44e59c5f9dfcddb4343e41686d90d5134b2d1d6` |

I read all of these with `git -C <checkout> ls-remote origin …`. Each PR is one commit on `1cbf2605` (merge-base = develop). The file counts and line counts match the READY mails: 12 files +551/-5, and 12 files +811/-11.

**Merge-tree (Q8), run in my clone:**
- `merge-tree --write-tree develop 1990`: rc 0, tree `96587b0e3aac…`. That equals 1990's own head tree.
- `develop 1991`: rc 0, tree `bb8a752c1b61…`. That equals 1991's own head tree.
- Shared paths between the two PRs: **0**. The control (1990 against itself) gives 12.
- 1991 onto develop+1990: rc 0, tree `eba3a575e8aa…`. 1990 onto develop+1991: rc 0, the same tree `eba3a575e8aa…`. The merge result is the same in either order.
- Planted controls: I made a develop commit that edits the same line of `key-vault.ts`. Merge-tree against 1990 gives rc 1 and names `key-vault.ts`. The same kind of commit on `redis-client.ts` against 1991 gives rc 1 and names `redis-client.ts`. So the instrument does detect conflicts.

**Host:**
- macOS Darwin 27, Node **v26.8.1** (not the LTS 24 line), TypeScript 5.9.3 (packages/shared), express 4.22.3, winston 3.19.0.
- Vitest **4.1.12** with vite 7.3.7 and esbuild 0.28.1, which are the versions pinned in develop's root lock. I installed them into an ignored `scratch/vt` folder because the sparse clone has no workspace-root install.
- I did NOT run on Node 24, in a container, against a real Redis, Postgres or Azure Key Vault, or over HTTP.

**Install:**
- The gate 171 and 172 installs both link to gate 148's `node_modules`, and that is now a husk of 832 KB (moved to G-DRIVE). The checkout's own install is at a different lock: root lock `6a419fb8` vs develop's `30777ce9`, with zod 3 vs 4. I linked neither.
- Instead I ran `npm ci --ignore-scripts` in my clone for `packages/shared`, `services/shared` and `services/auth`, from their own lock blobs. Those blobs are identical at develop, 1990 and 1991: `c100fb8e`, `c3938de8`, `cddd2274`.
- `@secuura/shared` is a symlink to my clone's `packages/shared`, and its `dist` was built with tsc in my clone.
- Disk: 25 GiB free at start and at end (floor 18).

**Method.**
- I swapped base and head per product file with `scripts/swap.sh`: develop's blob or the PR head's blob for the 9 product files, keeping the PRs' tests. The script printed the blob hashes on every swap.
- I drove the REAL modules from vitest recorders (`harness/`) with **17 value classes**: an ordinary Error, an Error whose message getter throws, a revoked Proxy, null, undefined, a string, a number, `Object.create(null)`, `{message: Symbol}`, `{message: BigInt}`, `{message: revoked Proxy}`, `{message: object whose toString throws}`, a Proxy whose get trap throws, a thrown Symbol, an Error whose name getter throws, a readable message with a throwing toString, and a plain `{message}`.
- Stand-ins were limited to the Azure vault client (an instance field), `pg` (vi.mock), `ioredis` (a `Module._load` hook for the rate limiter's runtime `require`, and vi.mock for redis-client), the services/shared `redis-client` (for the stores and cacheMiddleware), and req/res objects.
- The loggers were the real winston loggers. Output was captured at `console.*`, `console._stdout/_stderr` (winston's Console transport) and `process.std*.write`.
- `jwt.ts` is the REAL `services/auth/src/services/jwt.ts`. It imports the REAL key-vault through the same `@secuura/shared/vault/key-vault` module instance, with two RSA keys generated in memory only (A = environment, B = vault). Neither key was written anywhere: I grepped `runs/` and `results/` for PEM markers and their base64 form, and got 0 hits.
- The class bar is computed by `scripts/classbar.py`. For every site, the reference is BASE's outcome for the ordinary Error.
- Raw rows: `results/p1990_{base,head}.jsonl` (187 cells each) and `results/p1991_{base,head}.jsonl` (357 each). Side-by-side tables: `results/p199x_table.md`.

---

# PR 1990: packages/shared, five catches (key-vault, tenant rate limiter, tenant-pool-manager, tenant-context, auto-migrate)

**Verdict PR 1990: `GO WITH NOTES — MERGE (no HOLD-FOR-KAM)`**

**Class bar: 0 of 176 non-ordinary head cells are more permissive than base-ordinary.**
- 161 of 176 cells equal base-ordinary.
- 60 cells changed from base to head, and every one of them changed TO the base-ordinary outcome.
- The 15 cells that are not base-ordinary are unchanged from base (base = head), and all 15 are less permissive (a rejection or no answer). They are listed in G175-F2.

## Findings (PR 1990)

### G175-F1 — LOW (note for Wednesday's ruling): on the JWT key path, head now caches the environment key for an unreadable vault error, exactly as it already does for an ordinary vault error
- **FOUND:**
  - **getSecret, called directly with `fallbackToEnv: true` (jwt.ts's setting).** For 5 classes (message getter throws, revoked Proxy, null, undefined, throwing get trap), base REJECTED with a new Error or TypeError. Head RETURNS the environment value and caches it for 5 minutes, which is the ordinary-Error outcome. 9 more classes already did this at base.
  - **getSecret with `fallbackToEnv: false` (the production default for any other caller).** Head never returns a secret: 17/17 cells throw, base and head alike. The 5 changed cells move from throwing a new TypeError/Error to throwing `Secret "…" not found`.
  - **Through the real `initJwtKeys()`, the FIRST read uses the same key source at base and head in 17/17 cells:** the environment key A with `kid-env`. Head is never a different key source than base on the failing read.
  - **What changes is the cache.**
    - For the 5 classes, base cached nothing. So when I re-ran `initJwtKeys()` after the vault recovered, within the 5-minute cache, base switched to **vault key B**.
    - Head cached both `jwt-private-key` and `jwt-key-id` from the environment, and keeps serving **environment key A** until the cache expires.
    - Base already does exactly this for an ordinary vault Error (row V01: cached, env A after recovery).
  - Measured against base for the HOSTILE value, head serves a stale cached key for at most 5 minutes after the vault recovers. Measured against base-ordinary (the class bar), it is identical.
  - Head never yields a key read where base refused. In every cell, jwt.ts's own catch already read `JWT_PRIVATE_KEY` from the environment at base.
  - I did not write HOLD-FOR-KAM:
    - 0 cells exceed base-ordinary.
    - The key source never differs.
    - Key material is not one of section 6's named signature classes.
  - If Wednesday rules that JWT key material IS a signature class, the condition and the evidence are above.
- **TESTED:**
  - The real key-vault, 17 classes × {direct with fallback on, direct with fallback off, jwt.ts path} = 51 cells per tree.
  - The vault client is a stand-in that rejects with the value. No `@azure/*` package was loaded.
  - Not tested: a real Key Vault, a real rotation, or more than one process.
- **HOW:** `harness/p1990.test.ts` Q1a/Q1b, run by `scripts/run1990.sh base|head`. Positive control: the ordinary Error prints its sentinel in the vault warning (1 line) at both trees, so the instrument can see log output.

### G175-F2 — LOW: 15 head cells still do not reach base-ordinary (unchanged from base, all less permissive)
- **FOUND:**
  - **Tenant rate limiter, 9 cells.** These are `{message: Symbol}`, `{message: revoked Proxy}` and `{message: object whose toString throws}`, each × 3 triggers (redis.incr, res.setHeader, downstream next).
    - `reason = err.message` succeeds, but the template literal `${reason}` on line 207 then throws, and that is outside the guard.
    - The middleware still rejects with no `next()`, as at base.
  - **getSecret / jwt, 6 cells.** These are `{message: BigInt}` and `{message: revoked Proxy}`.
    - The real winston logger throws a TypeError while it formats the `{ error: reason }` meta, so getSecret rejects before the environment fallback, as at base.
    - jwt.ts's own catch still reads the environment key, so this is not a key-source difference.
  - **extractTenantContext, 4 cells (read, not driven).** For the same two classes, head builds a 503 body that `JSON.stringify` cannot serialise. My `res` stand-in does not serialise, so a real express `res.json` would throw out of the catch. This is the same at base.
- **TESTED:** recorder cells, base and head. Not tested: express `res.json` itself.
- **HOW:** `results/p1990_classbar.txt` lists all 15 cells with their base, head and reference outcomes.

### G175-F3 — LOW, PRE-EXISTING (base = head): extractTenantContext answers the thrown value's message to the client, and its try wraps `next()`
- **FOUND:**
  - The 503 body carries `message: err.message`. 8 of 34 cells carry my sentinel in the response body, at base and head equally. That runs against the KS-1346/1348 rule (types and field names, never values).
  - Because `next()` is inside the try, a downstream handler's synchronous throw is answered as `Tenant database unavailable` with that handler's message.
  - The rate limiter has the same pattern: its try also wraps `next()`, so a downstream throw calls `next()` a second time. This happens at base-ordinary and at head, in 3 of 3 triggers.
- **TESTED:** the real middleware with stand-in req/res. Not tested: whether originate's mounted chain (`services/originate/src/index.ts:235`) ever throws synchronously in production.
- **HOW:** Q3b and Q2 cells (the `downstream next() throws` trigger).

## What passed (measured), PR 1990

**Q1 (key material):**
- 51 cells per tree.
- The first-read key source is equal at base and head in 17/17 cells.
- 0 key reads at head where base refused.
- A stale cached key after vault recovery: 5 cells at head that base-hostile did not have, all identical to base-ordinary (see F1).

**Q2 (rate limiter, real middleware):** 3 triggers × 17 classes = 51 cells.
- Base, for the 5 changed classes: the middleware REJECTS. On express 4 that means no answer and an unhandled rejection; the request is neither refused (no 429) nor let through.
- Head, for those classes: `next()` once (twice on the downstream trigger), the same as base-ordinary.
- Cells where base's outcome was "request refused": **0** (base never answered 429 for any hostile value). So head is more permissive than a base REFUSAL in 0 cells.
- I drove the Redis path for real through the module's `require('ioredis')`, using a `Module._load` stand-in whose `incr` rejects.

**Q3 (refreshConfigs, init, extractTenantContext, runMigrations):**
- 34 + 34 + 17 cells, and head = base-ordinary in all of them.
- **refreshConfigs / init:**
  - Base rejects for the 5 classes; head resolves.
  - A prior good load's `suspended` status survives a failed refresh at both trees, in 17/17 cells. So a failed refresh does not unlock a suspended tenant.
  - A failed FIRST load (init) leaves the status map empty at both trees, for every class including the ordinary Error.
  - The caller that now proceeds where base stopped is `refreshTenantConfigs` (originate `db.ts:280`) and `init()` (`db.ts:439`). Each proceeds exactly as it does for an ordinary Error.
- **extractTenantContext:** 503 at base and head in 34/34 cells. Base for the 5 classes set the status but threw before any body; head answers 503 `unreadable thrown value`.
- **runMigrations:** for 10 classes base rejected; head returns `errors=1` with `applied=0`, which rolls back and stops (002 is not applied). That is the same as base-ordinary.

**Q6 (sentinel):**
- Log lines carrying the sentinel: base 43, head 43.
- Response bodies carrying it: base 8, head 8.
- Cells where head prints more than base: **0**.
- Positive control: the ordinary Error prints the sentinel at both trees.

**Q7 (red first and suites):**
- The PR's 20 cells:
  - At base, 10 fail, **all 10 by AssertionError**, and 10 pass (the C1/C2 controls, which pass at base by design).
  - At head, 20/20 pass.
- My recorder confirms the same flips across 17 classes.
- Whole `packages/shared` suite, in a sparse clone of 68 files:
  - Base: 644 / 660 pass, 16 fail.
  - Head: 653 / 660 pass, 7 fail.
  - Of those 7 head failures, 6 are the same environment failures as base (repo-walk guards and the CIP-8 test in a sparse clone).
  - The 7th is `threadToken` "different policy IDs", which timed out at 30 s in the full run. Run alone at head it passes 15/15 (the KS-1155 load class).
  - The same 15 files fail to load at both trees; the sparse clone lacks the other workspaces.

**Mutants (PR 1990 files):** 16 mutants, 16 killed (raw table: `results/mutants.tsv`). One is the removal of the rate limiter's `next()` in the catch, which was killed.

---

# PR 1991: services/shared, ten catches (redis-security-store ×6, cache-middleware, redis-client connect, connection-pool ×2)

**Verdict PR 1991: `GO WITH NOTES — MERGE (no HOLD-FOR-KAM)`**

**Class bar: 0 of 336 non-ordinary head cells are more permissive than base-ordinary.**
- 316 of 336 equal base-ordinary.
- 102 cells changed from base to head, and all but 18 changed TO base-ordinary.
- Those 18 are the ConnectionPool callers in G175-F4, and they are LESS permissive (they fail where base resolved).
- The remaining 2 cells are pre-existing (null or undefined thrown into createConnection gives `Failed to create connection`, base = head).

## Findings (PR 1991)

### G175-F4 — LOW (latent): ConnectionPool's callers now fail on a value whose String() throws, because createConnection rethrows the original value
- **FOUND:**
  - **Base.** The catch's `String(error)` threw a NEW, readable error on the first attempt. That error left createConnection immediately (1 factory call, no retries) and the callers handled it.
  - **Head.** Head retries 3 times (= base-ordinary) and then throws the ORIGINAL unreadable value. That value now reaches two caller catches that are still unguarded:
    - `initialize()` line 87: `.catch(err => …String(err))`
    - `performMaintenance()` line 279: `String(error)`
  - **Effect, for 6 classes** (message getter throws, revoked Proxy, `Object.create(null)`, throwing get trap, throwing name getter, throwing toString):
    - `initialize()` REJECTS where base resolved: 6/16 cells.
    - `performMaintenance()` rejects: 6/16 cells.
    - On the REAL `setInterval` (startMaintenance), each class produced **3 unhandled rejections in a 70 ms window**: 18 in total, against 0 at base. Under Node's default, an unhandled rejection ends the process.
  - Base-ordinary resolves in all of these.
  - The same "rethrow the original" shape exists in `redisClient.connect` and `RedisCSRFStore.generate`. Their only in-repo caller, `getSecurityStores`, swallows without reading the value: 16/16 cells equal.
  - This is not more permissive. It is a new failure shape one level up.
  - **Reachability, read only:**
    - The only `ConnectionPool` in the repo is `dbPool`, whose factory is `createMockConnection`, and that cannot throw.
    - `git grep` found no non-test importer of `services/shared/src/cache`, `src/security` or `@secuura/service-utils` in any service. The control: the same grep finds billing's import of `services/shared/types/svs-types`.
- **TESTED:** the real ConnectionPool with a factory that throws each value. Not tested: any deployed consumer (none was found).
- **HOW:** `harness/p1991_pool.test.ts` Q5c/Q5d, using a `process.on('unhandledRejection')` counter.

## What passed (measured), PR 1991

**Q4 (the three stores: real module, a stand-in redis client throwing each value, 6 methods × 17 classes):**

| method | base, hostile value (6 classes) | head, hostile value | base-ordinary | allow / deny at head |
|---|---|---|---|---|
| RateLimit.get | THROWS (new Error/TypeError) | `null` | `null` | allow (fresh window) |
| RateLimit.increment | THROWS | `{count:1}` | `{count:1}` | allow |
| BruteForce.get | THROWS | `null` | `null` | no block |
| BruteForce.set | THROWS | resolves (not stored) | resolves | n/a |
| CSRF.generate | THROWS (new) | rethrows the ORIGINAL value | rethrows | no token (deny) |
| CSRF.validate | THROWS | `false` | `false` | **deny** |

- Head = base-ordinary in 96/96 cells.
- **Callers.** No caller of these stores exists outside the module at head; I read this with `git grep` over the repo. The module re-exports them, and the only users are the in-file methods. I drove those too:
  - `isBlocked`, with the stored record saying BLOCKED and `get` failing: `{blocked:false}` at base AND head in 16/16 cells. Base's throw was already turned into fail-open by `isBlocked`'s own catch, not into a refusal.
  - `getAttempts`: 0 at both.
  - `recordFailure` (get fails): `{attempts:1}` at both.
  - `recordFailure` (set fails): base returned `{attempts:1}` with no lock for 6 classes; head returns the lock record, the same as base-ordinary. Head is **less** permissive there.
  - `CSRF.refresh` (set fails): rejects at both trees.
- **Cells where a caller turned a base THROW into a REFUSAL, so that head's fail-open is more permissive: 0** (none was found in the repo, and none among the in-file callers).

**Q5 (cacheMiddleware, redisClient.connect, ConnectionPool):** head = base-ordinary in every cell except F4's 18 and the 2 pre-existing ones.
- cacheMiddleware: base rejected with no `next()`; head calls `next()`.
- connect: rethrows the original value.
- removeConnection: emits `connectionRemoved` (2 events at head vs 0 at base for the 6 classes).
- **O99-P1's `caught` rename:** createConnection at head equals base-ordinary in 14/16 non-ordinary cells. The other 2 (null, undefined) are base = head. The mutant `lastError = caught` → `new Error(error)` is KILLED, so the identity of the rethrown value is pinned by a test. Beyond the guard, the rename changes no behaviour I could measure.

**Q6 (sentinel):**
- Log lines carrying the sentinel: base 105, head 93.
- Cells where head prints more: **0**.
- Head prints less in 12 cells: base's callers logged the getter's or trap's own Error text.
- No response body carries the sentinel.

**Q7 (red first and suites):**
- The PR's 32 cells:
  - At base, 20 fail, **all 20 by AssertionError**, and 12 pass (the C1/C2 controls).
  - At head, 32/32 pass.
- Whole `services/shared` suite:
  - Base: 25 / 45 (20 failures = the RED cells; the 3 pre-existing files, 13 tests, pass).
  - Head: 45 / 45.

**Mutants (PR 1991 files):** 32 mutants, 31 killed. Survivor 1: `connection-pool.ts` `error: String(error) });` occurrence #2.
- This is **off-target**: it is line 279, inside performMaintenance, which the PR did not change. My substitution hit a second occurrence of the same text.
- It is not equivalent: it would throw a ReferenceError in that catch.
- It survives because no PR cell drives maintenance. This is the same gap that F4 measures.

## Mutants, both PRs (raw table: `results/mutants.tsv`; my count of the rows)

- **48 mutants: 47 KILLED, 1 SURVIVED** (the off-target one named above). The script's headline matches this count.
- Kinds of mutant:
  - G1: the inner catch rethrows (that is, the base behaviour), 15 mutants.
  - G2: the constant changed, 15.
  - G3: the use-line goes back to reading the raw value (or, for the rate limiter, `next()` is removed), 18.
- Control: before mutating each file, I ran that file's unmutated PR tests and they passed (rc 0) for all 9 files.

## NOT tested (both PRs)

- No real Azure Key Vault, Redis, Postgres, or booted service. No HTTP request, and no express `res.json` serialisation (see F2).
- No Node 24 / LTS; host Node is v26.8.1.
- Not run: tsc, eslint, the test-types ratchet, the four platform suites, or the pre-push hook.
- The whole-package suites ran in a **sparse** clone of `packages/shared` + `services/shared` + `services/auth` + `services/originate`, without the workspace-root install, so 15 packages/shared files fail to load at both trees. My suite ratios are base-vs-head on the same install, not the seat's full-checkout numbers (1447 / 1467).
- Reachability: I measured none of the "caller" or "production" statements beyond `git grep` reads. Deployed images may vendor `services/shared` some other way I did not see.
- The `Projects Documents/fragments/*.html` files (2 per PR) were not assessed.
- jwt.ts was driven through `initJwtKeys`/`getActiveJwk`. No token was signed or verified against a second service.

## Plain answer for Kam

These two changes stop a handful of shared error handlers from crashing on a strange kind of error, so they now behave exactly as they already did for a normal error. Nothing becomes more open than it already was for a normal failure. The sign-in key is still taken from the same place, though after one of these strange vault errors it is now remembered for up to five minutes, just as it already is after a normal vault error. The rate limits stay open when their store fails, and the CSRF check still refuses. One small new wrinkle: a database-pool helper that nothing in the product uses today could now stop with an error instead of carrying on. It is worth fixing in the next KS-1868 batch, but it does not block either merge.

---
Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate175-ks1868-pr1990-pr1991/`. Tracked: `verdict.md`, `harness/`, `scripts/`, `results/`, `runs/`. Ignored (`.gitignore`): `repo/`, `scratch/`, `home/`, `tmp/`, `mut/`. Background processes: 3 started (the packages/shared head suite, the packages/shared base suite, and the mutant run), all exited on their own before this report; `ps` shows no vitest or gate175 process. Nothing was written outside the workdir. The checkout was used with read verbs only (`ls-remote`, `show`, `config` read, `remote get-url`, `hash-object` without `-w`), plus `git clone --shared` from it.

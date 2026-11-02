# QA Gate 139 verdict: Secuura/Distributed_Secuura PR 1956 (KS-1868, pool 'error' listener in four db.ts + ready-hook catch in two), TIER 2, round 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** Every number the author claims re-measures. The change does what it says and nothing else: 4 `db.ts` files, +16/-2 (analytics, api-gateway) and +8/-1 (anchoring, kyc), the same 8-line guard at all six sites. I ran the real `db.ts` of each service (base and head) in a real child process with only `pg`'s `Pool` replaced by an EventEmitter stand-in, 12 thrown values x 6 sites x 2 versions = 192 runs (logs/probe_matrix.jsonl, logs/probe_table.log). For an unreadable value, head equals what an ORDINARY Error already gets (one logged line, process lives, `initDb` resolves). Base differed: pool listener threw out of the emitter (uncaught exception), a hook failure made `initDb` reject (boot) or raised an unhandled rejection (retry timer). 54 of 66 mutants killed; the 12 survivors are two named branches (null/undefined error, null message) that the PR's fragment claims behaviour for but no cell pins (G139-F1).
Not measured on Node 24 (host Node v26.8.1 throughout).

## Heads
- START (logs/head_start.log, 2026-11-02T17:13:35Z): PR head `a85e03f6f7dcf32476705cc12959a1bfbfd74ca9` (matches the author's), develop `2d3b3bb3d3865689e3cad843f9ebb90a2f606960` (matches Wednesday's). Merge-base `157a41fb7c9493ef276ea3fa01a70c2130979221` (one commit).
- END (logs/head_end.log, 17:35:18Z): PR head and develop both unchanged; clone HEAD = `a85e03f6`; `git status` clean (every probe/mutant scratch file moved to logs/_quarantine or restored by sha256).
- **PR body not read** (no `gh` login reachable). I used the author's READY mail (evidence/batch_20261102T171139Z.txt, section "Seat R 75th") and the two fragments in the diff. Wording in the live body that I could not see is not verified.

## 1. Diffstat (logs/diffstat.log)
10 files, +611/-6, exactly as declared (numstat: product 16/2, 8/1, 16/2, 8/1; tests 144, 108, 153, 108; fragments 24 + 26). Nothing outside the declared paths. Product files changed: only the four `src/db.ts`.

## 2. The hunks
Pool listener (4 services), `-` `dbLog('error', 'DB pool unexpected error', { error: err.message });`
`+` `let reason: string | null | undefined; try { const m = err?.message; reason = m === undefined || m === null ? m : String(m); } catch { reason = 'unreadable thrown value'; } dbLog('error', 'DB pool unexpected error', { error: reason });`
Ready-hook catch (analytics, api-gateway): same guard around `err?.message` (was `{ error: err?.message }`); the log message `DB ready boot work failed` and level are unchanged.
Does NOT change: log message text, level, other keys, `probeDb` (its `error: err?.message` at db.ts:98/121/126 is still unguarded in all four: G139-F4), `initDb`'s return, `dbAvailable`. Differences from the guard already on develop (admin.ts, 8151e756: `reason = String(err.message)`): this guard keeps undefined/null as-is (the `error` key is dropped from the JSON line by `JSON.stringify`, or serialises `null`) where the siblings print the string "undefined"/"null". Deliberate, preserves old log shape (G139-F6).
Subtle side effect: `err.message` became `err?.message` in the POOL listener, so a null/undefined emitted value no longer throws (base threw TypeError, measured below).

## 3. The behaviour question (Q1, Q2). RUN, not read: real db.ts via tsx child per case; `pg` Pool replaced by an EventEmitter with a trivial `query`; real `dbLog`. The 'uncaught'/'unhandled' columns come from `process.on` handlers in the probe child.
Values: ordinary Error, revoked Proxy, Error with throwing `message` getter, message 42, message undefined (object without message), message null, message Symbol, message object whose toString throws, message object with toString 'custom-string', null, undefined, plain string. Cases in the log: logs/probe_table.log (96 comparisons: 40 SAME, 56 DIFF; every DIFF is listed there). Positive control: ordinary and plain-string rows are SAME at every site and show a log line (`error: "boom"`).

### Pool 'error' listener (all four services identical; api-gateway shown, analytics/anchoring/kyc rows equal in logs/probe_table.log)
| emitted value | base | head |
|---|---|---|
| ordinary Error | 1 line `error:"boom"`, no throw | same |
| plain string | 1 line, `error` key absent, no throw | same |
| revoked Proxy | **listener throws TypeError out of emit = uncaughtException**, no line | 1 line `error:"unreadable thrown value"`, no throw |
| Error whose message getter throws | **uncaughtException** (Error: getter boom) | 1 line `"unreadable thrown value"` |
| null / undefined (the emitted value itself) | **uncaughtException** TypeError "Cannot read properties of null" | 1 line, `error` key absent |
| message 42 | `error: 42` (number) | `error: "42"` (string) |
| message Symbol | key absent (JSON drops symbol) | `"Symbol(s)"` |
| message object, toString throws | `error: {}` | `"unreadable thrown value"` |
| message object, toString returns text | `error: {}` | `"custom-string"` |
| message undefined | key absent | key absent (UNCHANGED) |
| message null | `error: null` | `error: null` (UNCHANGED) |
State flag: the listener never sets `dbAvailable`; `isDbAvailable()` is the same at base and head for every value (false here, the pool was never probed). Process outcome in production, by service: **api-gateway** installs `process.on('uncaughtException')` (index.ts:1193) which logs and runs `gracefulShutdown('uncaughtException')`, so at base the gateway shut itself down. **analytics, anchoring, kyc** install no handler (git grep over their src, non-test, 0 hits; positive control: the same grep finds api-gateway/src/index.ts), so Node's default applies and the process dies. At head none of the four stops. Reachability: a real pg idle-client error is an `Error` whose message is a data property, so an unreadable value here needs a pg defect or monkeypatch; this is defence in depth like every other KS-1868 site.

### Ready-hook catch (analytics, api-gateway only; anchoring and kyc have no hook: git grep `runDbReadyHook|onDbReady` = 0 hits in both db.ts, 7 in each of the other two)
Two paths reach `runDbReadyHook`: boot (`initDb`, probe ok) and the retry timer (`scheduleRetry`, probe ok after a boot race). The author's note covers boot only; I ran both.
| hook failure value | boot, base | boot, head | retry timer, base | retry timer, head |
|---|---|---|---|---|
| ordinary Error | `initDb` resolves true, 1 line | same | 1 line, no rejection | same |
| revoked Proxy | **`initDb` REJECTS (TypeError)**, no line | resolves true, 1 line `"unreadable thrown value"` | **unhandledRejection** (TypeError), no line | 1 line, no rejection |
| message getter throws | **initDb REJECTS** | resolves true, 1 line | **unhandledRejection** | 1 line |
| message 42 / Symbol / toString throws | resolves true; `42` / key absent / `{}` | resolves true; `"42"` / `"Symbol(s)"` / `"unreadable thrown value"` | same shape | same shape |
| message undefined / null, null / undefined thrown, string | UNCHANGED (SAME) | | UNCHANGED | |
State flag: `isDbAvailable()` is true in every hook cell at both versions (the probe set it before the hook ran); the hook's outcome never changes it (consistent with the code comment "Boot work failing must not un-flag an otherwise reachable DB").
Callers (git grep `initDb(` over services src, non-test, then read each):
- **api-gateway** `startServer()` (index.ts:1234-1237) `await initDb(runDbBootTasks)`; called at :1293 `startServer().catch(... log('error','Failed to start server') ; process.exit(1))`. Base + unreadable hook value: `initDb` rejects, the gateway logs and exits 1 at boot. Head: it logs the DB line and continues to listen, as for an ordinary Error. Retry-timer path: the gateway runs `UNHANDLED_REJECTION_MODE=survive` (docker-compose.yml:441, services.bicep:637), so base logged and survived; head logs the proper line.
- **analytics** `initDb(loadStoresFromDb).then(...)` (index.ts:118), no `.catch`, no process handler: base boot = unhandled rejection, Node default ends the process; retry-timer path the same. Head: logged, `[Analytics] DB init: true`.
- **anchoring** `await initDb()` in `startup()` (index.ts:2384) and **kyc** `initDb().then(async ...)` (index.ts:1292): no hook, so only the pool listener changes for them (above).
Moves only toward what an ordinary Error already does: the unreadable-value after-state equals the ordinary-Error state at every site. **Raise accepted.**

### Q2 (undefined / null / 42), measured
- `message` undefined: base == head (key absent). `message` null: base == head (`error: null`). Thrown `null`/`undefined` value at the HOOK: SAME (the old `err?.message` already tolerated it); at the POOL listener it is not unchanged: base threw (uncaught), head logs a line without `error`. The author's wording ("undefined and null messages are UNCHANGED") is true for messages; the listener null/undefined-VALUE row is a fix, not unchanged (the fragment says so correctly).
- Readable non-string `message` 42: base logs the number `42`, head logs the string `"42"` (type change in the `error` field; Symbol: absent -> string). Both confirmed in all six sites.

## 4. Re-measure
- Red first (new files only, base product = develop `157a41fb` db.ts; logs/red_base_new_<svc>.log): analytics **5 failed | 4 passed (9)**, api-gateway **5|4 (9)**, kyc **3|2 (5)**, anchoring **3|2 (5)**. Every failure an `AssertionError`, 0 timeouts, 0 TypeError crashes. Failed cells R1-R5 (R1-R3 for kyc/anchoring); controls pass.
- Green at head, new files: 9/9, 9/9, 5/5, 5/5 within the whole-suite runs.
- Whole suites (each base figure = product at base with the new file moved out; head = PR): analytics 18 files/108 -> 19/117 (head log head_whole_analytics_run2.log: 117 passed rc 0); api-gateway 138/1412 -> 139/1421, all pass; kyc 14/79 -> 15/84, all pass; anchoring base 55 files 759 pass + 1 fail of 760 -> head 56 files 764 pass + 1 fail of 765. **The one anchoring failure is `threadTokenMint.test.ts > ... parameterises mint + spend with a deterministic per-seed policyId` at BASE (157a41fb) and at head: same cell, red without the PR (KS-562)**; base + new files = 4 failed (3 new reds + that one). Red on CURRENT develop `2d3b3bb3` not run (only base measured).
- **First head analytics whole run FAILED 1 cell by TIMEOUT** (logs/head_whole_analytics.log: new file's first cell C1 "Test timed out in 5000ms", took 18.5 s; host load1 about 16, cold import after `vi.resetModules()`); the re-run at load 12-16 passed 117/117 (run2). Not reproduced, not an assertion failure (G139-F5).
- tsc with the tests in the program (ad hoc `tsconfig.gate.json` per service extending its tsconfig, include `src/**/*`, removed afterwards; logs/tsc_head_<svc>.log): anchoring 0, kyc 0, api-gateway 27, analytics **2**. Base analytics 1 (the author's figure; the two extra TS2835 are `db.retry.test.ts(36,17)` and the new `ks1868-analytics-...test.ts(50,17)`, both `Relative import paths need explicit file extensions ... '../db.js'` for `return import('../db')`). api-gateway: the repo's ratchet leg `check.cjs services/api-gateway` rc 0: "27 errors: 27 in the baseline, 0 new". The default-list leg `test-types-ratchet.sh` rc 0: "OK - 5 service(s)". I did not rerun base tsc for the other three (the author's 0/0, 0/0, 27/27 agree with head; the PR adds no new error in them).
- eslint (cwd = service; db.ts + new test, logs/eslint_<svc>.log): 0 problems rc 0 in all four. Planted file (`no-debugger` + unused var): rc 1 in all four.
- docs-fragments `check` (logs/frag_check_clean.log): rc 0, "lint clean, render passes" with 105 new. It prints a cheat ADVISORY at committed line 6235 (the same advisory gate 90 saw on develop as G90-F7; not re-attributed on today's develop here). Planted defects: flow unclosed `<div>` rc 1, flow `<!--n-->.` removed rc 1, cheat unclosed `<div>` rc 1, cheat `</table>` corrupted rc 1; all four restored by sha, rc 0 after.

## 5. Mutants (scripts/mutants.py; ONE site per run in the product file only, tests untouched, sha256-restored and verified after every run: all `restore True`; the new test file of that service only; logs/mut_<svc><k>__<M>.log, table logs/mutants_table.log)
66 runs (11 mutants x 6 sites: analytics pool/hook, api-gateway pool/hook, anchoring pool, kyc pool): **54 killed, 12 survived.** Every kill was an `AssertionError`, 0 timeouts.
| mutant | all 6 sites |
|---|---|
| M0 revert to the unguarded read | KILLED (R cells) |
| M1 inner try dropped (`if (true) {` ... `} else {`) | KILLED |
| M2 constant text -> 'x' | KILLED |
| M3 `String(m)` -> `m` | KILLED (Symbol cells) |
| **M4 `err?.message` -> `err.message`** | **SURVIVED at all 6** |
| M5 `String(m)` for every message (undefined -> "undefined") | KILLED (C2/C4) |
| **M6 null message -> `"null"`** | **SURVIVED at all 6** |
| M7 undefined message -> text | KILLED |
| M8 constant for every value | KILLED |
| M9 the catch rethrows | KILLED |
| M10 log drops the `error` field | KILLED |
M4 and M6 are the two behaviours the PR text asserts but no cell reaches: a thrown/emitted null or undefined value (the listener fix above) and a null message (G139-F1).

## 6. merge-tree onto current develop `2d3b3bb3` (logs/merge_tree.log)
rc 0, tree `4eee067f7d3ed6949b6745b2595e9a41f53d7ad1`, clean. Two commits since the base (`8151e756` api-gateway admin.ts, `2d3b3bb3` anchoring index.ts + originate anchors.ts, KS-1868 message coercion): 13 paths, **0 shared with the PR's 10** (positive control: the develop path list against itself = 13). The merged tree differs from develop in exactly the PR's 10 paths (diff of path lists empty). Neither develop commit touches a `db.ts`. I did NOT re-run docs-fragments or the suites on the merged tree.

## 7. Kam's ks1346 rule (log type and field NAMES of a thrown object, never values). Q4
No new log LINE is added: the two existing messages keep text, level and keys; only the value of `error` changes. Per site:
- The constant `'unreadable thrown value'` is a type statement: compliant.
- A readable message is still logged, as before (`err.message` was already logged in these exact lines). That is the pre-existing practice and the same one accepted at the sibling KS-1868 sites; it is not a regression, but it is a value, not a field name.
- New: `String(m)` on a readable NON-string `message` stringifies a value. If `m` is an object with a custom `toString`, head logs what that method returns (`"custom-string"` in the probe). Base logged `JSON.stringify` of the object (`{}` for an object with no own enumerable fields; own fields would have been logged in full), so head is no wider; a throwing `toString` falls to the constant. pg errors do not produce object messages.
Verdict on Q4: **compliant for the new/changed lines relative to the existing pattern; info only** (G139-F3). No stack, no whole-object, no secret field is introduced.

## 8. Notes for the PR body
- **G139-F1 (recommended, test gap, measured)** Mutants M4 (`err?.message` -> `err.message`) and M6 (null message -> `"null"`) survive at all six sites. The fragment states "a `null` or `undefined` error threw at base and are logged at head" and "an undefined or null message ... byte-identical", yet no committed cell emits a null/undefined VALUE or a null message. One cell per service pair (emit `null` to the listener; `withMessage(null)`) would close both. Not a merge block: both branches are behaviour the old code also had or was fixed here, and the probe (logs/probe_table.log) shows them correct.
- **G139-F2 (INFO, the fragment omits a path, measured)** The fragment and mail describe the hook failure's effect at boot only. The same unreadable value also ran through the retry-timer path (scheduleRetry) at base as an **unhandled rejection** inside the timer callback (analytics: process ends; gateway: logged and survives under `survive` mode); head logs one line. Worth one sentence in the body (the head behaviour is the intended one).
- **G139-F3 (INFO, Q4)** ks1346: no new line; `String(m)` widens the value that is logged only for non-string `message`, and does so no more than the previous raw `JSON.stringify` did. See section 7.
- **G139-F4 (INFO, follow-up, read from source, not run)** `probeDb`'s catch `return { ok: false, error: err?.message }` is still an unguarded read in all four files (db.ts:98 anchoring/kyc, :121 analytics, :126 api-gateway). A rejection from the probe query that is a revoked Proxy or throwing getter would throw out of `probeDb`: in `initDb` that rejects boot; inside `scheduleRetry`'s async timer callback it is an unhandled rejection and the retry chain stops (the next `scheduleRetry()` is never reached). The author named this as untouched; it is a KS-1868 site-list follow-up, not this PR.
- **G139-F5 (INFO, flake risk, measured once)** The new analytics C1 cell timed out at the 5 s default once under host load 16 (cold `vi.resetModules()` + dynamic import of a module that loads `@secuura/shared`); the re-run was green. Each of the four new files imports the module in every cell with the same pattern; a slow CI runner could meet the same wall. Not reproduced; not a reason to hold.
- **G139-F6 (INFO, style)** The guard differs from the one now on develop for admin.ts (`reason = String(err.message)`): this one preserves undefined/null as absent/null. Intentional and tested at C2/C4; say so in the body so a reader of both does not think one is wrong.
- **G139-F7 (INFO, Q3 answer, measured)** The extra TS2835 in analytics: count **1 -> 2** confirmed (`db.retry.test.ts(36,17)` existing; new `ks1868-analytics-db-pool-error-and-ready-hook-unreadable-throw.test.ts(50,17)`, both `return import('../db')`). **No gate leg refuses it:** `test-types-ratchet.sh`'s default list is `services/auth services/api-gateway services/vc-issuer services/security services/m365-integration` (read at the script head, line 49; run: rc 0); analytics has no `tsconfig.test.json` and no baseline (`check.cjs services/analytics` exits 2 "no tsconfig.test.json"); analytics' own `tsconfig.json` excludes `src/__tests__`, so `npm run build` / CI `npm run build` never examines the file; preflight.sh and .githooks/pre-push name no analytics path (git grep 0). CI lint (`eslint src`) is clean (eslint 0). Class: **INFO now; recommended follow-up** to give analytics (and kyc, anchoring) a `tsconfig.test.json` plus baseline so the ratchet covers them. Not FIX-BEFORE-MERGE (no leg refuses it) and Wednesday's ruling "ship as held, no edit" stands. If Kam ever wants it gone the one-line fix is `import('../db.js')` in both analytics files, which would also drop the existing one.

## 9. NOT TESTED
The live PR body; a real Postgres or pg client (the `pg` Pool is a stand-in, so a real pool 'error' emission path from an idle client is read from pg-pool's contract, not run); a booted service (the gateway `process.on('uncaughtException')` and `startServer().catch` are read, not executed); the analytics/anchoring/kyc process death on an uncaught exception is Node's default, not run to exit; BigInt and cyclic-object messages (the author's claims, not re-run); `probeDb` unguarded read (G139-F4, read only); the suites and fragments on the merged tree; the threadTokenMint cell on current develop; the 4 platform suites; CI; the pre-push hook legs other than the ratchet leg; Node 24; Spark shadow review (not requested).

## Processes
All background runs I started (npm ci, probe matrix, suites, mutants) have finished; ps shows only another seat's vitest/run-shell-suites (worktree s-w19-auth-events-bus), none mine.

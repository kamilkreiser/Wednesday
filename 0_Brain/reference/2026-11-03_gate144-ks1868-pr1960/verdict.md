# QA Gate 144 verdict: Secuura/Distributed_Secuura PR 1960 (KS-1868, api-gateway redis.ts 'error' listener + initRedis catch), TIER 1, round 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge. No security control newly fails open because of THIS PR.**
Every figure the author gives re-measures (suite 142/1462 -> 143/1471, red first 6 of 9 by assertion, tsc ratchet 27/0/0, eslint 2 warnings both on the unpatched file). I ran the real `redis.ts`, `middleware/security.ts`, `middleware/rateLimitEnforce.ts`, `services/enforcement.ts` and the real winston logger, base and head, in a child process with only `ioredis` replaced by an EventEmitter stand-in that serves ONE shared store to two "replicas" (two fresh module graphs), or rejects every command when "down". For an unreadable value the head's after-state equals what an ORDINARY Error already gets at all three sites (listener, dev/test catch, production catch), in every cell.
**The flag being false is a degraded mode with real fail-open behaviour, but all of it is PRE-EXISTING**: an ordinary Error, a socket `close`, or the 4th retry already put every replica in it. The most serious one is not in the author's list: with the flag false, **document-type enforcement passes every rule (MFA, verification level, isActive, auth providers, metadata schema, approval gate) because the type catalogue reads empty** (measured, G144-F1). Recommended high-priority follow-up, not a merge block.
Host Node v26.8.1 throughout; nothing measured on Node 24.

## Heads
- START (logs/head_start.log, 18:42:46Z): PR head `5b08a162249e08c1728894c849d88f8611647b3f` (= the commission's pin and the author's), develop `0bd5e7bf62ac`. Merge-base `2d3b3bb3d386`; one commit on it.
- END (logs/head_end.log, 19:02:37Z): PR head **unchanged**. **develop moved during the gate** to `4d1ab2cb6574` (two more KS-1868 squashes, 35d23ac6 anchoring + 4d1ab2cb auth; 11 paths, none in api-gateway, none a PR path). Merge-tree redone onto it (section 6). Clone HEAD `5b08a162`, `git status` clean; product file sha256-restored after every swap (logs/suites_restore.log, static_restore.log, mutants restore=True x27). Base copies and the planted lint file sit in logs/_quarantine.
- **PR body not read** (no `gh` login in this seat); I used the author's READY mail (evidence/w19_pr1960_ready.txt) and the two fragments in the diff.

## 1. Diffstat (logs/diffstat.log, three-dot vs merge-base)
4 files, **+201/-4**, exactly as declared: `services/api-gateway/src/services/redis.ts` 18/4, new test 154/0, flow fragment 11, cheat fragment 18. Nothing outside the declared paths.

## 2. The hunks
- Listener: `-  logger.error('[Redis] Connection error', { error: err.message });` -> `+ let reason; try { const m = err?.message; reason = m === undefined || m === null ? m : String(m); } catch { reason = 'unreadable thrown value'; } logger.error('[Redis] Connection error', { error: reason });` followed by the UNCHANGED `isConnected = false;`.
- initRedis catch: the same guard on `(error as Error)?.message`, then the three existing uses (`FATAL` log `error:`, `throw new Error('REDIS_REQUIRED_IN_PRODUCTION: ' + reason)`, the dev/test `warn` `error:`) read `reason`.
Does NOT change: the production branch (still throws), `fallbackMode`/`return false` in dev/test, the `connect`/`close` listeners, `retryStrategy`, `isRedisAvailable()`, any get/set/delete, log messages, levels or keys. The commission's statement that the PR "changes a security-relevant FLAG's value" is right in effect: the flag is written by the same unchanged line, which the listener now reaches for every value.

## 3. Behaviour, and the four TIER 1 questions
Harness: scripts/probe_child.ts (modes `site`, `family`, `enforce`), scripts/probe_matrix{,2,3}.sh; results logs/probe_site*.jsonl and the tables logs/probe_site_table.log, probe_site2_table.log, probe_site3_table.log, probe_family_table.log. 11 values: ordinary Error, revoked Proxy, message getter throws, message 42, message null, object without message, Symbol message, message whose toString throws, null, undefined, plain string. 172 child runs, all rc 0, stderr empty, no harness error.

### Per site, base vs head (RUN)
| value | listener base | listener head | dev/test connect base | head | production connect base | head |
|---|---|---|---|---|---|---|
| ordinary Error | no throw, flag true->false, `error:"boom"` | SAME | resolves false, warn `boom` | SAME | rejects `REDIS_REQUIRED_IN_PRODUCTION: boom` | SAME |
| revoked Proxy | **listener throws, flag stays TRUE, no line** | no throw, flag ->false, `"unreadable thrown value"` | **rejects TypeError** | false + warn constant | **rejects TypeError** (not the named error), no FATAL line | rejects `REDIS_REQUIRED_IN_PRODUCTION: unreadable thrown value`, FATAL line |
| getter throws | **throws, flag TRUE** | ->false, constant | **rejects with getter's Error** | false | **rejects getter's Error** | named error |
| null / undefined value | **throws TypeError, flag TRUE** | ->false, `error` absent | **rejects TypeError** | false | **rejects TypeError** | `...: undefined` |
| message 42 | `error: 42` (number) | `"42"` | same shape | | `...: 42` | SAME text |
| Symbol message | flag ->false, key absent | `"Symbol(s)"` | | | **rejects TypeError (Symbol concatenation)** | `...: Symbol(s)` |
| message toString throws | `error: {}` | constant | | | **rejects with toString's Error** | named error |
| message null / object without message / plain string | SAME | | SAME | | SAME (`null` / `undefined` / `undefined`) | |
Listener emitted from an async callback, as ioredis does (`listener_async`, probe_site3_table.log): base = **uncaughtException** for revoked Proxy, getter, null, undefined; head = none, line logged, flag false.
Production json format (the author's NOT-run item): measured here, the real logger in production mode writes `{"error":"unreadable thrown value","level":"error","message":"[Redis] FATAL: ..."}`; the logger's File transports wrote to logs/child_cwd/logs (the probe chdir'd there).

### Q1: every reader of the flag, by family; flag false with Redis down vs up (READ for all, RUN where marked)
`isRedisAvailable()` occurs **41 times in redis.ts = its definition (line 144) + 40 call sites** (the author's "41 uses" counts the definition as a use; logs/inredis_uses.tsv). Outside redis.ts there are **two** direct readers (logs/flag_readers_all.log): routes/verification.ts:795 (connector create: 503 when false) and services/health.ts:54 (`/api/connector/info`: 503 when exactly false). Both FAIL CLOSED: confirmed by read. Indirect readers = every caller of a redis.ts function (logs/redisService_uses.log: index.ts 6, security.ts 4, admin.ts 43, proxy.ts 4, verification.ts 20, enforcement.ts 5, health.ts 3; system-status.ts via getRedisHealth). Not flag readers at all: rateLimitEnforce (reads `client.status === 'ready'`), auth.ts session check (`isSessionActive(…, getRedisClient())`), health.ts:204 ping, graceful shutdown, and the express-rate-limit limiters (global, verification, login, register, MFA… all use the default per-replica MemoryStore regardless of Redis).

Two-replica runs, one shared Redis (logs/probe_family_table.log, probe_site3_table.log enforce block). "stuck TRUE + down" is base's state after an unreadable value IF the process survived (see Q2); "false" is head's state after it AND both versions' state after an ordinary Error.
| family (call sites) | product callers | flag false, Redis up or down | flag stuck TRUE, Redis down | security effect |
|---|---|---|---|---|
| brute force get/set/delete (3) RUN | security.ts bruteForceProtection on /auth/login | lockout planted in Redis is invisible, middleware **ALLOWS** (next) on both replicas; a lockout written on A after the trigger is not seen by B | get rejects, middleware's catch **ALLOWS** ("fail open for availability", security.ts:196) | fail open in both states; base-stuck-true is no stronger. **And it never arms**: nothing calls `recordFailure` (git grep; docs/openapi/WORKFLOWS.md:238, KS-1372), so the gateway lockout is inert in production either way |
| rate limit get/set (2) RUN | **none** (zero product callers; dead code) | counter per-replica (B sees null) | rejects | none in production. The real limiters: machine limiter RUN = flag-independent (Redis counter when `status==='ready'`, per-replica memory otherwise, A/A/B gave next/429/429 up and next/429/next down in every flag state); express-rate-limit = per-replica MemoryStore always |
| document signatures (2) RUN | set: index.ts:193 boot back-fill; get: **no product caller** | A sees its in-memory copy, B null | set catches; get catches and falls to memory (same as false) | none reachable; equal |
| rejected documents (2) RUN | verification.ts:997 status lookup, then memRejectedDocuments, then **Postgres** | per-replica memory, then DB | catches, falls to memory, then DB (same) | DB is the source of truth; equal |
| workflow-doc mapping (2) | verification.ts:437, index.ts:179 | memory | catches, memory (same) | equal |
| notification settings / platform-settings (2) RUN | verification.ts:795/800 + 874, health.ts:54/64, admin.ts 1156/1181/1191/1565 | **null** (resolves); the two allow-list reads are behind the 503 guard; verification.ts:874 (workflow bypass) reads `{}` and therefore does NOT bypass (fail closed); admin save writes to one replica's memory | get rejects; callers' try/catch | allow-list FAIL CLOSED (503); bypass fail closed |
| **document types (4) RUN** | enforcement.ts:78/128 (`enforceDocumentTypeRules`, verification.ts:856), admin CRUD/seed, index.ts:944 public list | catalogue reads EMPTY on every replica -> `resolveDocumentType` null, `registered.length === 0` -> **`{ ok: true, docType: {} }`**: a type registered with `requireMFA` is **ALLOWED** for a user without MFA on both replicas, Redis up or down (base AND head after an ordinary Error; head after an unreadable value) | `keys()` rejects -> enforcement rejects (500 path) | **FAIL OPEN, pre-existing: G144-F1.** By read, the same pass-through skips `isActive`, `creatorVerificationLevel`, `allowedAuthProviders`, `metadataSchema`, and `createWorkflowInstanceIfRequired` sees no `requiresApproval`, so no approval workflow |
| workflow instances (3), pending documents (3), workflows (4) | verification.ts approve/reject, enforcement.ts:222/249/251, proxy.ts | per-replica memory: an approval/pending doc created on A is invisible on B | reject | availability/consistency, not an open door (a missing instance 404s) |
| integrations (4), verification policies (4), privacy (2), trusted verifiers (2, no product caller) | admin.ts config CRUD | per-replica memory, admin edits land on one replica | reject | configuration consistency; privacy settings read null on other replicas (defaults) |
| getRedisHealth (1) RUN | system-status.ts:438 | `fallback / in-memory` | ping rejects -> `error / redis` | reporting only |

### Q2: is head's unreadable-value after-state equal to an ordinary Error's? YES, at every site and every family cell
Family runs: `head revokedProxy` and `head getterThrows` rows are identical to `base ordinary` and `head ordinary` rows, field for field, Redis up and down (probe_family_table.log; enforce block). So **every fail-open in the Q1 table under "flag false" is PRE-EXISTING**: an ordinary Error already clears the flag. Further, independent of the listener, the flag also goes false on the unchanged `close` listener (ioredis `closeHandler` -> `setStatus('close')` -> emit, read in node_modules/ioredis 5.11.1 built/redis/event_handler.js:160) and on `fallbackMode = true` at the 4th retry (redis.ts:78). So base's "stuck TRUE while Redis is down" is not a state a real outage stays in: a real socket error is followed by `close`, which clears the flag at base too.
**Does the PR make the fail-open newly reachable?** No, for three reasons: (a) the state is reached at base by every real outage (ordinary Error, close, retry 4); (b) at base an unreadable listener value does not leave a SERVING gateway with the flag true: the throw escapes ioredis' socket callback (RUN: uncaughtException in listener_async), and the gateway's handler (index.ts:1193, READ, not run) logs and calls `gracefulShutdown`, which closes the server and exits; head keeps serving in the ordinary degraded mode instead; (c) ioredis emits Error instances from the socket, so no real source of a revoked Proxy / throwing getter at this listener is known (not measured). The one measured cell where base looks "stronger" (Redis UP, unreadable value, base flag stays true so the planted lockout and the MFA rule still hold) exists only in the harness where the throw is caught; in the gateway that throw ends the process. Classified as follow-up (G144-F1, F2), not a merge block.

### Q3: production initRedis stays fail-closed (RUN + READ)
RUN (probe_site2_table.log, connect_prod): **base rejects 11/11 and head rejects 11/11**; base rejects with the named `REDIS_REQUIRED_IN_PRODUCTION` error in 5/11 (ordinary, 42, null message, no message, plain string) and with a TypeError/foreign Error in 6/11; head with the named error in **11/11**. `initRedis` never resolves in production at either version; the flag is false after every production cell. Mutant M13 (production branch returns false) is killed by C2 and R2.
READ: `initRedis` has exactly one caller, `startServer()` at index.ts:1235 (git grep `initRedis(` over src non-test: 1 hit); `startServer()` is called only at index.ts:1293 under `require.main === module`, with `.catch((error) => { log('error', 'Failed to start server', { error: error.message }); process.exit(1); })`. Both confirmed at head and on develop `0bd5e7bf` (the zod squash added one import line at the top of index.ts; line numbers unchanged around 1235/1293).

### Q4: Kam's ks1346 logging rule: section 7.

## 4. Re-measure
- **Red first** (new file only, product at `2d3b3bb3`; logs/red_base_new.log): **6 failed | 3 passed (9)**, R1-R6, 6 `AssertionError`s, 0 timeouts; C1-C3 pass. As claimed.
- **Whole api-gateway suite** (`vitest run --root <clone>/services/api-gateway`): base without the new file **142 files / 1462 passed, rc 0** (logs/base_whole_excl_new.log); head **143 / 1471 passed, rc 0** (logs/head_whole_rerun.log, maxWorkers 2). +1 file, +9 cells, nothing else moved. As claimed.
  - Load flake, not the PR: my first head whole run (maxWorkers 4, logs/head_whole.log) had 1 failure, `ks1543-document-types-catch-logs-the-error.test.ts` C7 "Test timed out in 60000ms" (an in-test ESLint run); the same file hit a 10 s `beforeAll` hook timeout in base+new whole (logs/base_plus_new_whole.log) and again run alone at head cold (logs/head_ks1543_alone.log); it passed inside the head rerun. Present at base and head, timing only (G144-F6).
- **tsc with tests** (`tsc -p services/api-gateway/tsconfig.test.json`): head **27** errors, base 27, **identical sets**, none in a PR file (logs/tsc_tests_{head,base}.log). `check.cjs services/api-gateway`: "179 files, 143 under __tests__; 27 errors: 27 in the baseline, 0 new; 0 stale", rc 0 (logs/ratchet_head.log). Service tsconfig `--noEmit`: 0 errors.
- **eslint** (redis.ts + new test, api-gateway cwd): **2 warnings, 0 errors** at head (133 `preserve-caught-error`, 745 unused `error`); base redis.ts the same 2 at 119/731. Author's claim holds. Planted `debugger`/unused file: rc 1 (logs/eslint_*.log).
- **docs-fragments `check`**: rc 0, "lint clean, render passes" (107 new), with the same pre-existing cheat ADVISORY at line 6235 earlier gates saw. Planted: flow unclosed div rc 1, flow `<!--n-->.` removed rc 1, cheat unclosed div rc 1, cheat `</table>` corrupted rc 1; each restored by sha256; rc 0 after (logs/frag_*).

## 5. Mutants (scripts/mutants.py; product only, new test file, sha256-restored and verified after every run; logs/mutants_table.log)
27 runs: **19 killed, 8 survived**, 0 timeouts, every kill an AssertionError.
| mutant | listener (site 0) | catch (site 1) |
|---|---|---|
| M0 revert to unguarded read | KILLED R4 R5 R6 | KILLED R1 R2 R3 |
| M1 inner try dropped / M2 constant text / M9 catch rethrows | KILLED (R4 R5) | KILLED (R1 R2) |
| M3 no `String()` | KILLED R6 | KILLED R3 |
| M8 always constant | KILLED C3 R6 | KILLED C1 C2 R3 |
| M10 log drops `error` (listener / prod FATAL / dev warn) | KILLED | KILLED / KILLED |
| M11 `isConnected = false` removed | KILLED C3 R4 R5 R6 | |
| **M12 flag cleared only when the read succeeds** (the base bug, re-shaped) | **KILLED R4 R5** | |
| **M13 production branch fails open (`return false`)** | | **KILLED C2 R2** |
| M14 production throw uses the constant | | KILLED C2 |
| **M4 `?.` -> `.`** | **SURVIVED** | **SURVIVED** |
| **M5 `String` for all (undefined -> "undefined")** | **SURVIVED** | **SURVIVED** |
| **M6 null message -> text** | **SURVIVED** | **SURVIVED** |
| **M7 undefined message -> text** | **SURVIVED** | **SURVIVED** |
The flag and fail-closed guards are pinned. The survivors are the G139-F1/G141-F1 gap again: no cell emits a null/undefined VALUE (base threw, head logs without `error`; probe rows nullValue/undefinedValue), no cell has a null or undefined MESSAGE, none pins `42` -> `"42"` (G144-F3).

## 6. merge-tree
- Onto the commission's develop `0bd5e7bf62ac` (logs/merge_tree.log): rc 0, tree `372dc090`, merged-vs-develop paths == the 4 PR paths; redis.ts blob in the merged tree == head blob `12c5270a`.
- **Is any PR path among the three squashes' paths? No (overlap 0).** 4307ac87 (PR 1956) touched api-gateway `src/db.ts` + its test; cc33e702 (PR 1953, zod 3.25.76 -> 4.6.7) touched api-gateway `src/index.ts` (one import line, KS-1725 zod3-compat, top of file) + one test, and the workspace `package-lock.json`; **api-gateway's own package.json is not touched**; 0bd5e7bf (PR 1957) touched no api-gateway path.
- Onto develop as it stood at END, `4d1ab2cb6574` (logs/merge_tree2.log): rc 0, tree `1e1d3a85`, merged-vs-develop paths == PR paths; the two new squashes touch 11 paths, none in api-gateway.
- Suites were NOT re-run on a merged tree (it would need a fresh `npm ci` for zod 4; G144 NOT TESTED).

## 7. Kam's ks1346 rule (log type and field NAMES, never values), Q4
No new log line; three existing lines keep message, level and key (`error`); one existing thrown Error keeps its prefix. Judged per value kind:
- The constant `'unreadable thrown value'` is a type statement: compliant.
- A readable `message` is logged as before (base logged `err.message` as a value; pre-existing practice for this file and the KS-1868 class). For ioredis this is network text (e.g. `connect ECONNREFUSED host:port`, `WRONGPASS ...`): no credential value is formed into it by this code; the PR adds none.
- `String(m)` of a non-string message: number -> its digits; an object -> its own `toString()` return (base logged the object, i.e. its own fields via JSON, so head is no wider); a throwing `toString` -> the constant.
- A Symbol message -> `Symbol(<description>)`. I counted the description as a potential value but not a secret carrier: it is set by whoever created the Symbol in-process (no Redis/network data reaches it), and base already put it into the production throw path (where the concatenation threw). Compliant.
- The production throw message now carries `reason` where base carried `.message`: same content class; index.ts:1294 logs only `error.message` of it.
- No stack, no whole object, no URL added. Compliant (info).

## 8. Notes for the PR body
- **G144-F1 (recommended follow-up, HIGH priority, pre-existing, MEASURED)** With `isRedisAvailable()` false, `enforceDocumentTypeRules` passes everything: the catalogue reads empty (`documentTypesStore` is only written while the flag is false), so `resolveDocumentType` returns null and the "catalogue empty" branch returns `{ ok: true, docType: {} }`. Measured: a type registered with `requireMFA: true` -> `REFUSED 403 MFA_REQUIRED` with the flag true, **`ALLOWED`** on both replicas with the flag false, Redis up or down, at base AND head after an ORDINARY Error (logs/probe_site3_table.log enforce block). By read the same pass-through skips isActive, verification level, auth providers, metadata schema and the approval workflow gate. Reached by every Redis blip in production (ordinary error, `close`, retry 4); this PR does not change it and makes the unreadable-value path land in the same state. Suggested fix shape for a separate ticket: in the fallback mode, `enforceDocumentTypeRules` should refuse (503, like KS-1256/KS-1540) instead of treating an unreadable catalogue as an empty one.
- **G144-F2 (INFO, measured + read)** The author's "41 uses" is the definition + 40 call sites. Their seven families are right; the full map is in section 3. Additionally: the gateway brute-force lockout fails open in BOTH states (catch at security.ts:196 when Redis rejects; empty memory when the flag is false) and never arms anyway (`recordFailure` has no caller; KS-1372); `getRateLimitData/setRateLimitData`, `getDocumentSignature` and the trusted-verifier pair have no product caller; the real rate limits do not read the flag. Base's "flag stays true while Redis is down" holds only until the unchanged `close` listener or retry 4 clears it, and in the gateway the base listener throw ends the process via `uncaughtException` -> `gracefulShutdown`. One sentence in the body would make the behaviour statement exact.
- **G144-F3 (recommended follow-up, test gap, measured)** M4, M5, M6, M7 survive at both sites: no cell emits a null/undefined value to the listener (base threw), none has a null/undefined message, none pins `42` -> `"42"`. Same as G139-F1/G141-F1. Not a merge block: probe rows show the behaviour correct.
- **G144-F4 (INFO, measured)** Production rejection: base rejected 11/11 but with the named error in only 5/11; head 11/11 named. The author's 3-of-8 / 8-of-8 figure is the same shape on their 8 kinds.
- **G144-F5 (INFO)** Type change in the logged `error` field for a numeric message (`42` -> `"42"`) and the Symbol now logged as text: disclosed by the author; harmless.
- **G144-F6 (INFO, environment)** `ks1543-document-types-catch-logs-the-error.test.ts` timed out (60 s test / 10 s hook) under load at base and at head; green in the 2-worker rerun. Not related to this PR.
- **G144-F7 (INFO, harness hygiene for every gate)** The api-gateway suite's production-mode cells write the real logger's `logs/combined.log` relative to the process cwd; with the cwd at Wednesday's tree they append to `/Volumes/DevMASTER/WEDNESDAY/logs/combined.log` (pre-existing, gitignored, already holding earlier gates' lines; mine added request-log lines from test fixtures, no secrets). My own probe chdir'd to the workdir and did not.

## 9. NOT TESTED
The live PR body (no gh login); a real Redis or ioredis connection (stand-in; the ioredis emit/close/retry path is read in node_modules 5.11.1, not run); the command-level delay of a down client (`maxRetriesPerRequest` / offline queue; the stand-in rejects at once); a booted gateway (the `uncaughtException` -> `gracefulShutdown` path, `startServer().catch(process.exit(1))` and `require.main` are read); the Express routes over HTTP (middleware and `enforceDocumentTypeRules` were called directly); `createWorkflowInstanceIfRequired`, isActive/verification-level/provider/schema skips under fallback (read, only the MFA rule run); admin routes in fallback; whether a real unreadable value ever reaches this listener; suites and fragments on a merged tree; the four platform suites; CI; pre-push hook legs other than the ratchet; Node 24; Spark shadow review (not requested).

## Processes
All background runs I started (npm ci + shared build, three probe matrices, suites, static checks, mutants, reruns, one Monitor) have finished; `ps` shows no process with this workdir in its command line.

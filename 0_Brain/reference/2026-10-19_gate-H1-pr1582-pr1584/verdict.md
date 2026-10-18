#1582 KS-1540 head c86b91c5a7c2da906bce6f8db2d1226089863bb4: GO WITH NOTE (fail-closed read is closed end to end with the real redis module; one LOW residual: nothing in the KS-1540 suite pins the real module's isRedisAvailable)
#1584 KS-1504 head e8b4206f09d237fdb177c08a6b0c2b16e631acc2: GO (every interpolated field of the warning is escaped; all 11 plants come out as one line with no raw break or control character)
sha256/16: ec610baf7243a691

# GATE H1, tier 1 FULL, round 1 of 2. Independent QA, findings only. SECUURA.

Base: the brief named develop 385fc288. **Live develop moved twice during the gate**: b45b6917 (KS-1387, = #1581's content) then 4a547a11997e0e80bbeced0db57c2acb4c345368 (KS-1485 item 2, = #1583's content). Re-read with ls-remote at the start of the merge step and again before the final runs. Both PRs' merge-base is still 385fc288. The develop movement touches only governance/ and originate/ files. It overlaps nothing in api-gateway. All results below were run on both bases unless a line says otherwise.
Heads re-read with ls-remote and they match the brief: #1581 6b4bcaec, #1582 c86b91c5, #1583 16fc1d20, #1584 e8b4206f.

## FOUND

| # | PR | Severity | file:line | Finding |
|---|---|---|---|---|
| F1 | #1582 | LOW | services/health.ts:23, :53 | The author's residual is real but caught indirectly. If the real module's `isRedisAvailable` export is renamed, the guard's `?.()` returns undefined, the guard is a silent no-op, and the info reader goes back to 200 `[]`. Measured: with the export renamed (internal callers renamed too), the author's KS-1540 suite stays **5/5 green**, because it uses a double. My real-module suite goes 3 failed / 1 passed. **tsc does catch the rename, but only through routes/verification.ts:1276** (`redisService: typeof redisService`, a non-optional call), not through health.ts. So the protection depends on the create path keeping its non-optional call. A one-cell pin is worth adding: `import * as real from '../services/redis'`, `typeof real.isRedisAvailable === 'function'`, or one real-module case like my h1gate never-init suite. Severity LOW: this is not a hole today, it is the tripwire that would stop one from opening. |
| F2 | #1582 | NOTE (pre-existing, out of scope) | routes/admin.ts:1144-1146 with services/redis.ts:687 | In fallback mode, PUT /api/admin/settings read-modify-writes onto `{}` (the null from redis.ts:677) plus the defaults. It writes only to the per-replica in-memory store and answers 200 `success: true`. The write is lost on reconnect, and the in-memory copy lacks any stored integrations the body did not resend. This is not a fail-open on enforcement, because every enforcement reader refuses in fallback (see the reader census). It is a silent lost admin write. |
| F3 | #1582 | NOTE (pre-existing, out of scope) | routes/admin.ts:1119, :1154 | Same "null -> defaults" shape on two display readers. GET /api/admin/settings shows no `integrations` in fallback, so an admin sees connectors as unrestricted. Public GET /api/verification/policy reports the default `matchingStrategy: 'title_and_hash'` (and anchor/tamper defaults true) in place of whatever is stored. Neither reads the connector allow-list for enforcement. |
| F4 | #1584 | INFO | middleware/rateLimitEnforce.ts:181 vs :117-124 | authMethod is escaped at the call site, but principal and tenant are escaped inside `warnNoAllowance`. Today this is correct, because there is a single caller. A second caller passing a raw authMethod would reopen the gap. Optional: move the `logField` into line 123 for symmetry. Not a blocker. |
| F5 | #1584 | INFO | middleware/rateLimitEnforce.ts:159 | The hostile values cannot reach line 181 in production. The gate `MACHINE_AUTH_METHODS.has(user.authMethod)` (SameValueZero on primitives) admits only `api_key` or `oauth_app`. The author says so, and the suite reaches the line only through a getter that answers differently on its second read. The change is defence in depth, which is correctly scoped. |

**Reader census for the connector settings key (`platform-settings`) in fallback mode** (grep of `getNotificationSettings(`, `platform-settings`, `.integrations` and `allowedDocumentTypes` over Blockchain/Dev/services, non-test):
- services/health.ts:53 (info reader): **closed by this PR**, measured 503.
- routes/verification.ts:1276-1281 (create path allow-list): closed already (KS-1256 guard, before the read).
- routes/verification.ts:1355 (create path workflowPolicy): `catch {}` plus null -> `{}` -> `bypassWorkflow = false`. That is fail-closed (no bypass). It is also unreachable in fallback for a connector, because :1276 refuses the same request earlier in the same `if (connectorMeta)` path. Closed.
- routes/admin.ts:1119, :1144, :1154: the null -> `{}`/defaults shape, but these are display and admin-write readers, not allow-list enforcement. See F2 and F3.
- No other service reads the key. mcp-server only relays the gateway's /api/connector/info answer (api-client.ts:126; non-2xx handling is KS-1541's, already on develop).
**No allow-list enforcement reader is left open.**

## TESTED / HOW
All in the h1 scratch clone (`git clone --shared`, origin set to Secuura/Distributed_Secuura, fetch with the project's core.sshCommand) and one worktree. `npm ci` plus `npm run build -w packages/shared` in Blockchain/Dev. vitest 4.1.11 and tsc 5.9.3 from Blockchain/Dev/node_modules/.bin, node v24.7.0. Every loop ran from a script file under h1/.

1. **Hunk diff, three-dot from develop.** #1582 touches health.ts (+10, two hunks: the optional interface method at :21-23 and the guard at :49-56) plus its new suite. #1584 touches rateLimitEnforce.ts (+1/-1 at :181) plus its new suite. Nothing outside the named files. The 503 line in health.ts:54 is **byte-identical** (after stripping indentation) to routes/verification.ts:1277 on live develop.
2. **#1582, end to end with the REAL redis module.** I mounted `createHealthRoutes({}, realRedisNamespace)` on an express app, listened on an ephemeral port, sent a real HTTP fetch with x-api-key, and seeded the auth caches the way the author's harness does. I ran two states:
   (a) Never initialised (redisClient null). `isRedisAvailable() === false`, and the real read resolves null without throwing.
   (b) A real `initRedis()` against redis://127.0.0.1:1 (non-production). It returned false and set `fallbackMode`.
   - At develop: (a) **200 `allowedDocumentTypes: []`**; (b) **200 `[]`**. After a fallback-mode admin write of `['SSD_DOCUMENT']` into the memory store, it answered 200 `['SSD_DOCUMENT']`.
   - At c86b91c5, at live+#1582 and at live+both: all three cases answer **503 SERVICE_UNAVAILABLE** "Connector allow-list configuration is currently unreadable; refusing until it can be read", with no `allowedDocumentTypes`.
   - Pin cell: the real module exports `isRedisAvailable` as a function. Rename probe as in F1.
3. **#1584 plants.** I planted LF, CR, CRLF, U+2028, U+2029, a backslash (`a\nb` literal), a quote, NEL, DEL, TAB and ESC in authMethod (past the gate via the getter technique), and the same 11 in principal (connectorId) and tenant, plus an LF in the userId fallback principal. I read the console.warn line each time.
   - At e8b4206f, live+#1584 and live+both: **23/23**. Every line is one line with no raw CR, LF, LS, PS or NEL and no raw C0/C1 control. LF is written `\n`, U+2028 is written ` `, and the backslash is doubled (`a\\nb`).
   - At develop (and at the #1582 head, which has develop's limiter): **10 authMethod plants fail**, with a raw LF, CR, LS, PS, NEL, DEL, TAB or ESC, or an undoubled backslash, in the emitted line. QUOTE passes there because a raw quote is no break. principal, tenant and userId were **already escaped** (KS-1480): 11+1 pass at develop.
   - Other fields of that warning: principal and tenant go through logField at :123. clientId is used only as the throttle key and is never written. **No field is still written raw.**
4. **Red-first and green.** I copied the author suites onto develop's product.
   - KS-1540: **3 pass / 2 fail -> 5/5**. KS-1504: **3/3 -> 6/6**. Both match the claims.
   - Mutants: M1 (the guard if-block dropped, interface kept) gives KS-1540 2 fail, my real-module suite 2 fail. M2 (back to `String(user.authMethod)`) gives KS-1504 3 fail, my plant suite 10 fail.
   - Comment-only controls C1 (health.ts) and C2 (rateLimitEnforce.ts): both green (5/5, 6/6).
   - Full api-gateway suite:

     | Tree | Files | Tests | Result |
     |---|---|---|---|
     | develop 385fc288 | 121 | 1175 | pass |
     | live 4a547a11 | 121 | 1175 | pass |
     | #1582 head and live+#1582 | 122 | 1180 | pass |
     | #1584 head and live+#1584 | 122 | 1181 | pass |
     | live+both (tree 47a455d77dec) | 123 | 1186 | pass |

     The counts match the claims of 1180 and 1181.
   - tsc `-p services/api-gateway/tsconfig.json --noEmit`: rc 0, with 0 lines of output on every tree above.
   - ks1090 typecheck-tests leg (inside the full suite): green on all the trees. It went red only when my own gate files were present, so they are kept out of every full run.
5. **Merge prediction.** I used `git merge-tree --write-tree` plus `commit-tree` chains, all inside the scratch clone.
   - No file overlap between any of #1581-#1584, and no overlap with develop's movement for #1582 or #1584.
   - On brief base 385fc288: #1582 alone -> 2e1aa27e, #1584 alone -> d981be0d, both orders -> a37d28b0, all four PRs in **all 24 orders -> 47a455d77decfa848276c374aba96d7f160606bb**.
   - On live 4a547a11 (with #1581 and #1583 content already landed): #1582 alone -> 47875633, #1584 alone -> 37d4cd69, both orders -> **47a455d77dec**, and all 24 orders of the four -> **47a455d77dec**.
   - **R's prediction (tree 47a455d77dec in any order) holds on both bases.**
   - Planted conflicting control: a commit on live develop editing health.ts next to the guard's insertion point and the :181 line of rateLimitEnforce.ts. merge-tree reports **CONFLICT (content)** against #1582 (health.ts) and against #1584 (rateLimitEnforce.ts), rc 1 each, so the merge check can detect a conflict.

## NOT tested
- "leg 16 0 new": I do not know which leg the author means, so I did not run it as a separate leg. The ks1090 typecheck-tests leg inside the full suite is green on every tree.
- A connected (live) Redis: none was running on 6379, and Docker is out of scope. The Redis-available control is the author's double-based CONTROL cells only. I also did not drive a runtime transition: real Redis up, then down, `retryStrategy` reaching times===4, then fallbackMode.
- The full gateway app (index.ts with all middleware) was not booted. The route was driven through createHealthRoutes plus the real authenticateToken plus the real redis namespace, over real HTTP. index.ts:834 passes the same namespace (`import * as redisService`, index.ts:51), which I read but did not execute.
- `logDegraded` (rateLimitEnforce.ts:43-55): its clientId goes out as structured logger meta, not interpolated. It is a different warning and I did not test it.
- Other services' suites (governance, originate) at the merged trees: their content landed on develop outside this gate, and I ran api-gateway only.

## Hygiene
No write verb in !CODING. No push, no GitHub or Linear activity, no Docker. No rm and no cd. The only files written are this verdict and files under h1/. The gate test files and copies were moved (mv) out to h1/parked/ after each run. The worktree status was empty at the end. Scripts: h1/setup.sh, build.sh, run2.sh, evidence.sh, merge2.sh, final.sh, rename.sh. Logs: h1/logs, logs3, merge_*.out. (run.sh and merge.sh were first attempts: run.sh's full runs were contaminated by my own gate files, and merge.sh failed on a bash-3 associative array while develop had moved. Both are superseded and none of their results are cited.)

Scratch: /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/h1/

WALL-CLOCK: 18

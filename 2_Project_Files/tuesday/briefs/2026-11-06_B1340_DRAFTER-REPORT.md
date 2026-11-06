STARTABLE: YES (staged: the kit's first REFUSE holds it until seat N102's branch has landed; at drafting it has not, `rd573` test file reads 404 at main)

# B1340 SEAT-N104 drafter report (NexusAI log-injection round 2: RD-800, RD-799, RD-798 remainder), drafted 2026-11-06 16:07 to 16:25 AEDT

## BLUF
Kit written (146 lines, 8 four-underscore slots, control: `grep -c` 8; no at-sign token), slots file 8 keys. **46 open alerts, all `js/log-injection`; 44 in `backend/server.js` are the lane, 2 are in `backend/learningManager.js` (152, 153) and are held out.** Lane = one seat, one branch, three commits (A RD-800 eleven, B RD-799 eight, C RD-798 twenty-five), one PR. Builder C2 Sonnet; gate G1 Opus. No wrap changes a response, a status or a user-visible string; log text changes only by CR/LF removal, the 500 default cap, and three lines that now name fields instead of printing a body. Nothing needs a new word or a ruling.

## 1. The union (re-read by number at main 15b1426f, deduplicated, code line printed from the raw file)
Instruments: ticket numbers parsed with `#(\d+)\s+js/` (RD-798 44, RD-799 8, RD-800 12; 0 duplicates; **64 lines read = 64 parsed**, the R184 check; the Jira helper returns a tuple, my first loop crashed on that and was fixed, no count was affected). Each alert read by `gh api -X GET .../code-scanning/alerts/<n>` under the project's `GH_CONFIG_DIR`: **open 46 (RD-798 27, RD-799 8, RD-800 11), fixed 18 (RD-798 17, RD-800 1: #210)**. Controls that can fail: #220 reads `fixed`; the whole-repo open list (`alerts?state=open&ref=refs/heads/main`, 118 alerts, 47 `js/log-injection`) contains all 46 and exactly one more, **#161 (`scripts/instrument-cross-engine.js:280`, N103's lane, stays out)**. 27 + 19 = 46, which matches the sweep (RD-799 and RD-800: 8 + 11 = 19 open, #210 fixed). `backend/server.js` at that sha: 22431 lines, `git hash-object` of the raw read `3a548f44d21f69e7326bfb9d04c0a4fcb6ac670a` = the API blob. **All 46 are `js/log-injection`, severity `error`/`medium`. Not in `server.js`: 152 and 153 (`learningManager.js:125`, `:153`)**: that file has no `logSafe` require, so the fix is a require plus two wraps in another file, not the one-line fix; named, held out (HOLD 1). Alert 212 (`server.js:15387`) is in the lane, batch A; it is the line the independent review (B1323-6) measured as still forging at head.

| Alert | Ticket | path:line at main 15b1426f | The line, printed from the raw file |
|---|---|---|---|
| 152 | RD-798 | `backend/learningManager.js:125` | `` console.log(`[learning] Skipping duplicate pattern: "${ambiguousQuery}"`); `` |
| 153 | RD-798 | `backend/learningManager.js:153` | `` console.log(`[learning] Saved pattern: "${ambiguousQuery}" → "${description}"`); `` |
| 162 | RD-798 | `backend/server.js:190` | `` logger.info(`[AI Audit] Logged misunderstanding: "${query.substring(0, 80)}" — ${reason}`); `` |
| 163 | RD-798 | `backend/server.js:229` | `` logger.info(`[AI Audit] Auto-created feedback item #${nextId} for query: "${query.substring(0, 60)}"`); `` |
| 164 | RD-799 | `backend/server.js:2475` | `` `[auth] DENY: authentication state could not be established (settings store unreadable) — ${req.method} ${req.path}` `` |
| 165 | RD-799 | `backend/server.js:2520` | `` logger.error(`[storage] REFUSED ${req.method} ${req.path}: the data volume is not writable (${(error && error.code) \|\| 'unknown'})`); `` |
| 166 | RD-799 | `backend/server.js:2677` | `` logger.warn(`[storage] session activity not recorded — the data volume is not writable (${activityError.code}); ${req.method} ${req.path} continues`); `` |
| 167 | RD-799 | `backend/server.js:3108` | `` logger.info(`[Entra Auth] Initiating login, redirect URI: ${redirectUri}`); `` |
| 168 | RD-799 | `backend/server.js:3149` | `` logger.error(`[Entra Auth] OAuth error: ${error} - ${error_description}`); `` |
| 169 | RD-799 | `backend/server.js:3165` | `` logger.info(`[Entra Auth] Callback received - state from URL: ${state?.substring(0, 8)}..., stored cookie: ${storedState?.substring(0, 8) \|\| 'MISSIN `` |
| 170 | RD-799 | `backend/server.js:3169` | `` logger.error(`[Entra Auth] State mismatch - URL state: ${state}, cookie state: ${storedState \|\| 'MISSING'}`); `` |
| 171 | RD-799 | `backend/server.js:3525` | `` logger.info(`Session invalidation: revoked ${sessionsInvalidated} session(s) for ${email} after role/active/password change`); `` |
| 187 | RD-798 | `backend/server.js:7053` | `logger.info('Early catch for user query:', message);` |
| 188 | RD-798 | `backend/server.js:7086` | `logger.warn('Clarification message returned for user query, this should not happen:', response.substring(0, 100));` |
| 189 | RD-798 | `backend/server.js:7148` | `logger.info('Returning response for user query, length:', typeof response === 'string' ? response.length : 'object');` |
| 190 | RD-798 | `backend/server.js:7181` | `logger.info('Early catch for unusual activity/quick question:', message);` |
| 191 | RD-798 | `backend/server.js:8170` | `` logger.info(`[learning] Stored clarification: "${originalQuery}" → "${clarification}"`); `` |
| 192 | RD-798 | `backend/server.js:8573` | `` logger.info(`🎯 Negation intercept → non-printers for: ${query.slice(0, 80)}`); `` |
| 193 | RD-798 | `backend/server.js:8715` | `` logger.info(`🤖 AI cache hit [early] for "${query.slice(0, 60)}" (age=${Math.round((Date.now()-cached.at)/1000)}s)`); `` |
| 194 | RD-798 | `backend/server.js:8802` | `logger.info('User list query detected:', query);` |
| 195 | RD-798 | `backend/server.js:8810` | `logger.info('Color printing cost query detected:', query);` |
| 196 | RD-798 | `backend/server.js:8824` | `logger.info('Color/mono percentage query detected:', query);` |
| 197 | RD-798 | `backend/server.js:8837` | `logger.info('Duplex/simplex query detected:', query);` |
| 198 | RD-798 | `backend/server.js:8845` | `logger.info('Business hours query detected (early):', lowerQuery);` |
| 199 | RD-798 | `backend/server.js:8854` | `logger.info('User cost query detected:', query);` |
| 200 | RD-798 | `backend/server.js:8994` | `logger.info('Risk condition query detected:', lowerQuery);` |
| 201 | RD-798 | `backend/server.js:9004` | `logger.info('Business hours query detected:', lowerQuery);` |
| 202 | RD-798 | `backend/server.js:9083` | `logger.info('🔍 Scan analysis query detected (early):', query);` |
| 203 | RD-798 | `backend/server.js:9096` | `logger.info('🔍 Printer usage analysis query detected:', query);` |
| 204 | RD-798 | `backend/server.js:9654` | `` logger.info(`🤖 AI cache hit for "${query.slice(0, 60)}" (age=${Math.round((Date.now()-cached.at)/1000)}s)`); `` |
| 205 | RD-798 | `backend/server.js:9912` | `` logger.info(`👤 ${userName}: 0 in 30d, ${allLogsForUser.length} all-time → widening`); `` |
| 206 | RD-798 | `backend/server.js:13007` | `logger.info('📊 Generating printer usage analysis for query:', query);` |
| 207 | RD-798 | `backend/server.js:13290` | `logger.info('Printer-specific query detected for printer:', printerName);` |
| 208 | RD-800 | `backend/server.js:14634` | `console.error('[Log Analytics Setup] Invalid request body:', req.body);` |
| 209 | RD-800 | `backend/server.js:14659` | `console.log('[Log Analytics Setup] Invalid GUID format:', workspaceId);` |
| 211 | RD-800 | `backend/server.js:15342` | `console.log('[Log Analytics Query] Executing:', finalQuery);` |
| 212 | RD-800 | `backend/server.js:15387` | `console.log('[Log Analytics Schema] Getting schema for:', tableName);` |
| 213 | RD-800 | `backend/server.js:15651` | `` logger.info(`✅ Promoted data source ${req.params.id} (${decrypted.name \|\| ''}) to primary; live reconfigured.`); `` |
| 214 | RD-800 | `backend/server.js:16133` | `console.log('[Domain Setup] Request received:', req.body);` |
| 215 | RD-800 | `backend/server.js:16185` | `console.log('[Domain Setup] Saved domains:', allDomains);` |
| 216 | RD-800 | `backend/server.js:16189` | `console.log('[Domain Setup] Updated in-memory CORS allowed origins:', allDomains);` |
| 217 | RD-800 | `backend/server.js:16240` | `console.log('[AI Model Setup] Request received:', req.body);` |
| 218 | RD-800 | `backend/server.js:17121` | `console.log('[Data Sources] Testing connection for:', dsId);` |
| 219 | RD-800 | `backend/server.js:17305` | `console.log('[Data Sources] Deleting:', dsId);` |
| 222 | RD-798 | `backend/server.js:21844` | `` logger.info(`✅ Learned from user confirmation: "${originalQuery}" -> "${userResponse}"`); `` |
| 223 | RD-798 | `backend/server.js:21855` | `` logger.info(`✅ Learned pattern (basic): "${originalQuery}" -> "${userResponse}"`); `` |

## 2. Is 46-ish wraps in one seat one lane?
As a mechanical edit, yes (44 one-expression edits, same helper, same file, one rule). As a lane with a red per site, it is large: **ESTIMATE (mine, scaled from the landed file: 288 lines and 13 tests for 5 sinks): about 44 product lines, 700 to 1000 test lines in three files plus one helper, about 100 tests, two full verifies of about 24 minutes.** The cost sits in driving sites, not in wrapping. So the kit bounds it: three commits by ticket (A RD-800, B RD-799, C RD-798; simplest harness first, the 25 chat-route sites last, so a context stop loses the cheapest-to-redo batch), a time-box of two attempts per site (a site that cannot be driven falls to a shape-only cell with the evidence printed, it is not a stop), and a PARTIAL rule (commit only a batch that is green at its own head). **One PR is cheaper for the gate than three:** each PR costs a hosted Build, a CodeQL run, a Deploy-demo skipped run and a G1 verify of about 24 minutes; three PRs would also serialise on the counts file (each rebases onto the last pair). The price of one PR is that a bad batch holds the other two; the PARTIAL rule and the per-batch commits limit that. If you prefer two kits, the natural cut is A+B (19 sites, security surface, simple harness) and C (25 sites, chat harness); that is Q-1.

## 3. User-visible strings, responses, auth behaviour, gate and builder row
- **Response bodies, statuses, headers: none changed.** Every edit is inside a `logger.*`/`console.*` argument; `logSafe` never throws (`logSafe.js:36`-`:40`), and every argument expression is kept as it was (for example `state?.substring(0, 8)` stays inside the wrap, so a non-string `state` throws exactly where it threw). The kit also pins this with a head cell per route against a body measured at base.
- **User-visible strings: none.** Log text changes, all intended: (a) CR/LF removed and other controls escaped; (b) default cap 500 with a marker (a chat message over 500 characters is now cut in the log; the RD-799 ticket's own fix shape says "a truncated ... value"); (c) 208, 214, 217 print `typeof`/field names instead of `req.body` (the RD-800 ticket's words; the label text is unchanged); (d) 215/216 and 189 are kept text-equal by `logSafe(JSON.stringify(allDomains))` and wrapping the number (kit MEASURE FIRST 6 prints both).
- **Sensitive surface, named:** `server.js:2475`, `:2520`, `:2677` (the auth and storage middleware, every request passes `requireAuth` `:2529`, but the lines run only on the fault branches), `:3108` (`/api/auth/microsoft/login`), `:3149`, `:3165`, `:3169` (`/api/auth/microsoft/callback`, public), `:3525` (`PUT /api/auth/users/:email`, admin). No wrap changes a branch, a redirect, a cookie or an audit call. **Gate row: G1 Opus (`model-routing.md:108`), your default, agreed: security rule, product files, the auth middleware and the OAuth callback.** **Builder row: C2 Sonnet; I found no C3 surface**: nothing is designed on an auth surface, each edit is spelled out. One thing near the line: 170 (`:3169`) logs the OAuth `state` and the cookie state in FULL while 169 logs eight characters; the kit only wraps (Q-6).

## 4. Test design (two layers, avoiding B1323-1 and B1323-2)
- **Shape layer, every site (44 cells).** A helper reads `server.js` as text, finds the call by its label, takes the whole call by a balanced scan, and asserts each request-derived expression is inside `logSafe(...)`. Red at the base by assertion, and reversing any one wrap reddens exactly its cell. This is what answers B1323-2 (a wrap whose reversal reddens no cell): a wrap with no red on reversal is not added, and the rule is in the property. It is a shape proof, said so in the file header; `logSafe` itself is held by the existing unit file `rd801-feedback-log-injection.test.js`.
- **Behaviour layer, every site measured R.** Real server as a child process, real logger, the child's own output; assertion "no output line starts at the forged marker" with the ordinary-text line as positive control (the landed `rd798-...-ai-suggestion-sinks.test.js` shape, `recordOf` at `:99`). Drivers: chat routes through `POST /api/chat` (`:6974`, no control-character check); callback through `req.query` and the URL-decoded cookie; data-source routes through the URL-decoded `:id`; setup bodies through JSON strings. For 214 and 217 the base red is NOT CR/LF (`util.inspect` quotes and escapes them inside an object, so the whole body never forges a line): it is an extra body field's VALUE (`not-a-real-secret-rd800`) printed at base, absent at head, the field name still present. 208, 164-167, 189, 215-216 are my N reading (no request can put CR/LF there: undefined body, raw CR/LF refused by the HTTP parser in the target and headers, a number, validated domains): shape only, labelled.
- **Caps pinned both ways (B1323-1).** Default 500: a 501-character and a 5000-character value expect the marker at exactly 500, so a larger or infinite `max` goes red (plants Y3, Y4). The 2048 at 211: 1500 characters whole and 5000 cut at 2048 (Y5 to 1000 and to `Infinity`). Plants run by one script over the site table: PL-n per alert plus Y1 to Y5.
- **Test file added: yes, three** (`rd800-...`, `rd799-...`, `rd798-log-injection-chat-and-learning...`, plus an optional shape helper). That is what ties the lane to the counts file: +3 suites, +N tests, one `--update-counts`, which is why the kit is staged behind N102 (both move the pair). Arithmetic asserted before regenerating.

## 5. Landing rule, from NexusAI's records
`CLARIFICATIONS.md:2067` "Merge path: open a PR from the gated branch, wait for CodeQL (a background wait that EXITS), then land the SAME commit. Never squash, never rebase"; `:2068` never dismiss; C-68 `:665` (a gate verdict is valid at the head it ran on); `:2080` both thresholds. So a **merge commit pinned to the gated head**; the repo allows all three methods (`allow_merge_commit/squash/rebase` true), so the rule is the project's. **A merge does start Deploy demo** (`deploy-demo.yml:27-28` push to main, `:29-:32` paths-ignore does not match `__tests__/` or `backend/`), **but its two jobs skip while the variable is unset**: `:53` and `:91` need `vars.CI_DEPLOY_ENABLED == 'true'`, repo variables `total_count` 0, environments `dev` only, and the run of the merge of pull request 172 (id 42162626357, head `15b1426f`) has jobs `deploy` and `build` both `skipped` (control: 4412 runs read). Check: Tuesday re-reads variables and environments immediately before the merge and the new run's two jobs after; the seat never touches it. **Alerts are judged on main's analysis at the merge commit, never on the PR ref** (DRAFTER_RULES): the kit says so and treats a site still reported after the merge as a new round. Good news from the data: the two-argument form `logSafe(x, KQL_LOG_MAX_CHARS)` is no longer unprecedented, alerts 174, 177, 181 read `fixed` at 2026-11-06T04:30:41Z from pull request 172's merge.

## Other facts re-measured (instrument, control)
- Main `15b1426f` (`branches/main`); open PRs 0 (control `pulls?state=all` first number 172); `heads/b134` 0 (control `heads/b13` prints `refs/heads/b1317/...`); N102 and N103 branches not on origin; `rd573` test 404 at main (control: counts file 200). Counts blob `aadcc165...`, 5327/319.
- Ports: `lsof -nP -iTCP:9380-9389 -sTCP:LISTEN` 0 lines (control 7000: 3). **Word-boundary scan of `938[0-9]` over the 50 non-`.pre-` SEAT kits of 5 and 6 Nov: ONE hit, `2026-11-06_B1312_SEAT-H128_hpsmpoc-mock-rows-pause.md` lines 37, 83, 84 name 9380-9389 (and 9384-9387 for web/stub/hosted/chooser). H128's pane is not live (panes listed at 16:11 have H131, H133, no H128).** The kit types no port, so this is a paper overlap; reported, not changed (Q-7). `937[0-9]` hits 2 files (N102's block). `N104`/`B1340` as whole words: 0 files (control `N103`: 3).
- Source-level guards: 35 of 37 log texts in 0 test files; `REFUSED` 111 (positive control) and `widening` 13 are generic words, re-scanned as exact strings: 0. 61 test files read `server.js` as text (seat re-runs).
- Existing prior work: `data-source-save-log-redaction.test.js` (console.log cell on a setup route), `rd452-store-fault-preload.js` (a store fault inside a spawned server, for 164-166), `rd436-group-gate-callback` and `rd645-auth-limiter-mounted` (drive the callback). `@babel/parser` is not a declared dependency, so the shape helper is hand-rolled.
- Model: `model-routing.md:92` C2, `:93` C3, `:108` G1; `models_latest.json:23` `claude-sonnet-5-5`. Round count: B1323's verdict line reads "GO WITH FINDINGS round 1 of 2 on class RD-798 log sinks"; NO GO 0 on that class. This kit's gate is a fresh round 1 of 2 on a new class (suggest "RD-79x log sinks round 2").

## D-decisions (mine)
- D-1 One seat, three commits by ticket, one PR; counts file moves in the last commit only (earlier heads are not individually verify-green, said in the kit).
- D-2 Two layers (shape for all, behaviour for R) with a two-attempt time-box per site; N is recorded, not a stop.
- D-3 Bare values: numbers, constants and framework codes stay bare; a closed list stated as a property first.
- D-4 214/217/208 log field names via `logSafe(Object.keys(req.body || {}).join(', '))` / `typeof`, label text unchanged.
- D-5 Reuse `KQL_LOG_MAX_CHARS` (`:5982`) at 211 only; no new constant.
- D-6 Staging test: `rd573` test file present at main AND counts blob differs from `aadcc165`; other NexusAI panes tested by what their kit grants (N103 and R184 are not stops).

## Q-questions for Tuesday (each with a default)
- Q-1 One kit or two? Default one (A, B, C), as written.
- Q-2 N sites (about ten of 44 by my reading, 164-167, 189, 208, 215, 216, 188, maybe 171 and 213): wrap with a shape cell only, default yes; the alternative is to cut them and leave the alerts open.
- Q-3 Time: I propose Target READY 210 and HARD STOP 270 minutes (slot S5); the template's 90/120 is for five sinks.
- Q-4 `learningManager.js` 152 and 153: default held out (HOLD 1); a later two-line kit.
- Q-5 Default cap 500 on chat text: default keep (the ticket's own shape allows a cap); alternative a larger named constant.
- Q-6 Log the OAuth state in full at 170? Default wrap only, no truncation (not a wrap question).
- Q-7 Port block: I wrote 9380-9389 as asked, as a reservation only. H128's older kit also names it. Default: none typed, leave.

## The one default I doubt
Hosted CodeQL on the N sites. The number and constant sites (189, 164-167) are flagged by CodeQL through its model of `req.path`/`response.length`; B1323's plant PL5c shows a wrap that is not on the flow closes nothing. Here the wrap IS on the flow, but only the post-merge scan on main says so. Expect some of the 44 to need a round 3.

## UNMEASURED
Hosted CodeQL, Build and Gitleaks on any of this; which R sites are drivable with the harness's empty data (213, 171, 211, 188, the `analyzeQuery` keyword branches); whether 215/216's domains can carry CR/LF; the seat's run time; that N102 lands before launch; test line counts (estimate).

## Outside the fences
Reads: DRAFTER_RULES; B1317 kit, B1323 STATUS; B1335, B1336, B1337 kits (partition lines, line 9 of B1337, B1335 report and slots); SWEEP-1510 lines 139-144; `CLARIFICATIONS.md` lines 665, 2067, 2068, 2080 (local, read-only); `model-routing.md` and `models_latest.json` lines; `status_watch.sh:56`; Jira GET through `b774lib.py` for RD-798, RD-799, RD-800 and `RD-99999999` (no write, no JQL); `gh api -X GET` under the project's `GH_CONFIG_DIR` (alerts by number, whole-repo open list, contents raw of `server.js`, `learningManager.js`, `logSafe.js`, `logger.js`, `build.yml`, `deploy-demo.yml`, the rd798 test, the git tree, tarball of main extracted and grep-only in the session scratchpad, workflow runs and jobs, variables, environments); `lsof`; `tmux list-panes`. **Slips: (1) I typed `cd /dev/null` once inside a subshell in a port-scan command (a "never type `cd`" breach; it ran, no effect); (2) one `echo ====` was refused by the zsh hook, re-run without it.** Written: the three files, plus scratch files in the session scratchpad only (`jira.py` calls only `get`/`adf_texts`). No `decision_queue.sh`, no git in the project repo, no Artifact/Docs/mail.

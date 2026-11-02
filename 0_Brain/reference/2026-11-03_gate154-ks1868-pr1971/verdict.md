# QA Gate 154 verdict: Secuura/Distributed_Secuura PR 1971 (KS-1868, m365-integration src/oauthState.ts: OAuth state save + consume catches), TIER 2, round 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** Every figure the author claims re-measures. I ran the REAL routes of m365-integration/src/index.ts (POST /api/connections/init and GET /api/callback), the REAL oauthState.ts (base and head) and the REAL winston logger; only ./db (a fake state table), exchangeAuthCode, authenticate, express.listen and the Graph fetch were replaced (the harness of the existing KS-1677 test, extended), 10 value kinds x 2 sites x base/head = 40 cells. For an unreadable value head's after-state equals an ORDINARY Error's after-state at base, at both sites: same HTTP answer, same redirect, no code exchanged, no connection bound or changed, same state-row survival. At base an unreadable value in the consume catch left the callback request UNANSWERED (plus one unhandled rejection per request) and in the save catch turned the sign-in start into a 500. Mutants: 22 run, 16 killed, 6 survive (all about the value formatting / log level, none about the unreadable class): G154-F1. KS-1677 (callback rebind): the PR touches nothing on that path (G154-F3). Node v26.8.1 throughout, nothing measured on Node 24.

## Heads
- START (logs/head_start.log, ~22:1xZ / 09:1x AEDT): PR head `768ddf0f88134c2dae24ccfdee033941fb235c14` (matches the READY mail); develop `f7b4a7173010a407864ecb7ab92814824f9cb4b6` (the mail's ddd770cab4aa has moved on; it was 1969 or later). END (logs/head_end.log, 22:23:42Z): both unchanged.
- Merge-base = PR parent = `26955bf1b828` ("Base"). `git diff --name-only pr1971~1 origin/develop -- Blockchain/Dev/services/m365-integration` is EMPTY: develop has not touched the service since the PR's base.
- PR body not read (no gh login); READY mail copied in evidence/w21_pr1971_ready.txt.
- Clone left clean (`git status` empty); oauthState.ts sha256 restored after every swap (7c7c0adcbe5c...); probe copies moved to logs/_probe_copy_*.ts.

## 1. Diffstat (logs/diffstat.log, three-dot vs 26955bf1)
4 files, +166/-2 exactly as declared: oauthState.ts +16/-2; new test 122; flow fragment 11; cheat fragment 17. Paths: Blockchain/Dev/services/m365-integration/src/{oauthState.ts, __tests__/ks1868-oauth-state-db-catches-unreadable-throw.test.ts}, Projects Documents/fragments/{flow,cheat}/KS-1868-m365-oauth-state.html. Nothing outside.

## 2. The hunks (logs/hunks.diff)
Both catches (save line 96, consume line 137): `logger.warn('DB save|consume OAuth state failed', { error: err?.message })` becomes
`let reason; try { const m = err?.message; reason = m === undefined || m === null ? m : String(m); } catch { reason = 'unreadable thrown value'; } logger.warn(<same text>, { error: reason })`.
Consume still ends `return null;`; save still falls through (the state stays in memOAuthStates, set before the DB call).
Does NOT change: log texts and level (warn), the meta key, the SQL, the memory fallback, the `return null`, index.ts, the callback/start routes, refuseOAuthCallback.
Changes beyond the unreadable class (small, see G154-F2): a readable message that is not a string is now `String()`-ed (number 42 logged as "42"; a Symbol message as "Symbol(m)" where base passed the Symbol; an object message with a throwing toString becomes the constant text); null/undefined are passed through as before; a string message is unchanged.

## 3. Behaviour (RUN: scripts/ks1868-g154-probe.test.ts via scripts/probe_run.sh; logs/probe_base.jsonl, probe_head.jsonl, probe_table.log)
Harness: the real index.ts app served over 127.0.0.1, the DB seam throws the value on the state INSERT (save) or on the state DELETE...RETURNING (consume); a 2.5 s abort for "no answer"; an unhandledRejection counter; the real logger.warn wrapped with call-through to record the logged `error` field. Kinds: ordinary Error, revoked Proxy, Error with message getter that throws, null, undefined, string, number, plain object {message:'x'}, Error with Symbol message, object message whose toString throws. winston is console-only in this service (utils/logger.ts), no log FILE is written anywhere.

### Q1: the class bar with the real logger
| kind | base consume | head consume | base save (init route) | head save |
|---|---|---|---|---|
| ordinary Error | 302 invalid_state, warn "db boom" | same | 201, cookie set, warn "db boom" | same |
| revoked Proxy / message-getter throws | **NO ANSWER (timeout), 1 unhandled rejection per request, no warn** | 302 invalid_state, warn "unreadable thrown value", 0 unhandled | **500, no cookie, no warn** | 201, cookie set, warn "unreadable thrown value" |
| object message with throwing toString | 302 (logger got the object, `<object>`) | 302, "unreadable thrown value" | 201 | 201 |
| null / undefined / string / number / plain object / Symbol message | 302, field undefined / "x" / symbol | 302, field undefined / "x" / "Symbol(m)" (null/undefined unchanged) | 201 | 201 |
For both sites and every kind the HEAD row equals the ORDINARY-Error row (status, redirect, exchanged=0, connection stays pending, 0 unhandled, a warn line is written). The real logger threw in no cell at head. **Raise accepted.**

### Q2: the refusal path, consume -> null -> refuseOAuthCallback 'no_matching_state' -> invalid_state (RUN)
At head, for every kind including both unreadable ones: HTTP 302 to `.../admin/integrations?m365=error&message=invalid_state`, `exchangeAuthCode` called 0 times, the connection still `pending` when read back as its own organisation, no binding or rebinding. Same as the ordinary Error at base and head. At base the unreadable cells exchanged nothing and bound nothing either (they hung with an unhandled rejection: fail closed by accident, never answered). The cookie, state and org check are unchanged code (index.ts:644-651 read; the call sits outside any try, which is why the base rejection was unhandled: Express 4.22.3 does not forward an async handler's rejection, measured as "no answer"; process termination on the unhandled rejection is READ, not run: the service registers no handler (grep), same as gate 151).
After the throw the state row was never deleted (the DELETE threw), so with the DB healthy again the SAME browser retry completes (replay = success, 1 exchange) at base and head for every kind, ordinary Error included: a transient DB error does not burn a sign-in. That is existing behaviour, equal for the unreadable class at head.
**KS-1677** (the callback let any holder of a connection id rebind it): the PR does not touch it. At this base the callback derives the connection ONLY from the consumed record (`memConnections.get(pending.connectionId)`), never from the request; state is an opaque 32-byte token bound to the browser cookie, user and organisation. The existing ks1677 suites (callback binding R1..R19, state without DB) are in the whole-suite run and green. The PR changes only the log argument inside two catches.

### Q3: the save catch (RUN)
If the INSERT fails the catch logs (warn) and the function RESOLVES; the state is already in this process's memOAuthStates. The start route (index.ts:748, inside its try) then sets the binding cookie and answers **201 with the authorization URL** (identical to an ordinary Error at base; before this PR the unreadable class got 500 via next(error), no cookie, but the pending connection row was already written by dbSaveConnection just before: read). Is the flow refused later? Yes, measured: with the DB up, consumeOAuthState reads only the TABLE (memory is consulted only when the DB is down, oauthState.ts:112-117 read), the row is missing -> null -> invalid_state, 0 exchanges, connection stays pending, in every kind at head and for the ordinary Error at base and head. (KS-1677 R17 already pins this for the ordinary Error.) So a flow does proceed to Microsoft with a state that was never stored, and is refused at the callback. The user-visible change of this PR for an unreadable DB error at save is therefore 500 -> 201-then-refused, exactly what any ordinary DB error already gets (G154-F4).

## 4. Re-measure
- Install: `npm ci --ignore-scripts` SUCCEEDED here on develop's lockfile (logs/npm_ci.log, 1798 packages; gate 151's failure did not reproduce at this base), packages/shared built (rc 0).
- Red-first (new test only, product at base; logs/red_base_new.log): **4 failed / 2 passed (6)**, every failure an AssertionError (R1/R2 "expected { threw: true } to deeply equal { threw: false }", R3/R4 "... { threw: false, value: null }"), 0 timeouts; controls C1/C2 pass. As claimed.
- Whole m365-integration suite (--root anchored, --maxWorkers=2): head **31 files / 295 tests, rc 0** (logs/head_whole.log); base product + new test: 1 failed / 30 passed files, 291 passed / 4 failed of 295 (logs/base_plus_new_whole.log) = the 4 R cells only, so the base suite is 30 files / 289 (291 minus the 2 controls... 295-6): 289 -> 295 as claimed.
- tsc: service tsconfig (tests excluded) rc 0, 0 errors at head (logs/tsc_own_head.log). With tests (the service's own tsconfig.test.json): **0 errors at head and 0 at base** (logs/tsc_tests_*.log). The author's 0/0 reproduces. The "ratchet baseline" in this service is the vitest COVERAGE threshold (60/50/60/60), not a tsc count: coverage run at head rc 0, all files 75.39 st / 68.59 br / 71.42 fn / 77.22 ln, oauthState.ts 94.82/83.33/100/97.91 (logs/cov_head.log); base coverage not run.
- eslint (cwd = service so the flat config applies; scripts/eslint_run.js): oauthState.ts + new test rc 0, no output; planted `debugger;` + unused const rc 1 (no-debugger error, no-unused-vars warning), restored by sha.
- docs-fragments (Blockchain/Dev/scripts/docs-fragments.mjs check --root repo; scripts/frag.sh): clean rc 0 "lint clean, render passes", with the same pre-existing cheat ADVISORY at committed line 6235 as gates 139/141/150/151. Planted: flow unclosed div rc 1; flow `<!--n-->.` removed rc 1; cheat unclosed div rc 1; cheat `</table>` corrupted rc 1; every restore verified by sha; rc 0 after (logs/frag_*.log).
- Fragment claims: "+16/-2", "4 of 6 red by assertion", "30/289 -> 31/295", "0 at base and head" tsc all hold. The fragment's recorder statement (8 kinds x 2 functions, real logger) is consistent with my own 10 x 2 run; I did not re-run the author's scratch recorder.
- Note the COMMITTED test mocks the logger entirely (records warn calls); the real-logger claim rests on the author's scratch recorder and on my probe.

## 5. Mutants (scripts/mutants.py; one change per run in oauthState.ts only, committed test file only, sha256 restored after every run: all True; logs/mutants.jsonl)
22 runs: **16 killed (every kill an assertion failure), 6 survived.** Per site (save | consume are identical in outcome):
| mutant | result |
|---|---|
| M0 revert to `err?.message` | KILLED (R1,R2 | R3,R4) |
| M1 catch rethrows | KILLED (R1,R2 | R3,R4) |
| M2 constant text changed | KILLED (R1,R2 | R3,R4) |
| M4 always the constant text | KILLED (C1 | C2) |
| M5 log line dropped | KILLED (C1,R1,R2 | C2,R3,R4) |
| M8 meta key renamed | KILLED (C1,R1,R2 | C2,R3,R4) |
| consume M10 `return null` removed | KILLED (C2,R3,R4) |
| consume M11 `return memOAuthStates.get(stateHash) ?? null` (memory fallback with the DB up) | KILLED (C2,R3,R4), only because C1 of the same file put that hash in memory |
| **M3 null/undefined branch inverted** | **SURVIVED both sites** |
| **M6 `String(m)` dropped (pass-through)** | **SURVIVED both sites** |
| **M7 always `String(m)` (null becomes "null")** | **SURVIVED both sites** |
| **M9 log level raised to error** | **SURVIVED both sites** |
All six survivors concern the formatting of a READABLE non-string message or the log level; none can reintroduce the unreadable-value throw (every mutant that does is killed).

## 6. merge-tree onto develop `f7b4a717` (logs/merge_tree.log)
rc 0, tree `591e63009ae6...`, clean. The merged tree differs from develop in exactly the PR's 4 paths (logs/merged_vs_develop.log equals logs/pr_paths.log, diff empty). Suites/fragments not re-run on the merged tree (develop has no m365-integration change since the PR's base, so the service is byte-identical).

## 7. Kam's ks1346 logging rule
No new log line. Text, level and key are unchanged; the value of `error` is now a string of the message of a thrown value (as before for strings), "unreadable thrown value", or null/undefined. A thrown value's other fields are never logged. It is slightly TIGHTER than base for an object-valued message (base handed the object itself to the logger, head logs "[object Object]"-style String() or the constant). Compliant. (The pre-existing practice of logging an Error's message text is unchanged.)

## 8. Notes for the PR body
- **G154-F1 (recommended follow-up, test gap, measured)** Mutants M3, M6, M7, M9 survive at both sites: no cell pins the null/undefined pass-through, the stringification of a non-string message, or the warn level. Not a merge block: none can bring back the throw. One table-driven cell (null, 42, Symbol message, plain object -> expected `error` values) per site would pin M3/M6/M7; M9 needs a level assertion.
- **G154-F2 (INFO, disclosure)** Beyond the unreadable class the logged `error` field changes for readable non-string messages: number 42 -> "42"; Symbol('m') -> "Symbol(m)" (base passed the Symbol itself and the JSON logger drops it); an object message -> its String() or, if toString throws, the constant. null/undefined/string/plain `{message:'x'}` unchanged. Log-only; no response or state differs (measured, probe_table.log).
- **G154-F3 (INFO, answer to the gate question + KS-1677)** The PR touches only the log argument in two catches. The callback's refusal logic, cookie binding and the connection lookup (derived from the consumed record, not the request) are untouched, so the KS-1677 rebind path is neither reopened nor widened; its own suites stay green.
- **G154-F4 (INFO, measured, behaviour change worth stating)** Save failure with an unreadable value: sign-in start goes from 500 (no cookie) to 201 with the authorization URL and cookie; the callback is then refused with invalid_state (the DB table is the only authority when the DB is up). Equal to what an ordinary DB error already got. A user would reach Microsoft and be bounced back with the one invalid_state message; the pending connection row exists in both cases.
- **G154-F5 (INFO, measured)** A consume that fails on a DB error (any kind) leaves the state row in place; the same browser can retry once the DB is healthy (replay success, 1 exchange). Existing behaviour, equal for the unreadable class at head.
- **G154-F6 (INFO, consequence read)** At base the consume catch rejection is an unhandled rejection in an async Express 4.22.3 handler: measured "no answer + 1 unhandled rejection per request"; process exit on an unhandled rejection is read (no handler registered), not run.
- **G154-F7 (INFO, wording)** The mail's "develop ddd770cab4aa" is stale; develop is f7b4a717 now, and the PR's base 26955bf1 equals the service's state on develop. The mail records two wording edits to the Seat W 20th spec; not checkable without the PR body.
- **G154-F8 (INFO, tooling)** The "ratchet baseline" for m365-integration is vitest coverage thresholds, not a tsc count; tsc with tests is 0/0. `npm ci` worked at this base.
- **G154-F9 (INFO, test design)** The committed cells mock `./utils/logger`; the real-logger proof is the author's scratch recorder (not committed) and this gate's probe (scripts/ks1868-g154-probe.test.ts, logs/probe_*.jsonl).

## 9. NOT TESTED
The live PR body; a real Postgres (a fake table honouring the statements' parameters; the SQL itself runs on a real engine in the existing ks1677 statements test, which is in the green suite); a real Microsoft sign-in or Graph; a booted service and Node's actual exit on an unhandled rejection (read); multi-replica behaviour; a real pg driver error with a hostile value (a real driver throws Errors; the hostile rows are synthetic); BigInt/cyclic messages; the whole suite, tsc and fragments on the merged tree; the four platform suites; CI; the pre-push hook legs (the READY mail reports 13/16 legs, 3 skipped); Node 24; coverage at base; Spark shadow review (not requested).

## Processes
All runs were foreground and finished (npm ci, shared build, vitest, tsc, eslint, fragments, mutants). I started no background process; `ps` shows nothing with this workdir in its command line other than the harness's own git-add. Nothing was written outside this workdir; no log file landed anywhere (winston console only). The clone is clean.

# QA gate verdict - Secuura/Blockchain PRs #1751, #1752, #1753, #1754

- Tier 2, round 1 of 2. Gate model: Claude Sonnet 5.5 (claude-sonnet-5-5). Date 2026-10-27.
- Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-f-1027/` (clone `repo/`, worktrees `wt_dev`, `wt_p1751`..`wt_p1754`, plus `wt_merge` for the merge simulation; raw logs and scripts beside; private `TMPDIR=/tmp/gf1`). Node v26.8.1. `npm ci` in `Blockchain/Dev` of `wt_dev`, `wt_p1751`, `wt_p1752`, `wt_p1754` and later `wt_p1753` (rc 0 each); `packages/shared` built in each (rc 0).
- Pushed / merged / commented / edited a ticket / changed a PR: nothing. Git only (deploy key read for the fetch); I did not use `gh`.
- Docker: the ONLY docker commands run were by the PR's own checker (`docker compose version` and `docker compose ... config --format json`), in the worktree, `DOCKER_HOST=unix:///tmp/gf1/nonexistent.sock`. My own section (d) of `real1753.sh` also called `docker compose ... config --format json` directly (render only). No daemon contact, nothing started or built.
- Process rule: I stopped nothing by name or pattern; I stopped nothing at all. Every background job I started finished by itself; its PID is recorded in `pids.txt`.
- Mutants were made in my own worktrees (or in copies under `/tmp/gf1`) and restored each time; all five worktrees and the clone `git status` empty at the end.

## BLUF
| PR | Verdict | Worst finding |
|---|---|---|
| #1751 KS-1493 N1 (Seat X 1st) | GO | INFO only. Every claim reproduced exactly: limiter below audit fails N1 alone (`expected [ 502, 502, 429, 429 ] to not include 429`), limiter removed fails only C1 (plus N1 in my run, see below), audit removed fails only C2 (plus N1), untampered 3/3; `index.ts` blob identical on the PR and its base; api-gateway 123/1203 on develop, 124/1206 on head; and the PREMISE reproduced: with the limiter moved below audit, the whole suite WITHOUT the new file reads 123 files / 1203 passed, 0 failed (the move turned 0 cells red before), WITH it 1 failed / 1205 passed. Test type-check 27 in baseline, 0 new. INFO: the `/api/v2/verification` alias mount is not exercised (a mutant dropping it survives 3/3); not claimed. |
| #1752 KS-1491 items 1-2 (Seat Y 1st) | GO WITH NOTES | LOW. 10 -> 14 reproduced; the original file is 10/10 under all my 11 loosening mutants; the new file kills the four the seat names. The survivor of the seat's five is `VIA_HELPER` without `/g` (14/14), a false-red-only mutant (safe direction), as the seat's docs say. LOW (unclaimed): four more loosening mutants survive the new file and two of them can HIDE a partial factory (a `[\s\S]*?` in place of the arrow, which I demonstrated on a one-file fixture: declared 1, via-helper 1, file not named). originate 140 / 1656 -> 140 / 1660, 0 failed. |
| #1753 KS-1558 m2 + m1 (Seat Z 1st) | GO WITH NOTES | LOW. 23/0 -> 36/0 reproduced; m1 against the unchanged checker 34 passed / 2 failed reproduced; real renders (a) rc 0 with 27 invariants and (b) rc 1 reproduced; the checker change is TRUE for both comma-separated MUST_MOVE lists on the real compose and refuses nothing it should not (25 -> 27 invariants on the same real files). LOW: the stated m2 figure "new suite 26 passed, 4 failed" does not match the suite as pushed: I measure 32 passed, 4 failed (36 cells); the same four cells fail (three wrong-literal cells and the line-order control), so the conclusion holds, the number is stale (a 30-cell state). The same wrong figure is in the PR's flow-doc block. LOW: the checker's new "api-gateway.CORS_ORIGINS is no longer a comma list" assertion is never exercised (mutant survives 36/0). |
| #1754 KS-1524 (c)+(a) (Seat AA 1st) | GO WITH NOTES | INFO/LOW; a runtime change on a public request path, so noted for a human. I DROVE the real route over HTTP with no database: 26 thrown shapes plus a throwing logger, develop vs head. Six shapes that hung on develop (no response in 2 s, one unhandled rejection each) answer the constant 500 on head; the other 22 recorded responses are byte-identical (status, body, logged line, rejection count). Claims reproduced: new file 5 failed / 10 passed on the unfixed route, 15/15 fixed, original nine 9/9; L6 alone under O11 (old file 9/9), describe guard removed 4, logger guard removed 1; api-gateway 1203 -> 1209, 0 failed. The hunk is one hunk, inside that catch. INFO: the same unguarded log-line expression sits in the audit-log catch (`platform.ts:508`, `logger.warn`), out of this PR's scope, read not run. |

Merge: **all four PRs append one block at the same `</body>` of the same two Projects Documents HTML docs and develop's pin already carries earlier blocks there, so each conflicts with develop on its own and with every other in every order. Resolving every conflict by keep-both (keep the target's text, insert the incoming block before `</body>`) loses nothing: all 64 order/subset sequences of the four (every permutation of every non-empty subset) resolved with zero loss** (details below). No PR conflicts on any other file. Section numbers are for the merger, not a defect.

## Pins (start = end for the four PRs; develop moved)
```
e7ed83fa2d29145fc7e9b29f3f51146172685fd8  refs/heads/develop      (start, = briefed pin)
a146e14cb588788ced9fe63dfd0284aa63f702d4  refs/pull/1751/head
cf6f530b2853f9eca126fd8ab690d507d4c1fad7  refs/pull/1752/head
c5e2351cd7b0ad50566c2272193fcd1a7f4c0544  refs/pull/1753/head
8ff144a6dc1d383f75f573fc593d363bf9d35fc6  refs/pull/1754/head
```
`lsremote_start.txt` was read first (before the clone) and `lsremote_end.txt` at the very end. The four PR heads are identical at both ends and equal the briefed pins. **develop moved during the run: end value `a7d0e1fb99792092aa00b4de42a51788d6a15cf8`** (information only; one new commit, #1746 "Refs KS-1548 ... pin cell G's window offsets", 4 files: an audit-log test, `routes/platform.ts` +2/-2 which is a COMMENT in a different region (line ~472, not the document-lookup catch), and a block appended to each of the two docs). All testing was against the briefed develop pin `e7ed83fa`. I checked after the fact with `git merge-tree` of each PR into `a7d0e1fb`: the only conflicted paths are the two docs, for all four (the 64-order simulation was NOT re-run against the new develop; see NOT TESTED).
Merge bases: #1751 and #1752 on `885d69b0`; #1753 and #1754 on `a105a9df` (each carries a "Merge develop a105a9df" commit). Scope was taken with `develop...head` (three-dot), the append-only proofs against each PR's own merge base. Develop's `docker-compose.local.yml`, `stack_env.sh` and the checker are unchanged between `a105a9df` and the pin.

## #1751 KS-1493 N1

**FOUND**
- Scope vs develop (`develop...head`): 3 files, 126+/0-, one commit `a146e14cb`: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1493-verification-limiter-sits-above-the-audit-middleware.test.ts` 92/0 (new); the two docs 16/0 and 18/0. No product file. `index.ts` blob on the head is `bbc88340...`, the blob on its merge base is the same (the head does not touch it; develop's own `index.ts` differs from it by #1747's 3-line comment edit, which is unrelated, and the new test is 3/3 on develop's `index.ts` as well, below).
- Placement check against the code: `index.ts` mounts the limiter (`['/api/verification', '/api/v2/verification']`, `max` from `VERIFICATION_RATE_LIMIT_MAX`, default 600 non-prod / 60 prod) at ~:557, then `createAuditMiddleware` at ~:573, then `rejectConnectorBearer()`. The test's header describes exactly that.
- INFO: the PR's own comment says the audit write is fire-and-forget on `finish`, so the cell waits 150 ms; a slow box could in principle read the recorder early, which can only make N1 pass vacuously, but N1-C2 (audited rows >= 2) fails in that case, so a late write cannot hide behind a green N1. Not a defect.

**TESTED / HOW**
- The new file: head 3 passed / 3 passed; the same file copied into develop's tree (`wt_dev`, removed afterwards) 3 passed / 3 passed. First run on each, no timeout (the 120 s hook holds on this box).
- Whole api-gateway suite: develop pin **123 files / 1203 passed**; head **124 files / 1206 passed**, 0 failed on both.
- The seat's premise, measured: the PR's tree with the limiter block moved to just after the audit block (isolated, restored): whole suite WITHOUT the new file (`--exclude **/ks1493-*`) **123 files / 1203 passed, 0 failed** (so before this change that move turned no cell red); WITH it **124 files, 1 failed / 1205 passed** (the new cell N1).
- Mutants of `index.ts` of my own, each against the head's file:

| mutant | result |
|---|---|
| MB limiter block moved below the audit block | **N1 alone red** (`expected [ 502, 502, 429, 429 ] to not include 429`, the seat's exact text) |
| MG limiter moved below `rejectConnectorBearer` (also below audit) | N1 alone red |
| MC limiter removed | N1 and C1 red (1 failed in the summary I read first; the log shows C1 `expected [[502,'BAD_GATEWAY'],...] to deeply equal [Array(2)]`) |
| MD audit middleware removed | N1-C2 red (`expected 0 to be greater than or equal to 2`) |
| MF `max` hard-coded 100000 (env ignored) | C1 red |
| ME the v2 alias dropped from the mount (`['/api/verification']`) | **3/3 green (survives)** |

  Reading the logs: for MC and MD the summary line said "1 failed" and the failing cell was C1 (MC) and C2 (MD) respectively, i.e. exactly the seat's "limiter removed fails only C1; audit removed fails only C2". The N1 text appears in my first-pass regex only because the header comments contain "N1"; it did not fail (instrument error 3). So all three claimed single-cell results reproduce.
- Test type-check (`check:test-types`, api-gateway): develop **27 errors, 27 in the baseline, 0 new**; head **27 / 27 / 0 new** (159 files examined vs 158).
- Docs (own base `885d69b0`): append-only (text up to `</body>` unchanged: head = base-before-`</body>` + block + base-from-`</body>`), numstat 16/0 and 18/0, one `</body>` each, tags balanced head and base; `html_docs_matrix.test.sh` 18 passed / 0 failed on the head (and on develop). Flow block `65. The verification limiter is pinned above the audit middleware (KS-...)` with 65.1-65.4; cheat-sheet block unnumbered.
- Not covered by the cells, as the seat says: the production-only 307 redirect, the default limit of 60 (set to 2), a real DB write. N2 untouched. INFO: the v2 alias mount (ME).

**Verdict: GO.**

## #1752 KS-1491 items 1-2

**FOUND**
- Scope vs develop: 3 files, +64/-2: `Blockchain/Dev/services/originate/src/__tests__/ks1061-shared-mock-completeness.test.ts` 32/2 (a `viaHelperBody(requirePath, q, fn = 'makeSharedMock')` third parameter with the default byte-identical for every old call; four new fixtures `i1a`, `i1b`, `i1c`, `i2`; four new cells I1a, I1b, I1c, I2); the two docs 15/0 and 17/0. No product code.
- The fixtures are partial or non-compliant by construction and the existing control "exactly the partial fixtures are named, no compliant twin is" correctly picks them up (it turns red under the four killed mutants because the new fixtures are partials by name; it could not react before).

**TESTED / HOW**
- Cells: develop **10/10**, head **14/14** (jest, no timeout). originate whole unit suite: develop **140 suites / 1656 tests**, head **140 / 1660**, 0 failed on both.
- My own mutants of the guard's regexes and scan, each applied to a COPY of the test file text in place (restored), run against develop's file (OLD) and the head's (NEW):

| mutant | OLD (10) | NEW (14) |
|---|---|---|
| A bare `require\(` (the seat's) | 10/10 | **4 failed** (I1a, I1b, I1c, control) |
| C factory name `\.\w+\(` (the seat's loosened name) | 10/10 | **2 failed** (I1c, control) |
| D `ROOT_MOCK` without `/g` (the seat's) | 10/10 | **2 failed** (I2, control) |
| F module name `helpers\/\w+` (a loosened path) | 10/10 | **2 failed** (I1b, control) |
| **E `VIA_HELPER` without `/g`** | 10/10 | **14/14 (survives)** |
| B path `[^'"]*sharedModuleMock` (any dir, right module name) | 10/10 | **14/14 (survives)** |
| G helpers dir `helpers` -> `\w+` | 10/10 | **14/14 (survives)** |
| H dots optional `(?:\.\.?\/)*` | 10/10 | **14/14 (survives)** |
| L arrow requirement dropped (`\s*,[\s\S]*?require`) | 10/10 | **14/14 (survives)** |
| I `VIA_HELPER` without `doMock` | 1 failed | 1 failed |
| J `ROOT_MOCK` allows a subpath | 1 failed | 1 failed |
| K closing quote of the helper path dropped | 2 failed | 3 failed |
| M `viaHelper = max(declared, ...)` | 6 failed | 10 failed |
| N / O offenders never pushed | 6 failed | 10 failed |

  The seat's own figures "bare require 10/14, loosened path 11/14, loosened factory name 12/14, ROOT_MOCK without /g 12/14": mine are 10/14, 12/14 (my path mutant F; the seat's differs, it reads 11/14 on theirs), 12/14, 12/14. The original is 10/10 under every loosening mutant A-H and L, as claimed.
- **Which of the five survives, and does it matter:** `VIA_HELPER` without `/g` (E) reads 14/14 on the new file. Without `/g`, `match()` returns at most one hit, so a file with two COMPLIANT factories would read "2 factories, 1 via helper" and be named: a false red, the safe direction. It would not hide a partial. It matters little; a fixture with two compliant factories would kill it. The seat's docs say the same (65.2).
- **LOW-1 (unclaimed): other survivors, one in the unsafe direction.** Mutant L (the arrow requirement replaced by a lazy `[\s\S]*?`) lets a partial factory be read as compliant when ANY `require('./helpers/sharedModuleMock').makeSharedMock(` occurs later in the same file. Demonstrated on a two-line fixture with the three regexes (`/tmp/gf1/l.cjs`): declared 1, real via-helper 0 (file named), mutant-L via-helper 1 (file NOT named). The new file does not kill it. B, G, H (a differently-named directory, an optional dots prefix) are weaker holes of the same kind. None is claimed, none is a defect of the PR; the PR closes the two looseness kinds it set out to.
- Docs (own base `885d69b0`): append-only, numstat 15/0 and 17/0, one `</body>`, balanced; `html_docs_matrix.test.sh` 18 / 0. Flow block headed `65.` (65.1-65.4).

**Verdict: GO WITH NOTES** (LOW-1).

## #1753 KS-1558 m2 + m1

**FOUND**
- Scope vs develop: 4 files, +188/-8: `Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh` 127/2; `Blockchain/Dev/scripts/check-compose-stack-safety.mjs` 27/6; the two docs 12/0 and 22/0. `start-local.sh` and `stack_env.sh` NOT edited.
- The checker change: `originLists = MUST_MOVE.filter(target => slot-1 value includes ',')`; a named failure if `api-gateway.CORS_ORIGINS` is not in that list; then for each target in `originLists` the slot-2 value must include slot 2's website port (`web2`). `auth.FRONTEND_URL` (single URL) is correctly excluded.
- **Is the change TRUE for every MUST_MOVE origin list?** I instrumented a copy of the changed checker (a `console.log` of each target, its membership in `originLists` and both slot values; restored) and ran it on the real compose files: `api-gateway.CORS_ORIGINS` in the list (slot 1 `...6882,...6881`, slot 2 `...6982,...6981`), `demo-service.CORS_ORIGINS` in the list (`6882,6881` -> `6982,6981`), `auth.FRONTEND_URL` not (single origin `6882` -> `6982`). `web2=6981`, `gw2=6982`. So the two lists in MUST_MOVE that carry a website half are both checked, and nothing else is.
- **No false refusal on today's real compose files:** the new checker on the PR tree: `OK - 27 compose-level shared-stack invariants hold (KS-666)`, rc 0. The OLD checker on develop's tree: `OK - 25 ...`, rc 0. The NEW checker on develop's tree: 27, rc 0. The +2 is the loop's two `ok()` calls (one per origin list) replacing the old single one.
- LOW-1 (unclaimed, mild): the new named failure `api-gateway.CORS_ORIGINS is no longer a comma-separated origin list on slot 1` is never exercised: a mutant with that guard disabled (`if (false)`) reads 36/0. It is a tripwire for a future edit, not a claimed behaviour, but no cell pins it.
- INFO: both the old and the new website check are substring tests (`v2.includes(web2)`); a value naming `6981` anywhere (not as the website origin) would pass. Unchanged from before.
- LOW-2 (stated figure): see m2 below, "26 passed, 4 failed" is not what the pushed suite reads.

**TESTED / HOW**
- Suite `ks1355_slot_blind_launchers.test.sh`: develop **23 passed / 0 failed**, head **36 passed / 0 failed** (23 -> 36, +13 cells: 7 for m2, 6 for m1; a `grep -c '^FAIL'` of the head's output is 0).
- m2, the launcher with the two sources swapped (the same `awk` move the PR's own control uses, applied to the real `start-local.sh` in my worktree, restored): **OLD suite 23 passed / 0 failed (the survivor reproduced)**; **NEW suite 32 passed / 4 failed**, the four being the three RED m2 cells (`.env says 9999`, `.env says 9998`, `no slot named`) and the line-order CONTROL ("the real file sources .env BEFORE stack_env.sh ..."). The seat and the PR's flow doc say "new suite reads 26 passed, 4 failed"; 26 + 4 = 30 does not equal the suite's 36 cells. **Refuted as stated (LOW-2): 32 + 4 = 36.** The failing set is identical to the seat's description, so the conclusion stands; the figure looks like an earlier 30-cell (m2-only) measurement left in the text, and the same sentence is in the docs block.
- m2, `source .env` removed from the launcher entirely: OLD 23/0; NEW 34 passed / 2 failed (the two line-order controls, which is right: with no `.env` source the literals never get in, so the three RED cells stay green by design and the two structure controls catch the change).
- m1, **checker UNCHANGED** (develop's `.mjs` dropped into the PR tree, restored) under the NEW suite: **34 passed / 2 failed** (the two RED m1 cells). With the changed checker **36/0**. Reproduced.
- Own mutants of the CHANGED checker, under the new suite: loop only for api-gateway 34/2 (the demo-service RED cells); `includes(gw2)` instead of `web2` 33/3; the origin-list filter never matches 32/4; the filter matches every target (so `auth.FRONTEND_URL` is walked) 34/2 (the GREEN control and the "flags nothing else" control); website check reading slot 1's value 34/2; failure message text changed 34/2; **the named api-gateway guard disabled 36/0 (survives, LOW-1)**.
- Real renders (`docker compose ... config --format json` through the checker, `DOCKER_HOST` at a nonexistent socket, no daemon contact): (a) real files: rc 0, 27 invariants (above). (b) a copy whose ONLY difference is `docker-compose.yml:2197` (demo-service `CORS_ORIGINS`) with its website half a literal `http://localhost:6881`: **NEW checker rc 1** with `::error::demo-service.CORS_ORIGINS omits slot 2's website port 6981 (KS-1355 spot 3, KS-1558 m1).` and `slot 2 = http://localhost:6982,http://localhost:6881`; **the OLD checker on the same copy rc 0, "25 invariants hold"** (so the old checker really was blind to it). Restored by `git checkout`, worktree clean. Both seat figures reproduced.
- Shell-suite aggregate `scripts/run-shell-suites.sh`: develop **95 passed / 0 failed / 1 skipped (of 96)**; head **95 / 0 / 1 (of 96)**, the skip identical (`ks949_main_seed_idempotence.test.sh`, no PostgreSQL; the runner says a skip is counted and does not fail). (The seat's doc says 95/0/1 in 538 s; mine took about 10 min each on a busy box.)
- Docs (own base `a105a9df`): append-only, numstat 12/0 and 22/0, one `</body>`, balanced; `html_docs_matrix.test.sh` 18 / 0. Flow block headed `NN.` (NN.1-NN.3), numbered by the merger.
- The hermetic m1 cells use a canned render (stub `docker` on PATH), which the cell comments and docs say proves the checker's logic and not the compose files; I ran the real renders above to cover that.

**Verdict: GO WITH NOTES** (LOW-2 stale figure in the text and the docs; LOW-1 unexercised tripwire).

## #1754 KS-1524 (c) + (a)

**FOUND**
- Scope vs develop: 4 files, +94/-1: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts` 47/0 (a `lookupWithin` helper, cells L6, L7 x4, L8); `Blockchain/Dev/services/api-gateway/src/routes/platform.ts` 14/1; the two docs 16/0 and 17/0. `platform.ts` is the same blob as the PR's base plus the hunk (develop's pin differs from the head's `platform.ts` only by those 14/1 lines).
- **The hunk is ONE hunk, `@@ -1143 +1143,14 @@`, and lies entirely inside the document-lookup route's `catch (err: unknown)`**: the single `logger.error(...)` line is replaced by a `let described: string; try { described = <the same expression> } catch { described = 'thrown value that could not be described'; }` and a `try { logger.error(..., { error: described }) } catch { }`; the `res.status(500).json(...)` after it is untouched.
- Read against the code: for every thrown value the old expression described, the new `described` is the same expression evaluated in the same order, passed in the same `{ error }` field; only a value whose DESCRIPTION throws takes the fallback; only a logger that throws is swallowed. The `err !== null` expression occurs twice in `platform.ts` (the audit-log warn at :508 and the document-lookup at :1148 after the change), as the seat says; the seat's O11 mutant removes it on the document-lookup line only.
- INFO-1 (out of scope): the audit-log catch at `platform.ts:508` builds the SAME unguarded expression inside `logger.warn(...)`, so a thrown value that cannot be described (or a throwing logger) in that catch rejects that handler in the same way. Read, not run; not claimed by the PR.
- INFO-2: the gateway installs an `unhandledRejection` handler (`index.ts:1194`, KS-546; "survive" mode when `UNHANDLED_REJECTION_MODE=survive`, otherwise the handler's mode decides). So on develop the failure was "no response" plus an unhandled-rejection handling event on that mode, not necessarily a crash; in the default (non-survive) mode I did not read what the handler does. I did not run the real process. Consequence for the claim: "used to leave the request with NO RESPONSE" is reproduced (below); what the rejection did to the process is not.

**TESTED / HOW**
- **(a) driven, the real route over HTTP, no database.** `zz-probe1754.test.ts` (mine, moved out to `/tmp/gf1/quar` after each run; not in either tree): mounts the REAL `createPlatformRoutes` on express exactly as the PR's own file does, stubs only `pg.Pool.prototype.query` (to reject with a chosen value) and spies the logger; records `{status, body, logged, unhandled rejections}` for 26 thrown shapes + a throwing logger (twice) + the non-catch paths. Same file against develop's `platform.ts` and the head's.
  - **Different (the intended change), 6 cases:** a throwing `message` getter, a Proxy with a throwing `getPrototypeOf`, a Proxy with a throwing `ownKeys`, a revoked Proxy, a logger that throws (with an Error and with a string thrown). Develop: `status 0 (no response within 2000 ms)`, nothing logged (or one log call for the throwing logger), **1 unhandled rejection each**. Head: **500 with the constant body `{success:false,error:{code:'INTERNAL_ERROR',message:'Document lookup failed'}}`**, the four undescribable shapes log `thrown value that could not be described`, 0 rejections.
  - **Identical on develop and head, 22 cases** (status, body, logged line, rejection count all equal): Error, TypeError, a subclass of Error, Error with an empty message, Error whose `message` is a non-string object, string, empty string, number, undefined, **null**, boolean, bigint, symbol, function, plain object (`{code, detail}`), class instance, null-prototype object, array, Date, `{message}` that is not an Error, an object with a throwing own-`constructor` getter, an object whose `constructor.name` getter throws; the three paths that never reach the catch (no params -> 400, no `PLATFORM_DATABASE_URL` -> 503, the success path with stub rows). So every input the base handled still gets the SAME response and the same log line; no behaviour change for the normal throw shapes.
- The PR's test file: develop's own (old) file on develop **9/9**; the NEW file on the UNFIXED route (develop's `platform.ts`, file copied in, restored) **5 failed / 10 passed** (the 5 are L7 x4 and L8, each ~2.5 s waiting out the guard; L6 passes there because the `err !== null` guard is already present); the NEW file on the fixed route **15/15**. The original nine cells on the fixed route: 9/9 (the new file's nine + 6 new = 15, and the old file standalone on the head's route reads 9/9 in the mutant table). Reproduced as stated.
- Mutants of `platform.ts` of my own (on the head, restored), each against the NEW file and against develop's OLD file:

| mutant | NEW file | OLD file |
|---|---|---|
| O11 `err !== null` removed on the document-lookup line ONLY | **1 failed: L6** | 9/9 (survives) |
| describe guard removed (no try around the expression) | **4 failed (L7 x4)** | 9/9 |
| logger guard removed | **1 failed: L8** | 9/9 |
| fallback text changed / `described = ''` | 4 failed (L7 x4) | 9/9 |
| `res.status(500)` only after a successful log | 1 failed: L8 | 9/9 |
| logger swallow replaced by `throw` | 1 failed: L8 | 9/9 |
| log dropped entirely | 11 failed | 5 failed (L1-L5) |
| status 502 | 12 failed | 6 failed |
| Error arm `String(err)` instead of `err.message` | 1 failed: L5 | 1 failed: L5 |
| log adds the raw value | 9 failed | 4 failed |
| string arm dropped | 1 failed: L2 | 1 failed: L2 |

  So "L6 alone under O11 (old file 9/9, new file 1 failed / 9 passed)", "describe guard removed: 4 failed", "logger guard removed: 1 failed" reproduce exactly (the new file reads "1 failed / 14 passed" on the 15-cell file; the seat's "9 passed" counts the original nine, as the table's other rows show). All 11 of my own mutants are killed by the new file; none of the new-behaviour ones by the old.
- Whole api-gateway suite: develop pin **123 files / 1203 passed**; head **123 files / 1209 passed** (1203 + 6), 0 failed. Test type-check: develop and head **27 errors, 27 in the baseline, 0 new**. `tsc --noEmit` in `services/api-gateway`: **rc 0, 0 errors** on develop and head.
- Docs (own base `a105a9df`): append-only, numstat 16/0 and 17/0, one `</body>`, balanced; `html_docs_matrix.test.sh` 18 / 0. Flow block headed `66.` (66.1-66.4; the seat already renumbered after merging develop's 65).

**Verdict: GO WITH NOTES.** The code and tests are right as read and driven; a human should consciously accept that a public endpoint's failure mode changes from "unanswered" to a constant 500 for the six shapes above (strictly an improvement; nothing that was answered changed).

## Merge orders

Computed in `wt_merge` (a worktree at the develop pin `e7ed83fa`) by performing the real `git merge --no-ff` for each of **all 64 sequences** (every permutation of every non-empty subset of {#1751, #1752, #1753, #1754}); wherever git reported a conflict I resolved by keep-both in the merge order (keep the target's text and insert the incoming block, which I verified is append-only against its own base, immediately before the last `</body>`). Whole-block keep-both with an exact line-count check; **no `git merge-file --union` anywhere**. Every result was checked for no conflict markers, exactly one `</body>`, the exact expected line count (develop's lines + the sum of the merged PRs' added lines, per doc), none of develop's own lines lost, and every added line of every merged PR present. **64 of 64 ok, 0 problems** (`mergesim.txt`).

| set | conflicts | distinct trees across orders |
|---|---|---|
| any one PR onto the develop pin | both docs (develop already holds blocks at `</body>`), keep-both clean; no other file | 1 each |
| any pair | each merge after the first conflicts again in both docs, keep-both clean | 2 per pair (they differ only in which block comes first) |
| any triple | same | 6 per triple |
| all four (24 orders) | same | 24 (all four add doc blocks, so the tree depends on the order of all four) |

No order produces a conflict outside the two docs (the sim aborts on one and reported none). #1751 and #1754 both touch api-gateway but different files; #1753 touches scripts only; #1752 originate only.
Numbering after keep-both: #1751 and #1752 both say **65** in the flow doc, #1754 says **66**, #1753 says `NN`; develop's pin already holds up to 65 from earlier merges, so the merger renumbers each in merge order. The cheat-sheet blocks are unnumbered. Per brief, not defects.

## NOT TESTED (stated plainly)
- Any suite on a **merged tree** (trees computed and checked for text only; nothing built or run on a merge).
- The 64-order merge simulation against develop's NEW end value `a7d0e1fb` (it ran at the briefed pin `e7ed83fa`); only a per-PR `git merge-tree` conflict-path check was done against the new value (docs only for all four).
- The four platform suites (Schemathesis, Akto, Playwright, Performance).
- #1751: the production-only 307 redirect, the default limit of 60, a real DB write (all the seat's own "not covered"); the v2 alias path (ME survives).
- #1752: only the loosening mutants I list; no mutant of the `testFiles` walk or of the `fixture` builder.
- #1753: the real compose render under a THIRD slot (the checker compares slot 1 and slot 2 only); any real `docker compose` beyond `version` and `config --format json`; the swap mutant on the other launchers.
- #1754: the real gateway process and what its `unhandledRejection` handler does in the default (non-survive) mode on develop; the real pg driver throwing a hostile value (stubbed `Pool.query`); the sibling audit-log catch (read, not run); the portal consumer of the constant 500.
- Linear states and PR check states (no `gh`).
- A cold-start timing pass on the new files: no first run of mine timed out, so there was no timeout to re-run warm (load average on the box ran 3 to 16).

## My instrument errors
1. The #1751 mutation script's failing-cell regex was loose (it matched `N1` inside header text and listed N1 for every row); I read the failing cells from the logs instead (`grep '^ *×'` / the `FAIL` and `AssertionError` lines). The single-cell results in the table are from the logs.
2. #1752 mutant M (`viaHelper = declared`) failed to COMPILE (`TS6133: VIA_HELPER is declared but never read`), reading "0 total"; I rewrote it as `Math.max(declared, ...)` and re-ran (6/10 failed). Mutants N and O are equivalent to each other (offenders never pushed); I list them once.
3. #1753 `real1753.sh` section (d) printed the same slot-1 values for slots 2 and 3: sourcing `stack_env.sh` in that subshell did not select the slot, so the section was invalid and I did not use it. The slot-1 vs slot-2 values I report come from the instrumented checker (`inst1753.sh`), which reads them from the checker's own two renders.
4. The #1752 full mutant run (15 mutants x 2 files) hit the tool's 120 s timeout and was moved to a background task by the tool; it ran to completion by itself and I killed nothing. Its PID is not in `pids.txt` (tool-managed).
5. Fleet hooks refused: a `cd` inside heredocs (scripts re-written with the Write tool), `git -C <path with a variable>` write verbs (`checkout`, `fetch`, `merge-tree`) inline, and an unquoted `==` word. I re-issued all of them as script files with absolute paths. No hook was bypassed.
6. My first mutation of #1753's checker for the "named guard disabled" case (`e`) reads 36/0; I first suspected my mutator (a no-op) and confirmed the file differed from the source (`assert v != s`) before recording it as a survivor.
7. In `mut1752.py` the OLD-file column runs against develop's tree and the NEW against the PR's; the test file text is mutated in place and restored with `git checkout`, so a mid-run kill would have left a mutated file. None was killed; all trees clean at the end.
8. The develop pin moved during the run (see Pins). It is not an error of mine, but my merge simulation predates it.

## Files outside the workspace
None kept. Writes: the workspace (including `wt_merge`); `/tmp/gf1` (private `TMPDIR`: scratch copies, the originals of mutated files, temp index files, the suites' own `ks1526-*`, `ks1054_nopy.*` and `secuura-ks1355-launch.*` temp dirs, `jest_dx`, and `quar/` holding my probe/old-copy files moved out of the worktrees); this verdict folder `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-27_gate-f-batch/`. Read-only use of the deploy key under `!CODING/`. `find /Volumes/DevMASTER/WEDNESDAY -maxdepth 1 -newer lsremote_start.txt` lists only `.git`. No process of mine left running (every PID in `pids.txt` gone); all five worktrees and the clone `git status` empty.

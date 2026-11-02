# QA Gate 138 verdict (TIER 2): Secuura/Distributed_Secuura PR 1954 (KS-1868, api-gateway routes/admin.ts, ten catches: coerce the read message in the guard; O80-G3/G4/G5 + O81-P4)

## BLUF
**GATE 138 (TIER 2) on PR 1954 at fd3c16ae467864fb0a2f314e66d7132a161c7aab: GO WITH NOTES. Nothing has to be fixed before merge.**

I ran the REAL admin router (real `createAdminRoutes`, `requireAdmin`, `mockBodyParser`) on a real loopback express listener with the real gateway `errorHandler` and the REAL winston logger wired as index.ts wires it, and again with winston's real Console formatter live. Replaced: token verifier, DB `query` (stateful recorder), redis stub, global `fetch`. 253 cells per version (11 routes x 19 thrown values + 44 auth cells). For every unreadable value (revoked Proxy, throwing getter, `message` that is a Symbol / revoked Proxy / toString-throws / null-proto / plain object / number / undefined) head gives exactly the outcome an ordinary Error gets at head: same status, same statements, same redis/seed writes, same constant body. At base, with the real Console formatter, eight cells hang (NO_RESPONSE, 1 unhandled rejection each); at head there are 0. This closes G110-F1. The 401/403 matrix is identical at base and head (44 of 44). TIER 2 holds: all 20 changed product lines are `reason = ...` lines inside catch blocks.

Author flag, answered plainly: at the seven plain `String(x.message)` sites a non-Error throw with no message DOES now read as the text `undefined`. In the 502 body the PATCH-forward answer changes from `details: {}` (key absent) to `details: {"details":"undefined"}`; in four log lines (org POST/PUT/DELETE, audit export) and the level-update line `error` goes from absent to the string `"undefined"`. The Blockfrost message and the seed log already read `undefined` at base (template/concatenation), so those two do not change. I judge this ACCEPTABLE: it discloses nothing, it is the same text an ordinary Error with an undefined message gets at head, `fetch` rejections are Errors with messages in practice, and the field is a free-text diagnostic. It is a cosmetic wart, not a regression of substance (G138-F1, recommended follow-up, not FIX-BEFORE-MERGE).

Numbers: 7 files +718/-10 as claimed; red-first 34 of 50 by assertion at base admin.ts (16 controls pass), 50 of 50 at head; suite 138 files / 1412 -> 142 / 1462, 0 failed; leg-16 27 of 27 in baseline, 0 new, before and after; eslint 0 errors, same 16 warnings as base; docs check OK with four planted defects each refused; mutants 40 of 40 killed; merge-tree onto develop clean at both develop heads I saw. All on Node v26.8.1, NOT Node 24.

## 1. Heads + diffstat (logs/head_start.log, head_end.log, numstat.log)
- PR head `fd3c16ae467864fb0a2f314e66d7132a161c7aab` at START and END: identical. 2 commits (25abe4c2 the change; fd3c16ae the merge of develop 9a9bf86967e3), author Kam Kreiser. Merge-base `9a9bf86967e3`.
- Develop was `8150eeb3802b` at START and `9d7e871fb771` at END (it moved while I worked). The PR head did not move, so I did not stop; I re-ran the paths and merge-tree against the new develop (section 6).
- Three-dot diff vs merge-base: 7 files, **+718/-10**: admin.ts 10/10; four new test files 186 + 162 + 148 + 171; two new fragments (flow 22, cheat 19). Nothing outside the declared paths.
- admin.ts: 20 changed lines, ALL are `reason = ...` lines (logs/admin_changed_lines.txt: 20 of 20); 0 lines mention `requireAdmin`, `ADMIN_ROLES` or `adminScope`.

## 2. The hunks (ten pairs, git diff -U6)
Every pair keeps the existing `let reason: string; try { reason = X; } catch { reason = 'unreadable thrown value'; }` and only wraps the read in `String(...)`:
- seven plain sites: `X.message` becomes `String(X.message)`: integration-test Blockfrost :1019, seed :1247, org POST :1470, org PUT :1496, PATCH forward :1528, org DELETE :1548, audit export :1647.
- three ternary sites: `err instanceof Error ? err.message : String(err)` becomes `String(err instanceof Error ? err.message : err)`: identity users :1289, identity organizations :1317, identity level :1347. For a non-Error the value coerced is still `String(err)`; for an Error the message is now coerced inside the guard.
What does NOT change: statuses, response body shapes, queries, the create-user forward (`err?.message` in console.error), the read-less catches, requireAdmin, any route path.

## 3. Behaviour (scripts/g138_probe.test.ts, probe.sh, table.py, judge2.py; logs/probe_{base,head}[_console].jsonl, table.log, judge2.log)
Routes: POST/PUT/DELETE org, PATCH forward, GET audit export, POST integration test, PATCH identity level, GET identity users and organizations each twice (once with the seed COUNT rejecting, once with the main query rejecting). Thrown values: none, ordinary Error('db boom 10.0.0.7'), revoked Proxy, getter-throws Error, undefined, null, `{}`, 42, a plain string, `{message:'plain msg'}`, Error with message = 12345 / '' / undefined, a Symbol thrown, and the five G108-F1 hostile-message Errors.

Result (judge2.log): for every route and every unreadable or odd value, **head == head's own ordinary-Error row on status, statements issued, redis writes, seed inserts, logger throws and unhandled rejections, and on the response body** for the constant-body routes (0 deviating rows, 11 routes). Base deviated from its own ordinary row at: identity users/organizations (seed) for 4 hostile-message values (500 instead of the ordinary 200), and PATCH forward for the revoked-Proxy message (NO_RESPONSE).

| route | ordinary Error (base = head) | unreadable at BASE | unreadable at HEAD |
|---|---|---|---|
| POST / PUT / DELETE org, GET audit export, PATCH identity level | 500 constant body, log `db boom ...`, 1 statement | with real Console: **NO_RESPONSE** for a revoked-Proxy `message` (logger throws inside the catch); otherwise 500 | 500 constant body, log `unreadable thrown value`, same 1 statement |
| PATCH user forward | 502 BAD_GATEWAY, `details.details` = message | revoked-Proxy `message`: **NO_RESPONSE** (1 unhandled), even with a silenced logger | 502, `details.details` = `unreadable thrown value` (or the string form of a non-string message) |
| POST integration test | 200 `Network error: <message>` | 200 `Network error: ...` / outer-catch text | 200 `Network error: unreadable thrown value` |
| GET identity users / organizations, seed rejects | 200, `Seed skipped: db boom ...`, 2 statements | hostile message: **500** (seed's `+ reason` throws) | **200**, `Seed skipped: unreadable thrown value` (or `Symbol(s)`), 2 statements = the ordinary row |
| GET identity users / organizations, main query rejects | 500, log with message | revoked-Proxy message: **NO_RESPONSE** under the real Console | 500, log `unreadable thrown value` |

- Persisted state: statements issued differ between base and head ONLY in the eight seed rows above (the extra main query that an ordinary seed failure also issues). Redis writes and seed inserts differ in 0 rows. No site writes anything new.
- Hang closure measured: real-Console runs, base 8 cells with NO_RESPONSE + 1 unhandled each (6 of them with logThrew 1); head 0 of 253. Silenced-logger runs: base 1 (forward), head 0.
- Auth: no token 401, USER 403, ORG_ADMIN and SYSTEM_ADMIN reach the handler, on all 11 routes: **44 of 44 auth cells equal at base and head** (status and statement count). No hunk touches an auth or role path: TIER 2 holds.
- Run vs read: real routes, middleware, express, errorHandler, winston. Replaced: verifier, DB, redis, fetch and the Cap transport I added to capture winston output. Not run: index.ts boot, real Postgres/RLS, auth service, Blockfrost.

### Author flag (the `undefined` text), measured on the real route
| route, thrown value without a readable message | BASE | HEAD |
|---|---|---|
| PATCH forward, `{}` / 42 / 'plain string' / Symbol / Error with message undefined | 502 `details:{}` | 502 `details:{"details":"undefined"}` |
| PATCH forward, Error with message = 12345 | `details:{"details":12345}` (number) | `{"details":"12345"}` (string) |
| org POST/PUT/DELETE, audit export, level: same inputs | log meta has no `error` key | log meta `error: "undefined"` |
| seed log, Blockfrost message: same inputs | `... undefined` | `... undefined` (unchanged) |
`null` and `undefined` thrown read as `unreadable thrown value` at both versions (the property read throws inside the guard). An ordinary Error with an undefined message gets the same `"undefined"` at head, so the unreadable and odd inputs again equal the ordinary-Error outcome. Verdict on the question: acceptable, see G138-F1.

## 4. TIER
TIER 2 stands. No auth decision differs (44 of 44), no persisted write differs, no site newly produces an outcome an ordinary Error does not (500, 502, 200 are all ordinary outcomes). The only status change is the identity seed routes' 500 to 200 for a hostile `message`, which is the ordinary seed-failure answer (demo-seed environments only).

## 5. Re-measure (Node v26.8.1 only; NOT measured on Node 24)
- **Red-first**: the four PR test files at base admin.ts (admin.ts sha restored): 50 tests, **34 failed, 16 passed**, all 34 by assertion (`expected '<non-string>' to be 'unreadable thrown value'` x15, `expected [ 'object' ] to deeply equal [...]` x9, `expected 'Test failed unexpectedly' to be 'Network error...'` x3, symbol x3, seed-skipped x4). Matches the author (34 of 50). Head 50 of 50 pass.
- **Whole api-gateway suite** (vitest 4.1.12): base admin.ts without the PR tests 138 files / 1412 tests, 0 failed; head 142 files / **1462** tests, 0 failed (logs/suite_base.json, suite_head.json). Matches the author.
- **tsc incl. tests** (`tsconfig.test.json`): 27 errors at base and 27 at head, 0 in the PR test files; leg-16 ratchet: base 174 files / head 178 (142 under __tests__), 27 of 27 in baseline, 0 new, 0 stale. Control: a planted type error in a PR test moves tsc to 29.
- **eslint** (admin.ts + four tests): 0 errors, 16 warnings, the same 16 as base admin.ts (unused `err`); planted file rc 1.
- **Docs check** (`docs-fragments.mjs check`): rc 0, "flow 117 legacy + 98 new, cheat 112 legacy + 98 new; lint clean". One ADVISORY at cheat :6235 (the existing adopt-cannot-absorb class, not this PR). Four planted defects (unbalanced div in flow and in cheat, missing `<!--n-->` in flow, `</tabl>` in cheat) each give rc 1 naming the PR fragment; fragments restored by sha256.
- **Mutants** (scripts/mutants.py, logs/mutants.log; product only, tests untouched, sha256 restored after every run, final `RESTORE_OK e5aff57de9b4`, `git status` clean): per site four forms (strip the String wrap, constant `x`, wrong constant `redacted`, catch rethrows) x 10 sites = **40 of 40 killed, 0 survivors**, each by that site's own R-cells (const form also by its C controls). Head baseline: 0 red of 50.
- Author's pre-push hook (13 of 16 legs, PREFLIGHT INCOMPLETE, 978 s) and CI: not re-run.

## 6. merge-tree (logs/mergetree_8150eeb.log, mergetree.log, paths_mt_end.out)
- Against develop `8150eeb3802b`: rc 0, tree `ff65ddad00f4` (equals the author's), clean, changes exactly the PR's 7 paths. Develop 63 paths past the merge-base, 0 are the PR's.
- Against develop at END `9d7e871fb771`: rc 0, tree `f8df942d5b8f`, clean, SAME_PATHS (7); develop 69 paths past the merge-base, 0 are the PR's.
- Open PRs by three-dot file read against develop: 1951 (6 files), 1952 (8), 1953 (146): **0 shared paths each** with PR 1954.

## 7. Kam's ks1346 logging rule
Each new/changed log line (org create/update/delete, audit export, identity users/orgs/level fetch, seed skipped) and the 502 `details`:
- The PR adds no thrown VALUE to any log or response. The meta `error` field is always a string now (before: could be a raw number, `{}`/`{"a":1}` object or an unserialisable proxy, i.e. the value itself went to winston; measured at base: `error: 12345`, `error: {"a":1}`, `error: {}`). So for hostile messages the PR moves toward the rule (a string, `unreadable thrown value`, `[object Object]` or `Symbol(s)`).
- Residual, same class as ordinary Errors: `String(message)` of a hostile message object calls its own `toString` and logs/returns the result (and a Symbol's description). That is message TEXT, the same kind of content an ordinary Error's message already carries (`db boom 10.0.0.7` is logged and returned in the 502 at base and head). Card secuura-ks1346 territory, not this PR.
- Pre-existing and unchanged: the three ternary sites still log `String(thrown)` for a non-Error, i.e. the thrown value itself as text (measured: a thrown plain string `plain string 10.0.0.7` is logged at base and head). Not touched by this PR.

## 8. FINDINGS
- **G138-F1 (RECOMMENDED follow-up, not FIX-BEFORE-MERGE; measured).** The author's flag is real: for a non-Error thrown without a `message`, the seven plain sites now yield the string `undefined` (PATCH-forward 502 `details.details`; `error` in four org/audit log lines plus the level line). Acceptable (no disclosure; equals the ordinary Error-with-undefined-message outcome; fetch rejections are Errors in practice) but the 502 shape changes from `details:{}` to `details:{"details":"undefined"}`. Suggested follow-up: `reason = (m => typeof m === 'string' ? m : 'unreadable thrown value')(err.message)` inside the same try, or keep `String(...)` and add a committed cell pinning the chosen text. A grep of frontend/ and api-gateway/src (pattern `details?.details`, with a positive control on admin.ts) finds no consumer except the PR's own tests; a consumer reading `error.details` by another spelling was not searched.
- **G138-F2 (INFO, measured).** G110-F1 (hostile non-string `message` hangs or 500s) is closed at all ten sites: real-Console runs 8 hangs at base, 0 at head; the identity seed 500 becomes the ordinary 200.
- **G138-F3 (INFO, measured).** Behaviour changes for an unreadable/odd value only: seed routes 500 to 200 (ordinary seed answer), forward and log texts become strings, a number `message` becomes its string form (`12345` to `"12345"`) in the 502 body and in log meta. Documented by the fragment pair.
- **G138-F4 (INFO).** Committed cells call the last route handler directly with a stub logger, so they pin the handler but not the hang under the real winston formatter, `requireAdmin`, or the new `"undefined"` text. My probe covers those but is uncommitted. Optional follow-up. The author disclosed the missing committed `undefined` cell.
- **G138-F5 (INFO, mutants).** My "strip the String wrap" mutant at the three ternary sites strips to `err instanceof Error ? err.message : err` (not the exact base form `... : String(err)`); it is killed anyway, and the exact base form is covered by the 34-of-50 base run.
- **G138-F6 (INFO, outside this PR).** `npm ci` on a fresh checkout of origin/develop (about 8150eeb, at my first install) failed: "lock file's @harmoniclabs/crypto@0.2.5 does not satisfy @harmoniclabs/crypto@0.3.1". At the PR head (which carries develop 9a9bf86967e3) it installed cleanly (1798 packages), so I measured there. Possible lockfile drift on develop after 9a9bf86967e3; not investigated further, not this PR's. (Also: my very first probe run immediately after install failed to resolve `@secuura/shared`, the same files worked on re-run; I treat that as a timing slip of my own install step, all reported figures are from the re-runs.)
- **No FIX-BEFORE-MERGE item.**

## 9. UNMEASURED / NOT TESTED
- The live PR body, the Linear ticket comment, CI, the author's pre-push legs, Node 24.
- Clients reading the forward 502 `details` by a spelling other than `details?.details` (the one pattern searched found only the PR's tests).
- Real index.ts boot, real Postgres with RLS, real auth service, real Blockfrost; winston production json/File transports (only the dev Console formatter and a capture transport were run).
- Whether any hostile or message-less thrown value occurs in reality (all synthetic).
- The fragment pair against the author's canonical bytes (no held diff; read and linted only). I did not read the held Spark diffs for hand-edit equivalence (this PR's commit is the author's own, 2 commits).
- Fail-fast `UNHANDLED_REJECTION_MODE` (the gateway runs survive mode per gate 110).
- Mutant forms beyond the four listed.
- Background processes: none of mine remain. My install and probe runs all ran in the foreground or ran to completion (install2.sh finished: install.done written). The `npm ci`, vitest and playwright processes visible in `ps` belong to other sessions (a Spark clone, playwright MCP), not to this gate.

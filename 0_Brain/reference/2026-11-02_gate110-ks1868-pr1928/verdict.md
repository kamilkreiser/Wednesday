# QA Gate 110 verdict (TIER 2): Secuura/Distributed_Secuura PR 1928 (KS-1868, api-gateway routes/admin.ts, seven catches, O72-P3/P4/P5)

## BLUF
**GATE 110 (TIER 2) on PR 1928 at dd3558044692: GO WITH NOTES. Nothing has to be fixed before merge.**

I ran the REAL admin router (real `createAdminRoutes`, `requireAdmin`, `mockBodyParser`) on a real loopback express listener with the real gateway `errorHandler` mounted after it and the real winston logger wired as `index.ts` wires it. Replaced: the token verifier, the DB `query` (stateful recorder), the redis stub and global `fetch` (which rejects with the thrown value). For an unreadable value (revoked Proxy, Error whose `message` getter throws, `undefined`), head gives exactly what an ordinary Error gives at head, on status, body shape and statements issued, at all seven sites. At base the five route handlers gave NO RESPONSE (client hangs, 1 unhandled rejection per request, no log), the integration test fell to its outer catch, and the seed made the two identity list routes answer 500. The 401/403 guard is identical at base and head on every touched route. No persisted write differs. TIER 2 stands.

Numbers: 6 files +569/-7 as claimed; the held diffs P4+P5+P3 applied strictly give byte-identical files (4 of 4); red-first 15 of 25 by assertion at base; suite 135 files/1387 -> 138/1412, 0 failed; leg 16 27 in baseline 0 new before and after; eslint 0 errors, same 16 warnings; docs check OK with planted defects caught; mutants 28 of 28 killed; merge-tree onto develop `829233f1a388` clean, exactly the PR's 6 paths.

One residual gap, identical to base so not a regression: the guard wraps only the READ of `.message`, so a HOSTILE NON-STRING `message` (G110-F1, the G108-F1 class) still hangs or 500s at several sites (recommended follow-up).

## 1. Heads + diffstat + hand-edit check (logs/head_start.log, head_mid.log, head_end.log, numstat.log, check1_apply.log)
- PR head `dd35580446928eb084616354dae5229fb10b515c` at START (06:24Z), MID and END: identical. Develop `829233f1a388` at all three (the author's mail said so too). One commit, parent `968f17070208`, author Kam Kreiser.
- Three-dot diff: 6 files, **+569/-7**: admin.ts 49/7, tests 163 + 150 + 166, flow fragment 21, cheat fragment 20. Nothing outside the declared paths.
- **Strict apply of the held diffs** (evidence/held/P3,P4,P5.patch, extracted from the three READY files in local-model/night/): `git apply --check -p1` rc 0 for each at base `968f17070208` admin.ts, then applied in order P4, P5, P3 (the author's order), in a scratch dir outside any git repo. Resulting sha256, admin.ts `e2cefa9b5b19...` and the three test files `8971324f...`, `35cbe414...`, `dc9c6c9d...`, equal the PR head's blobs: **4 of 4 EQUAL, no hand edit**. Control: re-applying P3 is refused (rc 1). The fragment pair is the author's own (no held diff), read not compared.
- PR body NOT read (no Secuura gh auth here). I used the READY mail, its CORRECTION and the BUILT AND PROVEN mail (evidence/). The CORRECTION's ratchet line (174 files, 138 under __tests__, 27/27 baseline, 0 new, 0 stale) matches my leg-16 run exactly.

## 2. The hunks (git diff -U4 of admin.ts, seven pairs)
Every pair is the same shape: `X.message` read inline becomes `let reason: string; try { reason = X.message; } catch { reason = 'unreadable thrown value'; }` then `reason` is used where the message was. Sites (base lines): integration-test Blockfrost branch `err.message` :1018, seed `(err as Error).message` :1238, org POST :1455, org PUT :1475, user forward PATCH `err.message` :1501, org DELETE :1514, audit export :1608. Not changed: any response body shape, status, query, the create-user forward at :1432, and the three PR 1916 identity catches. The expression read is the same one the catch already used, so a readable string is byte-identical.

## 3. Behaviour (scripts/g110_probe.test.ts + probe.sh + table.py; logs/probe_base.jsonl, probe_head.jsonl, probe_table.log, judge.log)
112 cells per version (8 routes x 10 thrown values, plus 32 auth cells), vitest rc 0 at both. Thrown values: none, ordinary Error('db boom 10.0.0.7'), revoked Proxy, getter-throws Error, `undefined`, and five G108-F1 values (Error whose `message` getter returns a revoked Proxy / a Symbol / an object whose toString throws / a null-prototype object / a plain object).

| route | ordinary Error (base = head) | unreadable value at BASE | unreadable value at HEAD |
|---|---|---|---|
| POST / PUT / DELETE org | 500 constant body, log `db boom ...`, 1 statement | NO_RESPONSE, 1 unhandled, no log | 500, body byte-equal to the ordinary body, log `unreadable thrown value`, 1 statement, 0 unhandled |
| GET audit export | 500 constant, log | NO_RESPONSE, 1 unhandled | 500 = ordinary body, log constant |
| PATCH user forward | 502 BAD_GATEWAY, `details.details` = message | NO_RESPONSE, 1 unhandled | 502 BAD_GATEWAY, `details.details` = `unreadable thrown value` |
| POST integration test (Blockfrost) | 200 `Network error: <message>` | 200 `Test failed unexpectedly` | 200 `Network error: unreadable thrown value` |
| GET identity users / organizations (awaits the seed) | 200, log `Seed skipped: db boom ...`, 2 statements | **500** (seed rejects) | **200**, log `Seed skipped: unreadable thrown value`, 2 statements, identical to the ordinary row |

- `undefined` thrown (the null-ish case) behaves as the revoked Proxy row at base and head for all seven.
- **Seed claim confirmed**: base 500, head 200, and the 200 is exactly what an ordinary seed failure already gives (same body, same two statements). Seed inserts issued: 0 in every cell (the COUNT query is what rejects).
- **Persisted state**: statements issued are identical between the unreadable and ordinary rows at head for every route (org writes: the one INSERT/UPDATE/DELETE, once; audit export: one SELECT; forward and integration test: 0 DB statements; integration-test redis writes 0 in both rows). No site writes anything new.
- **requireAdmin**: the auth matrix (no token, USER, ORG_ADMIN, SYSTEM_ADMIN) on all 8 routes gives the same status and statement count at base and head: no token 401, USER 403, ORG_ADMIN and SYSTEM_ADMIN reach the handler (judge.log AUTH rows). The admin.ts diff does not touch `requireAdmin`, `ADMIN_ROLES` or `adminScope`.
- **Unanswered request, measured not read**: author said "Express 4 does not answer a rejected async handler: read, not requested". I requested it: NO_RESPONSE after a 1.5 s client timeout with exactly 1 unhandled rejection per request. The gateway runs `UNHANDLED_REJECTION_MODE=survive` (KS-546, index.ts:1187), so base leaks an open socket per request rather than exiting; a fail-fast mode would instead shut the process down. Head removes both.
- Run vs read: real routes, middleware, express, errorHandler, winston. Replaced: verifier, DB, redis, fetch, and the Cap transport I added to capture winston's output. Not run: the real index.ts boot, real Postgres/RLS, real auth service.

## 4. TIER
TIER 2 stands. No persisted write differs from the ordinary path (Check 3), no auth decision differs (401/403 matrix equal), no site newly produces an outcome an ordinary Error does not (the 502, 500 and 200 are the ordinary outcomes). The only status change is the seed's 500 -> 200, and that is the ordinary seed-failure answer; demo-seed environments only (`enableDemoSeed`).

## 5. Re-measure (Node v26.8.1 only; NOT measured on Node 24)
- **Red-first**: three test files at base admin.ts: **15 failed, 10 passed** of 25, all 15 by assertion (`expected 200 to be 500`, `expected undefined to deeply equal { error: 'unreadable thrown value' }`, `expected undefined to be '[Identity] Seed skipped: ...'`, ...); the 10 passes are the controls. Matches the author (logs/red_base.json). At head 25 of 25 pass.
- **Mutants** (scripts/mutants.py, logs/mutants.log; product only, tests untouched, sha256 restored after each, final `RESTORE_OK e2cefa9b5b19`, `git status` clean): per site four forms (undo the guard, constant reason `x`, wrong constant `redacted`, catch rethrows) x 7 sites = **28 of 28 killed, 0 survivors**, each by that site's own R1/R2 cells (the constant form also trips C1; the create route also R3).
- **Whole api-gateway suite** (vitest 4.1.12, `npm ci --ignore-scripts` worked with the lockfile): base 135 files / 1387 tests, 0 failed; head 138 files / **1412** tests, 0 failed (logs/suite_base.json, suite_head.json). Matches the author.
- **tsc incl. tests** (`tsconfig.test.json`): 27 errors at base and 27 at head, 0 in the PR's three test files; leg-16 ratchet `check.cjs`: base 171 files / head 174, 27 of 27 in baseline, 0 new, 0 stale. A planted type error in a PR test file moves tsc to 29 (control fires).
- **eslint** (admin.ts + three tests): 0 errors, 16 warnings, the same 16 at base admin.ts (all unused `err` at other catches); planted file rc 1 (`no-debugger`).
- **Docs check** (`docs-fragments.mjs check`): rc 0, "flow 117 legacy + 78 new, cheat 112 legacy + 78 new; lint clean". One ADVISORY line at cheat :6235 (the G105-F8 "adopt cannot absorb" class, not this PR). Planted defects each give rc 1 naming the PR's fragment (unbalanced div in flow and cheat, missing `<!--n-->` in flow, `</tabl>` in cheat), fragments restored by sha256.
- The author's pre-push hook (13 of 16 legs, PREFLIGHT INCOMPLETE, 1164 s) and CI: not re-run.

## 6. merge-tree (logs/mergetree.log, mt_changed.txt, pr_paths.txt)
`git merge-tree --write-tree develop(829233f1a388) pr1928`: rc 0, tree `926a97cb88b6`, clean. The result changes exactly the PR's 6 paths (SAME_PATHS). Develop moved 17 paths past the base; **0** are the PR's.

## 7. Kam's ks1346 logging rule
The diff adds no value to any log: the only new text is the constant `unreadable thrown value`. Pre-existing and unchanged: readable Errors still log their message as a VALUE (control cells pin `db boom 10.0.0.7` in the log), and the forward still returns an ordinary `err.message` to the caller inside the 502 body (`details.details`). Both are card secuura-ks1346 territory, not this PR's.

## 8. FINDINGS
- **G110-F1 (RECOMMENDED follow-up, not FIX-BEFORE-MERGE; measured; same class as G108-F1, identical at base so no regression).** The guard wraps only the READ of `.message`. If the read succeeds and returns a hostile NON-string, the use of `reason` throws inside the catch, outside the guard. Measured at head (identical to base):
  - Seed (`'...' + reason`) and thus GET identity users/organizations: a Symbol, an object whose toString throws, a null-prototype object or a revoked Proxy as `message` still gives **500** (a plain object gives 200).
  - PATCH forward (`details: reason` into `res.json`): `message` = revoked Proxy gives **NO_RESPONSE** (1 unhandled) at base and head; Symbol, toString-throws, null-proto and plain object give 502.
  - Org POST/PUT/DELETE and audit export: with the real winston Console formatter live (scripts probe `PROBE_REAL_CONSOLE`, logs/probe_*_console.jsonl) a `message` = revoked Proxy makes `log()` itself throw: **NO_RESPONSE** at all four, at base and head (logThrew 1, unhandled 1). With winston silenced they answer 500, so the hang comes from the logger's formatter. Integration test: falls to the outer catch, 200 "Test failed unexpectedly", no hang.
  - Suggested follow-up: coerce inside the same try (`reason = String((err as Error).message)`) and add a cell; the fragment does not claim this shape is handled. Synthetic only, no evidence such a throw occurs.
- **G110-F2 (INFO, measured).** Base behaviour of the five handlers is a hung request plus one unhandled rejection per request, not a crash, because the gateway is in survive mode; the fragment's "read, not requested" is now measured. In a fail-fast mode base would exit the process, which makes this a small availability fix, not only an error-text fix.
- **G110-F3 (INFO, measured).** Response-text changes for an unreadable value only: forward `details.details` and integration-test message become the constant; seed 500 -> 200. The fragment discloses all three.
- **G110-F4 (INFO).** The create-user forward at :1432 (`err?.message` in `console.error`) and the three `catch (err)` blocks in admin.ts without a read are not touched; disclosed in the fragment and the READY mail. Other unguarded reads may remain elsewhere in the service.
- **G110-F5 (INFO, test gap).** The author's 25 cells call the last route handler directly, so they pin the handler, not `requireAdmin`, the hang or the winston path. My probe covers those but is uncommitted. Optional.
- **G110-F6 (INFO, side effect disclosed).** My first probe pass let one "no failure" cell for the integration test call the real `fetch` to `cardano-preprod.blockfrost.io` with a dummy project id (no response used, no credential). I stubbed that cell and re-ran; all reported figures come from the stubbed run.
- **No FIX-BEFORE-MERGE item.**

## 9. UNMEASURED / NOT TESTED
- The live PR body, the Linear ticket, CI, the author's pre-push legs, Node 24.
- A real index.ts boot, real Postgres with RLS (`adminScope` roles), a real auth service, a real Blockfrost response, and winston's production (json + File) transports; only the dev Console formatter was run live.
- Whether any hostile thrown value occurs in reality (all values synthetic).
- The fragment pair against the author's canonical bytes (no held diff for it).
- Fail-fast `UNHANDLED_REJECTION_MODE` behaviour (read from index.ts, not run).
- The cheat ADVISORY at :6235 was not compared with base.
- Mutant forms beyond the four listed.

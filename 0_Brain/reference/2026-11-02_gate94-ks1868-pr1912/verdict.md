# QA Gate 94 verdict: Secuura/Distributed_Secuura PR 1912 (KS-1868, services/security/src/index.ts: key-register save catch O54-P1, key-revoke save catch O56-P1, admin-scopes PUT catch O56-P2), TIER 1

## BLUF
**GO WITH NOTES at head `31b9a9a623fa1a8a8f1c734baf0c190c314a83e4`. Nothing has to be fixed before merge.**
I ran the real DELETE /api/keys/:id, POST /api/keys (plain and rotate), PUT /api/keys/admin-scopes/:userId and POST /api/keys/validate routes at base and at head. They went through the real db.ts (`query()`, `transaction()`, `initDb()`) and the real shared `queryWithTenantGuc`. Only the `pg` driver was replaced, by a recording Pool that stages writes until COMMIT. Each route got 8 kinds of thrown value: 34 cells per version (logs/probe_table.log).
- **Q1 (revoke).** In every failure cell, at base and at head, the in-memory revoke is KEPT (`isActive false`) and nothing is persisted (the stored row stays active). The same process refuses the key ("Key revoked").
  - Infrastructure Error: 503 at both.
  - Ordinary non-infrastructure Error: 500 at both.
  - Unreadable `code`: base sends NO answer and raises one unhandled rejection per cell; head answers 500 INTERNAL_ERROR with the KS-888 line.
  - Revoked Proxy and throwing `message` getter: dbSaveApiKey turns both into an ordinary Error before the route sees them, so both answer 500 at base and at head.
  - Head therefore equals what an ordinary non-infrastructure Error gets. That satisfies card `secuura-ks888-revoke-validate-on-failed-save` = a as Wednesday ruled it, and I agree with the ruling.
  - **Can a revoked key be used after a failure?** In the same process, never (both versions). After a restart, or on another replica, YES in every failure path at both versions, because the store still says active. That is the card's accepted "may not survive a restart" design (KS-1569), and this PR does not change it. One thing does change: at base the unreadable path ends the process on its own (read, not measured, see Q1). That restart re-validates the key. Head removes that trigger.
- **Q2 (register).** No key material is issued or returned on any failure path at either version: no `key`, no `sk_` in the body, 0 in memory, 0 committed, ROLLBACK. The KS-888 line carries `keyId`, `infra` and (when readable) `code`, the same fields as base. No message, stack or thrown object.
- **Q3 (admin-scopes).** Confirmed. Every unreadable kind answers 500 INTERNAL_ERROR "An unexpected error occurred", which is what an ordinary Error gets. The infrastructure kind answers 503. A ZodError answers 400 BAD_REQUEST both from a bad body and from inside the transaction, identical at base and head. Nothing is written in any failure cell. **Gap (G94-F2):** no committed test pins the 400. Two mutants that delete the Zod branch survive the WHOLE security suite (392/392).
- **Q4 (eslint).** Acceptable as a follow-up, not FIX-BEFORE-MERGE. The one-line fix is measured: eslint 0 and tsc 0.
- **Q5 (O54-P1 golden).** Re-checked. The product hunk in the READY file equals the golden and the PR's first hunk line for line, with the same `@@` ranges. The only difference is the missing `diff --git` line and git's function-context text after `@@`. Reverting the three hunks reconstructs the base file byte-identical.

Re-measured: red-first 6 failed / 8 passed of 14 by assertion; green 14/14; suite 378 -> 392; tsc (plain and tests) 0; leg 16 0; docs-fragments clean with 4 planted defects caught. merge-tree is clean onto develop `cde2dee4` and onto `b8874803`, the develop that moved during this gate. Mutants: 17 of 19 killed.

## Heads
- START (logs/head_start.log, 2026-11-01T22:17:40Z): PR head `31b9a9a623fa1a8a8f1c734baf0c190c314a83e4` (equals the expected value), parent = merge-base `03977e89a343`, develop `cde2dee4dffb` (equals the expected value), one commit. Author/committer Kam Kreiser, subject "Refs KS-1868: security key register, revoke and scopes catches guard an unreadable throw", trailer Co-Authored-By Claude Sonnet 5.5.
- END (logs/head_end.log, 2026-11-01T23:34:37Z): PR head `31b9a9a6...` (UNCHANGED), local HEAD equal, product sha256 `e5a3a187...` (equals start), working tree clean. **Develop MOVED to `b8874803`** (2 commits: c8d77dce auth routes, b8874803 nft minting; both KS-1868, 11 paths, 0 under services/security, 0 shared with this PR's paths, control 11). The PR head did not move, so I did not stop. I re-ran merge-tree onto the new develop (Section 6).
- Base product (`03977e89`) = develop `cde2dee4` product = develop `b8874803` product, sha256 `c72ce93f...`. This is gate 90's head (PR 1908 merged). Head product `e5a3a187...`.
- Clone: a fresh `git clone` was not attempted. Following gate 92's route, gate 90's `.git` (key config and push URL `no_push_qa_gate`) was copied into repo/ and `refs/pull/1912/head` + develop were fetched (logs/fetch.log). Nothing was pushed. GitHub, Linear and mail were not touched.
- **PR body not read directly** (no Secuura gh login here). I used the commit message, the author's READY and BUILT AND PROVEN mails (evidence/) and the fragment pair instead.

## 1. Diffstat (logs/diffstat.log)
6 files, +535/-6, as the PR claims: index.ts +29/-6; three new tests (148, 150, 164 lines); one fragment pair (+22 each). Three-dot against the merge-base gives the same 6 paths. Nothing else is touched.

## 2. The hunks (logs/product_diff.log)
- **H1 POST /api/keys save catch (@@ -1410).** `const infra = isInfrastructureDbError(saveErr)` and the inline `code: saveErr?.code` become `let infra = false; let code: unknown; try { infra = ...; code = saveErr?.code; } catch { /* comment */ }`. The log line becomes `{ keyId: apiKey.id, code, infra }`.
- **H2 DELETE /api/keys/:id save catch (@@ -1580).** The same change, character for character, at 4-space indentation.
- **H3 PUT admin-scopes catch (@@ -1765).** `if (error instanceof z.ZodError) return badRequestFromZod(...)` becomes `let isZod = false; let infra = false; try { isZod = error instanceof z.ZodError; infra = isInfrastructureDbError(error); } catch { return next(new Error('unreadable thrown value')); }`, then `if (isZod) ...badRequestFromZod(res, error as z.ZodError)`. The later `if (isInfrastructureDbError(error))` becomes `if (infra)`.
- **What does NOT change:**
  - the messages, statuses and response bodies;
  - `memApiKeys.delete` in register;
  - `apiKey.isActive = false` before the revoke try (base :1574);
  - the infrastructure log line and the final `next(error)` in admin-scopes;
  - imports, exports, signatures, route registration.
- **What does change for a readable value:** `isInfrastructureDbError` now also runs on a ZodError before the Zod decision. The order of decisions is the same (Zod -> 400, then infra -> 503, then next). `isInfrastructureDbError` (:1149) is pure (`String(e?.code)`, `String(e?.message)` against two regexes), so this has no effect.
- **Proof the hunks are exactly these:** applying all three "revert" mutants (M0) to head gives a file byte-identical to base (scripts/mutants.py; checked True).

## 3. The behaviour question (scripts/probe.test.ts via scripts/probe.sh; logs/probe_{base,head}.jsonl, logs/probe_table.log)
**Setup.** A real app on loopback, a real RS256 super_admin token, the real db.ts with positive control `initDb: true, isDbAvailable: true` at both versions. The stand-in pg models BEGIN/COMMIT/ROLLBACK over svc_api_keys and admin_organisation_scopes. The rejecting statement is the `INSERT INTO svc_api_keys` upsert (register and revoke) or `DELETE FROM admin_organisation_scopes` (scopes). Unhandled rejections are counted with vitest's listeners removed (gate 90's method). 34/34 cells ran at each version (rc 0).

**Thrown kinds:**
- infraError (`code ECONNREFUSED`)
- ordinaryError
- revokedProxy
- messageGetterThrows
- codeGetterThrows (an Error)
- codeGetterThrowsInfraMsg (message "Connection terminated unexpectedly", code getter throws)
- plainObjCodeGetter
- zodError (scopes only), plus a bad-body Zod cell

The first probe run had a bug in my control cells (they rejected with `undefined`). That run is kept in logs/probe_run1_buggy_controls/ and is not used below.

### Q1 DELETE /api/keys/:id (seeded key active in memory and in the store; after the DELETE: validate in the same process, then memory cleared to simulate a restart, then validate again)
| kind | status base / head | memory isActive | stored is_active | validate same process | validate after restart | KS-888 line base / head | unhandled base / head |
|---|---|---|---|---|---|---|---|
| control (save lands) | 200 / 200 | false | **false** | refused "Key revoked" | refused | none | 0 / 0 |
| infraError | 503 / 503 | false | true | refused | **valid** | keyId,code,infra (ECONNREFUSED, true) / same | 0 / 0 |
| ordinaryError | 500 / 500 | false | true | refused | **valid** | keyId,infra (false) / same | 0 / 0 |
| revokedProxy | 500 / 500 | false | true | refused | valid | same as ordinary / same | 0 / 0 |
| messageGetterThrows | 500 / 500 | false | true | refused | valid | same as ordinary / same | 0 / 0 |
| codeGetterThrows | **UNANSWERED** / 500 | false | true | refused | valid | **none** / keyId,infra (false) | **1** / 0 |
| codeGetterThrowsInfraMsg | UNANSWERED / 500 | false | true | refused | valid | none / keyId,infra (false) | 1 / 0 |
| plainObjCodeGetter | UNANSWERED / 500 | false | true | refused | valid | none / keyId,infra (false) | 1 / 0 |

- Memory and store are identical at base and head in every cell. The in-memory revoke survives every failure path: dbSaveApiKey's first line `memApiKeys.set(k.id, k)` (:454) puts the revoked copy into memory before the DB try, and the catch never undoes it.
- **Can a revoked key be used after a failure path?**
  - In the same process: no, at either version. Validate's KS-888 R2 rule (:1868-1871) keeps a cached revoke over a stored active row.
  - After a restart, or on another replica (KS-1370 validate decides on the stored row): **yes, at BOTH versions, in EVERY failure path**, the ordinary and infrastructure ones included. This is what card a accepted ("the API key revoke could not be saved, so it may not survive a restart"; KS-1569 in Backlog). It is pre-existing and not changed here.
  - The one difference this PR makes: at base an unreadable `code` raises an unhandled rejection in an Express 4 async handler. The security service installs no `unhandledRejection` listener (grep over services/security/src finds none; the shared KS-546 handler is not installed here), so under Node's default throw mode the process would exit (READ, not measured at process level). The restart that follows rebuilds memory from the store and **re-validates the just-revoked key**. Head answers 500 and keeps the process, so the in-memory revoke holds until the next ordinary restart.
- **Card verdict:** the base route already answers 500 to every ordinary non-infrastructure Error (cell ordinaryError, base = head). An unreadable value cannot be classified as infrastructure, so it gets the same 500 with the revoke kept. That satisfies "keep in-memory revoke", and it reads "503" the way the shipped route already does (503 only for infrastructure). I agree with Wednesday's ruling.
- Info (G94-F5): `codeGetterThrowsInfraMsg` answers 500 at head. A readable Error with the same message would get 503, because `isInfrastructureDbError` reads `code` first and the throw skips the message test. That is still the ordinary non-infrastructure answer, so no new outcome.

### Q2 POST /api/keys (plain path through dbSaveApiKey -> queryWithTenantGuc; rotate path through transaction())
| kind | plain: status base / head | rotate: status base / head | key issued / `sk_` in body / memory / committed (all cells, both versions) | KS-888 line base / head |
|---|---|---|---|---|
| control | 201 / 201 | 201 / 201 | yes / yes / 1 / 1 (COMMIT) | none |
| infraError | 503 / 503 | 503 / 503 | no / no / 0 / 0 (ROLLBACK) | keyId,code,infra / same |
| ordinaryError | 500 KS-888 msg / same | 500 KS-888 msg / same | no / no / 0 / 0 | keyId,infra / same |
| revokedProxy | 500 KS-888 msg / same (dbSaveApiKey converts it) | **500 "An unexpected error occurred"** / 500 KS-888 msg | no / no / 0 / 0 | plain: both; rotate: **none** / keyId,infra |
| messageGetterThrows | as revokedProxy | as revokedProxy | no / no / 0 / 0 | as revokedProxy |
| codeGetterThrows, codeGetterThrowsInfraMsg, plainObjCodeGetter | **500 generic** / 500 KS-888 msg | 500 generic / 500 KS-888 msg | no / no / 0 / 0 | **none** / keyId,infra |

- Fail-closed holds at both versions in every cell. Head only restores the KS-888 line and the specific message, which is the answer an ordinary Error gets. 503 is never produced for an unreadable value.
- This measures operator 56's correction: a readable message with a throwing `code` reaches the route catch RAW on the NON-rotate path too. Base gives the generic 500 and no KS-888 line; head fixes both.
- **ks1346:** the KS-888 line's fields are exactly `keyId`, `infra` and `code` when readable. These are the base's names. No message, stack or thrown object is logged. `code` is a field VALUE (an SQLSTATE or errno string), logged by base too. This is pre-existing, and Kam's rule (names, not values, of a thrown OBJECT) is not newly engaged.

### Q3 PUT /api/keys/admin-scopes/:userId (stored scope {A}; the request asks for {B})
| kind | status base / head | body code / message (head) | stored scopes base / head | statements end | unhandled base / head |
|---|---|---|---|---|---|
| control | 200 / 200 | - | {B} / {B} | COMMIT | 0 / 0 |
| Zod, bad body | 400 / 400 | BAD_REQUEST "Validation failed" | {A} / {A} | (no transaction) | 0 / 0 |
| ZodError from the transaction | 400 / 400 | BAD_REQUEST | {A} / {A} | ROLLBACK | 0 / 0 |
| infraError | 503 / 503 | SERVICE_UNAVAILABLE, infrastructure line 1 | {A} / {A} | ROLLBACK | 0 / 0 |
| ordinaryError | 500 / 500 | INTERNAL_ERROR "An unexpected error occurred" | {A} / {A} | ROLLBACK | 0 / 0 |
| revokedProxy, messageGetterThrows, codeGetterThrows, codeGetterThrowsInfraMsg, plainObjCodeGetter | **UNANSWERED** / 500 | INTERNAL_ERROR "An unexpected error occurred" (= ordinaryError) | {A} / {A} | ROLLBACK | **1** / 0 |

- `next(new Error('unreadable thrown value'))` reaches the shared errorHandler (packages/shared/src/errors/index.ts:230). It is not a ZodError, AppError, body-parser or status error, so it falls through to the 500 JSON that `next(ordinaryError)` gets: measured equal on status, code and message.
- The errorHandler's log line was NOT captured by my probe (winston's transport bypassed my stdout spy). From the source: it logs `err.message` (the constant) and the new Error's own stack, never the thrown value.
- Nothing is written in any failure cell (real `transaction()`: BEGIN ... ROLLBACK).

## 4. Re-measure (Node v26.8.1, vitest 4.1.12; NOT measured on Node 24)
- Head, the 3 new files: **14/14 passed** (logs/head_new_tests.log).
- Base product + new files: **6 failed | 8 passed** (logs/red_base_new_tests.log). All six failures are `AssertionError`: revoke and scopes see `{status: 0}` (no answer); register sees status 500 with the generic body and no KS-888 line. vitest also reported **4 unhandled rejections** at base (revoke R1/R2, scopes R1/R2); head reports 0.
- Whole suite: base without the new files **37 files, 378/378**; head **40 files, 392/392** (logs/base_whole_excl_new.log, logs/after_whole.log). Product restored, RESTORE_OK.
- tsc `tsconfig.json --noEmit` rc 0; `tsconfig.test.json` rc 0. Leg 16: "59 files, 47 under __tests__; 0 errors: 0 in the baseline, 0 new; 0 stale". Planted TS6133 in a new test gives rc 2, and the file was restored byte-identical (logs/tsc_*.log, logs/leg16_security.log).
- eslint (cwd services/security): head `index.ts` + 3 tests: 0 errors, **2 warnings, `no-useless-assignment` at 1782:9 (`isZod`) and 1783:9 (`infra`)**. Base index.ts through stdin under the same filename: 0. Planted `debugger` gives rc 1 (logs/eslint_*.log).
- docs-fragments: clean rc 0, "flow 117 legacy + 64 new, cheat 112 legacy + 64 new". Four planted defects (flow unclosed div, flow `<!--n-->.` removed, cheat unclosed div, cheat `</table>` corrupted) each give rc 1; all were restored by sha and give rc 0 after (logs/frag_outer.log). The cheat ADVISORY at line 6235 is pre-existing (gate 90's G90-F7).
- The author's figures (378 -> 392, 8/6 red-first, 14/14, eslint 2 warnings at 1782/1783, leg 16 59/47) all re-measure exactly. Hook and preflight lines are quoted from the mail, not re-run.

## 5. Mutants (scripts/mutants.py; one site per run, product only, tests untouched, sha256 restored and checked after every run: all True; logs/mutants_table.log, logs/mut_*.log)
**19 runs: 17 killed, 2 survived.** Every kill fails only that site's own file, by AssertionError.

| Mutant | register (H1) | revoke (H2) |
|---|---|---|
| M0 revert to base | KILLED R1 R2 | KILLED R1 R2 |
| M1 drop the inner try | KILLED R1 R2 | KILLED R1 R2 |
| M2 inner catch rethrows | KILLED R1 R2 | KILLED R1 R2 |
| M3 inner catch sets infra = true (503) | KILLED R1 R2 | KILLED R1 R2 |
| M4 log line also carries `error: saveErr` | KILLED R1 only | KILLED R1 only |
| M5 log removed | KILLED C1 R1 R2 | KILLED C1 C3 R1 R2 |

| Mutant | admin-scopes (H3) |
|---|---|
| M0 revert to base | KILLED R1 R2 |
| M1 `next(error)` with the raw value | KILLED R1 R2 |
| M2 inner catch throws | KILLED R1 R2 |
| M3 inner catch falls through as infra | KILLED R1 R2 |
| M4 Zod probe dropped (`isZod` stays false) | **SURVIVED, also against the WHOLE suite 392/392** (logs/mutants_whole.log) |
| M5 `if (isZod)` branch dropped | **SURVIVED, whole suite 392/392** |
| M6 inner catch answers 400 | KILLED R1 R2 |

- M4/M5 on admin-scopes are not equivalent. A ZodError would go to `next(error)`, and the shared errorHandler would answer **422 VALIDATION_ERROR** (ValidationError, errors/index.ts:97-99) where the route answers 400 BAD_REQUEST. I read that from source; my probe shows the 400 at both versions. -> G94-F2.
- M4 on register/revoke dies only because `JSON.stringify` of a revoked Proxy throws inside `log()`. A KS-888 line that carried a readable thrown object would pass C1 and R2. No cell asserts the line's field set. -> G94-F3.

## 6. merge-tree (logs/merge_tree.log, logs/merge_tree2.log, logs/develop2.log, logs/frag_merged.log)
- Onto develop `cde2dee4` (the develop named in the assignment): **rc 0, tree `d4c57843`.** The merged tree changes exactly the PR's 6 paths. Its index.ts diff equals the PR's. 0 shared paths with develop's 6 since the base (control 6).
- Onto develop NOW `b8874803` (moved during the gate; old develop is an ancestor): **rc 0, tree `141ed61f`**, exactly the PR's 6 paths, index.ts diff equal to the PR's, develop's product unchanged (`c72ce93f`). 0 shared paths (control 11).
- docs-fragments `check` on that merged tree (worktree merged/): rc 0, "67 new".

## 7. Kam's ks1346 logging rule
- KS-888 register/revoke lines: field names `keyId`, `code`, `infra`, unchanged from base. No message, stack or thrown object.
- Admin-scopes: no new log line. The errorHandler logs the constant 'unreadable thrown value' and the stack of the Error the route built (read from source).
- Complies. G94-F3 is the test gap that would let a regression here pass.

## 8. FINDINGS / notes for the PR body
- **G94-F1 (INFO; Q1; pre-existing; measured at both versions)** Every failure path of the revoke leaves the stored row active. A restart, or a second replica, honours the revoked key again (validate after the simulated restart: `valid: true` in all 7 failure kinds, base and head). This is the accepted design of card a / KS-1569, and the PR does not change it. The PR does remove one cause: at base the unreadable `code` path is an unhandled rejection that, with no `unhandledRejection` listener in security, would end the process (read). That restart re-honours the key at once. Say so in the revoke section.
- **G94-F2 (LOW, recommended; test gap; measured)** No committed cell pins PUT admin-scopes' Zod 400. Mutants M4 and M5 (drop the Zod probe or the branch) survive the whole security suite and would turn the 400 BAD_REQUEST into the errorHandler's 422 VALIDATION_ERROR. This PR rewrote exactly that line. Recommend one control cell in the admin-scopes file: a ZodError from the transaction (or a bad body) answers 400 BAD_REQUEST. Probe evidence: 400 at base and head for both shapes. Not a merge block.
- **G94-F3 (LOW, optional; test gap)** No cell asserts the KS-888 line's FIELD SET. A line that added the thrown object is killed only incidentally (revoked Proxy serialisation). Optional: assert `Object.keys` of the line in C1.
- **G94-F4 (Q4; follow-up, NOT fix-before-merge)** The 2 `no-useless-assignment` warnings are real: the inner catch returns, so the `= false` initialisers are never read. Rule level is warn, no hook or preflight leg runs eslint, and there is no behaviour effect. Measured fix: `let isZod: boolean; let infra: boolean;` gives eslint 0 and `tsc --noEmit` 0 (logs/eslint_fixed_index.log, logs/tsc_fixed_variant.log). It can ride the next KS-1868 security PR.
- **G94-F5 (INFO)** With a throwing `code` getter and an infrastructure-looking message, the head answers 500, not 503. The `code` read throws first and the message test is skipped. That is the ordinary non-infrastructure answer, so no new outcome. Guarding the two reads separately would classify by message; not worth it for a synthetic value.
- **G94-F6 (INFO, wording)** The fragment and the revoke route's own comment (:1579 base, "this handler takes no next") are wrong in a small way. `app.delete('/api/keys/:id', ...)` DOES take `next` (:1532; it calls `next(err)` for the scope read), and so does the admin-scopes handler. The real reason an uncaught throw escapes is that Express 4 does not forward an async handler's rejection. The comment is pre-existing; fix the fragment wording if convenient.
- **G94-F7 (INFO, Q5)** The O54-P1 READY lacks the `diff --git` line for index.ts. Its product hunk is otherwise equal to the golden and to PR hunk 1, with identical `@@ -1410,8 +1410,15 @@` ranges. The trailing `@@` text is git's function context. The O56 READY files carry `diff --git`. O56-P1/P2 differ from the PR only in the new-start line (+7, +14), which is the cumulative offset of the earlier hunks (logs/q5.log).
- **G94-F8 (INFO)** Remaining same-class sites the PR body already lists: GET admin-scopes catch (:1803 head), dbSaveApiKey's `err?.message` (:475), errorHandler's `err.message` (errors/index.ts:238). Also, the admin-scopes infrastructure log re-reads `error?.code` outside the guard. That runs only after a successful read, so only a stateful getter could throw there. Unreachable.

## 9. NOT TESTED
- The real PR body (no gh auth).
- A real PostgreSQL / pgbouncer (the stand-in pg models staging only).
- A booted service and the process-level exit on an unhandled rejection at base (read from source; counted in-process only).
- A real restart (simulated by clearing memApiKeys) and a second replica (read from validate's code).
- The gateway hop.
- Node 24.
- The four platform suites; CI; the pre-push hook legs (quoted).
- The errorHandler's log line content (read, not captured).
- Linear ticket and card texts (the card option is quoted from the assignment).
- A spark shadow review.

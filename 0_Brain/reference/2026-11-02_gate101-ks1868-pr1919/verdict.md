# QA Gate 101 verdict: Secuura/Distributed_Secuura PR 1919 (KS-1868, originate, six held Spark passes, eight hunks, +44/-10 product), TIER 2

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** Tier 2 holds (Q-E below). I re-measured the four key questions by running the real code with only the database / fetch / email / logger replaced (scripts/probe.test.ts, scripts/probe2.test.ts, run at base and head; logs/probe_table.log):
- **A (O63-P2).** Through the real `systemErrorsRouter` and the real `trackError`, an insert that rejects with an unreadable value (revoked Proxy, or an Error whose message getter throws) answers **500 at base and 201 at head**. At head it equals an ordinary Error and a thrown string in all three respects: status 201, body `{"success":true}`, persisted rows 0 (the insert failed in every case), and the same single log line shape `Failed to persist error` with `error: 'unreadable thrown value'` (ordinary: its own message). Same on `/ingest` and `/client-errors`. Unhandled rejections 0 in every cell.
- **B (O68-P1).** The real `notifyDocumentCertified` with `fetch` rejecting: at base an unreadable value makes it REJECT and send nothing; at head it resolves and the SMTP fallback sends exactly one certification mail, identical to the ordinary-Error and string cells. No recipient and no message content in any warn/error line (`warnHasRecipient: false`, `warnHasTitle: false`). The recipient does appear in the pre-existing INFO line `Notification sent via SMTP fallback` (see G101-F3).
- **C (O63-P1 log text).** Confirmed with an object carrying `secret: 'SECRET-VALUE-...'`: the head logs `thrown Object with fields [code, secret]`, a class instance `thrown Custom with fields [code, secret]`, `5` -> `thrown number`, `null` -> `thrown object`, `undefined` -> `thrown undefined`. **The secret value is in no log line** (`secretInLog: false`, all 18 cells). Base logged `[object Object]` / `5` / `null` / `undefined`. Errors and strings log identically at base and head.
- **D (O65-P1/P2).** Real `verifyDbReady` of both repos: unreadable value at head logs the "connection FAILED" line with `error: 'unreadable thrown value'` and throws `Error('Database is required for ...')`, exactly the ordinary-Error outcome. At base it threw the raw TypeError (or the getter's own Error) and wrote no "FAILED" line. The index.ts startup `.catch` (index.ts:514) reads `err?.message` and logs a warn, never exits, in every case; only the message text differs (now the repo's constant).
All other numbers re-measure: 6 files, +44/-10, 14 files +674/-10 with the tests and fragments; red-first 16 of 36 by assertion; whole suite 1999 -> 2035; tsc 0; eslint 0 errors; merge-tree clean; 8 hunks each killed by mutants (two rethrow mutants are inconclusive, G101-F4).

## Heads
- START (logs/head_start.log, 2026-11-02 ~02:00Z): PR head `b22b6ec521294e7ccefcebbe2b2252d448c0d160` (matches the brief), develop `92a26320e30ad680459cdb96c5b68b91a5f175a5` (matches), merge-base `d9acf71a3fcc9b70a216a904d7339a8fc1ccf4a0`. One commit, author Kam Kreiser, subject "Refs KS-1868: originate catches log a constant reason when a thrown value cannot be read".
- END (logs/head_end.log, 02:25:49Z): PR head `b22b6ec5...` UNCHANGED, local HEAD the same, working tree clean, product sha256 before/after every swap equal (logs/runs_sha_before/after.txt, RESTORE_OK each time). **develop MOVED to `04ff5262ad526a13c1a0df99480b76860a8d11d1` while I worked.** The PR head did not move, so I did not stop; I re-ran merge-tree on the new develop (Q5) and it is clean.
- Diffstat (logs/diffstat.log): 14 files +674/-10 = 6 product (+44/-10) + 6 tests (+585) + 2 fragments (+45). Nothing outside `services/originate/src/{routes,services,repositories,utils,__tests__}` and the two `Projects Documents/fragments` files.
- **PR body not read.** No gh login for the Secuura account here. I used the author's READY and BUILT AND PROVEN mails (evidence/). Body wording I could not see is NOT verified.

## FINDINGS
- **G101-F1 (INFO, measured)** O63-P2 raises 500 -> 201 for an unreadable insert error; it is exactly the ordinary-Error outcome (Q-A table). Not reachable by a caller: the rejection comes from Prisma `$executeRaw` (an Error subclass) and the parameters are zod-validated strings from the request body, not objects pg could call into. Defence-in-depth, as every KS-1868 site.
- **G101-F2 (INFO, measured, the author flagged it)** O63-P1 log text changes for a thrown value that is neither Error nor string, at both ingest catches: `String(value)` -> fail500's description (type + field names). Names only, never values (Q-C). Acceptable, and an improvement under Kam's ks1346 rule: base logged nothing useful (`[object Object]`).
- **G101-F3 (INFO, pre-existing, ks1346 adjacent)** notificationClient.ts logs the recipient address `to` in three INFO lines (:52 `Notification sent via service`, :87 `SMTP not configured`, :115 `Notification sent via SMTP fallback`). Not new text, not a thrown-object leak (ks1346 is about thrown objects), and the ordinary-Error path already emits it. But the consequence of this PR is that the hostile-value path, which used to emit no line, now emits the :115 line with `to` like the ordinary path. No message content (title, certifier, reason) is logged anywhere (`allHasTitle: false`). Candidate card for Kam: whether recipient addresses belong in logs at all (PII).
- **G101-F4 (INFO, mutant gap in tooling, not a product gap)** Two rethrow mutants hung jest instead of reporting: `fail500(...); throw err` (O63-P1a/b M5) and the metering catch rethrowing (O68-P2 M3). A rethrow in an Express 4 async handler leaves the request unanswered, which is the very "NO ANSWER" state the committed cells assert against, so they cannot pass. I killed the runs; I record them INCONCLUSIVE, not killed. Everything else was a clean assertion kill.
- **G101-F5 (INFO, test gap, same class as G90-F3)** Readable non-Error branch: mutant M6 (`String(err)` -> `'x'`) is KILLED at all 6 guard sites here (C-cells with a thrown string exist). So no survivor of the G90-F3 kind in this PR. Noting it as a positive.
- **G101-F6 (INFO)** O63-P1's R1/R2 cells are defensive: with the real `trackError` the ingest catches can only see an unreadable value if `trackError` itself is replaced (probe C replaces it by spy). Same as the author said. Real route cells for A are not committed (the committed cells for O63-P1 stub trackError); my probe A is an uncommitted route-level confirmation. Optional follow-up: one route-level cell for O63-P2's 500 -> 201 (cf. G90-F2).
- **G101-F7 (INFO)** docs-fragments `check` prints two ADVISORY lines (flow :6249, cheat :6235). They also appear without this PR's fragments (G90-F7 saw the same line numbers on earlier develop), so they are not from this PR. rc 0, "71 new".
- **G101-F8 (INFO)** eslint shows 2 warnings (`preserve-caught-error` on the repos' unchanged `throw new Error(...)` lines certificationRepo.ts:68, documentRepo.ts:149). Pre-existing lines, unchanged by the hunks. 0 errors.
- **G101-F9 (INFO)** At notificationClient site A the try also spans the non-OK `await sendSmtpFallback(payload)` branch; the second guarded catch now makes sendSmtpFallback never reject, so `certifications.ts` :1153/:1303 callers (no `.catch`) no longer risk an unhandled rejection from a hostile SMTP error. Read from source, not run.
- No FIX-BEFORE-MERGE item.

## Q-A..Q-E, the key questions (section 3)
Probe method: jest with the real module under test, `../db` prisma stub that records inserts, a recording logger, `authenticate` bypassed, a real loopback listener and `fetch` (probe A/C); for B the real notificationClient with `fetch` and `../services/email` stubbed (records every send); for D the real `verifyDbReady` of each repo with a throwing `$queryRaw`. Base = the PR merge-base product files, head = PR head; the probe files were moved to logs/_quarantine after each run, tests/products restored by sha256.

**A. O63-P2 trackError, through the real route** (ordinary / string / revoked Proxy / throwing getter), same on `/ingest` and `/client-errors`:
| | base | head |
|---|---|---|
| ordinary Error | 201, `{"success":true}`, rows 0, log `Failed to persist error` `db down` | same |
| string | 201, same body, rows 0, log `plain string` | same |
| revoked Proxy | **500** `INTERNAL_ERROR`, rows 0, log `System error ingest failed` with the TypeError text | **201**, `{"success":true}`, rows 0, log `Failed to persist error` `unreadable thrown value` |
| throwing getter | **500**, rows 0 | **201**, same as above |
| control (insert ok) | 201, rows 1 | 201, rows 1 |
Head equals the ordinary-Error outcome in status, body and persisted state. Note a failed insert persists nothing in every case, so "persisted state" is identical (0 rows) by construction; the answer 201 means the caller is told success although the error report was not stored, exactly as for an ordinary DB error today.

**B. O68-P1 notificationClient** (fetch rejects):
| value | base | head |
|---|---|---|
| ordinary Error | resolves, 1 mail sent, warn `Error: svc down`, info `sent via SMTP fallback` | same |
| string | resolves, 1 mail | same |
| revoked Proxy | **REJECTS, 0 mails sent, no log line** | resolves, **1 mail sent** (identical args), warn `error: 'unreadable thrown value'` |
| throwing getter | **REJECTS, 0 mails** | resolves, 1 mail |
Dropped -> sent, as for an ordinary Error. Warn/error lines contain template + error only; no recipient, no title (probe flags false). The recipient is in the INFO line only (G101-F3). Retry: none (SMTP fallback only), unchanged.

**C. O63-P1 log text:** see BLUF. The sixteen cells (2 routes x 9 values) show: objects log type + names, no value; revoked Proxy / throwing getter at base give NO ANSWER (status 0 after a 2.5 s abort, no log line), at head 500 with `thrown value that could not be described`; Error and string lines are byte-identical. Positive control: the secret string is present in the thrown object (`secret` field) and absent from the serialized log array.

**D. verifyDbReady x2:** table in logs/probe_table.log (rows D). Head unreadable == head ordinary: the thrown error is `Error('Database is required for ...')`, the FAILED line is written. Boot: `index.ts:410-515` runs both in `Promise.all` and the `.catch` only logs a degraded-functionality warn; `certificationRepo.initRepo` (certifications.ts:70) catch logs `err.message`, now always the constant. Startup does not exit in either state. The only observable change on boot is the text in that warn (TypeError text -> the repo's constant), the same as for an ordinary Error. Not run: a real boot.

**E. Tier.** Nothing here touches auth, money, identity or data destruction. Sites: error-reporting ingest (stores an error row), startup DB readiness probes, notification email dispatch (content/recipients unchanged), a read-only usage SELECT's error log. The metering route reads charge-event totals but only its catch changed (log text; the constant 500 and `Failed to read usage` unchanged). No SQL, no auth middleware, no write path other than the error-report INSERT, no deletion. **Tier 2 stands; Sonnet gate is sufficient.**

## Q2. The eight hunks (logs/product_diff.log)
- systemErrors.ts x2: `logger.error(..., {error: err instanceof Error ? err.message : String(err)}); res.status(500).json({... 'Internal server error'})` -> `fail500(res, '<same context>', err)`. fail500 (:93-109, KS-730/KS-1772) describes the value in its own try, logs in another, then sends the same constant 500 body. Same context text, same 500 body (identical JSON); only the log description changes for non-Error non-string values (G101-F2).
- errorTrackingService.ts, certificationRepo.ts, documentRepo.ts, metering.ts: a 6-line guard `let reason: string; try { reason = <same expression>; } catch { reason = 'unreadable thrown value'; }` and `error: reason`. Nothing else changes: the repos still throw the same constant Errors, metering still answers the same constant 500, trackError still resolves.
- notificationClient.ts x2: same guard around `String(err)`; the warn text, `template` key and the SMTP fallback call are unchanged.
- Not changed: any status code, response body, SQL, statement, new import, rethrowing catches in the two repos.

## Q4. Re-measure
- Red at base (logs/red_base.json, red_base_new.log): new tests + base product, whole run: **16 failed, 2019 passed, 2035 total**. By file: notification 4, ingest 4, trackError 2, certificationRepo 2, documentRepo 2, metering 2. **All 16 carry an `expect(` failure message** (checked over every failure message; 6 of them, ingest 4 and metering 2, also carry the product's own TypeError as the first message, as the author said).
- Green at head: 6 files, **36/36** (logs/head_new_tests.log).
- Whole originate suite (jest, Node v26.8.1, NOT Node 24): base without the 6 new files **163 files 1999/1999** (logs/whole_base.json); head **169 files 2035/2035** (logs/whole_head.json); cell by cell: 36 new, **0 vanished, 0 passed -> not passed**. Load average 14-17 during the runs.
- tsc: `tsconfig.json --noEmit` rc 0 (logs/tsc_plain_head.log). With the tests in the program (scratch config in scripts/tsconfig.tests.json extending the service's): head **0 errors, 199 test files** (6 of them the new ones); with the 6 new files excluded: 0 errors, 193 test files (logs/tsc_tests_base_excl.log) = the author's 193/199. Planted `TS2322` in a test file -> rc 2, reported once; file moved to quarantine.
- eslint (cwd = services/originate): the 12 changed files **0 errors, 2 warnings** (G101-F8), rc 0. Planted file: `no-debugger` error + unused-var warning, rc 1.
- docs-fragments (logs/frag_head.log): rc 0, "flow 117 legacy + 71 new, cheat 112 legacy + 71 new; lint clean". Planted unbalanced `<div>` in the cheat fragment: rc 1, "tags are not balanced: <div> opened 3, closed 2"; file restored by sha256.
- Quoted, not re-run: the pre-push hook ("PREFLIGHT INCOMPLETE 13/16, 3 skipped, nothing failed", legs 3 4 8 need the local stack), the author's own mutants and probes.

## Q5. Mutants (scripts/mutants.py and mutants2.py; ONE site per mutant, product only, tests untouched; sha256 restored and checked every run, all `restore True`; logs/mutants_run.log, mutants2_run.log, mut_*.log)
Guard sites (6: O63-P2, O65-P1, O65-P2, O68-P2, O68-P1a, O68-P1b), mutants: M0 revert guard, M1 drop the inner try, M2 catch assigns `String(err)`, M3 catch rethrows, M4 constant for all values, M6 readable branch -> `'x'`, M7 `error:` ignores `reason`, M8 constant text changed. **Every runnable one KILLED by assertion**:
- M0, M1, M2, M4, M6, M8 killed at all 6 sites (2 cells each, M6 1 cell at the single-expression sites, 8/4 at notification).
- M7 first version (`error: undefined`) failed to compile under `noUnusedLocals` (my mutant, not a finding); re-ran as `error: (reason ? 'x' : 'x')`: killed at all 6 sites (4/4/4/4/8/4 cells).
- M3 killed at 5 sites; **O68-P2 M3 (rethrow in the route catch) hung jest, inconclusive (G101-F4).** M2 at O68-P2 (variable `error`) killed, 2 cells.
fail500 sites (O63-P1a/b): M0 revert to inline killed (2), M1 no call killed (4), M2 context text changed killed (4), M3 `String(err)` as argument killed (3); **M5 rethrow after fail500 hung jest, inconclusive (G101-F4)**.
Net: 0 survivors; 3 inconclusive hangs (O63-P1a M5, O63-P1b M5, O68-P2 M3), all the same "request never answered" class that the cells assert against.

## Q6. merge-tree (logs/merge_tree_92a2.log, logs/merge_tree.log)
- Onto develop at START `92a26320`: rc 0, tree `440281b9f2943771d58de15141be6cb33150aebe` = the author's tree `440281b9f294`. Clean.
- Onto develop at END `04ff5262` (moved during my work): rc 0, tree `67c5d718a0ac345fb981665d42f44298f6718083`, clean. The result changes exactly the PR's 14 paths (SAME_PATHS against the three-dot list). Develop changed 16 paths since the merge-base; **0 shared with the PR** (positive control: the changed list is non-empty, 16).

## Q7. Kam's ks1346 rule (log type and field NAMES of a thrown object, never values)
Every new/changed log line: (1) fail500's description of a non-Error non-string: type + `Object.keys` only (probe C, secret absent); a revoked Proxy / throwing getter yields the constant `thrown value that could not be described`. (2) the guard sites log `err.message` for an Error (unchanged), `String(err)` for the other readable values (unchanged, so a plain object stays `[object Object]`, a string stays itself) and the constant for unreadable. (3) notification warns log `template` + `String(err)` only; no recipient or content in any warn/error line (probe B). A thrown string is still logged verbatim, which is pre-existing behaviour at every site, and not a new leak. **Compliant.** Adjacent pre-existing item: G101-F3.

## NOT TESTED
- The real PR body (no gh auth); a real PostgreSQL/Prisma, notification service, SMTP server or Express app boot; a real HTTP request to a running originate; Node 24 (host v26.8.1; every figure is not measured on Node 24); the four platform suites; CI; the pre-push hook legs (quoted); whether a real unreadable throw can occur at any of these sites (the thrown values are synthetic; Prisma and fetch reject with Error subclasses); the frontend ErrorBoundary callers (read by the author, not exercised by me); the Linear ticket text.

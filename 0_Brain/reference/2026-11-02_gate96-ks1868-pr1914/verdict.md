# QA Gate 96 verdict: Secuura/Distributed_Secuura PR 1914 (KS-1868, services/analytics/src/routes/analytics.ts, 12 catches in 4 passes O60-P1 + O61-P1..P3), TIER 2

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** Q1: I ran the real Express 4.22.3 app on a loopback port with the real router and the real request schemas (only the two service modules and the logger replaced), 12 routes x 9-10 thrown values, at base and head. 78 of 117 cells are byte-identical (status, body text, log lines): ordinary Error (500), string, plain object, null, a ZodError from the service (400 with its details), a REAL ZodError from the real schema on the nine Zod routes (400, details identical), and a ZodError whose message getter throws (still 400 on the nine Zod routes). The 39 cells that differ are all unreadable-value cells: base = no response (client abort) plus one unhandled rejection, head = the route's constant 500 with one log line `{error: 'unreadable thrown value'}` and 0 unhandled. Q2 exact (four tokens, test files only; tsc 1 / 5 / 1). Q3 EQUAL for all four passes. Q4 yes: the nine C1 cells pin the 400 body fully (full `toEqual` of success/code/message/details, and "nothing logged"); 27 mutants of the 400 branch all died.
Other numbers re-measure exactly: red-first 24 failed / 24 passed by assertion; head 48/48 three times; suite 56 (13 files) -> 104 (17 files); eslint 0; docs-fragments OK with a planted defect caught; merge-tree clean onto develop b8874803 with 0 shared paths. Mutants: 93 of 102 killed; the 9 survivors are one mutant (M8, the ZodError skip in the probe) and are a LOW test gap (G96-F1).

## Heads
- START (logs/head_start.log): PR head `481d1b7a83f9d8e6bf96b80114d548df974a8ebc` (as expected), develop `b887480394cc67764922b0aa123027c344241ed7`, merge-base = parent = `03977e89a343ad7362760e4fb0270602fb6da5ce`. One commit.
- END (logs/head_end.log): both unchanged. Product sha256 `d5afff9cd2073371...` at start and end (restored after every mutant/probe run). Working tree clean except my own untracked `tsconfig.gate96.json`.
- Clone: no direct clone attempted; gate 90's `.git` copied to `repo/`, PR head and develop fetched (refs/qa/pr1914, refs/qa/develop), checked out -f. Install: `npm ci --ignore-scripts -w packages/shared -w services/analytics --include-workspace-root` at Blockchain/Dev (the services are npm workspaces; an install inside one service alone leaves `@secuura/shared` and eslint deps unresolved). Node v26.8.1 only: NOT measured on Node 24.
- PR body not read (no gh auth for Secuura); I used the author's READY and BUILT AND PROVEN mails (evidence/). Body wording I could not see is not verified.

## 1. Diffstat (logs/diffstat.log, three-dot vs 03977e89)
7 files, +739/-12: analytics.ts +102/-12 (the only product file), four new test files (139/150/150/154), two fragments (flow 20, cheat 24 lines). Exactly the PR's claim; nothing outside the declared paths.

## 2. The hunks
- 12 hunks. Three O60 sites (GET /realtime, GET /exports/:id, GET /exports): `logger.error(..., { error: error instanceof Error ? error.message : String(error) })` becomes a 6-line `let reason: string; try { reason = <same expression> } catch { reason = 'unreadable thrown value' }` plus `{ error: reason }`. Nothing else changes (message text, constant 500 body, level).
- Nine O61 sites (overview, certifications, verifications, governance, revenue, users, activity, POST exports, POST reports): `catch (error)` -> `catch (thrown)`, `let error: unknown = thrown;`, a probe `try { if (!(thrown instanceof z.ZodError)) { String(thrown instanceof Error ? thrown.message : thrown); } } catch { error = new Error('unreadable thrown value'); }`, and the untouched code below (the 400 branch on `error instanceof z.ZodError`, the `logger.error` line, the constant 500). For an ordinary ZodError `error === thrown`, only the `instanceof` runs, so the 400 branch and its `details: error.errors` are unchanged by construction. The probe makes the same two reads, in the same order, as the old code.

## 3. Q1: behaviour (RUN: real Express router; scripts/probe.test.ts, probe.sh, probe_cmp.py; logs/probe_base.json, probe_head.json, probe_cmp.log)
Real `express()` + `express.json()` + the real `routes/analytics.ts` + the real `AnalyticsQuerySchema/ActivityQuerySchema/ExportRequestSchema/ReportRequestSchema` (real `@secuura/shared`). Replaced: `analyticsService`, `exportService` (plain functions that reject with the value under test) and the logger (records message and a JSON copy of the meta). Real HTTP via fetch on 127.0.0.1, 2.5 s abort for "no response", `process.on('unhandledRejection')` counted. 117 cells at base and at head.

| value thrown (12 routes unless noted) | base | head | identical? |
|---|---|---|---|
| ordinary Error('boom ordinary') | constant 500, log with its message | same | yes (12/12) |
| string, plain object, null | constant 500, logged as String(v) | same | yes |
| ZodError rejected by the service | 400 with details = its issues, nothing logged | same | yes (9/9 Zod routes; on the 3 O60 routes it is an ordinary Error and gets 500, same at both) |
| REAL ZodError from the real schema (bad query/body; 9 routes) | 400 "Invalid query parameters / Invalid request body-style" message and `details` from the schema | byte-identical body | yes (9/9) |
| ZodError whose `message` getter throws (9 Zod routes) | 400 | 400, body identical | yes (9/9) |
| revoked Proxy, Error with throwing message getter, null-prototype object (12 routes x 3 = 36) | NO RESPONSE (abort), 0 logs, 1 unhandled rejection | constant 500, 1 log `{error:'unreadable thrown value'}`, 0 unhandled | the only change, and it equals what an ordinary Error gets |
| ZodError whose message getter throws on the 3 O60 routes | no response, 1 unhandled | 500, constant log | change (they read `.message`; it is an unreadable value there) |

Persisted state: none of the 12 routes writes in the catch; POST /exports and POST /reports call a service that already ran or failed, and the catch changes nothing it did (read from source; the service was a stand-in). Verdict on Q1: **yes**. The 400 branch is byte-identical (ordinary and real ZodError), an ordinary Error is today's 500, and only an unreadable value changes, from no-response to the constant 500. This also measures what the author's fragment calls "the operators' reading, not run here": with a real Express 4.22.3 the base request never answers and Node sees an unhandled rejection (G96-F3).
Also read: the logged value on the new path is the constant string, never a field of the thrown value.

## 4. Q2: the hand edit (logs/q2/*, scripts/tsc.sh, logs/tsc.log)
- Each PR test file was compared to the operators' generated source (the `+` lines of `section_2.diff`, which equals `.decl` and `.tdz` for all four): the ONLY difference in all four files is one line, `await import('../routes/analytics');` -> `await import('../routes/analytics.js');` (lines 88, 95, 95, 99). Four tokens, test files only, nothing else in them.
- tsc (scratch `tsconfig.gate96.json` extending the service tsconfig, include `src/**/*`, tests included, noEmit): **head as pushed 1 error** (`db.retry.test.ts:36` TS2835, pre-existing); **head with the four tests at the operators' bytes: 5 errors** (that one + one TS2835 in each new test); **base (product at 03977e89, the four test files absent): 1 error**, the same line. Plain `tsc --noEmit` on the head product: rc 0.
- Hand edit does not change what runs: vitest resolves `.js` to the `.ts` (48/48).

## 5. Q3: product hunks equal the held sections (scripts/q3.sh, logs/q3.log)
Each pass's `out.md.checker/section_1.diff` (run dirs without -control) applied to the base file, in old-line order O61-P1, O61-P2, O60-P1, O61-P3: all four apply, and the resulting file is **byte-identical to the PR head's analytics.ts** (cmp). Changed-line counts per pass: O60-P1 24, O61-P1 30, O61-P2 30, O61-P3 30 = 114, equal to the PR's 114 (sorted +/- multiset EQUAL).
- O60-P1: EQUAL
- O61-P1: EQUAL
- O61-P2: EQUAL
- O61-P3: EQUAL

## 6. Re-measure (logs/runs.log; scripts/runs.sh)
- Head, new files: **48/48, 4 files, three runs**. Base product + new files: **24 failed | 24 passed**, all 24 failures are `RED ks1868 R1/R2` cells (6 of 12 per file), by `AssertionError: expected 200 to be 500`; 0 TypeError, 0 import errors; all C1/C2 controls pass at base. Restore RESTORE_OK.
- Whole analytics suite: base without the new files **13 files, 56/56** (`--exclude 'src/__tests__/ks1868-analytics-routes-*'`); base + new 104 tests, 24 failed, 80 passed; head **17 files, 104/104**. Ratio 56 -> 104 (+48 = the 4 x 12 cells), no existing test changed.
- eslint (services/analytics cwd, root flat config) on analytics.ts + the 4 test files: 0 problems, rc 0 (logs/eslint_pr.log); planted file: `no-debugger` error + unused-var warning, rc 1.
- docs-fragments check: OK, "flow 117 legacy + 64 new, cheat 112 + 64 new", rc 0. Planted literal section number "7." in the flow fragment: rc 1, two findings naming the file; restored byte-identical, rc 0 after. It prints 2 ADVISORY lines; both also print with the PR's fragments removed (logs/frag_without_pr.log), so neither comes from this PR.

## 7. Mutants (scripts/mutants.py, scripts/mut400.py; product file only, tests untouched, sha256 restored and checked after every run: all True)
- 102 runs: 9 Zod sites x 9 mutants + 3 O60 sites x 7 mutants. **93 killed, 9 survived.** In no run did a cell of ANOTHER route turn red (0 cross-route): each mutant is caught by its own route's cells.
- O61 sites (9 mutants): M0 drop the probe (revert) R1 R2; M1 probe read removed R2; M2 `error = thrown` in the catch R1 R2; M3 replace always C1 C2; M4 rethrow R1 R2; M5 constant text changed R1 R2; M6 guard inverted R2; M7 probe reads only `instanceof Error` R2; **M8 drop the ZodError skip from the probe (`if (true)`): SURVIVED at all nine sites** (G96-F1).
- O60 sites (7 mutants): revert R1 R2; constant for all values C1 C2; rethrow R1 R2; constant text R1 R2; readable string branch const C2; readable Error branch const C1 R2; `String(error)` only C1. All killed (the C2 string cell kills the readable non-Error branch here, unlike gate 90's G90-F3).
- Q4 mutants (400 branch, 9 sites x 3: drop `details`, `details: []`, change `code`): **27/27 KILLED**, every time by the site's own C1 cell.

## 8. merge-tree (logs/merge_tree.log, merge_result_vs_develop.log)
`git merge-tree --write-tree` develop `b887480394cc` + PR head: rc 0, tree `1d5af464d64c...`, clean. The result differs from develop in exactly the PR's 7 paths (4 test files A, analytics.ts M, 2 fragments A). Develop moved 3 commits past the base (cde2dee4 mcp-server, c8d77dce auth, b8874803 nft minting), 17 files changed, **0 shared paths** with the PR's 7. The merged analytics.ts blob equals the PR head's blob (32bb4e9f).

## 9. Kam's ks1346 logging rule (type and field names, never values)
No new log line is added. The 12 sites log the same message strings; the value logged on the new path is the constant `'unreadable thrown value'`, never the object, a field or a getter result. The existing ordinary-path behaviour (logging `error.message` of an ordinary Error, `String(error)` of a string) is unchanged by this PR and is the pre-existing practice in these routes; I did not judge it against ks1346 here. The 400 branch logs nothing. Complies.

## 10. FINDINGS / notes for the PR body
- **G96-F1 (LOW, test gap, measured)** Mutant M8 (drop `!(thrown instanceof z.ZodError)` from the probe, so a ZodError would also be message-read) survives at all nine Zod sites: no committed cell throws a ZodError whose `message` getter throws. Behaviour at head is right (my probe: 400, body identical to base, 9/9), the skip is the thing that keeps it, and it is practically unreachable (a ZodError's message is JSON.stringify of its issues, which are built from request strings). Optional: one extra C-cell. Not FIX-BEFORE-MERGE.
- **G96-F2 (INFO, positive)** Q4: no analytics test pinned the 400 body before (ks1364 tests only exercise the schemas/OpenAPI; nothing imports routes/analytics.ts). The nine new C1 cells are the first pin and they pin it fully: `toEqual` on `{success:false, error:{code:'BAD_REQUEST', message:<route text>, details: zerr.errors}}` plus "logger.error not called". Dropping `details`, emptying it or changing the code is caught at every site (27/27). Limit: the C1 cells use pass-through schema stand-ins and a hand-built ZodError; the real schemas' error bodies are covered only by this gate's uncommitted probe (identical base vs head, 9/9).
- **G96-F3 (INFO, wording)** The flow fragment says the "real Express 4" and "real request schemas" are not run and that Express 4 leaving a rejected async handler unhandled "is the operators' reading". This gate ran both (Express 4.22.3, real schemas, real HTTP): base = no response + one unhandled rejection, head = constant 500, 0 unhandled. The PR body may say so, citing the gate. (The caveat "the cells call the handlers directly" stays true for the committed cells.)
- **G96-F4 (INFO)** The nine Zod catches probe once and the old code then reads again: a getter that throws only on its second read is not covered (already named by the author). Same for the three O60 sites (single read, so fine).
- **G96-F5 (INFO)** Environment: the four services in this repo are npm workspaces; an install inside the analytics folder alone misses `@secuura/shared` (5 of 17 files fail to load) and the root eslint deps. The fragments' run line `npm run test -w services/analytics` from Blockchain/Dev is the right one.
- Tier: 2 is reasonable (read/report analytics routes, catch-only, constant 500, no money/keys/auth); nothing here argues for 1.

## 11. NOT TESTED
The real PR body text (no gh auth); a booted analytics service, the gateway proxy hop (read from the mails), a real database or the real export/analytics services (stand-ins reject with the value); Node 24; the four platform suites; CI; the pre-push hook legs (quoted from the author's mail: 13/16 ran, 3 skipped, nothing failed); the Linear ticket text; whether an unreadable value can really arise from the real services (synthetic values only; my guess is no, same as every KS-1868 site).

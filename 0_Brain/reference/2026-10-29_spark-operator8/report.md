# Spark operator 8 report, 2026-10-29 (tip e4cd2e1325ba = refs/wed/develop in the cache clone)

## BLUF

All three briefs are READY TO QUEUE (dry-run OK, golden control PASS 7/7 + A2a, golden BYTE-IDENTICAL). Nothing was queued, queue.md untouched, queue.sh not started, no model call made.

| brief dir | what | tier | exact queue line (for queue.md) |
|---|---|---|---|
| `night/briefs/ks_1801_p1` | KS-1801 part 1: 9 of the 11 S1-only sites (the `isMissingTableError` GETs), as 9 new ROUTES rows + a `withTenant` mock fix | test_only | `ks_1801_p1` |
| `night/briefs/ks_1801_p2` | KS-1801 part 2: the other 2 sites (the `errorMessageIncludes` ones: POST /document-types, GET /rights-holders/:id/documents), a new describe block | test_only | `ks_1801_p2` |
| `night/briefs/ks_1802_p1` | KS-1802: adminConfig.ts:2112 `err?.message` in the seed loop catch (9-line helper + one changed line) + a NEW jest test | code_patch | `ks_1802_p1` |

Each dir carries its own `spark.pins`, so the queue line is just the dir name (relative dirs resolve against `local-model/night/briefs/`).

Cautions for Wednesday before queueing / raising:
1. **p1 and p2 edit the SAME test file** (p1 at :14 and :54, p2 inserts at :98). They apply independently at the tip, but raise them as ONE change, or regenerate p2 after p1 merges (its hunk header line numbers shift, and round.sh refuses a brief whose named file moved since `Tip:` unless `allow_drift=1`).
2. `overlap.py` reports OVERLAP **held** only against `READY_KS-1780-...ks_1780_p2_admin_s` (the test file) and `READY_KS-1779-...ks_1779_p1` + the same KS-1780 p2 (adminConfig.ts). Those held passes are already on develop (git log of adminConfig.ts at the tip: `e4cd2e132 #1802 Refs KS-1780 part 2`, `b5583cb69 #1787 Refs KS-1779`), so the overlap is stale, not live. Wednesday to confirm.
3. **Open PRs: no overlap.** overlap.py read all 60 open-PR file sets of the Secuura repo with the project's gh token (in a scratch GH_CONFIG_DIR); none touches any file of the three briefs.
4. **Lanes: none touched.** The only files in the three goldens are `originate/src/routes/adminConfig.ts` (ks_1802_p1 only) and two originate `__tests__` files. No anchoring/**, hono, lockfile, package.json, certifications.ts, originate.openapi.ts, docs/openapi/** or Projects Documents/*.html.
5. Both KS-1801 briefs declare 26 / 4 RED cells by title substring (the tamper also reddens the 4 already-existing rows, and the checker counts an undeclared red as a failed control, so they are declared too). Because the new rows are table rows, A3x byte checks do not apply (test_only).

Not ready: none. Not briefed: nothing else was screened for task 2 (KS-1802 was the obvious candidate and consumed the room I had). The NEXT-PICKUP filing lists name no other adminConfig/Secuura ticket I judged a Spark fit without a longer read.

## The 11 sites (e4cd2e1325ba, all in `Blockchain/Dev/services/originate/src/routes/adminConfig.ts`)

15 catch sites call a guarded reader. Driven already by ROUTES (4): GET /document-types :212, /workflows :312, /settings :543, /organizations :840. The 11 S1-only:

| # | file:line (the guarded call) | route | method | helper | p |
|---|---|---|---|---|---|
| 1 | :248 | /document-types | POST | errorMessageIncludes 'unique constraint' (409) | p2 |
| 2 | :400 | /verification-queue | GET | isMissingTableError | p1 |
| 3 | :455 | /integrations | GET | isMissingTableError | p1 |
| 4 | :724 | /verification-policies | GET | isMissingTableError | p1 |
| 5 | :955 | /api-keys | GET | isMissingTableError | p1 |
| 6 | :1248 | /audit-logs | GET | isMissingTableError | p1 |
| 7 | :1411 | /rights-holders | GET | isMissingTableError (query inside `withTenant`) | p1 |
| 8 | :1589 | /rights-holders/:id/documents | GET | errorMessageIncludes 'does not exist' (200 empty) | p2 |
| 9 | :1680 | /users | GET | isMissingTableError | p1 |
| 10 | :1717 | /identity/users | GET | isMissingTableError | p1 |
| 11 | :1745 | /identity/organizations | GET | isMissingTableError | p1 |

The count 15 = 13 `isMissingTableError(err)` + 2 `errorMessageIncludes(err,..)` call sites; the file's own header comment still says "fifteen catch blocks / four GET routes".

## ks_1801_p1 (test_only)
- Path: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1801_p1/` (KS-1801.md, golden.diff, spark.pins: tier=test_only, test_file, ref=ks1780-system-errors-list..., line=142, ctx=65536; ctx was needed: first dry-run REFUSED at ~34.7K prompt tokens vs 32768).
- Edits (2 points, one file `ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts`): (1) :14 `withTenant: (_t: unknown, fn: () => unknown) => fn(),` -> `fn: (tx: unknown) => unknown) => fn({ $queryRaw: mockQueryRaw, $executeRaw: jest.fn() })` (rights-holders queries through `tx.$queryRaw`; with the old mock `tx` is undefined and C1/C2 would 500). (2) ROUTES: 9 rows appended after the /organizations row (:54).
- Tamper: adminConfig.ts:142 `  try {` -> `  JSON.stringify([err?.message, err?.code]); try {` (isMissingTableError reads the value outside its try).
- --dry-run: `SPARK ROUND ks_1801_p1: DRY-RUN OK — brief accepted, input built at e4cd2e1325ba (138856 B) in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/state/dry/ks_1801_p1_20261029-164127; a real round would call http://127.0.0.1:47788 with code_patch/task.md, thinking OFF`
- --control: `SPARK ROUND ks_1801_p1: CONTROL-PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip e4cd2e1325ba · 153s round, no model (control) · /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1801_p1-control`
- Checker detail: A3 test-only file set OK; A4 26 failed / 66 run under the tamper, controls green, assertion reds; A5 66 passed / 66 run at the tip; A6 no new red; A7 tsc rc 0; 7/7.
- Run dir: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1801_p1-control`

## ks_1801_p2 (test_only)
- Path: `.../night/briefs/ks_1801_p2/` (pins: tier=test_only, same test_file/ref, line=134, ctx=65536).
- Edit (1 point): one hunk inserted above `describe('KS-1780: ...` (:98): `MESSAGE_ROUTES` (2 rows: POST /document-types with JSON body, GET /rights-holders/:id/documents), its own caller `callMessageRoute` (method/body aware; the existing `callWithThrow` is left untouched), and a describe with B1/B2 (RED: revoked Proxy, throwing getter -> constant 500), D1 (recognised Error answered as before: 409 / 200 empty), D2 (ordinary Error), D3 (`{code:'42P01'}` is NOT recognised by these two catches -> 500). Inserted above, not appended, because the builder refuses a pure insertion with no trailing context.
- Tamper: adminConfig.ts:134 `  try {` -> `  JSON.stringify(err?.message); try {` (errorMessageIncludes).
- --dry-run: `SPARK ROUND ks_1801_p2: DRY-RUN OK — brief accepted, input built at e4cd2e1325ba (140303 B) in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/state/dry/ks_1801_p2_20261029-164141; a real round would call http://127.0.0.1:47788 with code_patch/task.md, thinking OFF`
- --control: `SPARK ROUND ks_1801_p2: CONTROL-PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip e4cd2e1325ba · 84s round, no model (control) · /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1801_p2-control`
- Checker detail: A4 4 failed / 31 run, controls green; A5 31/31; 7/7.
- Run dir: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1801_p2-control`

## ks_1802_p1 (code_patch; KS-1802)
- Path: `.../night/briefs/ks_1802_p1/` (pins: tier=code_patch, ref=ks1780 test, line=148, ctx=65536).
- Edits: product adminConfig.ts, TWO hunks: (1) after `isMissingTableError`'s closing `}` (:147) insert a blank line + doc comment + `function readableErrorMessage(err: any): string | undefined { try { return err?.message; } catch { return 'thrown value that could not be described'; } }` (7 lines); (2) :2112 `error: err?.message` -> `error: readableErrorMessage(err)`. Test: ONE NEW file `ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` (6 cells: R1 revoked Proxy on every insert, R2 throwing getter on every insert, R3 hostile on the first user only; each expects 200 with the failed/created counts instead of the constant 500; controls C1 ordinary Error + message logged, C2 all created, C3 all conflict). Both seed env flags are set before import, the route is driven over a loopback listener with the KS-1780 mocks.
- --dry-run: `SPARK ROUND ks_1802_p1: DRY-RUN OK — brief accepted, input built at e4cd2e1325ba (136525 B) in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/state/dry/ks_1802_p1_20261029-164154; a real round would call http://127.0.0.1:47788 with code_patch/task.md, thinking OFF`
- --control: `SPARK ROUND ks_1802_p1: CONTROL-PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip e4cd2e1325ba · 117s round, no model (control) · /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1802_p1-control-r2`
- Checker detail (first control, same golden text bar two UNMEASURED/prose lines): A3 file set OK; A3c 9 plus lines; A4 3 failed / 6 run at the tip, controls green; A5 6/6; A6 no new red; A7 tsc rc 0; 7/7. The `-control-r2` run is the regeneration after I corrected two prose lines (helper is 7 lines, not 8; a range note); the product/test bytes are unchanged.
- Run dirs: `.../runs/spark_secuura_2026-10-29_ks_1802_p1-control` and `.../runs/spark_secuura_2026-10-29_ks_1802_p1-control-r2`
- Judgement call: KS-1802 changes product behaviour in a demo-only route (Low); it is a 2-hunk, one-file product change with a mechanism-checked new test, the rung-2 shape (like ks_1684_p1). Its PR must say it Refs KS-1802 until the QA gate. Wednesday decides whether it fits the tier rules; it is not a security-shaped change.

## TESTED / NOT TESTED / HOW
TESTED:
- brief_lint (inside round.sh) accepted all three; builders produced inputs (136-140 KB, ~34-35K prompt tokens at ctx 65536).
- Golden controls through the real checker in the cache-clone work dir: jest runs of the touched test files, A4 red under tamper (test_only) or at the tip (code_patch), A5 green, whole services/originate suite no new red, tsc rc 0, A2a anchors. All BYTE-IDENTICAL to golden.
- Open-PR and held-READY overlap with gen/overlap.py (60 open PRs read).
- The ks1000 cache-clone red cells (IMPROVEMENTS 2026-10-29) did not occur for originate; they are the auth/api-gateway suites and were not in play.
NOT TESTED:
- No real Spark model round (not my job). So whether DeepSeek reproduces the 10-line ROUTES table, the 55-line p2 block or the 129-line new test byte-exactly is UNMEASURED; the test_only briefs give every + line, so the expected risk is transcription, not design.
- p1/p2 raised together or in sequence (the combined file) was not run: each was controlled alone against the tip. Applying both goldens to the tip together was not checked.
- Nothing was run against a real database or the live route; the cells use the file's mocked prisma.
- ESLint on the added lines (the repo has lint-warning tickets like KS-1779) was not run.
- No harness fault was found, so I fixed none and added no IMPROVEMENTS row.
HOW: `bash local-model/spark/round.sh <dir> --dry-run` then `--control`; specs that generated the dirs are kept beside this report (`spec1801p1.py`, `spec1801p2.py`, `spec1802.py`; regenerate with `GEN_OVERWRITE=1 GEN_TIP=e4cd2e1325bacbe1fd39e549f8aaefc943485d12 python3 -I spark/gen/mk_testonly.py <spec>` (p1,p2) or `mk2.py <spec>` (1802); each brief's spark.pins then needs the line `ctx=65536` added by hand, mk_testonly does not write it).

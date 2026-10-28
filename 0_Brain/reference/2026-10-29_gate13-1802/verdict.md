# QA GATE 13 (tier 2, round 1 of 2) - Secuura/Blockchain PR #1802 - head 8f38c452

## BLUF

**Verdict: GO WITH NOTES.** 0 Major, 1 Minor, 3 Note.

All 15 catch sites survive a hostile thrown value. I drove every one of them myself (the builder's cells drive only 4). No ordinary-error behaviour changed: 150 base-vs-head outcome pairs, 0 differences. The 9 reds fail for the stated reason, and the product hunks are byte-identical to the canonical Spark patch. Docs are additions only. The notes are about test coverage (11 of 15 sites pinned only by a source-text cell) and one unhardened sibling read in the same file that is out of scope.

## Findings

| id | severity | what | where (head) | evidence |
|---|---|---|---|---|
| 1802-1 | Minor | 11 of the 15 hardened sites have no behavioural cell in the PR. They are pinned only by S1, a source-text regex (`^\s*if \(err\?\.(message\|code)`). S1 would not notice a site that reverted to a differently shaped direct read (for example `if (!err.message.includes(..))` or a read not at the start of a line). Behaviour for all 15 is correct today (see matrix), but nothing in the PR keeps it so. The PR's own docs admit "four GET routes". | test file, S1 cell (last `it`), and `ROUTES` const (4 entries) | My scratch matrix (not committed, copy in this folder as `scratch-matrix.test.ts.txt`) shows all 15 sites answer 500 for the 3 hostile shapes. It also shows that, at base, 14 of 15 hang (the 15th, see 1802-3, is the ordinary-shape control for the same harness). Extending `ROUTES` is cheap: 11 more entries, with POST /document-types and /rights-holders/:id/documents needing a body or id. Not blocking. |
| 1802-2 | Note | Semantics are `=== true`, where the old code was truthiness. `err?.message?.includes(x) === true` differs from the old `if (err?.message?.includes(x))` only if `message` is a non-string whose `includes` returns a non-boolean truthy value. No such value arises from pg, Prisma, or Error. Also, a thrown object whose `message` getter throws but whose `code` is `'42P01'` now gets 500 instead of the empty list. That is the intended hostile-value handling (the whole `\|\|` expression sits in one try). | `routes/adminConfig.ts` 133-147 | Read. Matrix `codeGetter` shape gives 500 at all 15 (for the 12 sites with a code test, the `message` is `'boom'`, so the code getter throws inside the try). |
| 1802-3 | Note | Out of scope but same file and same pattern. The inner catch in seed-demo-users still reads `err?.message` unguarded inside the `logger.error` argument. A hostile throw there escapes the inner catch. It is inside the route's outer try, so the outcome is the outer `fail500` constant 500, not a hang, but the seed loop stops and `failed` is not counted. The prior KS-1772 pass did not cover it either. Not one of the 15, not driven by me. | `routes/adminConfig.ts:2112` | Found by `grep -nE 'err\??\.'` over all 88 `catch` tokens. The only remaining direct reads of `err` outside helpers and the KS-1772 describers are at 2112 (this one) and 2272 (a guarded describer). Reached outer catch by reading only. |
| 1802-4 | Note | The cells' hostile shapes are revoked Proxy and a `message` getter that throws. A `code`-getter shape is not in the PR's cells (the PR docs say so: "a thrown object whose code getter throws" is Not measured). I measured it: 500 at all 15 sites at head. Also, `GET /rights-holders/:id/documents` has no `42P01` test (it never did, per base), so a `{code:'42P01'}` throw gives 500 there at both base and head - unchanged, not a defect of this PR. | n/a | m_head matrix, `codeGetter` row for 15 of 15 = 500; `code42P01` on `/rights-holders/:id/documents` and POST /document-types = 500 at base and head. |

## What was tested and how

**Q1 - do all 15 sites survive?**
- FOUND: enumerated the sites from the head diff and cross-checked against head. 88 `catch` tokens in the file; the product diff touches 15 conditions. They are GET /document-types, POST /document-types, GET /workflows, /verification-queue, /integrations, /settings, /verification-policies, /organizations, /api-keys, /audit-logs, /rights-holders, /rights-holders/:id/documents, /users, /identity/users, /identity/organizations. Count of 15 confirmed independently. Ten share the `isMissingTableError` shape (message `includes('does not exist')` OR code `42P01`). Two (POST /document-types `unique constraint`, /rights-holders/:id/documents `does not exist`) use `errorMessageIncludes`. Both helpers wrap the whole read in `try/catch` and return false. The shapes are same as the driven ones in kind, and the 11 undriven sites differ from the 4 driven ones only in which helper and which needle.
- TESTED/HOW: scratch jest test in my own clone (never committed; moved out of the tree afterwards; copy in this folder as `scratch-matrix.test.ts.txt`). It reuses the PR test's mocks, drives each of the 15 routes over a real loopback listener with `$queryRaw` rejecting, across 13 thrown shapes: revoked Proxy, throwing `message` getter, throwing `code` getter, ordinary Error, "does not exist", `{code:'42P01'}`, "unique constraint", pg 23505, ZodError-like, string, null, undefined, number. The thrown value is injected through both `prisma.$queryRaw` and my own `withTenant` stub (the PR's `withTenant` mock calls `fn()` with no tx, so `/rights-holders` never reaches the query; I caught this in my first pass, when `/rights-holders` returned a 500 from a TypeError, and fixed my harness before recording).
- Result at head: 195 outcomes (15 sites x 13 shapes). All 45 hostile outcomes (3 shapes x 15) are exactly `500` plus the constant body `{success:false,error:{code:'INTERNAL_ERROR',message:'Internal server error'}}`. Zero NO ANSWER.
- Control (instrument check): same hostile shapes at base. 14 of the 15 routes plus POST /document-types answered NO ANSWER (hang) for revokedProxy and messageGetter; the exception is a tooling note, not a PR defect: the first `/rights-holders` run at base returned 500 only because my stub was wrong, and after the stub was fixed it also hung (b_rh2: NO ANSWER x3). So at base all 15 hang. The instrument fires.

**Q2 - ordinary-error behaviour.**
- TESTED/HOW: base's adminConfig.ts swapped in (copied from `git show 5dccdcb29e:`), same matrix with the 3 hostile shapes skipped: 150 outcomes (15 sites x 10 ordinary shapes); head the same. 0 differences in status or body. Covers per distinct catch shape: the missing-table shape (message and code), the `unique constraint` 409 on POST /document-types, the `does not exist` empty list on /rights-holders/:id/documents, pg 23505, ZodError-like, and non-Error primitives, null, undefined. Statuses seen: 200 empty-list where expected, 409 once, 500 for the rest.

**Q3 - do the 9 reds fail for the right reason, controls at both ends?**
- TESTED: ran the PR's test with base's adminConfig.ts: 9 failed / 12 passed. A1 and A2 on the 4 routes (8 cells) fail at ~1.5 s each, which is the 1500 ms abort timeout, so the failure is the request getting no answer (the hang, via the escaping throw). The ninth is S1, the source matcher. 12 controls (C1, C2, C3 x 4) pass at base and at head. Head: 21/21.

**Q4 - is the diff the canonical patch?**
- TESTED: split `.../runs/spark_secuura_2026-10-28_ks_1780_p2_admin/out.md.checker/patch.diff` into its two file diffs. Added/removed lines of the adminConfig.ts diff: identical (51 vs 51, equal as lists). Hunk headers and context differ only because the PR diff was produced with more context and function-name annotations than the patch file. The test file diff: identical after dropping `index` lines (129 vs 129 lines, equal).

**Q5 - docs.**
- TESTED: `git diff base head -- "Projects Documents"`: 0 removed lines, 2 hunks, 1 added `<h2>` in each of the two HTML files. The Architecture Flow Diagrams doc has the new `105.` section after 104. The QA cheat sheet has an un-numbered h2 for the same topic. The numbers in the docs (9 failed / 12 passed, 146 files / 1724 cells to 147 / 1745) match what I measured for the head side and the 9/12 base side.

**Gates run at head:** full originate jest 147 suites / 1745 tests, rc 0; `tsc --noEmit -p tsconfig.json` rc 0; eslint on the two touched files `--max-warnings 0` rc 0.

## NOT TESTED

- A real Postgres or a real running stack: everything is mocked at `$queryRaw` and `withTenant`. A real pg error object (for example a `PrismaClientKnownRequestError`) was approximated by plain Error with `code`.
- Base's 146 files / 1724 cells (the docs' base figure). I ran the full suite only at head.
- The four platform suites the docs call UNMEASURED.
- The Node 24 LTS run (mine is Node v26.8.1, same as the builder's host).
- Whether other route files in originate have the same pattern (out of scope for this PR).
- Line 2112 behaviour, by reading only (1802-3).
- Eleven shapes other than the three hostile ones were not run hostile-style through each helper's `=== true` branch beyond the ones listed (a non-string `message` with a truthy `includes` was not constructed).

## Setup

- Clone: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate13-1802/repo` (did not exist before; made with mkdir plus `git init`).
- Toplevel assert before any fetch: equal to the clone path. Toplevel assert at the end: equal to the clone path. Both OK.
- Fetched with the project deploy key via `GIT_SSH_COMMAND` (`-o IdentitiesOnly=yes`), `--depth=50`, refs `develop` and `refs/pull/1802/head`. Head 8f38c45284fafda02ad94e63934fa0d2dae9e21d; its single parent 5dccdcb29ec20393e80cbdb1e359a49caa633165 (develop tip). Working tree clean at the end (the scratch test was moved out; adminConfig.ts restored to head, `git status` empty).
- `npm ci` in `Blockchain/Dev` (1806 packages, rc 0), then `npm run build` in `packages/shared` at the head commit (tsc, rc 0). The Secuura project's own node_modules were not used.
- Tests run from `Blockchain/Dev/services/originate` with `npx jest`. The base-vs-head swaps copied `git show 5dccdcb29e:...adminConfig.ts` over the product file and restored the head copy (a saved copy in the scratchpad) afterwards.
- No network call except the git fetch. No Docker. No process stopped. Nothing written under `!CODING`. Nothing posted anywhere.
- Artifacts: this file and `scratch-matrix.test.ts.txt` (the matrix, in this directory).

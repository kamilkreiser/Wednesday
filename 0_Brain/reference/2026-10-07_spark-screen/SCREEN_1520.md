# KS screen for the Spark: 2026-10-07, 15:20 batch (2 briefs delivered, both KS-1410, one on code_patch2)

Written 2026-10-07 15:35 AEDT (shell `date`; the briefs are stamped 15:30:26) by a Spark brief-writer sub-agent for Wednesday. Secuura only. Authority: Wednesday's 15:17 commission (keep the Spark fed toward 50 tasks a day; prioritise the new multi-file tiers), the kit predicate (`spark-kit_2026-09-23/02_FOR_THE_COORDINATOR.md` §2) and the round counter (original + ONE rebrief).

**Read-only on client systems:**
- Linear: GraphQL reads only. `LINEAR_API_KEY` came from the Blockchain `4_Credentials/.env` in a `set -a` subshell and was never printed.
- GitHub: REST GET only (open PRs and their files). `GH_TOKEN` was handled the same way.
- Git under `!CODING/`: read verbs only (`ls-remote`, `show`, `grep`, `ls-tree`, `status`, `log`). The checkout reads 0 tracked-modified lines after the work.
- Every git write verb ran in a `git clone --shared` copy under this session's scratchpad.
- `round.sh --dry-run` and `--control` used round.sh's own cache and run dirs.

**Not touched:** `spark/queue.md`, `night/queue.md`, `PAUSE_QUEUE`. No model round was run. No mail, no Linear write, no GitHub write, no tmux.

## BLUF

1. **Tip:** develop `147ae442074c7f3b5be9ce7ccc4452c8dae34b4f`. `ls-remote` read it at 15:17:17 and again at 15:34, unchanged. This is the tip the commission expected.
2. **Board count: 276** KS Backlog + Todo (246 backlog + 30 unstarted).
   - Instrument: GraphQL `issues(first:100)` with filter team KS and `state.type in [backlog, unstarted]`, paginated until `hasNextPage` was false (3 pages). This is a real count, not a cap: 276 nodes, 276 distinct identifiers.
   - Positive control: KS-1435, KS-1410 and KS-1438 are all in the pull.
   - The 11:20 screen counted 275. The one added since is KS-1438, created today.
   - Only one ticket was updated after 11:20 (KS-1438, which is excluded), so the 11:20 verdicts on the 10-06 delta still stand.
3. **Delivered: 2 briefs.** Both pass `--dry-run` with rc 0 ("DRY-RUN OK", prompt source WEDNESDAY BRIEF). Both pass `--control` with **CONTROL-PASS 7/7 + A2a, golden BYTE-IDENTICAL**.

   | Brief dir (`2_Project_Files/local-model/night/briefs/`) | Ticket | Tier | Files | Edits | Dry-run | Control |
   |---|---|---|---|---|---|---|
   | `KS-1410-apigw-batch-audit-export-500` | KS-1410 | **code_patch2** (rung 3) | `api-gateway/src/routes/batch.ts`, `routes/audit-export.ts`, new `__tests__/ks1410-batch-and-audit-export-500-never-answer-err-message.test.ts` (136 lines) | 6 product hunks: 4 in batch (import + helper, 3 one-line sites), 2 in audit-export (import + helper, 1 site) | rc 0 | PASS 7/7. A3x 3/3 files byte-identical. A4: 9 failed / 12. A5: 12/12. A6 and A7 OK. 53 s. `runs/spark_secuura_2026-10-07_KS-1410-apigw-batch-audit-export-500-control` |
   | `KS-1410-apigw-notifications-500` | KS-1410 | code_patch | `api-gateway/src/routes/notifications.ts`, new `__tests__/ks1410-notifications-500-never-answers-err-message.test.ts` (138 lines) | 7 product hunks: import + helper, then 6 identical one-line sites | rc 0 | PASS 7/7. A3b 6/6 sites. A4: 12 failed / 15. A5: 15/15. A6 and A7 OK. 57 s. `runs/spark_secuura_2026-10-07_KS-1410-apigw-notifications-500-control` |

   Each dir holds `KS-1410.md`, `golden.diff` and `spark.pins`. The pins:
   - batch/audit-export: `tier=code_patch2 ref=…/notifications.test.ts line=166`
   - notifications: `tier=code_patch ref=…/notifications.test.ts line=126`

   sha256 prefixes:
   - batch/audit-export: brief `128414fe73b0fa10`, golden `417c112c7be043da`
   - notifications: brief `4f5e1e901a59a160`, golden `59f20b6bc1af75ba`
4. **Routing reason (both go to the Spark).** This is the KS-1334 / KS-1341 class, which the Spark has already passed. Originate's `fail500` is held as READYs dated 09-26/27, and KS-1334's copy is landed at the tip (`adminConfig.ts:103`).
   - These briefs use the same helper and the same constant body, with an in-process router test (no server, no network).
   - The fix shape is the ticket's own: *"KS 1334 and KS 1341 are the same defect, already fixed per-file"*.
   - Neither brief is an auth surface. Every 401/403/400 gate is untouched, and each gate is pinned green by a control cell.
5. **Over the kit's 3-edit rule, stated in both briefs.** The notifications brief has 7 hunks and the batch/audit-export brief has 6. Neither can be split: every site calls the helper that the first hunk adds, so a second carve could only run after the first merged. This is the same reason Wednesday queued KS-1274 at 8 hunks. Every site hunk is the same one-line shape.
6. **The two goldens stack.** With both applied, the api-gateway suite goes from **92 files / 818 tests / 0 failed at the tip** to **94 / 845 / 0**, and `tsc --noEmit` returns rc 0 (hand-measured in a scratch clone). Between them they close 10 of KS-1410's 28 sites. **Refs KS-1410; they do not close it.**
7. **Why only 2 and not 4–8.** I re-screened every ticket the earlier screens rejected only for "multi-file". None is left whose only blocker was the file count; each fails another clause (see the table). The 15 tickets no prior screen had named were read in full: only KS-1410 passes. Its other sites fail on their own clauses (see follow-ups). **The pool, not the tiers, is the limit.**
8. **Not queued.** Wednesday appends the two dir names to `spark/queue.md`. Counter: round 0 of 2 on both.

## Delivered briefs: detail

| Dir | Ticket | Tier | Files | Edit count | Dry-run rc | Control | Routing reason |
|---|---|---|---|---|---|---|---|
| `KS-1410-apigw-batch-audit-export-500` | KS-1410 (Backlog, Kamil, 0 comments) | code_patch2 | 2 products + 1 new test | 6 hunks (2 import + helper, 4 one-line) | 0 | CONTROL-PASS 7/7 + A2a 6/6, BYTE-IDENTICAL | multi-file tier as asked; precedent fix; in-process cells |
| `KS-1410-apigw-notifications-500` | KS-1410 | code_patch | 1 product + 1 new test | 7 hunks (1 import + helper, 6 one-line) | 0 | CONTROL-PASS 7/7 + A2a 7/7, BYTE-IDENTICAL | same class; single file, so the tier is code_patch |

How the goldens were measured: in a `--shared` scratch clone at the tip, with node_modules farmed by `tasks/code_patch/prepare_clone.sh`.
- **Red-first.** At the tip, the new test alone fails 9/12 for batch/audit-export and 12/15 for notifications. Every failure is an `AssertionError`.
- **Each product file is load-bearing.** With batch.ts alone, the 2 audit rows red. With audit-export.ts alone, 7 rows red.
- **Real reachable path (R3).** `POST /api/batch/certifications` with `{"documents":[null]}` returns the TypeError text in the 500 body today.
- **Strict apply.** Each brief's fences, assembled, apply strict at the tip, and the results are `cmp`-identical to the hand edit.
- **ASCII only.** Every fence is all ASCII. The notifications first hunk's trailing context stops at `:19`, because `:20` carries an em dash.

## Verdict table: every ticket screened this session

Read in full this session (the 15 that no prior screen named, the multi-file re-screens, and the KS-1410 sibling sites):

| Ticket | Verdict · predicate clause that failed |
|---|---|
| **KS-1410** 28 unguarded `err.message` in 500 bodies | **BRIEFED ×2** (10 of 28 sites). |
| KS-1410 `transfer/src/routes/delegations.ts:283` (1 site) | NOT: **Seat E 10th's files** (`services/transfer`). |
| KS-1410 `tenant-provisioning/src/index.ts` (7 sites) | NOT: **no in-process harness**. Importing `index.ts` runs a top-level `await platformPool.query` and `app.listen` (10-06 screen, unchanged). |
| KS-1410 `mcp-server/src/http-server.ts` (10 sites) | NOT: **no in-process seam**. `enforceProductionConfig` and `app.listen` run at module load and the app is not exported. Each site is a 2-line pair; 10 hunks plus a helper exceeds any one brief, and carves would need the helper merged first. KS-1214's open file-read defect (security) is in the same file. |
| KS-1419 revoke 400 vs 404 when deleted mid-race | NOT: **decision**. "for example a discriminated result … or a cheap existence re-read", and both touch every caller of `updateDocument`. |
| KS-1409 webhooks reject connector principals | NOT: **decision** ("could reasonably be a 4xx, or the list could be keyed on the organisation … the owner's"); connector-principal (auth) surface. |
| KS-1407 password change leaves other sessions live | NOT: **auth/session surface**. |
| KS-1420 gate63 minors on KS-1404 trust anchors | NOT: **security surface** (TSA trust anchors). N-1388-3 is also a test-only regex cell, and no tier takes test-only. |
| KS-1415 gate62 minors | NOT. Item 1 is the two platform docs under `Projects Documents/` (**excluded**). Item 2 is a **bash test-only** count cell in `prometheus_targets.test.sh`: bash_patch2 still needs ≥ 1 product script. |
| KS-1418 flow doc block 18.3 attribution | NOT: a **documentation** attribution with no spelled text and no runner. |
| KS-1308 squash body base not an ancestor | NOT: **process/PR-text**; no repo code. |
| KS-1222 upload screen unreachable | NOT: **decision** ("The owners decide what the route should be"); measure-first. |
| KS-954 billing leading `//` 404 | NOT: **mechanism not determined** ("Reproduce before fixing"); no fix shape. |
| KS-630 wire the status-page XSS probe into preflight | NOT: **decision** ("or decide not to"); preflight is NO-NEW-LEG. |
| KS-581 register-connector alerting/rate limit | NOT: **security surface** (connector re-key); a feature. |
| KS-582 [Decision] bulk re-key approval shape | NOT: **decision**; credential surface. |
| KS-603, KS-604 (BM-2, BM-5) | NOT: **business/document** work, no code. |
| KS-1381 (re-screen, multi-file) | NOT: an auth-named harness (`auth-matrix-smoke.sh`); `smoke-test.sh` is in held `READY_KS-1250`; slot-tooling lane. |
| KS-1413 (re-screen) | NOT: **credential surface** (prints the demo issuer password) and "your call". |
| KS-1417 (re-screen) | NOT: **decision** (delete vs replace with a comment). |
| KS-1343 (re-screen) | NOT: RLS/multi-tenancy docs (security), with no spelled replacement. |
| KS-1197 (re-screen) | NOT: **auth surface** (token-claim coercion). |
| KS-1389 (re-screen) | NOT: **decision** ("asks for your view"). |
| KS-576, KS-583 (re-screen) | NOT: **credential (key-rotation) surface**. |
| KS-709, KS-716 (re-screen) | NOT: Peter's split (systemTest/akto) and security tier. |
| KS-678 (re-screen) | NOT: **decision** ("Calls needed from @PeterD"). |
| KS-1184 | NOT: **decision** ("A design call … Two shapes"); `verification.ts` is a Seat E 10th file. |
| KS-683 | NOT: the fix is Platform-S side and already landed (PS-644); the remaining layers are ops. |
| KS-785 | NOT: **decision** (two candidate shapes "neither chosen") and a credential checker. |
| KS-1163 | NOT: **past the round counter** (the 09-25 ruling comment: "this ticket sits past the local model's counter"). |
| KS-939, KS-940, KS-1085 | NOT: the **launcher** (`Launch_Claude.command`), not repo code. |
| KS-1088 | NOT: **decision** ("Decide whether the runner should enforce isolation"). |
| KS-1338 | NOT: **residue of a capped round** (the counter is exhausted) and test-is-product. |
| KS-1405 | NOT: **decision** ("Whoever picks it up should decide which"). |

Excluded before screening (the commission's exclusion list, measured on the pull):
- **Peter or Stuart assigned (23):** KS-61, 101, 135, 139, 188, 239, 492, 525, 590, 608, 982–985, 1042, 1366, 1367, 1396, 1416, 1428–1431.
- **Live seats' tickets on the board (5):** KS-998, KS-1326 (Seat R 9th); KS-591, KS-1432, KS-1435 (Seat E 10th).
- **Held or just handled (3 on the board):** KS-1250, KS-1274, KS-1438.
- **A `READY_*` exists (9 on the board):** KS-593, 623, 884, 960, 1009, 1186, 1219, 1328, 1355.

The remaining ~200 tickets: the verdicts of the 10-05 widened screen, the 10-06 screen and the 11:20 screen stand.
- **Instrument:** `updatedAt` on this pull.
- **Result:** apart from KS-1438, no ticket was updated after 2026-10-06T14:47Z, and every one of the 10-06 / 10-07 delta tickets carries a verdict in those screens.
- **Their clauses**, as listed in `2026-10-05_spark-screen-widened/SCREEN.md` "The remaining ~200 by clause": security/auth/token/tenant surface, decision/ruling/business, or no runner/live stack/ops.
- **Tickets whose last comment is Peter's or Stuart's** (KS-491, 565, 576, 582, 621, 668, 696, 709, 716, 724, 725, 752, 770, 784, 955, 1102, 1162, 1178, 1357, 1384, 1385, 1387, 1390, 1413, 1421, 1427, 1433, 1434): all already NOT on another clause in those screens, or above.

## Ticket-text errors

- **None found in the tickets read at source.** KS-1410's site lines were measured at `f01c1da` and are still exact at `147ae442074c`: `batch.ts:166/214/262`, `audit-export.ts:196`, `notifications.ts:126/147/176/204/234/290`. Its mcp-server line numbers name the `const message` line of each pair; the `res.status(500)` line is the next line. That is not an error, but a brief writer should know it.
- **One wording note, not an error.** KS-1410 calls the class "no NODE_ENV guard". The precedent fix (`fail500`) adds no `NODE_ENV` guard either: it answers the constant body in every environment and logs the text. The briefs follow the precedent, not a literal `NODE_ENV` branch.

## Collision census

- **Open PRs:** GitHub REST GET on `Secuura/Distributed_Secuura`, ~15:20 AEDT: 22 open PRs, 115 files.
  - None touches `routes/batch.ts`, `routes/audit-export.ts`, `routes/notifications.ts`, or either new test path.
  - **Positive control:** the same census lists #995 (`api-gateway/src/utils/trustHeaders.ts`), #923 (`ks570-proxy-mount-auth.test.ts`), and #649/#575 (`api-gateway/package.json`).
- **Held Spark work:**
  - No brief golden, `READY_*`, `spark/queue.md` or `done.md` row touches `batch.ts` or `notifications.ts`.
  - `READY_KS-745_…_2026-09-15` touched `audit-export.ts`, and it is landed: its KS-745 comments are at the tip's `:138` and `:145`.
  - KS-1410 has no row in `spark/done.md`, `spark/queue.md` or `night/done.md`. Positive control: KS-1435 has 1 row in `spark/done.md`.
- **Lane files:** neither brief touches any Seat R 9th or Seat E 10th file, nor the `Projects Documents/` docs.

## Tooling findings (none edited; Wednesday's call)

1. **code_patch2's A3b grades only the FIRST product's `## Where` sites.** `night/build_input.sh` parses `` `:N` `` bullets against the first product (`build_input2.sh` runs it for product 1). So `audit-export.ts:196` is not an A3b site: the control reported "3 site(s), 2 product file(s)".
   - It is still covered, by A3x (per-file `+` lines byte-identical) and by the A4/A5 audit cells (red without the audit-export hunks, measured).
   - The KS-1278 brief's `file.ts:N` bullets were silently ignored for the same reason.
   - A per-file Where syntax would close this.
2. **Two per-round clones were added** under `spark/cache/work/` (339 MB each, the two controls). Nothing was removed.
3. **`build_input.sh` counted 17 expected `+` lines for notifications against 20 written.** The three empty `+` lines are not counted. This is benign: A3c passed with the golden.

## Follow-ups (not briefed)

- **KS-1410's remaining 18 sites:**
  - `transfer/src/routes/delegations.ts:283`: briefable once Seat E 10th releases `services/transfer`. It needs a one-file code_patch with the same helper.
  - `tenant-provisioning/src/index.ts` ×7: needs an in-process seam first, either a route module or a guarded `listen`.
  - `mcp-server/src/http-server.ts` ×10: needs `app` exported (or the `listen` guarded) before any in-process cell can reach it.
- **The audit-export 502 at `:159`–`:166`** (`Failed to reach security service: ${err.message}`): KS-1410 lists it as a leak that is not counted. It is a one-hunk follow-on once the batch/audit-export brief lands, and it would reuse that brief's helper shape.

## UNMEASURED

- **No model round.** Whether the Spark reproduces either golden was not measured. The controls prove the builder, the checker and the goldens only.
- **No live stack.** Most red rows are planted by a throwing getter on `req.user` / `req.body`. Only R3 (`documents:[null]`) is a real request shape. Which errors reach these catches in production is KS-1410's own UNMEASURED.
- **The winston logger is mocked** in both tests.
- **node_modules** come from the Blockchain checkout's install, not a fresh `npm ci` at `147ae442074c`.
- **eslint** was not run on the new tests.
- **Seven-hunk and six-hunk briefs on the Spark:** whether it copies them as cleanly as KS-1274's eight is what the round itself will measure.
- **Peter-last-comment tickets.** Whether any of those comments is a question was not read for every one; every one fails another clause first.

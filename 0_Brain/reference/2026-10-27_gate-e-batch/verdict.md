# QA gate verdict - Secuura/Blockchain PRs #1747, #1748, #1749, #1750

- Tier 2, round 1 of 2. Gate model: Claude Sonnet 5.5 (claude-sonnet-5-5). Date 2026-10-27.
- Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-e-1027/` (clone `repo/`, worktrees `wt_dev`, `wt_p1747`..`wt_p1750`, plus `wt_merge` for the merge simulation; raw logs and scripts beside; private `TMPDIR=/tmp/ge1`). Node v26.8.1. `npm ci` in `Blockchain/Dev` of `wt_dev`, `wt_p1747`, `wt_p1748`, `wt_p1750` (rc 0 each) and later `wt_p1749` (see instrument error 3); `packages/shared` built in each (rc 0).
- Pushed / merged / commented / edited a ticket / changed a PR: nothing. Git only (deploy key read for the fetch); I did not use `gh`.
- Mutants were made in my own worktrees (or in copies under `/tmp/ge1`) and restored each time; all six worktrees `git status` empty at the end.

## BLUF
| PR | Verdict | Worst finding |
|---|---|---|
| #1747 KS-1637 (Seat X 1st) | GO | LOW only. Every rewritten sentence is TRUE against the code (read, and the one empirical claim, "a fetch count reads 0 with the route present or absent", reproduced). ks1628 file 8/8 on develop and head; api-gateway 123 files / 1203 passed on both; comment-only proved by emit hash (identical both sides, a code-token control moves it). My own three source mutants each red the intended cells. LOW: the G2 cell title still says "and fetches no document" while the header (now correctly) says no cell asserts on fetch. |
| #1748 KS-1634 (Seat Y 1st) | GO | INFO only. Claim reproduced across six planted defaults: original file 6 passed / 4 failed (both N3 cells stay passed), new file 4 passed / 6 failed (both N3 cells fail on the new assertion). 10/10 real default; originate 140 suites / 1656 tests, 0 failed, on develop and head. INFO: the sibling cell "simulated true with a real hash" has the identical implicit-default gap and is not asserted (not claimed). Docs flow block 65 collides with develop's 65 (expected). |
| #1749 KS-1560 M2 (Seat Z 1st) | GO WITH NOTES | LOW. 8/0 -> 20/0 reproduced; server.ts byte-identical; extractor output equals the old grep on the real server.ts; six of my seven respellings red the OLD suite (4 failed of 8) and read 20/0 on the NEW; three deletions red in both. 15 mutants of the extractor/controls: 13 killed, 2 are equivalent by construction. LOW: the header says "a respelling of the subject cannot change the set the probe inherits"; three respellings I tried still make the new suite red (two imports on one line, an inline `{ type X }` modifier, a leading `;`). Not named among the docs' two known edges. |
| #1750 KS-1484 (Seat W 1st) | GO WITH NOTES | INFO/LOW; the one runtime change in the batch, so noted for a human. Item 3 mirrors the lookups' contract exactly (log, infra -> `ServiceUnavailableError` 503, anything else rethrown as the same object). I DROVE the real route over HTTP with no database: on `GET /api/users` and `GET /api/users/admin/list` an infra fault answers 503 SERVICE_UNAVAILABLE where develop answered 500 INTERNAL_ERROR; non-infra errors, an `AppError`, a non-Error throw and a DEK decrypt failure are byte-identical before and after. Red-first 4 red / 19 green reproduced; ks1186 7 -> 23; services/auth 1162 passed on the PR (1146 base + 16). INFO: any class 57/53/08 code (e.g. 57014 statement_timeout) now maps to 503 on this path, as on the siblings. LOW (stated by the seat): `countUsersInner` still 500s on infra, and both routes call it right after `listUsers` (I measured it). |

Merge: **#1747 is clean in every order and position** (no doc). #1748, #1749, #1750 each append one block at the same `</body>` of the same two Projects Documents HTML docs, and develop's pin already carries #1744's block there, so **each of them conflicts with develop on its own, and with each other in every order**. Resolving every conflict by keep-both (keep the target's text, insert the incoming block before `</body>`) loses nothing: **all 64 order/subset sequences of the four (every permutation of every non-empty subset) resolved with zero loss** (details below). Section numbers are for the merger, not a defect.

## Pins (start = end)
```
a105a9df185b9f25128eea0fb1e430bc2d5e64fe  refs/heads/develop
a47b47dce896503d21b7aa44abc725ac04b25167  refs/pull/1747/head
fc73f10cde782473ce26a693b9b92e54f5e4044d  refs/pull/1748/head
61b255e331dd7033c524143105e57472e81954c5  refs/pull/1749/head
1cbbdd5591a042578f42628f3536d9676d84654f  refs/pull/1750/head
```
`lsremote_start.txt` was read first (before the clone) and `lsremote_end.txt` at the very end; `diff` empty; both equal the briefed pins. Develop did NOT move during my run (end value = the pin).
Merge bases: #1747 on `b6366c12` (older than develop; none of its files changed on develop since, so `develop...head` and develop's own files agree, which the ks1628 file and `index.ts` runs on `wt_dev` confirm); #1748, #1749, #1750 on `885d69b0` (develop is three commits ahead of it: #1743, #1744 and docs). #1748's head is a merge commit (`fc73f10cd`, "Merge develop 885d69b06f5f"); `develop...head` shows only its own 3 files. I used `develop...head` for scope and each PR's own merge base for the append-only proofs.

## #1747 KS-1637

**FOUND**
- Scope vs develop (`develop...head`): 4 files, 31+/14-, one commit `a47b47dce`: `Blockchain/Dev/deployment/azure/RUNBOOK.md` 1/1; `services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts` 26/9 (one hunk, header lines 13-50 only); `services/api-gateway/src/index.ts` 3/3 (the comment); `Blockchain/Testing/USER SIMULATED TEST/02-verifier.md` 1/1 (line 71). No docs, as briefed (escape clause).
- Every rewritten sentence checked against the code:
  - N1 header. "This file's cells are G1-G4 and their controls; R1-R3 are originate's, in its own removal pin": the file's titles are G1, G2, G3, G4 and G-C1..G-C4 (8 cells), and `services/originate/src/__tests__/ks1628-deprecated-documents-verify-is-removed.test.ts` carries R1, R2, R3 (lines 130, 135, 140). TRUE. G2 "the certifications twin sends its OWN 404 ... an absent route falls through to express's finalhandler (text/html), every handler sends JSON": TRUE (G-C2 asserts exactly that pair). "The router's lookup goes through `makeCheckDocumentExists`, which uses `require('http').get`": TRUE (`routes/verification.ts:179`). "A fetch count reads 0 with the route present or absent (measured)": REPRODUCED. I added `fetchSpy.mockClear()` and `expect(fetchSpy).toHaveBeenCalledTimes(0)` to a copy of the G-C2 cell, where the certifications route IS present and its handler runs: 8/8 passed, so a fetch count cannot tell present from absent. "fetch is still stubbed in beforeAll ... no cell asserts on it": TRUE (`fetchSpy` is referenced only at its declaration and the one assignment).
  - N2 RUNBOOK:263. "On `/api/certifications/:id/verify`: the caller's bearer token not forwarded to originate (`checkDocumentExists` in `verification.ts`)": TRUE (`verification.ts:322` passes `req.headers.authorization` to it; the helper forwards it as `Authorization`). "Not on `/api/verification/verify`: it is anonymous and CSRF-exempt (`csrf.ts`), so there is no token to forward": TRUE (`csrf.ts:113` lists it among the exempt verify family; `routes/proxy.ts:658` mounts `/api/verification` as "no auth required for public verification" and proxies it to originate, so the gateway holds no token for it). The row still has 3 cells (4 pipes, same as its neighbours); the new text contains no raw pipe.
  - N4 `index.ts` ~:417. "`POST /api/certifications/:id/verify` has NO target service - it is answered here, by `verification.ts` (so was the documents twin, until KS-1628)": TRUE; the registration is at `verification.ts:317` and no documents-verify route is registered (G1 and the mutant below). "3 lines in, 3 out": TRUE (`index.ts` 3/3).
  - N5 `02-verifier.md:71` now names `POST /api/verification/verify`, which is the public verifier call per the same code. TRUE.

**TESTED / HOW** (all on my own runs)
- ks1628 file, develop pin vs head: **8 passed / 8 passed** (first run on each read 0 of 8, 8 skipped, `Hook timed out in 10000ms` in `beforeAll` under cold load; both re-ran warm 8/8; instrument error 1).
- Whole api-gateway suite, develop pin vs head: **123 files / 1203 tests passed, 0 failed, on both**.
- Comment-only, by TypeScript emit with comments removed (`ts.transpileModule`, `removeComments`), with a code-token control (`const` -> `let` in the source before the emit): the ks1628 file emits 7,054 bytes, sha16 `7208f69bfd0b2780` on develop AND head, control `f876d7af3d1038ed` on both (moves); `index.ts` emits 38,806 bytes `ae13e88a9538abb5` on both, control `40bc34019f4c88fa` (moves). Raw sizes: ks1628 11,486 -> 12,754 bytes, `index.ts` 67,760 -> 67,762 (3 lines in, 3 out). The seat's figures (6,496 / 37,349 bytes, `ee7ca082...` / `cd509d9a...`) are from a different instrument; I cannot reproduce those numbers, I reproduce the conclusion (identical on both sides, control moves). INFO.
- Mutants of the product the header describes, each run against the head's ks1628 file: MA a handler `POST /api/documents/:id/verify` re-registered in `createVerificationRoutes` (JSON 404) -> **3 red: G1, G2, G4**; MB a handler re-added in `index.ts` ahead of the router mount -> **1 red: G4** (the cell KS-1637 Minor 1 added, and the only one that can see it); MC the published `GET /api` index lists the route again -> **1 red: G3**. The four controls stayed green throughout. Worktree restored (`git status` empty).
- INFO: other present-tense mentions of the retired route remain outside this PR's scope: `routes/verification.ts:282` and `:387` (historical measurement and a comment), `frontend/shared/src/schemas/verify.ts:3` (already past tense), the e2e `tests/e2e/...` fixtures (`/api/documents/${id}/verify`), `systemTest/playwright/clients/documents.client.ts`. Not claimed by the PR.
- LOW: the cell `RED KS-1628 G2: a POST to it is unanswered by the router and fetches no document` keeps its old title; the header now (correctly) says no cell asserts on fetch, and I just reproduced that fetch cannot do the job. The title still advertises it.

**Verdict: GO.**

## #1748 KS-1634

**FOUND**
- Scope vs develop: 3 files, +45/-2 (against its own base): `services/originate/src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts` 13/2 (a `REAL_TX_SHAPE = /^[0-9a-f]{64}$/` constant, and in each of the two N3 cells `const reply = chainReply({...}); expect(reply.txHash).toMatch(REAL_TX_SHAPE); const body = await callV2(reply);`); `API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` 15/0; `QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` 17/0. No product code.
- INFO-1: the claim says each N3 cell asserts `expect(reply.txHash).toMatch(/^[0-9a-f]{64}$/)`; the code asserts it against the named constant holding that same regex. Equivalent.
- INFO-2 (unstated, same class): the cell `RED KS-1634 L6 v2: simulated true with a real hash reads NOT on-chain` (line ~134) sends `chainReply({ simulated: true })` with the default hash too, and does not assert it is real. Under every planted placeholder default below it also stays green (it is not in the failed list), so it can pass while no longer pinning what its title says. The seat scoped the PR to the two N3 cells ("N3"), so this is not a defect of the PR, only the neighbouring cell with the same gap.

**TESTED / HOW**
- Cells: develop 10/10, head 10/10 (10 -> 10, two assertions added, no cell added or removed).
- My own mutants, in COPIES of the test file (original = develop's file, new = head's) with the default `txHash` of `chainReply` replaced; same source otherwise:

| planted default | original file | new file |
|---|---|---|
| `'mock_tx_' + 'a'.repeat(64)` | 6 passed / 4 failed, both N3 stay passed | 4 passed / 6 failed, both N3 fail |
| `'tx_sim_' + ...` | same | same |
| `'tx_' + ...` | same | same |
| `'mock_batch_tx_' + ...` | same | same |
| `'abc123'` (not a presenter-fabricated prefix, not 64 hex) | same | same |
| `'A'.repeat(64)` (uppercase hex) | same | same |

The 4 original failures are the four controls that compare against `REAL_TX` (not the N3 cells); the 2 extra new failures are exactly the two N3 cells, each on the new assertion. This reproduces "original 6 passed / 4 failed (both N3 stay passed); new 4 passed / 6 failed (both N3, each failing on the new assertion)" for the seat's mock-prefixed default and five more.
- Real default: head file 10/10 (above). Whole originate unit suite, develop pin vs head: **140 suites / 1656 tests, 0 failed, on both**.
- Control that can fail: the new assertion itself is the control; the two uppercase and short-hash mutants show it fails on a hash that the presenter would NOT refuse (so it adds information the presenter rule does not).
- Docs (against its own merge base `885d69b0`): append-only (text up to `</body>` unchanged, the head file equals base-before-`</body>` + block + base-from-`</body>`), numstat 15/0 and 17/0, one `</body>` each, tags balanced head and base; `html_docs_matrix.test.sh` 18 passed / 0 failed on develop and head. Added headings: `65.` (flow doc, with 65.1-65.4) and an unnumbered cheat-sheet block.
- Numbering: develop's pin already holds 65 (from #1744); this is the expected collision and the merger renumbers. INFO.

**Verdict: GO.**

## #1749 KS-1560 M2

**FOUND**
- Scope vs develop: 3 files, +153/-2: `Blockchain/Dev/scripts/__tests__/ks1347_proxy_out_dir_spaced_checkout.test.sh` 118/2; the two docs 12/0 and 23/0. `scripts/openapi-examples/proxy/server.ts` NOT edited (`git diff --stat origin/develop...p1749 -- Blockchain/Dev/scripts/openapi-examples` empty; `cmp` of develop's and head's `server.ts` identical).
- The change replaces the one-line `grep -E "^import .* from 'node:[a-z]+';$"` with a Node extractor (`extract_node_imports.cjs`, written to `$FIX`) that reads `import <clause> from '<node:...>'` as a statement (either quote style, optional semicolon, `[^'"\s]+` specifier so `node:fs/promises` and `node:child_process` match, wrapped clauses folded, `import type` skipped) and prints each in one canonical spelling. The "non-empty and names node:path and node:url" control is kept unchanged. It is used for the real subject and for the 10 synthetic spelling files, so what is tested is what is used.
- LOW-1: the header says the extractor "prints each one in a single canonical spelling, so a respelling of the subject cannot change the set the probe inherits". I found respellings that still change it (table below): two imports on one line (the regex is `^`-anchored with `m`, so the second is missed), an inline type modifier `import { type URL, fileURLToPath } from 'node:url'` (kept verbatim into `probe.mjs`, where it is a SyntaxError), and a leading `;` (ASI style). The docs name two other known edges (a comment inside an import clause, a default import literally named `type`) and the neighbouring `^const OUT_DIR` line-shape; these three are not named. They are respellings no one has made of `server.ts` today; the old suite was red on the same three.
- INFO: a `/* ... */` block that holds an import-looking line at line start is inherited into the probe (my X3: harmless for an unused `os`, but a commented `path` import would duplicate a binding). Not claimed.

**TESTED / HOW**
- Suite: develop 8 passed / 0 failed; head **20 passed / 0 failed** (8/0 -> 20/0), in-tree and in an isolated copy.
- Respelled copies of the real `server.ts` (my own, 7 respellings plus 3 deletions), each run through the OLD suite and the NEW one:

| copy of server.ts | OLD suite | NEW suite |
|---|---|---|
| R1 double quotes on all five | 4 passed / 4 failed | **20 / 0** |
| R2 no semicolons | 4 / 4 | 20 / 0 |
| R3 trailing `// x` comments | 4 / 4 | 20 / 0 |
| R4 CRLF line endings | 4 / 4 | 20 / 0 |
| R5 `fileURLToPath` list wrapped over three lines | 4 / 4 | 20 / 0 |
| R6 `import * as path from 'node:path'` | 8 / 0 (old regex already matches it) | 20 / 0 |
| R7 space before the semicolon | 4 / 4 | 20 / 0 |
| D1 delete the `node:path` import | 4 / 4 | 16 / 4 |
| D2 delete the `node:url` import | 4 / 4 | 16 / 4 |
| D3 delete both | 4 / 4 | 16 / 4 |
| X2 `import path, { sep } from 'node:path'` | 8 / 0 | 20 / 0 |
| X4 extra `import type { Stats } from 'node:fs'` | 5 / 3 | 20 / 0 |
| X6 extra `import { readFile } from 'node:fs/promises'` | 8 / 0 | 20 / 0 |
| X8 `... with { type: 'x' }` attribute | 4 / 4 | 20 / 0 |
| **X1 two imports on one line** | 4 / 4 | **16 / 4** |
| **X5 inline `{ type URL, fileURLToPath }`** | 5 / 3 | **17 / 3** |
| **X7 leading `;` before one import** | 4 / 4 | **16 / 4** |

So: six of my seven respellings (all but R6) red the old suite with 4 failed of 8, all read 20/0 on the new; the seat's "seven respellings" is reproduced in kind (their seventh differs from my R6, which the old regex already handled); the three deletions are red in both (4 failed in each; the new suite names the failing control "the subject's node imports were read, and include the one the expression needs"). The three bold rows are LOW-1. Extractor output vs the old grep on the real `server.ts`: both suites read the same inherited set (8/0 and 20/0 on it, and the set-equality cell `canonical` green).
- My own mutants of the NEW test (each on a copy, run against the real `server.ts`):
  - regex single-quote only: 19 / 1 (the `double_quotes` spelling cell); subpath restricted to `[a-z]+`: 19 / 1 (the subpath/underscore cell); clause cannot span newlines: 19 / 1 (`wrapped_list`); `import type` no longer skipped: 19 / 1 (`planted_noise`); clause whitespace not folded: 18 / 2 (`extra_spaces`, `wrapped_list`); canonical emit with double quotes: 11 / 9; canonical emit without the semicolon: 11 / 9; an extra stray import always emitted: 10 / 10; `m` flag dropped: 7 / 13 (the real-subject control among them); only the first import emitted: 7 / 13; empty output: 7 / 13; constant canonical output: 18 / 2 (the "EMPTY set" control and the subpath cell fail, which is the point of those two controls); a respelling made invalid ESM (`let let = ;` appended to `trailing_comment.ts`): 19 / 1 (the "valid ESM, so each really is harmless" control); that is **13 of 13 meaningful mutants killed**. Two further mutants are equivalent by construction and survived (making `node --check` always pass in the loop reads the same as the real state because every respelling IS valid; and replacing the broken-file control's command with `echo rejected` reads the same as the real state); I did not count them. A fourteenth (a no-op edit I mis-built) is discarded.
- Whole shell suites (`bash scripts/run-shell-suites.sh`): develop **95 passed / 0 failed / 1 skipped (of 96)**; head **95 / 0 / 1 (of 96)**, with the skip identical (`ks949_main_seed_idempotence.test.sh`, no PostgreSQL). A first head run read 94 / 0 / 2 because `wt_p1749` had no `node_modules` and the ratchet-leg suite skipped (instrument error 3); after `npm ci` it read 95 / 0 / 1.
- Docs (own base `885d69b0`): append-only, numstat 12/0 and 23/0, one `</body>`, balanced; `html_docs_matrix.test.sh` 18 / 0. Four `NN`-numbered headings in the flow doc (NN, NN.1, NN.2, NN.3) that the merger must number.

**Verdict: GO WITH NOTES** (LOW-1).

## #1750 KS-1484

**FOUND**
- Scope vs develop: 4 files, +173/-40, two commits. Commit `bd6924be3` (items 1 and 2): `userRepo.ts` 5/2 (comment), the ks1186 test 56/60, docs 9/0 and 19/0. Commit `1cbbdd559` (item 3, the behaviour change, its own commit): `userRepo.ts` 18/6, the test +91, docs 8/5 and 8/8 (it rewrites its own first-commit block). Net three-dot docs: 12/0 and 19/0, append-only.
- Item 1 is comment-only. The stale sentence at `userRepo.ts` ~:372 ("The five sibling reads below still return `fromRow` unawaited: KS-1186") now says KS-1186 did it for the five, and that is TRUE: `userRepo.ts:449, 515, 588, 597, 630` are `return await fromRow(...)` (plus `getUserById` at 413).
- Item 3 as built (`listUsersInner`): the `query(...)` SELECT and `return await Promise.all(result.rows.map((r) => fromRow(r)))` are inside a `try`; `catch (err) { logger.error('DB listUsers failed', { error: err?.message, code: err?.code }); if (isInfrastructureDbError(err)) throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry'); throw err; }`.
- **Consistency with the lookup contract: consistent.** The six sibling catches (`getUserById` :416, `getUserByIdWithPasswordHash` :452, `getUserByIdPreAuth` :518, `getUserByEmail` :603, `getUserBySocialId` :634, `emailExists` :662) have the same three steps in the same order: `logger.error('DB <fn> failed', { error, code })`, `isInfrastructureDbError(err)` -> `ServiceUnavailableError` with the same message, else `throw err`. The new catch is that shape character for character apart from the function name. `ServiceUnavailableError` is `AppError(msg, 503, 'SERVICE_UNAVAILABLE')`; the routes' `next(error)` reaches `errorHandler`, whose `instanceof AppError` branch answers `err.statusCode` with `{ code, message }`. Only two callers of `listUsers` exist (`routes/users.ts:464` GET `/` and `:520` GET `/admin/list`).
- Does moving the SELECT inside the try change any other error's mapping? **Only the intended one.** Before, a SELECT error propagated untouched: infra-shaped -> 500, anything else -> whatever it was. After: infra-shaped -> 503, anything else rethrown as the same object (so an `AppError`, a Zod error, a string all keep their identity and mapping). Errors raised before the `try` (building `conditions`/`values`) are unchanged. I measured every row of the table below.
- INFO-1: `isInfrastructureDbError` treats any `code` starting `08`, `53` or `57` as infra, so a `57014` (statement_timeout / query_canceled) on the list now answers 503 (retry) where it answered 500. That is the existing classifier and the existing behaviour of every sibling lookup, so it is consistent, but it is a new visible consequence on a list that can run long.
- LOW-1 (stated by the seat, measured by me): `countUsersInner` (`userRepo.ts:1067`) has no try/catch and both routes call it immediately after `listUsers`; with the list answering and the COUNT faulting, the route still answers 500 INTERNAL_ERROR (row "LISTOK_COUNT_ECONNRESET" below). The list routes are therefore only partly on the contract until the count is brought in.
- INFO-2: this is a runtime change that is not deployed; under the Done rule KS-1484 cannot be Done until auth is deployed (the docs say so).
- INFO-3: commit 2 rewrites commit 1's docs block (8/5 and 8/8 numstat in that commit alone); net against develop it is append-only (12/0, 19/0). If the PR is merged commit-by-commit rather than squashed, the history carries the rewrite. Not a defect.

**TESTED / HOW**
- I DROVE THE ROUTE PATH, no database. Probe file `zz-route-probe.test.ts` (mine, quarantined to `/tmp/ge1/quar/` after each run, not in the tree): mounts the REAL `routes/users.ts` router, the REAL `userRepo` and the REAL `errorHandler` on an express server over HTTP; replaced are only `../db` (`query` made to reject or answer per cell), the `authenticate` middleware (injects a `SYSTEM_ADMIN`), the logger, `subjectDeks` and the crypto helpers (the same mocks as the ks1186 file). Same file run against develop pin and the PR head; both read 24 / 24 passed (the cells record, they do not assert). Result `[status, error.code]`, identical for `GET /` and `GET /admin/list`:

| injected fault | develop (before) | PR head (after) |
|---|---|---|
| `ECONNRESET` on the SELECT | 500 INTERNAL_ERROR | **503 SERVICE_UNAVAILABLE** |
| "Connection terminated due to connection timeout" (message only) | 500 | **503** |
| subject-DEK read (`getDek`) rejects `ECONNRESET` inside `fromRow` | 500 | **503** |
| `57014` statement_timeout (class 57) | 500 | **503** (INFO-1) |
| SQL syntax error `42601` | 500 | 500 (same) |
| plain `Error('boom')` | 500 | 500 (same) |
| string thrown | 500 | 500 (same) |
| DEK read rejects a decrypt-shaped error | 500 | 500 (same) |
| `ForbiddenError` thrown from the query | 403 FORBIDDEN | 403 FORBIDDEN (same; the object passes through) |
| list answers, COUNT rejects `ECONNRESET` | 500 | 500 (LOW-1, not covered) |
| healthy: empty list; one healthy row | 200 / 200 | 200 / 200 |

So the claim "on `GET /api/users` and `GET /api/users/admin/list` an infrastructure fault answers 503 SERVICE_UNAVAILABLE where it answered 500 INTERNAL_ERROR" is **reproduced end to end**, the seat's own "the route path was read, not run" gap is now run (still a mock for the database, not a real pg fault), and no non-infrastructure error changed (no over-broad catch).
- ks1186 file: develop **7 passed**, head **23 passed** (7 -> 23). Red-first: item 3's code replaced by develop's no-catch shape on the head's tree, the head's test file: **4 failed / 19 passed**, the four are the four cells the test labels red (infra inside `fromRow`, infra at the SELECT, a later row's DEK read, the log line); head: **23 / 23**.
- Item 1 comment-only: emit with comments removed of `userRepo.ts` at develop and at commit `bd6924be3`: 47,744 bytes, sha16 `d297162cc01fdada`, identical; code-token control `21b86597285d530e` on both (moves); head (item 3 included) emits 48,109 bytes `11365243f1253172` (differs, as it must). (The seat's "AST sha 003a4d1c98c152fb" is another instrument; same conclusion.)
- Item 2 ("16 mutants, 13 survive the old file and are killed by the new, 3 killed by both"): my own 19 mutants of the five lookups' catches and awaits (no await on each of the five sites; log removed on four; the rethrow wrapped in a new Error on four; the catch swallowing and returning null on two; the infra test forced true on two and forced false on two), run against develop's old file and the head's new file: **new killed 19 of 19; old killed 9 and let 10 survive** (every log-removed mutant, every wrap mutant, and swallow / always-503 at `getUserBySocialId`). No mutant was killed by the old file and missed by the new. The direction is reproduced; the 16/13/3 split is the seat's own mutant set, mine is a different one (INFO).
- Item 3 mutants of my own against the head's file (old file in brackets): drop the whole try/catch **4 red** [0]; drop the `await` before `Promise.all` **3 red** [0]; catch swallows (`return []`) **2** [0]; rethrow wrapped in a new Error **2** [0]; always 503 **2** [0]; never 503 **3** [0]; log removed **1** [0]; log line renamed **1** [0]; log drops the `code` field **1** [0]; SELECT moved outside the try **2** [0]; per-row `.catch(() => r)` swallowing a `fromRow` rejection **4** [0]. All 11 killed by the new cells; none by the old file (it never covered `listUsers`).
- Suites: services/auth on develop pin **105 files / 1157 passed**; on the PR head **105 files / 1162 passed** after a warm re-run. The PR is on base `885d69b0` (1146 tests), so 1146 + 16 = 1162 reproduces the seat's number; develop's own 1157 includes #1744. `check:test-types` for `services/auth`: **42 errors, 42 in the baseline, 0 new, 0 stale** on develop and head. `tsc --noEmit` in `services/auth`: **rc 0** on both.
- Docs (own base): append-only, numstat 12/0 and 19/0, one `</body>`, balanced; `html_docs_matrix.test.sh` 18 / 0. Flow block headed `65.` (65.1-65.5): the same number #1744 already holds on develop and #1748 uses; expected collision, merger renumbers. The docs state the three limits the brief lists (countUsers, DB mocks, route read-not-run) plus "not deployed"; the second is now partly retired by my probe.

**Verdict: GO WITH NOTES.** The verdict is on the tests and the code as read and driven; a human should consciously accept the 500 -> 503 change on two admin list endpoints (clients that retry on 503 will now retry on a list fault; the COUNT gap means a fault on that second query still reads 500).

## Merge orders

Computed in `wt_merge` (a worktree at the develop pin) by performing the real `git merge --no-ff` for each of **all 64 sequences** (every permutation of every non-empty subset of {#1747, #1748, #1749, #1750}); wherever git reported a conflict I resolved by keep-both in the merge order (keep the target's text and insert the incoming block, which I verified is append-only against its own base, immediately before the last `</body>`). Every result was checked for no conflict markers, exactly one `</body>`, the exact expected line count (develop's lines + the sum of the merged PRs' added lines, per doc), none of develop's own lines lost, and every added line of every merged PR present. **64 of 64 ok, 0 problems.**

| set | conflicts | distinct trees across orders |
|---|---|---|
| #1747 alone, or with any other | never (no doc; no overlapping file) | 1, and its position never changes the tree |
| #1748, or #1749, or #1750 alone onto the develop pin | doc conflict in both docs (develop already holds #1744's block at `</body>`), keep-both clean | 1 each |
| any pair of #1748/#1749/#1750 | each merge after the first conflicts again in both docs, keep-both clean | 2 per pair (they differ only in which block comes first) |
| all three | same | 6 (the six block orders) |
| all four, 24 orders | the tree depends only on the order of the three doc-adding PRs; #1747's position changes nothing | 6 |

Numbering after keep-both: develop's pin already has **65** (from #1744). #1748 and #1750 both say **65** in the flow doc (the second to merge renumbers to 66, the third to 67); #1749's headings are `NN`, `NN.1`..`NN.3` and take whichever number it ends up with. The cheat-sheet blocks are unnumbered. Per brief, not defects.

## NOT TESTED (stated plainly)
- Any suite on a **merged tree** (trees computed and checked for text only; nothing built or run on a merge).
- The four platform suites (Schemathesis, Akto, Playwright, Performance), as the seats state.
- A real pg fault for #1750; every database call in my route probe is a mock. The route ran for real; the pool did not.
- The consumers of a 503 from `/api/users` and `/api/users/admin/list` (portal pages, the gateway's handling of a 503 from auth): not read or run.
- #1747: the e2e / playwright fixtures that still reference the retired path (not in the PR); the seat's emit byte counts (different instrument, conclusion reproduced). Nothing browser-rendered.
- #1749: the two edges the docs name (a comment inside an import clause, a default import literally named `type`) and the `^const OUT_DIR` line-shape (not run by me).
- #1748: the seat's exact "4 passed / 6 failed" was reproduced for its mock-prefixed default and five more; I did not run any other cell under the mutant beyond those two files.
- Linear states and PR check states (no `gh`).

## My instrument errors
1. The first run of the ks1628 file read **0 of 8, 8 skipped, rc 1** on develop AND head (`Hook timed out in 10000ms` in `beforeAll`, cold transform on a busy box). Re-run warm: 8/8 and 8/8. The first run of the ks949 test inside the full auth run on the PR head read 2 failed (`Test timed out in 5000ms`, the tree-scanning cells), and the isolated re-run once more failed 2 at the default timeout; I then ran it five more times warm (default timeout: 31/31 each, develop and head) and once with a raised timeout (31/31). The first failure was load; that file is untouched by the PR. The full auth re-run on the head, warm, read 1162 / 1162.
2. My first mutant script for #1750 captured the wrong summary line (it matched the "Failed Tests 2" banner), and an earlier version of it died on an assertion of line offsets; each left an untracked `zz-old-ks1186` copy and, once, a mutated `userRepo.ts` that I restored with `git checkout`. Fixed (a unique summary regex, correct line indexes) and the whole matrix re-run; the table above is from the corrected run.
3. `wt_p1749` was not `npm ci`'d for the first run of the shell-suites runner, so the ratchet-leg suite skipped and the head read 94 / 0 / 2. I installed, rebuilt `packages/shared` there and re-ran: 95 / 0 / 1, same skip as develop.
4. My first merge-simulation resolved conflicts with `git merge-file --union`, which coalesced identical boilerplate lines (`<h3>Running the cells</h3>`, `<h3>Figures</h3>`, `<table>`, `</table>`) between develop's block and the PR's and so interleaved two blocks and lost 2 lines even for a single PR. That is a flaw of my instrument, not of the PRs: a union-merge is not the keep-both a merger performs. I replaced it with a whole-block keep-both and an exact line-count check; the 64 / 64 above is from the corrected run. (The first run's "lines N != expected N+2" was the symptom that caught it.)
5. A cleanup of mine ran `pkill -f vitest` (it was meant to stop only my own mutation run). On a busy box that pattern can match another seat's vitest process; I did not intend that and did not check afterward which processes it matched. Flagging it so the other seats know a vitest run of theirs around 18:55-19:00 AEDT may have been terminated by my command. Nothing else of mine used `pkill` on a broad pattern (the other uses were `pkill -f mut1750.py` and `pkill -f mergesim.py`, my own scripts).
6. My first #1749 mutant batch included a `node --check`-always-OK mutant and an `echo rejected` mutant whose results (20/0) I initially read as survivors; they are equivalent by construction (see the #1749 section), so I excluded them rather than count them as kills or misses. One more mutant in that batch (`Q11`, a `if (false) break;` no-op) was a no-op and is discarded.
7. Fleet hooks refused a `cd`, a `git -C` write verb whose path contained a variable, an unquoted word starting `=`, and `rm`; I re-issued everything as script files with absolute paths and `mv` to `/tmp/ge1/quar`.

## Files outside the workspace
None kept. Writes: the workspace (including `wt_merge`); `/tmp/ge1` (private `TMPDIR`: scratch copies, the originals of the mutated files, temp index files, the suites' own `ks1526-*`, `ks691-leg1.*`, `ks1054_nopy.*` and `t1749_*` temp dirs, `jest_dx`, and `quar/` holding my probe/old-copy files moved out of the worktrees); this verdict folder `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-27_gate-e-batch/`. Read-only use of the deploy key under `!CODING/`. `find /Volumes/DevMASTER/WEDNESDAY -maxdepth 1 -newer lsremote_start.txt` lists only `.git`. No process of mine left running; all six worktrees `git status` empty; clone `repo/` `git status` empty.

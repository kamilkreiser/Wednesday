GO WITH NOTES

# Gate 210: PR 2020, KS-1534 (b), head `ae8e8c78f91f75568706fac14ac382d140f7ad71`, tier 1, round 1

## BLUF
Head conforms to Kam's card (`secuura-ks1534-allow-list-array-of-non-strings-1105` = a, "Refuse in both reads with one shared message (fail closed)"). On the real routers, every stored array holding a non-string answers 403 FORBIDDEN with the one constant on both routes, and no such create reaches enforcement. On base I reproduced the reason for the ruling: mixed lists admit an SSD_DOCUMENT create (201, enforcement reached). Table: 115 of 115 route-cells as expected. Suites match the seat's figures exactly. One Minor test gap (a surviving mutant), no product defect. This GO is about the SHA above only; it expires if the head moves.

## Head readings (ls-remote via the shared checkout)
| time (Z) | refs/pull/2020/head + branch `feature/ks-1534-ks-1232-gate-follow-ups-share-the-allow-list-predicate-b` | develop |
|---|---|---|
| 23:24:00 (drafter) | `ae8e8c78f91f` | `1b1b65c7415f` |
| 23:37:47 (mid) | `ae8e8c78f91f` | `1b1b65c7415f` |
| 23:41:34 (end) | `ae8e8c78f91f` | `1b1b65c7415f` |

## Findings

**F-1, Minor (test gap; the product is correct). A predicate that ignores middle elements survives all 29 cells.** Evidence class: MEASURED AT RUNTIME.
- Where: `services/api-gateway/src/__tests__/ks1534-an-allow-list-of-non-strings-is-refused-by-both-reads.test.ts:51-63`. No fixture in `NON_STRING_LISTS` is longer than 2, and the R5 verdict list uses the same fixtures.
- Mutant O3: `return list.length > 0 && (typeof list[0] !== 'string' || typeof list[list.length - 1] !== 'string');`. tsc 0 errors. Red cells across the ks1534 pair + ks1232 + ks1531: none.
- What it admits, on the real routes, stored `['SSD_DOCUMENT',1,'X']`: under O3, info 200 echoing the list and create 201 with enforcement reached. That is the same class of mixed-list admission the ruling closes.
- On the unmutated head the same row is 403 with the constant on both routes, enforcement 0. So nothing is wrong today; a later rewrite of the predicate could reopen it silently.
- Fix-shape (owner authors): add one fixture of length 3 or more with the non-string in a middle position. The new shape flows into R1-R5.
- Evidence: `evidence/q4_mutants.txt`, `evidence/q4_mutants2.txt`, `evidence/q4_table_head.json`, `evidence/q4_table_O3.json`.

**N-1, Note. An empty-string element is admitted as a string, and no cell pins that decision.** Evidence class: MEASURED AT RUNTIME.
- `''` is a string, so "contains non-strings" does not reach it literally, and the head does not refuse it. The write side agrees: `routes/admin.ts:1174` tests `typeof t === 'string'` on each element.
- Head and base are identical here. `['']`: info 200 echoing `[""]`, every create 403 "not permitted to register". `['SSD_DOCUMENT','']`: info echoes it, SSD_DOCUMENT create 201.
- Mutant O4 (counting `''` as a non-string) survives, as predicted. The behaviour is defensible but unpinned. Whether to pin it is the owner's call; no ruling covers it.
- A bare `''` (not in an array) keeps the older refusal text on both routes.

**N-2, Note against the brief, not the seat.** `wed_brief_extract_k16.txt` says "`null`, an object and a string ... must stay on the existing non-array refusal". On base, `null` is not refused: it means no restriction on both routes (the guard excludes null; measured 200 `[]` / 201). The head keeps that, cell C1 pins it, and the commission's Q3 expects it. An object and a string do stay on the older refusal. The head is right; that brief line is wrong about `null`. The READY states null's behaviour but does not flag that it differs from the brief's wording.

**N-3, Note, not against this PR. Published-contract gap on `POST /api/documents`.** Evidence class: READ ONLY for the spec, MEASURED AT RUNTIME for the 403.
- Neither base nor head names allow-list refusals in that operation's description or 403 text. Its 403 text does say the list is "NOT exhaustive — always read `error.code` and `error.message`", which softens the gap.
- A connector integrating from the spec alone cannot learn this 403 from the POST operation. The seat states this; confirmed. See `evidence/q7_ops.txt`.

**N-4, Note. Two advisories, not one.** `docs-fragments.mjs check` prints a cheat ADVISORY at line 6235 and also a flow ADVISORY at line 6249. Both are pre-existing: the ADVISORY lines are sha256-equal on base and head. The READY text on file does not mention either; the commission names only the cheat one. See `evidence/q8_docs_base.txt`, `evidence/q8_docs_head.txt`.

**N-5, Note for the merge seat (not measured here, carried from the READY).** PR 2020 is attached to both KS-1534 and KS-1232, so a merge may walk both tickets. No Linear read by this gate.

## Answers by question

**Q1 Scope: PASS.** One commit, parent is `85881fde5a48`, exactly the nine paths, +438/-5 (`git diff --numstat`).
- `routes/verification.ts`: +8/-0, two hunks. The import goes after `:19`, the guard after base `:873`. No other changed line, and neither hunk touches the `try`/`catch` region.
- `services/health.ts`: +8/-0, its import plus the guard after the non-array guard. Nothing else.
- Evidence: `evidence/q1_hunks.diff`.

**Q2 Conformance by reading: PASS.** Lines at the head:
- (a) `connectorAllowList.ts:19-24`: `for (let i = 0; i < list.length; i += 1) { if (typeof list[i] !== 'string') return true; } return false;`. It is an index walk, so a hole reads as undefined and counts. `undefined`, `null`, numbers, booleans, objects, nested arrays and String objects all return true. `''` returns false (see N-1).
- (b) Both call sites, once each, straight after the non-array guard, `health.ts:121` and `verification.ts:878`: `if (Array.isArray(rawAllowedTypes) && allowListHoldsANonString(rawAllowedTypes)) {` then `res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: CONNECTOR_ALLOW_LIST_NOT_ALL_STRINGS_MESSAGE } }); return;`.
- (c) Unchanged lines: `verification.ts:882` `const allowedTypes = (rawAllowedTypes || []) as string[];` and `health.ts:130` `allowedDocumentTypes: rawAllowedTypes || [],`.
- (d) The info reader still echoes a list of strings (measured in Q3).
- Message copies: case-insensitive grep for `not a list of strings` finds the constant's own definition at `connectorAllowList.ts:12` (the positive control) and no other copy of the message in product code. The only other product-code hits are the two spec description sentences at `api-gateway.openapi.ts:935` and `:960`, which are prose rather than the refusal text. Test files hold their own expected text deliberately. Evidence: `evidence/q2_grep.txt`.
- Envelope and status: the seat's 403 FORBIDDEN and `{success:false,error:{code,message}}` match the adjacent guard and the info operation's published 403. No Kam ruling names them; they are consistent. The published `allowedDocumentTypes: array of string` is now true of the handler.

**Q3 Behaviour table: PASS, 115 of 115 route-cells, 0 failing.**
- Method: 23 stored values x 5 route-cells (info, create naming SSD_DOCUMENT, create naming INVOICE, untyped create, create via the `type` key), on base and head. That is the commission's 17 values (undefined measured both as an absent key and as an explicit key, so 18 rows) plus 5 gate extras. Real `createHealthRoutes` and `createVerificationRoutes`; same seam as the seat (only `getNotificationSettings` doubled; enforcement and workflow are spies).
- Base datum reproduced: ADMITTED (201, enforcement reached): `['SSD_DOCUMENT',1]`, `['SSD_DOCUMENT',null]`, `['SSD_DOCUMENT',{}]`, `['SSD_DOCUMENT',['x']]`, the hole, `['SSD_DOCUMENT',undefined]`, plus extras `['A','SSD_DOCUMENT',1]` and `[true,'SSD_DOCUMENT']`.
- Head: 0 non-string rows admit any create, and the two routes never disagree for one stored value. Non-array rows (`''`, `'SSD_DOCUMENT'`, `{}`, `0`, `false`, extra `true`) keep the older text and are byte-equal to base. `undefined`, `null`, `[]` and `['SSD_DOCUMENT']` are byte-equal to base.
- Evidence: `evidence/q3_table.txt`, `evidence/q3_base.json`, `evidence/q3_head.json`, harness `probe/gate210-table.test.ts`, comparator `probe/table_compare.mjs`.

**Q4 Mutants: 6 of 6 predictions matched on the killing mutants, plus 2 predicted survivors.** Predictions were written in the scripts before running. Every mutated file was restored sha256-equal.

| mutant | tsc | predicted red | actual red |
|---|---|---|---|
| S1 predicate checks list[0] only | 0 | R1-R5 | R1-R5 |
| S2b guard off in verification.ts | 0 | G6 R2 R3 R4 | G6 R2 R3 R4 |
| S3b health.ts answers the older text | 0 | G6 R1 R4 | G6 R1 R4 |
| S4 predicate uses some() | 0 | R1-R5 | R1-R5 |
| O1 own: a hole is skipped | 0 | R1-R5 | R1-R5 |
| O2 own: null/undefined let through | 0 | R1-R5 | R1-R5 |
| O3 own: first and last element only | 0 | survivor | none (F-1) |
| O4 own: `''` counted as a non-string | 0 | survivor | none (N-1) |

My first forms of S2 and S3 failed tsc with TS6133 (unused import). They are inadmissible and I discarded them, though they reddened the same cells; S2b and S3b are the admissible re-runs. That failure also serves as the positive control that `tsc` can fail. Evidence: `evidence/q4_mutants.txt`, `evidence/q4_mutants2.txt`, `evidence/mut_*.json`.

**Q5 Pin test: PASS.** The diff is 35 added lines after the existing describe block; 0 deletions, so G1-G5 are untouched. Base: 5 of 5. Head: 7 of 7. Both PR test files together: 17 of 17. Evidence: `evidence/q5_pin_base.txt`, `evidence/q5_pin_head.txt`.

**Q6 Suites: PASS. No known-red cell found for api-gateway; none named.** Own clone, no stack, Node v26.8.1, vitest 4.1.12.
- api-gateway plain vitest: base `85881fde5a48` 157 files / 1654 passed / 0 failed; head 158 / 1666 / 0. No failing cell, so nothing to classify. The seat's "before" figure names `7d2d6dc`, one commit behind its base; that commit changes nothing under `services/api-gateway`, and my base count equals its figure.
- `tsc --noEmit -p .`: 0 errors.
- `check.cjs services/api-gateway`: 25 errors, 25 in the baseline, 0 new, 0 stale, 158 test files. Planted type error: rc 1, "1 new", names the file. Only api-gateway's leg was run, as commissioned.
- eslint on the six .ts files: rc 0. Planted `debugger`: rc 1 `no-debugger`.
- `check:openapi`: rc 0, 422 examples.
- Evidence: `evidence/q6_*`.

**Q7 Spec and yaml: PASS.** The yaml diff is two lines (16836, 16861), both under `/api/connector/info` (description and 403). With a junk line planted in the yaml, `--check` gave rc 1; the generator then rewrote it to sha256 `5c7c87eb60f3...`, equal to the committed blob. `POST /api/documents`: see N-3. Evidence: `evidence/q7_regen.txt`, `evidence/q7_ops.txt`.

**Q8 Docs fragments: PASS.** Head check rc 0, "lint clean". Planted unbalanced tags in the PR's flow fragment: rc 1, FAIL naming that file. Restored sha256-equal. Advisories: N-4. Evidence: `evidence/q8_*`.

**Q9 Merge: PASS.**
- `merge-tree --write-tree` onto `1b1b65c7415f`: rc 0, tree `d467b978a8c5`.
- Shared paths between the PR's 9 and develop's 10 since base: 0. Planted control prints the added path. Evidence: `evidence/q9_*`.
- OVL knob, re-checked: both T 12th branches have heads and are unmoved from the seat's reading (KS-1539 `a56b949c56f0`, KS-1614 `8d4f6fca8388`). Neither has a PR: of 1942 `refs/pull/*/head` refs, neither SHA appears, and the control `ae8e8c78f91f` does. Objects were readable in my clone, so this is measured, not UNMEASURED.
- Against this head: KS-1539 rc 0, KS-1614 rc 0, both merged rc 0. Control, a planted commit at the insertion point on develop: rc 1, CONFLICT in `verification.ts`. Evidence: `evidence/q9_overlap.txt`.

## Not covered
- No stack, and no real stored config read: whether any stored list holds a non-string today is unknown. The storage read was doubled at `getNotificationSettings`, the seat's seam. Holes and explicit `undefined` cannot survive JSON, so those rows are reachable only through the double.
- The Postgres settings branch of `readPlatformSettings` (the harness has no database).
- No Node 24; all figures are v26.8.1.
- The four platform suites and pre-push legs 3, 4 and 8. Not commissioned: no stack is permitted here.
- `check:test-types` for the other four services (commissioned for api-gateway only). Base was not run for tsc, eslint or `check:test-types`.
- MCP consumer: READ ONLY. `services/mcp-server/src/tools/info.ts` already reports a gateway refusal with its text and `http-server.ts` passes the status through. Not driven.
- Merged-tree behaviour (this head plus the T 12th heads) was not executed; conflict check only.
- The seat's "16 open PRs" count, its ticket comment and the Linear census: not read (no Linear).

## Gate conduct
- Writes: only inside this folder, including objects written by `merge-tree` and `commit-tree` into my own clone (no ref written; `for-each-ref` shows none).
- Network: `git ls-remote origin` only, as Q9 directs. No fetch.
- `repo/` is my `--shared` clone of `worktrees/s-k16-base`, plus APFS-clone copies of Seat K 16th's `node_modules` and `packages/shared/dist`, read from `worktrees/s-k16-ks1534` (1.4G nominal; gitignored in this project). Left in place, like earlier gates' `repo/`. Quarantining it is Wednesday's call.
- The `no_cd` hook refused `git -C "$VAR" merge-tree` because it cannot resolve a variable. The target was inside WEDNESDAY, so I used the literal path, which it accepts. No hook was changed or bypassed.
- No process of mine remains running.

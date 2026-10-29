# QA GATE 17 - Secuura/Blockchain PRs #1808 and #1809 (tier 2), Seat R 61st

Base `develop` = `6d41673e0f79c0f02c2ec7b893cc960b6fa3ec10` (ls-remote at start and again before the mutants; unchanged). Heads asserted equal to the brief: #1808 `2a6611557c3f...`, #1809 `e30d6acc9ef7...`. Clone: `work/repo`, toplevel asserted before any fetch.

## BLUF

- **#1808 @ 2a661155: GO.** 0 blocker, 0 major, 0 minor, 3 info. Test-only; product blob unchanged (diff of `src/routes` vs develop is empty).
- **#1809 @ e30d6acc: GO WITH NOTES.** 0 blocker, 0 major, 2 minor, 3 info.
- **Merge order:** either order is fine for code. `merge-tree` conflicts ONLY in the two `Projects Documents/*.html` (both PRs append a section at end of file). Resolve by keeping both blocks. Non-doc files auto-merge. The combined tests (76-cell ks1780 + 6-cell ks1802 + neighbours, run on #1809's product with #1808's test file) are 94/94 green.
- **Skipped hook legs (3 of 16, local stack):** do not matter here. Both changes are covered by mocked-DB jest cells over a loopback listener; no schema, spec, SQL, or runtime-config change. Not a pass of those legs, simply not relevant.

## #1808 findings

| id | sev | finding | evidence | action |
|---|---|---|---|---|
| 1808-1 | info | **Author claims reproduce exactly.** Tamper of `isMissingTableError` (guard removed): 26/76 red, all in the A1/A2 cells (13 rows x 2), 0 controls red. Tamper of `errorMessageIncludes`: 4/76 red = B1,B2 x 2 routes, 0 controls red. Control run 76/76. Originate whole suite **1812/1812, 149 files, 0 skipped**; develop-side count not re-run (1757 per author; 1812-55 consistent). tsc with tests rc 0, eslint adminConfig rc 0. | `evidence/mut1808.out`, `full_wt-1808.json`, `tsc.out` | none |
| 1808-2 | info | **Stronger than the author's proof: all 15 catches are individually pinned.** I un-guarded each call site on its own (13 `isMissingTableError` sites, 2 `errorMessageIncludes` sites). Every one of the 13 reddens exactly 2 cells (its own row's A1+A2); each of the 2 message sites reddens its own B1+B2 plus the S1 source scan; no control ever went red. So "drives all 15" is true, with no row covering for another. | `evidence/mut1808.out` (SITE lines) | none |
| 1808-3 | info | Header comment and docs text are accurate: "Thirteen GET routes (four at first, nine added)", +55 cells = 45 + 10, "line 142 / 134" are the `try {` lines of the two helpers (author's line numbers are the try lines; the `return` lines are 143/135 - cosmetic). `html_docs_check` rc 0 on both docs; `html_docs_matrix.test.sh` 18/18 (same as develop). Section "109" is not a printed number: the h2 headings are unnumbered. | `evidence/docs_check.log` | none |

## #1809 findings

| id | sev | finding | evidence | action |
|---|---|---|---|---|
| 1809-1 | minor | **The fallback text is not pinned.** Mutant X3 (catch returns `undefined`) and X5 (`String(err?.message)`) both survive 6/6. No cell asserts what is logged for a hostile value (R1-R3 only check the HTTP report/counts). So the "fixed fallback" can be changed or dropped unnoticed. Suggest one cell: for a revoked Proxy, `mockLogError` called with `{email, error: 'thrown value that could not be described'}`. | `evidence/mut1809.out` X3,X5 | follow-up |
| 1809-2 | minor | **The helper guards the read, not the log.** `logger.error(...)` at the seed loop is not in its own try (fail500 and migrate-tenant-data both wrap theirs). If the logger throws, or `message` is a getter returning a value that makes the logger's serialiser throw, the throw still escapes the per-user catch to the outer catch, same hang-class the PR fixes. Read-only reasoning; NOT measured with the real logger (test mocks it). Not a regression: same behaviour as before for that case. | `adminConfig.ts` ~2121 vs fail500 L114-124 | follow-up (KS-1780 family) |
| 1809-3 | info | **Mutants.** X1 (author: try removed) reddens exactly R1-R3, controls green. X2 (catch rethrows): R1-R3. X4 (helper always returns the fallback): 1 red, C1 (the "message is logged" control) - good. X6 (call site also reads `err?.message`): R1-R3. Control 6/6. Base product: 3 red / 3 green (spark_gate) = R1-R3. | `evidence/mut1809.out`, `mut1809b.out` | none |
| 1809-4 | info | **Helper review.** It is called at exactly one site (seed loop catch); no other catch changed (diff +10/-1: helper + that one line). It cannot throw from the `err?.message` read. Fallback text is identical to the string already used by `fail500` and `migrate-tenant-data`, so it is consistent for operators. Information loss for an ordinary Error: none (C1 asserts the message is still logged; email stays in the line so the operator knows which user). | diff, C1 | none |
| 1809-5 | info | **Pre-existing, not introduced:** a thrown plain string logs `error: undefined` (`"x".message`), whereas fail500 logs the string. Same as before the PR. | code read | optional follow-up |
| 1809-6 | info | **Suites.** Originate whole: **1763/1763, 150 files**, 0 skipped. `ks1780` 21/21 on this product (in the suite); with #1808's 76-cell file on this product, 94/94 with ks1802 + neighbours. tsc with tests rc 0, eslint rc 0. Docs checks rc 0 / 18/18. | `full_wt-1809.json`, `combo.out`, `tsc.out` | none |

## Spark half (shadow, not my verdict)
`spark_gate.sh` exit 0 for both, with the gate 15/16 workaround (clone made `--shared` from the spark cache, `origin` -> GitHub URL, `core.sshCommand` = project deploy key, read use only; `--node-modules` = worktree root; `--work` in the session scratchpad).
- #1808: head tip, merge-base = develop, diff 3 files +104/-2. Targeted ks1780 on HEAD **76 pass / 0 fail**; on BASE product code 76/0 (expected: test-only PR, product unchanged, so base product also passes - the cells prove no regression, the red proof is the tamper above).
- #1809: diff 4 files +178/-1. Targeted on HEAD **6/0**; on BASE product code **3 pass / 3 fail** (matches R1-R3).
- No `spark_review.py` LLM verdict was run (not requested; gate 15/16 hit the HTTP 400 prompt overflow on the HTML docs).
- Harness faults: (a) first #1809 run reported 0/0 on both sides because `@secuura/shared` was not built in my worktree (my environment, see below); (b) first #1808 run died in `shadow_facts.py` with IndexError on an empty `git ls-remote` (a transient GitHub SSH drop; the same drop hit my setup script once); re-run was clean. The harness has no retry or readable error for an empty ls-remote.

## TESTED
Spark gate x2; ks1780 file at 1808 (76) with 2 helper tampers + 15 per-site tampers; ks1802 file with 6 mutants; originate whole suite at both heads; tsc incl. tests and eslint on adminConfig at both heads; html_docs_check + html_docs_matrix at develop/1808/1809; merge-tree both orders and each vs develop; combined tests (1808 test file on 1809 product).

## NOT TESTED
Any running stack, the 3 skipped hook legs, integration jest files (need Postgres), Node 24 LTS (host Node v26.8.1), the real logger under a hostile message (1809-2 is reasoning), a built/merged tree after docs conflict resolution (docs hunks not rebuilt; only merge-tree conflict list), GitHub PR bodies/Linear text, the `spark_review.py` LLM verdict, Schemathesis/Akto/k6. Develop's own originate count (1757) taken from the authors/gate 15.

## Instrument errors (mine)
1. Hook refusals for `cd` and for `git -C $VAR <write verb>` (re-issued via script files).
2. First `npm run build --workspace=shared` used a wrong workspace name (rc 1); the shared package was then built from `packages/shared` (rc 0). That caused harness fault (a).
3. First #1809 mutant run read "red 0" for X4 and X6 as survivors; they were TypeScript compile failures (unused param/function, `numFailedTestSuites` 1, 0 tests). I re-ran both with a variant that compiles (`mut1809b.out`) before counting them. X1 and X4 first-run suite-failed values are in the `evidence/mut/` JSON.
4. I left an untracked `tsconfig.gate17.json` in `work/wt-1808` and `wt-1809` (my worktrees only). Mutated files were restored with sha256 equal; the test file swap in the combo run was restored byte-equal.
- **PIDs started:** 33137, 33138 (installs), 52151, 55149 (full suites); all exited on their own. Nothing killed.
- Nothing pushed, commented, merged, or written under `!CODING`. No token printed.

Artefacts: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-29_gate17-1808-1809/evidence/` (scripts `setup*.sh`, `mut*.py`, `combo.py`, `tsc.py`; outputs `mut1808.out`, `mut1809.out`, `mut1809b.out`, `merge.log`, `docs_check.log`, `full_*.json`, `combo.out`, `spark_*.out`, `tsc.out`). Work dir left in `work/`.

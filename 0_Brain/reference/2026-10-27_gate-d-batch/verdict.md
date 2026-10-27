# QA gate verdict - Secuura/Blockchain PRs #1743, #1744, #1745, #1746

- Tier 2, round 1 of 2. Gate model: Claude Sonnet 5.5 (claude-sonnet-5-5). Date 2026-10-27.
- Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-d-1027/` (clone `repo/`, worktrees `wt_dev`, `wt_p1743`..`wt_p1746`, raw logs and scripts beside; private `TMPDIR=/tmp/gd1`). Node v26.8.1. `npm ci` in `Blockchain/Dev` of all five worktrees (rc 0 each) and `packages/shared` built in each (rc 0).
- Pushed / merged / commented / edited a ticket / changed a PR: nothing. Git only (deploy key for the fetch); I did not use `gh`.
- Mutants were made in my own worktrees and restored with a saved copy each time; all five worktrees `git status` empty at the end.

## BLUF
| PR | Verdict | Worst finding |
|---|---|---|
| #1743 KS-1621 item 3 (Seat X 1st) | GO | INFO only. Comment-only proved (emit with comments stripped 6,880 bytes, sha16 cf10f87b237cb568 on develop, base and head; a code-token control moves it). The new header is true against the catch. |
| #1744 KS-1529 (Seat W 1st) | GO | INFO only. Every number reproduced (73/73 -> 84/84; red-first 4 red / 7 green; 8+ mutants each red the intended cell; the ticket's own shape for (b) leaves M3 green, the AST pin kills it; check:test-types 42/0 new). The two stated residuals are real and I found two further unstated blind shapes of the same class. |
| #1745 KS-1756 (Seat Z 1st) | GO | INFO only. 75/0 -> 82/0; `-z` disjunct is an equivalent mutant (75/0 vs 82/0, zero cells move); M_accept 75/0 survives vs 76/6; M_2nd 71/4 vs 79/3; `preflight.sh` blob identical; run-shell-suites 95/0/1 of 96. Docs carry literal `NN` headings (5 of them) that the merger must number. |
| #1746 KS-1548 (Seat AA 1st) | GO | INFO only. The softened comment is TRUE (fetchWithTimeout's timer is cleared at fetch() resolve, so a stalled body is unbounded; I measured 6016 ms against a 2000 ms budget). Comment-only proved (emit hash 7304f87a279c9b00, 34,261 bytes, identical; control moves). nit mutant: old 18/18 x2, new 1 failed / 17 passed x3, cell G alone. |

Merge: **#1743 is clean in every order and position** (touches no doc). #1744, #1745, #1746 each append one block at the same `</body>` of the same two Projects Documents HTML docs, so any two of them conflict textually; **every one of the 64 order/subset sequences (all permutations of every non-empty subset of the four) resolves by keep-both with zero loss** (details below). Section numbers are for the merger; not a defect.

## Pins (start = end)
```
885d69b06f5fce7c8f58effea68623ecb25407b1  refs/heads/develop
7b8094724cbd3b71665d5b6f9734daadf10c4431  refs/pull/1743/head
d71107ad141b815bf99eb00c7be3090458fc2b4f  refs/pull/1744/head
4da9cc83484e84d7f3d765a94cd0302edda59f86  refs/pull/1745/head
3fb9cca01377967e75301ff8903af2ea8e7da50f  refs/pull/1746/head
```
`lsremote_start.txt` was read before anything else (after the one command that failed on a hook, before any clone) and `lsremote_end.txt` at the very end; `diff` empty (rc 0); both equal the briefed pins.
Merge bases: #1743 on `b6366c12` (a commit behind develop; the file it touches is unchanged on develop since, so `develop...head` and the emit of develop's file agree); #1744, #1745, #1746 on `885d69b0` = develop. I used `develop...head` for every diff.

## #1743 KS-1621 item 3

**FOUND**
- Scope vs develop (`develop...head`): exactly 1 file, 4+/4-: `services/api-gateway/src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts`, header lines 1-6 only (a 6-line comment block becomes a 6-line comment block).
- The new header is TRUE. It says the catch logs "via fail500's describer (routes/batch.ts, KS-1346; KS-1619 part 3 replaced `err instanceof Error ? err.message : String(err)`)". Read: `routes/verification.ts:1067` (the `/api/document-types` catch) logs `err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + ctor + ' with fields [..]' : 'thrown ' + typeof err`, byte-for-byte the expression in `routes/batch.ts` `fail500` (lines 24-28, KS-1346). `String(err)` survives only at `verification.ts:907` (the document-create pipeline), which the new header no longer claims for this catch.
- INFO-1: "via fail500's describer" is an inlined COPY of the describer expression, not a call to `fail500` (the catch must log through the router's injected `log`, and `fail500` uses the module logger). The route comment at :1066 says the same; accurate enough, but a reader may look for a call.
- INFO-2: pre-existing and NOT in this diff: the KS-1619 comment further down the same test file still says "the :1579 log line"; the catch is at `verification.ts:1067`. The item the PR was filed to fix (the header) is fixed; this is a neighbouring stale line citation.
- Docs not updated: the escape clause, as briefed. Nothing to check.

**TESTED / HOW**
- Comment-only, by TypeScript emit with comments removed (`ts.transpileModule`, `removeComments: true`, same filename for both sides): develop's file, the merge-base's file and the head's file all emit **6,880 bytes, sha16 cf10f87b237cb568**, matching the seat's figure. Control that can fail: in a copy, one string literal and one identifier changed -> **d388822fff61bc01**, differs.
- `ks1543-document-types-catch-logs-the-error.test.ts` (10 cells): develop **10/10**, head **10/10**, rc 0 both (warm runs; see instrument errors 1).
- My own mutant of the code the header describes: in my head worktree, the catch's log expression replaced by `err instanceof Error ? err.message : String(err)` (the thing the old header described). Result **4 failed / 6 passed**: KS-1619 D1 (plain object), D2 (null), D3 (number), D4 (class instance) red; restored, 10/10 again. So the header's contrast (describer, not `String(err)`) is what the test file actually pins.
- Verdict note: through-code is enough for this one, and this is through-code plus a mutant.

## #1744 KS-1529

**FOUND**
- Scope vs develop: 3 files, 188+/6-: `services/auth/src/__tests__/ks1000-auth-test-files-are-type-checked-against-a-shrinking-baseline.test.ts` 154+/6-, flow doc 10+/0-, cheat sheet 24+/0-. No product code. The test gains `import ts from 'typescript'` (already in the workspace; the file ran).
- Test design (read in full): `RUN_AS_ONE_VALUE = /expect\(\s*[[{][^\]}]*(?:\.status[^\]}]*\.out|\.out[^\]}]*\.status)/g` over the JOINED text (not line by line); `runsComparedAsOneValue` maps match index to a 1-based line; the REAL gate cell now passes the named constant `AUTH_GREEN_SUMMARY`; a new describe plants 5 forbidden and 4 permitted shapes in a copy of the file's own text, plus a "can fail" cell and an AST pin cell that reads the REAL cell off the TypeScript syntax tree. 11 new cells = 5 + 4 + 2.
- Docs: numstat 0 deletions; head text equals merge-base text up to `</body>` and the suffix from `</body>` is unchanged in both docs (pure append, 10,399 and 5,895 bytes added); tags balanced (HTMLParser: 0 mismatches, 0 open, both ends, both docs); `html_docs_matrix.test.sh` 18/0, rc 0 (also on develop and the other heads). Section **65**; develop's last is 64, so 65 is correct against current develop (collides with #1746's 65, see merge orders).
- INFO-1: the docstring's stated residual is real and slightly understated in position: ANY bracket nested before `.out` (or before the second field) ends the scan, whether it sits before the first or the second field. I measured `[parts[0], r.status, r.out]`, `[r.status, parts[0], r.out]` and an object with a nested object literal first: all **missed**. Stated by the seat as not fixed; confirmed, not a defect in the claim.
- INFO-2: two further shapes the guard does not see and the PR does not claim: a template string joining both (`` expect(`${r.status} ${r.out}`) ``) and an array built into a variable first (`const v = [r.status, r.out]; expect(v)`). Both **missed**. Out of the ticket's stated scope (object, reversed, split); noting them as the next blind spots of the same guard.
- INFO-3: `expect([r.status, r.out.length])` is **flagged** (it holds both fields in one value). Conservative, and none exist in the file.
- INFO-4: docs say "measured at base b6366c12a8ab"; the PR's merge-base is `885d69b0`. Same pattern as earlier batches.

**TESTED / HOW** (`TMPDIR=/tmp/gd1`, vitest 4.1.12, `services/auth`)
- The ks1000 file: develop **73/73**, head **84/84**, rc 0 both. Claim holds (BEFORE and AFTER).
- Red-first (claimed "4 red / 7 green of the 11 new cells"): the new file with the OLD guard (per-line array-only regex) and the literal back in the REAL cell, `-t KS-1529`: **4 failed / 7 passed**. The 4: RED (a) object, RED (a) reversed, RED (a) split over lines, RED (b) REAL-cell pin. Claim reproduced exactly.
- check:test-types: develop, head: `auth ... 42 errors: 42 in the baseline, 0 new; 0 stale`, rc 0 both (and api-gateway 27/27/0 new).
- The ticket's own shape for (b) does not kill M3 (claim): M3 (the REAL cell reduced to `expect(r.status, r.out).toBe(0)`) with the pin cell EXCLUDED (`-t` negative lookahead): **83 passed, 1 skipped, 0 red, rc 0**. Same M3 with the pin: the pin cell goes red alone. Reproduced both ways.
- Mutants of my own on the test file (scan `-t "KS-1529|compares a run as one value|REAL: services/auth against the committed baseline passes"`; control = 13 passed, rc 0):
| arm | result | cell(s) that went red |
|---|---|---|
| m0 control (unmodified) | 13 passed | none |
| m1 regex array-only | 2 failed | RED (a) OBJECT, RED (a) REVERSED |
| m2 scan bounded by `)` (the ticket's first suggestion) | 1 failed | RED (a) nested CALL ahead of `.status` |
| m3 reversed alternative dropped | 1 failed | RED (a) REVERSED |
| m4 REAL cell -> bare status check (M3) | 1 failed | RED (b) pin cell |
| m5 REAL `expectRun` call commented out | 1 failed | RED (b) pin cell |
| m6 `AUTH_GREEN_SUMMARY = ''` | 1 failed | RED (b) "can fail" cell |
| m7 scan allowed to read across closed brackets (`[\s\S]*?`) | 2 failed | CONTROL (a) permitted: "closed array followed by a use of both fields" and "each field in an array of its own" |
| m8 scan back to line-by-line | 1 failed | RED (a) SPLIT over several lines |
  Every mutant reds exactly the cell(s) meant to catch it. The claim "8 for (a) + 7 for (b)" I did not reproduce count-for-count (I ran 8 mutants of my own choosing, plus the pin's own five internal mutants run inside the pin cell); each of mine was killed.
- Controls that can fail: the permitted-shape cells are red under m7; the pin's own five internal mutants are exercised by the pin cell (it asserts each mutant differs from the cell AND finds zero green calls).

## #1745 KS-1756

**FOUND**
- Scope vs develop: 3 files, 77+/2-: `scripts/__tests__/preflight_deps.test.sh` 40+/2-, flow doc 14+/0-, cheat sheet 23+/0-. `scripts/preflight/preflight.sh` is **NOT edited**: blob `965255bfad091bcdf4ec1929b638d99b8dcae281` on develop and on the head (zero preflight files in the name-only diff). The seat's sha256 `bae62e73...` I did not recompute; the git blob identity is the stronger statement.
- The fix: `nocontrol` now writes a hook whose control line starts with `#` (dropped by the filter at `preflight.sh:722`), so the derived set is really empty; the old `: # ...` line is kept as new mode `trailingcomment`. Seven new cells (five whole-line assertions on the refusal's `Derived: [...]` line plus two controls). I confirmed the filter regex (`grep -vE '^[[:space:]]*#'`) and the refusal text at :731-735 match what the cells assert.
- Docs: numstat 0 deletions; pure append before `</body>` in both docs (8,754 and 5,436 bytes), tags balanced, `html_docs_matrix.test.sh` 18/0. The flow-doc headings are literal `NN.`, `NN.1`..`NN.4` (5 occurrences) as briefed; the cheat sheet is unnumbered. INFO-1: the merger must replace all five `NN` tokens (not one).
- INFO-2: docs say "measured at base b6366c12a8ab"; merge-base is `885d69b0`.
- INFO-3: "also 82/0 on the merged head" I did NOT measure on a merged tree (the PR touches only this one suite file, so the suite on a merge of the other three would see no change from it; unmeasured, not refuted).

**TESTED / HOW** (bash 3.2, `TMPDIR=/tmp/gd1`)
- `preflight_deps.test.sh`: develop **75/0**, head **82/0**, rc 0 both; `bash -n` rc 0. Claim holds.
- Red-first: head suite with only the `nocontrol` line reverted to `: #` (the old defect): **80 passed / 2 failed** (the empty-set cell and its control), as the docs say.
- Mutants on `preflight.sh:731`, run against the base suite (wt_dev) and the edited suite (wt_p1745), file restored after each:
| mutant | base suite | edited suite | reading |
|---|---|---|---|
| M_eq: `-z` disjunct deleted | 75/0 | 82/0 | zero cells move: EQUIVALENT mutant, claim holds (for an empty set the second half is also true) |
| M_accept: an empty set is accepted (`[ -n .. ] && ! grep`) | 75/0, survives | 76/6 | claim holds exactly |
| M_2nd: only `-z` remains | 71/4 | 79/3 | claim holds exactly |
| M_x (mine): `Derived: [..]` brackets changed to `(..)` | 75/0, survives | 80/2 | the new whole-line cells catch a message change the base suite cannot |
| M_y (mine): refusal never fires (`if false`) | 71/4 | 73/9 | both kill; the edited suite more strongly |
  Controls that can fail: each arm's `Derived` assertion has a control that the other arm's output must NOT satisfy; M_accept and M_x are exactly the mutants that make those cells move.
- Whole shell-suite run `scripts/run-shell-suites.sh` on the head: **95 passed, 0 failed, 1 skipped (of 96)**, rc 0; the skip is `ks949_main_seed_idempotence.test.sh` (no PostgreSQL, ruled). Claim holds. I did not run it on develop; the 96-suite population and the skip I did not compare base against head.

## #1746 KS-1548

**FOUND**
- Scope vs develop: 4 files, 37+/3-... precisely: test 3+/1-, `routes/platform.ts` 2+/2-, flow doc 16+/0-, cheat sheet 17+/0-. No other product file. `platform.ts` stays 1,150 lines (the docs rely on that for citations): confirmed (`git show` of both = 1150).
- The comment, now at `platform.ts:474-476`: "...so a SLOW upstream degrades the page to the audit_logs rows. The budget bounds the HEADERS wait, not the BODY read (KS-1548 m1): fetchWithTimeout's timer stops at fetch(), so a stalled body holds the request." **TRUE against the code**: `fetchWithTimeout` (:217-233) arms an AbortController timer, `return await fetch(...)`, and `finally { clearTimeout(timer) }`, so the timer ends when the headers arrive; `await r.json()` at ~:491 runs with no timer. The old "never hangs" claim is gone and nothing replaces it with a new overclaim. Also checked: the surrounding sentences (per-window timeout `min(UPSTREAM_TIMEOUT_MS, remaining)`, discard-on-spent-budget) still match the loop below it.
- The assertion: cell G's second `expect` now compares `calls.map(c => c.offset)` to `Array.from({length: ceil((250+25)/upstreamClamp)}, (_, i) => i * upstreamClamp)` = `[0,100,200]`. It tracks the clamp variable, so a cell edit to another clamp keeps the formula honest.
- m2: already on develop as `5e59eacb3 ... (KS-1548 item m2) (#1698)`.
- Docs: numstat 0 deletions; pure append before `</body>` in both docs (6,935 and 3,295 bytes), tags balanced, `html_docs_matrix.test.sh` 18/0. Section **65**, correct against develop's top of 64; collides with #1744's 65 (merge orders). INFO-1: docs say "base 885d69b06f5f" (correct for this PR) while #1744/#1745 say b6366c12.
- INFO-2: cell G pins window STARTS only, not the window LIMITS (200, 175, 75 under clamp 100); the docs say so themselves (65.3). Not tested by me beyond reading.

**TESTED / HOW** (`TMPDIR=/tmp/gd1`, api-gateway)
- ks1512 file: develop **18/18**, head **18/18**, rc 0 both.
- Comment-only claim, by emit with comments removed (one filename): develop's `platform.ts` and the head's both emit **34,261 bytes, sha16 7304f87a279c9b00**, IDENTICAL, matching the seat's figure. Controls that can fail: `if (remaining <= 0)` -> `< 0` in a copy moves it to **0c6e8f7315f5bd43** (also the seat's figure); a comment-only edit in a copy leaves it at 7304f87a279c9b00.
- m1 measured ("a body stalled 6000 ms ... answered at 6016 ms"): a copy of the head test file with the first window's body delayed 6000 ms (cell M's harness, 2000 ms budget): **PROBE_M1_MS 6016, status 200, 1 upstream call**. Exactly the seat's 6016 ms. So the budget does not bound a stalled body, and the comment now says so.
- The nit mutant ("retry a short window": when a window returns fewer rows than asked, `total` says more exists, ask the same offset again once): old assertion (develop's test file) **18/18 in 2 of 2 runs**; new assertion **1 failed / 17 passed in 3 of 3 runs, cell G alone**. Reproduced exactly. (My first two candidate mutants were too coarse and are in instrument errors 3.)
- m2 on develop (claim "current file fails cell M ALONE"): in my worktree the `if (remaining <= 0) throw` guard deleted: **1 failed / 17 passed, cell M alone**, in the new test file AND in develop's old test file (2 of 2; the seat said 5 of 5, I ran two).
- api-gateway whole suite: head **123 files / 1203 tests, 0 failed, rc 0**; develop **123 / 1203, 0 failed, rc 0 on the re-run** (see instrument errors 2 for the cold first run). `check:test-types` rc 0, api-gateway `27 errors: 27 in the baseline, 0 new`, both ends.

## Merge orders (my clone only; `git merge-tree --write-tree --name-only` chained with `commit-tree`; script `merges.py`, output `merge_out.txt`)
Develop at 885d69b0. All four heads sit on develop or one commit behind it; #1743 touches no doc. Conflicts occur only when two of #1744/#1745/#1746 meet: both add their block at the same `</body>` of the same two files, `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` and `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html`. The script refuses to resolve any other file (it asserts the conflict list is non-empty and a subset of those two) and none arose.
Resolution used: keep the accumulated text and insert each PR's added block (head minus merge-base, asserted to be a pure pre-`</body>` insertion) before `</body>`, in merge order. For every one of the **64 sequences** (4 + 12 + 24 + 24: every ordered selection of 1, 2, 3 or 4 of the four PRs): no conflict markers remain, the doc text starts with develop's text up to `</body>` and ends with develop's `</body>...` suffix, exactly one `</body>`, every merged PR's block is present in both docs, and the merged additions/deletions vs develop equal the sum of the PRs' `develop...head` numstats (e.g. all four: +307 / -15 = 4+4, 188+6, 77+2, 38+3). **Zero loss in every sequence; 0 mismatches.**

| orders | result |
|---|---|
| #1743 alone, or #1743 before/after anything | clean in every position (identical tree to the same set without it; e.g. `{1744,1743}` = one tree) |
| #1744 alone, #1745 alone, #1746 alone | each clean against develop (develop has not moved under any of them) |
| any pair of #1744/#1745/#1746 | doc conflicts in both docs (expected class), keep-both clean; 2 distinct trees per pair, differing only in which block comes first |
| all three of #1744/#1745/#1746 (6 orders) | first merged is clean, 2nd and 3rd each conflict in both docs, keep-both clean; 6 distinct trees = the 6 block orders |
| all four, 24 orders | the tree depends only on the order of the three doc-adding PRs: 6 distinct trees across the 24; #1743's position changes nothing |

Numbering after keep-both: #1744 and #1746 both say **65** (the merger renumbers the second to 66, or the third to 67 if #1745's `NN` takes one); #1745's five `NN` tokens take whichever number it gets. Cheat-sheet sections are unnumbered. Per brief, not a defect.

## NOT TESTED (stated plainly)
- Any of the suites on a **merged tree** (trees computed only; nothing built or run on a merge). This includes the seat's "82/0 on the merged head" for #1745.
- The four platform suites (Schemathesis, Akto, Playwright, Performance), as the seats state.
- The whole `services/auth` suite (the seat's "1143 of 1146, 3 failures in ks949-platform-admin..."): I ran only the ks1000 file (needs no Postgres). Lint (ESLint on changed files) was not run by me.
- `run-shell-suites.sh` on develop (population 96 base vs head; skip identity beyond the one skip printed).
- The seat's count of "8 mutants for (a) + 7 for (b)" is not reproduced count-for-count; my own 8 killed as listed. #1746's "m2 5 of 5 runs": I ran 2. "Window LIMITS under a lower clamp" (not pinned by cell G, by the seat's own admission).
- Any browser render of the two HTML docs; I checked append-only, balance and the repo's own `html_docs_matrix.test.sh`.
- Linear states and PR check states (no `gh`).

## My instrument errors
1. First head run of `ks1543` read **0 of 10, 10 skipped, rc 1**: `Hook timed out in 10000ms` in `beforeAll` (cold transform, load from my concurrent shell/vitest jobs). A re-run in isolation read 10/10; develop 10/10. My concurrency, not the PR. The same first cold run of my String(err) mutant was also a `beforeAll` timeout (10 skipped), which I discarded and re-ran warm (4 red / 6 green, the result above).
2. First full api-gateway run on develop read **3 files failed / 2 tests failed (1189 passed)**: `Hook timed out in 10000ms` and `Test timed out in 5000ms` in ks815, ks1054, ks1101 (cold cache, my other jobs running). Re-run on the same tree: **123 / 1203, 0 failed**. These three files are untouched by any of the four PRs. The first run is my instrument; it does mean that suite is load-sensitive on a cold box (INFO, pre-existing).
3. My first #1746 mutants were bad instruments: a global retry flag that leaked across cells (reds cell E) and an "extra window" mutant (reds C, D, G, I, K1) both failed old and new files alike, so they do not discriminate. I replaced them with the scoped "retry a short window once, only when `total` says more exists" mutant above, which is the one behind the old-18/18 vs new-1/17 figures.
4. My first merge script lost the first conflicted file name (list slice off by one), so the first two conflicted merges left git conflict markers in the docs and the line counts were off by +3. A conservation check caught it (+313 vs expected +307). I fixed the parse, added "conflict list non-empty", "no `<<<<<<<` in the result" and exact-sum checks, and re-ran; the table above is from the corrected run.
5. I read `platform.ts` from the live #1746 worktree while my mutant script had it mutated (1,152 lines, hash DIFFER). I re-read it from the commit with `git show` (1,150 lines, IDENTICAL). The result above is from the commit.
6. My raw token-stream compare for #1746 reported one differing token (a scanner artefact: the bare TypeScript scanner has no parser context and mis-lexes a template literal near the changed comment). The compiler emit hash, which has context, is the evidence used; I do not claim the token compare.
7. The first #1746 probe script had a non-unique anchor (cell H and M share text) and wrote no file; I re-did it with a unique anchor. Fleet hooks also refused `cd`, `rm`, and an unquoted-variable command; I re-issued everything as script files with absolute paths and used `mv` to `/tmp/gd1/quarantine` instead of `rm`.

## Files outside the workspace
None kept. Writes: the workspace; `/tmp/gd1` (private TMPDIR, scratch copies, temp index files, the suites' own `ks1526-*`, `ks691-leg1.*`, `ks1054_nopy.*` temp dirs, and `quarantine/` holding my probe/old-copy test files moved out of the worktree); this verdict folder `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-27_gate-d-batch/`. Read-only use of the deploy key under `!CODING/`. `find /Volumes/DevMASTER/WEDNESDAY -maxdepth 1 -newer lsremote_start.txt` lists only `.git`. No process of mine left running; all five worktrees `git status` empty; clone `repo/` `git status` empty.

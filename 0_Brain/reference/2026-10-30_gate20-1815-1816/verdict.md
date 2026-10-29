# QA GATE 20 - Secuura/Blockchain PRs #1815 and #1816 (tier 2, test additions plus one logging guard)

Base `develop` = `203734468019feaf44428975b10cf5f799483187` (ls-remote at start, 2026-10-29T16:04:03Z, and again at end, 16:19:32Z; unchanged). Heads read at origin in the same action as the pin, and equal to the brief at both times: #1815 `331d50e09868e9c73d3641812e42e3480ff3dbe2`, #1816 `b587566ec83779e4e78a0e1d99ccd3d1ffa76869`. **Neither PR nor develop moved during the gate.** My clone is `work/repo`, made at a non-existent path, toplevel asserted before any fetch. Network git used the Secuura deploy key through `core.sshCommand` with `GIT_SSH_COMMAND` unset. Findings only: I pushed, commented, merged and messaged nothing, and wrote nothing under `!CODING`. Linear was read only.

## BLUF

- **#1815 @ 331d50e0: GO WITH NOTES.** 0 blocker, 0 major, 1 minor, 4 info. **Nothing to fix before merge** except the docs renumber, which is merge prep.
  - **Zero product bytes** (0 files outside `__tests__` and `Projects Documents`).
  - **Its cells still pass on the new develop.** I built develop `20373446` plus the PR's two test files: the two files are **51 of 51**, and B6 reads the `:id` handler after #1813 changed it. The whole anchoring suite on that tree is 36 files / 537 cells, 536 pass, 1 fail, the pre-existing `threadTokenMint` cell.
  - **Both seat mutants reproduce.** X16 (comment out the spread) reddens exactly B6. X8 (also admit `declare`) reddens exactly the R6-declare cell. I also ran X8 for all 25 other verbs: **each reddens exactly its own R6 cell, and no other.**
  - **One survivor:** a live line that keeps the spread text in a trailing `//` comment stays 51 of 51 (1815-1).
- **#1816 @ b587566e: GO WITH NOTES.** 0 blocker, 0 major, 1 minor, 4 info. **No fix-before-merge.**
  - **The product change is exactly one guarded logger call and nothing else.** `git diff -w` minus comment lines shows one removed line and two added (`try { <same logger.error call> } catch {` and `}`). The arguments are unchanged.
  - **R4 and R5 are red on the unfixed product, 2 of 9.** X3 (the helper returns `undefined`) reddens exactly R6.
  - **One gap:** the fallback's TYPE for a message-less thrown value is still unpinned (a `String()` coercion survives 9 of 9). That is gate 17's X5, which KS-1817's ticket names (1816-1).
- **Merge onto develop `20373446`:** **code merges clean for both. Both conflict in the two `Projects Documents/*.html` files only** (end-of-file append collision with #1813's section 113). Not a finding, by design.
- **Order: #1816 first, then #1815.** The code is independent (different services). #1816 numbers its section `114`, which fits after develop's 113: it needs a conflict resolution that keeps both blocks, but no renumber. #1815 numbers its section `113`, which now collides with develop's merged #1813 block: it must renumber (to 115 if it goes second). The other order needs two renumbers.

## Spark half (run FIRST per PR, one at a time, bare base ref `develop`; an input, not my verdict)

- **#1815:** exit 0. Tip `331d50e0`, merge-base `d7ddfa1f`, diff 4 files +70/-1. Targeted: **HEAD 51 pass / 0 fail; BASE product code 51 / 0.** BASE is also green because the PR changes no product code; the red-proof is the mutants below.
- **#1816:** exit 0. Tip `b587566e`, merge-base `d7ddfa1f`, diff 4 files +77/-1. Targeted: **HEAD 9 pass / 0 fail; BASE product code 7 pass / 2 fail** (R4 and R5).
- **Harness fault, mine:** the first #1815 run had no usable runner. `--node-modules` pointed at `services/anchoring/node_modules` (it has no `.bin`), so every file died with `vitest: command not found` and facts.json showed 0 passed 0 failed with exit 0. Kept as `evidence/spark_1815.try1_nodemodules_wrong_dir.out`. I re-ran with the workspace-root `node_modules`. **Proposal: `spark_gate.sh` should exit non-zero when `files_failed` equals `files` with `passed + failed = 0`.** It exits 0 today.
- No `spark_review.py` LLM verdict was run (not requested).

## Verdicts

| PR | verdict | B | Ma | Mi | I | fix-before-merge |
|---|---|---|---|---|---|---|
| #1815 @ 331d50e0 | **GO WITH NOTES** | 0 | 0 | 1 | 4 | none (docs renumber at prep) |
| #1816 @ b587566e | **GO WITH NOTES** | 0 | 0 | 1 | 4 | none |

---

## #1815 (KS-1827 + KS-1828): FOUND

| id | sev | finding | instrument / line | evidence class | action |
|---|---|---|---|---|---|
| 1815-1 | **minor** | **B6's comment stripper handles only `/* */` blocks and WHOLE-line `//`.** A mutant that makes the line live-different but leaves the spread text in a trailing comment (`...{}, // ...anchorSignatureHashView(...)`) passes 51 of 51: B5 matches the text, B6 does not strip trailing comments. B6's title says "live code, not commented out", and a trailing comment is a comment. Contrived (it needs a deliberate edit), but it is the exact class KS-1827 was filed for. | `ks1454-...-read-back-...test.ts` B6 (`split('\n').filter(startsWith('//'))`); mutant X16c in `mut1815.out` | MEASURED | follow-up: also strip `\s//.*$` per line (the slice holds no URLs on the lines of interest; check before applying) |
| 1815-2 | info | **Seat facts reproduce.** Zero product bytes. X16 at `index.ts:960` reddens B6, 1 of 11 in its file; X8 at `anchorSchema.ts:301` reddens R6-declare, 1 of 40 in its file. I confirmed both line numbers at the head. Counts: 11 + 40 = 51, the 28 new cells are 2 + 26 (25 R6 + C5). | spark_1815.out, `mut1815.out` | MEASURED | none |
| 1815-3 | info | **Cross-PR check passes.** On develop `20373446` (#1813 moved the `:id` handler: `index.ts` +6, the spread is now line 964) B6 and B7 still pass, and X16 on the new handler still reddens exactly B6. | `merged_1815_targeted.out`, `mut1815.out` | MEASURED | none |
| 1815-4 | info | **B7's third assertion is pinned to the exact text of a product comment** (`'KS-1454: the SHA-256 of the detached'`). Rewording that comment reddens B7 though nothing is wrong. It is the control's deliberate anchor, and it will say so loudly. B6 also still cannot see an unreachable-but-live spread (after a `return`); the PR's doc 113.3 states this. | B7; doc 113.3 | READ ONLY | none |
| 1815-5 | info | **Docs section collision, by design.** #1815 adds `<h2>113.` and develop already has #1813's 113, so the file conflicts at end of file in both docs (merge-tree rc 1, those two files only). Renumber at prep. | grep of develop and head; `git_checks.out` | MEASURED | docs re-prep of whichever merges second |

### #1815 TESTED (HOW, with the FAIL condition each carried)

- **Diff read against KS-1827 and KS-1828, every changed line.** The only edits are the `ACCEPTED_LIFECYCLE_VERBS` import, B6, B7, `OTHER_VERBS`, R6 (`it.each`), C5, and two doc blocks. No existing cell is edited, so none lost meaning. B5 stays as the old text pin and B6 is strictly stricter.
- **Does each cell test its title?**
  - B6: strips comments, requires the live spread. Killed by X16, X16b and X15 (below).
  - R6: one cell per accepted verb that is not `sign` (25), each posting a `signatureHash` and expecting a refusal.
  - C5: asserts the list has `declare` and `upload`, never `sign`, and the full list does have `sign`, so `it.each` cannot go empty unnoticed.
- **Spark gate:** HEAD 51/0, BASE 51/0 (test-only PR).
- **Merged tree (develop `20373446` + the PR's two test files; develop did not touch those paths):** the two files **51 of 51**. Whole anchoring suite: **36 files, 537 tests, 536 pass, 1 fail** = `threadTokenMint ... deterministic per-seed policyId`, also the one failure at the PR's own head (35 files / 525 / 524 / 1, seat: 525) and at base per KS-1827. FAIL condition: any other red. None.
- **Mutants (mine, each planted alone as an exact-once replace in the merged tree, restored, sha256 equal every time):**

  | mutant | change planted | red cells |
  |---|---|---|
  | X16 | spread line `//`-commented | B6 only |
  | X15 | spread line removed | B5, B6 |
  | X16b | spread inside `/* */` | B6 only |
  | X16c | live line with the text in a trailing `//` | **none (survives)** |
  | X17 | spread argument broken | B5, B6 |
  | X8[verb] x25 | refinement also admits one verb (each of the 25) | exactly that verb's R6 cell (for `upload`, also the old R2) |
  | S-all | refinement disabled | 27 (R2, R3, 25 R6) |
  | S-flip | `=== 'sign'` | 30 |

  Controls: baseline 51/0 before the run; X15 (a removal) is seen by B5 as well, so the harness shows red.
- **Docs:** `html_docs_check.mjs` rc 0 on both files at both heads and at develop. **Planted defect** (a 300-character `<p>` of prose outside a table, before `</body>`, in scratchpad copies of all four head files): rc 1 on all four, finding "prose outside a table". The instrument can fail. Content: 51 of 51 (11 and 40), 28 new cells, 35 files / 525 cells (524 pass, 1 fail) all match what I measured. Section number `113` collides with develop (1815-5).
- **Linear KS-1827 and KS-1828:** read; the ticket claims match the diff and the numbers (25 other verbs; B6/B7; C5).

---

## #1816 (KS-1818 + KS-1817): FOUND

| id | sev | finding | instrument / line | evidence class | action |
|---|---|---|---|---|---|
| 1816-1 | **minor** | **The fallback's type is still unpinned.** R6 pins the TEXT for a revoked Proxy and a throwing getter. A mutant making the helper return `String(err?.message ?? err)` (a message-less thrown value logs `"[object Object]"`/`"undefined"` instead of `undefined`) stays 9 of 9 (Y7, Y10). That is the X5 survivor named in KS-1817's own text ("fallback's text and type"). The PR's doc claims only the X3 text pin, so nothing is overstated; the ticket stays open per the PR comment. | `readableErrorMessage` (`adminConfig.ts:148-154`); mutants Y7 and Y10 in `mut1816.out`, `mut1816b.out` | MEASURED | follow-up: one cell whose insert rejects with a message-less value (a plain string) expecting `error: undefined` |
| 1816-2 | info | **Product change is exactly the guarded logger call.** Non-comment diff lines: one removed (`logger.error('Demo user seed failed', { email: u.email, error: readableErrorMessage(err) });`), two added (the same call inside `try { ... } catch {`, and the closing `}`). `readableErrorMessage(err)` is evaluated INSIDE the new try, so a throwing serialiser is covered too. `failed++` stays before the try, so a log failure still counts the failure. +5/-1 as stated (3 are comment lines). | `git diff -w` filtered; `adminConfig.ts:2118-2125` | MEASURED | none |
| 1816-3 | info | **Seat facts reproduce.** R4/R5 are 2 of 9 red on the unfixed product (7 pass / 2 fail, the seat's "2 of 8" excludes R6). X3 at `adminConfig.ts:154` reddens exactly R6. Whole originate suite: 150 files / 1821 / 0 failed. | spark_1816.out, `mut1816.out`, `full_originate_wt-1816.json` | MEASURED | none |
| 1816-4 | info | **No state leaks between cells.** `beforeEach` runs `mockLogError.mockReset()`, which drops the throwing implementation R4/R5 install, so C1-C3 are not run under a throwing logger. R6 resets inside its loop for each hostile value. | test file `beforeEach`, `:61-66` | READ ONLY (plus the mutants) | none |
| 1816-5 | info | **Two doc/text nits, not defects.** The test file's header still describes only the message-READ guard (KS-1802), not the logger guard. The docs section number `114` will collide with #1815's after a renumber (by design). | test header lines 1-4; docs | READ ONLY | optional |

### #1816 TESTED (HOW, with the FAIL condition each carried)

- **Diff read against KS-1818 and KS-1817, every changed line,** with the loop around it. R4 expects 200 with `failed: 14` and the logger called 14 times (FAIL: constant 500 or a wrong count). R5 expects 13 created and 1 failed when one insert's log line throws (FAIL: the loop stops). R6 filters to calls with the message `'Demo user seed failed'` and requires 14 of them, the first with `james.wilson@ox.ac.uk` and the fallback text, and every call carrying the fallback.
- **Spark gate:** HEAD 9/0, BASE product code 7/2 (red = R4, R5 exactly).
- **Whole originate suite at the head** (jest, `--config jest.config.js`): **150 files, 1821 tests, 1821 pass, 0 fail, 0 pending.** Matches the seat. Develop's #1813 changed only anchoring files, so the originate result does not depend on the merge. FAIL: any red. None.
- **Mutants (mine, each alone, restored, sha256 equal every time), on the merged-code tree:**

  | mutant | change planted | red cells |
  |---|---|---|
  | U0 | guard removed (bare call) | R4, R5 (2 of 9) |
  | X3 | helper catch returns `undefined` | R6 only |
  | Y1 | fallback text changed | R6 only |
  | Y2 | log message text changed | R6, C1 |
  | Y3 | `email` key dropped from the log context | R6, C1 |
  | Y4 | guard catch rethrows | R4, R5 |
  | Y5 | guard catch `break`s the loop | R4, R5 |
  | Y6b | log call dropped, helper still called | R4, R6, C1 |
  | Y8 | helper catch returns `''` | R6 only |
  | Y9 | `failed++` dropped | 6 (R1-R5, C1) |
  | Y7 | `String()` around the helper | **none (survives, 1816-1)** |
  | Y10 | helper falls back to `String(err)` when message-less | **none (survives, 1816-1)** |

  Y6 (first cut: an empty `try {}`) failed ts-jest type-checking (an unused import), so it is invalid, not a kill; I re-cut it as Y6b. Controls: baseline 9/0 before the run; U0 shows the harness goes red.
- **Docs:** rc 0 at both heads; planted defect gave rc 1 on all four head files (see #1815). The figures match: 6 of 6 at base, 2 of 8 then 8 of 8 then 9 of 9, 150 / 1818 to 1821, X3 1 of 9. Section number `114`.
- **Linear KS-1818 and KS-1817:** read; the claims match the diff, and KS-1817's own text names X3 (killed here) and X5 (not).

---

## Merge onto develop `203734468019` (merge-tree, `git_checks.out`)

| PR | rc | conflicts |
|---|---|---|
| #1815 | 1 | the two `Projects Documents/*.html` files only (end-of-file append) |
| #1816 | 1 | the same two files only |

**All code files merge clean for both.** The code trees I tested (develop plus each PR's code files) are built from those clean paths. After both are in, only the docs need hand merging; the pair's code is disjoint (anchoring versus originate).
**Order:** #1816, then #1815 (see BLUF for the renumber count).

## NOT TESTED (Rule 2)

- **No stack and no box:** no running gateway, originate or anchoring; no request against any host; no Docker; no Postgres. The logger, the database and the anchoring routes are mocked or source-read; a real logger or serialiser was not driven (1816). The by-id route itself was not driven either (1815 pins source text, as the PR says).
- **A both-PRs merged tree** was not run as one tree (the code is disjoint and each was tested on develop). My attempt at a pair merge-tree in `git_checks.sh` errored (`must give exactly one tree`, a script fault); the file lists show the disjointness.
- **The seat's own mutant lists** were not re-run as such; I ran X16, X8, X3 and my own extras.
- **Docs after the hand merge** (renumber and keep-both) were not checked, because the merge is the author's.
- **Not run at all:** the integration suites, the four platform suites (Schemathesis, Akto, Playwright, k6), the pre-push hook legs, `tsc` and eslint over the changed files, Node 24 (host Node is v26.8.1, not an LTS line), and the `spark_review.py` LLM half.
- **The PR bodies on GitHub** were not read (no `gh`); I relied on the Linear comments.

## Instrument errors (mine)

1. **Spark `--node-modules` pointed at the wrong directory** for the first #1815 run; exit 0 with 0 passed 0 failed (see Spark half). Re-run valid.
2. **`jest` without `--config`** failed in my first full-suite and targeted run (no config found from `--rootDir`); I added `--config <pkg>/jest.config.js`. The failed log is kept as `full_originate_wt-1816.try1_noconfig.log`.
3. **The first verb-list mutant pass** read 0 verbs (my regex expected a literal array); I derived the 25 verbs from the R6 cell titles instead (`mut1815b.py`).
4. **Pair merge-tree** in `git_checks.sh` errored (above).
5. **Mutant Y6** did not compile (above); re-cut as Y6b.

Evidence is in `evidence/` beside this file: `spark_1815.out`, `spark_1816.out`, `mut1815.out`, `mut1815b.out`, `mut1816.out`, `mut1816b.out`, `full_*.json/log`, `git_checks.out`, `docs_check.log`, `linear.out`, `merged_*_targeted.out`, `lsremote_*.out`.

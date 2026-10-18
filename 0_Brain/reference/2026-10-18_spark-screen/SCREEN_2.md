# Spark screen, part 2 (2026-10-18 late evening): 3 briefs, 3 rounds, 3 PASS

Written 2026-10-18 ~23:2x AEDT by a Spark brief-writing sub-agent for Wednesday. Secuura only. Develop tip read by me: `git -C <Blockchain checkout> ls-remote origin refs/heads/develop` = `1f73d7ac8cc17add318601c6c572bcace3d5a596` (re-read at 23:13, unmoved). Every brief is pinned to it; line text quoted from `git show <tip>:<path>` (read in the Spark cache clone after fetching develop there, which is what round.sh does itself; the Secuura checkout got `ls-remote` only). Nothing held, raised, pushed, merged, or written to Linear. Nothing deleted.

## Result

| # | ticket / part | brief dir (`local-model/night/briefs/`) | mode / rung | edit points | control | round | golden | model s · tokens | run dir (`local-model/runs/`) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | KS-1482 p1: `.githooks/pre-push` `diff --no-renames --name-only` at :129 and :143 + 2 RED cells (branch exists at remote; branch has upstream) in the ks998 judges-the-push suite | `ks_1482_p1` | bash_patch · 2 | 3 (2 product lines, 1 test hunk) | CONTROL-PASS 7/7, BYTE-IDENTICAL (`..._ks_1482_p1-control-r2`; r1 FAIL, see below) | **PASS** | TREE-IDENTICAL | 45.5 · 27499+1017 | `spark_secuura_2026-10-18_ks_1482_p1` |
| 2 | KS-1482 p2: the :252 new-branch site + 1 RED cell | `ks_1482_p2` | bash_patch · 2 | 2 (1 product line, 1 test hunk) | CONTROL-PASS 7/7, BYTE-IDENTICAL (`..._ks_1482_p2-control`, first control) | **PASS** | TREE-IDENTICAL | 36.6 · 26524+622 | `spark_secuura_2026-10-18_ks_1482_p2` |
| 3 | KS-1497 items 2+4: `prisma-generate.cjs` refuses a symlinked or non-directory `node_modules/.generate` ("generate:" message, exit 2) + NEW bash suite (5 RED, 2 CONTROL) | `ks_1497_p1` | bash_patch2 · 2 | 2 (1 pure-insertion product hunk, 1 new test file) | CONTROL-PASS 9/9, BYTE-IDENTICAL (`..._ks_1497_p1-control`, first control) | **PASS** | TREE-IDENTICAL | 42.0 · 12274+1673 | `spark_secuura_2026-10-18_ks_1497_p1` |

Checker verdict lines (from each run's `checker.out`):
- `ks_1482_p1`: `RESULT: PASS (7/7)`; B4 "fails at the untouched tip (rc=1, 2 FAIL line(s))", B5 "rc=0, 0 FAIL lines, 78 pass line(s))", B6 "no NEW failure after (14 suite(s))"; `SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)`, A2a hunks=3 ok=3 bad=0.
- `ks_1482_p2`: `RESULT: PASS (7/7)`; B4 "(rc=1, 1 FAIL line(s))", B5 "76 pass line(s)", B6 14 suites; `SPARK RESULT: PASS`, A2a hunks=2 ok=2.
- `ks_1497_p1`: `RESULT: PASS (9/9)`; B3x "declared=2 measured=2 ok=2 diff=0"; B4 "RED(rc 1, 5 FAIL)"; B5 "(7 pass)"; `SPARK RESULT: PASS`, A2a hunks=1 ok=1 skipped_newfile=1. (No B6 line was printed for the bash_patch2 round; I did not look into why.)

No FAIL, so no model/harness/brief classification of a round. One brief-defect control failure, fixed before any model run: `ks_1482_p1` control r1 FAIL at B3b ("must_change site(s) NOT changed by the script hunk: :252 ..."), cause: my `## Where` bullet for the site that belongs to the sibling brief carried bold (`**NOT in this brief**`), and the builder reads any `**` bullet that is not marked "(correct)" as must_change (`night/build_input.sh:470`, `tasks/bash_patch/build_bash_input.sh:79`). Fixed by dropping the bold in both briefs (the same text was in p2); control r2 PASS. Worth one README line: never bold a Where bullet that stays.

## Partition and counter

- Partition: none of the three briefs touches `verification.ts`, the KS-1619 p1/p2 test hunks, or KS-1490's bash_patch2 file. Files touched: `.githooks/pre-push`, `ks998_pre_push_judges_the_push.test.sh`, `prisma-generate.cjs`, one new `ks1497_*.test.sh`. I did NOT check open PRs or live seats' unpushed work for overlap (unmeasured).
- Counter: every ticket got its original brief only; no rebrief used.

## What each brief carries (read these at source before holding)

- KS-1482 (ticket text read from the 10-18 screen's saved Linear dump, `ks.json`, not a fresh Linear call): the ticket's `:80`/`:184` are stale; at the tip the three `git diff --name-only` calls that build the changed set are `:129`, `:143`, `:252` (`:87` is a comment). The edit adds `--no-renames` after `diff` at each. Cells: three scenarios, one per base path of `_judge_ref` (mirroring the suite's own SC18 / SC18b / SC18c), each doing `git mv Blockchain/Dev/file.txt docs/moved.txt`, committing, pushing the checked-out commit, and asserting rc 0 and exactly one `[preflight] ran`. Measured by me in a scratch clone with the suite's own `HOOK_SH` override: p1 vs the TIP hook 76 passed / 2 failed (both RED cells `want '0/1', got '0/0'`), vs the edited hook 78/0; p2 vs tip 75/1, edited 76/0. Both goldens applied together to one tree apply cleanly and give 80 passed / 0 failed (measured). Each CONTROL cell asserts the trap is real in the fixture (the rename shows only `docs/moved.txt`, 0 `^Blockchain/Dev/` lines). Split p1/p2 only to keep each brief at 3 edit points or fewer; their test hunks are in different places of the suite (p1 appended after SC21, p2 after SC17).
- KS-1497 items 2 and 4: one `lstat` guard inserted between `:67` and `:68`: ENOENT passes, symlink and non-directory call the existing `fail()` (exit 2, "generate: ..." message); a real stale directory is still reused and removed. Items 1, 3, 5, 6 of the ticket are untouched and stated as narrowing in the brief. The new suite drives the real script with the script's own test hooks (`PRISMA_GENERATE_SVC_DIR`, `PRISMA_SCHEMA_SRC`) against a fixture with a stub `prisma` CLI; `PRISMA_GENERATE_CJS` lets it point at another copy. Measured vs the TIP script: 2 passed, 5 failed (symlink rc `got '0'`, target holds 1 stray file, file case rc `got '1'`); vs edited: 7/0 (node v24.7.0). The BYTE-IDENTICAL golden was ordered product-first, test-second.

## NOT done / NOT tested

- **Candidate (c), KS-1620 / KS-1621 / KS-1622, NOT briefed.** The Spark README names no Linear reader, and the commission allowed reading them only if Wednesday's tooling already does so per the README; so I skipped them without reading them and make no claim about their cells. (The earlier screen sourced a Blockchain `.env` key by hand; I did not.) A seat with a Linear reader can brief them; the p1 briefs of today are templates.
- I stopped at 3 rounds of the 5 allowed because no further candidate was briefable inside the commission.
- No hold, no raise, no REVIEW.md. TREE-IDENTICAL means the model's patch builds the same tree as my golden; I did not read the three model patches line by line. Wednesday reads each at source. Audit-surface note: KS-1482 changes the push gate's changed-set (a tooling gate, not an auth line), KS-1497 is developer tooling.
- Not run by hand: the KS-1305 vitest suites that also drive `prisma-generate.cjs` (no node_modules in the scratch clone; read for fixture shape only); the real `prisma generate`; the systemTest formatting gate's share of the renamed-out list; `systemTest/playwright/.githooks/pre-push` (a different file, not read for this).
- Not tested: a dangling symlink for KS-1497 (same branch as a live link, no cell); heavy-edit moves below git's similarity threshold (already listed as add plus delete).
- Open PR census was not redone; develop was read at 22:4x and 23:13 and was unmoved both times.

## Queue

Queue ends empty. WHY (also appended to `spark/queue.md`): 3 briefed, 3 PASS; the only remaining named candidates (KS-1620/1621/1622) need a Linear read this sub-agent was not given.

## Files written

Briefs: `night/briefs/ks_1482_p1/`, `ks_1482_p2/`, `ks_1497_p1/` (each `KS-<n>.md`, `golden.diff`, `spark.pins`; sha256/16 of the briefs `5227bdc07601e39b`, `f04cca179b2d73bc`, `e3579ae445497190`). `spark/queue.md` (3 provenance comments + 3 lines, consumed by queue.sh, + the WHY line), `spark/done.md` (3 rows by queue.sh), `runs/` and `spark/state/dry/` and `spark/cache/` (round.sh's own, incl. the fetch of develop into the cache), this file. Scratch (not durable): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/spark_drafter/` (clone, golden generators `gold1482.py` / `gold1497.py`, brief generators `mkbrief1482.py` / `mkbrief1497.py`, `prove.sh`, logs).

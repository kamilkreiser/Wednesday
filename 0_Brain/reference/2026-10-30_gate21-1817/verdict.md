# QA GATE 21 - Secuura/Blockchain PR #1817 (KS-1830, tier 2: tests and docs only, zero product bytes)

TIER 2 because the PR is test-only: 12 lines in one test file plus two documentation blocks. No product file is touched, so the gate is mutation-based (does the new test go red when the target line is tampered) and not a behaviour review.

PR head `e6ee492d18f1e324e14801af9871b7c8c7a75a37` (one commit). Read at origin by ls-remote at the start and at the end of the gate, equal both times, equal to the brief. PR base (merge-base) `203734468019feaf44428975b10cf5f799483187`. **Develop has moved on to `1fa9f9db802b4d9b6f435ac506228a511e614254`** (the known #1816 merge). Findings only: I pushed, commented, merged and mailed nothing, and wrote nothing under `!CODING`. I read the node_modules and `packages/shared` of the `s-r64-ks1830` worktree (copy only, nothing run or written there). My clone is `scratchpad/gate21/repo` (made at a non-existent path, toplevel asserted equal before any fetch; origin and `core.sshCommand` set to the Secuura values; only `refs/pull/1817/head` and `develop` fetched). No background process was started, so no PID needed stopping.

## BLUF

- **VERDICT: GO WITH NOTES.** 0 blocker, 0 major, 1 minor, 5 info. **No fix-before-merge item** except the docs renumber at merge-prep (already accepted).
- **Zero product bytes.** `git diff --stat develop...head` lists exactly 3 files, +51/-0 (12 + 20 + 19). `anchorSchema.ts` and `index.ts` are absent.
- **Every author claim about the red-first cells reproduces:** `+` alone: exactly 2 of 143 red (actorDid + orgDid plus-sign refusals). `/` alone: exactly 2 (the slash refusals). Both: exactly 4. File green 143 of 143. Before the PR the same three tampers pass 135 of 135 on the base file.
- **One claim did not reproduce:** the whole anchoring suite counts match (509 base, 517 head) but **the "1 failure" does not**: in my environment it is 509/509 and 517/517, 0 failures, including the `threadTokenMint ... deterministic per-seed policyId` cell, which passes (1817-1).
- **Merge onto develop `1fa9f9db`:** merge-tree rc 1, **conflicts in the two `Projects Documents/*.html` files only**. Code merges clean. Develop already holds `<h2>114.` (#1816), so this PR's `114` must be renumbered (to 115, or later if #1815 lands first).

## Verdict table

| PR | verdict | blocker | major | minor | info | fix-before-merge |
|---|---|---|---|---|---|---|
| #1817 @ e6ee492d | **GO WITH NOTES** | 0 | 0 | 1 | 5 | none (docs renumber at prep) |

## Findings

| id | sev | finding | instrument / evidence | evidence class | FIX-BEFORE-MERGE |
|---|---|---|---|---|---|
| 1817-1 | **minor** | **The docs state one environment-dependent figure as a fixed fact.** Both docs say the whole suite is "509 cells (508 pass, 1 fail)" and "517 (516 pass, 1 failed)", "the same 1 pre-existing failure ... (the threadTokenMint cell)". The cell totals reproduce exactly (509 and 517; 36 files each), but on my host the `threadTokenMint ... deterministic per-seed policyId` cell **passes at both trees** (509/509 and 517/517, rc 0). So the failure is host-dependent (gate 20 saw it fail, I did not). The docs make no claim it is stable. Nothing the PR adds depends on it. | `evidence/suite_head.json`, `suite_base.json` (cell status `passed` for the policyId test); doc 114.1 and 114.4, cheat-sheet "Running the cells" and "Figures" | MEASURED | no (wording at prep, optional: say "1 pre-existing host-dependent failure on the author's host") |
| 1817-2 | info | **Mutants beyond the author's: the new cells kill exactly what they claim and no more.** Killed: `+` and `/` (2 each), `+/` (4), a range `*-/` that happens to contain both (4), `=` (2, the older padding cells), `.+` (10), `[^\s]+` (6), a shape check that stops after the first character (14 red: 5 older refusal rows x 2 fields + the 4 new cells), a `$`-only anchor (71). **Survived, 143 of 143 green:** `!`, `*`, `@`, `#`, the `A-z` range (adds `[ \ ] ^ _` and the backtick), and a trailing optional `\+?` at the END of the payload. These are outside E1/E2's scope, and doc 114.3 says so ("not claimed ... any character other than `+` and `/`"). Note the end-position plus: the row inserts at offset 40 only, so a plus at the end is not pinned. | `evidence/mutants.out`, `mut_*.json` | MEASURED | no (possible follow-up ticket for a class-wide ASCII sweep) |
| 1817-3 | info | **The 12 test lines read correctly.** Two `SHAPE_REFUSALS` rows insert exactly one `+` / one `/` at offset 40 of `REALISTIC_DID_JWK` (inside the payload; `did:jwk:` is 8 chars). Titles are unique per field. `label.includes('plus sign')` and `includes('slash')` each match exactly one row (no other label contains either word). Each control asserts `row.replace(ch,'') === REALISTIC_DID_JWK` and `split(ch).length === 2`, so a missing row (`undefined`) fails and a drifting row fails. No cross-contamination: the plus-only tamper reddens only plus cells and the slash-only tamper only slash cells, so neither row holds the other character. The controls are product-independent and run once per field (identical assertion twice), harmless. | diff read end to end; `mut_T_plus.json`, `mut_T_slash.json` | MEASURED | no |
| 1817-4 | info | **Docs blocks are additions only and valid.** `git diff --numstat`: 20/0 and 19/0. `html_docs_check.mjs` rc 0 on both head files; **positive control:** a 12-sentence `<p>` outside a table in a scratch copy gives rc 1 ("prose outside a table"). Figures in the blocks match what I measured (143, 135 at base, +8 = 4 RED + 4 controls, 2/2/4, 509/517). The `tsc` claim also reproduces: the package tsconfig excludes `src/__tests__` (a planted type error gave rc 0 there), so I used a tsconfig that includes it: 0 errors, and a planted `const x: number = "s"` gives rc 2. | `docs_check.out`, `docs_check_plant.out`, `tsc_withtests*.out` | MEASURED | no |
| 1817-5 | info | **Docs section collision, known and accepted.** Develop `1fa9f9db` has `<h2>114.` (#1816) in the flow-diagrams doc; this PR adds `<h2>114.` too. merge-tree rc 1 on exactly the two docs; the code file merges clean. Renumber at merge-prep. | `merge_tree.out` | MEASURED | docs renumber only |
| 1817-6 | info | **Instrument notes for Spark.** (a) `spark_gate.sh` exited 0 again when every file died (first run: `ERR_MODULE_NOT_FOUND` at the `--node-modules` dir, 0 passed 0 failed, `files_failed` 1 = `files` 1). The directory had to be named `node_modules`. The known defect, still unfixed. (b) It resolves `origin/develop` before bare `develop` when both exist, so the BASE it reports is `1fa9f9db`; the merge-base is still `20373446`, so the result is the same here. (c) A test-only PR is green on BASE product code (143/143), as expected: the red-proof is the tamper table below. | `spark_1817.try1_facts.json`, `spark_1817.out` | MEASURED | no |

## Spark half (deterministic, run FIRST, bare base ref `develop`; an input, not my verdict)

- Run 1: exit 0 but **dead**: HEAD `files_failed 1`, `passed 0 failed 0`, tail `ERR_MODULE_NOT_FOUND Cannot find package '@vitest/utils'` (my node_modules copy sat in a directory not named `node_modules`). I read the output, not the rc. Kept as `evidence/spark_1817.try1_facts.json`.
- Run 2 (fixed, valid): exit 0. Head `e6ee492d` (tip), merge-base `20373446`, base tip `1fa9f9db`, diff 3 files +51/-0. **Targeted HEAD 143 pass / 0 fail; BASE product code 143 / 0.** Positive control that the instrument can show red: the same runner went to 14, 71 and 2 reds under my tampers.
- No `spark_review.py` LLM verdict was run (not requested).

## TESTED (how, with the FAIL condition each carried)

1. **Diff scope.** `git diff --stat` and `--numstat` of `develop...pr/1817`: 3 files, 12/20/19 added, 0 deleted; `grep -c anchorSchema|index.ts` = 0. FAIL: any product file. None.
2. **RED-FIRST, each tamper alone** at `anchorSchema.ts:124` (`DID_PATTERN` class), exact-once replace of the regex text, run, restore by content, whole-file sha256 read back equal (`ca46ef18...` before and after, checked every run):

   | tamper | red cells |
   |---|---|
   | baseline (untouched) | 0 of 143 |
   | `+` added to the class | 2: actorDid and orgDid "refuses a plus sign inside the payload" |
   | `/` added | 2: actorDid and orgDid "refuses a slash inside the payload" |
   | `+` and `/` | 4: those four |

   The same three against the **base** file and base test file: 135 of 135 each (so before the PR nothing noticed). Positive control: the baseline is green and the tampers go red under the same harness.
3. **Whole anchoring suite.** `vitest run` over the package at the PR head and at pure `203734468019`: **head 517/517, base 509/509**, 118 suites, rc 0 at both. +8 cells (4 RED + 4 controls) matches. FAIL: any red. None (see 1817-1 for the author's 1 failure that did not appear).
4. **Independent mutants (mine, beyond the author's).** 15 regex variants (list in 1817-2), each planted alone and restored sha256-equal (`restored sha equal: True`). Zero survivors are real: the same harness reddened the others.
5. **Docs:** additions only, `html_docs_check.mjs` rc 0 on both with a planted-defect control rc 1, figures cross-checked, `tsc` with the test file in the program (control rc 2).
6. **Merge onto develop:** `git merge-tree --write-tree` rc 1, conflicted paths = the two docs only.

## NOT TESTED

- The anchoring integration suites, the four platform suites (Schemathesis, Akto, Playwright, k6), the pre-push hook legs, eslint, Node 24 (host Node is v26.8.1, not an LTS line), any running stack, Docker or database. The cells call the exported schema, so none is needed for the property.
- A hand-merged docs state (the renumber is the author's).
- The PR body on GitHub (no `gh`); the Linear ticket KS-1830 was not read in this gate (the brief carried the claims).
- The E2-by-script insertion path itself: I judged the resulting file, not how it was produced; the file content is what the diff shows and what ran.
- `spark_review.py` (LLM half).

## Instrument errors (mine)

1. First Spark run dead (node_modules dir name); re-run valid.
2. My base-file tamper script first overwrote the head tamper JSONs of the same names (a copy-paste of the runner); I kept the base results as `base_file_*.json` and re-ran the three head tampers (`mutants_head_rerun.out`, same reds: 2/2/4).
3. The first whole-suite run lacked `packages/shared` (workspace symlink), so 4 files failed to load; fixed by copying the built `packages/shared` beside the node_modules copy; the 517/509 figures above are from the fixed runs.

Evidence in `evidence/` beside this file: `spark_1817.out`, `spark_facts.json`, `spark_1817.try1_facts.json`, `mutants.out`, `mut_*.json`, `mutants_base.out`, `base_file_*.json`, `suite_head.json`, `suite_base.json`, `merge_tree.out`, `docs_check*.out`, `tsc*.out`, `lsremote_end.out`, and the scripts `mut.py`, `run.sh`, `summ.py`.

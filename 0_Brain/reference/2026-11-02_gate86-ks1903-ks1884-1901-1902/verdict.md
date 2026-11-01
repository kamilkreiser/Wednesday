# QA Gate 86 verdict (batched, tier 2): Secuura/Distributed_Secuura PR 1901 (KS-1903) and PR 1902 (KS-1884)

## BLUF
- **PR 1901 (KS-1903, check-dockerfile-non-root.sh): GO WITH NOTES.** The 4-line product change does what it says. Red at base 7 pass / 4 fail by assertion, 11/0 at head; behaviour matrix of 29 Dockerfile inputs shows exactly the claimed exit 0 -> 1 flips and nothing else; the real tree (35 Dockerfiles, no colon) is OK at base and head; run-code-guards.sh is GREEN at head (13 guards). Nothing to fix before merge; one cheap optional cell (G86-1901-F1).
- **PR 1902 (KS-1884, manifest_readers_agree stderr): GO WITH NOTES.** The product-side (test-file) change is correct and safe: temp dir by `mktemp -d` + EXIT trap (verified removed), passing output byte-identical to base (24/0 both), and a real failure (npx missing) now shows `writer stderr: env: npx: No such file or directory` where base shows nothing. The 3 survivors the author reports are **real gaps**, and there are more than three (9 of 13 of my mutants survive). A strengthened suite (+7 cells, about 25 lines, evidence/manifest_readers_agree_stderr.strengthened.test.sh) kills 12 of 13. Not blocking (test-only, the survivors are disclosed in the fragment), but **I recommend folding those cells in before merge since they are cheap** (G86-1902-F1).

## Heads
- START (logs/head_start.log, 14:27Z): PR 1901 `15fbdbdaa2986d2014bc3ec5158b4235a30078db`, PR 1902 `6b3c9eaa7410d2cc258c8e13f4fa7aa65455d70e`, both one commit on develop `8126b22bd5aa505be194996c9301b6e1ced5583e` (merge-base for both); develop now `8afcf256ed5fb38d05f7273e08e1b912446bac5c`. All match EXPECTED.
- END (logs/head_end.log, 14:43Z, ls-remote): all three unchanged; worktree HEADs identical; worktrees clean (status 0 lines). Nothing pushed, commented or written outside WORKDIR and /private/tmp/gate86_spark.
- Diffstat as claimed: 1901 4 files +105/-1 (2 M, 2 A); 1902 4 files +130/-4 (1 M, 3 A) (logs/diffstat_*.log). Modes: manifest_readers_agree.test.sh 100755 -> 100755; every new file 100644, as its sibling suites; check-dockerfile-non-root.sh and its suite 100644 both sides. Product vs test split: 1901 has one product file (the script, 4 lines) + the suite + 2 fragments; 1902 is test-only (the changed test + new suite + 2 fragments).

## FINDINGS

### PR 1901
- **G86-1901-F1 (LOW, test strength, optional)** The author's note is right that `0:1000` and `Root:Root` have no cell. Measured consequence: my mutant M13 (lowercase only the literal `ROOT`, via `sed 's/ROOT/root/'`) SURVIVES 11/0 (logs/mut1901_M13*.log). Mixed case `Root` is therefore unpinned. Cheap fix: one cell `USER Root:Root` -> exit 1 (and optionally `0:1000`). The product lines are correct for both (matrix, logs/1901_matrix_head.log).
- **G86-1901-F2 (INFO, pre-existing, not this PR)** Still read as non-root and pass: `USER 00`, `USER "root"` (quoted). Docker treats both as root. Lower-case `user root` is not recognised as a USER instruction (grep is case-sensitive), giving "NO USER directive" (fails closed). Worth a follow-up ticket; no change to what the PR claims.
- **G86-1901-F3 (INFO, side effect)** `USER :1000` (empty user) went exit 0 -> 1 and prints "has NO USER directive": the strip empties the value. Fails closed, message slightly misleading; an empty user is not valid Dockerfile anyway. Worth one line in the PR body.
- **G86-1901-F4 (INFO)** Lowercasing makes the guard stricter than the runtime: Linux user lookup is case-sensitive, so `USER ROOT` fails at container start rather than running as root. Fail-closed, defensible, and the PR says so as a behaviour change.
- No HIGH/MEDIUM. Nothing blocks.

### PR 1902
- **G86-1902-F1 (MEDIUM-LOW, test strength; fix recommended before merge, not blocking)** The new suite cannot tell which driver lost its stderr file. Its stub prints the same `STUB-NPX-NOISE` whichever of the three npx drivers ran, so cell 1 passes while any one of them is back on `/dev/null` (mutants A, B, C survive). It also never checks labels, that stderr is not printed on a passing case (F; cell 4 inspects only lines starting `ok `, and the stderr lines are on separate lines), that stderr does not leak into the answer (I), that drivers do not share one file (J), or that the temp dir is removed (K). 9 of my 13 mutants survive (table below), versus 3 of 7 for the author. Real exposure: a driver regressing to `/dev/null` is the exact defect KS-1884 fixes and would go unnoticed.
  - Cost of closing it: about 25 lines, 7 cells, proven by mutation. (1) stub noise carries `$*` so each driver's noise names its own source; (2) per-driver cells `^ +writer stderr: .*fixtures/manifest.ts`, same for playwright (`config/actorManifest.ts`), performance (`runner/actor_manifest.ts`), schemathesis (`STUB-PY-NOISE`); (3) an awk cell: no `stderr:` line directly after an `ok ` line; (4) the silent case keeps `writer='' playwright='' performance='' schemathesis=''`; (5) run the silent case with `TMPDIR=$WORK/tmpd` and assert no `readers-agree.*` is left. Working copy with the cells: `evidence/manifest_readers_agree_stderr.strengthened.test.sh` (it is a scratch copy with the paths of the PR's suite; green on the head subject 11/0). Cells 1-3 of the author's suite are unchanged.
- **G86-1902-F2 (INFO)** A FAIL line is followed by every non-empty driver stderr file, including a driver that answered correctly but wrote warnings (tsx notices); and the same line repeats under every failing case (24 FAILs in the no-npx run, logs/1902_nonpx_1902.log). Verbose when everything is broken, harmless otherwise, and bounded by `head -c 400`.
- **G86-1902-F3 (INFO, measurement)** Truncation (`head -c 400`) is unpinned (mutant L survives even the strengthened suite); low value.
- No HIGH. Nothing blocks.

## PR 1901 per-check sections

1. **Diff exactly as claimed.** `git diff origin/develop...pr/1901` = the script +4 lines (comment, `last_user=${last_user%%:*}`, `last_user=$(printf '%s' "$last_user" | tr 'A-Z' 'a-z')`, blank), the suite +59/-1 (cells 5-11, count guard 4 -> 11), 2 fragments (logs/diffstat_1901.log). Both lines sit after the `tr -d '[:space:]'`; the comment strip runs before, so `0:0 # c` is handled (matrix).
2. **Red at base, green at head (own runs).** Head suite on base script: `7 passed, 4 failed`, failures cells 5, 6, 7, 10 by assertion, each "rc=0 out=OK - all 1 Dockerfile(s) drop root" (logs/1901_red_base.log). Head: `11 passed, 0 failed` (logs/1901_green_head.log, and inside the full runner). Matches the author. `bash -n` rc 0 on both files (logs/bash_n.log).
3. **Behaviour matrix, 29 inputs, base vs head** (scripts at /private/tmp/gate86_spark/matrix.sh; logs/1901_matrix_base.log, logs/1901_matrix_head.log). Flipped 0 -> 1: root:root, root:app, 0:0, 0:1000, ROOT, Root, Root:Root, root:, 0:0 # c, ROOT:ROOT (trailing space), Root:0, 0:root, tab-separated root:root, CRLF root:root, and `:1000` (see F3). Unchanged 0: app, app:root, app:app, 1000:1000, nobody:nogroup, App:APP, `${APP_USER}`, `$UID:0`, and the pre-existing gaps `00` and `"root"` (F2). Unchanged 1: root, 0. This confirms the author's three named flips and shows the rest are the same class.
4. **Census and the real tree.** 35 Dockerfiles, final USER values: secuura 16, nodejs 11, app 4, nginx 2, postgres 1, migrate 1; none has a colon (logs/1901_census.log). Script on the real tree: base rc 0 / head rc 0, both "OK - all 35 Dockerfile(s) drop root for runtime" (logs/1901_real_tree_*.log).
5. **run-code-guards.sh (guards every push).** At head: rc 0, "OK - 13 code guards passed", including the dockerfile line and check-script-portability (7 rules over 106 scripts) (logs/1901_code_guards_head.log); base rc 0 as well. The change keeps the guard GREEN.
6. **Runner.** `--list` 107 suites incl. the suite; `--check-unreached`: OK, all 107 reached (logs/runner_list_1901.log, runner_check_1901.log). Full runner at head: `104 passed, 1 failed, 2 skipped (of 107)` (logs/runner_full_1901.log). Not the author's 107/0/1, for the same environmental reasons as gate 83: `blockchain_testing_target_base_follows_the_slot.test.sh` is `FATAL: tsx not installed` (my fresh worktree has no node_modules; identical failure at base, logs/btb_base.log and btb_1901.log, rc 2) and `preflight_test_types_ratchet_leg` skips ("workspace install absent"); ks949 skip is the no-PostgreSQL skip. The PR's suite ran inside it: 11 passed, 0 failed. No new failure attributable to the PR.
7. **SKIP line format (G83-F1 check).** Neither PR adds a `SKIP` line (`grep SKIP` over both new/changed suites: none). The existing skip lines in the runner log (`SKIP — no PostgreSQL ...`, `SKIP — workspace install absent ...`) use the em dash and are counted by `run-shell-suites.sh:428`'s regex `^[[:space:]]*SKIP[[:space:]]*[-—]`. Nothing to flag.
8. **Mutants (scripts/mut1901.py, copies under /private/tmp/gate86_spark/mut1901, suite driven by CHECK_DOCKERFILE_NON_ROOT_SH; logs/mut1901_summary.log).** 13 mutants, 10 killed, 3 survived.
   | Mutant | Result |
   |---|---|
   | M1 no group strip | KILLED (8/3) |
   | M2 no lowercase | KILLED (10/1) |
   | M3 strip shortest suffix `%:*` | SURVIVED, equivalent for a one-colon value (the only valid form) |
   | M4 keep group `##*:` | KILLED (9/2) |
   | M5 lowercase before strip | SURVIVED, equivalent (order-independent) |
   | M6 `tr a-z a-z` (no-op) | KILLED |
   | M7 lowercase only A-M | KILLED |
   | M8 drop the `0` check | KILLED |
   | M9 drop the `root` check | KILLED (7/4) |
   | M10 strip only digit groups | KILLED |
   | M11 strip only `root:*` | KILLED |
   | M12 strip only `root:root`/`0:0` | KILLED |
   | M13 lowercase only the literal ROOT | SURVIVED, REAL gap (G86-1901-F1) |
   The author's "M5/M6 equivalent" corresponds to my M3 and M5 and both really are equivalent (reasoned above, and the suite agrees).
9. **Merge.** merge-tree of the head onto current develop 8afcf256: rc 0, tree `2d7f32e57508c837e8ed0c11bbc4a21cf414ec8d`, no conflicts (logs/merge_tree_1901.log). Nothing in 8126b22b..8afcf256 touches the script, the suite, or the fragments (logs, name-only check).
10. **Docs fragments.** `docs-fragments.mjs check` at head: rc 0, "flow 117 legacy + 50 new, cheat 112 legacy + 50 new; lint clean, render passes html_docs_check ... OK", 2 ADVISORY committed-page lags (by design, as gates 78/81/82/83) (logs/frag_clean_1901.log). Planted `<div>` on the KS-1903 flow fragment: rc 1, "tags are not balanced: <div> opened 2, closed 1", FAIL (logs/frag_planted_1901.log); restored from a copy, sha256 equal (RESTORE_OK). The fragment text matches what I measured (seven cells 5-11, 7/4 red, 4 of 6 mutants, 35 Dockerfiles and the USER histogram).

## PR 1902 per-check sections

1. **Diff exactly as claimed.** The changed test: four `2>/dev/null | tail -1` become `2>"$ERR_DIR/<driver>" | tail -1`; `ERR_DIR="$(mktemp -d "${TMPDIR:-/tmp}/readers-agree.XXXXXX")"` and `trap 'rm -rf "$ERR_DIR"' EXIT` added; the FAIL branch loops over the four labels printing `head -c 400 | tr '\n' ' '` of each non-empty file (logs/diffstat_1902.log; diff read in full). `+15/-4` there, new suite 77 lines. The `trap` is the only trap in the subject (no overwrite). The new suite is `100644` like its siblings and runs under `bash <file>` so no execute bit is needed.
2. **Temp files and leaks.** `mktemp -d` honours TMPDIR; with `TMPDIR=/private/tmp/gate86_spark/tmp_head` a full run left no `readers-agree.*` (only tsx's own caches) (logs/1902_full_head.log). Passing output is **byte-identical** to base: `diff` of the two full logs is empty; 24 passed, 0 failed at base and head; no line contains "stderr" (logs/1902_full_base.log, 1902_full_head.log). Real failure demo: with `PATH=/usr/bin:/bin` (no npx) base prints `writer='' playwright='' performance='' schemathesis='ERROR'` and nothing else; head adds `writer stderr: env: npx: No such file or directory` and the same for playwright and performance (logs/1902_nonpx_base.log vs 1902_nonpx_1902.log). That is the whole value of the PR, observed on real drivers.
3. **Red at base, green at head (own runs).** New suite against the base subject (`MANIFEST_READERS_AGREE_SH=base copy`): `2 passed, 2 failed`, cells 1 and 2 fail by assertion (logs/1902_new_suite_on_base.log). Head: `4 passed, 0 failed`, three runs, rc 0 each (logs/1902_new_suite_head_1..3.log). The whole affected suite (`manifest_readers_agree.test.sh`, real drivers via npx/tsx and python3) is 24/0 at base and head. `bash -n` rc 0 on both.
4. **Runner.** `--list` 108 suites incl. `manifest_readers_agree_stderr.test.sh`; `--check-unreached` OK, 108 reached (logs/runner_list_1902.log, runner_check_1902.log). Full runner at head: `105 passed, 1 failed, 2 skipped (of 108)` (logs/runner_full_1902.log); the same environmental failure and skips as PR 1901 (tsx / workspace install absent), the new suite ran inside it (cells printed PASS). Note both full runners ran concurrently on one machine; nothing in the results suggests interference, and the one failure reproduces alone at base.
5. **SKIP format.** No SKIP line in either new/changed suite; see PR 1901 section 7.
6. **Mutants (scripts/mut1902.py; copies under /private/tmp/gate86_spark/mut1902; logs/mut1902_summary.log and mut1902_summary_strengthened.log).** The PR's suite against the mutated subject copy, then the strengthened suite.
   | Mutant | PR suite | Strengthened |
   |---|---|---|
   | A writer back to /dev/null | SURVIVED | KILLED |
   | B playwright back to /dev/null | SURVIVED | KILLED |
   | C performance back to /dev/null | SURVIVED | KILLED |
   | D schemathesis back to /dev/null | KILLED | KILLED |
   | E all four back to /dev/null | KILLED | KILLED |
   | F stderr printed under a passing case | SURVIVED | KILLED |
   | G print loop cut to writer | KILLED | KILLED |
   | H non-empty test inverted | KILLED | KILLED |
   | I stderr merged into stdout (`2>&1`, noise becomes the answer) | SURVIVED | KILLED |
   | J playwright shares writer's file | SURVIVED | KILLED |
   | K trap removed (temp dir leaked) | SURVIVED | KILLED |
   | L no 400-byte cap | SURVIVED | SURVIVED |
   | M label dropped from the stderr line | SURVIVED | KILLED |
   PR suite: 4 of 13 killed (author: 4 of 7, the same three A/B/C/F gaps plus the five more I added). Strengthened: 12 of 13. L is a cap on length and not worth a cell.
   **The 3 survivors the author lists are real gaps**: a driver regressing to `/dev/null` would go unnoticed for writer, playwright and performance (any one), because the stub's noise is identical for all three. Cost per driver: one `grep` cell on a per-driver marker, 3 lines each once the stub puts `$*` in its noise (the drivers' `-e` sources are already distinct: `fixtures/manifest.ts`, `config/actorManifest.ts`, `runner/actor_manifest.ts`).
7. **Merge.** merge-tree onto develop 8afcf256: rc 0, tree `1b28e414b3e165f3394a1e2be1c9f81aff4f11e7` (logs/merge_tree_1902.log). Drift 8126b22b..8afcf256 does not touch manifest_readers_agree*.
8. **Docs fragments.** At head: rc 0, "flow 117 legacy + 50 new ... OK", the same 2 ADVISORY lags (logs/frag_clean_1902.log). Planted `<div>`: rc 1, "tags are not balanced: <div> opened 2, closed 1", FAIL; restored, sha256 equal (logs/frag_planted_1902.log). The fragment accurately states the 4/7 mutants and the 3 survivors, so the PR is honest about the gap.

## Both PRs together
- The two diffs share **no file** (`comm -12` of the name-only lists is empty). merge-tree of 1902 onto (develop 8afcf256 + 1901 merged, scratch commit `0673a6a6...` made with commit-tree in the gate clone only): rc 0, tree `afef20c3bc89ad3a0ce5835ab5235668c789fd03`, no conflicts (logs/merge_tree_1902_on_1901.log). The fragments have distinct names. Merge order does not matter.

## Spark shadow calibration
Evidence: evidence/spark_shadow_1901/, evidence/spark_shadow_1902/ (facts.json, targeted logs, prompt, raw, review.json). spark_gate.sh ran the suites at head and on base product code; spark_review.py ran once per PR (1901 needed a second attempt after a repetition abort; both valid). PR bodies were not fetched; I supplied the coordinator's claims as the body (evidence/pr_body_*.md).
- **PR 1901:** shadow targeted: head 11 passed 0 failed, base 7 passed 4 failed. This reproduces my red-first exactly (the suite is a test+product pair and the product is the only changed code, so the shadow base is a true red here). Spark verdict **GO WITH NOTES**, 5 Notes. Match with mine: verdict yes. Recall of my substantive findings: F1 (mixed-case gap) missed, F2 missed, F3 missed, F4 missed (0 of 4, all of low severity). Its notes only flag claims "not in facts.json" (census, mutants, shell-suite numbers) as unmeasured; true and I measured them (census, run-code-guards and the matrix are my section 3-5). Note 2 (4 of 11) is a confusion of its own, harmless. Quotes found in input: false for the notes sampled.
- **PR 1902:** shadow targeted: head 28 passed, base **28** passed (24 + 4). That is an artefact, not a finding about the PR: the shadow runs head's *test files* against base *product*, and here the changed file IS a test file (manifest_readers_agree.test.sh), which is also the subject of the new suite, so the base run uses the head subject. It therefore cannot show the red (my real red-first is 2/2 failing against the base subject copy, section 3). Spark took the artefact at face value in notes 1 and 4 ("claimed red-first not corroborated"): **two false positives, both caused by the gate's design for test-only PRs; worth a shadow_facts.py fix (run the new suite against the merge-base copy of the named subject) or a caution in the prompt.** Spark verdict **GO WITH NOTES**, 4 Notes. Match with mine: verdict yes. Recall: F1 partly hit (note 2: cell 4 "weaker than the claim" is the real cell-4 gap; it did not find the A/B/C survivors or I/J/K/M), F2 and F3 not raised. Note 3 (trap only on normal exit) is wrong on a point of bash: an EXIT trap also fires on `exit` after an error and on SIGINT/SIGTERM-handled exit; kill -9 only skips it, which is inherent. One note in three is accurate.
- Net: Spark agrees on the verdict and adds no finding I lacked; its main risk is the false red on test-only PRs.

## Notes for the PR body

### PR 1901
1. State the new edge: `USER :1000` now exits 1 (message "has NO USER directive", base printed OK).
2. Add one cell `USER Root:Root` (and optionally `0:1000`): the body names both as behaviour changes but no cell pins them, and mutant M13 (lowercase only literal ROOT) survives.
3. Confirmed numbers: 7/4 red at base, 11/0 at head, 35 Dockerfiles none with a colon, run-code-guards 13 green, merge-tree clean. The "runner 107/0/1" was not reproduced here (104/1/2 of 107); the 1 fail and 1 extra skip are environmental (no node_modules in a fresh worktree) and identical at base.
4. Follow-up ticket candidates (not this PR): `USER 00`, quoted `USER "root"`, and lower-case `user` instruction are not handled.

### PR 1902
1. Strengthen the new suite with the per-driver and negative cells (evidence/manifest_readers_agree_stderr.strengthened.test.sh): turns 9 surviving mutants of 13 into 1; about 25 lines; the stub change is `echo "STUB-NPX-NOISE tsx failed to start $*"`.
2. Fix the mutant count in the fragment accordingly (author 4 of 7; with the extra five I tried it is 4 of 13 before the cells).
3. Confirmed numbers: 24/0 before and after with real drivers and identical pass output; new suite 2 pass / 2 fail at base by assertion, 4/0 at head (3 runs); `--check-unreached` OK on 108. The "runner 107/0/1" was not reproduced (105/1/2 of 108, environmental, same one failure at base).
4. Optional: say in the PR body that a FAIL line will list stderr for any non-empty driver file, including warnings from a driver that answered correctly.

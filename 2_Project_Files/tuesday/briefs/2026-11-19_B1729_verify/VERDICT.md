GATE B1729: GO WITH FINDINGS @ 2ec6937 (delta over cd019f3) on main 37fb1bc

This is a G2 round-2 delta gate run on Opus 5.5, independent of the builder. Every row below was measured by this gate on Thu 19 Nov 2026, between 10:00:04 and 10:07:33 AEDT (clocks from `date`). The round-1 verdict (B1727, GO WITH FINDINGS on cd019f38) stands for everything this delta does not change. Its F1 to F4 are carried over unchanged, because this delta touches none of those paths.

Work folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s291/g1729/`.
- The clone is my own (`clone/`). Its push URL is set invalid and it was never pushed. It fetched main and the branch read-only.
- I made three worktrees: `head27` and `mut37` at 2ec69377, and `rone37` at cd019f38. All three are jest slot 17 (band 30880-31519), printed by `worktreeSlot()` in each tree.
- No SEAT kit of 18 or 19 Nov names slot 17 or its band. A program over 149 brief files found only one mention: the finished B1690 gate verdict of 18 Nov. The same program reports slot 13 for the builder's `b1728-nodot/new21` and slot 14 for `b1719-nodot/old15` (controls).
- `node_modules` is an APFS clone copy of the round-1 gate's copy. `package-lock.json` blob 2d7dbece is equal at main and at the head, and `require('sqlite3')` loads.

The lock was acquired once: tag `b1729-gate`, after 0 s, at 10:02:59, through `nexusai-lock.sh jest` with `NEXUSAI_LOCK_BASE=locks-laptop-1017`. It was released at 10:03:40 with lock rc 0. The chain printed `NODE_OPTIONS=[unset]`. The band read 0 listeners before every run and after the last one. Every run had EADDRINUSE 0.

## Findings
| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Observation (hosted, read-only) | Hosted CodeQL on the new head has run. The PR's javascript-typescript analysis at 2ec69377 (created 23:00:36Z, CLI 2.27.4) has **0 results**. Its SARIF has 0 results; the same instrument reads 5 on the cd019f38 PR analysis and 29 on main. Open alerts on `refs/pull/229/head`: **0**. The check run `CodeQL` reads `success`, "No new alerts in code changed by this pull request". However, its `completed_at` (22:58:40Z) is BEFORE the javascript analysis was created, so that check-run row by itself does not prove the javascript result. The analysis count and the alert count do. | At landing, re-read the check run and `mergeable_state`. They read `unstable` at 10:03 AEDT, while hosted Build was still `in_progress`. |
| F2 | Observation | Hosted Build on 2ec69377 read `in_progress` at 10:06:57 AEDT. This gate did not wait for it. | The landing waits for Build to be green, as always. |
| F3 | Minor (builder STATUS text) | The builder's STATUS first line still reads `B1728 STATUS (placeholder, Step 0 running)`, although the file ends `READY B1728: 2ec6937...`. Its Correction 1 (`cd` typed early in the session) is process only and does not affect any result this gate re-measured. | No change needed to land. |

No Blocker, no Major.

## Measured rows
1. **SCOPE.**
   - `ls-remote` (10:01:24): branch 2ec6937792ffc48abbd11a2928b293c954e14cd5, main 37fb1bcbec2e19f2404774633349da76b75120d3. `pulls/229`: open, head 2ec69377, base 37fb1bcb. The compare API for cd019f38...2ec69377 reads `ahead 2, behind 0`, with `__tests__/rd1007-user-add-unparsed-body.test.js +6 -6` and `backend/server.js +4 -1`.
   - `rev-list --left-right --count cd019f38...head` reads 0 2. Against main it reads 0 7. Both `merge-base --is-ancestor` checks (cd019f38 into the head, and main into the head) return rc 0.
   - Commits: 47eedb91 (parent cd019f38) changes only `backend/server.js`, 4/1. 2ec69377 (parent 47eedb91) changes only the rd1007 test, 6/6. Nothing else.
   - Head blobs: server.js 0335a98ea26fc2d70965521cd8738d7f0fb06fce (= Tuesday's reproduced blob); rd1007 499d9675814b40377603e669bc3e8ad1ba894c45. At cd019f38 the blobs are dc23d449 and eb44176c (the round-1 blobs).
   - **A7b equals the kit's frozen hunk by program.** Its removed line equals the kit's (1 line) and its added lines equal the kit's (4 lines).
     - The last added line is main's field read byte for byte, and that text occurs once in main.
     - The early refusal sits exactly 3 lines above that line.
     - From main to the head, the user-add hunk is a pure insertion, `@@ -3606,0 +3616,5 @@`: removed 0, added 5. server.js has 10 hunks from main, as in round 1.
   - Counts in server.js:
     - `if (!isPlainRequestObject(req.body)) {`: 0 at main, 0 at r1, 1 at the head.
     - Main's field read: 1 at main, 0 at r1, 1 at the head.
     - The round-1 ternary read: 0 at the head.
     - The 400 text: 1, 1, 2.
     - `function isPlainRequestObject(`: 1 at each.
     - Non-ASCII characters: 1256 at each.
   - **T7b equals the kit's four replacements by program.** Removed 6 and added 6 lines, all equal to the kit's. Its hunks are `-6,2`, `-119`, `-122,2` and `-125`.
   - **RD-994 block is unchanged.** BEGIN..END is 93 lines, sha256 prefix `f0bc2a77b68d4743` at main, r1, A7b and the head. A control with one changed byte gives b18b9d850b2cb784. The mount count is 1 at each.
   - `merge-tree --write-tree main head` is clean, tree 49793dfa, equal to the head tree. `scripts/verify-expected-counts.json` is unchanged from cd019f38 to the head (diff 0 lines). It reads 6041/382.
2. **BEHAVIOUR.** Runs in my own trees inside the one lock acquisition.
   - Head, rd1007 and rd1005, run 1 and run 2: 2/2 suites and 32/32 cells green each time (rd1007 9, rd1005 23).
   - Head readers, run once: rd969 (11 cells, H8 included) and rd691 (6 cells), 17/17 green.
   - **User add probe: head versus round 1.** I used an untracked probe file (`probes/zz-gate1729-users-probe.test.js`), copied into `head27` and `rone37`. It uses the enforced shape with a seeded administrator and viewer, and reads "stored" from GET users after each request. It sends 13 shapes as the viewer and as the administrator, 26 rows. For **0 of 26 rows** does the status, the full JSON body or the stored flag differ between the two trees.
     - Administrator, merge-patch+json, vnd.api+json, text/plain, no type and no body, JSON with no body, `[]` and `[{...}]`: 400 `Email, name, and password are required`, stored false, at both.
     - JSON `null` and `"x"`: 400 `Invalid request` from the strict JSON parser, at both.
     - Missing name: 400, the same text, stored false.
     - Ordinary JSON add and form add: 200, stored true.
     - Viewer: 403 `Admin access required` for every shape that reaches the route (11 of 13; the parser answers 400 first for `null` and `"x"`, as in round 1), stored false. The administrator check still comes first.
   - **Plants** in `mut37`, content-anchored. Each plant was reverted by blob to 0335a98ea26f (EQUAL, 2 of 2).
     - P7b (the early refusal's three lines removed): rd1007 **R1-R4 RED**, each received `500 "Failed to add user"`. **C1 RED**, received refusal 0. N1-N4 green.
     - P11 (the field read set back to the round-1 ternary, refusal kept): **C1 RED only**, received fields 0. The other 8 are green.
   - The received colours equal the kit's MUTATIONS table and the builder's matrix.
3. **HOSTED RULE, reproduced locally.**
   - Tools: CLI 2.27.4, suite `javascript-security-extended.qls`, `--threads=4`. The drafter's tools were read whole and copied verbatim, with sha256 equal to the kit's (`mkdb.sh` 87a77efa, `analyze.sh` 18416fc0, `cmp.py` 618f76bb, `difffilter.py` 9a6d04c5, `mkdiffpack.py` 1e15c238). `CQ_BASE` was exported to my `cq/`, and the driver's first line names it.
   - Inputs: archives of main, cd019f38 and 2ec69377, with server.js blobs df442bc8, dc23d449 and 0335a98e; none has `node_modules`. The hosted SARIFs were fetched with `gh api -X GET`: main analysis 2198430304 (sha256 a2b1a0ba) and PR analysis 2199861480 (579924d5), both equal to the drafter's.
   - Databases and analyses: rc 0 each, 29 results in each tree.
   - Multiset against hosted main by (rule, file, fingerprint): main, cd019f38 and the head each read **new 0, gone 0**. A control with one perturbed fingerprint reads new 1, gone 1.
   - Fingerprint table, printed by program from the SARIF files:

     | rule | main line:col | main fp | r1 line:col | r1 fp | head line:col | head fp | head = main |
     |---|---|---|---|---|---|---|---|
     | js/http-to-file-access (jsonStorage.js) | 524:34 | 421941c6a9bc55b1:1 | 524:34 | 421941c6a9bc55b1:1 | 524:34 | 421941c6a9bc55b1:1 | True |
     | js/user-controlled-bypass | 3620:13 | 1957a54887b4c6f6:1 | 3631:13 | 1957a54887b4c6f6:1 | 3634:13 | 1957a54887b4c6f6:1 | True |
     | js/user-controlled-bypass | 3609:14 | fb6be83c60b60503:1 | 3620:14 | fb6be83c60b60503:1 | 3623:14 | fb6be83c60b60503:1 | True |
     | js/user-controlled-bypass | 3609:24 | fb6be83c60b60503:1 | 3620:24 | fb6be83c60b60503:1 | 3623:24 | fb6be83c60b60503:1 | True |
     | js/user-controlled-bypass | 3609:33 | fb6be83c60b60503:1 | 3620:33 | fb6be83c60b60503:1 | 3623:33 | fb6be83c60b60503:1 | True |

     The local main tracked rows equal hosted main's.
   - Post-filter (`mkdiffpack.py` ranges from main to the tree; my own re-implementation in `work/fptable.py` agrees with `difffilter.py` on every count):
     - The user-add added range is 3616-3618 at r1 and 3616-3620 at the head.
     - Start-line rule at cd019f38: keeps **5**, equal to hosted PR analysis 2199861480 by (rule, path, line, column, fingerprint). This is the control.
     - Start-line rule at 2ec69377: keeps **0**.
     - Span rule: keeps 7 at cd019f38 and 2 at the head. The 2 are the `js/missing-token-validation` results at server.js 1469 and 1487, which are open on main at 1460 and 1478 under the same fingerprints.
     - At the head, the four bypass results' related locations are 3621 (main's field read, unchanged text) and 3649. Neither is an added line.
   - **What the span residual means for the hosted check.** There is no reason to expect the hosted check to keep these two. Three readings, each measured, say so:
     - (a) The geometry is identical at cd019f38 and the head. In each, the only location that touches the diff is one related location covering the whole user-add handler: it starts at the unchanged line 3606 and ends at 3671 or 3674, and it spans the added lines without starting on one. Hosted had exactly that geometry at cd019f38 and did NOT report them: its 5 results equal the start-line set, not the span set.
     - (b) The CLI's own `codeql/util` `AlertFiltering.qll` (lines 21-25) lets a query restrict itself by span intersection, and lines 17-19 say a query MAY omit, not must. So span is the query-side filter, and the reported set reflects a further start-line step. Hosted output at cd019f38 is the proof of that step, not this file.
     - (c) Directly: the hosted javascript analysis at 2ec69377 reads 0 results and the PR ref has 0 open alerts (F1).

     The residual would matter only if the hosted pipeline changed between the two runs. It did not: the CLI is 2.27.4 in both.
4. **TEXT.** Scanned: the 10 added lines and both commit messages (14 lines).
   - Name scan: 0, using the underscore-aware regex over the standard ban list. Controls: `_by_<name>_` fires for every name, and `Kamikaze` does not.
   - B-number, seat, coordinator and gate ids: 0 (a planted `B1728 and N156` fires).
   - Card and decision ids: 0 (a control fires).
   - Alert numbers (`229`-`235`, `67`, `68`, `#n`): 0 (a control fires).
   - Product-owner attribution: 0.
   - Non-ASCII: 0 (a planted U+202E counts 1). Cf and bidi characters: 0. Dotted quads: 0.
   - Ticket keys: RD-1007 only. No `RegExp(`, `eval(`, `new Function`, `child_process`, `innerHTML`, timer or skip token.
   - Both trailers read `Co-Authored-By: Claude Sonnet 5.5`, the builder's model.
   - Both bodies say, in plain words, that the refusal moved above an unchanged field read and the answers are unchanged.
5. **FULL VERIFY: not re-run.** Row 2 shows no behaviour difference. The builder's claim, read at source in `.tools/b1728/logs/step-p-plain.log`:
   - Tree `49793dfa56c5640b495d010989ee2f3b75baf364` is the head tree; this gate measured it with `rev-parse 2ec69377^{tree}`.
   - `VERDICT: PASS - 6041/6041 tests passed across 382 suites (jest exit 0)`, rc 0, EADDRINUSE 0.
   - The pair 6041/382 equals the committed counts file, which this gate read at the head.

Deploy: unchanged from round 1. The merge touches `backend/**` and `__tests__/**`, so a Deploy demo run will start. Its jobs are gated on `CI_DEPLOY_ENABLED` and must read skipped.

## Builder STATUS claims (graded)
- **True:** commit shas and parents; numstats; both blobs; the kit-equal hunks; RD-994 prefix; the fingerprint table; multiset 0/0; r1 start 5 = hosted; r1 span 7; head start 0; head span 2 (1469, 1487); the related lines 3621 and 3649; rd1007 colours at head (two runs); P7b and P11 received colours; the counts pair; one fast-forward with PR head = 2ec69377.
- **Not re-measured (taken as the builder's, not needed for this delta):** readers 39/725, scanners 71/1308, the red-base and red-r1 runs, P8. This gate's head-versus-r1 probe (row 2) covers the same equivalence directly over HTTP.

## FOUND / TESTED / NOT TESTED / HOW
- FOUND: F1 to F3. No Blocker, no Major.
- TESTED: rows 1 to 4, measured. Row 5 was read and paired.
- NOT TESTED:
  - The full verify (not required: row 2 shows no difference).
  - The 39-file reader and 71-file scanner runs.
  - P8.
  - Hosted Build (in progress).
  - Linux and the production setting.
  - The Deploy demo run.
  - A browser render.
- HOW:
  - `git` read verbs and `merge-tree` in my own clone. `gh api -X GET` only, for compare, pulls, analyses, SARIF, alerts and check-runs.
  - `work/scope.py` and `work/text.py`.
  - `work/chain.sh` under `nexusai-lock.sh jest b1729-gate` with `env -u NODE_OPTIONS`, using `work/plant.js` with content-anchored plants and blob reverts.
  - `work/runcq.sh` (the drafter's tools, verbatim), plus `work/fptable.py` and `work/resid.py`.
  - No `server.js` range was printed. Nothing was pushed or deleted. No PR, alert or ruleset was touched.

# QA gate verdict - Secuura/Blockchain PRs #1737, #1738, #1739

- Tier 2, round 1 of 2. Gate model: Claude Sonnet 5.5 (claude-sonnet-5-5). Date 2026-10-27.
- Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-b3-1027/` (clone in `repo/`, worktrees `wt_dev`, `wt_p1737`, `wt_p1738`, `wt_p1739`, raw logs beside; private `TMPDIR=/tmp/gb3`). Scripts (`*.sh`, `*.cjs`) are in the workspace too.
- Pushed / merged / commented / edited a ticket: nothing. Node v26.8.1.

## BLUF
| PR | Verdict | Worst finding |
|---|---|---|
| #1737 KS-1746 item 5 (Seat R 5th) | GO WITH NOTES | LOW: collides with #1739 on both HTML docs (section 61 vs 62 appended before `</body>`); whichever lands second must be rebased/resolved. All numeric claims reproduced; G2 matched pair reproduced exactly (75/0 vs 72/3, same 3 cells). |
| #1738 KS-1667 (Seat T 4th) | GO | INFO: comment-only proven by my own AST-printer instrument with controls; 1656/1656 across 140 suites both sides; the branch is based on older develop c3eb63c9 (not a develop merge), so a raw `diff develop..head` is polluted by #1734/1735/1736; three-dot diff is clean. |
| #1739 KS-1750 (Seat R 5th) | GO WITH NOTES | LOW: same doc collision with #1737 (section 62). Red arm, refusal control and counts reproduced. INFO: both doc entries stamp "base c3eb63c9d23b" while the head merges develop f3042778. |

Merge: #1738 is clean against everything. **#1737 + #1739 CONFLICT in both HTML docs in either order** (same two files, same insertion point). Resolution keep-both is mechanical and loses nothing (see Merge orders). Trees below.

## Pins (start = end)
```
f3042778cd0ef9a363043c329039853e93b60477  refs/heads/develop
a3d22fd99a1bf2ac12034b875b8fe56c43bf57b8  refs/pull/1737/head
56ddf5d49729072c990c49a20ed286ecfd432294  refs/pull/1738/head
7df12b384e872205ac6489e11aeb30dec9cf24ee  refs/pull/1739/head
```
`lsremote_start.txt` and `lsremote_end.txt` in the workspace; `diff` empty (rc 0); equal to the briefed pins. `gh api user` = `kksecura`; all three PRs read as OPEN / mergeStateStatus UNSTABLE (read-only). The cache `src` clone `git status` is empty; its deploy-key ssh command was copied into my clone's repo-local config for the fetch only.

## #1737 KS-1746 item 5

**FOUND**
- Diff vs develop (head is a merge, parents c5b75d4a + f3042778; develop is its ancestor so the merge drags nothing): exactly 3 files, 106+/2-: `preflight_deps.test.sh` 66+/2-, flow doc +15/-0, cheat sheet +25/-0. `preflight.sh` is not in the diff; its sha256 at head `bae62e73e2b08714...` equals develop's (I printed the first 16 hex of both). No product file touched.
- Test-file changes: new `commented` hook mode in the fixture, a new `STUB-SAW-FAKE` line in the fixture stub, 7 new cells (4 substantive: derived set exactly ALLOW_FORCE, FAKE named nowhere, suite still sees FAKE=1, plus the G2-sensitive green cell; 3 controls: ALLOW_FORCE stripped in same run, FAKE-unset arm green, FAKE-unset probe reads `<unset>`). The comment explains why the unset probe is vacuous, and a cell pins that statement.
- Docs: one hunk each, zero deletions (numstat 0 deleted), pure append before `</body>` (asserted by a script: head text up to `</body>` equals develop's). Tag balance (per-tag open/close counts, whole file) develop vs head: imbalance set empty for all of them.

**TESTED / HOW** (shell, bash 3.2, `TMPDIR=/tmp/gb3`)
- `preflight_deps.test.sh`: develop **68/0** (rc 0) -> head **75/0** (rc 0). Claim holds.
- Other two suites untouched at this head: `pre_push_hook_base` 36/0, unchanged.
- **G2 matched pair** (`g2.sh`): faithful layout copied to `/tmp/gb3/g2ctl` and `/tmp/gb3/g2mut` (`Blockchain/`, `.githooks/`, `systemTest/`, `Projects Documents/` beside each other), `PREFLIGHT_DEPS_TEST_ROOT` pointing at each copy's `Blockchain/Dev`. In the mutant copy I replaced the `grep -vE '^[[:space:]]*#' "$hook_src"` stage at `preflight.sh:722` with `cat "$hook_src"` (anchor asserted to occur exactly once; sha before `bae62e73`, after `b2f1e911`; the real worktree file untouched, `diff` shows the one line).
  - control copy 75/0 rc 0; mutant 72/3 rc 1; cell-by-cell verdict diff (ok/FAIL prefix stripped) moves exactly the summary line and the 3 cells: "derived set is EXACTLY ALLOW_FORCE" (want 1 got 0), "FAKE is named NOWHERE in the strip line" (want 0 got 1), "suite still SEES FAKE=1" (want 1 got 0). Nothing else moved. Claim "72/3, moving exactly my 3 substantive cells" holds.
  - **Survival of the old suite** (control for "no cell could reach it"): develop's `preflight_deps.test.sh` against the same mutant copy = **68/0**. So G2 did survive before, and does not now.
  - Bare copy (no repo layout), as the seat said: 51 passed / 6 failed, i.e. a bare copy does redden unrelated cells (6). Confirms why the faithful layout matters.
- Aggregate `run-shell-suites.sh`: develop (with my `npm ci`) **95/0/1 of 96**, skip = ks949 (no PostgreSQL). #1737 head, in my install-less worktree: **94/0/2 of 96**, the second skip being `preflight_test_types_ratchet_leg` with the printed reason "SKIP - workspace install absent (leg 1 refuses this tree)". That suite alone: develop (install present) 46/0, heads (no install) 27/0. So the 95/0/1 aggregate is reproduced on develop and the head difference is **my environment asymmetry**, not the PR (I did not install in the head worktrees). Claim "95/0/1 of 96" is therefore reproduced as 94/0/2 with a documented cause, not as 95/0/1; fair reading is "not contradicted".

**SEVERITIES**
- LOW: doc collision with #1739 (below).
- INFO: doc stamp "measured at base c3eb63c9d23b" (older than the develop it merges); figures I re-measured at f3042778 agree (68 -> 75), so no figure is wrong.
- INFO: the new probe only works because the caller sets FAKE; documented by the seat and pinned by a cell. No MAJOR/MINOR.

## #1738 KS-1667

**FOUND**
- The head is NOT a develop merge: parent c3eb63c9, which is two develop commits behind f3042778 (it lacks #1735/#1736). `git diff develop head` therefore shows 7 files including reversals of #1734/1735/1736 content; `git diff develop...head` (merge-base c3eb63c9) is exactly **2 files**: `routes/documents.ts` 3+/3-, `ks1662-tenant-predicate-without-rls.integration.test.ts` 4+/4-. No docs touched (the PR makes no doc entry; none needed, no figure moves). The seat's "3435 and 331 lines" net zero: reproduced (3435/3435, 331/331).
- Every changed line is a comment: programmatic filter of `+`/`-` lines not starting with `*`, `//` or `/*` = **0**.
- Citations: `runWithPlatformScope` non-test call sites in originate: `routes/adminConfig.ts` (many) and `services/gdprService.ts` (435, 558, 949, 1348, 1633), definition-only mention in `db.ts`, none in `documents.ts`; the new "adminConfig.ts and gdprService.ts" wording is correct. `tenant-guc.ts:102` is `export function runWithPlatformScope`, `:116` is `tenantGucContext`, `:131` closes it, so `(:116-131)` holds. `039_rls_fail_closed.sql:156-157` = `DROP POLICY IF EXISTS users_auth_lookup` / `CREATE POLICY users_auth_lookup`, so the rescoped "is what created users_auth_lookup" is accurate (the old "is what changed it" was loose).

**TESTED / HOW**
- Instrument (mine, `tok3.cjs`): TypeScript `createSourceFile` + printer with `removeComments`, develop vs head. documents.ts printed 95,047 bytes both, **EQUAL**; ks1662 file 12,341 both, **EQUAL**; parse diagnostics 0 on both sides. Controls run in the same invocation: identifier tamper -> differs (both files); line-comment edit -> equal (both); commenting out an import -> differs (both); real string-literal tamper -> differs (documents.ts). **For ks1662 my string-literal tamper control did not discriminate (printed false: my regex hit a string that is not a printed literal), so that file has 3 working controls, not 4.** Size > 5000 asserted so an empty read cannot pass.
- The seat's byte figures (88,085 / 11,164) come from a different tool (esbuild emit); I did not reproduce those numbers, only the same equality by an independent method.
- originate unit (`npm test` = jest, `services/originate`): develop **140 suites / 1656 tests all passed**, rc 0; with the head's two files overlaid on develop (a `git checkout p1738 -- <2 files>` in my worktree, restored after, `git status` clean) **140 / 1656 passed**, rc 0. Ratios equal both sides; 140/140 suites ran. The overlay equals the post-merge content of those two files because no other PR touches them.
- The ks1662 integration file (not part of `npm test`, needs Postgres): not run, per the brief (no regression claim made).

**SEVERITIES**: INFO only (the stale-base note above).

## #1739 KS-1750

**FOUND**
- Diff vs develop (head is a merge, parents abc1068e + f3042778): exactly 3 files, 67+/0-: `pre_push_hook_base.test.sh` 27+/0-, flow doc +15, cheat sheet +25. All additions in the test file are `#` lines (27 comment lines) inserted between `set -uo pipefail` and the KS-883 block. The warning quotes none of the three graded strings (hits at head: stale 0, replacement 1, anchor 1; develop: stale 0, replacement 1), as claimed.
- Docs: one hunk each, zero deletions, pure append before `</body>`, tag balance empty-imbalance on both. Doc 62.3 says a second grading pair exists (`pre_push_stack_legs_comment.test.sh`); the file exists at head.

**TESTED / HOW** (`red1739.sh`, all arms on COPIES in `/tmp/gb3/r39`, graded with `HOOK_BASE_SUITE=<copy>`, worktree file never edited)
- Grader `pre_push_hook_base_leg_comment.test.sh`: develop **4/0**, head **4/0**, rc 0 both. Subject `pre_push_hook_base.test.sh`: develop **36/0**, head **36/0**, rc 0. Claim holds.
- Control arm (an innocuous extra comment line inserted into the warning block): 4/0, rc 0, so the arm can pass.
- Red arm: warning plus a line quoting the replacement sentence -> **3 passed / 1 failed, rc 1, CELL 2 `hits=2`**. As claimed.
- Extra arms I added: quoting the retired sentence -> CELL 1 red (`hits=1`); quoting the anchor sentence -> CELL 3 red (`hits=2`); each arm 3/1, rc 1, exactly one cell. Refusal control: `HOOK_BASE_SUITE=` (set but empty) -> **rc 2**; nonexistent path -> rc 2.
- Aggregate: see #1737 (94/0/2 in an install-less worktree, same cause).

**SEVERITIES**
- LOW: doc collision with #1737.
- INFO: the warning protects only against edits by readers of the subject file; the graded strings can still be reworded by anyone who does not read it (the PR says it is not loosening the grader, deliberately).
- No MAJOR/MINOR.

## Merge orders (my clone only, `git merge-tree --write-tree` chained with `commit-tree`; `merge_out.txt`, `resolve_out.txt`)
| order | result | tree |
|---|---|---|
| develop + #1737 | clean | 663824fe6e6c9712b192f96d5b1d3105626bd395 |
| develop + #1738 | clean | 17ddf83da96509303d4d3793bd4559d06a835c86 |
| develop + #1739 | clean | d3d8832328f8de5bfb0b40c0e29cd60303ccd243 |
| 1737,1738 = 1738,1737 | clean, one tree | ba68985c4a69c111cb0fb071dbc1a05c679134f8 |
| 1738,1739 = 1739,1738 | clean, one tree | bf9251e5f17c1970cf2a132092289f291e669c47 |
| 1737,1739 | **CONFLICT** rc 1, both HTML docs | - |
| 1739,1737 | **CONFLICT** rc 1, both HTML docs | - |
| every triple (6 orders) | **CONFLICT** wherever 1737 and 1739 meet | - |

**The conflict**: both PRs add their block immediately before the same `</body>` at the same place in `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` (line ~4754) and `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` (line ~4725), so git sees both as inserting at one spot. Content-wise they do not overlap: I verified each PR's change is a pure append before `</body>` with the same unchanged tail, and the resolution (keep both blocks, drop nothing) was built by script, then merged with the rest by `merge-tree`:
| resolution (keep both) | flow-doc headings in file order | cheat-sheet headings | 1737+1739 tree | + #1738 (any triple) |
|---|---|---|---|---|
| 1737 first, then 1739 | `## 61 (KS-1746)` then `## 62 (KS-1750)`: **numbering stays correct** | KS-1746 then KS-1750 | 1288f74311bc583af859efb30faf0e3f46ac1f97 | 3758a6e712502b66b5e0040ce975fbd039a28455 |
| 1739 first, then 1737 (natural append order) | `## 62` appears ABOVE `## 61`: **numbers out of order**, each internally consistent | KS-1750 then KS-1746 | 608c3d06d79b6ad140952735d56d2882f8ff97c8 | d800591e3e41ded5e37fc5da26e00a75b135b0fe |
In each resolved tree the two docs are +30/0 and +50/0 versus develop (15+15 and 25+25, no deletions), so nothing is lost. The numbered flow doc sorts correctly only in the first arrangement; the recommended resolution is the 1737-block-above-1739-block arrangement (tree `1288f743...`, triple `3758a6e7...`) whichever PR merges first. Whichever merges second needs a rebase/merge-from-develop and a keep-both resolution; the cheat sheet has no numbering. #1738 adds nothing to the picture (disjoint files).

## NOT TESTED
- The seat's claim "95/0/1 of 96" at the heads, under an install-complete worktree (I reproduced it on develop; heads gave 94/0/2 for the documented install reason; I did not install in the head worktrees).
- ks1662 integration file (needs Postgres); the seats' esbuild-emit byte counts 88,085 / 11,164.
- Platform suites, lint, Linear states, anything in browsers.
- Whether the merged (resolved) trees pass the suites; I computed trees only, did not run suites on a merged tree.

## My instrument errors
1. `tok.cjs` (TypeScript scanner, no re-scan) first reported documents.ts NOT equal: the scanner mis-tokenised a backtick inside a comment and produced one differing "template" token that contained the changed comment text. The same file under a real parse (`tok2.cjs`: one differing token, parse-confirmed) and under the AST printer (`tok3.cjs`: equal) is equal. I treat the scanner result as an instrument artefact and rely on the printer. I kept the scanner output in `tok_out.txt` for transparency.
2. ks1662 string-literal control (printer instrument) did not discriminate (see #1738).
3. The head worktrees were created without `npm ci`, so the aggregate shell runs there skipped one install-dependent suite (explained above); I should have installed first.
4. The fleet hooks refused `cd`, `git -C $VAR fetch` and a `rm` inside a heredoc; I re-issued as script files with literal paths. No effect on results.

## Files outside the workspace
None written. Writes: the workspace, `/tmp/gb3` (private TMPDIR and mutant/arm copies), and this verdict folder `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-27_gate-b3-batch/`. `find /Volumes/DevMASTER/WEDNESDAY -maxdepth 1 -newer lsremote_start.txt` lists only `.git` (the repo's own, not a root file); no stray file in the WEDNESDAY root.

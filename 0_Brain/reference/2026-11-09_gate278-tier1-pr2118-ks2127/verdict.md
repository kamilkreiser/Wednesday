PR 2118: GO WITH NOTES

# Gate 278, tier 1 (Opus): PR 2118 / KS-2127, the pre-push hook fails safe when its git diff fails

| PR | head | verdict |
|---|---|---|
| 2118 (KS-2127) | 08cf86d0ec5fde3e1d465f9729ce861d270dc534 | **GO WITH NOTES** |

Nothing here needs a ruling from Kam.

**Pins.** I read them through the project remote with its deploy key, at the start (01:32:39Z) and the end (01:43:42Z). develop stayed at `b9fd80eee85b791dfd0e532d23d8f0da9b4f80ea` both times. The PR head (branch `feature/ks-2127-pre-push-hook-a-failing-git-diff-reads-as-no` and `refs/pull/2118/head`) stayed at `08cf86d0ec5fde3e1d465f9729ce861d270dc534` both times. **Neither pin moved.** The PR is one commit on 273de443c30c. The hook blob at 273de443 equals the one at develop b9fd80ee (`0c53e79ea5d5`), so "develop's hook" means the same thing in both. The head's hook blob is `aa389d83008f`.

## BLUF

The fix does what the READY says and nothing more. All three diff sites (head lines 145, 160, 270; develop lines 129, 143, 252) now read the exit status of `git diff`. On failure the new helper `_jr_diff_failed` (head lines 116-123) sets the KS-2127 banner, a `changed` marker and `st_all=1`, and returns from `_judge_ref`. This fails safe, which is the right direction: a change set that cannot be computed now forces the preflight (or the existing not-HEAD refusal) where it used to pass silently.

In a healthy repo, the head's hook behaves byte-identically to develop's on every legitimate push shape I ran (21 shapes under sh, 19 under dash) and on all 264 cells of the 9 existing suites. Pushes change only when a diff fails. In that case the hook used to fail open, and it now runs the preflight with `--all`. A push whose tip is not HEAD is now refused, and that refusal does not say why (G278-1). The docs sentence about tag pushes is wrong in detail (G278-2). No cell pins `st_all=1` (G278-3).

## Findings

**G278-1 · Minor · `.githooks/pre-push` head lines 145 and 160 (stderr discarded), 369-378 (refusal printed before the banner).** MEASURED AT RUNTIME.
- **Behaviour change:** with the fault planted (`diff.orderFile` names a missing file), a push whose tip is not HEAD is now refused rc 1. On develop's hook it passed rc 0. I measured four shapes:
  - a docs-only push to an existing branch;
  - a docs-only branch that tracks `origin/develop`;
  - a docs-only new branch;
  - a tag on a new commit that is not HEAD.

  This is fail-closed and consistent with KS-1483: the change set "cannot be shown not to" touch Blockchain/Dev.
- **The defect:** the refusal never says that the diff failed.
  - The KS-2127 banner is printed only at line 378, after the KS-1483 refusal check at line 369 has already exited.
  - Sites 1 and 2 send git's own error to `2>/dev/null`.
  - So for an existing or tracking branch, the pusher sees only "which changes Blockchain/Dev (or cannot be shown not to), but HEAD is …" and no cause. Site 3 keeps git's stderr, so new-branch and tag pushes do show `fatal: failed to read orderfile …`.
- **Recoverable:** following the printed advice (check out the branch and push again) works. The push then runs the preflight under the KS-2127 banner.
- **Fix shape (owner's call):** when `_jr_banner` is set, print it (or a one-line KS-2127 cause) inside the line 369-375 refusal, or stop discarding stderr at sites 1 and 2. Add a cell that pushes a non-HEAD ref under the fault and asserts rc≠0 and that the output contains `KS-2127`.

**G278-2 · Minor (text a client will read) · both fragments, the READY's NOT COVERED list, and by extension the PR body if it repeats them.** MEASURED AT RUNTIME.
- **What the cheat fragment says:** "A tag push whose diff fails now runs the preflight instead of being skipped as 'nothing new lands'". The flow fragment says the same, minus the quoted phrase.
- **Measured on develop's hook:** under the fault, a tag on a new commit was **not** skipped as `tagnobase` ("nothing new lands"). `_informative=1`, so that note is never reached. The push passed rc 0 silently, after the format gate ran on an empty set.
- **Measured on the head's hook:** the tag push runs the preflight **only when the tag's commit is HEAD**. A tag on a new commit that is not HEAD is **REFUSED** (rc 1, see G278-1).
- **Unaffected:** release tags on commits the remote already has still take `onremote` before any diff, with or without the fault. Tags whose commit every base contains still take `tagnobase` before any diff.
- **Suggested sentence:** "a tag on a new commit whose diff fails used to pass silently; it now runs the preflight if it is HEAD and is refused otherwise."

**G278-3 · Note (test quality) · `Blockchain/Dev/scripts/__tests__/ks2127_pre_push_failing_diff.test.sh`.** MEASURED AT RUNTIME.
- **Gap:** no cell can fail on `st_all`. The stub format gate ignores `--all`.
- **My mutant M3** sets `st_all=0` in the helper: the suite stays 8/8.
- **The behaviour itself is right:** my own probe, whose format-gate stub logs its arguments, shows the head's hook passing `--all` on every fault-path shape (14 of 14).
- **Owner's choice:** a cell asserting `--all` reached the gate.
- **Also survives:** mutant M4 (`continue` in place of `return 0` at site 3) stays 8/8. In practice it is equivalent: a diff failure is repo-wide, so every later ref fails the same way and nothing resets the marker. It is not a finding.

## TESTED / HOW

Instrument: a blobless clone of `Secuura/Distributed_Secuura` at `/private/tmp/g278/repo`, checked out at the PR head, plus worktrees `/private/tmp/g278/wt-develop` (b9fd80ee) and `/private/tmp/g278/wt-merge` (a local probe commit `85aa089ce375` of the merge tree; nothing pushed). I pushed only to local bare fixture remotes; I never ran the hook against the real remote. I used `TMPDIR=/private/tmp/g278/tmp`, so the suites' own `trap rm -rf` cleaned up only their own mktemp directories inside my gate area.

1. **The diff, read whole.** 4 files, +246/-3: the hook (+21 -3, all three sites and the helper), the new suite, and two fragments. The commission describes the change as "+21/-3", but `git diff --stat` reports 24 lines changed (+21 -3 = 24); that is consistent. Line 141 (the force-push merge-base) and lines 283-305 (the tag, KS-882 and KS-854 blocks) are untouched. Lines 369-384 and the `exit 0` at 390 are untouched. I checked the control flow by hand:
   - `var=$(cmd) || {…; return 0; }` takes the status of the command substitution.
   - The return at site 3 leaves `_judge_ref` from inside a `for` loop that is not a subshell.
   - The caller's `while … done <<EOF` is not a subshell either (the existing code already relies on that).
   - The hook has no `set -e`.

2. **Legitimate push shapes, healthy repo** (probe `/private/tmp/g278/probe/shapes.sh`; local bare origin; preflight and format-gate stubs that log). I ran 21 shapes:
   - a new branch (Dev change, docs-only, no new commit);
   - a fast-forward of an existing branch (Dev, docs);
   - a plain push with `-u` upstream;
   - a branch that tracks `origin/develop`;
   - a no-op push (up to date);
   - a delete;
   - a lightweight tag and an annotated tag on a commit the remote has;
   - a tag on a new HEAD commit;
   - a tag on a new commit that is not HEAD;
   - a docs push of a branch that is not HEAD (new, existing, tracking);
   - `HEAD:refs/heads/g`;
   - a two-ref push;
   - a force push (refused);
   - a RED commit (refused);
   - a new branch alongside a local `develop`.

   **develop's hook and the head's hook produced IDENTICAL rc, preflight, refusal, banner and format-gate arguments on every shape.** Two notes on the probe:
   - **Control:** the RED and force-push shapes are refused on both hooks.
   - **Instrument defect, caught and fixed:** my first run committed `.githooks/` through `git add -A`, so the non-HEAD shapes ran with no hook at all. I added `.githooks/` to the fixture's `info/exclude` and reran everything; only the post-fix runs are reported.

3. **The same 21 shapes under the fault.**
   - **develop's hook:** every push passed rc 0 with no preflight, including the RED commit. That is the defect.
   - **head's hook:**
     - the delete, no-op, tags on remote commits, new branch with no new commit, and the force-push refusal are all unchanged;
     - every other shape whose tip is HEAD runs the preflight with the KS-2127 banner and `--all`;
     - the RED commit is refused;
     - the 4 shapes whose tip is not HEAD are refused (G278-1).

4. **Red-proof of the new suite.**
   - develop's hook: 3 passed, 5 failed, and the 5 failures are exactly the fault cells.
   - head's hook: 8/8.
   - I reproduced R's site-3 tamper (back to `|| true`): exactly its 3 cells go red.
   - **My own mutants:**
     - M1 (site 1: the helper runs but no `return`, so line 146 overwrites `changed` with an empty grep) turns exactly the "branch the remote already has" cell red, 7/1.
     - M2 (the same at site 2) turns exactly the upstream cell red, 7/1.
     - M3 and M4 survive (G278-3).

5. **The 9 existing suites.** I ran each suite from its own tree: wt-develop for develop's hook, the clone for the head's hook. The suites are byte-identical between the two (`git diff` shows only the hook and the new suite under `scripts`, `systemTest` and `.githooks`). The tallies are **identical** on both hooks, all rc 0:

   | suite | cells |
   |---|---|
   | pre_push_hook_base | 36 |
   | pre_push_hook_base_fixture_guard | 12 |
   | pre_push_hook_current_develop | 4 |
   | ks998_pre_push_judges_the_push | 80 |
   | ks998_pre_push_stale_base_hint | 21 |
   | ks884_pre_push_tag_named_develop | 10 |
   | pre_push_stack_legs_comment | 4 |
   | preflight_deps | 82 |
   | preflight_gateway_slot | 15 |
   | **total** | **264 passed, 0 failed** |

   R's 264 is confirmed.

6. **Leg 12** (`run-shell-suites.sh --check-unreached`): 124 suites reached at the head, 124 on the merge result, 123 on develop.

7. **POSIX.**
   - `sh -n` (bash 3.2.57, measured) and `dash -n` (`/bin/dash` is present) both return rc 0 on the head's hook. As a positive control, `if then` gives rc 2 under both.
   - **Beyond the commission (this closes R's "dash parsed only"):** I made a copy of each hook with its shebang changed to `#!/bin/dash`. The new suite run against it gives head 8/8 and develop 3/5, the same as sh. All 19 default shapes under dash, healthy and under the fault, matched the sh results line for line. The evidence class is PROBED: dash ran it through the shebang git execs; I did not separately assert the interpreter's identity.

8. **Fragments.** `node Blockchain/Dev/scripts/docs-fragments.mjs check` ends **OK** at the head (224 new) and on the merge result (225 new, which counts both the KS-1972 and the KS-2127 fragments). The two `ADVISORY … line 6249/6235` lines also appear on develop, so they are not introduced by this PR. The fragment content is true except for the tag sentence (G278-2). The flow fragment's "The new-branch site keeps its stderr" is true, and that is exactly why G278-1 bites only at sites 1 and 2.

9. **Merge tree on b9fd80eee85b.** `git merge-tree --write-tree` returns rc 0 and tree `32c483d2ce6eec7c256a052b0e6eec60d6d6eb0f`. The diff from develop to that tree is exactly the PR's 4 paths, and its hook blob is `aa389d83008f`, the same as the head's.

10. **Open-PR overlap.** I had no gh login: the project's gh config says "not logged in". As the proxy for open PRs I used the 49 PRs that have a `refs/pull/N/merge` ref at the remote; 2118 itself has one, and R counted 46 open. **Overlap with the 4 paths: only 2118 itself, which is the self-control.** I also planted a control: I added a path from PR 1129 (`5_Project_History/history.md`) to the needle list, and it was detected.

    A wider net over all 1,283 unmerged remote branches found 9 older branches that touch `.githooks/pre-push` (PRs 903, 1189, 1190, 1247, 1474, 1532, 1540, 1545, 1577). None of them has a merge ref, so they are presumably closed or squash-merged. I could not confirm their state without the API, but none of them is in the merge-ref set.

## NOT TESTED

- **The ticket comment 8d3c3eff and the PR body:** I have no Linear or GitHub API read here. I checked the commit message (likely the PR body's source); its claims are true apart from the tag sentence, which the commit message does not contain.
- **Other ways a diff can fail:** I planted only the `diff.orderFile` shape. The fix keys on the exit status, so any failure takes the same path. R's "other failing-diff shapes" is not a finding.
- **Partial or tree-less clones** where the diff needs a lazy fetch: my probe was inconclusive (its control was invalid), so I report it as not measured.
- **R's push receipt** (driver 70615, 1077 s) and the full leg-14 replica: not re-run.
- **Open state of the 9 older hook branches:** not confirmed through the API (see item 10).

## R's NOT COVERED list

- **Other failing-diff shapes:** not a finding (see above).
- **"dash parsed only":** now RUN by this gate, under dash, and clean (TESTED 7).
- **"A tag push whose diff fails now runs the preflight; no cell":** partly inaccurate. It runs the preflight only when the tag is HEAD and is refused otherwise. That is G278-2 (Minor, the text) and part of G278-1 (Minor, the silent refusal).

## Conduct

- I was findings-only. I wrote only this verdict, the probe script `/private/tmp/g278/probe/shapes.sh` and its outputs, and everything else under `/private/tmp/g278`.
- In the `!CODING` checkout I used only read verbs: `remote -v`, `config --get`, `cat-file`, `status`. I did not fetch there; its status shows 18 pre-existing entries, which I did not touch.
- All write verbs (clone, checkout, worktree add, commit-tree, merge-tree) ran in `/private/tmp/g278`.
- I pushed only to local bare fixtures. I posted, mailed and commented nothing, and deleted nothing.
- **Clone left in place, as the commission says (no rm): `/private/tmp/g278` = 1.3 GB on the boot volume** (the clone plus 2 worktrees plus fixtures).
- load1 peaked at 7.74, at my start and before I ran anything, and stayed between 4.2 and 6.6 while I worked.
- The common rules file says to remove the clone. This commission says not to (no rm), and the narrower, newer instruction is the one I followed.
- The READY cites no decision-queue card, so I read none.
